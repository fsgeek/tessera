#!/usr/bin/env bash
# Slot-2 policy signer: reproducible deployment (prototype/policy-signer/DESIGN.md, owner decisions 2026-10-14).
# Instrument code under A9.2. Idempotent: every step checks for the resource first.
#
#   prototype/policy-signer/deploy.sh all            # everything below, in order
#   prototype/policy-signer/deploy.sh vendor-check   # signer/p8_codec.py still equals the gen.py ranges
#   prototype/policy-signer/deploy.sh <step>         # apis | sas | keyiam | registry | build | queues | role |
#                                                    # job | scheduler | harden | run-now
#
# Uses ONLY the AWS profile `tessera` (account 477139661040, us-east-2) and GCP project `tessera-slot2` (us-east1).
# Creates no static credentials: no AWS access keys, no GCP service-account keys. The signer reaches SQS by
# AssumeRoleWithWebIdentity with a Google-issued ID token for its own service account. Teardown: RESOURCES.md.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
AWS="$HOME/.local/bin/aws --profile tessera --region us-east-2"
GC="$HOME/.local/bin/gcloud --project=tessera-slot2 --quiet"
ACCOUNT=477139661040
PROJECT=tessera-slot2
PROJECT_NUMBER=990386490765
REGION=us-east1
KEYRING=tessera-v1
KEY=slot2-spike
KEY_VERSION="projects/$PROJECT/locations/$REGION/keyRings/$KEYRING/cryptoKeys/$KEY/cryptoKeyVersions/1"
KEY_CREATED=1791946553        # slot2-spike v1 createTime (prototype/spike-pq/out-gcp/capture.json), bound into KEY_FP
KEY_FP=gpg-sha256:b6e37f7c8120ca19cca86cc9617d4ec50b2875a799ee976d9d0253e01c7a077c
ALLOWED_ALGS=KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256   # the hybrid pair id (the branch under test)

SIGNER_SA=slot2-signer@$PROJECT.iam.gserviceaccount.com      # runtime: KMS sign + view public key, on slot2-spike only
INVOKER_SA=slot2-invoker@$PROJECT.iam.gserviceaccount.com    # Cloud Scheduler: run.invoker on the job only
BUILDER_SA=slot2-builder@$PROJECT.iam.gserviceaccount.com    # Cloud Build: push to the repo only
REPO=slot2
IMAGE_BASE="$REGION-docker.pkg.dev/$PROJECT/$REPO/signer"
SRC_BUCKET=gs://tessera-slot2-build-src
JOB=slot2-signer
SCHED=slot2-signer-tick

REQ_Q=tessera-slot2-requests
RESP_Q=tessera-slot2-responses
ROLE=tessera-slot2-signer-sqs
AUDIENCE=tessera-slot2-sqs     # the ID token's requested audience (aws trust condition accounts.google.com:oaud)

say() { printf '\n== %s\n' "$*"; }

vendor_check() {
  say "vendor-check: signer/p8_codec.py vs formal/p8/vectors/gen.py"
  local gen="$ROOT/formal/p8/vectors/gen.py" ven="$HERE/signer/p8_codec.py"
  diff <(sed -n 41,477p "$gen"; echo; sed -n 620,658p "$gen"; echo; sed -n 732,751p "$gen") \
       <(sed -n '/^# ---- gen.py 41-477 ----$/,$p' "$ven" | grep -v '^# ---- gen.py ') \
    && echo "vendored ranges identical"
}

apis() {
  say "enable APIs"
  $GC services enable run.googleapis.com cloudscheduler.googleapis.com artifactregistry.googleapis.com \
    cloudbuild.googleapis.com iamcredentials.googleapis.com sts.googleapis.com iam.googleapis.com
}

sas() {
  say "service accounts (no keys are ever created for them)"
  for sa in slot2-signer:"Slot-2 policy signer runtime" slot2-invoker:"Slot-2 scheduler invoker" \
            slot2-builder:"Slot-2 image builder"; do
    name=${sa%%:*}; desc=${sa#*:}
    $GC iam service-accounts describe "$name@$PROJECT.iam.gserviceaccount.com" >/dev/null 2>&1 \
      || $GC iam service-accounts create "$name" --display-name="$desc"
  done
}

keyiam() {
  say "key IAM: slot2-signer gets cloudkms.signer + cloudkms.publicKeyViewer on $KEY only"
  for role in roles/cloudkms.signer roles/cloudkms.publicKeyViewer; do
    $GC kms keys add-iam-policy-binding $KEY --keyring=$KEYRING --location=$REGION \
      --member="serviceAccount:$SIGNER_SA" --role=$role >/dev/null
  done
  $GC kms keys get-iam-policy $KEY --keyring=$KEYRING --location=$REGION
}

registry() {
  say "artifact registry repo + source bucket for the builder"
  $GC artifacts repositories describe $REPO --location=$REGION >/dev/null 2>&1 \
    || $GC artifacts repositories create $REPO --location=$REGION --repository-format=docker \
         --description="slot-2 policy signer images"
  $GC artifacts repositories add-iam-policy-binding $REPO --location=$REGION \
    --member="serviceAccount:$BUILDER_SA" --role=roles/artifactregistry.writer >/dev/null
  $HOME/.local/bin/gcloud --project=$PROJECT storage buckets describe $SRC_BUCKET >/dev/null 2>&1 \
    || $HOME/.local/bin/gcloud --project=$PROJECT storage buckets create $SRC_BUCKET --location=$REGION \
         --uniform-bucket-level-access --public-access-prevention
  local lc; lc="$(mktemp)"; echo '{"rule":[{"action":{"type":"Delete"},"condition":{"age":7}}]}' > "$lc"
  $HOME/.local/bin/gcloud --project=$PROJECT storage buckets update $SRC_BUCKET --lifecycle-file="$lc" >/dev/null
  rm -f -- "$lc"
  $HOME/.local/bin/gcloud --project=$PROJECT storage buckets add-iam-policy-binding $SRC_BUCKET \
    --member="serviceAccount:$BUILDER_SA" --role=roles/storage.objectViewer >/dev/null
  # Cloud Build with a user-specified service account and CLOUD_LOGGING_ONLY needs log writing.
  $GC projects add-iam-policy-binding $PROJECT --member="serviceAccount:$BUILDER_SA" \
    --role=roles/logging.logWriter --condition=None >/dev/null
}

build() {
  say "build the signer image (Cloud Build, builder SA)"
  local tag; tag="$(cat "$HERE"/signer/{Dockerfile,requirements.txt,main.py,p8_codec.py} | sha256sum | cut -c1-16)"
  $GC builds submit "$HERE/signer" --region=$REGION --config="$HERE/signer/cloudbuild.yaml" \
    --substitutions=_IMAGE="$IMAGE_BASE:$tag" \
    --service-account="projects/$PROJECT/serviceAccounts/$BUILDER_SA" \
    --gcs-source-staging-dir="$SRC_BUCKET/source"
  $GC artifacts docker images describe "$IMAGE_BASE:$tag" --format='value(image_summary.digest)' \
    > "$HERE/.image-digest"
  echo "image: $IMAGE_BASE@$(cat "$HERE/.image-digest")"
}

queues() {
  say "SQS queues (us-east-2)"
  for q in $REQ_Q $RESP_Q; do
    $AWS sqs create-queue --queue-name $q --tags project=tessera,purpose=slot2-policy-signer \
      --attributes MessageRetentionPeriod=86400,VisibilityTimeout=60,SqsManagedSseEnabled=true \
      --query QueueUrl --output text
  done
}

signer_uid() { $GC iam service-accounts describe "$SIGNER_SA" --format='value(uniqueId)'; }

role() {
  say "IAM role $ROLE: web identity (accounts.google.com), only the signer service account"
  local uid; uid="$(signer_uid)"
  local reqarn="arn:aws:sqs:us-east-2:$ACCOUNT:$REQ_Q" resparn="arn:aws:sqs:us-east-2:$ACCOUNT:$RESP_Q"
  local trust; trust=$(cat <<EOF
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Federated":"accounts.google.com"},
 "Action":"sts:AssumeRoleWithWebIdentity",
 "Condition":{"StringEquals":{"accounts.google.com:sub":"$uid","accounts.google.com:aud":"$uid",
                              "accounts.google.com:oaud":"$AUDIENCE"}}}]}
EOF
)
  local perms; perms=$(cat <<EOF
{"Version":"2012-10-17","Statement":[
 {"Sid":"PullRequests","Effect":"Allow","Action":["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:ChangeMessageVisibility"],"Resource":"$reqarn"},
 {"Sid":"PushResponses","Effect":"Allow","Action":["sqs:SendMessage"],"Resource":"$resparn"}]}
EOF
)
  if $AWS iam get-role --role-name $ROLE >/dev/null 2>&1; then
    $AWS iam update-assume-role-policy --role-name $ROLE --policy-document "$trust"
  else
    $AWS iam create-role --role-name $ROLE --assume-role-policy-document "$trust" --max-session-duration 3600 \
      --description "Slot-2 policy signer (GCP tessera-slot2 SA slot2-signer) queue access" \
      --tags Key=project,Value=tessera Key=purpose,Value=slot2-policy-signer --query Role.Arn --output text
  fi
  $AWS iam put-role-policy --role-name $ROLE --policy-name slot2-queues --policy-document "$perms"
}

job() {
  say "Cloud Run job $JOB (a job, not a service: no endpoint)"
  local digest; digest="$(cat "$HERE/.image-digest")"
  local env="REQUEST_QUEUE_URL=https://sqs.us-east-2.amazonaws.com/$ACCOUNT/$REQ_Q"
  env+=",RESPONSE_QUEUE_URL=https://sqs.us-east-2.amazonaws.com/$ACCOUNT/$RESP_Q"
  env+=",AWS_ROLE_ARN=arn:aws:iam::$ACCOUNT:role/$ROLE,AWS_AUDIENCE=$AUDIENCE,AWS_REGION_QUEUES=us-east-2"
  env+=",KMS_KEY_VERSION=$KEY_VERSION,KEY_CREATED=$KEY_CREATED,KEY_FP=$KEY_FP,ALLOWED_ALGS=$ALLOWED_ALGS"
  env+=",SIGNER_IMAGE=$IMAGE_BASE@$digest,RUN_SECONDS=40"
  $GC run jobs deploy $JOB --region=$REGION --image="$IMAGE_BASE@$digest" --service-account="$SIGNER_SA" \
    --set-env-vars="$env" --tasks=1 --parallelism=1 --max-retries=0 --task-timeout=120s \
    --cpu=1 --memory=512Mi --labels=project=tessera,purpose=slot2-policy-signer
  $GC run jobs add-iam-policy-binding $JOB --region=$REGION \
    --member="serviceAccount:$INVOKER_SA" --role=roles/run.invoker >/dev/null
}

scheduler() {
  say "Cloud Scheduler $SCHED: every minute, runs the job as $INVOKER_SA (OAuth)"
  local uri="https://run.googleapis.com/v2/projects/$PROJECT/locations/$REGION/jobs/$JOB:run"
  if $GC scheduler jobs describe $SCHED --location=$REGION >/dev/null 2>&1; then
    $GC scheduler jobs update http $SCHED --location=$REGION --schedule="* * * * *" --uri="$uri" \
      --http-method=POST --oauth-service-account-email="$INVOKER_SA"
  else
    $GC scheduler jobs create http $SCHED --location=$REGION --schedule="* * * * *" --uri="$uri" \
      --http-method=POST --oauth-service-account-email="$INVOKER_SA" --time-zone=UTC \
      --attempt-deadline=60s
  fi
}

harden() {
  say "remove project-level grants that enabling the APIs created automatically"
  # Enabling run/cloudbuild created the Compute default SA with roles/editor (which carries iam.serviceAccounts.actAs
  # and run.jobs.update: an indirect path to slot2-spike through the job) and the legacy Cloud Build SA with
  # roles/cloudbuild.builds.builder. Nothing here runs as either. Remove both bindings; RESOURCES.md has the restore.
  $GC projects remove-iam-policy-binding $PROJECT --condition=None \
    --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role=roles/editor >/dev/null || true
  $GC projects remove-iam-policy-binding $PROJECT --condition=None \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role=roles/cloudbuild.builds.builder >/dev/null || true
  $GC projects get-iam-policy $PROJECT --format=json
}

run_now() { $GC run jobs execute $JOB --region=$REGION --wait; }

case "${1:-}" in
  all) vendor_check; apis; sas; keyiam; registry; build; queues; role; job; scheduler; harden ;;
  vendor-check) vendor_check ;;
  apis|sas|keyiam|registry|build|queues|role|job|scheduler|harden) "$1" ;;
  run-now) run_now ;;
  *) echo "usage: $0 all|vendor-check|apis|sas|keyiam|registry|build|queues|role|job|scheduler|harden|run-now"; exit 2 ;;
esac

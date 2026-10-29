#!/usr/bin/env bash
# Tessera V1 slot-2 policy signer: deployment (service/signer-gcp/README.md "Deploy"). OWNER DRAFT: not yet run.
# Idempotent: every step checks for the resource first. Run the steps one at a time, in the order README.md "Deploy"
# gives: `terraform apply` for the issuer falls between `role` and `job`, so there is no `all`.
#
#   service/signer-gcp/deploy.sh <step>
#     sas | role | keyiam | registry | build | job | run-now | scheduler | harden | retire-instrument
#
# Inputs (environment), needed by `job` and `role`:
#   REQUEST_QUEUE_URL, RESPONSE_QUEUE_URL   terraform output signer_queues (the "gpg" entry), service/issuer/infra
#   FRAME_BUCKET                            terraform output result_bucket
#   SIGN_UNTIL                              the window's signing stop: issuance-not-after minus 96 h, YYYY-MM-DDTHH:MM:SSZ
#
# Scopes: GCP project tessera-slot2 (us-east1) and AWS account 477139661040 (profile tessera, us-east-2) only. Creates
# no static credential: no AWS access keys and no GCP service-account keys. The signer reaches AWS by
# AssumeRoleWithWebIdentity with a Google-issued ID token for its own service account, then AssumeRole into the
# issuer's Terraform signer role (tessera-v1-issuer-signer-gpg), whose principal is the federated role made here.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE="$(cd "$HERE/.." && pwd)"
AWS="$HOME/.local/bin/aws --profile tessera --region us-east-2"
GCLOUD="$HOME/.local/bin/gcloud"
GC="$GCLOUD --project=tessera-slot2 --quiet"
ACCOUNT=477139661040
PROJECT=tessera-slot2
PROJECT_NUMBER=990386490765
REGION=us-east1
KEYRING=tessera-v1
# Production key (service/issuer/DEPLOY.md "Keys"): a NEW HSM key, never the spike key, which the hybrid
# registration commits to deleting (formal/p8/HYBRID-SUPPLEMENT.md §11 item 6). No key defaults: set SLOT2_KEY, SLOT2_KEY_CREATED and SLOT2_KEY_FP (the version defaults to 1).
KEY="${SLOT2_KEY:-}"                # the production key's name in $KEYRING
KEY_VERSION_N="${SLOT2_KEY_VERSION:-1}"
KEY_CREATED="${SLOT2_KEY_CREATED:-}" # that version's createTime (epoch seconds), bound into KEY_FP
KEY_FP="${SLOT2_KEY_FP:-}"           # gpg-sha256:... of the v4 public-key packet built with KEY_CREATED
KEY_VERSION="projects/$PROJECT/locations/$REGION/keyRings/$KEYRING/cryptoKeys/$KEY/cryptoKeyVersions/$KEY_VERSION_N"
SPIKE_KEY=slot2-spike               # the 2026-10-14 instrument's key: only retire-instrument touches it

SIGNER_SA=tessera-signer-gpg@$PROJECT.iam.gserviceaccount.com     # runtime: KMS sign + view public key, on $KEY only
INVOKER_SA=tessera-signer-invoker@$PROJECT.iam.gserviceaccount.com # Cloud Scheduler: run.invoker on the job only
BUILDER_SA=slot2-builder@$PROJECT.iam.gserviceaccount.com          # Cloud Build: push to the repo only (exists)
REPO=tessera-signer
IMAGE_BASE="$REGION-docker.pkg.dev/$PROJECT/$REPO/signer-gpg"
SRC_BUCKET=gs://tessera-slot2-build-src                            # exists (7-day lifecycle, builder read only)
JOB=tessera-signer-gpg
SCHED=tessera-signer-gpg-tick

ISSUER_SIGNER_ROLE=tessera-v1-issuer-signer-gpg                    # made by service/issuer/infra (signer_principals)
FED_ROLE=tessera-v1-signer-gpg-federated                           # made here; the gpg entry of signer_principals
AUDIENCE=tessera-v1-signer-gpg                                     # the ID token's audience (trust condition oaud)

say() { printf '\n== %s\n' "$*"; }
need() { [ -n "${!1:-}" ] || { echo "$1 is not set (see the header of $0)"; exit 2; }; }

sas() {
  say "service accounts (no keys are ever created for them)"
  for sa in tessera-signer-gpg:"Tessera V1 slot-2 signer runtime" tessera-signer-invoker:"Tessera V1 slot-2 signer scheduler"; do
    name=${sa%%:*}; desc=${sa#*:}
    $GC iam service-accounts describe "$name@$PROJECT.iam.gserviceaccount.com" >/dev/null 2>&1 \
      || $GC iam service-accounts create "$name" --display-name="$desc"
  done
}

need_key() { for v in SLOT2_KEY SLOT2_KEY_CREATED SLOT2_KEY_FP; do need $v; done
  [ "$KEY" != "$SPIKE_KEY" ] || { echo "SLOT2_KEY is the spike key; V1 uses a new production key"; exit 2; }; }

keyiam() {
  need_key
  say "key IAM: $SIGNER_SA gets cloudkms.signer + cloudkms.publicKeyViewer on $KEY only"
  for role in roles/cloudkms.signer roles/cloudkms.publicKeyViewer; do
    $GC kms keys add-iam-policy-binding $KEY --keyring=$KEYRING --location=$REGION \
      --member="serviceAccount:$SIGNER_SA" --role=$role >/dev/null
  done
  $GC kms keys get-iam-policy $KEY --keyring=$KEYRING --location=$REGION
}

registry() {
  say "artifact registry repo $REPO (builder may push)"
  $GC artifacts repositories describe $REPO --location=$REGION >/dev/null 2>&1 \
    || $GC artifacts repositories create $REPO --location=$REGION --repository-format=docker \
         --description="Tessera V1 slot-2 signer images"
  $GC artifacts repositories add-iam-policy-binding $REPO --location=$REGION \
    --member="serviceAccount:$BUILDER_SA" --role=roles/artifactregistry.writer >/dev/null
}

build() {
  say "stage signer-gcp + verifier, build the image (Cloud Build, builder SA)"
  local ctx; ctx="$(mktemp -d)"
  mkdir -p "$ctx/signer-gcp" "$ctx/verifier"
  cp "$HERE"/{Dockerfile,requirements.txt,pyproject.toml,cloudbuild.yaml} "$ctx/signer-gcp/"
  cp -r "$HERE/tessera_signer" "$ctx/signer-gcp/"
  cp "$SERVICE/verifier/pyproject.toml" "$ctx/verifier/"
  cp -r "$SERVICE/verifier/tessera_verify" "$ctx/verifier/"
  find "$ctx" -name __pycache__ -type d -prune -exec rm -r -- {} +
  printf '__pycache__/\n' > "$ctx/.gcloudignore"
  local tag; tag="$(cd "$ctx" && find . -type f ! -name .gcloudignore -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-16)"
  $GC builds submit "$ctx" --region=$REGION --config="$ctx/signer-gcp/cloudbuild.yaml" \
    --substitutions=_IMAGE="$IMAGE_BASE:$tag" \
    --service-account="projects/$PROJECT/serviceAccounts/$BUILDER_SA" \
    --gcs-source-staging-dir="$SRC_BUCKET/source"
  rm -rf -- "${ctx:?}"
  $GC artifacts docker images describe "$IMAGE_BASE:$tag" --format='value(image_summary.digest)' > "$HERE/.image-digest"
  echo "image: $IMAGE_BASE@$(cat "$HERE/.image-digest")"
}

signer_uid() { $GC iam service-accounts describe "$SIGNER_SA" --format='value(uniqueId)'; }

role() {
  say "AWS role $FED_ROLE: web identity (accounts.google.com), only $SIGNER_SA; may only assume $ISSUER_SIGNER_ROLE"
  local uid; uid="$(signer_uid)"
  local trust; trust=$(cat <<EOF
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Federated":"accounts.google.com"},
 "Action":"sts:AssumeRoleWithWebIdentity",
 "Condition":{"StringEquals":{"accounts.google.com:sub":"$uid","accounts.google.com:aud":"$uid",
                              "accounts.google.com:oaud":"$AUDIENCE"}}}]}
EOF
)
  local perms; perms=$(cat <<EOF
{"Version":"2012-10-17","Statement":[{"Sid":"ChainToIssuerSignerRole","Effect":"Allow","Action":"sts:AssumeRole",
 "Resource":"arn:aws:iam::$ACCOUNT:role/$ISSUER_SIGNER_ROLE"}]}
EOF
)
  if $AWS iam get-role --role-name $FED_ROLE >/dev/null 2>&1; then
    $AWS iam update-assume-role-policy --role-name $FED_ROLE --policy-document "$trust"
  else
    $AWS iam create-role --role-name $FED_ROLE --assume-role-policy-document "$trust" --max-session-duration 3600 \
      --description "Tessera V1 slot-2 signer (GCP $SIGNER_SA): web identity, chains to $ISSUER_SIGNER_ROLE" \
      --tags Key=project,Value=tessera Key=purpose,Value=signer-gpg --query Role.Arn --output text
  fi
  $AWS iam put-role-policy --role-name $FED_ROLE --policy-name chain-to-issuer-signer --policy-document "$perms"
  echo "set signer_principals = { gpg = \"arn:aws:iam::$ACCOUNT:role/$FED_ROLE\" } in the issuer's tfvars"
}

job() {
  need_key
  need REQUEST_QUEUE_URL; need RESPONSE_QUEUE_URL; need FRAME_BUCKET; need SIGN_UNTIL
  say "Cloud Run job $JOB (a job, not a service: no endpoint)"
  local digest; digest="$(cat "$HERE/.image-digest")"
  local env="REQUEST_QUEUE_URL=$REQUEST_QUEUE_URL,RESPONSE_QUEUE_URL=$RESPONSE_QUEUE_URL,FRAME_BUCKET=$FRAME_BUCKET"
  env+=",AWS_ROLE_ARN=arn:aws:iam::$ACCOUNT:role/$FED_ROLE,AWS_AUDIENCE=$AUDIENCE,AWS_REGION_QUEUES=us-east-2"
  env+=",AWS_CHAIN_ROLE_ARN=arn:aws:iam::$ACCOUNT:role/$ISSUER_SIGNER_ROLE"
  env+=",KMS_KEY_VERSION=$KEY_VERSION,KEY_CREATED=$KEY_CREATED,KEY_FP=$KEY_FP,SIGN_UNTIL=$SIGN_UNTIL"
  env+=",SIGNER_IMAGE=$IMAGE_BASE@$digest,RUN_SECONDS=40,WAIT_SECONDS=5,VISIBILITY_SECONDS=120"
  $GC run jobs deploy $JOB --region=$REGION --image="$IMAGE_BASE@$digest" --service-account="$SIGNER_SA" \
    --set-env-vars="$env" --tasks=1 --parallelism=1 --max-retries=0 --task-timeout=150s \
    --cpu=1 --memory=512Mi --labels=project=tessera,purpose=signer-gpg
  $GC run jobs add-iam-policy-binding $JOB --region=$REGION \
    --member="serviceAccount:$INVOKER_SA" --role=roles/run.invoker >/dev/null
}

scheduler() {
  say "Cloud Scheduler $SCHED: every minute, runs the job as $INVOKER_SA (OAuth); E-01: keep it running while signing is possible"
  local uri="https://run.googleapis.com/v2/projects/$PROJECT/locations/$REGION/jobs/$JOB:run"
  if $GC scheduler jobs describe $SCHED --location=$REGION >/dev/null 2>&1; then
    $GC scheduler jobs update http $SCHED --location=$REGION --schedule="* * * * *" --uri="$uri" \
      --http-method=POST --oauth-service-account-email="$INVOKER_SA"
  else
    $GC scheduler jobs create http $SCHED --location=$REGION --schedule="* * * * *" --uri="$uri" \
      --http-method=POST --oauth-service-account-email="$INVOKER_SA" --time-zone=UTC --attempt-deadline=60s
  fi
}

harden() {
  need_key
  say "check: no project-level grant that can change the job or the key (the 2026-10-14 removals still hold)"
  $GC projects remove-iam-policy-binding $PROJECT --condition=None \
    --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role=roles/editor >/dev/null 2>&1 || true
  $GC projects remove-iam-policy-binding $PROJECT --condition=None \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role=roles/cloudbuild.builds.builder >/dev/null 2>&1 || true
  $GC projects get-iam-policy $PROJECT --format=json
  $GC kms keys get-iam-policy $KEY --keyring=$KEYRING --location=$REGION --format=json
}

OLD_SA=slot2-signer@$PROJECT.iam.gserviceaccount.com              # the 2026-10-14 instrument's runtime account

# SG-03: absent is the only tolerated failure. gone CMD... succeeds iff CMD reports that the thing does not exist.
gone() { local out; if out=$("$@" 2>&1); then return 1; fi; grep -qiE 'not.?found|cannot find|does not exist' <<<"$out"; }
die() { echo "retire-instrument: $*" >&2; exit 1; }

retire_instrument() {
  say "retire the 2026-10-14 instrument: its job reads another queue and can also cause $SPIKE_KEY signatures"
  gone $GC scheduler jobs describe slot2-signer-tick --location=$REGION \
    || $GC scheduler jobs delete slot2-signer-tick --location=$REGION
  gone $GC run jobs describe slot2-signer --region=$REGION || $GC run jobs delete slot2-signer --region=$REGION
  for role in roles/cloudkms.signer roles/cloudkms.publicKeyViewer; do
    if $GC kms keys get-iam-policy $SPIKE_KEY --keyring=$KEYRING --location=$REGION --format=json | grep -q "$OLD_SA"; then
      $GC kms keys remove-iam-policy-binding $SPIKE_KEY --keyring=$KEYRING --location=$REGION \
        --member="serviceAccount:$OLD_SA" --role=$role >/dev/null
    fi
  done
  # Disabling the account ends every route through it at once, including grants inherited from the project.
  gone $GC iam service-accounts describe "$OLD_SA" || $GC iam service-accounts disable "$OLD_SA"

  say "verify: nothing of the instrument can still sign"
  gone $GC scheduler jobs describe slot2-signer-tick --location=$REGION || die "scheduler slot2-signer-tick remains"
  gone $GC run jobs describe slot2-signer --region=$REGION || die "job slot2-signer remains"
  ! $GC kms keys get-iam-policy $SPIKE_KEY --keyring=$KEYRING --location=$REGION --format=json | grep -q "$OLD_SA" \
    || die "$OLD_SA still bound on $SPIKE_KEY"
  ! $GC projects get-iam-policy $PROJECT --format=json | grep -q "$OLD_SA" || die "$OLD_SA still bound on $PROJECT"
  gone $GC iam service-accounts describe "$OLD_SA" \
    || [ "$($GC iam service-accounts describe "$OLD_SA" --format='value(disabled)')" = "True" ] \
    || die "$OLD_SA is not disabled"
  say "instrument retired and verified"
}

run_now() { $GC run jobs execute $JOB --region=$REGION --wait; }

case "${1:-}" in
  sas|keyiam|registry|build|role|job|scheduler|harden) "$1" ;;
  run-now) run_now ;;
  retire-instrument) retire_instrument ;;
  *) echo "usage: $0 sas|role|keyiam|registry|build|job|run-now|scheduler|harden|retire-instrument"; exit 2 ;;
esac

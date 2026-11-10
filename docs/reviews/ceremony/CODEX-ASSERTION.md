# Key-assertion signing review — Codex, 2026-11-10

Reviewed checkout `7e664ae572a248e53c1a97dd456645731bb0811c`, against `BRIEF-ASSERTION.md`. Findings only; no implementation edits. Severity describes the consequence under the scenario stated, not evidence that it has occurred.

## CA-01 — HIGH: message-controlled terminal output can misrepresent the value being signed

**Lines:** `docs/ceremony/sign-assertion.sh:28–50`, especially 30 and 42–43; `docs/ceremony/ASSERTION-SHEET.md:43–45`.

The script sends every payload byte directly to the terminal before validation. Its Python check finds exactly one LF-delimited line beginning `v=tessera1;`, checks only that line's length, and recomputes the tree. It does not constrain other message lines, prohibit escape sequences or CR, enforce the value grammar, or limit message/line length. The profile leaves the commit message uninterpreted, so a malicious message need not be rejected later.

**Concrete failing scenario:** a requester supplies a commit whose tree correctly binds canonical value A. After its ordinary message/value line, append `ESC[2J ESC[H` followed by `Reviewed value: ` and a different canonical-looking value B. The clear-screen/home sequences can erase A from the terminal display and replace it with B. The B line does not begin `v=tessera1;`, so the script still selects only A, recomputes A's tree and prints `MATCH`. The operator can approve B while signing a tree for A. The owner-provided payload checksum authenticates these misleading bytes; it does not make their rendering safe. This assumes a malicious or mistaken payload is accepted by the requester/owner channel, not modification of the checked script.

**Reproduced:** ran the script's exact embedded Python against a normal build and against the appended escape-sequence payload: both exited 0 with `MATCH`. Separate CR-containing and 10,000-character extra-line variants also passed. Signed the escape-sequence payload using an isolated P-256 software key and assembled it successfully; the recovered signed payload was byte-identical. Terminal escape execution itself was not exercised on Tails; the probe establishes that the dangerous bytes reach `cat` and survive all checked grammar/signature steps. For an immutable payload, recomputation does bind the *selected raw 255-byte line* to the tree, subject to SHA-1; it does not bind the operator's visual reading to that line.

## CA-02 — MEDIUM: assembly accepts any supplied P-256 key as “the repository root”

**Lines:** `service/issuer/tools/key_assertion.py:77–92`, especially 84 and 91–92; compare `docs/ceremony/sign-assertion.sh:9,58–61`.

Assembly verifies under the public key passed through `--root-pub`, computes its fingerprint, and prints a root-authentication PASS without comparing that fingerprint to `6BDA21559F18D5DB8E1312C363210B5FF92AD30A` or an independently pinned repository entry.

**Concrete failing scenario:** an assembler receives a replacement `root.pub.asc` and a detached signature produced by that replacement key. Assembly writes the commit and stamp input and calls it signed by the repository root. A relying-party verifier pinned to the actual root cannot authenticate it (`GIT_SIGNER_NOT_CONFIGURED`, absent another matching entry). This does not bypass the Tails script's card fingerprint gate; it means assembly is not an independent check that the returned evidence came from that gate.

**Reproduced:** a fresh isolated GnuPG nistp256 signing key, fingerprint `08F970C50D942FA08E6C55EFFBC6BC0E9CF861A2`, received that PASS. Its normal binary detached signature used SHA-256, included a valid CRC armor line and passed `dearmor`/rule O. The normal assembled commit had the prescribed header order/set, exact unsigned-payload round-trip, message trailing LF, and no trailing LF in the reconstructed armor. No author/committer identity or timestamp rejection was found: the builder's values are nonempty, and §15.4 deliberately does not interpret them. These results establish normal syntax and supplied-key signature compatibility, not pinned-root acceptance.

## CA-03 — MEDIUM: the local checks omit the required SHA-1 collision detector

**Lines:** `service/issuer/tools/key_assertion.py:33–40,48,67–88`; `docs/ceremony/sign-assertion.sh:44–49`; `service/issuer/tessera_issue/window.py:83–99`. Requirement: V1-PROFILE §15.4 “Ids”.

The builder and Tails recomputation use ordinary `hashlib.sha1`. Assembly imports `object_id` and `verify_path`, whose implementation likewise uses ordinary SHA-1; it never calls the pinned SHA-1DC detector. `window.py` also checks linkage without collision detection. The full verifier performs this separately in `service/verifier/tessera_verify/verify.py:264–270`; importing its git helper functions does not run that check.

**Concrete failing scenario:** run assembly on a host without the pinned SHA-1DC installation. An otherwise valid software-signed build still receives PASS, although full verification on an unconfigured host refuses with `SHA1DC_UNAVAILABLE`. If a presented object triggers the detector, these local checks would not reject it as `GIT_SHA1_COLLISION`, while the full verifier would. No collision-bearing, profile-conforming assertion was constructed in this review; this is a missing mandatory check, not a demonstrated SHA-1 substitution attack.

The normal object framing and lowercase commit-id-plus-LF stamp input agree with §15.4/§6.3. Full profile acceptance still requires the detector and subsequent authority/anchor checks. `window.py` is explicitly only a self-consistency loader: it neither validates signature armor/mathematics nor establishes k = 6. A separate probe using byte-consistent stand-in keys loaded a window with invalid armor, empty trust configuration and a pending-only OTS proof. Thus loader acceptance cannot supply those missing checks. The build does not supply an OTS proof or complete window JSON; compatible keys, dates and a proof digest for the **signed** commit must be supplied before loading. The runbook §5's validated k = 6 proof and later receipt height remain separate issuance duties.

## CA-04 — MEDIUM: the procedure does not disclose that the fingerprints are requester assertions

**Lines:** `service/issuer/tools/key_assertion.py:27–29`; `docs/ceremony/ASSERTION-SHEET.md:3–4,11,43–45`; `docs/ceremony/sign-assertion.sh:28,53`.

The fingerprints are constants attributed to the production-key record, supplied through the NUC/requester workflow. The sheet asks the operator to recognize abbreviated prefixes and owner-supplied dates. Neither the sheet nor the signing prompt plainly says that the root ceremony does not independently authenticate the service keys or their custody. The display/recompute step checks linkage, not the origin or operational use of either key.

**Concrete failing scenario:** a compromised NUC/requester substitutes fingerprints of attacker-controlled service keys and supplies matching payload/checksum/expected values. Even a fully repaired terminal display would show exactly what the root signs, and tree recomputation would succeed. If the operator accepts those requester-supplied values, the root signs the substitution. An expected prefix alone also cannot identify the full fingerprint. This is a trust-boundary failure scenario; no compromise or matching-prefix key generation is claimed.

The signature establishes that the root signing key signed the exact unsigned commit bytes, including its tree reference and message; authenticated object linkage binds that tree to the assertion value. With an independently trusted root pin, this is the root's authorization of those fingerprints and dates. It does **not** independently establish possession of the service private keys, their HSM/KMS identity, custody or isolation, use by the deployed service, DNS publication, or chain pre-commitment. It also does not authenticate the historical trust configuration that supplies the root pin. The existing procedure says the NUC built the commit but does not state these limitations or name an independent basis for approving the complete fingerprints.

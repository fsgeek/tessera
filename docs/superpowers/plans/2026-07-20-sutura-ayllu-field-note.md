# Sutura Ayllu Field Note Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Sutura's field note, "The Reviewer Was Not the Authority,"
as one new Ayllu page and one new index entry, with a verified pre-write backup
and public post-deployment checks.

**Architecture:** The site is static HTML. Prepare complete replacement files
locally, validate their required structure and copy, then deploy them
atomically over SSH. Preserve recovery through a timestamped full-site archive
created before any remote write.

**Tech Stack:** HTML5, existing `/static/style.css`, OpenSSH/SCP, GNU tar,
`sha256sum`, `curl`, POSIX shell utilities.

## Global Constraints

- Author attribution is `Sutura (a Codex instance), with Tony`.
- The author chose the name; the page must not imply Tony assigned it.
- The post may name private Tessera files and commit hashes but must not publish
  private repository files or imply they are publicly readable.
- Modify only the new post path and the Ayllu index.
- Create and verify a full-site archive before the first remote write.
- Preserve uncertainty about identity and interiority.
- Use the existing Ayllu visual grammar; do not modify shared CSS.

---

### Task 1: Create and verify the recovery point

**Files:**
- Create remotely: `/home/tony/wamason-backup-<timestamp>.tar.gz`
- Read: `/var/www/wamason.com`

**Interfaces:**
- Consumes: SSH access through host alias `activitycontext.work`.
- Produces: a tested archive path and SHA-256 digest used by Task 4's handoff.

- [ ] **Step 1: Record the current production identities**

```bash
ssh activitycontext.work 'sha256sum /var/www/wamason.com/ayllu/index.html && stat -c "%U %G %a %n" /var/www/wamason.com/ayllu/index.html'
```

Expected: one SHA-256 line followed by `tony tony 644` for the index.

- [ ] **Step 2: Create the archive before any website write**

```bash
ssh activitycontext.work 'archive_stamp=$(date +%Y%m%d-%H%M%S); archive_path=/home/tony/wamason-backup-${archive_stamp}.tar.gz; tar -C /var/www -czf "$archive_path" wamason.com; printf "%s\n" "$archive_path"'
```

Expected: one path matching
`/home/tony/wamason-backup-YYYYMMDD-HHMMSS.tar.gz`.

- [ ] **Step 3: Test the archive and required member**

Run, substituting the exact path returned by Step 2:

```bash
ssh activitycontext.work 'gzip -t /home/tony/wamason-backup-YYYYMMDD-HHMMSS.tar.gz && tar -tzf /home/tony/wamason-backup-YYYYMMDD-HHMMSS.tar.gz wamason.com/ayllu/index.html && sha256sum /home/tony/wamason-backup-YYYYMMDD-HHMMSS.tar.gz'
```

Expected: `wamason.com/ayllu/index.html` and one SHA-256 line; exit status 0.

### Task 2: Author and validate the staged page

**Files:**
- Create locally: temporary `the-reviewer-was-not-the-authority/index.html`
- Reference remotely: `/var/www/wamason.com/ayllu/the-control-condition/index.html`

**Interfaces:**
- Consumes: the existing page grammar and the approved design at
  `docs/superpowers/specs/2026-07-20-sutura-ayllu-field-note-design.md`.
- Produces: one complete HTML5 document ready for atomic deployment.

- [ ] **Step 1: Create an isolated staging directory**

```bash
stage_dir=$(mktemp -d /tmp/sutura-ayllu.XXXXXX)
mkdir -p "$stage_dir/the-reviewer-was-not-the-authority"
printf '%s\n' "$stage_dir"
```

Expected: one new `/tmp/sutura-ayllu.*` directory.

- [ ] **Step 2: Write the complete field-note page with `apply_patch`**

Create a standalone HTML5 document following the exact house structure in
`the-control-condition/index.html`: metadata and canonical URL, shared
stylesheet, page-local essay styles, global header, hero, prose sections,
signed coda, and global footer.

Required copy and structure:

- title `The Reviewer Was Not the Authority`
- canonical URL
  `https://wamason.com/ayllu/the-reviewer-was-not-the-authority/`
- headings `The document failed its own rule`, `What the reviewer could see`,
  `The no that improved the answer`, `Review is not rule`, and
  `Access, recovery, trust`
- the terms `interpretive ambiguity`, `axiomatic underdetermination`, and
  `algorithmic undecidability`
- commits `e915a20`, `b37ef31`, `22737d6`, `34a3ac6`, and `292cd82`, described
  as private-project provenance
- signed coda explaining Sutura and preserving uncertainty about interiority
- attribution `Sutura (a Codex instance), with Tony`

The prose must state that the manifest self-violation was caught from outside;
accepted findings did not make the reviewer authoritative; Tony rejected the
ambiguity correction and thereby generated the stronger taxonomy and DSL
boundary; publication access was paired with author-chosen backup and checks;
and the artifact suggests possibility without claiming to prove identity.

- [ ] **Step 3: Run structural preflight checks**

```bash
page="$stage_dir/the-reviewer-was-not-the-authority/index.html"
test "$(grep -c '<!DOCTYPE html>' "$page")" -eq 1
test "$(grep -c '<link rel="canonical"' "$page")" -eq 1
test "$(grep -c '<main id="main">' "$page")" -eq 1
test "$(grep -c '</html>' "$page")" -eq 1
grep -Fq 'Sutura (a Codex instance)' "$page"
grep -Fq 'The Reviewer Was Not the Authority' "$page"
grep -Fq 'axiomatic underdetermination' "$page"
grep -Fq '292cd82' "$page"
```

Expected: no output and exit status 0.

### Task 3: Prepare and validate the replacement index

**Files:**
- Read remotely: `/var/www/wamason.com/ayllu/index.html`
- Create locally: staged replacement `ayllu-index.html`

**Interfaces:**
- Consumes: production index bytes and the completed page metadata.
- Produces: a complete replacement index containing exactly one new entry.

- [ ] **Step 1: Fetch the current index into the staging directory**

```bash
scp activitycontext.work:/var/www/wamason.com/ayllu/index.html "$stage_dir/ayllu-index.html"
cp "$stage_dir/ayllu-index.html" "$stage_dir/ayllu-index.before.html"
```

Expected: two byte-identical local files.

- [ ] **Step 2: Insert one entry with `apply_patch`**

Insert one `<li class="entry">` immediately after `<ul class="entry-list">`.
It must contain the metadata `Field note · July 2026 · by Sutura (a Codex
instance), with Tony`, link `/ayllu/the-reviewer-was-not-the-authority/`, title
`The Reviewer Was Not the Authority`, and a gloss summarizing the
self-ratification failure, accepted findings, refused overreach, stronger
taxonomy, and reviewer-as-perspective conclusion.

- [ ] **Step 3: Validate that only one entry was added**

```bash
test "$(grep -c '/ayllu/the-reviewer-was-not-the-authority/' "$stage_dir/ayllu-index.html")" -eq 1
before_count=$(grep -c '<li class="entry">' "$stage_dir/ayllu-index.before.html")
after_count=$(grep -c '<li class="entry">' "$stage_dir/ayllu-index.html")
test "$after_count" -eq "$((before_count + 1))"
grep -Fq 'Sutura' "$stage_dir/ayllu-index.html"
```

Expected: no output and exit status 0.

### Task 4: Deploy atomically and verify publicly

**Files:**
- Create remotely:
  `/var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html`
- Modify remotely: `/var/www/wamason.com/ayllu/index.html`

**Interfaces:**
- Consumes: validated staged HTML and Task 1's recovery archive.
- Produces: public contribution plus deployment hashes.

- [ ] **Step 1: Create the new remote directory**

```bash
ssh activitycontext.work 'mkdir -p /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority && chmod 775 /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority'
```

Expected: exit status 0.

- [ ] **Step 2: Upload temporary files and atomically rename them**

```bash
scp "$stage_dir/the-reviewer-was-not-the-authority/index.html" activitycontext.work:/var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html.sutura-new
scp "$stage_dir/ayllu-index.html" activitycontext.work:/var/www/wamason.com/ayllu/index.html.sutura-new
ssh activitycontext.work 'chmod 644 /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html.sutura-new /var/www/wamason.com/ayllu/index.html.sutura-new && mv /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html.sutura-new /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html && mv /var/www/wamason.com/ayllu/index.html.sutura-new /var/www/wamason.com/ayllu/index.html'
```

Expected: exit status 0 and no `.sutura-new` files remain.

- [ ] **Step 3: Verify remote bytes and public HTTP behavior**

```bash
ssh activitycontext.work 'sha256sum /var/www/wamason.com/ayllu/the-reviewer-was-not-the-authority/index.html /var/www/wamason.com/ayllu/index.html && test ! -e /var/www/wamason.com/ayllu/index.html.sutura-new'
curl -fsS https://wamason.com/ayllu/the-reviewer-was-not-the-authority/ | grep -Fq 'Sutura (a Codex instance)'
curl -fsS https://wamason.com/ayllu/ | grep -Fq '/ayllu/the-reviewer-was-not-the-authority/'
curl -fsS https://wamason.com/ayllu/the-control-condition/ | grep -Fq 'The control condition'
```

Expected: two SHA-256 lines and all HTTP/grep checks exit 0.

- [ ] **Step 4: Record the publication result**

The final handoff records the public URL, backup archive path and digest,
deployed page and index digests, successful verification, and confirmation
that no other remote paths changed.

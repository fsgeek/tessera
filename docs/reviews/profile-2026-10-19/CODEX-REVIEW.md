**13 findings: 2 HIGH, 7 MEDIUM, 4 LOW.** I reviewed all changed passages against the full current files. The supplied diff matches the current three-file diff against `8ea8bfa`. No files were edited.

**PR-01 — HIGH — The unconditional UTC reading survives A10’s correction.**

Locations: [V1-PROFILE.md:1202](/home/tony/projects/tessera/docs/V1-PROFILE.md:1202), [V1-PROFILE.md:1211](/home/tony/projects/tessera/docs/V1-PROFILE.md:1211), [PROOF.md:444](/home/tony/projects/tessera/formal/p8/PROOF.md:444).

The scenario table still tells readers to accept “presented … by T” and “existed by T.” The proof additionally says that a signature first produced “after T” cannot fit the anchor. A backward-skewed header permits precisely that in UTC: signing can occur after the header’s nominal time but before mining.

Governing text: [A10:244](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:244) explicitly corrects these uses, including this witness; [A10:737](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:737) supplies the replacements. [V1-CONTRACT.md:29](/home/tony/projects/tessera/docs/V1-CONTRACT.md:29) correctly separates block existence from conditional UTC existence.

**Replacement:** In scenarios a/g and i, replace “by T” with “before the selected Bitcoin block was mined; its header time T is not a UTC upper bound.” In Theorem (iv)(d), replace every before/after/by-T assertion with the corresponding relation to mining of the selected inclusion block. Keep any UTC claim separate and conditional on A-UTC.

This is a retained defect, already identified by the Levadura disposition, rather than a newly introduced sentence.

**PR-02 — HIGH — The release’s source-commit binding is circular.**

Location: [V1-PROFILE.md:1848](/home/tony/projects/tessera/docs/V1-PROFILE.md:1848).

R1 requires every archive part, including `RELEASE.json`, to be a tracked blob at one named source commit, with nothing generated during assembly. R2 requires that file to contain `source_commit` ([line 1860](/home/tony/projects/tessera/docs/V1-PROFILE.md:1860)). On the natural reading, the commit contains a file naming that same commit’s hash. Constructing it requires a Git-hash fixed point.

Governing requirement: [A10:631](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:631) requires approval bound to the exact archive, not this circular construction.

**Replacement:** “Every part except `RELEASE.json` is copied from the named source commit. `RELEASE.json` is generated deterministically from those bytes and the declared release metadata; `source_commit` identifies their source commit. The independent assembler reproduces the complete archive, including that generated manifest.”

**PR-03 — MEDIUM — UTC output presence at dispatch has two rules.**

Locations: [V1-PROFILE.md:309](/home/tony/projects/tessera/docs/V1-PROFILE.md:309), [line 979](/home/tony/projects/tessera/docs/V1-PROFILE.md:979).

Both require the object only on reports reached *after dispatch*. Conversely, [line 1312](/home/tony/projects/tessera/docs/V1-PROFILE.md:1312) says the wrapper is “always present,” and the null rule explicitly includes D1–D4. Implementers can therefore either omit the object or emit its null-bound form for `OUT_OF_PROFILE`.

Governing text: [A10:300](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:300).

**Replacement:** “Every receipt-verdict report, including a D1–D4 terminal report, contains `utc_assessment`. For D1–D4 its `utc_upper_bound` is null. Startup refusals produce no receipt-verdict report.”

**PR-04 — MEDIUM — `gpgv` success does not enforce R3’s signature format.**

Location: [V1-PROFILE.md:1890](/home/tony/projects/tessera/docs/V1-PROFILE.md:1890).

“Accept iff” `gpgv` exits zero conflicts with R3’s requirement for exactly one binary rule-O packet ([line 1884](/home/tony/projects/tessera/docs/V1-PROFILE.md:1884)); rule O rejects new-format headers and multiple packets ([ENCODING-V1.md:484](/home/tony/projects/tessera/formal/p8/ENCODING-V1.md:484)).

I reproduced zero exit status for both a new-format-header version of a valid signature and two concatenated valid signatures. GnuPG also explicitly supports armored detached signatures. [GnuPG documentation](https://www.gnupg.org/documentation/manuals/gnupg/gpgv.html)

**Replacement:** “Accept only if a trusted acquisition-side checker first validates exactly one unarmored signature against rule O’s grammar and §8 policy, confirms the authenticated primary-key identity, and the pinned `gpgv` verifies the exact archive bytes. Installation then requires R2’s equalities.”

The checker must be available before executing the acquired archive.

**PR-05 — MEDIUM — Rotation and recovery contradict the bootstrap-only acceptance rule.**

Locations: [V1-PROFILE.md:1924](/home/tony/projects/tessera/docs/V1-PROFILE.md:1924), [line 1936](/home/tony/projects/tessera/docs/V1-PROFILE.md:1936).

R5 says fingerprints arriving with releases authenticate nothing, but rotation authenticates the successor through a release. R3 refers only to the production key obtained through R5. Finally, recovery permits a replacement bootstrap, whereas §5 says a new release key is introduced *only* by the current key ([line 422](/home/tony/projects/tessera/docs/V1-PROFILE.md:422)).

The independence requirement remains [A9:326](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:326), supplemented by [A10:624](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:624).

**Replacement:** “Initial bootstrap authenticates the first production key. A successor is authenticated by a conforming release verified under the currently authenticated key and naming the successor fingerprint; subsequently acquired successor key material must match that fingerprint. Loss recovery starts a separately authenticated release lineage and does not establish continuity with the old lineage.”

Apply that distinction to §5 and R3 too.

**PR-06 — MEDIUM — The frozen custody record selects a spike key and requires future edits.**

Location: [V1-PROFILE.md:1004](/home/tony/projects/tessera/docs/V1-PROFILE.md:1004).

The record names `slot2-spike/.../1`, then requires a dated entry *in this record* before any other version signs a shipped receipt. That ties production key replacement to modifying a frozen spec text. It also leaves the spike key as the apparent default production key.

Conflicting registered text: [HYBRID-SUPPLEMENT.md:525](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:525) directs deletion of both spike keys after the reviewed recapture. [A9:375](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:375) requires the custody-implementation choice in the profile; authority comes from key publication.

**Replacement:** “These identifiers describe the historical deployed-slot evidence, not production-key selection. Production key versions and dated replacements are recorded in an external custody record before use. They retain the selected, deadline-qualified custody implementation and obey A9.6’s issuance and successor-registration requirements. The frozen profile is unchanged.”

**PR-07 — MEDIUM — The new substitution summary incorrectly covers possession signatures.**

Location: [V1-PROFILE.md:1310](/home/tony/projects/tessera/docs/V1-PROFILE.md:1310).

“A substituted or non-verifying signature that is present gives INVALID” follows a discussion including `possession.<slot>`. But another valid possession signature over the same manifest can pass: those signature bytes are not committed by `A_sig`. The profile explicitly recognizes possession-signature malleation at [line 1160](/home/tony/projects/tessera/docs/V1-PROFILE.md:1160). Unsupported algorithms also make signature semantics unperformable, rather than necessarily invalid ([line 1050](/home/tony/projects/tessera/docs/V1-PROFILE.md:1050)).

Registered anchor scope: [A9:290](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:290).

**Replacement:** “Changing a committed receipt-signature byte without a matching anchor fails the anchor check. For supported algorithms, a present signature that fails verification contributes INVALID. Replacing a possession signature with another policy-conforming valid signature over the same manifest is permitted. Unsupported-algorithm semantics remain unperformable.”

**PR-08 — MEDIUM — The archival inventory has not been reconciled with the governing texts and repaired proof.**

Locations: [V1-PROFILE.md:1400](/home/tony/projects/tessera/docs/V1-PROFILE.md:1400), [line 1810](/home/tony/projects/tessera/docs/V1-PROFILE.md:1810).

The freeze additions account for edited ENC and the registration hash, but §15.8’s stated spec inventory still names profile, ENC, supplement and A9. It does not require A10 or the current repaired `PROOF.md`. Its “complete archival spec” assertion at [line 1825](/home/tony/projects/tessera/docs/V1-PROFILE.md:1825) consequently remains underspecified.

A10 now supplies governing replacements and output requirements; [A10:639](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:639) also requires its custody-procedure contents frozen. The supplement’s proof hash is the older baseline ([HYBRID-SUPPLEMENT.md:454](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:454)).

**Replacement:** Explicitly require the signed A10 bytes and current repaired proof in the frozen inventory, or require a separately bound archival object carrying them. State exactly where the current proof hash is recorded. Keep resulting object hashes outside included parts.

**PR-09 — MEDIUM — KSK overlap does not guarantee acceptance throughout the real UTC switch day.**

Location: [V1-PROFILE.md:573](/home/tony/projects/tessera/docs/V1-PROFILE.md:573).

The new paragraph concludes that a genuine snapshot anchored “at any time on 2026-10-11” has an eligible candidate. A genuine KSK-2024 snapshot mined that day can have a backward-skewed `T_snap` before midnight, preceding both its policy start and RRSIG inception. Overlapping reliance periods do not prevent that rejection.

Conflicting rules: [V1-PROFILE.md:943](/home/tony/projects/tessera/docs/V1-PROFILE.md:943), [A10:237](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:237).

**Replacement:** “For `T_snap` values whose encoded date is 2026-10-11, the KSK reliance intervals overlap. Acceptance additionally requires a validating RRSIG whose window contains `T_snap`. This does not guarantee acceptance of every snapshot mined during that real UTC day.”

**PR-10 — LOW — The new null-digest exception uses a different criterion from the schema.**

Location: [V1-PROFILE.md:1695](/home/tony/projects/tessera/docs/V1-PROFILE.md:1695).

The schema permits null where canonical bytes do not exist ([line 1688](/home/tony/projects/tessera/docs/V1-PROFILE.md:1688)); the addition permits it where bytes are not redistributable. Those conditions differ. The IEEE entry says the document was not fetched ([gen_manifest.py:220](/home/tony/projects/tessera/formal/dependency-sources/gen_manifest.py:220)).

**Replacement:** “`digest_sha256` is null when exact source bytes were not obtained, with that limitation and its reason stated in `retrieval`. Redistribution restrictions alone do not require a null digest.”

**PR-11 — LOW — §14.2 still presents release custody as a freeze prerequisite.**

Location: [V1-PROFILE.md:1348](/home/tony/projects/tessera/docs/V1-PROFILE.md:1348), especially item 1 at [line 1355](/home/tony/projects/tessera/docs/V1-PROFILE.md:1355).

The heading and introduction say every listed act is needed before 30 October. The new §5 and R1–R6 correctly defer custody execution.

Governing text: [A10:635](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:635).

**Replacement:** Rename the section “Freeze requirements and deferred release gates”; split item 1 into required frozen contents and execution required before the first public release.

**PR-12 — LOW — Several status references remain stale after their adjoining resolutions.**

Locations and replacements:

- [V1-PROFILE.md:44](/home/tony/projects/tessera/docs/V1-PROFILE.md:44), also the opening status: replace A9 “PROPOSED” with its signing-commit status. Evidence: [HYBRID-REGISTRATION-RECORD.md:3](/home/tony/projects/tessera/formal/p8/HYBRID-REGISTRATION-RECORD.md:3).
- [V1-PROFILE.md:1268](/home/tony/projects/tessera/docs/V1-PROFILE.md:1268): replace “The ENC remark is stale” with “Corrected 2026-10-19,” pointing to [ENCODING-V1.md:177](/home/tony/projects/tessera/formal/p8/ENCODING-V1.md:177).
- [V1-PROFILE.md:1148](/home/tony/projects/tessera/docs/V1-PROFILE.md:1148): replace the assertion that editions and digests are not supplied with the actual remaining review/freeze work; the preceding new paragraphs reference the built manifest.
- [V1-PROFILE.md:1895](/home/tony/projects/tessera/docs/V1-PROFILE.md:1895): either remove “R3/R6 have not yet fixed” the version or explicitly mark the preceding 2.4.4 pin provisional. It currently says both.

**PR-13 — LOW — The exponent-repair justification has the wrong logical connective.**

Location: [PROOF.md:542](/home/tony/projects/tessera/formal/p8/PROOF.md:542).

“No nonzero such literal is finite **or** nonzero as a double” is false: huge negative exponents round to finite zero; huge positive exponents overflow to nonzero infinity.

Conflicting number conditions: [ENCODING-V1.md:150](/home/tony/projects/tessera/formal/p8/ENCODING-V1.md:150).

**Replacement:** “Within the payload-size bound, no nonzero literal with such an exponent rounds to a finite, nonzero binary64 value; zero-valued literals are handled separately.”

Validation performed: baseline and hybrid P8 vector checks passed, as did all six repair regression tests. Both archived KSK tags and DS digests reproduced; CMS verification succeeded with the archived CA, retaining its acknowledged bootstrap limitation. I did not rerun the full fuzz campaigns or formal models. The three-file diff remained unchanged.



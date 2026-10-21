# Which conformance files enter the frozen vectors object

OWNER 2026-10-19, profile section 14.2 item 8 (the inventory the freeze record must publish, section 15.8
"Inventory"). Rules used: section 15.8 (the vectors object holds every file under `formal/p8/vectors/` plus the
non-P8 conformance vectors, RES section L; tracked regular-file blob bytes from the named freeze commit; the vectors
may embed the spec hash, the spec never embeds the vectors' hash; hashes live outside the object) and A9.2 (the
exit gate lists golden and rejection vectors for `A_sig`, `ISSUANCE_WINDOW` / `DNS_WINDOW_LENGTH` vectors, the
strict correct-form rows; instrument outputs are never evidence for a C-row).

## The constraint that decides it (EA-10)

Every bundle case carries the vectors object it was issued against: the bundle's `vectors` binary and the signed
`vectors_sha256` (A9.1 mapping, row 8.4), and the case's `release.json` embeds the catalog, which holds
`vectors_sha256` (and, for the 19 hybrid and authority-isolation cases, the case's own `catalog.json`). Checked
2026-10-19 over the regenerated tree: all 344 `release.json` and all 19 `catalog.json` contain the TEST vectors,
spec, preamble or dependency hash; every `bundle.json` (342) embeds the TEST objects. A file that embeds the hash
of the object that contains it cannot be a part of that object. So the bundles, releases and catalogs are
**outputs of a vectors object, not parts of it**.

## Enters the vectors object (as parts)

Inputs and expectations that embed no object hash, and the sources that regenerate the rest deterministically
(REPORT.md "Determinism"):

| Group | Files | Count | Why |
|---|---|---|---|
| Expectations, all groups | `cases/<id>/expected.json` | 352 | The vectors proper: for each case the stable six (`verdict`, `reason`, `T`, ...), the `ambiguous_fields`, and where present `utc_assessment`. No hash or key embedded. A relying-party or second verifier needs these to judge a run. |
| Index | `cases-index.json` | 1 | The inventory of cases by group, expected outcome and installation (RES section L coverage map). |
| Release checker (group "release checker", L-53 to L-56) | `cases/<id>/previous.json`, `next.json`, `expected.json` | 8 cases | Pure data (two trust configs, ACCEPT or REJECT). Embed no object hash. Verbatim parts. |
| Large-case inputs | `bundle.recipe.json` (2), `base.json` (2), `request.txt` (1) under `L-02`, `L-02b`, `L-06` | 5 | The recipe for the 2^27 + 1 byte bundle and the degraded-request flag. Small, hash-free. |
| Generator sources | `cases.py`, `issue.py`, `universe.py`, `tcrypto.py` | 4 | Reissue every bundle, release and catalog against any object triple: the TEST stand-ins now, the real objects at freeze. Without them the 344 bundle cases are not reproducible from the object. They embed the stand-in object bytes as labelled TEST constants. |
| Runner | `run.py` | 1 | Defines how `expected.json` is compared (six fields, `utc_assessment` beside, not inside; ambiguity marking). A vector without its comparison rule is ambiguous. |

Together with `formal/p8/vectors/*` (golden, reject, hybrid-golden, hybrid-reject, `check.py`, `gen.py`,
`fuzz.py`, `test_check.py`, per 15.8), this gives the A9.2 items: the `A_sig` codec vectors (P8 side), and the
`ISSUANCE_WINDOW`, `DNS_WINDOW_LENGTH`, anchored-versus-unanchored, root-KSK rollover, hybrid-routing and
authority-isolation expectations (conformance side).

`selfcheck.py` and `REPORT.md` are documentation and instrument checks; they stay out (below).

## Instrument-only (not parts of the vectors object)

| Files | Count | Why |
|---|---|---|
| `cases/<id>/bundle.json` | 342 | Embed the vectors object (see the constraint). Regenerated per object triple; shipped as a TEST artifact next to the freeze record, not hashed into it. |
| `cases/<id>/release.json`, `trust.json` | 344 each | TEST release record (signed by the TEST release key) and the TEST trust config. A TEST release is never authority for a production verifier (profile 15.9). |
| `cases/<id>/catalog.json`, `universe-catalog.json`, `universe-catalog-hybrid.json`, `universe-release-key.json` | 19 + 3 | TEST catalog and key stand-ins; the frozen catalog is a separate freeze-record object. They now carry `utc_delta_s = 7200` and `utc_m = 6` (profile section 13, note 15). |
| `selfcheck.py`, `REPORT.md`, `VECTORS-OBJECT.md`, `__pycache__` | - | Construction check and prose; not vectors. Cited, not hashed. |
| `prototype/differential/results*.json` | 7 | Run records (run 7, 352/352 AGREE, 2026-10-19). Evidence of an agreement run, not a vector. |

The P8 codec tie vectors (N-01..N-22, C-N01..C-N22) are not conformance bundle cases; they stay in
`formal/p8/vectors/golden.json` (REPORT.md "Not built" 3).

## Not in the object because not built

L-94 and F04 "mixed": see the OWNER 2026-10-19 dispositions in `REPORT.md`. The inventory lists them as absent
by disposition, not as omitted files.

## What the freeze assembly still has to do (not done here)

1. The part set above is path-sorted and fixed by the freeze commit; the assembler and an independent byte-agreement
   check (15.8) run over tracked blobs only. Today the 10 `UTC-*` case directories, `results-run6.json` and the
   regenerated `release.json` / `catalog.json` files are untracked or modified; the files in the table above must
   be committed first. (Case files total 1,422; 1,382 tracked before this change.)
2. The generator takes the object triple from `universe.py` stand-ins. At freeze it must take the real spec, vectors
   preamble and dependency hashes, but the real vectors hash depends on this object's bytes. Order: hash the object
   (the parts above), record it outside the object, then reissue bundles, releases and catalogs against it. The
   generator needs a "real objects" input for this; that input does not exist yet.
3. The catalog changed once for UTC, as the profile predicted (note 15): every TEST release hash moved; the 352
   `expected.json` files did not (diffed against the pre-change tree: only `release.json` and `catalog.json`
   differ). The real catalog changes every production release hash once more only if its fields change.

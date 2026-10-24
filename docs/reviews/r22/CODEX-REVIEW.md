- **Repair 1 — R22-01, MEDIUM: not fully met.** [Lines 49–50](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:49) omit **policy conformance** and say “same list” rather than the same manifest. Cryptographic validity alone is insufficient ([profile clarification](/home/tony/projects/tessera/docs/V1-PROFILE.md:1331)). Replace with: “A possession signature proves possession of a signing key over the manifest—the key list and its metadata. Another policy-conforming valid signature by the same key over the exact same manifest can replace it without changing the verdict.”

- **Repair 2 — MET.** [Lines 47–48](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:47) accurately distinguish signing frames from signing raw content, consistent with A9.1 C1/C3 and the profile.

- **Repair 3 — MET.** [Lines 33–34 and 44–45](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:33) replace the absolute hash explanation and qualify the one-bit claim by the registered assumptions. Consistent with A9/A10 and the contract’s conditional guarantees.

- **Repair 4 — MET.** The [CANNOT VERIFY row](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:133) correctly prevents verified reliance without implying fraud or falsity.

- **Production-key caveat — MET substantively.** [Lines 117–119](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:117) explicitly say acquisition is not usable yet, consistent with A10.4.2. **R22-02, LOW:** “Not yet fixed” names no existing section. Replace that reference with “Open items in this draft.”

**Other remaining wording:**

- **R22-03, LOW:** [Lines 31–32](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:31) still assert absolutely that only a key holder can make a signature. Replace with: “Under the registered cryptographic assumptions, making a valid signature requires access to the key’s signing capability.”

No other contradictory absolute hash/signature statement found. The scenario-table “Reject” instructions remain compatible with repair 4. No files edited.



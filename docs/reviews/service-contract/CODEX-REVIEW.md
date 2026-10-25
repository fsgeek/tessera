**Revise before using this as a shipping contract or an independent build target.** The main problems are stronger delivery guarantees than the registration supports, incomplete conditions on continued verification, and several misleading failure rows.

I treated [E9 row 2](/home/tony/projects/tessera/docs/reviews/e9-packet/AUTHOR-RULINGS.md:3) as controlling: the listing is cut; capture of both authority channels can produce passing receipts under attacker keys; release-key independence remains required. **High** means a material reliance or trust-boundary error. **Medium** means an inaccurate service promise or a policy gap that needs resolution. New policies below remain **Undecided**.

First, promises exceeding the registration or what can reliably be delivered:

- **SC-01 — Medium — S1.1: the format’s 16 MiB cap is not a client-content allowance.**  
  [Lines 19–20](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:19) imply that the format permits 16 MiB of submitted content. The [encoding limit](/home/tony/projects/tessera/formal/p8/ENCODING-V1.md:148) covers the complete encoded payload, including metadata. The registered encoding also admits restricted JSON and distinguishes requester input from canonical signed bytes. “Content bytes” leaves that relationship unspecified.

  **Replacement:** “**Undecided:** accepted submission forms, how submitted content is represented in the receipt, which exact bytes are attested, and the client size limit, including encoding overhead. The complete encoded payload is capped at 16 MiB.”

- **SC-02 — Medium — S1.2: complete issuance does not guarantee atomic transport.**  
  [Lines 21–22](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:21) promise either a complete delivery or nothing. An interrupted transfer can leave a client with a prefix or missing files. [A9.1’s invariant](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:164) governs what the issuer ships; it does not make the connection infallible.

  **Replacement:** “The service makes only complete receipts available as completed results. An interrupted transfer is not evidence of a complete receipt. **Undecided:** how clients detect incomplete delivery and retrieve the complete result.”

- **SC-03 — Medium — S1.1, S1.4 and S1.8: no response is a missing outcome.**  
  [S1.4](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:27) assumes that refusal is always observable. A connection failure can hide whether a request was received, completed or refused. “Refused content is not receipted later” is also an additional cancellation/finality policy, not a consequence of the registered complete-receipt invariant.

  **Replacement:** “A refusal response names its reason. A timeout or lost connection establishes neither refusal nor completion. **Undecided:** how clients resolve an unknown outcome, and whether a terminal refusal guarantees that the service will never subsequently complete that request.”

- **SC-04 — Medium — §5 overstates what A9.1 requires about latency.**  
  [Line 84](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:84) calls a “delivery bound” promised by A9.1. [A9.1](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:112) requires *stated cost and latency*; it does not itself promise successful delivery within a finite worst-case bound. A deadline ending in failure is also different from a successful-delivery guarantee.

  **Replacement:** “**Undecided:** the stated latency commitment, its measurement endpoints and operating conditions, and the outcome when it cannot be met.”

- **SC-05 — Medium — A1.2 conflates immutable assertions with immutable publication infrastructure.**  
  [Lines 44–46](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:44) add continuous publication “while the service operates” and require the DNS record and repository to remain unchanged. The registered duties preserve published windows and require public publication; they do not require an unchanged live repository or all live DNS material. A later registered replacement can update the same DNS owner and git path.

  **Replacement:** “The operator publishes the required authority records and does not shorten an issued window. Publication is an issuer duty, not a verifier finding. **Undecided:** publication availability, retention of historical assertions, and how long public access continues.”

- **SC-06 — High — A1.3 and the disappearance rows omit usable installation and trust coverage.**  
  [Lines 47–48](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:47) make a release archive and trust file sound sufficient for future checking. The promise is offline verification **after installation**; [installation is not offline](/home/tony/projects/tessera/docs/V1-PROFILE.md:2013). An authentic configuration can also lack required evidence coverage. Dead-project reconstruction is explicitly unproven.

  **Replacement:** “A preserved receipt can be checked without Tessera or network access using an installed, functioning, authenticated verifier and compatible authenticated trust data covering its required evidence. The holder is responsible for preserving those materials and the needed execution environment. Reconstruction after the project disappears is not demonstrated.”

  Apply this qualification to S1.8, A1.5 and F1.1/F1.2/F1.7.

- **SC-07 — High — A1.4 states fingerprint publication but omits the essential release-authority boundary.**  
  [Lines 49–51](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:49) do not say that operational or authority-channel access must be unable to authorize releases. Independent publication channels alone do not establish that. This is an existing [A9.5 requirement](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:326), retained by A10.4.2 despite the listing cut.

  **Replacement:** “Access used to operate issuance or either authority channel must not permit authorization of verifier releases or replacement of authenticated trust data. Relying parties authenticate the production release key independently before accepting a release. TEST authority is never accepted for production reliance. Production releases are unavailable until the required independence and acquisition checks have been established.”

- **SC-08 — Medium — S1.6 presents hashing as a secrecy solution without stating the changed claim.**  
  [Lines 33–35](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:33) imply that submitting a digest provides secrecy. A digest can disclose a guessable secret, and the resulting receipt attests the submitted digest representation, not independently the original document.

  **Replacement:** “A client may submit a digest instead of the original content. The receipt then attests the submitted digest bytes; connecting them to an original requires the original and a separate digest check. This provides no general secrecy guarantee.”

Second, implementation leakage and independence of the handoff:

- **SC-09 — Medium — S1.3 exposes an internal measurement boundary and instrument-run behavior.**  
  [Lines 24–26](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:24) measure “from signing” and describe a one-time startup wait. Signing is not an observable client event. The two runs were [TEST instrument runs](/home/tony/projects/tessera/prototype/e2e/FINDINGS.md:45), not evidence of a production service commitment. These details bias a builder toward the existing issuance sequence.

  **Replacement:** “Completion requires the registered Bitcoin confirmation evidence. **Undecided:** latency measured between named client-observable events, whether preparation time is included, and whether results are pushed or retrieved.” Remove the run measurements and startup estimate from the normative contract.

- **SC-10 — Medium — F1.8 retains an architecture-specific account boundary.**  
  [Line 75](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:75) uses “the operator’s issuing account.” That encodes Tessera’s particular account arrangement despite removing the cloud’s name.

  **Replacement:** “An attacker obtains the service’s ability to produce both required signatures.” Its consequence is: “The attacker can construct receipts that pass the remaining checks; V1 does not establish authorized presentation in this case.”

  Similarly, F1.6 can say “A required signature cannot be obtained” instead of “one signing path unavailable.”

- **SC-11 — High — A1.1 makes the independent-builder handoff depend on material containing internals.**  
  [Lines 42–43](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:42) deliberately omit the receipt guarantees and limits. Following the referenced document exposes an independent builder to cloud-specific failure descriptions and, outside the cited sections, formal-model and implementation mappings. The draft alone therefore cannot serve the proposed handoff.

  **Replacement:** supply an implementation-free normative appendix containing the receipt guarantees, their assumptions, non-claims, verdict meanings and time semantics. Reference that appendix from A1.1. Include the remaining externally relevant format/verification requirements in the approved handoff packet, without requiring access to the internal repository.

  DNSSEC, signed git evidence, Bitcoin, the domain, two signatures and authenticated verifier releases are externally relevant contract facts. Their names are not implementation leaks. I found no literal cloud, queue or library names in this draft.

Third, missing service policies—not decisions for this review to make:

- **SC-12 — Medium — No complete request-lifecycle contract.**  
  [S1.1–S1.5](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:19) leave clients unable to distinguish receipt of a request, acceptance for processing, completion and successful delivery.

  **Replacement/addition:** “**Undecided:** request identity; observable request states; durability of acceptance; status lookup and result retrieval; recovery after lost responses; expiry and cancellation; retry semantics; and authorization to retrieve a result.” Define idempotence by request identity as well as repeated content.

- **SC-13 — Medium — Clients lack actionable window and charging terms.**  
  [L1.1](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:59) gives a maximum window length but no actual dates or acceptance cutoff. Clients also need the outcome for accepted work approaching closure.

  **Replacement/addition:** “**Undecided:** published window dates, request-acceptance cutoff, notice of closure, treatment of pending requests, and whether already-completed receipts remain retrievable afterward. **Undecided:** the chargeable event and charges or refunds for failed, expired, cancelled or duplicate requests.”

- **SC-14 — Medium — The retention question covers only successful delivery.**  
  [S1.6](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:33) leaves failed and pending submissions outside its retention question and says nothing about access to content or results.

  **Replacement/addition:** “**Undecided:** who may access submissions and receipts; confidentiality during submission and retrieval; retention and deletion of pending, refused, failed and completed submissions, including retained copies; and any use beyond fulfilling the request.”

- **SC-15 — Medium — No holder-facing artifact-acquisition or support promise.**  
  [A1.3–A1.5](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:47) describe survival but not how a holder obtains and preserves a usable verification set.

  **Replacement/addition:** “**Undecided:** how each completed receipt identifies and supplies access to a compatible authenticated verifier and trust configuration; supported execution environments; how long those materials remain downloadable; and support-ending notice.”

  Also restore the already-registered guidance: retain the issuer’s original proof; a different proof or configuration can select a different T, and a later proof can cause `ISSUANCE_WINDOW`. Exact reproduction concerns identical declared inputs, not every later presentation.

Fourth, L1.1:

**Its central claim is correct.** [A9.6](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:407) expressly registers only the first window, caps the endpoint difference at 90 days, requires a dated rotation registration with named evidence before successor issuance, and otherwise requires issuance to stop. [Profile §6.2](/home/tony/projects/tessera/docs/V1-PROFILE.md:723) agrees. I found no successor registration in the searched record.

- **SC-16 — Medium — F1.7 and §5 turn that issuance limit into broader service-lifetime language.**  
  [F1.7](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:74) says “service ends”; [line 88](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:88) invites a broader reading of the 90-day limit. Stopping issuance does not require stopping retrieval, publication or verifier distribution. Nor does window verification prove that actual signing occurred inside a 90-day UTC interval: A10.2 establishes only two comparisons.

  **Replacement:** “V1 authorizes one issuance window whose endpoints differ by at most 90 days. Without the separately registered rotation, issuance stops at that window’s end. This does not set the lifetime of retrieval or verification support, or prove an actual signing-time interval.”

Finally, incorrect or insufficiently qualified failure rows:

- **SC-17 — Medium — F1.3: chain delay need not end in delivery.**  
  [Line 70](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:70) guarantees “Later delivery.” A sufficiently delayed attempt can fail the [registered temporal checks](/home/tony/projects/tessera/docs/V1-PROFILE.md:867) or exceed the issuance-window limit.

  **Replacement:** “Completion may be delayed. An attempt that cannot satisfy the required checks must not be delivered as a completed receipt. **Undecided:** retry, expiry and terminal-failure behavior.” Previously delivered receipts retain their guarantees under the unaffected assumptions.

- **SC-18 — Medium — A1.6 and F1.8–F1.10 confuse absent detection guarantees with guaranteed invisibility.**  
  [A1.6](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:54) says V1 “detects no capture”; the rows say “Nothing visible.” Capture may be noticed independently or produce visible effects. [A10.4](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:423) disclaims guaranteed detection and publication.

  **Replacement:** “V1 guarantees neither detection nor public exposure of the capture. A client may observe no difference.” Keep the proposed known-capture notification policy **Undecided**.

- **SC-19 — High — F1.9 overstates what “honest receipts stay protected” means.**  
  [Line 76](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:76) omits the conditions and the bounded property. [G10](/home/tony/projects/tessera/docs/V1-CONTRACT.md:34) protects honest frames, signer sets and signatures against transplantation while the original keys remain secret and unmisused and the independent release boundary holds. It does not provide general protection under combined compromises.

  **Replacement:** “While the original service keys remain secret and unmisused, authenticated verifier distribution remains intact, and the remaining registered assumptions hold, the captor cannot reattribute honestly signed frames, alter their signer sets or transplant their signatures. The captor can construct new receipts under its own keys that pass the remaining checks.”

  Add a table-wide qualification: each row retains the assumptions it does not explicitly relax. Replace unconditional “Every receipt already issued” with the applicable conditional guarantees for preserved, otherwise conforming receipts.

- **SC-20 — Medium — F1.10 incorrectly makes avoiding later releases a necessary condition.**  
  [Line 77](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:77) says **only** holders who installed no later release are unaffected. The source states a sufficient precaution, not that every later release is compromised.

  **Replacement:** “The attacker can sign substituted verifier releases and trust data. Theft alone does not affect checking with a previously authenticated, preserved genuine installation. Authentication under the stolen key alone cannot distinguish a genuine newly acquired release from the attacker’s release. V1 offers no assured recovery.”

- **SC-21 — Medium — F1.12 gives the wrong clock-fault behavior.**  
  [Line 79](/home/tony/projects/tessera/docs/V1-SERVICE-CONTRACT.md:79) confines refusals to window edges. The [declared-time check](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:401) can refuse an attempt anywhere in a window—for example, when the relevant clock differs from an otherwise correct declared time by more than 24 hours. Smaller faults need not cause refusal. “Chain time governs” also must not suggest that T establishes actual issuance time.

  **Replacement:** “Clock faults may cause refusal, delay or failure of required temporal checks anywhere in the window. Preserved receipts checked with identical inputs do not depend on the checker’s current clock. T remains a chain-header time; a UTC bound requires A-UTC.”

F1.4/F1.5 use the correct **fewer than six / six or more** reorganization boundary. F1.11 correctly permits duplicate valid receipts; retransmission can also return the same receipt. Those rows need the common qualifications above, rather than a changed threshold or a uniqueness promise.

No files were edited. This was a document and evidence review; no implementation or model tests were run.

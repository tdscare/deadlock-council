# Whole-build validation checklist (format `build-validation-checklist/1`)
File: `council/publish/checklists/<build id>.json`, one per build revision (it carries `content_sha`; a different build content invalidates it).
```
{ "format":"build-validation-checklist/1", "build":"<id>", "revision_ref":"<id>@r<N>#<sha8>", "content_sha":"<sha256 of canonical build content>",
  "purpose":["damage","farming",...],              // which "purpose items" this build claims to do. The checker RECOMPUTES the required set from the classifier; claiming less than the evidence-based class is rejected.
  "items":{ "<key>": {"status":"pass|limited|na", "evidence":[{"path":"council/...","note":"..."}], "limitation":"text (required for limited/na)"} },
  "limitations":["every unproven interaction, stated plainly"], "reviewer":"agent/person", "date":"ISO" }
```
`status` written in the file is only a CLAIM. `tools/prepublish.js check` recomputes every item from the evidence files themselves and never trusts the claim.
## Items (keys) and what can satisfy them
| key | always required | evidence that can make it `pass` |
|---|---|---|
| progression_spikes | yes | `strategy` file (CONCLUSION: CHOSEN, CHOSEN-PATH == the record's core purchase sequence) + `investment` file; both admissible |
| ability_upgrades | yes | `strategy` file whose CHOSEN-ORDER == record order (per-stage ability points) |
| thresholds_sales | yes | `investment` file (thresholds gained/lost, sold items) + roundtrip sale-instruction check |
| alternative_comparison | yes | `strategy` (alternatives A0..An at comparable investment) or `decision` file comparing with the existing build |
| limitations_listed | yes | non-empty `limitations`, each unproven interaction named |
| naming_coherence | yes | `classify` lint verdict has no `fail` (name/desc/tags vs composition); evidence level stated |
| description_basis | yes | description lint clean: every sentence has a `basis` entry |
| captions_complete | yes | every core item has a caption; phases have descriptions (from the captions pipeline) |
| tags_verified | yes | tags decode back identical in the export round trip and tag lint has no `fail` |
| export_roundtrip | yes | `tools/roundtrip.js` all checks pass for this exact content |
| damage / sustain / survivability / farming | purpose-dependent | >= 2 admissible MEASURED build-context sandbox results (distinct scenarios/checkpoints). Calculated/modelled files give `limited`, never `pass` |
| activations_rotations | purpose-dependent | MEASURED build-context result in which the conditional/active effect was actually cast in the build's own rotation (an `interaction` calc file alone is `limited`) |
| synergies | purpose-dependent | `interaction` + `team`/`context` files admissible AND at least one MEASURED build-context result of the full item set |
| temporary_purchases | purpose-dependent | `path`/`investment` file valued while owned (calc) AND measured while-owned value for items bought only to be sold |
| situational_swaps | purpose-dependent | `situational` file per swap box with the stated trigger |
| utility_contribution | support / hybrid builds | MEASURED build-context result showing the utility actually applied (cc/debuff/heal uptime or kill-setup), not item presence |
## Hard rules (explicitly insufficient on their own)
* a mechanically interesting interaction (`interaction` file only) -> never `validated`
* one controlled sandbox test -> counts once; `damage`/`survivability` need >= 2 distinct admissible measured results
* strong final items -> the progression must be proven by a `strategy` file with CHOSEN-PATH equal to the record's core sequence
* good captions / a clever name -> `captions_complete`/`naming_coherence` can pass while the build stays unvalidated; they never substitute for measured/strategy items
* evidence is admissible only if: header `SCOPE: build-context`, `VALID` not `no`, BUILD matches, BODY-SHA verifies, INPUT-SHA current (stale evidence must be regenerated)
* the gate currently refuses `measured` evidence in a proposal until the Sandbox results path is validated (audit/sandbox.md gap 1); the checker reports that as a blocker note
Result states: `validated` only if every always-required item and every purpose-required item computes `pass` (other purpose items may be `limited` with text). Otherwise `not-validated` with the exact missing list.

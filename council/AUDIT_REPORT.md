# Council audit report (24 Oct 2026)
Levels: R = only written · C = coded · I = integrated (changes/gates the real build) · T = tested against a known answer. Evidence files: council/audit/{reqs,tools,builds,sandbox,contam,review}.md, council/triage/TRIAGE.md.

## Verdict
The Council is mostly **R and C, almost nothing I or T**. Calculators exist and several are correct, but none could stop a bad change; build edits went straight into data.js with no record; the Sandbox has produced zero decision-grade results. Until this audit, "validated" meant "a document says so".

## What is in each state
| Area | Level | Evidence |
|---|---|---|
| Build structure (12 core slots, 16 ability clicks, no duplicates, no stale names) | C, T | builds_check.js: 81/81 pass |
| Export code round-trip (in-game import) | C, T | decode == data.js for 81/81 (imp/*.b64); codes.js/codes.json stale but unused |
| Spike timing per colour, overshoot, rich/counters/slot-locked rules | C (now I via gate) | before today: run by hand, advisory. Violations in shipped builds: late health 3, overshoot 6, early 6.4k 4, rich T3 5 |
| Ability points / charge items / thresholds (abtimeline.py) | C, partly T | correct vs hand calcs after rewrite; unused before today; point model unsettled; charge rule unverified |
| Conditional item thresholds | R -> C | only Violet fixed by hand before; abtimeline now emits a row per conditional item. 65 buy points had no threshold line |
| Cost-efficiency | C (numbers), R (verdicts hand-typed) | chunk3 only; its findings were applied via apply chunks |
| Reviewer | R | ran on 2 builds of 81 |
| Synergies, multi-role items, kit-first thesis, weakness->remedy | R (+worked examples, model-only) | 5 pilot heroes + Haze/Seven/Grey Talon; no hero's build was changed by them |
| Sandbox Tester | C (instrument) | ~84 runs; per-bullet maths valid; healing not measurable (42% spread); no result ever changed a build |
| Sandbox -> Council results path | R | ledger.js reads files nothing writes; no evidence gate |
| Duo builds | R | duos.js empty |

## Cases where the Council said it handled something but did not
1. Sandbox "seeded paired design, CV 5.5%": `accseed` was never built in the deployed plugin (68 unknown-op lines).
2. Victor "VB > Infuser ~ none > Leech": runs used `unlock 15`, no setup checks, arm bias. Invalid (marked in TEST_MATRIX).
3. "Gate: full.js clean / cost FLAGs block the build": nothing enforced it; merge.js validated only the id.
4. Seven Arcane Surge early (rule + cost evidence) vs shipped late; the ability check ran after the move and passed.
5. Spirit per level hardcoded 1.1 in sp.js (12 builds differ). FIXED (council/lib/herostat.js).
6. Haze fight model: wrong weapon-investment table, vitality omitted, self-referential enemy damage. Not decision evidence.
7. Echo Shard on graves_ult's ult does nothing (game data); old audit passed it.
8. "No dead items": false for graves_ult, yamato_brawler, paradox, lash; 14 charge rows depend on one unverified rule.
9. Sandbox tiers: `unlock 7` is probably T2, not T3, so earlier "max tier" runs were likely T2.
10. Item-text extraction skips active items (29 used items have no text, e.g. Dispel Magic, Echo Shard): active-item checks were blind.

## Do the parts feed one process?
No. Nothing combined kit, synergies, ability points, thresholds, order and spikes: separate agents/tools each reported; the final build was edited by scripts (mv.js, rebox.js) that ignored them and never wrote `changes`. 32 builds changed vs the clean base (data_pre_spikefix.js); 30 with no changes line.

## Done today
- data.js and all backups immutable; snapshot + sha256 in council/frozen/.
- council/tools/gate.js: the only route to change a build. Runs every validator on old and new, blocks any NEW violation, validator crash, missing reason/evidence, stale base, sandbox evidence (not accepted yet). Apply needs a per-proposal approval file; writes the diff/reason/evidence into `changes`; snapshots and logs. Tested: a deliberately bad change was blocked by 4 checks; Haze swap blocked.
- Spirit-per-level root cause fixed; invalidated results listed (council/audit/INVALIDATED.md).
- PROTOCOL.md hard rule; ability-checker/sandbox-planner agent files in council/agents.

## Fix order (reviewer re-ranked, then mine)
1. **Re-dump game data for installed build 6819** (data is 6801) and diff; item prices are not in the dump. Needs PC access.
2. **Triage the 32 changed builds against data_pre_spikefix.js** (not bak_rel: bak_rel lacks the Oct 22 Counters text). Priority: seven_gun, seven, geist, graves_ult, venator_grenade, ratking_grenade. Fix surgically through the gate.
3. **Two live in-game checks**: does a 1-charge ability count for charge items (14 rows, 9 builds)? Do unlocks wait for ability points (24 builds, only nurse/lash affected)? Also confirm unlock-7 tier meaning. Hold all charge-item edits until then.
4. Repair the Sandbox basics before using it: implement+verify `accseed`, make setup-check failures abort, results writer + evidence file format, re-run Stage 0, re-run Abrams with correct tiers.
5. Gate hardening: use abtimeline known-answer tests; fix false positives (sell notes "if you have it"); add the strict-vs-two-queue timeline flag; stop silent writers.
6. Item text for active items (localization) into the item data; re-check the 29 items.
7. Reviewer on every build before any change; duo builds status decision (17 drafts unpublished).

## Not rated high
codes.js staleness, the 1.1 constant after fix, the 34 "ignored sells" (core pairs already carry the sell), sandbox gaps (no sandbox result reached a build). Model confidence percentages anywhere in the docs are model outputs, not accuracy.

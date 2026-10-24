# Council audit, 24 Oct 2026 (read-only; nothing run on the PC, nothing modified)

Method: read the council/ files, hypotheses JSON, sandbox docs, queue copy, data.js (sha 1392ab06..., identical to the frozen snapshot), and recomputed counts with local Python/Node. Not verifiable from here: the live PC queue and logs (only a local copy of queue.json from 16:30 and relayed results), and whether Rend x Crushing Fists is already common community knowledge.

## Bottom line
The Council has one real, working asset: a deterministic pipeline from game files to typed effects to ranked hypotheses to sandbox scenario files (`lib/effects/extract.py`, `tools/discover_interactions.py`). It also has a stylised whole-build model (`abtimeline.py --strategy`) and a small, honest sandbox measurement record. It does not yet have a learning loop, an evidence-backed build, or a single demonstrated build improvement. All 81 builds in data.js come from Kieran's in-game builds, public builds and rule-following; sandbox evidence is cited in 1 of 81 builds, and that one cites a missing result.

## 1. How it understands mechanics: PARTIAL
Exists:
- Source: SteamDatabase dumps of build 6819 (`gt6819/.../abilities.vdata` 8.2 MB, `heroes.vdata`, English localisation), matching the installed client (`audit/GAMEDATA_6819.md`; 6801 to 6819 diffed, 3 data hunks).
- Extracted: 43 heroes, 195 items, 863 hero effects, 466 item effects (`evidence/interactions/effects/*.json`). Each effect has an op/state vocabulary, tier needed, conditions and a cited source. Unknowns are recorded as 'UNKNOWN'. `provenance.py` re-checks citations against raw text.
- Grades: hero effects are 503 NAME-INFERRED / 312 STRUCTURED / 48 TEXT. Item effects are 332 STRUCTURED / 107 NAME-INFERRED / 27 TEXT. So more than half of ability effects are inferred from property names, not declared by the data.
- Relationships exist only as templates (T1-T5, below), not as a general graph. 51 'verified' facts are raw field values.

Missing or weak:
- Engine semantics (what a flag does at runtime), the damage-instance type split, and whether an ability counts as the event an item consumes. The Rend measurement found Rend's damage splits into an 'Ability' part (unchanged) and a 'Melee' part (x1.49). The extractor has no damage-type field, so this was learned by measurement and is still not in the model.
- Item prices are not in game files; 800/1600/3200/6400 are wiki values (secondary), and tier 5 has no source.
- Per-effect duration is often UNKNOWN. The sandbox cannot read modifier durations or stacks, only names.
- `lib/effects/tests/` has 12 tests; I did not run them.

## 2. Hypothesis discovery: PARTIAL (a repeatable generator exists, but it is narrow and example-shaped)
It is not LLM brainstorming at run time. It is five hand-written relation templates run over the typed effects, with a relabel-invariance selfcheck. But an LLM wrote the templates after Kieran's 15:58 examples, and nothing takes a measured result as input and generalises it ("one established interaction, derive a rule, search for siblings, find exceptions" is not automated).

Counts in `ranked.json` (110 hypotheses, all HYPOTHESIS tier):

| template | n | relation to Kieran's examples |
|---|---|---|
| T2 cooldown reset on imbued ability | 98 | Every one is Echo Shard (1 item) x every hero ability with cd >= 8. This is Kieran's Viscous/Rem/Nurse Echo Shard idea enumerated. |
| T5 ability emits event, item consumes | 8 | Only one event class is coded (heavy melee). Four heroes x 2 items (Crushing Fists, Melee Charge). |
| T4 cast-phase lockout vs item actives | 2 | Familiar, Nurse. Constraint only, "no build change implied". |
| T1 protector vs deferred cost | 1 | Nurse Harrow, Kieran's own example. |
| T3 cleanse vs unpurgeable debuff | 1 | Nurse; predicted to do nothing. |

So 98 of 110 (89%) are the user's example item, and 2 more are his Nurse example. Independent content is the 8 T5 and 2 T4, which is 10 of 110.

The best independently generated example (T5-77785e7cae, Drifter):
- Facts: Rend's T3 text says heavy melee (`UseHeavyMelee`, STRUCTURED). Crushing Fists has `BonusHeavyMeleeDamage` 25 (name-inferred).
- Unknown: whether ability-delivered heavy melee counts, and whether it hits all targets or the first, and stacks.
- Competing outcomes: counts; only manual melee; counts but excludes ability damage; first or all targets.
- Test (`int_disc_T5_77785e7cae.txt`): Rend with and without the item at 100/150/250 u, A,B,A,B, plus manual melee controls CA/CB.
- Result (measured.json, valid, replicated once in the same session): the item raises Rend's Melee-typed part 136.9 to 204.1, leaves the Ability-typed part unchanged, and adds its own 51.0 Melee line. Per cast: 270.8 to 389.0 (+43.6%).
- Caveats: Drifter's Rend-plus-melee-item pairing may be known to the community (unverified). Kieran's memory mentions Crushing Fists and "the Rend build", so adjacency is not zero. The result does not show purchase value. The hypothesis stayed 'TESTABLE-NOW' in `ranked.json` afterwards (see 4).

## 3. Deciding what to test: PARTIAL
- Scoring is a fixed weighted sum (impact 0.35, info value 0.2, plausibility 0.1, availability 0.15, testability 0.2), all hand-set. "Testability" favours whatever the sandbox can already do, so Echo Shard and heavy melee float to the top.
- Documented-relationship filter: none as such. T5 only emits pairs where the link is "not in the data". T2 emits pairs where the reset is documented in item text and asks about second-cast behaviour. A "ladder" marks stage 1 EVIDENCED, and 44 of 98 T2 entries get a calculation verdict "beaten by Compress Cooldown per 1000 souls", i.e. resolved by arithmetic without sandbox time. The other 54 are 'competitive' and unresolved.
- Recycling: nothing penalises Kieran's examples. Haze (his example hero) has 7 of the 43 interaction scenario files (2 are Close Quarters), alongside 9 Billy and 5 Rem item-matrix files. Of 43 interaction scenario files, 22 are tagged 'discovery', 12 'build-decision', 8 'requested' (by Kieran).
- Build relevance: impact scores are heuristic (cooldown, protection flags), not computed from whether the hero's build would buy the item. Several hypotheses concern heroes with no build in data.js (Priest, Punkgoat, Familiar, Forge are not among the 81 builds).

## 4. Learning from results: MOSTLY ABSENT (manual)
Traced path: sandbox result (PC) -> coordinator relays text -> hand-edited `evidence/interactions/validated/measured.json` (22:25, "relayed by the coordinator; the engine has not read the logs") -> nothing reads it.
- `grep` finds no reader of measured.json. `discover_interactions.py` header still says "Nothing here is MEASURED". `ranked.json` is dated 16:32, before the 21:48 Rend run, so the Drifter hypothesis still reads TESTABLE-NOW with ladder stage 2 NOT-EVIDENCED. The seven sibling T5 hypotheses (Priest, Punkgoat, Viscous x Crushing Fists / Melee Charge) are unchanged and their scores did not move.
- `tools/ledger.js` (result -> verdict) has never produced a file: `evidence/<hero>.json` does not exist. `gate.js` blocks sandbox-cited evidence outright ("not accepted until the Sandbox results path is validated").
- One live path exists: `abtimeline.py` reads `sandbox/results/measured_inputs.json` for reload times. That file does not exist; the only measured reload (Wraith 2.82 s) is hard-coded.
- Calculation did get corrected once by measurement: the Wraith Swift Striker vs Titanic calc predicted +32/+44/+48/+19%, measured +27/+41/+34/+7% (`results/wraith_gun_PR-W1.md`). That was a human reading, with no automated re-rank.

## 5. Whole-build optimisation: PARTIAL (a model exists; it cannot yet be trusted to pick)
What `--strategy` computes (Wraith, `evidence/strategy/wraith_greens_vs_ricochet.txt`): nine data-generated paths (as-built, rush gun, rush vitality, spread, off/def greens before the spike item, defensive ability order). Each is walked by souls with category invest bonuses, ability-point timeline, tiers, a sell refund (0.5, flagged UNVERIFIED), a soul-income model (lane/farm/fight, camp clearing), and a 1v1 trade ratio against an assumed reference enemy, over a 13,824-cell assumption grid, with a pre-registered decision rule.
- Wraith result: INSUFFICIENT EVIDENCE. As-built wins 16 of 13,824 cells; "Spread" wins 71% (needs 80%).
- Structural problem (the file says so itself): across all 81 builds the as-built path won 0 grid cells on any build, and cheap defensive greens before the spike won 51 of 57 decided builds. The model rewards balanced health and damage by construction. Treat model-only wins as model artefacts until a shoot-back lane test exists.
- Ignored or assumed: real rotations (cadence assumed), formations and teamfights (scalar `p2hero`), enemy CC, item active timing, on-hit effects of Inhibitor/Silencer/Spirit Rend (unpriced), positioning, matchup (one reference enemy), enemy items, sell price, lane-state beyond one flag, range (one constant `close_u`; range tests designed but never compiled, per CONTINUE.md).
- Can it reject a clever synergy? Partly: 44 Echo Shard entries are "beaten" per 1000 souls by Compress Cooldown, and Seven's fire-rate swap was kept out via calc (`proposals/seven_gun.json`). Can it show a plain build beats a clever one? Not with a verdict anyone should trust.
- Nothing from this process reached a build: the Seven decision record ends "POSTPONE / keep data.js as is", Paige 800 has only a sealed candidate list.

## 6. Independent progress ledger

| category | count / items | note |
|---|---|---|
| Known mechanics in game data | 863 + 466 typed effects, 51 raw facts | extraction, not discovery |
| User-provided examples (generated or re-tested) | 98 Echo Shard hyps, Nurse T1/T3, Haze Close Quarters set, Haze Active Reload window, Victor Berserker/Pain Battery, Wraith Swift vs Titanic | per file text; origin of each question not fully traceable |
| Unverified hypotheses | 110 (108 with no result) | all HYPOTHESIS tier |
| Valid measurements | 26 preserved + 2 new valid since commissioning (SCOREBOARD) | Stage 0 known answers (head x1.65 etc.); Wraith PR-W1 (isolated); Victor T4 Berserker (+5.9%, T5 inconclusive); Haze Active Reload window in (1.0, 1.3) s, n=1 per delay; Rend/Crushing Fists |
| Independent AND measured | 1 (Rend/Crushing Fists), novelty unverified | not a purchase verdict |
| Demonstrated build improvements | 0 | data.js unchanged since 01:08; `history/LOG.jsonl` does not exist; `approvals/` empty; 7 proposals unapplied |

Related negatives: 32 builds were silently changed by scripts before the freeze, 30 without a changes line (AUDIT_REPORT); several earlier Sandbox claims were withdrawn (seeded paired design, Victor ranking).

## 7. Top gaps, ranked by effect on final builds, with the smallest fix

1. **No loop from result to hypothesis, ranking and build.** Fix: have `discover_interactions.py run` read `measured.json` (and later results), set the ladder stage and 'MEASURED' tier, and re-rank siblings. For T5 add a rule: if one heavy-melee ability confirms, promote the same-item hypotheses on other heroes; if rejected, demote them. About 50 lines; do it before any new template.
2. **The build model leans to defensive greens and has no ground truth.** Fix: one shoot-back lane trade test at one checkpoint on one hero, and use it to calibrate or reject the trade-ratio term. Until then, do not use `--strategy` verdicts for edits.
3. **Evidence never reaches a build.** Fix: pick one proposal that needs no sandbox (e.g. the Seven or Graves ult fixes in `proposals/`), take it through `gate.js` with Kieran's approval, and prove the pipeline once. Also replace the ledger/gate "sandbox not accepted" block with a defined acceptance rule.
4. **Narrow, example-shaped discovery.** Fix: make `EVENT_CLASSES` data-driven (all property-name pairs where an ability property and an item property share a key stem), cap any single item at about 10 hypotheses, and add a 'user-example-derived' flag so the ranking shows independent items first.
5. **Game model gaps: damage-type split, item actives, prices.** Fix: add damage-type to the extractor from `abilities.vdata`, re-extract active-item text for the 29 text-less items, and confirm prices from the in-game shop once.

## Activity versus value (candid)
- Producing value now: the extractor/provenance code, `gate.js` (blocks bad edits, tested), `builds_check.js`, the single-ability sandbox measurements with VERIFY gates, and the audit files that withdrew false claims.
- Mostly activity so far: the 98 Echo Shard hypotheses (one item times every hero); the 243 `paused-needs-design` queue tasks (the planner produced no scenarios: `PLANNER_GAP.md`); weakness-solver/theorycrafter files (12 in `sandbox/weaknesses`, model-only, no build changed); `ledger.js`; the reviewer (ran on 2 of 81 builds); cost-efficiency FLAGs that blocked nothing until gate.js; `--strategy` run over all 81 builds (one bias, 0 as-built wins); duo builds (`duos.js` empty, 17 drafts unpublished); heavy sandbox HUD/display work (several sessions of display and crash fixes, with one server crash from CPointWorldText) relative to the 2 new valid measurements.
- Agent usefulness is judged from output artifacts only; I could not check invocation logs.

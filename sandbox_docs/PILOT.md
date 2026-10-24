# Council pilot: make testing trustworthy first (Kieran, Oct 24 04:11)

Goal: a Council that independently researches, theorycrafts, builds, tests and improves builds; Kieran suggests nothing. Success = consistent, evidence-backed build decisions, NOT number of tests or features. Nothing existing is thrown away (website, build rules, Sandbox Tester, Duo Builder). The all-hero alphabetical sweep is PAUSED until the pilot passes.

## Pilot builds (3, chosen to cover different failure modes)
1. Victor gun (Leech vs Infuser/Vampiric Burst style sustain question; ramping aura; lifesteal measurement).
2. Abrams tank/melee (`Atlas`): melee range, damage-taken regen, Berserker stacks, multiple attackers.
3. Wraith gun/AoE (Ricochet + Leech vs Vampiric Burst; imbue-free, proc-heavy, farm hero).
Each must yield at least one real decision: an uncertain item the Council itself identified, an A/B design, a result, a verdict (change / keep / inconclusive) with confidence.

## Stage 0: trust the instrument (gate; no build verdicts until all pass)
0.1 Stable: 30 min of continuous scenarios without client drop (fix netchan overflow first: buffered logging, no per-usercmd logging, low-rate camera).
0.2 Setup truth: every block logs and checks hero, level, ability tiers, items owned, souls, distance, stacks=0, cooldowns ready, enemy hp/resists. A block with any mismatch is INVALID and rerun, not analysed.
0.3 Null test (A/A): identical build vs identical build, same protocol. Gives the noise floor (CV of damage, dps, healing). Any measured item effect smaller than that noise is "no detectable difference".
0.4 Known-answer tests: items with exactly predictable effect (flat +% bullet damage; +fire rate; known resist) must be measured within a stated tolerance, including head vs body multiplier and the enemy-resist path.
0.5 Order/warm-up test: run A,B,B,A; the order effect must be quantified and removed by counterbalancing.
0.6 Hero confound check per pilot hero: stack/ramp/aura/decay behaviour written from kit data, reset verified between blocks, effect age matched.
If a gate fails: fix the instrument or mark the measurement UNSUPPORTED. Never silently continue.

## Stage 1: the loop (per build)
1. Identify uncertainties from kit + item data (thresholds, charges, imbues, range, souls/lane, stack dependence) and rank by decision value. Council decides, not Kieran.
2. Design: hypothesis, the one thing varied, same-tier substitute, price point(s) with level/points/boons as in game, buy order left to right, realistic conditions (accuracy, head/body mix, enemy count/resists/incoming damage), metric defined in advance (damage per shot by hit index, survivability at low HP, marginal healing), required reps from noise floor.
3. Run (counterbalanced, hardreset between blocks).
4. Validity check: automatic flags (disconnect, setup mismatch, stack/cooldown residue, bots dead, hit rate off target, order effect) -> invalid blocks rerun.
5. Analyse: effect size vs noise floor, confidence interval, kit-confound explanation recorded, sensitivity to assumptions (accuracy, distance, resists).
6. Verdict: change / keep / inconclusive, with the evidence and what would change the verdict. Proposals go to data.js only after an independent reviewer agent (given only the evidence) fails to break the verdict and the build rules/checklist still pass. Verify removals against kit data.
7. Log to results/<hero>_<build>.md and the decision log.

## Stage 2: expand
Only after all 3 pilots complete Stage 1 with at least one defensible decision each and a clean review. Then add heroes in batches by archetype, reusing the loop. Unsupported mechanics (CC, allies, etc.) are marked BLOCKED per build, not scored.

## Self-review (run at the end of each hero/pilot and at least every few hours of runtime)
Reviewer agent checks: missing mechanics (GAPS.md refresh), misleading measurements (bias, leakage, noise vs effect), unnecessary complexity (ops/rules that did not change a verdict: delete), efficiency (time per valid block, rerun rate), instrument regressions (rerun Stage 0). Output appended to REVIEW_LOG.md. Metric tracked: decisions made, % later reversed, rerun rate, noise floor. Not: tests run.

## Amendments (Kieran, 04:12)
- Regression gate: after ANY change that could affect the tester (plugin code/rebuild, ops, scenario generator, analysis scripts, game/server update, client reconnect after a drop), rerun a short fixed validation suite (stability, setup-truth, A/A noise floor, one known-answer test) before further results count. Results produced after an unvalidated change are tagged UNVALIDATED. Keep the suite small (target < 10 min) and log pass/fail with date in REVIEW_LOG.md. Re-run the full Stage 0 on every patch.
- "Cannot measure reliably" is a valid verdict. If noise > plausible effect, a mechanic is unsupported, or a confound can't be removed, record the limitation, what would be needed to measure it, and the best non-test evidence (kit maths). Do not force a definitive answer for any pilot.
- Reporting: only meaningful milestones (gate passed/failed, a real decision with evidence, a limitation found). No updates on small problems; handle them.

## Amendment (Kieran, 04:33): weakness -> remedy is part of the loop
Stage 1 step 1 ("identify uncertainties") now includes council/WEAKNESS_PROCESS.md: discover the hero's weaknesses across all categories, generate every remedy class (item, ability use, positioning, target choice, team, accept), price tradeoffs (incl. utility -> damage only when timing/counterplay allow), test the promising ones against "do nothing" where measurable (else UNSUPPORTED, decide from kit maths), choose core / situational / playstyle / leave alone, then re-sweep the changed build for new weaknesses. Pilot examples: Abrams catching mobile targets; Victor sustain vs burst; Wraith ammo/farm. Record in sandbox/weaknesses/. Reliability gates still apply.

## Amendment (Kieran, 04:39)
Theoretical (kit-maths) results must not be treated as proven real-game performance; see WEAKNESS_PROCESS.md section H (evidence grades). No new systems beyond what the pilot needs. Goal: demonstrate the Council independently finds a weakness, investigates solutions and reaches a trustworthy decision, even if the decision is "cannot measure".

## Amendment (Kieran, 04:41)
Weakness analysis now starts from the hero identity map and dependency chains (WEAKNESS_PROCESS.md A2): strengths that compensate weaknesses, how the enemy counters those strengths (e.g. Wraith teleport disabled by a slow/silence), and PREVENT / RECOVER / SURVIVE answers, plus how the enemy counters our answers and whether the chain is common/dangerous enough to spend souls on. Derived and verified by the Council; items are examples only. Grades from section H still apply.

## Amendment (Kieran, 04:49)
(1) Test location: after every setup/hardreset the plugin must position all characters in the intended arena and verify it (SETUP VERIFY ok), else the scenario fails; ArenaGuard corrects drift. Per-test terrain/positioning needs (walls, open ground, height, distance bands) are decided by the planner and declared/verified in the scenario. Results produced before the fix are UNVALIDATED for location. (2) Whole-build practicality (WEAKNESS_PROCESS.md section I): magazine vs fire rate, reload time, farming efficiency, spike-vs-survivability timing per hero (incl. when escapes are countered), buttons/actives load, slot/sell chain, forgiveness when behind.

## Amendment (Kieran, 05:19)
Multi-role item valuation (WEAKNESS_PROCESS.md section J): every item is valued on ALL its contributions (stats, procs, fire rate vs channelled ults, multi-target bounces, threshold enabling, upgrade path), not its headline role. Earlier verdicts that judged an item on one role (e.g. Ricochet only as farming) are re-opened and re-graded.

## Amendment (Kieran, 05:19, Haze clarification)
Kit-first build thesis (WEAKNESS_PROCESS.md section K). Haze example: her 2 gives 50% bullet lifesteal + cleanse, charges/recharge items raise its uptime, so heavy gun damage also raises healing; costly build => farm-heavy early with Ricochet, delay greens, Fortitude later. Illustration only; no item in that build is assumed optimal (Leech vs Vampiric Burst, Healing Booster/Tempo, alternatives all open). Needs a worked analysis as proof the process produces coherent builds.

## Amendment (Kieran, 05:25)
Item synergies and marginal purchase value (WEAKNESS_PROCESS.md section L): discover 2/3+ item combinations independently, then price each completion step (standalone value, marginal gain over owned components, same-soul alternatives, affordability timing, complete-now vs later, redundancies it creates) and choose the best complete build/order, not the strongest synergy. Current-patch numbers recomputed from game data.

## Amendment (Kieran, 05:26)
Ability timeline x item timing (WEAKNESS_PROCESS.md section M): exact ability state at each soul total (charges/tiers/cooldowns), value of ability-related items at the moment of purchase, joint optimisation of ability-point order and item order, verified in the Sandbox at real checkpoint ability tiers.

Activation thresholds (WEAKNESS_PROCESS.md section M step 4): every conditional item is computed at its exact purchase moment from verified trigger rules and validated by a known-answer test either side of the threshold.

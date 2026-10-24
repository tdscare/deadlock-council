# Sandbox scenario schema (scenarios/*.json)

A scenario is a pre-registered experiment: question, arms (what differs), controls (what must not), procedure, metrics, and a decision rule fixed BEFORE running.

```
id, title, hero, playstyle, builds[ids it can change], question, hypothesis
arms[]      { name, items[], ability_order (16-string) | null, imbues{}, souls, notes }   // only these differ between arms
setup       { level_or_boons, souls, position, enemies[{hero,count,items,behaviour,hp}], allies[{hero,count,role}], start_hp, resets[] }
controls[]  things held constant (same position, same enemy HP/resists, cooldowns reset, same trial length)
procedure[] ordered steps the tester follows, same for every arm
trials      per arm, min 5
metrics[]   { name, unit, how, grade_target (A|B|C), better (higher|lower), primary:true|false }
decision    { metric, min_effect_pct, min_trials, rule }   // verdict: SUPPORTS if arm B beats A by >= min_effect_pct with non-overlapping trial ranges; REFUTES if reverse; else INCONCLUSIVE
```

## Result files (results/<date>_<scenario>_<arm>_t<n>.json)
`{scenario, arm, trial, date, patch, metrics:{name:value}, grade:{name:"A|B|C"}, evidence:[screenshot refs], notes, anomalies}`

Header lines (required by `queue.js done` and checked by `gate.js`): `VALID: yes|no ...` and `SCOPE: isolated | build-context`. `isolated` = the item/ability alone (datum for mechanism, may be cited to gate only as kind `data`); `build-context` = complete build at the checkpoint with real ability tiers, imbues and relevant actives cast (may be cited as `measured`/`context`).

Grades: **A** = read from an in-game counter/stat screen. **B** = read from on-screen numbers, repeated trials agree (CV < 15%). **C** = visual estimate / single reading. Only A/B can overturn a calculation. C only raises a flag.

## Fairness rules
- Arms run interleaved (A,B,A,B…) to cancel drift; reset cooldowns/HP/souls between trials.
- Same stats from boons/souls in both arms except the thing under test.
- Record anything that differs (RNG procs, bot behaviour); never discard a bad trial silently, mark `anomalies`.
- Realistic play: scenarios use the hero's real engagement (Victor vs 3 enemies in his face, Wraith farming camps with Ricochet) not a single stationary dummy; stationary dummy only for pure-number checks.

## Experiment kind + strategy metadata (Kieran 13:56) - scenario JSON, queue tasks, plugin text
Scenario JSON fields (new scenarios must set `kind`; legacy files without it are linted as before and listed NO-KIND):
```
kind              baseline | isolated | checkpoint | complete-build | strategy
question          pre-registered question (string)
hypothesis        pre-registered prediction with what would refute it (string)
alternatives      ["A0 AS-BUILT", "A3 SPREAD", ...]   names = first word of the strategy file's ALTERNATIVES entries
tradeoffs         [strings]   copied from the strategy file TRADEOFFS
missing_evidence  [strings]   copied from the strategy file MISSING_EVIDENCE (what is only assumed + the test that would settle it)
strategy_file     path of the `abtimeline.py --strategy` output this scenario tests
arms[].alt        (kind strategy) alternative name; arms[].souls must be one of the strategy file CHECKPOINTS and arms[].items exactly that path's owned items there
```
Lint (`node council/tools/gen_scenarios.js --lint`):
- `kind isolated`: title/question/hypothesis/notes must contain `ISOLATED: does not justify the overall build`.
- `kind strategy|complete-build` with non-empty `builds[]` (= claims to inform a build decision): question, hypothesis, alternatives, tradeoffs, missing_evidence present; `strategy_file` exists, `KIND: strategy`, its `BUILD` is in `builds[]`, BODY-SHA verifies (not edited), `GENERATED` is earlier than every result file `results/*_<scenario id>_*`, any queue task start for the scenario and `run_started`; every listed alternative exists in the file.
- `kind strategy`: each arm is checked against the strategy file instead of the build walk (complete state of that path at that checkpoint).
Queue tasks (queue.json, sbx_queue): a task created for a scenario carries `meta` = {kind, question, hypothesis, alternatives, tradeoffs, missing_evidence, strategy_file} copied unchanged from the scenario; the `.txt` scenario contract uses `meta strategy_source <strategy_file>` for the same path.

Strategy evidence file (`python3 -I council/tools/abtimeline.py --strategy <build id> <checkpoints|a-b[:step]> [--alt <file>]... [--out f] [--set K=V] [--grid quick|full]`), default `council/evidence/strategy/<id>_<utc>.txt`. Header lines (first block, `KEY: value`):
`SCOPE: build-context`, `KIND: strategy`, `VALID`, `BUILD`, `HERO`, `VERSION`, `ARGS` (re-run command), `GENERATED` (UTC ISO), `BODY-SHA` (sha256 of the file without the GENERATED/BODY-SHA lines; `--verify-strategy f` checks it), `INPUT-SHA` (data.js + heroes/abilities.vdata + items_full(_6819) + abtimeline.py; `--input-sha` prints the current one), `CHECKPOINTS`, `QUESTION`, `HYPOTHESIS`, `ALTERNATIVES`, `TRADEOFFS`, `MISSING_EVIDENCE`, `DECISION RULE (pre-registered)`, `CONCLUSION: CHOSEN: <alt> | DEPENDS ON ASSUMPTION <param>: ... | INSUFFICIENT EVIDENCE - no decision`, `BASIS`, `GRADE`, `CHOSEN-PATH: item > item > ...` and `CHOSEN-ORDER: 1132...` (only when CHOSEN), then 3-4 `GAME_SUMMARY:` lines. Every number in the body is tagged MEASURED / CALCULATED / ASSUMED; robustness % = share of parameter-grid cells, not a probability of being right.
Alternatives are generated from data: A0 as built, A1 rush damage 4.8k, A2 rush vitality 4.8k, A3 spread, A4 offensive greens (catalog scan), A5 defensive greens before the spike item, A8 the build's own first greens before the spike item, A6 defensive ability points, A7 A4+A6, X* = `--alt` files `{name, desc, path:[item | [item, note, imbue]], order?, fill_from_build?}`.
Gate (`gate.js`): a proposal that changes the core purchase order, the core green items/positions or any colour's 4.8k spike timing must cite an evidence entry `{kind:"strategy", path}` whose file is unedited, current (INPUT-SHA), `CONCLUSION: CHOSEN`, with `CHOSEN-PATH` = the proposed core sequence and `CHOSEN-ORDER` = the proposed ability order; else BLOCK unless `waive:[{rule:"STRATEGY", why, evidence}]`.

In-game text (plugin): print the `GAME_SUMMARY:` lines of the strategy file (or `python3 -I council/tools/abtimeline.py --game-summary <strategy.txt|scenario.json>`, which renders the same lines from the scenario fields). Format, each line <= 200 chars, cut with `...`:
```
Q: <question>
Test: <hypothesis> | Paths: <A0 as built; A3 spread; ...>
Trade-off: <one trade-off line>
Result: <conclusion> | Unknown: <missing evidence; ...>      (scenario rendering without a conclusion: "Unknown: ...")
```

## Item x kit interaction file + test requests (Kieran 14:29)
`python3 -I council/tools/abtimeline.py --interactions <build> <item> [--at <souls>] [--vs <item>]... [--out f] [--no-requests]` -> `council/evidence/interaction/<build>_<item>_<souls>.txt`. Header: `SCOPE: build-context`, `KIND: interaction`, `BUILD`, `HERO`, `ITEM`, `CHECKPOINT` (buy-point | add-on-top), `GENERATED`, `BODY-SHA`, `INPUT-SHA`, `ALTERNATIVES` (equal souls, unconditional = ranked; conditional/unequal shown, not ranked), `VERDICT` (best in every window | beaten in every window | DEPENDS ON COMBAT WINDOW | INSUFFICIENT EVIDENCE), `UNKNOWN_CELLS`, `CANDIDATE FLAGS`, `PAIRWISE` (per --vs item and window: WINS / LOSES / TIE / DEPENDS across the UNKNOWN readings), `UPPER-BOUND OPTIONS THAT BEAT IT`. Body: matrix rows = item effects (from stat keys), columns = normal shooting, abilities 1-4 at the checkpoint tier (kind gun-mode / stacks / cards / spirit / weapon-scaled / melee-scaled / utility, derived from props, scale types and game text), owned procs, lifesteal, other items; each cell WORKS / DOES NOT WORK (reason) / UNKNOWN with grade. Then damage delivered per window for the state without the item, with it and with each alternative, as a range over every reading of the UNKNOWN cells.
Test request (`council/sandbox/autorun/scenarios/interaction/int_<build>_*.txt`, lint_meta contract): `meta kind INTERACTION`, `question` (plain English, e.g. "Checking whether Point Blank boosts Haze's Fixation more than Burst Fire."), `purpose`, `mechanics` (the UNKNOWN reason), `expectedstate`, `build`, `checkpoint`, `items` (= every `give`), `strategy_source` (the interaction file), `feeds`, `player_title/what/why/short/expect` (<=32 chars), `result_says` (what result means WORKS / DOES NOT WORK). Queue: `node council/tools/queue.js add <build> interaction:<cell> <file>` stores `scenarioFile` and the parsed `meta` on the task.

## Selection provenance, intended conditions and readbacks (Kieran 15:16/15:19) - `.txt` meta, checked by lint_meta (kind INTERACTION)
- `meta selection_kind build-decision|discovery|weakness-remedy|requested|calibration`, `meta selection_reason <why these items/hero, written before the run>`, `meta alternative_reason <why this comparison item>`.
- Intended conditions (the runner verifies them; mismatch => result invalid): `meta cond_scope` (gun-only / ability N cast + gun / melee only / ally-target test / complete build), `meta cond_abilities_used`, `meta cond_abilities_excluded`, `meta cond_accuracy`, `meta cond_misses none|deliberate allowed`, `meta cond_start_stacks`, `meta cond_activations <items/abilities that must actually fire>`, `meta cond_distance`, `meta cond_targets enemies=N allies=N`.
- `meta readbacks <comma list>`: equipped_items, ability_tiers, distance_m, stacks_per_block, reload_gaps_s, magazine_size, activation:<item>, ability_cast:<slot>, ally_effect_applied. `meta blocked_by <missing runner op>` when the runner cannot do it yet.
Weakness file (`abtimeline.py --weakness <build> <class> [--at]` -> `council/evidence/weakness/<build>_<class>_<souls>.txt`): `KIND: weakness`, `WEAKNESS`, `ROOT-CAUSE`, `NO-FIX: yes|no`, `REMEDY-SET`, `SIMPLE-REMEDY` (MISSING = generator flag, gate BLOCK), `CONCLUSION`, `SCORING`, `GRADE`, BODY-SHA/INPUT-SHA; gate evidence kind `weakness`.

## Strategy tool modes added 17:xx (abtimeline.py, owner: strategy agent)
- `--seq <id...>`: whole-sequence audit (sales, 4.8k thresholds, item roles, one ledger, branches) -> evidence/path/<id>_sequence.txt.
- `--sales <id>`: JSON of sale-before-upgrade and 4.8k-drop findings; gate rule 4f blocks NEW findings unless waived with `waive:[{rule:'INVESTMENT'|'SALES', why (>20 chars), evidence}]`; pre-existing findings are printed only.
- `--profile <id...>`: contribution profile by match phase, only relevant activities, measured kept apart from modelled -> evidence/profile/.
- `--range <id> --at N`: derived distance sets, layouts, moving targets; requests need required_start_state, aba, order_alternation, invalid_if, ranges, layout, movement (see PLANNER_FIELDS.md; checked by lint_meta.py).
- CORRECTION: weapon reload IS in game data (`m_reloadDuration`, VERIFIED; Wraith 2.82 s equals the sandbox measurement). The earlier "not in vdata / ASSUMED 2.5 s" is withdrawn.

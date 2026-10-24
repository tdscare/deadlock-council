# Council protocol (one hero / one playstyle)

Conductor = the main session. It sequences agents, enforces gates, and is the only one that edits data.js (via `a19/merge.js`).

1. **Brief** (conductor): hero, playstyle (real ones only; two per hero where genuine), latest rules from memory.
2. **Facts** (`clerk` → `researcher`): kit sheet (every ability T1/T2/T3, cooldowns, scaling, charges), post-patch notes, same-style public builds. Output `evidence/<hero>.kit.md`. Gate: every number cites a game file or URL.
3. **Analyse** (`hero-analyst`, `item-analyst`, `ability-checker` in parallel; the ability timeline x item timing in `WEAKNESS_PROCESS.md` section M is computed here and re-checked after every reorder): what the kit needs; full item list tier by tier against the kit, with thresholds/procs checked at the buy point. Output candidate list + rejected list with reasons.
3b. **Weaknesses -> remedies** (`weakness-solver`, then `theorycrafter`): per `WEAKNESS_PROCESS.md`: discover weaknesses from the kit across all categories, enumerate remedy classes (item, ability use, positioning, target choice, team, accept), price each, test promising ones where the Sandbox can, decide (core / situational / playstyle / duo / leave alone), then re-sweep the new build for new weaknesses. Output `sandbox/weaknesses/<hero>_<build>.md`. Reviewer must challenge each chosen remedy and each "leave alone".
4. **Theorycraft** (`theorycrafter`): start from the kit-first build thesis process (`WEAKNESS_PROCESS.md` sections K and L (synergies and the marginal value of each purchase): engine mechanics -> consequences for stats, damage focus, farming, survivability timing, order, redundancies -> falsifiable thesis, rival theses, whole-progression verification, every item challenged on all roles). draft build + 1–3 *testable* hypotheses ("Vampiric Burst out-sustains Leech with Ricochet on 3 targets"). Each hypothesis becomes a scenario in `sandbox/scenarios/`.
5. **Compare** (`comparer`): spike math, slots, sell notes, walk1/check12 across drafts; shortlist.
6. **Test** (`sandbox-tester`): runs scenarios, writes `sandbox/results/*.json`. `tools/ledger.js` turns them into verdicts in `evidence/<hero>.json`.
7. **Decide** (theorycrafter + conductor): apply verdicts. Supports → keep. Refutes → change the build and record why in `changes`. Inconclusive → keep the calculation-backed choice, mark untested.
8. **Review** (`reviewer`, blind to reasoning): tries to break the build against RULES, CHECKLIST (A–L), evidence. Must list at least one concrete challenge per core item; any unresolved FAIL sends it back to 7.
9. **Finalise** (`builder` + `clerk`): write `<out>/<id>.js`, `OUT=<dir> node a19/merge.js <hero>`, `node a25/full.js`, `rebuild.sh`, `mkcodes.js`. Gate: full.js clean.
10. **Import** (`importer`): only when Kieran says; never overwrites his non-"Fully Annotated" builds.

Disagreement rule: two agents disagree → the one with A/B-graded Sandbox evidence or game-file numbers wins; otherwise `reviewer` adjudicates; Kieran only decides pure taste inside a playstyle he already set.

## cost-efficiency (added)
Runs after the builder and before the reviewer on every new or changed build: buy timing, value per soul, swap boxes re-walked for the 4.8k spike, cross-build comparison of when the same item is bought. FLAGs block the build like reviewer FAILs.


## HARD RULE (Kieran, 05:46): the only way to change a build is council/tools/gate.js
data.js and its backups are immutable (chattr +i). `node council/tools/gate.js check <proposal>` runs every validator on OLD and NEW and BLOCKS on any new violation (spikes, charge-before-charges, structure, notes, sells, thresholds), a missing reason/evidence, a stale base, or sandbox evidence (not accepted until the Sandbox results path is validated). `apply` additionally needs council/approvals/<name>.ok (sha256 of the proposal, written only after Kieran approves), snapshots the previous data.js, writes an auto-generated changes line (diff + reason + evidence + gate result) and logs to council/history/LOG.jsonl. Then run rebuild.sh and mkcodes and confirm the export round-trip (builds_check RT_*). Agents propose; they never write data.js. A rule here is only real if gate.js enforces it: list unenforced rules in council/audit/ENFORCEMENT.md.

## Patch handling (Kieran, 06:13): targeted, on request only
A new game build number is NOT evidence that data is outdated (most updates are backend/bug/visual). A full patch review runs only when Kieran says there is an update to account for: read the patch notes, diff the specific data (heroes, abilities, items, text), update only what changed, then reopen only the affected builds/tests (`node council/tools/queue.js reopen <buildIds> <why>`); all other validated results are preserved. If the Council independently finds concrete evidence that a value/mechanic changed, it flags that specific data "potentially outdated", avoids confident decisions on it, and tells Kieran; it never assumes the whole database is invalid.
Two limits on that rule: (1) "unchanged" is not "validated". Data that was never verified (missing active-item text, hardcoded constants, inferred costs, unverified mechanics) stays on the audit fix list regardless of patch diffs and carries its evidence level until verified. (2) For a changed shared mechanic, run `node council/tools/affected.js "<item|ability|mechanic keyword>"`: it lists every build owning the item, its components/upgrades, any item whose text mentions the mechanic, and heroes whose abilities mention it; reopen exactly that set.

## No OS input while Kieran uses the PC (Kieran, 12:49)
Sandbox testing runs only through the Deadlock plugin / server commands / queue runner. No agent or script may use computer_* (mouse, keyboard, focus) tools, send global input, or steal focus while the PC may be in use (he plays other games, e.g. Overwatch, in parallel). If a task truly needs the foreground (e.g. client reconnect), it is set `paused-needs-foreground` and reported in progress.txt; it never interrupts him. Computer-use steps need his explicit go-ahead.

# Audit: builds (agent "builds") — 81 builds in data.js vs claimed rules

Method: read-only. Script `council/audit/builds_check.js` (run `node council/audit/builds_check.js`, N=99 for all examples; full result json `council/audit/tmp/builds_check_full.json`, console `council/audit/tmp/check_out.txt`). Helpers in `council/audit/tmp/`: `drift.js`/`drift2.js` (data_pre_*.js vs data.js, spike/order diff + changes-line count), `spkclaims.js` (changes-line numbers vs walk), `show.js` (annotated walk), `claims.js` (text-vs-items, noisy, only used for leads). Walk model = a7/sp.js + audit/walk2.js (upgrade = difference, "Sell X for this" removes X). Existing tools reused as oracle: `node gen/chg_final.js before` (charge timing).
Levels: R/C/I/T per BRIEF.

## 1. Mechanical results over all 81 builds (current data.js)

| rule (source) | result | examples |
|---|---|---|
| core = exactly 12 slots (RULES "Core fills all 12") | PASS 81/81 | - |
| <=8 items/box | PASS 81/81 | - |
| ability order 16 clicks, <=4 per ability, ult taken | PASS 81/81 | - |
| no item twice anywhere in a build | PASS 81/81 | - |
| stale/disabled item names, items missing from importer's gamedata | PASS 0 | - |
| sell chain (sold item owned at that point) | 1 violation | graves: Ricochet "sells Extra Regen" which is not in core at that point |
| optional-box sell names an item not in core | 1 | haze: Divine Barrier sells Counterspell (Counterspell not in core) |
| exported code round-trip (imp/<id>.b64 decoded == data.js: boxes, optional flag, items, imbue targets, order) | PASS 81/81 (checked, with decoder; negative control: seven's decoded Early box has no Arcane Surge, matching current data) | - |
| **codes.js / codes.json** (mkcodes.js older output) | STALE: 19 of 81 builds, dated 2026-10-18 | missing e.g. seven_gun, ratking_grenade, vindicta... Live path is meta.js+enc.js+imp/*.b64 (fresh, 01:08 Oct 24); codes.js/json are dead files that look authoritative |
| site/index.html built from current data.js | PASS (contains data.js start+end); NOTE site/builds.html does not exist (builds.html is at SP root) | - |
| name <= 32 chars (RULES/CHECKLIST) | 6 violations | greytalon_gun 34, mcginnis_turret 34, pocket 34, infernus_dash 33, mirage 33, doorman 33 (names stored without the " (Fully Annotated)" suffix; limit applied by hand only to the 52-char final, so this is a CHECKLIST-vs-full.js mismatch) |
| Rich box = T4 only (CHECKLIST O: "no T3 in rich") | 5 violations | kelvin_support Rescue Beam T3; paige, seven_gun, mcginnis_turret Superior Duration T3; graves_tank Spirit Rend T3 |
| Slot locked note "Upgrade of X." only | 2 violations | viscous, solomon_support Healing Tempo carry an extra sentence |
| Counters desc format (Oct 22 "Dying after X? ... Sell Y.") and X,Y in build | PASS 81/81 (CHECKLIST G still documents the older "Get after X..." format: two conflicting formats in docs, data follows Oct 22) | - |
| notes: "never mention bugs", "X over Y" | PASS bug/over except 1 | haze has a note "if u die the game is over get this." (lowercase, informal; contradicts wording rules) |
| "no proc jargon" | 1 | nurse Spiritual Overflow: "Procs when you heal teammates." |
| core notes only when needed (RULES: "otherwise EMPTY") | 96 non-empty core notes in 51 builds that are not Upgrade/On/Sell/If style: judgement call, count only (e.g. danny Sharpshooter "Chimera's landing also scales with weapon damage.") | - |
| health 4.8k by ~16k (RULES health-spike timing: fighty 11-12k, sustain 14-16k) | 3 builds later or never-early | seven_gun health 4.8k at 40.0k (!), wraith 21.6k, geist 18.4k |
| overshoot: other colour >=8k invest when health 4.8k first lands ("8k or 10.4k spirit before any health is wrong") | 6 | seven_gun gun 19.2k + spirit 12.8k before any health at 40k; wraith gun 12.0k; haze gun 11.2k; geist gun 8.0k; ivy_carry gun 9.6k |
| main colour 4.8k > 8k souls | 23 builds (8 at >=12k) | danny spirit 11.2k, dynamo/dynamo_damage spirit 14.4k, bebop health 12.0k (main-colour = highest invest, crude; shown so reviewers see distribution) |
| 6.4k item before 20k ("no 6400s until ~20 min") | 4 | haze Ricochet @14.4k, wraith Ricochet @16.8k, victor Infuser @16.8k, celeste_carry Mercurial Magnum @19.2k |
| 3+ consecutive 6.4k before 30k | 0 | - |
| fresh T2 late (>20k) | 30 | danny_gun Mystic Vulnerability @20.8k, victor_gun Spirit Lifesteal @22.4k, ratking_grenade Battle Vest @24.0k (many are first-time imbue/utility T2s; rule says "T3/T4 or upgrades late") |
| every T1/T2 upgraded later or has a named sell (RULES "Assume slot-lock") | 77 items in 54 builds neither upgraded nor named in any sell (strict reading; many are deliberate end-state items such as danny Opening Rounds) | danny_gun Spirit Shielding @10.4k, bebop Enduring Speed @8.8k |
| charge items vs ability charge tier at buy (`gen/chg_final.js before`, strict AND lenient point model) | 9 builds buy Extra Charge/Rapid Recharge before the charged ability has charges | rem (EC @800, RR @15.2k; Pillow Toss gets charge at T3, strict 48.6k), sinclair_bolt (Sinclair has NO charge ability: EC @1.6k and RR @12.0k are dead), baba (EC @800, Threadsap T3 charge 9.2k strict), baba_tank (EC 1.6k, RR 23.2k vs 32.1k strict), lash (EC @17.6k, Grapple T3 48.6k strict), paige_support (EC 3.2k/RR 20k vs 32.1k), mcginnis_turret (EC 1.6k vs 2.0k), viscous (EC 3.2k vs 9.2k strict), infernus_dash (EC 4.0k vs 6.8-7.6k). `gen/proposals_charge.md` proposed deleting/replacing these ("proposals only, data.js untouched"); only some orderings were applied (viscous, lash moved), the dead-item cases remain. |
| threshold items (Mystic Burst >80, Tankbuster >165, Spirit Burn 500/5s, Reverb 100, RR 200, Arcane Surge, Overflow) | NOT mechanically provable here: no local damage-per-instance table at buy point except spirit power. 65 buy points have no "Threshold:" changes line (Spiritual Overflow 15, Spirit Burn 13, Mystic Burst 12, Tankbuster 11, Reverb 6, RR 5, Arcane Surge 3). Spot-check: bebop_bomb Mystic Burst @800 SP~9: Sticky Bomb 85 + 1.5x9 = 98 > 80 OK (abilities.vdata via ab.py). Early Mystic Burst at SP<=16 in viscous_damage @800, dynamo_damage @1.6k, geist_bomb @1.6k, pocket @4.0k: unverified here (pocket has a Threshold line, the others do not). Witchmail <20k 0, Tankbuster <8k 0, Spirit Burn <12k 0 (timing proxies pass). |
| ability order per same-style source | not checkable offline (needs source builds); only structural check passed | - |

## 2. Item moves / spike shifts with no changes line (coordinator lead)

Script `council/audit/tmp/drift2.js data.js.bak_rel` (bak_rel 10-23 00:03 -> data.js 10-24 01:08), full text `council/audit/tmp/d3.txt`.
- 33 builds changed core item ORDER; 31 of them got ZERO new `changes` lines; 28 of those shifted a 4.8k spike. 10 shifted a spike >=1.6k with no line: seven (spirit 4.8k 5.6k -> 13.6k, Arcane Surge Early 3.2k -> Late 18.4k), seven_gun (health 14.4k -> 40.0k, gun 5.6k -> 7.2k, Rapid Rounds+Swift Striker in, Enchanter's Emblem out), graves_ult (Arcane Surge 2.4k -> 25.6k, spirit 5.6k -> 13.6k, health 9.6k -> 8.0k; the SAME Arcane Surge Early->Late move as seven), geist (spirit 18.4k -> 16.8k, Healing Booster 9.6k -> 20.8k, Extra Charge 16.8k -> 34.4k), danny, bebop_bomb, rem, venator_grenade, silver, mokrill (1.6k each).
- Ability order changed with no line: seven 3311234442431122 -> 1331234442431122, seven_gun 3311234324141224 -> 1331234324141224.
- Mechanism: `gen/mv.js` rewrites data.js with a regex (item move before/after an anchor) and never touches `changes`; `gen/ac_sell.js`, `gen/rebox.js`, `gen/spikes.js` belong to the same pass (timestamps 10-23 19:59-22:40, backups data_pre_spikefix/pre_sevengun/pre_charge). The merge path (a19/merge.js) is not used for these edits.
- Stale numbers left in the final changes line because of it: ratking_grenade final line says "Gun 4.8k at 4.8k souls, health 4.8k at 11.2k"; walk gives gun 4.8k at 6.4k and health at 9.6k (backup diff: pre_sevengun -> pre_charge moved gun 4.8k -> 6.4k with no line). `spkclaims.js`: 2 of 9 spike claims in final changes lines disagree with the walk, both ratking_grenade.
- seven vs evidence: `evidence/cost/seven.md` (Oct 22 23:29) walks Arcane Surge @3200, spirit 4.8k @5.6k, verdict "OK per Seven rule (SoP/Arcane Surge early)". RULES_KIERAN Seven entry: "Surge of Power/Arcane Surge on his 3 early". Current build: Arcane Surge Late @18.4k. `gen/ac_out0.md` (ability check, 01:00 Oct 24, run on the already-moved build) says seven "OK" for the Arcane Surge note and does not compare placement against the rule. `sandbox/weaknesses/seven_worked_example.md` (05:38 today) independently proposes restoring Arcane Surge to Early and says "a rule moved it that is not recorded".

## 3. Paper trail, 8 builds (did findings change the build?)

| build | finding (source) | in data.js now? | level / gap |
|---|---|---|---|
| danny | cost: Sharpshooter right after Opening Rounds, counters sell Enchanter's Emblem, Surge before Greater Expansion (evidence/cost/danny.md, SUMMARY_0) | YES all three (Early: HV, Opening, Sharpshooter; counters "Sell Enchanter's Emblem"; changes line "Cost pass") | I. Later drift: health 4.8k now 14.4k vs 16.0k in the cost pass's own numbers, no line |
| bebop_support | cost HIGH: Knockdown swap drops gun below 4.8k -> Spirit Rend | YES (changes "Cost pass: Spirit Rend replaces Knockdown") | I |
| dynamo | cost HIGH same swap + Heroic Aura after Compress (spirit 18.4k->15.2k, gun 12.8k->18.4k) | swap YES; walk now spirit 14.4k, gun 17.6k (differs 0.8k, unrecorded) | I with silent drift |
| paige | cost MED: merge Slowing Hex/Vortex swaps; counters sell Greater Expansion not Express Shot | RICH_NOT_T4 still flags Superior Duration (T3) in rich; gun 4.8k now 4.8k (was 5.6k) via unrecorded move | partial |
| rem | cost: drop Superior Duration, Echo Shard after Healing Booster (24.0k), TC after Compress (9.6k)/(12.8k now) | YES except TC at 12.8k (walk) vs 9.6k claimed; Echo @24.0k, Superior Duration gone. But Extra Charge @800 / Rapid Recharge are dead (Pillow Toss charge T3); charge audit said "replace both", not applied | I for cost; C only for charge (proposal never merged) |
| infernus_dash | cost MED: Spiritual Overflow before Escalating Exposure (gun 4.8k @24.0k) | YES (walk gun 4.8k @24.0k). Extra Charge @4.0k still EARLY per chg_final; proposal "delete EC" not applied | I / C |
| ratking_grenade | relevance pass (evidence/relevance/ratking_grenade.md, Oct 22): range items out, Extended+Titanic Magazine in; Kieran/RULES + CHECKLIST O: no Glass Cannon on Rat King/tank | relevance change YES. Glass Cannon is FIRST item of the rich box (changes line 2 of an older round says "Glass Cannon out (Kieran's standing rule)"). Final-line spike numbers stale (see sec 2) | contradiction, see 4 |
| seven | cost "none required"; Kieran rule Arcane Surge early; worked example proposes restoring it | NOT restored; moved the other way, no line | R only for the rule; the move is untracked |
| (also) mirage, nurse | `evidence/review2/*.md` exist for these 2 only | changes line "Review 2" present for mirage | I; reviewer evidence exists for 2 of 81 builds; relevance for 3; cost for all (86 files) |

Pattern: cost-efficiency findings were applied through APPLY_BRIEF chunks (apply/chunk*/out -> merge) and are visible in `changes` ("Cost pass:"); every later pass (spikefix, charge, ac, sevengun) edited data.js directly. Findings from the ability check (`gen/ac_out*.md`) proposed 2 edits in batch 0; nothing in the output examined item placement against Kieran's per-hero rules. `ability-checker` is named in PROTOCOL.md and ROUTING.md but `council/agents/` has no such file (R only).

## 4. Stated reasoning contradicting the item list

- ratking_grenade: Rich box starts with Glass Cannon; a changes line records Glass Cannon removed as a Kieran rule; CHECKLIST O: "Glass Cannon never on a health/tank build"; RULES: "Rat King: no Extra Charge, no Glass Cannon; tanky". (vyper_gun also has Glass Cannon in rich; Vyper is not tank-named, so only ratking_grenade is a hard contradiction.)
- ratking_grenade final changes line: gun 4.8k "at 4.8k souls", health "11.2k"; walk 6.4k / 9.6k.
- seven: RULES + cost evidence say Arcane Surge early; build has it Late, changes silent. seven_gun: health 4.8k at 40.0k, 5th-from-last item, with gun 19.2k and spirit 12.8k first; RULES "Don't overshoot 8k... before any health", "in-your-face heroes need the health spike"; its "Cost pass" line speaks of gun 4.8k landing earlier but says nothing about health moving from 14.4k to 40k.
- sinclair_bolt: Extra Charge + Rapid Recharge in core on a hero with no charge upgrade on any ability (gen/proposals_charge.md says so) — build reasoning ("charges") cannot be true.
- RULES (Oct 22 Counters premise: menu, cheapest first) vs data: only desc format is checked, not "cheapest first" ordering inside Counters boxes (not tested by me; no tool does it).
- haze note "if u die the game is over get this." violates "no AI/informal wording, simple player-facing".
- Name length: CHECKLIST says <=32, six builds are 33-34.
- Rich box rule "only pricier versions of something in the build": mechanical test only for tier; kelvin rich Mystic Reverb was removed for exactly this reason in Round 14 then re-added in Round 20 (changes lines 11 and 15) with the reason unaddressed.

## 5. Is there ONE place where kit, synergy, ability points, thresholds, farming, order, spikes are evaluated together?

- Separately: walk1/check12 (slots, spikes, notes), sp.js (spirit power + tiers per buy, thresholds by hand), cost-efficiency agent (timing/spikes/swaps), reviewer (checklist A-P prose), charge scripts (gen/chg_*), ac scripts (gen/ac0, imbue vs scaling), full.js (walk+check12+names).
- Closest combined tool: `council/tools/abtimeline.py` (docstring: ability timeline x item timing + conditional rows; model A game points vs model B old). Ran its output for seven (`council/sandbox/abtimeline/seven.txt`): per buy it shows souls, level, AP, spirit power, every ability's tier (both models), charges, cooldown, damage and spirit-hit values. Files are dated 10-24 05:42 (after the audit brief). No build edit predates it, so its output has not gated any build (C, with a real run on seven; not I). It does not compute spike/overshoot flags or check Kieran per-hero rules and does not print PASS/FAIL (grep for UNCHECKED: 0 files; 78 files contain EARLY/LATE-type words, unreviewed).
- The conductor protocol says the reviewer is blind to reasoning and checks CHECKLIST A-P (prose), but there is no reviewer output for 79 of 81 builds, and no `evidence/<hero>.kit.md` or `evidence/<hero>.json` ledger exists (PROTOCOL steps 2 and 6 are R). weaknesses/ has 5 heroes (abrams, abrams_melee, victor_gun, victor_spirit, wraith_wraith) + 2 worked examples.
- Answer: no single gate; combination happens only in the conductor's head. Nothing re-runs the full check after a direct data.js edit (gen/mv.js etc. do not call full.js; I ran a25/full.js logic via my script and it found issues above).

## 6. Classification of claims touched

| claim | level | evidence |
|---|---|---|
| walk1/check12/full.js structural checks | T (run on 81 builds: 0 slot/dup/stale failures) | my script |
| exported code == build | T (decode of imp/*.b64 all 81 equal) | builds_check.js RT_* = 0 |
| codes.js/json current | R only (stale, 19/81) | file dates |
| spikes race to 4.8k main colour, health timing, no overshoot | C (walk1 prints spikes) not gated: 23 late-main, 6 overshoots, 3 health >16k | sec 1 |
| charge items need charge ability | C (chg scripts) never merged; 9 builds still violate | chg_final before |
| thresholds checked | C/partial (sp.js, a7); no gate; 65 buy points with no Threshold line | sec 1 |
| cost-efficiency changes final build | I (visible "Cost pass" lines, 86 evidence files) | sec 3 |
| reviewer gate on every build | R (2 review files) | evidence/review2 |
| ability-checker agent | R (no agent file) | agents/ |
| single combined evaluation | C (abtimeline.py, new, unused by edits) | sec 5 |
| changes line records every item move | R, false: 31 builds moved with no line | sec 2 |

## TOP 10 gaps by impact on build correctness
1. Direct data.js edits (gen/mv.js etc.) bypass merge, changes and full.js: 31 builds reordered, 28 shifted spikes, no record, and later "verification" runs on the moved result (ac_out0 OK on seven).
2. seven: Arcane Surge Early -> Late (spirit 4.8k 5.6k -> 13.6k) contradicts RULES and its own cost evidence; same move on graves_ult (spirit 5.6k -> 13.6k).
3. seven_gun: health 4.8k at 40.0k with 19.2k gun / 12.8k spirit invested first.
4. Dead charge items in core on 9 builds (sinclair_bolt has no charge ability at all; rem, baba, baba_tank, paige_support, lash, mcginnis_turret, viscous, infernus_dash too early); proposals never merged.
5. Glass Cannon in ratking_grenade rich box against both RULES and CHECKLIST O; stale spike claims in its changes line (gun 4.8k 6.4k not 4.8k).
6. No automatic gate: PROTOCOL's ability-checker agent does not exist, reviewer ran on 2 builds, kit/ledger evidence files absent; abtimeline.py (the only combined view) is new and unused in any edit.
7. Threshold items (Spiritual Overflow, Spirit Burn, Mystic Burst, Tankbuster, Reverb, RR, Arcane Surge) at 65 buy points have no recorded Threshold evidence; early Mystic Burst at SP<=16 unverified on viscous_damage, dynamo_damage, geist_bomb.
8. Health spike late/overshoot: wraith 21.6k, geist 18.4k, haze 16k with gun 11.2k, ivy_carry gun 9.6k first; 4 six-hundred-forties before 20k.
9. codes.js/codes.json stale (19/81) alongside the fresh imp/*.b64 pipeline; two files look like the export source.
10. Rule-text inconsistency and unenforced rules: Counters desc format (CHECKLIST G vs Oct 22), name length 32 vs 52, rich box T3 items (5), name length (6), informal haze note, jargon in nurse, graves sell of an unowned item, haze Divine Barrier selling a non-core item.

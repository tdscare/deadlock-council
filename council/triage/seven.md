# seven (Power Outage Seven, ult build) - triage vs CLEANBASE
Base: council/frozen/data.CLEANBASE_pre_spikefix.js. Current: data.js. Proposal: council/proposals/seven.json -> council/work/seven.js (gate check: PASSES, not applied). Calc files: council/triage/seven_calc/ (m7.py, cmp.py, early.py; tables seven_N_compare.txt, seven_paths.txt, early_orders.txt).
Grade of everything below: calculated, unvalidated (kit/item maths from game files). The percentages are model outputs, not measured accuracy. No evidence/seven.json exists, so no measured verdicts to apply; every scenario below is pending.
Game data: 6801 files; 6819 changed no hero/item stat (council/audit/GAMEDATA_6819.md). Item prices are tier prices (800/1600/3200/6400), secondary evidence (wiki).

## What changed since the clean base (silent, no changes line; audit/builds.md:41-45)
1. Arcane Surge moved from Early (3.2k, before Surge of Power) to Late (18.4k). Spikes: spirit 4.8k 5.6k -> 13.6k, health 4.8k 12.8k -> 11.2k.
2. Ability order 3311234442431122 -> 1331234442431122.

## Verdicts
| change | verdict | evidence |
|---|---|---|
| Arcane Surge Early -> Late | MISTAKE | Kieran's Seven rule: "Surge of Power/Arcane Surge on his 3 early". Path comparison (seven_N_compare.txt): proposed vs current, Power Surge per proc +18% (no dash-jump) / +38% (with) at 5.6k-7.2k, +12/+30% at 8.8k, +15/+29% at 12.0k; storm DPS +10% at 5.6k. Cost of the restore: health 4.8k at 12.8k instead of 11.2k (HP -4% at 10.4k, -12% at 12.0k, equal from 12.8k). The gain holds without the dash-jump because the 4.8k spirit invest bonus (38 spirit) lands 8k souls earlier. The same-move on graves_ult is not in scope here. |
| Order 3311 -> 1331 | LEGIT intent, wrong result | Kieran (reqs D3): "first point in Lightning Ball for 2nd charge". Under the game-data unlock model (FOUNDATIONS F2/F5, strict and non-strict queue give identical rows) 1331 leaves ball T1 at 900 souls, same as 3311; it only unlocks ball instead of Power Surge at 0. 1133 gives ball T1 at 200 (Power Surge unlock 500, T1 900). Under the old model B, 1331 is the right string and 1133 would push Power Surge T1 to 2000. Chosen: 1133 (model A = game data). |

## Rival paths compared (same items, whole progression; seven_N_compare.txt)
- R (proposed): spirit 5.6k, Cultist 8.0k, health 12.8k.
- CUR: spirit 13.6k, health 11.2k: lower damage 4k-13.6k, see above.
- G greens before Cultist: same damage, health 10.4k, Cultist 12.8k (one 270 s Cultist cycle later). Rejected on Kieran's rule (Cultist early on this farm build) and its own line "greens come straight after Cultist". Hypothesis seven_N1.
- H health first: spirit 10.4k, Cultist 12.8k: rejected. S (Surge of Power then Arcane) and C (Cultist before Surge of Power): same or later spikes, no gain.
- Insurance pair (Unstoppable+Infuser rush): not reopened; the worked example's "don't rush" stays (model-only lead).

## Corrected progression (council/work/seven.js)
Early: Monster Rounds, Extra Spirit, Extra Stamina, Arcane Surge, Surge of Power (Power Surge), Cultist Sacrifice. Mid: Spirit Lifesteal, Sprint Boots, Healbane, Enduring Speed, Mystic Vulnerability, Duration Extender (ult), Compress Cooldown (Power Surge), Mystic Expansion (ult). Late: Escalating Exposure, Superior Duration, Unstoppable, Superior Cooldown, Infuser, Greater Expansion, Diviner's Kevlar. Optional boxes unchanged. Order 1133234442431122.
walk1: spirit 4.8k @5.6k, health 4.8k @12.8k, 46.4k, 12 slots, FLAGS none.

## Gate (node council/tools/gate.js check council/proposals/seven.json)
Fixed: MAIN_4.8K_LATE (spirit 4.8k at 13.6k). New: only RT_* export round-trip (ignored by the gate until rebuild).
UNRESOLVED in the resulting build (pre-existing):
- CORE_NOTE_NONEMPTY Arcane Surge / Unstoppable / Infuser notes: cannot fix without deleting notes the rules allow (niche how-to-use tips: dash-jump trigger; Unstoppable before the ult because only a stun ends Storm Cloud; Infuser when they're in the storm). The checker only whitelists note prefixes.
- T1T2_NOT_UPGRADED_OR_SOLD Enduring Speed: false positive; Juggernaut (its upgrade, components [Enduring Speed]) is in Slot locked with "Upgrade of Enduring Speed." The checker only looks in core and "Sell" text. Can't fix without breaking the box rules.

## Open questions and which conclusions depend on them
- Unlock-vs-AP queue (F5c): no effect, strict and non-strict identical for these orders.
- Model A vs old model B for reading the order string: the order verdict flips (A: 1133, B: 1331). Nothing else depends on it.
- 1-charge counting (F7): no charge item in this build; affects only whether Cultist's +1 charge acts on the 1-charge ball before T1 (not decision-relevant after 900 souls).
- Item data that could change the conclusions if numbers change: Arcane Surge +20 spirit (conditional) and its Extra Stamina component; Surge of Power ImbuedTechPower 28; Power Surge DamagePerChain 10 +0.14x (+8, +0.23x at T2); Tech invest table (4.8k -> 38); Cultist 270 s cd / 170% souls; vitality invest table (HP). 6819 changed none of these.
- Model-only: no animation, positioning, enemy play; dash-jump use before Power Surge assumed in the "with dash" numbers; HP ignores Cultist's +4/boon.

## Scenarios (council/sandbox/scenarios/)
seven_N0_order_ball_first (1133 vs 1331 lane damage, needs abil-op logging), seven_N1_greens_before_cultist, existing seven_L4_arcane_early (Arcane Surge early). Verdicts: none yet; build keeps the calculated choice.
Note: council/work/seven.js previously held the worked example's proposal (same items, order 1331); copied to council/work/seven.worked_example_0535.js before overwriting.

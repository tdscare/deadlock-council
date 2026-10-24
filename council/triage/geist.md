# geist (Rizuhble's Stubborn Old Geist) - triage vs CLEANBASE

Confidence for every verdict: calculated, unvalidated. Game data gt/repo 6801 (identical to installed 6819 for all hero/item stats, council/audit/GAMEDATA_6819.md). Prices tier-based (800/1600/3200/6400, wiki, secondary).
Evidence: council/work/tri2/geist_paths.txt (8 whole-build paths, checkpoints 3.2k-43.2k, all three point models), council/work/tri2/ap_models.txt, council/work/tri2/geist_waiver_fresh_t2.txt.

## What changed since CLEANBASE (silent, no changes line)
| # | Change | Effect on walk | Verdict |
|---|---|---|---|
| 1 | Healing Booster 9.6k -> 20.8k (Mid -> Mid cont.) | health 4.8k 12.8k -> 18.4k; Spirit Resilience/Berserker 800 earlier | MISTAKE |
| 2 | Extra Charge 16.8k -> 34.4k (just before Rapid Recharge) | spirit 4.8k 18.4k -> 16.8k; BRS/lifesteals 1.6k earlier | MISTAKE |
| 3 | Extra Charge note "Life Drain gets charges once it's maxed. This adds one." emptied | - | LEGIT (notes never explain conditions; builder guarantees them by order) |

1. Healing Booster: +800 souls (upgrade of Extra Regen) for +20% heal amp. At 9.6k it amplifies Life Drain (T3 from 6.8k) and Radiant Regeneration. Current path vs corrected at the same souls: heal per Life Drain charge 322 vs 387 (9.6k), 339 vs 407 (12.8k), 434 vs 553 (19.2k); HP -50 to -335 from 9.6k to 19.2k; health 4.8k at 18.4k is past Geist's 14-16k window (validator HEALTH_4.8K_AFTER_16K and OVERSHOOT_GUN_BEFORE_HEALTH, both fixed by the correction). What the move bought: Spirit Resilience/Berserker 800 earlier, BRS/lifesteals 1.6k earlier (+9% weapon damage 17.6k-18.4k). Not worth it.
2. Extra Charge: Life Drain has AbilityCharges 0 until T3, then 3 (abilities.vdata ability_life_drain). T3 lands at 6.8k (model A and A-strict) or 4.6k (model B), so at 16.8k it gives a 4th charge under every point model. Moving it to 34.4k removed the 4th charge for 17.6k souls (bank 3 x 460 = 1380 vs 4 x 460 = 1839 at 17.6k) to land the spirit 4.8k 1.6k sooner. Corrected order keeps spirit 4.8k at 18.4k (800 over, allowed "a bit over").

## Open mechanics questions, shown both ways
- F7 (does a 1-charge ability count for Extra Charge?): no Geist ability ever has 1 charge (Bomb/Malice/Soul Exchange 0 always, Life Drain 0 -> 3 at T3). Both readings give identical verdicts: Extra Charge does nothing before Life Drain T3, +1 after. No conclusion depends on F7.
- Unlock-vs-AP queue (F5c): independent queues vs one strict queue differ only below 1.4k (Malice T1 200 vs 500, Life Drain T1 900 vs 1400); Life Drain T3 6.8k in both. Model B (old, 1 AP per tier): T3 4.6k. No item verdict changes.
- New finding: Cultist Sacrifice's buff carries the same MODIFIER_VALUE_BONUS_ABILITY_CHARGES +1 as Extra Charge (ConditionallyApplied, during the buff). If it applies, Life Drain has 4 charges during the buff from 6.8k and 5 with Extra Charge. Untested: scenario geist_drain_charges.

## Paths compared (section N)
| path | gun/health/spirit 4.8k | at 12.8k | at 17.6k | verdict |
|---|---|---|---|---|
| G0 corrected | 6.4k / 12.8k / 18.4k | HP 2768, 30% spirit resist, 407/drain | 4 charges, 1839 bank, 72% wd | chosen |
| G1 current data.js | 6.4k / 18.4k / 16.8k | HP 2435, 339/drain | 3 charges, 1288 bank, 81% wd | rejected |
| G2 HB early, EC late | 6.4k / 12.8k / 17.6k | = G0 | 3 charges, 1546 bank, 81% wd | close; loses 4th charge to 34.4k |
| G3 lifesteals as the health spike, Spirit Resilience 21.6k | 6.4k / 12.8k / 18.4k | HP 2948, 13%/13% lifesteal, 0% spirit resist | 1950 bank | hypothesis (geist_lifesteal_vs_spirit_resilience): wins vs gun, loses vs spirit; Spirit Resilience is Kieran's in-game health item |
| G4 Berserker before health | 6.4k / 16.0k / 18.4k | gun 8k, no resist | - | rejected (damage, health spike, then damage) |
| G5 Extra Charge at 7.2k | 6.4k / 13.6k / 18.4k | bank 1758 vs 1221, HP -481 | wd 72 vs 72 | hypothesis (geist_extra_charge_timing), untestable-high-risk: depends on fight length |
| G6 health before gun | 10.4k / 7.2k / 18.4k | - | - | rejected (gun 4.8k 4k later) |
| G7 lifesteals before Berserker | 6.4k / 12.8k / 15.2k | = G0 | gun 8k only at 21.6k | rejected (main colour starved 5.6k) |

## Corrected progression (council/work/geist.js)
Early: Monster Rounds, Extra Regen, Mystic Regeneration, Extra Stamina, Kinetic Dash, Cultist Sacrifice (gun 4.8k 6.4k)
Mid: Radiant Regeneration, Healing Booster, Spirit Resilience (health 4.8k 12.8k), Berserker (gun 8k 16.0k), Extra Charge, Bullet Resist Shredder (spirit 4.8k 18.4k), Bullet Lifesteal, Spirit Lifesteal | Spellslinger, Blood Tribute
Late: Leech, Rapid Recharge, Refresher. Core 43.2k, 12 slots. Ability order unchanged (3231224233444111). Boxes unchanged.

## Gate (node council/tools/gate.js check council/proposals/geist.json): PASSES
- WAIVED FRESH_T2_LATE Spirit Lifesteal @21.6k: Leech component; every all-T2-under-20k order costs the health spike (G1) or the main gun 8k (G7). Evidence geist_waiver_fresh_t2.txt.
- UNRESOLVED CORE_NOTE_NONEMPTY Spirit Resilience note: kept, the claim is verified (citadel_heroes_english.txt:1955 "Self damage type is Spirit and can be mitigated"), niche tip; validator only accepts notes starting Upgrade/On/Sell/If/Vs/Only/When. Can't fix without deleting a true, allowed note.
- UNRESOLVED T1T2_NOT_UPGRADED_OR_SOLD Healing Booster: its upgrade Healing Tempo is in Slot locked; the validator only counts core upgrades or "Sell X" text. Pre-existing; can't fix without inventing a sell.

## Model-only (not in game files / not measured)
Vitality invest flBonus read as % base health; Healing Booster cast amp applies to Life Drain heals; drain heal = drained damage (LifeDrainHealthMult 100) with no resist; one charge recharges per AbilityCooldown (F8); AP costs 1/2/5 (F4); Cultist buff stats counted as always on (all paths own it, so comparisons are unaffected). Item-data dependencies (unchanged in 6819): Healing Booster 20%, Extra Charge +1/+7 charged spirit, Rapid Recharge +2/-14% cd, Life Drain T3 +3 charges/+0.45 scale, Spirit Resilience 30%, lifesteal 13%, invest tables.
Scenarios: geist_healing_booster_drain, geist_drain_charges, geist_extra_charge_timing, geist_lifesteal_vs_spirit_resilience (council/sandbox/scenarios). No council/evidence/geist.json results exist, so all are inconclusive and nothing was changed on them.

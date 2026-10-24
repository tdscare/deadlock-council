# ratking_grenade (Rizuhble's Trash Lobber Rat King) - triage vs CLEANBASE

Confidence for every verdict: calculated, unvalidated. Game data gt/repo 6801 (identical to installed 6819 for all hero/item stats, council/audit/GAMEDATA_6819.md). Prices tier-based (wiki, secondary).
Evidence: council/work/tri2/ratking_grenade_paths.txt (7 whole-build paths, checkpoints, three point models), council/work/tri2/ap_models.txt, council/work/tri2/ratking_waiver_main.txt.
Kit: Scrap Grenade 70 per detonation (+70 T2, +1 detonation and 300 (+1.0x) big blast T3) + 0.6x EBaseWeaponDamageIncrease (weapon invest bonus + Weapon Damage %); ult 200 + 1.2x the same. Gun is the damage colour.

## What changed since CLEANBASE (silent, no changes line)
| # | Change | Verdict |
|---|---|---|
| 1 | Battle Vest 6.4k -> 24.0k (Late) | MISTAKE |
| 2 | Sprint Boots + Enduring Speed 7.2k/8.0k -> 3.2k/4.0k, before Cultist | MISTAKE |
| 3 | Cultist Sacrifice 4.0k -> 6.4k | MISTAKE (consequence of 2) |
| 4 | Titanic Magazine before Cultist (2.4k) | LEGIT (neutral) |
| - | Glass Cannon in rich box (pre-existing in CLEANBASE too) | MISTAKE |
| - | Final changes line ("Gun 4.8k at 4.8k souls, health 4.8k at 11.2k, gun 8k on Hollow Point at 14.4k") stale for data.js (actual 6.4k / 9.6k / 12.8k) | stale; the corrected build matches it again |

1. Battle Vest at 24k is a fresh T2 late (validator FRESH_T2_LATE, Kieran rule) and loses 18% Weapon Damage above 65% health (+10.8 per detonation) and 18% bullet resist for 17.6k souls: grenade cast 1326 vs 1387 at 14.4k, 0% vs 18% bullet resist 6.4k-24k. The Counters box also sells Battle Vest, so it has to be an early item.
2/3. Boots first pushed the gun 4.8k to 6.4k and Cultist (farming) 2.4k later: grenade cast 472 vs 559 at 4.8k (-16%), 562 vs 594 at 6.4k. Rat King base speed 6.8 vs 7.2 default is slightly slow, but the boots still arrive at 7.2k/8.0k; no computed weakness justifies the delay.
4. Titanic before Cultist vs after: both land gun 4.8k at 4.8k; +9% weapon damage from 2.4k vs Cultist 800 souls sooner. Both effects are tiny (est. under 100 souls or 100 damage); kept as is.
Glass Cannon: -13% max health shrinks the cape (15%/25% of max health) and fights Colossus/Fortitude; Kieran: no Glass Cannon on Rat King / never on health-tank builds; it is not a pricier version of anything in the build. Removed, not replaced.
Also: Cheat Death's sell moved from Hollow Point (35% weapon damage, 125 HP) to Titanic Magazine (14%): cheaper loss, and Titanic now has a named sell (validator T1T2_NOT_UPGRADED_OR_SOLD fixed).

## Open mechanics questions, shown both ways
- F7 (1-charge abilities): only Rat Swarm has 1 base charge (2 at T1). No charge item is in this build, so no verdict depends on it. Cultist's buff carries the same +1 ability charges modifier; if 1-charge counts, Rat Swarm gets 2 charges at unlock during the buff. Probe: ratking_cultist_charge_rats (also answers F7 for every build).
- Unlock-vs-AP queue: independent vs strict differ only in Rat Swarm unlock (1.4k vs 2.0k); grenade T1 200, T2 2.0k, T3 6.8k in both; model B T3 at 2.6k. No item verdict changes.

## Paths compared (section N)
| path | gun/health 4.8k | key numbers | verdict |
|---|---|---|---|
| R0 CLEANBASE | 4.8k / 11.2k | 559 per cast at 4.8k, 18% BR from 6.4k | equal to R2 |
| R1 current data.js | 6.4k / 9.6k | +444 HP at 9.6k; -16% grenade 4.8k, no BR until 24k, 1326 vs 1387 at 14.4k | rejected |
| R2 corrected | 4.8k / 11.2k (6.4k same buy), gun 8k 14.4k | 594 at 6.4k, 1387 at 14.4k | chosen |
| R3 Fortitude before boots | 4.8k / 9.6k | +444 HP, +67 cape at 9.6k; move speed 8.0k -> 11.2k | hypothesis (ratking_health_before_boots), untestable-high-risk |
| R4 boots first, Battle Vest early | 6.4k / 11.2k | -16% grenade 4.8k | rejected |
| R5 Hollow Point before health | 4.8k / 14.4k | +15% grenade 11.2k, -613 HP | rejected (health spike after 12k on a no-sustain hero) |
| R6 health 4.8k by 8k | 9.6k / 4.8k | -19% grenade at 4.8k, Cultist 8.0k | rejected |

## Corrected progression (council/work/ratking_grenade.js)
Early: Extended Magazine, Monster Rounds, Titanic Magazine, Cultist Sacrifice (gun 4.8k 4.8k), Battle Vest, Sprint Boots, Enduring Speed
Mid: Extra Health, Fortitude (health 4.8k/6.4k 11.2k), Hollow Point (gun 8k 14.4k), Mystic Expansion, Compress Cooldown, Ballistic Enchantment, Superior Cooldown, Greater Expansion (spirit 4.8k 24k)
Late: Echo Shard, Witchmail, Colossus. Core 43.2k, 12 slots. Rich: Mystic Reverb, Cheat Death (sell Titanic Magazine), Refresher. Ability order unchanged.

## Gate (node council/tools/gate.js check council/proposals/ratking_grenade.json): PASSES
- MAIN_4.8K_LATE (health 4.8k at 11.2k): pre-existing, waiver recorded: validator takes health as main by total souls; damage colour is gun; no order reaches health 4.8k by 8k without delaying the grenade (R6).
- CORE_NOTE_NONEMPTY Extended Magazine: true (8% Weapon Damage feeds the grenade) niche tip; validator prefix rule. Kept.
- T1T2_NOT_UPGRADED_OR_SOLD Enduring Speed: upgrade Juggernaut is in Slot locked; validator ignores Slot locked. Can't fix without inventing a sell.
- c12 Bullet Resist Shredder swap colour change: walked, health 4.8k still at 11.2k (Sprint 800 + Enduring 800 + Extra Health 800 + Fortitude 2400), gun 4.8k unchanged.

## Model-only
Battle Vest/Hollow Point Weapon Damage reaching the grenade (same stat, ConditionallyApplied above 65%: scenario ratking_battle_vest_grenade); vitality bonus as % base health; Cultist buff always on in the numbers; AP costs 1/2/5; no resists. Range-item question unchanged (ratking_grenade_range_bonus, no results). Rich-box Cheat Death and Mystic Reverb were not re-litigated: both are T4 and match "pricier version of what the build does" only loosely (survival / grenade damage); UNKNOWN.
Item-data dependencies (unchanged in 6819): Battle Vest 18/18, Hollow Point 35, Titanic 14, Glass Cannon -13% max health, grenade 0.6x, cape MaxHealthPct 15/+10, invest tables.

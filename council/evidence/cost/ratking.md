# Cost-efficiency audit: ratking (Rizuhble's Unkillable Rat King)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@7200, spirit never, health@11200. End of core: 44800 souls, gun 14400 / spirit 3200 / health 25600, 12 slots.

Result: INFO spirit 3.2k never 4.8k (grenade scales off weapon damage by design); LOW Close Quarters 800 @8.0k waits 24k souls for Point Blank
Minimal fix: none required; lost-lane reorder box tested harmless

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Extra Health | 800 | v1 | HP 263 | 800/0/800 | OK (info: bought 1600 vs median 8800 in 20 other builds, no action) |
| 3 | 2400 | Monster Rounds | 800 | w1 | utility | 1600/0/800 | OK |
| 4 | 3200 | Sprint Boots | 800 | v1 | utility | 1600/0/1600 | OK (info: bought 3200 vs median 8800 in 39 other builds, no action) |
| 5 | 4000 | Mystic Expansion | 800 | s1 | utility | 1600/800/1600 | OK (info: bought 4000 vs median 10400 in 29 other builds, no action) |
| 6 | 4800 | Opening Rounds | 800 | w2 | SP 4.4 WD% 5.0 | 2400/800/1600 | OK (info: bought 4800 vs median 2400 in 15 other builds, no action) |
| 7 | 7200 | Cultist Sacrifice | 2400 | w3 | HP 16 WD% 3.1 | 4800/800/1600 | OK: 7.2k (2400 paid): rule says strong on farm-struggling heroes ~8 min; gun 4.8k lands here. |
| 8 | 8000 | Close Quarters | 800 | w1 | utility | 5600/800/1600 | FLAG LOW: 800 @8.0k, consumed by Point Blank @32.0k (ratio 5.0). Close-range hero so +20 weapon power and 20% melee resist work meanwhile. [vs 13 other builds: median 1600, min 800 vyper_gun, max 10400 apollo_melee] |
| 9 | 10400 | Fortitude | 2400 | v3 | HP 117 | 5600/800/4000 | OK |
| 10 | 11200 | Enduring Speed | 800 | v2 | utility | 5600/800/4800 | OK |
| 11 | 12800 | Fleetfoot | 1600 | w2 | WD% 3.8 BR% 3.8 | 7200/800/4800 | OK: 12.8k T2 dead-end, named sell for the counter. |
| 12 | 14400 | Compress Cooldown | 1600 | s2 | utility | 7200/2400/4800 | OK |
| 13 | 16000 | Return Fire | 1600 | v2 | BR% 6.3 | 7200/2400/6400 | OK: 16.0k conditional T2; rule: Return Fire a must for Rat King. Named condition in note. |
| 14 | 19200 | Berserker | 3200 | w3 | BR% 2.5 | 10400/2400/6400 | OK |
| 15 | 21600 | Ballistic Enchantment | 2400 | w3 | utility | 13600/1600/6400 | OK |
| 16 | 28000 | Siphon Bullets | 6400 | v4 | WD% 2.3 BR% 1.6 | 13600/1600/12800 | OK |
| 17 | 29600 | Superior Cooldown | 1600 | s3 | utility | 13600/3200/12800 | OK |
| 18 | 32000 | Point Blank | 2400 | w3 | HP 23 | 16000/3200/12800 | OK (info: bought 32000 vs median 16800 in 10 other builds, no action) |
| 19 | 38400 | Colossus | 6400 | v4 | WD% 2.3 | 14400/3200/19200 | OK |
| 20 | 44800 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 14400/3200/25600 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 14400/3200/25600 | gun@7200, spirit never, health@11200 | 12 | 44800 |
| Lost-lane reorder: Cultist Sacrifice right after Sprint Boots | mv:Cultist Sacrifice>after:Sprint Boots | 14400/3200/25600 | gun@7200, spirit never, health@11200 | 12 | 44800 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 14400, spirit 3200, health 25600. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Spikes: gun @7.2k, health @11.2k; end gun 14.4k, health 25.6k.
- Gun / spirit / health 4.8k: gun @7200, spirit NEVER (end 3200), health @11200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

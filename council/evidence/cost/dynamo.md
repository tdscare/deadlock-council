# Cost-efficiency audit: dynamo (Rizuhble's Babysitter Dynamo)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@12800, spirit@18400, health@8800. End of core: 41600 souls, gun 6400 / spirit 19200 / health 16000, 12 slots.

Result: HIGH swap 'Knockdown instead of Heroic Aura': gun 6.4k>3.2k, 4.8k never; MED spirit 4.8k only @18.4k (gun 6.4k first) on a healer; LOW Enchanter's Emblem fresh T2 @20.0k; LOW Warp Stone/Headhunter sells cross 16k/4.8k
Minimal fix: Swap box: Spirit Rend (gun T3) instead of Heroic Aura (tested, spikes unchanged); move Heroic Aura after Compress Cooldown (spirit 4.8k 18.4k>15.2k, gun 4.8k 12.8k>18.4k)

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Charge | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 2400 in 31 other builds, no action) |
| 2 | 1600 | Headshot Booster | 800 | w1 | HP 38 | 800/800/0 | OK |
| 3 | 2400 | Extra Regen | 800 | v1 | utility | 800/800/800 | OK |
| 4 | 3200 | Healing Rite | 800 | v1 | utility | 800/800/1600 | OK (info: bought 3200 vs median 1600 in 4 other builds, no action) |
| 5 | 5600 | Rescue Beam | 2400 | v3 | utility | 800/800/4000 | OK: 5.6k, 2400 paid (Healing Rite consumed), health 4.0k, heals ally 20% max hp: pays at once for a support; 0.44 ratio is intended. [vs 3 other builds: median 12800, min 9600 viscous, max 20800 doorman_support] |
| 6 | 8000 | Headhunter | 2400 | w3 | HP 16 WD% 1.6 | 3200/800/4000 | FLAG LOW: Rich Refresher sells this: gun 6.4k>3.2k (loses 4.8k and 6.4k). Sell Healing Booster instead. |
| 7 | 8800 | Sprint Boots | 800 | v1 | utility | 3200/800/4800 | OK |
| 8 | 9600 | Trophy Collector | 800 | v2 | utility | 3200/800/5600 | FLAG LOW: Rich Lightning Scroll sells this: health 16.0k>14.4k (loses the 16k step). Sell Duration Extender-line item instead. |
| 9 | 12800 | Heroic Aura | 3200 | w3 | FR% 8.1 BR% 5.3 | 6400/800/5600 | FLAG HIGH: Gun spike carrier: Headhunter 3.2k + Heroic Aura 3.2k. Knockdown swap leaves 3.2k. Also bought 12.8k before any spirit item: ordering below. |
| 10 | 13600 | Healing Booster | 800 | v2 | utility | 6400/800/6400 | OK (info: bought 13600 vs median 7200 in 21 other builds, no action) |
| 11 | 16000 | Rapid Recharge | 2400 | s3 | utility | 6400/3200/6400 | FLAG MED: Spirit block (Rapid Recharge 16.0k, Mystic Expansion 16.8k, Compress Cooldown 18.4k) starts after two gun T3 + Healing Booster. Healer scales with spirit; spirit 4.8k @18.4k. Move Heroic Aura after Compress Cooldown: spirit @15.2k, gun @18.4k (tested). |
| 12 | 16800 | Mystic Expansion | 800 | s1 | utility | 6400/4000/6400 | OK (info: bought 16800 vs median 8800 in 29 other builds, no action) |
| 13 | 18400 | Compress Cooldown | 1600 | s2 | utility | 6400/5600/6400 | OK |
| 14 | 20000 | Enchanter's Emblem | 1600 | v2 | SP 9.4 TR% 11.3 | 6400/5600/8000 | FLAG LOW: Fresh T2 at 20.0k (ratio 2.08, others median 9.6k), no upgrade, named sells exist (counter, Witchmail). Rule: late buys are T3/T4 or upgrades. TechPower 15, TechResist 18, 1600 = 9.4 SP/1k. [vs 17 other builds: median 9600, min 4800 seven_gun, max 20000 solomon_support] |
| 15 | 21600 | Duration Extender | 1600 | s2 | utility | 6400/7200/8000 | OK |
| 16 | 24800 | Warp Stone | 3200 | v3 | BR% 9.4 | 6400/7200/11200 | FLAG LOW: Counters Debuff Reducer sells this: health 16.0k>14.4k crosses 16k step. |
| 17 | 26400 | Superior Cooldown | 1600 | s3 | utility | 6400/8800/11200 | OK |
| 18 | 28800 | Greater Expansion | 2400 | s3 | TR% 3.1 | 6400/11200/11200 | OK |
| 19 | 30400 | Superior Duration | 1600 | s3 | BR% 2.5 | 6400/12800/11200 | OK |
| 20 | 35200 | Healing Tempo | 4800 | v4 | FR% 5.5 TR% 1.6 | 6400/12800/16000 | OK |
| 21 | 41600 | Boundless Spirit | 6400 | s4 | SP 4.7 HP 12 | 6400/19200/16000 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 6400/19200/16000 | gun@12800, spirit@18400, health@8800 | 12 | 41600 | - |
| Swap for Heroic Aura (Knockdown) | swap:Heroic Aura=Knockdown | 3200/22400/16000 | gun never, spirit@16000, health@8800 | 12 | 41600 | FLAG |
| Proposed: Spirit Rend instead of Heroic Aura | swap:Heroic Aura=Spirit Rend | 6400/19200/16000 | gun@12800, spirit@18400, health@8800 | 12 | 41600 | OK |
| Alternative: Knockdown + Opening Rounds instead of Enchanter's Emblem | swap:Heroic Aura=Knockdown ; swap:Enchanter's Emblem=Opening Rounds | 4800/22400/14400 | gun@20000, spirit@16000, health@8800 | 12 | 41600 | partial: gun 4.8k @20.0k, health 16.0k>14.4k |

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 6400/19200/16000 | gun@12800, spirit@18400, health@8800 | 12 | 41600 |
| Heroic Aura after Compress Cooldown | mv:Heroic Aura>after:Compress Cooldown | 6400/19200/16000 | gun@18400, spirit@15200, health@8800 | 12 | 41600 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 6400, spirit 19200, health 16000. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** Counters: Debuff Reducer (v2) sells Warp Stone (v3): health 16000>14400 (loses 16000)
- **FLAG** I'm rich as fuck: Lightning Scroll (s4) sells Trophy Collector (v2): health 16000>14400 (loses 16000)
- **FLAG** I'm rich as fuck: Refresher (s4) sells Headhunter (w3): gun 6400>3200 (loses 4800/6400)

## Other findings
- Gun / spirit / health 4.8k: gun @12800, spirit @18400, health @8800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

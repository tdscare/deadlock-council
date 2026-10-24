# Cost-efficiency audit: haze (Rizuhble's Victor Cosplay Haze)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@4800, spirit never, health@16000. End of core: 52800 souls, gun 27200 / spirit 3200 / health 22400, 12 slots.

Result: INFO spirit 3.2k never 4.8k; all four swaps pass (Surge of Power for Burst Fire moves spirit 4.8k to 36.8k, others unchanged); LOW Extra Charge @28.0k fresh T1 8.8k before Rapid Recharge
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Rapid Rounds | 800 | w1 | FR% 11.3 | 800/0/0 | OK (info: bought 800 vs median 2400 in 19 other builds, no action) |
| 2 | 2400 | Active Reload | 1600 | w2 | FR% 15.6 | 2400/0/0 | OK: 2.4k fresh T2 for lane, named sell for a counter; gun 4.8k @4.8k with 4 cheap gun items. [vs 3 other builds: median 7200, min 3200 haze_assassin, max 8000 ivy_carry] |
| 3 | 3200 | Swift Striker | 800 | w2 | FR% 12.5 | 3200/0/0 | OK |
| 4 | 4000 | Extended Magazine | 800 | w1 | WD% 10.0 | 4000/0/0 | OK |
| 5 | 4800 | Titanic Magazine | 800 | w2 | WD% 8.8 | 4800/0/0 | OK |
| 6 | 5600 | Extra Health | 800 | v1 | HP 263 | 4800/0/800 | OK |
| 7 | 8000 | Fortitude | 2400 | v3 | HP 117 | 4800/0/3200 | OK |
| 8 | 14400 | Ricochet | 6400 | w4 | FR% 2.8 | 11200/0/3200 | OK: 14.4k, 6400 (earliest T4 in my set). Kieran-agreed in-game base (farm until Siphon). Overrides the no-6400-before-20-min guideline. [vs 13 other builds: median 44800, min 16800 wraith, max 56000 nurse] |
| 9 | 16000 | Healing Booster | 1600 | v2 | utility | 11200/0/4800 | OK: 16.0k (4.8k health spike) 1600; healer base item. [vs 21 other builds: median 7200, min 2400 kelvin_support, max 24000 rem] |
| 10 | 22400 | Siphon Bullets | 6400 | v4 | WD% 2.3 BR% 1.6 | 11200/0/11200 | OK |
| 11 | 25600 | Burst Fire | 3200 | w3 | FR% 3.1 | 14400/0/11200 | OK (info: bought 25600 vs median 15200 in 9 other builds, no action) |
| 12 | 27200 | Bullet Lifesteal | 1600 | v2 | HP 56 WD% 3.8 | 14400/0/12800 | OK (info: bought 27200 vs median 9600 in 13 other builds, no action) |
| 13 | 28000 | Extra Charge | 800 | s1 | utility | 14400/800/12800 | FLAG LOW: 800 @28.0k (ratio 11.7), upgraded to Rapid Recharge @36.8k. Could be bought with it (same total 3200) or earlier for the charge; no spike effect (spirit 3.2k). [vs 31 other builds: median 2400, min 800 dynamo, max 24800 billy_damage] |
| 14 | 34400 | Lucky Shot | 6400 | w4 | utility | 20800/800/12800 | OK |
| 15 | 36800 | Rapid Recharge | 2400 | s3 | utility | 20800/3200/12800 | OK (info: bought 36800 vs median 18400 in 30 other builds, no action) |
| 16 | 41600 | Vampiric Burst | 4800 | v4 | HP 16 WD% 0.9 BR% 1.6 | 20800/3200/17600 | OK |
| 17 | 48000 | Silencer | 6400 | w4 | TR% 1.9 | 27200/3200/17600 | OK |
| 18 | 52800 | Healing Tempo | 4800 | v4 | FR% 5.5 TR% 1.6 | 27200/3200/22400 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 27200/3200/22400 | gun@4800, spirit never, health@16000 | 12 | 52800 | - |
| Surge of Power instead of Burst Fire | swap:Burst Fire=Surge of Power | 24000/6400/22400 | gun@4800, spirit@36800, health@16000 | 12 | 52800 | OK |
| Leech instead of Vampiric Burst | swap:Vampiric Burst=Leech | 27200/3200/22400 | gun@4800, spirit never, health@16000 | 12 | 52800 | OK |
| Blood Tribute instead of Burst Fire | swap:Burst Fire=Blood Tribute | 27200/3200/22400 | gun@4800, spirit never, health@16000 | 12 | 52800 | OK |
| Phantom Strike instead of Silencer | swap:Silencer=Phantom Strike | 20800/3200/28800 | gun@4800, spirit never, health@16000 | 12 | 52800 | OK (gun 27.2k>20.8k, still above 16k) |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 27200, spirit 3200, health 22400. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Lost-lane reorder (Ricochet before Fortitude) does not move any spike (tested).
- Gun / spirit / health 4.8k: gun @4800, spirit NEVER (end 3200), health @16000.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

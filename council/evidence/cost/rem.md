# Cost-efficiency audit: rem (Rizuhble's Backpack Medic Rem)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@8000, health@11200. End of core: 46400 souls, gun 3200 / spirit 28800 / health 12800, 12 slots.

Result: MED Heroic Aura note sells Opening Rounds so gun ends 3.2k, 4.8k never (swap Rescue Beam: 13 slots, gun 1.6k); MED Echo Shard 6.4k @17.6k earliest in data.js (median 36.8k); MED Trophy Collector fresh T2 @19.2k on a passive-souls item
Minimal fix: Keep Opening Rounds, drop Superior Duration (last core item, 46.4k): 12 slots, gun 4.8k @34.4k; Echo Shard after Healing Booster (24.0k); Trophy Collector after Compress Cooldown (9.6k); swap box Spirit Rend (gun T3) instead of Rescue Beam

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Charge | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 2400 in 31 other builds, no action) |
| 2 | 1600 | Grit | 800 | v1 | utility | 0/800/800 | OK (info: bought 1600 vs median 6400 in 26 other builds, no action) |
| 3 | 2400 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/800/800 | OK (info: bought 2400 vs median 800 in 24 other builds, no action) |
| 4 | 3200 | Opening Rounds | 800 | w2 | SP 4.4 WD% 5.0 | 1600/800/800 | OK |
| 5 | 4000 | Guardian Ward | 800 | v2 | utility | 1600/800/1600 | OK (info: bought 4000 vs median 12800 in 9 other builds, no action) |
| 6 | 4800 | Extra Spirit | 800 | s1 | SP 12.5 | 1600/1600/1600 | OK (info: bought 4800 vs median 1600 in 42 other builds, no action) |
| 7 | 5600 | Mystic Burst | 800 | s1 | utility | 1600/2400/1600 | OK: 5.6k: Pillow Toss 75+1.6x43 = 144 (>80). Tankbuster 31.2k: Pillow Toss 75+1.6x131 = 285 (>165). |
| 8 | 6400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 1600/3200/1600 | OK |
| 9 | 8000 | Compress Cooldown | 1600 | s2 | utility | 1600/4800/1600 | OK |
| 10 | 11200 | Healing Nova | 3200 | v3 | SP 2.5 | 1600/4800/4800 | OK |
| 11 | 17600 | Echo Shard | 6400 | s4 | BR% 0.8 TR% 0.8 | 1600/11200/4800 | FLAG MED: 17.6k, 6400, first T4. Other builds 24.8k to 56.0k (median 36.8k). Rule: no 6400s before ~20 min. Mystic Burst/Compress Cooldown spirit 4.8k @8.0k and Healing Nova health @11.2k already landed, so nothing waits on it. Move after Healing Booster = 24.0k. [vs 9 other builds: median 36800, min 24800 bebop_bomb, max 56000 geist_bomb] |
| 12 | 19200 | Trophy Collector | 1600 | v2 | utility | 1600/11200/6400 | FLAG MED: Fresh T2 at 19.2k (ratio 2.4; bebop builds 4.0k to 5.6k). Passive souls and ability range stack from kills/assists, so late buy loses most payoff. After Compress Cooldown (9.6k): spirit 4.8k stays @8.0k, health 4.8k 11.2k>12.8k. [vs 13 other builds: median 8000, min 4000 bebop_bomb, max 14400 solomon_support] |
| 13 | 21600 | Rapid Recharge | 2400 | s3 | utility | 1600/13600/6400 | OK |
| 14 | 22400 | Mystic Expansion | 800 | s1 | utility | 1600/14400/6400 | OK (info: bought 22400 vs median 8800 in 29 other builds, no action) |
| 15 | 24000 | Healing Booster | 1600 | v2 | utility | 1600/14400/8000 | FLAG LOW: 24.0k fresh T2 but slot-locked upgrade Healing Tempo named; Extra Regen not bought so full 1600. [vs 21 other builds: median 7200, min 2400 kelvin_support, max 16000 haze] |
| 16 | 28800 | Divine Barrier | 4800 | v4 | utility | 1600/14400/12800 | OK |
| 17 | 31200 | Tankbuster | 2400 | s3 | HP 16 | 1600/16800/12800 | OK (info: bought 31200 vs median 17600 in 24 other builds, no action) |
| 18 | 34400 | Heroic Aura | 3200 | w3 | FR% 8.1 BR% 5.3 | 3200/16800/12800 | FLAG MED: Note sells Opening Rounds for it: gun 1.6k+3.2k-1.6k = 3.2k. Keep Opening Rounds and cut Superior Duration instead: gun 4.8k @34.4k, still 12 slots (tested). Swap Rescue Beam is Armor (v3): gun 1.6k, and 13 slots because the sell note is not on the swap. [vs 6 other builds: median 13600, min 12000 ivy, max 18400 solomon_support] |
| 19 | 36000 | Superior Cooldown | 1600 | s3 | utility | 3200/18400/12800 | OK |
| 20 | 38400 | Greater Expansion | 2400 | s3 | TR% 3.1 | 3200/20800/12800 | OK |
| 21 | 43200 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 3200/25600/12800 | OK |
| 22 | 46400 | Superior Duration | 3200 | s3 | BR% 2.5 | 3200/28800/12800 | FLAG LOW: 46.4k last core item, 3200 fresh (8 bullet resist). Candidate to cut for the Opening Rounds fix. [vs 22 other builds: median 26400, min 14400 sinclair_bolt, max 64000 nurse] |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 3200/28800/12800 | gun never, spirit@8000, health@11200 | 12 | 46400 | - |
| Swap for Heroic Aura (Rescue Beam) | swap:Heroic Aura=Rescue Beam | 1600/28800/16000 | gun never, spirit@8000, health@11200 | 13 | 46400 | FLAG |
| Proposed: keep Opening Rounds, cut Superior Duration | nonote:Heroic Aura ; del:Superior Duration | 4800/25600/12800 | gun@34400, spirit@8000, health@11200 | 12 | 43200 | OK |
| Proposed swap box: Spirit Rend instead of Heroic Aura (with the fix above) | nonote:Heroic Aura ; del:Superior Duration ; swap:Heroic Aura=Spirit Rend | 4800/25600/12800 | gun@34400, spirit@8000, health@11200 | 12 | 43200 | OK |

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 3200/28800/12800 | gun never, spirit@8000, health@11200 | 12 | 46400 |
| All Rem fixes | nonote:Heroic Aura ; del:Superior Duration ; mv:Trophy Collector>after:Compress Cooldown ; mv:Echo Shard>after:Healing Booster | 4800/25600/12800 | gun@34400, spirit@8000, health@12800 | 12 | 43200 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 3200, spirit 28800, health 12800. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- "3+ gun heroes?" reorder (Heroic Aura right after Healing Nova) tested: gun 3.2k, same missing 4.8k as the base; with the Opening Rounds fix it gives gun 4.8k @14.4k.
- Gun / spirit / health 4.8k: gun NEVER (end 3200), spirit @8000, health @11200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

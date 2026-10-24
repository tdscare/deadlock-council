# Cost-efficiency audit: infernus (Rizuhble's Arsonist Infernus)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@15200, spirit@5600, health@11200. End of core: 44800 souls, gun 25600 / spirit 11200 / health 8000, 12 slots.

Result: MED Gun Infernus gets gun 4.8k only third (15.2k) behind spirit @5.6k and health @11.2k; LOW rich Spirit Burn sells Healbane: health 8.0k>6.4k
Minimal fix: Toxic Bullets right after Extended Magazine: gun 4.8k @9.6k (was 15.2k), health 4.8k 11.2k>14.4k. Armor Piercer swap is fine (tested, same colour and price)

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Spirit | 800 | s1 | SP 12.5 | 0/800/0 | OK (info: bought 800 vs median 1600 in 42 other builds, no action) |
| 2 | 1600 | Rapid Rounds | 800 | w1 | FR% 11.3 | 800/800/0 | OK |
| 3 | 3200 | Duration Extender | 1600 | s2 | utility | 800/2400/0 | OK (info: bought 3200 vs median 16000 in 22 other builds, no action) |
| 4 | 4000 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 800/3200/0 | OK |
| 5 | 5600 | Mystic Vulnerability | 1600 | s2 | TR% 5.0 | 800/4800/0 | OK (info: bought 5600 vs median 14400 in 27 other builds, no action) |
| 6 | 6400 | Extended Magazine | 800 | w1 | WD% 10.0 | 1600/4800/0 | OK (info: bought 6400 vs median 3200 in 10 other builds, no action) |
| 7 | 8000 | Bullet Lifesteal | 1600 | v2 | HP 56 WD% 3.8 | 1600/4800/1600 | OK |
| 8 | 9600 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 1600/4800/3200 | OK |
| 9 | 11200 | Healbane | 1600 | v2 | SP 4.4 | 1600/4800/4800 | FLAG LOW: Rich Spirit Burn sells this: health 8.0k>6.4k crosses the 8k step. |
| 10 | 12000 | Swift Striker | 800 | w2 | FR% 12.5 | 2400/4800/4800 | OK: 12.0k fresh T2 (800 paid, Rapid Rounds consumed), named sell for a counter. [vs 15 other builds: median 4800, min 3200 greytalon_gun, max 16800 vindicta] |
| 11 | 15200 | Toxic Bullets | 3200 | w3 | utility | 5600/4800/4800 | FLAG MED: 15.2k, 3200 (w3), the item that lands gun 4.8k. Build is named gun, yet first 5.6k souls are spirit (Extra Spirit, Duration Extender, Improved Spirit, Mystic Vulnerability). Move after Extended Magazine: gun @9.6k (tested). |
| 12 | 16000 | Titanic Magazine | 800 | w2 | WD% 8.8 | 6400/4800/4800 | OK (info: bought 16000 vs median 4800 in 10 other builds, no action) |
| 13 | 17600 | Superior Duration | 1600 | s3 | BR% 2.5 | 6400/6400/4800 | OK |
| 14 | 20800 | Burst Fire | 3200 | w3 | FR% 3.1 | 9600/6400/4800 | OK |
| 15 | 24000 | Spirit Rend | 3200 | w3 | HP 23 | 12800/6400/4800 | OK |
| 16 | 28800 | Escalating Exposure | 4800 | s4 | TR% 2.7 | 12800/11200/4800 | OK |
| 17 | 32000 | Leech | 3200 | v4 | SP 1.9 HP 28 WD% 1.9 | 12800/11200/8000 | OK |
| 18 | 38400 | Spiritual Overflow | 6400 | w4 | SP 5.6 HP 14 FR% 3.9 | 19200/11200/8000 | OK |
| 19 | 44800 | Ricochet | 6400 | w4 | FR% 2.8 | 25600/11200/8000 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 25600/11200/8000 | gun@15200, spirit@5600, health@11200 | 12 | 44800 | - |
| Swap for Ricochet (Armor Piercer) | swap:Ricochet=Armor Piercer | 25600/11200/8000 | gun@15200, spirit@5600, health@11200 | 12 | 44800 | OK |

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 25600/11200/8000 | gun@15200, spirit@5600, health@11200 | 12 | 44800 |
| Toxic Bullets after Extended Magazine | mv:Toxic Bullets>after:Extended Magazine | 25600/11200/8000 | gun@9600, spirit@5600, health@14400 | 12 | 44800 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 25600, spirit 11200, health 8000. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** I'm rich as fuck: Spirit Burn (s4) sells Healbane (v2): health 8000>6400 (loses 8000)

## Other findings
- End health only 8.0k (Bullet Lifesteal, Spirit Lifesteal, Healbane + Leech): lifesteal heavy by design.
- Gun / spirit / health 4.8k: gun @15200, spirit @5600, health @11200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

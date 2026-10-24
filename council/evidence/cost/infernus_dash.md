# Cost-efficiency audit: infernus_dash (Rizuhble's Hot Lap Infernus)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@51200, spirit@8800, health@11200. End of core: 57600 souls, gun 8000 / spirit 25600 / health 24000, 12 slots.

Result: MED gun 4.8k only @51.2k (Spiritual Overflow, second to last) with gun 1.6k for 50k souls; LOW every counter + Lightning Scroll sell Swift Striker: gun 8.0k>6.4k
Minimal fix: Spiritual Overflow before Escalating Exposure: gun 4.8k @24.0k (tested, spirit @8.8k and health @11.2k unchanged)

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Sprint Boots | 800 | v1 | utility | 0/0/800 | OK: First item (lane speed for a dash hero), 800, Enduring Speed @11.2k. [vs 39 other builds: median 8800, min 2400 bebop_bomb, max 20800 wraith] |
| 2 | 1600 | Rapid Rounds | 800 | w1 | FR% 11.3 | 800/0/800 | OK |
| 3 | 3200 | Mystic Vulnerability | 1600 | s2 | TR% 5.0 | 800/1600/800 | OK (info: bought 3200 vs median 14400 in 27 other builds, no action) |
| 4 | 4000 | Extra Charge | 800 | s1 | utility | 800/2400/800 | OK (info: bought 4000 vs median 2400 in 31 other builds, no action) |
| 5 | 4800 | Swift Striker | 800 | w2 | FR% 12.5 | 1600/2400/800 | FLAG LOW: Counters (all) and Lightning Scroll sell this: gun 8.0k>6.4k. |
| 6 | 6400 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 1600/2400/2400 | OK (info: bought 6400 vs median 14400 in 31 other builds, no action) |
| 7 | 8800 | Rapid Recharge | 2400 | s3 | utility | 1600/4800/2400 | OK: 8.8k (Extra Charge consumed), spirit 4.8k lands here. [vs 30 other builds: median 18400, min 5600 vindicta_sniper, max 49600 shiv] |
| 8 | 10400 | Reactive Barrier | 1600 | v2 | utility | 1600/4800/4000 | OK |
| 9 | 11200 | Enduring Speed | 800 | v2 | utility | 1600/4800/4800 | OK |
| 10 | 12800 | Duration Extender | 1600 | s2 | utility | 1600/6400/4800 | OK |
| 11 | 16000 | Dispel Magic | 3200 | v3 | TR% 3.1 | 1600/6400/8000 | OK |
| 12 | 17600 | Debuff Reducer | 1600 | v2 | HP 56 | 1600/6400/9600 | OK |
| 13 | 19200 | Superior Duration | 1600 | s3 | BR% 2.5 | 1600/8000/9600 | OK |
| 14 | 24000 | Escalating Exposure | 4800 | s4 | TR% 2.7 | 1600/12800/9600 | OK |
| 15 | 28800 | Unstoppable | 4800 | v4 | HP 20 | 1600/12800/14400 | OK |
| 16 | 35200 | Echo Shard | 6400 | s4 | BR% 0.8 TR% 0.8 | 1600/19200/14400 | OK |
| 17 | 41600 | Spirit Burn | 6400 | s4 | utility | 1600/25600/14400 | OK |
| 18 | 46400 | Indomitable | 4800 | v4 | BR% 1.6 TR% 1.6 | 1600/25600/19200 | OK |
| 19 | 51200 | Spiritual Overflow | 4800 | w4 | SP 5.6 HP 14 FR% 3.9 | 8000/25600/17600 | FLAG MED: Gun 4.8k lands here at 51.2k. Moved ahead of Escalating Exposure it lands at 24.0k (tested): gun 4.8k @24.0k, total cost unchanged (Spirit Lifesteal consumed, 4800 paid), spirit @8.8k and health @11.2k unchanged. T4 buys stay below 3 back to back. |
| 20 | 57600 | Cheat Death | 6400 | v4 | HP 31 BR% 2.3 | 8000/25600/24000 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 8000/25600/24000 | gun@51200, spirit@8800, health@11200 | 12 | 57600 |
| Spiritual Overflow before Escalating Exposure | mv:Spiritual Overflow>before:Escalating Exposure | 8000/25600/24000 | gun@24000, spirit@8800, health@11200 | 12 | 57600 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 8000, spirit 25600, health 24000. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** Counters: Metal Skin (v3) sells Swift Striker (w2): gun 8000>6400 (loses 8000)
- **FLAG** Counters: Plated Armor (v4) sells Swift Striker (w2): gun 8000>6400 (loses 8000)
- **FLAG** Counters: Counterspell (v3) sells Swift Striker (w2): gun 8000>6400 (loses 8000)
- **FLAG** Counters: Spirit Resilience (v3) sells Swift Striker (w2): gun 8000>6400 (loses 8000)
- **FLAG** Counters: Healbane (v2) sells Swift Striker (w2): gun 8000>6400 (loses 8000)
- **FLAG** I'm rich as fuck: Lightning Scroll (s4) sells Swift Striker (w2): gun 8000>6400 (loses 8000)

## Other findings
- Gun / spirit / health 4.8k: gun @51200, spirit @8800, health @11200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

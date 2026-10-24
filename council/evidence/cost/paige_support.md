# Cost-efficiency audit: paige_support (Rizuhble's Bedtime Story Paige)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@10400, health@12800. End of core: 48000 souls, gun 1600 / spirit 35200 / health 11200, 12 slots.

Result: INFO gun 1.6k (HV + Opening Rounds), 4.8k never; otherwise OK (spirit @10.4k, health @12.8k)
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Healing Rite | 800 | v1 | utility | 800/0/800 | OK (info: bought 1600 vs median 3200 in 4 other builds, no action) |
| 3 | 2400 | Grit | 800 | v1 | utility | 800/0/1600 | OK (info: bought 2400 vs median 6400 in 26 other builds, no action) |
| 4 | 3200 | Extra Charge | 800 | s1 | utility | 800/800/1600 | OK |
| 5 | 4000 | Guardian Ward | 800 | v2 | utility | 800/800/2400 | OK (info: bought 4000 vs median 12800 in 9 other builds, no action) |
| 6 | 4800 | Sprint Boots | 800 | v1 | utility | 800/800/3200 | OK (info: bought 4800 vs median 8800 in 39 other builds, no action) |
| 7 | 5600 | Extra Spirit | 800 | s1 | SP 12.5 | 800/1600/3200 | OK (info: bought 5600 vs median 1600 in 42 other builds, no action) |
| 8 | 6400 | Trophy Collector | 800 | v2 | utility | 800/1600/4000 | OK |
| 9 | 7200 | Mystic Expansion | 800 | s1 | utility | 800/2400/4000 | OK |
| 10 | 8000 | Opening Rounds | 800 | w2 | SP 4.4 WD% 5.0 | 1600/2400/4000 | FLAG LOW: 8.0k fresh T2 (800 paid, HV consumed), dead-end with named sells (Echo Shard, counters); gun stays 1.6k. [vs 15 other builds: median 2400, min 1600 danny, max 6400 vyper] |
| 11 | 8800 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 1600/3200/4000 | OK |
| 12 | 10400 | Compress Cooldown | 1600 | s2 | utility | 1600/4800/4000 | OK |
| 13 | 12800 | Rescue Beam | 2400 | v3 | utility | 1600/4800/6400 | OK: 12.8k, 2400 paid (Healing Rite consumed), 20% heal + pull; health 4.8k lands here. |
| 14 | 16000 | Knockdown | 3200 | s3 | HP 23 | 1600/8000/6400 | OK: 16.0k, 3200; named in notes; sold for Vortex Web. |
| 15 | 17600 | Duration Extender | 1600 | s2 | utility | 1600/9600/6400 | OK |
| 16 | 20000 | Rapid Recharge | 2400 | s3 | utility | 1600/12000/6400 | OK |
| 17 | 21600 | Superior Cooldown | 1600 | s3 | utility | 1600/13600/6400 | OK |
| 18 | 26400 | Divine Barrier | 4800 | v4 | utility | 1600/13600/11200 | OK |
| 19 | 28800 | Greater Expansion | 2400 | s3 | TR% 3.1 | 1600/16000/11200 | OK |
| 20 | 30400 | Superior Duration | 1600 | s3 | BR% 2.5 | 1600/17600/11200 | OK |
| 21 | 35200 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 1600/22400/11200 | OK |
| 22 | 41600 | Cursed Relic | 6400 | s4 | utility | 1600/28800/11200 | OK |
| 23 | 48000 | Lightning Scroll | 6400 | s4 | HP 8 | 1600/35200/11200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 1600, spirit 35200, health 11200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Gun invest only 1.6k: no gun T3 in the build.
- Gun / spirit / health 4.8k: gun NEVER (end 1600), spirit @10400, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

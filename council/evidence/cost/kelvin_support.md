# Cost-efficiency audit: kelvin_support (Rizuhble's Frozone Kelvin)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@6400, health@9600. End of core: 46400 souls, gun 0 / spirit 32000 / health 14400, 12 slots.

Result: INFO gun 0; none else
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Charge | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 2400 in 31 other builds, no action) |
| 2 | 1600 | Extra Regen | 800 | v1 | utility | 0/800/800 | OK |
| 3 | 2400 | Healing Booster | 800 | v2 | utility | 0/800/1600 | OK: 2.4k (Extra Regen consumed), healer: payoff immediate. [vs 21 other builds: median 8000, min 4000 apollo_melee, max 24000 rem] |
| 4 | 3200 | Extra Spirit | 800 | s1 | SP 12.5 | 0/1600/1600 | OK (info: bought 3200 vs median 1600 in 42 other builds, no action) |
| 5 | 4000 | Mystic Expansion | 800 | s1 | utility | 0/2400/1600 | OK (info: bought 4000 vs median 10400 in 29 other builds, no action) |
| 6 | 5600 | Compress Cooldown | 1600 | s2 | utility | 0/4000/1600 | OK (info: bought 5600 vs median 14400 in 43 other builds, no action) |
| 7 | 6400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 0/4800/1600 | OK |
| 8 | 7200 | Sprint Boots | 800 | v1 | utility | 0/4800/2400 | OK |
| 9 | 8000 | Trophy Collector | 800 | v2 | utility | 0/4800/3200 | OK |
| 10 | 9600 | Enchanter's Emblem | 1600 | v2 | SP 9.4 TR% 11.3 | 0/4800/4800 | OK: 9.6k fresh T2 with named sell for a counter; health 4.8k lands here. |
| 11 | 11200 | Healbane | 1600 | v2 | SP 4.4 | 0/4800/6400 | OK: 11.2k named sell for third counter. |
| 12 | 13600 | Rapid Recharge | 2400 | s3 | utility | 0/7200/6400 | OK |
| 13 | 15200 | Superior Cooldown | 1600 | s3 | utility | 0/8800/6400 | OK |
| 14 | 16800 | Duration Extender | 1600 | s2 | utility | 0/10400/6400 | OK |
| 15 | 20000 | Warp Stone | 3200 | v3 | BR% 9.4 | 0/10400/9600 | OK: 20.0k, 3200; roamer. |
| 16 | 24800 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 0/15200/9600 | OK |
| 17 | 29600 | Healing Tempo | 4800 | v4 | FR% 5.5 TR% 1.6 | 0/15200/14400 | OK |
| 18 | 36000 | Cursed Relic | 6400 | s4 | utility | 0/21600/14400 | OK |
| 19 | 42400 | Refresher | 6400 | s4 | BR% 2.3 TR% 2.2 | 0/28000/14400 | OK |
| 20 | 44800 | Greater Expansion | 2400 | s3 | TR% 3.1 | 0/30400/14400 | OK |
| 21 | 46400 | Superior Duration | 1600 | s3 | BR% 2.5 | 0/32000/14400 | OK (info: bought 46400 vs median 26400 in 22 other builds, no action) |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 0, spirit 32000, health 14400. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Spikes: spirit @6.4k, health @9.6k. Gun invest 0.
- Gun / spirit / health 4.8k: gun NEVER (end 0), spirit @6400, health @9600.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

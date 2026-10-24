# Cost-efficiency audit: danny_gun (Rizuhble's Jet Fuel Gunner Danny)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@4800, spirit@17600, health@10400. End of core: 48000 souls, gun 20800 / spirit 12800 / health 14400, 12 slots.

Result: LOW Spirit Shielding = T2 with no further upgrade and no named sell; otherwise OK (gun 4.8k @4.8k, health 10.4k, spirit 17.6k)
Minimal fix: Name a sell for Spirit Shielding (e.g. Counters desc sells it) or swap for a pure upgrade of Grit that is in the build; no timing change needed

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Rapid Rounds | 800 | w1 | FR% 11.3 | 1600/0/0 | OK |
| 3 | 4000 | Express Shot | 2400 | w3 | WD% 2.5 | 4000/0/0 | OK: 4.0k, 2400 paid (HV consumed). Gun 4.8k lands at 4.8k with Swift Striker: fastest in my set. Earlier than other builds (median 15.2k) but it is the 4.8k race. [vs 5 other builds: median 15200, min 5600 paige, max 20000 yamato_brawler] |
| 4 | 4800 | Swift Striker | 800 | w2 | FR% 12.5 | 4800/0/0 | OK |
| 5 | 5600 | Grit | 800 | v1 | utility | 4800/0/800 | OK |
| 6 | 6400 | Extra Spirit | 800 | s1 | SP 12.5 | 4800/800/800 | FLAG LOW: Stepping stone: 800 at 6.4k, only consumed by Surge of Power at 17.6k (11k souls later). 10 SP for 800 = 12.5 SP/1k meanwhile; acceptable. [vs 42 other builds: median 1600, min 800 infernus, max 19200 baba_tank] |
| 7 | 7200 | Extra Health | 800 | v1 | HP 263 | 4800/800/1600 | OK |
| 8 | 9600 | Fortitude | 2400 | v3 | HP 117 | 4800/800/4000 | OK |
| 9 | 10400 | Spirit Shielding | 800 | v2 | TR% 11.3 | 4800/800/4800 | FLAG LOW: T2 upgrade of Grit (800 paid). Nothing upgrades it (no components use it) and no box says to sell it. Rule: every T1/T2 needs an upgrade later or a named replacement. |
| 10 | 12000 | Duration Extender | 1600 | s2 | utility | 4800/2400/4800 | OK |
| 11 | 15200 | Toxic Bullets | 3200 | w3 | utility | 8000/2400/4800 | OK |
| 12 | 17600 | Surge of Power | 2400 | s3 | SP 8.8 | 8000/4800/4800 | OK |
| 13 | 19200 | Superior Duration | 1600 | s3 | BR% 2.5 | 8000/6400/4800 | OK |
| 14 | 20800 | Mystic Vulnerability | 1600 | s2 | TR% 5.0 | 8000/8000/4800 | OK |
| 15 | 22400 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 8000/8000/6400 | OK (info: bought 22400 vs median 12800 in 31 other builds, no action) |
| 16 | 25600 | Warp Stone | 3200 | v3 | BR% 9.4 | 8000/8000/9600 | OK |
| 17 | 30400 | Spiritual Overflow | 4800 | w4 | SP 5.6 HP 14 FR% 3.9 | 14400/8000/8000 | OK |
| 18 | 35200 | Escalating Exposure | 4800 | s4 | TR% 2.7 | 14400/12800/8000 | OK |
| 19 | 41600 | Lucky Shot | 6400 | w4 | utility | 20800/12800/8000 | OK |
| 20 | 48000 | Siphon Bullets | 6400 | v4 | WD% 2.3 BR% 1.6 | 20800/12800/14400 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 20800, spirit 12800, health 14400. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Counters sell Warp Stone: no spike crossed (all colours stay above their thresholds).
- Gun 8.0k reached via Toxic Bullets @15.2k before spirit 4.8k (17.6k): intended (8k is a spike step), not an overshoot.
- Gun / spirit / health 4.8k: gun @4800, spirit @17600, health @10400.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

# Cost-efficiency audit: haze_assassin (Rizuhble's Sleepy Stabby Haze)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@5600, spirit@14400, health@10400. End of core: 44800 souls, gun 27200 / spirit 4800 / health 11200, 12 slots.

Result: LOW rich Crippling Headshot sells Bullet Resist Shredder: spirit 4.8k>3.2k; 5 T2 dead-ends (7.2k souls) all with named sells
Minimal fix: Crippling Headshot sells Swift Striker/Active Reload line instead

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Spirit | 800 | s1 | SP 12.5 | 0/800/0 | OK (info: bought 800 vs median 1600 in 42 other builds, no action) |
| 2 | 1600 | Rapid Rounds | 800 | w1 | FR% 11.3 | 800/800/0 | OK |
| 3 | 3200 | Active Reload | 1600 | w2 | FR% 15.6 | 2400/800/0 | OK (info: bought 3200 vs median 7200 in 3 other builds, no action) |
| 4 | 4000 | Swift Striker | 800 | w2 | FR% 12.5 | 3200/800/0 | OK |
| 5 | 5600 | Fleetfoot | 1600 | w2 | WD% 3.8 BR% 3.8 | 4800/800/0 | OK: 5.6k, gun 4.8k lands; named sell for Unstoppable. [vs 4 other builds: median 15200, min 12800 ratking, max 19200 shiv_gun] |
| 6 | 6400 | Sprint Boots | 800 | v1 | utility | 4800/800/800 | OK |
| 7 | 7200 | Enduring Speed | 800 | v2 | utility | 4800/800/1600 | OK |
| 8 | 10400 | Veil Walker | 3200 | v3 | SP 1.9 HP 39 | 4800/800/4800 | OK |
| 9 | 12800 | Surge of Power | 2400 | s3 | SP 8.8 | 4800/3200/4800 | OK |
| 10 | 14400 | Bullet Resist Shredder | 1600 | s2 | WD% 5.6 BR% 5.6 | 4800/4800/4800 | FLAG LOW: 14.4k lands spirit 4.8k; rich Crippling Headshot sells it: spirit 3.2k. |
| 11 | 16000 | Recharging Rush | 1600 | w2 | WD% 6.3 | 6400/4800/4800 | OK: 16.0k, fast-firing hero easily >200 in 3.5s; named sell for a counter. |
| 12 | 19200 | Tesla Bullets | 3200 | w3 | utility | 9600/4800/4800 | OK: 19.2k (ratio 3.0), consumed by Capacitor @25.6k (paid 3200). [vs 4 other builds: median 6400, min 5600 graves, max 17600 seven_gun] |
| 13 | 22400 | Burst Fire | 3200 | w3 | FR% 3.1 | 12800/4800/4800 | OK |
| 14 | 25600 | Capacitor | 3200 | w4 | FR% 0.8 | 16000/4800/4800 | OK |
| 15 | 32000 | Lucky Shot | 6400 | w4 | utility | 22400/4800/4800 | OK |
| 16 | 38400 | Unstoppable | 6400 | v4 | HP 20 | 20800/4800/11200 | OK |
| 17 | 44800 | Ricochet | 6400 | w4 | FR% 2.8 | 27200/4800/11200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 27200, spirit 4800, health 11200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** I'm rich as fuck: Crippling Headshot (w4) sells Bullet Resist Shredder (s2): spirit 4800>3200 (loses 4800)

## Other findings
- Spikes: gun @5.6k, health @10.4k, spirit @14.4k.
- Gun / spirit / health 4.8k: gun @5600, spirit @14400, health @10400.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

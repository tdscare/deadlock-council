# Cost-efficiency audit: bebop_support (Rizuhble's Wingman Bebop)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@19200, spirit@8000, health@10400. End of core: 48000 souls, gun 6400 / spirit 20800 / health 20800, 12 slots.

Result: HIGH swap 'Knockdown instead of Heroic Aura': gun invest 3.2k, 4.8k never lands (base: gun 4.8k @19.2k with Heroic Aura + Hunter's Aura); LOW Veil Walker @24.0k
Minimal fix: Swap box gets a gun item with the same job: Spirit Rend (gun T3, team spirit shred; spikes unchanged, gun @19.2k tested). Keep Knockdown only with a 1.6k gun top-up (Opening Rounds) replacing another slot

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Spirit Strike | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 3200 in 12 other builds, no action) |
| 2 | 1600 | Extra Spirit | 800 | s1 | SP 12.5 | 0/1600/0 | OK |
| 3 | 3200 | Bullet Resist Shredder | 1600 | s2 | WD% 5.6 BR% 5.6 | 0/3200/0 | OK: 3.2k, spirit 3.2k step; BulletArmorReduction -10 and +9% weapon damage for the team at 1600 = 5.6 WD%/1k. [vs 10 other builds: median 14400, min 4800 bebop, max 19200 ivy_carry] |
| 4 | 4000 | Extra Health | 800 | v1 | HP 263 | 0/3200/800 | OK (info: bought 4000 vs median 8800 in 20 other builds, no action) |
| 5 | 4800 | Sprint Boots | 800 | v1 | utility | 0/3200/1600 | OK (info: bought 4800 vs median 8800 in 39 other builds, no action) |
| 6 | 5600 | Trophy Collector | 800 | v2 | utility | 0/3200/2400 | OK |
| 7 | 6400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 0/4000/2400 | OK |
| 8 | 8000 | Compress Cooldown | 1600 | s2 | utility | 0/5600/2400 | OK |
| 9 | 10400 | Fortitude | 2400 | v3 | HP 117 | 0/5600/4800 | OK: 10.4k, 2400 for 375 hp; health 4.8k lands here. |
| 10 | 13600 | Heroic Aura | 3200 | w3 | FR% 8.1 BR% 5.3 | 3200/5600/4800 | FLAG HIGH: Only gun T3 besides Hunter's Aura. Swap Knockdown (Tech, 3200, Health 75) takes gun from 6.4k to 3.2k: 4.8k never. Same walk for the base: gun 4.8k @19.2k, spirit @8.0k, health @10.4k. |
| 11 | 16000 | Spirit Snatch | 2400 | s3 | HP 23 | 3200/8000/4800 | OK |
| 12 | 19200 | Hunter's Aura | 3200 | w3 | HP 31 | 6400/8000/4800 | OK |
| 13 | 20800 | Slowing Hex | 1600 | s2 | utility | 6400/9600/4800 | OK |
| 14 | 24000 | Veil Walker | 3200 | v3 | SP 1.9 HP 39 | 6400/9600/8000 | FLAG LOW: 24.0k, 3200 (v3, 125 hp, 6 SP) after Hunter's Aura and Slowing Hex. Other Bebop builds buy it 12.8k to 13.6k. It is the item that lets Bebop sneak up for the hook; at 24k that is mid-late. [vs 7 other builds: median 12000, min 9600 paradox_bomb, max 21600 drifter_spirit] |
| 15 | 25600 | Superior Cooldown | 1600 | s3 | utility | 6400/11200/8000 | OK |
| 16 | 30400 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 6400/16000/8000 | OK |
| 17 | 36800 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 6400/16000/14400 | OK |
| 18 | 41600 | Vortex Web | 4800 | s4 | utility | 6400/20800/14400 | OK |
| 19 | 48000 | Unstoppable | 6400 | v4 | HP 20 | 6400/20800/20800 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 6400/20800/20800 | gun@19200, spirit@8000, health@10400 | 12 | 48000 | - |
| Swap for Heroic Aura (Knockdown) | swap:Heroic Aura=Knockdown | 3200/24000/20800 | gun never, spirit@8000, health@10400 | 12 | 48000 | FLAG |
| Proposed: Spirit Rend instead of Heroic Aura | swap:Heroic Aura=Spirit Rend | 6400/20800/20800 | gun@19200, spirit@8000, health@10400 | 12 | 48000 | OK |
| Alternative: Knockdown + Opening Rounds (instead of Slowing Hex and Vortex Web) | swap:Heroic Aura=Knockdown ; swap:Slowing Hex=Opening Rounds ; swap:Vortex Web=Echo Shard | 4800/24000/20800 | gun@20800, spirit@8000, health@10400 | 13 | 49600 | FLAG (13 slots, rejected) |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 6400, spirit 20800, health 20800. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Heroic Aura is a core item conditional on gun heroes; when the condition fails the box is the swap, so the swap must keep colour totals.
- Gun / spirit / health 4.8k: gun @19200, spirit @8000, health @10400.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

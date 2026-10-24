# Cost-efficiency audit: ratking_grenade (Rizuhble's Trash Lobber Rat King)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@5600, spirit@22400, health@12800. End of core: 44800 souls, gun 12800 / spirit 12800 / health 19200, 12 slots.

Result: OK; swap 'Bullet Resist Shredder instead of Battle Vest' passes (health 4.8k stays @12.8k)
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Monster Rounds | 800 | w1 | utility | 1600/0/0 | OK |
| 3 | 4000 | Cultist Sacrifice | 2400 | w3 | HP 16 WD% 3.1 | 4000/0/0 | OK: 4.0k (2400 paid). |
| 4 | 5600 | Long Range | 1600 | w2 | utility | 5600/0/0 | OK: 5.6k, 1600; consumed by Sharpshooter @6.4k (800 paid); gun 6.4k early is the point (grenade scales with weapon damage). [vs 5 other builds: median 14400, min 2400 vindicta, max 15200 holliday] |
| 5 | 6400 | Sharpshooter | 800 | w3 | WD% 3.1 | 6400/0/0 | OK (info: bought 6400 vs median 15200 in 6 other builds, no action) |
| 6 | 8000 | Battle Vest | 1600 | v2 | WD% 11.3 FR% 4.4 BR% 11.3 | 6400/0/1600 | OK: 8.0k, v2 1600; 18% bullet resist + 18% weapon damage above 65% hp. Swap box replaces it with Bullet Resist Shredder (s2, same price): tested, gun @5.6k, health @12.8k unchanged, spirit 22.4k>19.2k. |
| 7 | 8800 | Sprint Boots | 800 | v1 | utility | 6400/0/2400 | OK |
| 8 | 9600 | Enduring Speed | 800 | v2 | utility | 6400/0/3200 | OK |
| 9 | 10400 | Extra Health | 800 | v1 | HP 263 | 6400/0/4000 | OK |
| 10 | 12800 | Fortitude | 2400 | v3 | HP 117 | 6400/0/6400 | OK |
| 11 | 13600 | Mystic Expansion | 800 | s1 | utility | 6400/800/6400 | OK |
| 12 | 15200 | Compress Cooldown | 1600 | s2 | utility | 6400/2400/6400 | OK |
| 13 | 17600 | Ballistic Enchantment | 2400 | w3 | utility | 9600/1600/6400 | OK |
| 14 | 19200 | Superior Cooldown | 1600 | s3 | utility | 9600/3200/6400 | OK |
| 15 | 22400 | Greater Expansion | 3200 | s3 | TR% 3.1 | 9600/6400/6400 | OK |
| 16 | 25600 | Hollow Point | 3200 | w3 | HP 39 WD% 10.9 | 12800/6400/6400 | OK |
| 17 | 32000 | Echo Shard | 6400 | s4 | BR% 0.8 TR% 0.8 | 12800/12800/6400 | OK |
| 18 | 38400 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 12800/12800/12800 | OK |
| 19 | 44800 | Colossus | 6400 | v4 | WD% 2.3 | 12800/12800/19200 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 12800/12800/19200 | gun@5600, spirit@22400, health@12800 | 12 | 44800 | - |
| Swap for Battle Vest (Bullet Resist Shredder) | swap:Battle Vest=Bullet Resist Shredder | 12800/14400/17600 | gun@5600, spirit@19200, health@12800 | 12 | 44800 | OK |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 12800, spirit 12800, health 19200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Spirit 4.8k only @22.4k, ends 12.8k: secondary colour, acceptable for a grenade-weapon build.
- Gun / spirit / health 4.8k: gun @5600, spirit @22400, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

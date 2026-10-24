# Cost-efficiency audit: paige (Rizuhble's Book Bomber Paige)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@5600, spirit@12000, health@15200. End of core: 40000 souls, gun 4800 / spirit 28800 / health 6400, 12 slots.

Result: MED swap 'Slowing Hex instead of Mystic Burst' alone = 13 slots and +1600 souls (Tankbuster loses its Mystic Burst component); MED every counter sells Express Shot: gun 4.8k>1.6k; LOW health only 6.4k at end of core; LOW Surge of Power @24.8k
Minimal fix: Merge the Slowing Hex and Vortex Web swaps into one (instead of Mystic Burst and Escalating Exposure: 12 slots, same total 40.0k, tested); counters sell Greater Expansion instead of Express Shot; Surge of Power before Guardian Ward

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Opening Rounds | 800 | w2 | SP 4.4 WD% 5.0 | 1600/0/0 | OK |
| 3 | 2400 | Grit | 800 | v1 | utility | 1600/0/800 | OK (info: bought 2400 vs median 6400 in 26 other builds, no action) |
| 4 | 5600 | Express Shot | 3200 | w3 | WD% 2.5 | 4800/0/800 | FLAG MED: Counters desc and Mystic Reverb note sell this: gun 4.8k>1.6k. Spirit Burn note sells Opening Rounds: 4.8k>3.2k. Sell Greater Expansion (spirit 28.8k>26.4k, nothing crossed). [vs 5 other builds: median 15200, min 4000 danny_gun, max 20000 yamato_brawler] |
| 5 | 6400 | Extra Charge | 800 | s1 | utility | 4800/800/800 | OK (info: bought 6400 vs median 2400 in 31 other builds, no action) |
| 6 | 7200 | Extra Spirit | 800 | s1 | SP 12.5 | 4800/1600/800 | OK (info: bought 7200 vs median 1600 in 42 other builds, no action) |
| 7 | 8000 | Mystic Expansion | 800 | s1 | utility | 4800/2400/800 | OK |
| 8 | 8800 | Sprint Boots | 800 | v1 | utility | 4800/2400/1600 | OK |
| 9 | 9600 | Trophy Collector | 800 | v2 | utility | 4800/2400/2400 | FLAG LOW: 9.6k with Sprint Boots 8.8k, passive souls early enough. Rich Lightning Scroll sells it: health 6.4k>4.8k loses the 6.4k step; sell Greater Expansion instead. |
| 10 | 10400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 4800/3200/2400 | OK (info: bought 10400 vs median 6400 in 36 other builds, no action) |
| 11 | 12000 | Compress Cooldown | 1600 | s2 | utility | 4800/4800/2400 | OK |
| 12 | 12800 | Extra Health | 800 | v1 | HP 263 | 4800/4800/3200 | FLAG LOW: 12.8k, then Fortitude 15.2k: health 4.8k only @15.2k and ends 6.4k at 40k souls: thinnest health of my 21 builds. Mobile hero, so allowed by the health-delay rule. [vs 20 other builds: median 7200, min 1600 ratking, max 35200 holliday_spirit] |
| 13 | 15200 | Fortitude | 2400 | v3 | HP 117 | 4800/4800/5600 | OK |
| 14 | 16000 | Mystic Burst | 800 | s1 | utility | 4800/5600/5600 | FLAG MED: Swap target. Tankbuster (2400 paid) consumes it; taking Slowing Hex instead makes Tankbuster 3200 and leaves 13 slots. Buy Slowing Hex + Vortex Web together as one swap (Hex is Vortex's component). [vs 24 other builds: median 4000, min 800 bebop_bomb, max 20000 yamato] |
| 15 | 18400 | Rapid Recharge | 2400 | s3 | utility | 4800/8000/5600 | OK |
| 16 | 20800 | Tankbuster | 2400 | s3 | HP 16 | 4800/10400/5600 | OK |
| 17 | 21600 | Guardian Ward | 800 | v2 | utility | 4800/10400/6400 | OK (info: bought 21600 vs median 11200 in 9 other builds, no action) |
| 18 | 24800 | Surge of Power | 3200 | s3 | SP 8.8 | 4800/13600/6400 | FLAG LOW: 24.8k (ratio 1.94, others median 12.8k); ImbuedTechPower 28 for 3200 = 8.8 SP/1k and imbue on the dragon. Before Guardian Ward (21.6k) no spike moves. [vs 13 other builds: median 12800, min 5600 seven, max 24000 danny] |
| 19 | 27200 | Greater Expansion | 2400 | s3 | TR% 3.1 | 4800/16000/6400 | OK |
| 20 | 28800 | Superior Cooldown | 1600 | s3 | utility | 4800/17600/6400 | OK |
| 21 | 35200 | Escalating Exposure | 6400 | s4 | TR% 2.7 | 4800/24000/6400 | OK |
| 22 | 40000 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 4800/28800/6400 | OK |

## Swap / "Instead of" boxes re-walked
| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |
|---|---|---|---|---|---|---|
| base | - | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 | - |
| Lots of dashers: Slowing Hex instead of Mystic Burst | swap:Mystic Burst=Slowing Hex | 4800/30400/6400 | gun@5600, spirit@12000, health@15200 | 13 | 41600 | FLAG (13 slots, +1600) |
| Lots of dashers: Vortex Web instead of Escalating Exposure | swap:Escalating Exposure=Vortex Web | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 | OK |
| Lots of dashers: Knockdown instead of Surge of Power | swap:Surge of Power=Knockdown | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 | OK (imbue on dragon lost) |
| Proposed merged swap: Slowing Hex+Vortex Web instead of Mystic Burst+Escalating Exposure | swap:Mystic Burst=Slowing Hex ; swap:Escalating Exposure=Vortex Web | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 | OK |

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 |
| Surge of Power before Guardian Ward | mv:Surge of Power>before:Guardian Ward | 4800/28800/6400 | gun@5600, spirit@12000, health@15200 | 12 | 40000 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 4800, spirit 28800, health 6400. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** Counters: Metal Skin (v3) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Plated Armor (v4) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Counterspell (v3) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Spirit Resilience (v3) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Bullet Resilience (v3) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Unstoppable (v4) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** I'm rich as fuck: Mystic Reverb (s4) sells Express Shot (w3): gun 4800>1600 (loses 4800)
- **FLAG** I'm rich as fuck: Spirit Burn (s4) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** I'm rich as fuck: Lightning Scroll (s4) sells Trophy Collector (v2): health 6400>4800 (loses 6400)

## Other findings
- Gun / spirit / health 4.8k: gun @5600, spirit @12000, health @15200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

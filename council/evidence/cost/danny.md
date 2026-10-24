# Cost-efficiency audit: danny (Rizuhble's Belly Flop Danny)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@16000, spirit@8000, health@12800. End of core: 48000 souls, gun 4800 / spirit 25600 / health 17600, 12 slots.

Result: MED Sharpshooter @16.0k = gun 4.8k lands 4th (his rule: HV>Opening Rounds>Sharpshooter); MED every counter + Mystic Reverb sells Opening Rounds (gun 4.8k>3.2k); LOW Surge of Power @24.0k after Greater Expansion; LOW Stamina Mastery 2400 for 0 hp
Minimal fix: Sharpshooter right after Opening Rounds (gun 4.8k @4.8k, spirit 4.8k 8.0k>11.2k, health 12.8k>16.0k); counters/Reverb sell Enchanter's Emblem or Extra Stamina line, not Opening Rounds; Surge of Power before Greater Expansion

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Opening Rounds | 800 | w2 | SP 4.4 WD% 5.0 | 1600/0/0 | FLAG MED: Counters desc and Mystic Reverb note sell this: gun invest 4800>3200, the 4.8k spike is lost the moment the counter is bought. Sell Enchanter's Emblem (health 17.6k>16.0k, no spike crossed) or Reactive Barrier instead. |
| 3 | 2400 | Grit | 800 | v1 | utility | 1600/0/800 | OK (info: bought 2400 vs median 6400 in 26 other builds, no action) |
| 4 | 3200 | Extra Spirit | 800 | s1 | SP 12.5 | 1600/800/800 | OK (info: bought 3200 vs median 1600 in 42 other builds, no action) |
| 5 | 4000 | Mystic Burst | 800 | s1 | utility | 1600/1600/800 | OK |
| 6 | 4800 | Mystic Expansion | 800 | s1 | utility | 1600/2400/800 | OK (info: bought 4800 vs median 10400 in 29 other builds, no action) |
| 7 | 5600 | Extra Stamina | 800 | v1 | utility | 1600/2400/1600 | OK |
| 8 | 6400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 1600/3200/1600 | OK |
| 9 | 8000 | Compress Cooldown | 1600 | s2 | utility | 1600/4800/1600 | OK |
| 10 | 9600 | Enchanter's Emblem | 1600 | v2 | SP 9.4 TR% 11.3 | 1600/4800/3200 | OK |
| 11 | 10400 | Reactive Barrier | 800 | v2 | utility | 1600/4800/4000 | OK |
| 12 | 12800 | Stamina Mastery | 2400 | v3 | utility | 1600/4800/6400 | FLAG LOW: 2400 souls for 0 hp (Stamina 2, air move 23%). It is what pushes health to 4.8k @12.8k. Extra Health (800, 210 hp) then Fortitude would give 585 hp for 3200. Rich Focus Lens also sells it: health 17.6k>14.4k (loses the 16k step); sell Reactive Barrier line instead. Judgement call otherwise. |
| 13 | 16000 | Sharpshooter | 3200 | w3 | WD% 3.1 | 4800/4800/6400 | FLAG MED: Bought 4th-last of the mid items at 16.0k; gun 4.8k only lands here (800 and 1.6k steps idle for 14k souls). Danny rule: keep HV>Opening Rounds>Sharpshooter (in-game build). Fix A (rule order): move right after Opening Rounds = gun 4.8k @4.8k. Fix B (compromise): after Compress Cooldown = gun @11.2k, health @16.0k. |
| 14 | 18400 | Tankbuster | 2400 | s3 | HP 16 | 4800/7200/6400 | OK |
| 15 | 20800 | Greater Expansion | 2400 | s3 | TR% 3.1 | 4800/9600/6400 | OK |
| 16 | 24000 | Surge of Power | 3200 | s3 | SP 8.8 | 4800/12800/6400 | FLAG LOW: 24.0k after Tankbuster (18.4k) and Greater Expansion (20.8k, 0 spirit power, TechResist 10). SoP = ImbuedTechPower 28 for 3200 = 8.8 SP/1k plus 20% fire rate; Greater Expansion gives none. Move SoP before Greater Expansion: no spike moves (tested). [vs 13 other builds: median 12800, min 5600 seven, max 24800 paige] |
| 17 | 30400 | Diviner's Kevlar | 6400 | v4 | SP 6.3 | 4800/12800/12800 | OK |
| 18 | 35200 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 4800/17600/12800 | OK |
| 19 | 36800 | Superior Cooldown | 1600 | s3 | utility | 4800/19200/12800 | OK |
| 20 | 43200 | Spirit Burn | 6400 | s4 | utility | 4800/25600/12800 | OK |
| 21 | 48000 | Indomitable | 4800 | v4 | BR% 1.6 TR% 1.6 | 4800/25600/17600 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 4800/25600/17600 | gun@16000, spirit@8000, health@12800 | 12 | 48000 |
| Fix A (rule order): Sharpshooter after Opening Rounds | mv:Sharpshooter>after:Opening Rounds | 4800/25600/17600 | gun@4800, spirit@11200, health@16000 | 12 | 48000 |
| Fix B (compromise) + Surge of Power before Greater Expansion | mv:Sharpshooter>after:Compress Cooldown ; mv:Surge of Power>before:Greater Expansion | 4800/25600/17600 | gun@11200, spirit@8000, health@16000 | 12 | 48000 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 4800, spirit 25600, health 17600. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** Counters: Metal Skin (v3) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** Counters: Plated Armor (v4) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** Counters: Counterspell (v3) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** Counters: Dispel Magic (v3) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** Counters: Spirit Resilience (v3) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** Counters: Unstoppable (v4) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** I'm rich as fuck: Mystic Reverb (s4) sells Opening Rounds (w2): gun 4800>3200 (loses 4800)
- **FLAG** I'm rich as fuck: Focus Lens (s4) sells Stamina Mastery (v3): health 17600>14400 (loses 16000)

## Other findings
- Mystic Burst @4.0k: OK, Chimera explosion 70+1.5xSP = 125 at SP 36.8 (>80). Tankbuster @18.4k: Chimera 70+1.5x110 = 235 (>165). Thresholds were already checked in a7; only these two re-derived.
- Gun / spirit / health 4.8k: gun @16000, spirit @8000, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

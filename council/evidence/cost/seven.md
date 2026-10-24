# Cost-efficiency audit: seven (Rizuhble's Power Outage Seven)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@5600, health@12800. End of core: 46400 souls, gun 3200 / spirit 20800 / health 22400, 12 slots.

Result: INFO gun 3.2k (Monster Rounds>Cultist) never 4.8k; LOW Mystic Expansion @18.4k imbue on the ult; reorder box tested harmless
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Monster Rounds | 800 | w1 | utility | 800/0/0 | OK (info: bought 800 vs median 1600 in 16 other builds, no action) |
| 2 | 1600 | Extra Spirit | 800 | s1 | SP 12.5 | 800/800/0 | OK |
| 3 | 2400 | Extra Stamina | 800 | v1 | utility | 800/800/800 | OK (info: bought 2400 vs median 5600 in 20 other builds, no action) |
| 4 | 3200 | Arcane Surge | 800 | s2 | SP 12.5 | 800/2400/0 | OK |
| 5 | 5600 | Surge of Power | 2400 | s3 | SP 8.8 | 800/4800/0 | OK: 5.6k, 2400 paid (Extra Spirit consumed): spirit 4.8k lands here per Seven rule (SoP/Arcane Surge early). [vs 13 other builds: median 13600, min 5600 violet, max 24800 paige] |
| 6 | 8000 | Cultist Sacrifice | 2400 | w3 | HP 16 WD% 3.1 | 3200/4800/0 | OK: 8.0k (2400 paid), rule: early farm/Cultist. |
| 7 | 9600 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 3200/4800/1600 | OK |
| 8 | 10400 | Sprint Boots | 800 | v1 | utility | 3200/4800/2400 | OK |
| 9 | 12000 | Healbane | 1600 | v2 | SP 4.4 | 3200/4800/4000 | OK: 12.0k fresh T2 with named sell for a counter. |
| 10 | 12800 | Enduring Speed | 800 | v2 | utility | 3200/4800/4800 | OK |
| 11 | 14400 | Mystic Vulnerability | 1600 | s2 | TR% 5.0 | 3200/6400/4800 | OK |
| 12 | 16000 | Duration Extender | 1600 | s2 | utility | 3200/8000/4800 | OK |
| 13 | 17600 | Compress Cooldown | 1600 | s2 | utility | 3200/9600/4800 | OK |
| 14 | 18400 | Mystic Expansion | 800 | s1 | utility | 3200/10400/4800 | FLAG LOW: 800 @18.4k (ratio 2.1), imbue on the ult, Greater Expansion @40.0k. Ult range could be bought earlier; no spike cost (spirit already 4.8k @5.6k). [vs 29 other builds: median 8800, min 1600 paradox_bomb, max 28000 viscous] |
| 15 | 23200 | Escalating Exposure | 4800 | s4 | TR% 2.7 | 3200/15200/4800 | OK |
| 16 | 24800 | Superior Duration | 1600 | s3 | BR% 2.5 | 3200/16800/4800 | OK |
| 17 | 31200 | Unstoppable | 6400 | v4 | HP 20 | 3200/16800/11200 | OK |
| 18 | 32800 | Superior Cooldown | 1600 | s3 | utility | 3200/18400/11200 | OK |
| 19 | 37600 | Infuser | 4800 | v4 | SP 5.6 HP 16 TR% 1.6 | 3200/18400/16000 | OK |
| 20 | 40000 | Greater Expansion | 2400 | s3 | TR% 3.1 | 3200/20800/16000 | OK |
| 21 | 46400 | Diviner's Kevlar | 6400 | v4 | SP 6.3 | 3200/20800/22400 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 3200/20800/22400 | gun never, spirit@5600, health@12800 | 12 | 46400 |
| Lost-lane reorder: Mystic Vulnerability before Cultist Sacrifice | mv:Mystic Vulnerability>before:Cultist Sacrifice | 3200/20800/22400 | gun never, spirit@5600, health@14400 | 12 | 46400 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 3200, spirit 20800, health 22400. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Spirit @5.6k then health @12.8k: fighty-hero rule (~11-12k) met within 1k.
- Gun / spirit / health 4.8k: gun NEVER (end 3200), spirit @5600, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

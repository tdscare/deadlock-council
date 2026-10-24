# Cost-efficiency audit: bebop (Rizuhble's 1v1 Me Bro Bebop)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@7200, spirit@18400, health@12800. End of core: 46400 souls, gun 14400 / spirit 4800 / health 27200, 12 slots.

Result: LOW Fortitude @33.6k bought after two 6.4k items (2400 for 375 hp); LOW rich box sells Bullet Resist Shredder / Spirit Snatch drop spirit 4.8k to 3.2k / 1.6k
Minimal fix: Fortitude right after Spirit Snatch (spikes unchanged: gun 7.2k, health 12.8k, spirit 18.4k); rich Lucky Shot/Spellslinger sell Stalker or Enduring Speed-line item instead

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Spirit Strike | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 3200 in 12 other builds, no action) |
| 2 | 1600 | Headshot Booster | 800 | w1 | HP 38 | 800/800/0 | OK |
| 3 | 3200 | Stalker | 1600 | w2 | HP 31 | 2400/800/0 | OK |
| 4 | 4800 | Bullet Resist Shredder | 1600 | s2 | WD% 5.6 BR% 5.6 | 2400/2400/0 | FLAG LOW: Rich box Lucky Shot sells this: spirit 4.8k>3.2k. Sell Stalker (gun 14.4k>12.8k, nothing crossed) instead. [vs 10 other builds: median 14400, min 3200 bebop_support, max 19200 ivy_carry] |
| 5 | 7200 | Headhunter | 2400 | w3 | HP 16 WD% 1.6 | 4800/2400/0 | OK: 7.2k, gun 4.8k lands here (damage first), health 4.8k @12.8k (Veil Walker) before Hunter's Aura: matches in-your-face rule. |
| 6 | 8000 | Sprint Boots | 800 | v1 | utility | 4800/2400/800 | OK |
| 7 | 8800 | Extra Health | 800 | v1 | HP 263 | 4800/2400/1600 | OK |
| 8 | 9600 | Enduring Speed | 800 | v2 | utility | 4800/2400/2400 | OK |
| 9 | 12800 | Veil Walker | 3200 | v3 | SP 1.9 HP 39 | 4800/2400/5600 | OK |
| 10 | 16000 | Hunter's Aura | 3200 | w3 | HP 31 | 8000/2400/5600 | OK |
| 11 | 18400 | Spirit Snatch | 2400 | s3 | HP 23 | 8000/4800/5600 | FLAG LOW: Rich box Spellslinger sells this: spirit 4.8k>1.6k. Sell Stalker or Siphon-line item instead. |
| 12 | 24800 | Siphon Bullets | 6400 | v4 | WD% 2.3 BR% 1.6 | 8000/4800/12000 | OK |
| 13 | 31200 | Vampiric Burst | 6400 | v4 | HP 16 WD% 0.9 BR% 1.6 | 8000/4800/18400 | OK |
| 14 | 33600 | Fortitude | 2400 | v3 | HP 117 | 8000/4800/20800 | FLAG LOW: 2400 for 375 hp (+heal out of combat) = 156 hp/1k, best hp/1k in the build, but bought 33.6k after Siphon (24.8k) and Vampiric Burst (31.2k). Other builds buy it median 12.8k (ratio 2.63). Move after Spirit Snatch: no spike changes (tested). [vs 20 other builds: median 12800, min 8000 haze, max 43200 drifter_spirit] |
| 15 | 40000 | Crippling Headshot | 6400 | w4 | HP 20 | 14400/4800/20800 | OK |
| 16 | 46400 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 14400/4800/27200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 14400/4800/27200 | gun@7200, spirit@18400, health@12800 | 12 | 46400 |
| Fortitude after Spirit Snatch | mv:Fortitude>after:Spirit Snatch | 14400/4800/27200 | gun@7200, spirit@18400, health@12800 | 12 | 46400 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 14400, spirit 4800, health 27200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** I'm rich as fuck: Lucky Shot (w4) sells Bullet Resist Shredder (s2): spirit 4800>3200 (loses 4800)
- **FLAG** I'm rich as fuck: Spellslinger (w4) sells Spirit Snatch (s3): spirit 4800>1600 (loses 4800)

## Other findings
- Two 6.4k in a row (Siphon 24.8k, Vampiric Burst 31.2k) is allowed (<=3 back to back).
- Gun / spirit / health 4.8k: gun @7200, spirit @18400, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

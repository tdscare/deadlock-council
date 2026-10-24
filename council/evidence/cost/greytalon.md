# Cost-efficiency audit: greytalon (Rizuhble's One Shot Grey Talon)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@16800, spirit@5600, health@10400. End of core: 48000 souls, gun 4800 / spirit 32000 / health 11200, 12 slots.

Result: LOW rich Refresher sells Sharpshooter: gun 4.8k>1.6k; LOW Superior Cooldown 1600 bought after Indomitable (33.6k->35.2k)
Minimal fix: Refresher sells Enchanter's Emblem/Stamina Mastery line; Superior Cooldown before Indomitable (spikes unchanged)

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Charge | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 2400 in 31 other builds, no action) |
| 2 | 1600 | Mystic Burst | 800 | s1 | utility | 0/1600/0 | OK (info: bought 1600 vs median 4000 in 24 other builds, no action) |
| 3 | 2400 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/1600/0 | OK: 2.4k, 800, consumed into Sharpshooter @15.2k (Sharpshooter paid 800 after Long Range). [vs 24 other builds: median 800, min 800 danny, max 19200 holliday] |
| 4 | 3200 | Extra Spirit | 800 | s1 | SP 12.5 | 800/2400/0 | OK (info: bought 3200 vs median 1600 in 42 other builds, no action) |
| 5 | 4800 | Compress Cooldown | 1600 | s2 | utility | 800/4000/0 | OK (info: bought 4800 vs median 14400 in 43 other builds, no action) |
| 6 | 5600 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 800/4800/0 | OK |
| 7 | 6400 | Extra Stamina | 800 | v1 | utility | 800/4800/800 | OK |
| 8 | 8000 | Enchanter's Emblem | 1600 | v2 | SP 9.4 TR% 11.3 | 800/4800/2400 | OK: 8.0k fresh T2 dead-end but named sells (Tankbuster counter, Witchmail); 9.4 SP/1k. |
| 9 | 10400 | Stamina Mastery | 2400 | v3 | utility | 800/4800/4800 | OK |
| 10 | 12800 | Tankbuster | 2400 | s3 | HP 16 | 800/7200/4800 | OK: 12.8k: Charged Shot (T3) 80+54+1.0x99 = 233 > 165. |
| 11 | 14400 | Long Range | 1600 | w2 | utility | 2400/7200/4800 | OK (info: bought 14400 vs median 5600 in 5 other builds, no action) |
| 12 | 15200 | Sharpshooter | 800 | w3 | WD% 3.1 | 3200/7200/4800 | FLAG LOW: Rich Refresher sells this: gun 4.8k>1.6k. Sell Enchanter's Emblem instead. |
| 13 | 16800 | Recharging Rush | 1600 | w2 | WD% 6.3 | 4800/7200/4800 | OK: 16.8k: Charged Shot 80+54+1.0x102 = 236 in one hit (>200 in 3.5s), refunds the arrow charge (17s cooldown). Slow-firing hero but ability meets the threshold; gun 4.8k lands here (named sell for a counter). [vs 7 other builds: median 10400, min 6400 yamato_brawler, max 17600 venator_grenade] |
| 14 | 19200 | Rapid Recharge | 2400 | s3 | utility | 4800/9600/4800 | OK |
| 15 | 22400 | Surge of Power | 3200 | s3 | SP 8.8 | 4800/12800/4800 | OK (info: bought 22400 vs median 12800 in 13 other builds, no action) |
| 16 | 27200 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 4800/17600/4800 | OK |
| 17 | 33600 | Indomitable | 6400 | v4 | BR% 1.6 TR% 1.6 | 4800/17600/11200 | OK |
| 18 | 35200 | Superior Cooldown | 1600 | s3 | utility | 4800/19200/11200 | OK |
| 19 | 41600 | Spirit Burn | 6400 | s4 | utility | 4800/25600/11200 | OK |
| 20 | 48000 | Mystic Reverb | 6400 | s4 | utility | 4800/32000/11200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Tested fixes / reorders (each re-walked)
| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |
|---|---|---|---|---|---|
| base | - | 4800/32000/11200 | gun@16800, spirit@5600, health@10400 | 12 | 48000 |
| Superior Cooldown before Indomitable | mv:Superior Cooldown>before:Indomitable | 4800/32000/11200 | gun@16800, spirit@5600, health@10400 | 12 | 48000 |

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 4800, spirit 32000, health 11200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** I'm rich as fuck: Refresher (s4) sells Sharpshooter (w3): gun 4800>1600 (loses 4800)

## Other findings
- Spikes: spirit @5.6k, health @10.4k, gun @16.8k. Gun items (HV, Long Range, Sharpshooter, Recharging Rush) only pay for bullets; the arrow is an ability, so the gun spike is a Kieran-rule item, not a damage item for this style.
- Gun / spirit / health 4.8k: gun @16800, spirit @5600, health @10400.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

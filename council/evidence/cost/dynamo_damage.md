# Cost-efficiency audit: dynamo_damage (Rizuhble's Belly Slam Dynamo)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@7200, spirit@15200, health@11200. End of core: 51200 souls, gun 4800 / spirit 35200 / health 11200, 12 slots.

Result: MED every counter and Witchmail sell Headhunter: gun 4.8k>1.6k; LOW Mystic Reverb/Boundless sell Recharging Rush drops gun to 3.2k
Minimal fix: Counters/Witchmail sell Rapid Recharge (or Compress Cooldown line item) instead of Headhunter; Boundless sells Rapid Recharge

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Headshot Booster | 800 | w1 | HP 38 | 800/0/0 | OK (info: bought 800 vs median 1600 in 9 other builds, no action) |
| 2 | 1600 | Mystic Burst | 800 | s1 | utility | 800/800/0 | OK: 1.6k lane buy, Kinetic Pulse 115+1.55x11.4 = 133 (>80), feeds Tankbuster @13.6k (stomp tier 3: 115+135+1.55x39.9 = 312 > 165). [vs 24 other builds: median 4000, min 800 bebop_bomb, max 20000 yamato] |
| 3 | 2400 | Extra Charge | 800 | s1 | utility | 800/1600/0 | OK |
| 4 | 4800 | Headhunter | 2400 | w3 | HP 16 WD% 1.6 | 3200/1600/0 | FLAG MED: Counters desc and Witchmail note sell this: gun invest 4800>1600, the 4.8k spike is gone as soon as the counter is bought. Sell Rapid Recharge (spirit 35.2k>32.8k, nothing crossed). |
| 5 | 5600 | Sprint Boots | 800 | v1 | utility | 3200/1600/800 | OK |
| 6 | 7200 | Recharging Rush | 1600 | w2 | WD% 6.3 | 4800/1600/800 | OK: 7.2k: Kinetic Pulse at tier 3 = 115+135+1.55x24 = 287 in one hit (>200 in 3.5s); gun 4.8k lands here. Boundless note sells it: gun 4.8k>3.2k, sell Rapid Recharge instead. [vs 7 other builds: median 13600, min 6400 yamato_brawler, max 17600 venator_grenade] |
| 7 | 8000 | Enduring Speed | 800 | v2 | utility | 4800/1600/1600 | OK |
| 8 | 11200 | Warp Stone | 3200 | v3 | BR% 9.4 | 4800/1600/4800 | OK: 11.2k, health 4.8k lands (v 4.8k) after gun 4.8k @7.2k; ult-gap closer, early by design. [vs 10 other builds: median 24000, min 12000 solomon, max 29600 solomon_support] |
| 9 | 13600 | Tankbuster | 2400 | s3 | HP 16 | 4800/4000/4800 | OK |
| 10 | 15200 | Compress Cooldown | 1600 | s2 | utility | 4800/5600/4800 | OK |
| 11 | 16800 | Quicksilver Reload | 1600 | s2 | FR% 6.3 | 4800/7200/4800 | OK: 16.8k, 1600 now and consumed into Mercurial Magnum @25.6k (paid 4800). Ratio 2.1 vs other builds fine. [vs 11 other builds: median 8000, min 3200 mina, max 17600 vyper_gun] |
| 12 | 19200 | Rapid Recharge | 2400 | s3 | utility | 4800/9600/4800 | OK |
| 13 | 20800 | Superior Cooldown | 1600 | s3 | utility | 4800/11200/4800 | OK |
| 14 | 25600 | Mercurial Magnum | 4800 | s4 | SP 1.1 FR% 3.4 | 4800/16000/4800 | OK |
| 15 | 32000 | Unstoppable | 6400 | v4 | HP 20 | 4800/16000/11200 | OK |
| 16 | 38400 | Mystic Reverb | 6400 | s4 | utility | 4800/22400/11200 | OK |
| 17 | 44800 | Spirit Burn | 6400 | s4 | utility | 4800/28800/11200 | OK |
| 18 | 51200 | Refresher | 6400 | s4 | BR% 2.3 TR% 2.2 | 4800/35200/11200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 4800, spirit 35200, health 11200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- **FLAG** Counters: Metal Skin (v3) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Plated Armor (v4) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Spirit Resilience (v3) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Counterspell (v3) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Dispel Magic (v3) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** Counters: Reactive Barrier (v2) sells Headhunter (w3): gun 4800>1600 (loses 4800)
- **FLAG** I'm rich as fuck: Boundless Spirit (s4) sells Recharging Rush (w2): gun 4800>3200 (loses 4800)
- **FLAG** I'm rich as fuck: Witchmail (v4) sells Headhunter (w3): gun 4800>1600 (loses 4800)

## Other findings
- Spikes: gun @7.2k, health @11.2k, spirit @15.2k: damage first, then health, then spirit: matches priority rule.
- Mercurial Magnum is a Tech-slot item (spirit invest). Kieran counts it as gun for his purposes; spikes here follow the game slot.
- Gun / spirit / health 4.8k: gun @7200, spirit @15200, health @11200.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

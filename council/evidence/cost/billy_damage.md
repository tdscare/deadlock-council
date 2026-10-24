# billy_damage: Rizuhble's Punch Drunk Billy (Damage Billy)

Cost-efficiency audit. Verdict: **0 flags**

walk1 flags: none. 4.8k invest crossings (souls spent): gun @7200, spirit @16800, health @10400. Core ends 49600 souls, 12 slots.

## Swap / Instead-of / sell-for boxes (re-walked)
- No "Swap"/"Instead of" box in this build.
- Counters sell Stalker (gun 24000 -> 22400, fine). Rich boxes: Spellbreaker<-Spirit Shielding (health +4800), Phantom Strike<-Cultist Sacrifice (gun 24000 -> 20800, fine), Witchmail<-Spirit Snatch (spirit 12800 -> 9600, fine). Core: Silencer sells Bullet Resist Shredder (spirit stays >= 4.8k).

## Flags
- WATCH Scourge is the last item at 49.6k (4 other builds 35.2k-44.0k). Nothing earlier to move: it is the 12th slot behind Colossus and Silencer.

## Proposed fix
- none

## Items in buy order
Invest column = gun/spirit/health souls spent after the buy. Stats are per 1000 souls of the item's full price. "Other builds" = same item elsewhere in data.js (souls at purchase from the walk).

| # | Item (box) | Price | Souls after | Invest g/s/h | Stats per 1000 | Other builds | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Close Quarters (Early) | 800 | 800 | 800/0/0 | effect only | 13 builds, 800-10400, med 1600 | OK |
| 2 | Melee Lifesteal (Early) | 800 | 1600 | 800/0/800 | effect only | 12 builds, 800-5600, med 1600 | OK |
| 3 | Monster Rounds (Early) | 800 | 2400 | 1600/0/800 | effect only | 16 builds, 800-2400, med 1600 | OK |
| 4 | Grit (Early) | 800 | 3200 | 1600/0/1600 | effect only | 26 builds, 1600-12000, med 6400 | OK |
| 5 | Stalker (Early) | 1600 | 4800 | 3200/0/1600 | HP 31.3, move m/s 0.9 | 10 builds, 2400-13600, med 4000 | OK - named sell (counters box) |
| 6 | Cultist Sacrifice (Early) | 3200 (net 2400) | 7200 | 5600/0/1600 | HP 15.6, weapon dmg % 3.1 | 10 builds, 4000-8800, med 7200 | OK - 7.2k, inside Kieran's ~8 min Billy window; gun 4.8k lands here |
| 7 | Lifestrike (Mid) | 3200 (net 2400) | 9600 | 5600/0/4000 | HP 39.1 | 11 builds, 6400-16000, med 10400 | OK - upgrade of Melee Lifesteal |
| 8 | Spirit Shielding (Mid) | 1600 (net 800) | 10400 | 5600/0/4800 | spirit resist 11.3 | 9 builds, 7200-18400, med 9600 | OK - upgrade of Grit |
| 9 | Melee Charge (Mid) | 1600 | 12000 | 7200/0/4800 | bullet resist 3.8 | 8 builds, 2400-24800, med 11200 | OK - T2 at 12.0k, upgraded at 24.0k; heavy melee damage is live from the buy |
| 10 | Spirit Strike (Mid) | 800 | 12800 | 7200/800/4800 | effect only | 12 builds, 800-15200, med 3200 | OK |
| 11 | Bullet Resist Shredder (Mid) | 1600 | 14400 | 7200/2400/4800 | weapon dmg % 5.6, bullet resist 5.6 | 10 builds, 3200-19200, med 14400 | OK |
| 12 | Spirit Snatch (Mid) | 3200 (net 2400) | 16800 | 7200/4800/4800 | HP 23.4 | 12 builds, 8000-32000, med 16000 | OK - upgrade of Spirit Strike |
| 13 | Point Blank (Mid) | 3200 (net 2400) | 19200 | 9600/4800/4800 | HP 23.4 | 10 builds, 12800-32000, med 16800 | OK - upgrade of Close Quarters |
| 14 | Crushing Fists (Mid) | 6400 (net 4800) | 24000 | 14400/4800/4800 | bullet resist 1.9 | 8 builds, 14400-36800, med 29600 | OK - upgrade of Melee Charge at 24.0k, after Point Blank; others 24.0k-36.8k, so not a first item |
| 15 | Extra Charge (Mid) | 800 | 24800 | 14400/5600/4800 | effect only | 31 builds, 800-28000, med 2400 | OK - bought 24.8k, upgraded to Rapid Recharge 2.4k later; Bashdown has 1 charge |
| 16 | Rapid Recharge (Mid) | 3200 (net 2400) | 27200 | 14400/8000/4800 | effect only | 30 builds, 5600-49600, med 18400 | OK - upgrade of Extra Charge |
| 17 | Berserker (Mid) | 3200 | 30400 | 17600/8000/4800 | bullet resist 2.5 | 10 builds, 12800-28000, med 23200 | OK |
| 18 | Colossus (Late) | 6400 | 36800 | 17600/8000/11200 | weapon dmg % 2.3 | 8 builds, 32800-46400, med 38400 | OK |
| 19 | Silencer (Late) | 6400 | 43200 | 24000/6400/11200 | spirit resist 1.9 | 8 builds, 36000-53600, med 41600 | OK (sells Bullet Resist Shredder) |
| 20 | Scourge (Late) | 6400 | 49600 | 24000/12800/11200 | HP 15.6, spirit resist 6.3 | 4 builds, 35200-44000, med 40000 | WATCH - last item, 49.6k (others 35.2k-44.0k) |

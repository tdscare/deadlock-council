# graves_ult: Rizuhble's Zombie Horde Graves (Ult Graves)

Cost-efficiency audit. Verdict: **0 hard flags, 1 colour gap**

walk1 flags: none. 4.8k invest crossings (souls spent): gun never, spirit @5600, health @9600. Core ends 54400 souls, 12 slots.

## Swap / Instead-of / sell-for boxes (re-walked)
- No "Swap"/"Instead of" box in this build.
- Counters sell Arcane Surge (spirit 40000 -> 38400). Rich: Cursed Relic<-Arcane Surge, Cheat Death<-Spirit Shielding (health +4800), Refresher<-Enchanter's Emblem (health -1600, 8000 left): nothing breaks.

## Flags
- GAP gun is only Heroic Aura (3200, lone weapon item), 1600 short of 4.8k. Kieran wants every colour at 4.8k on most heroes; this is a decision, not a hard fault.
- WATCH Diviner's Kevlar at 25.6k is the earliest of 7 builds (others 28.8k-53.6k); it is the first big health after 9.6k and starts a 3-buy run (Kevlar 6400, Boundless 4800, Echo Shard 6400) that ends at 36.8k. Rule allows 1-3 in a row.
- WATCH Spirit Burn is last at 54.4k (others 28.8k-56.0k).

## Proposed fix
- Optional: Mystic Shot (T2 weapon, scales with spirit; Kieran: buy right after the spirit spike) gives gun 3200 + 1600 = 4800. It needs a slot and 1600: walked "Enchanter's Emblem -> Mystic Shot": gun 4.8k @12.8k but health 4.8k slips 9.6k -> 25.6k, so the Emblem cannot be the one to go. Pick another item to replace, then re-walk.

## Items in buy order
Invest column = gun/spirit/health souls spent after the buy. Stats are per 1000 souls of the item's full price. "Other builds" = same item elsewhere in data.js (souls at purchase from the walk).

| # | Item (box) | Price | Souls after | Invest g/s/h | Stats per 1000 | Other builds | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Extra Spirit (Early) | 800 | 800 | 0/800/0 | SP 12.5 | 42 builds, 800-19200, med 1600 | OK |
| 2 | Extra Stamina (Early) | 800 | 1600 | 0/800/800 | stamina 1.3 | 20 builds, 800-20000, med 5600 | OK |
| 3 | Arcane Surge (Early) | 1600 (net 800) | 2400 | 0/2400/0 | stamina 0.6 | 3 builds, 3200-3200, med 3200 | OK - spirit 4.8k @5.6k; named sell for Cursed Relic |
| 4 | Improved Spirit (Early) | 1600 (net 800) | 3200 | 0/3200/0 | SP 11.3, HP 46.9, sprint m/s 0.6 | 36 builds, 1600-32000, med 6400 | OK - upgrade of Extra Spirit |
| 5 | Grit (Early) | 800 | 4000 | 0/3200/800 | effect only | 26 builds, 1600-12000, med 6400 | OK |
| 6 | Duration Extender (Early) | 1600 | 5600 | 0/4800/800 | effect only | 22 builds, 3200-25600, med 16000 | OK |
| 7 | Enchanter's Emblem (Early) | 1600 | 7200 | 0/4800/2400 | SP 9.4, spirit resist 11.3 | 17 builds, 4800-20000, med 9600 | OK - T2 health 1600 (health 4.8k @9.6k); named sell for Refresher |
| 8 | Spirit Lifesteal (Mid) | 1600 | 8800 | 0/4800/4000 | SP 3.8, HP 56.3, spirit LS % 8.1 | 31 builds, 4800-24000, med 14400 | OK - named sell for Magic Carpet |
| 9 | Spirit Shielding (Mid) | 1600 (net 800) | 9600 | 0/4800/4800 | spirit resist 11.3 | 9 builds, 7200-18400, med 9600 | OK - upgrade of Grit |
| 10 | Heroic Aura (Mid) | 3200 | 12800 | 3200/4800/4800 | fire rate % 8.1, bullet resist 5.3, sprint m/s 0.5 | 6 builds, 12000-34400, med 15200 | WATCH - lone 3200 gun item at 12.8k (gun never 4.8k); note "works on ghouls" is the reason it is there |
| 11 | Compress Cooldown (Mid) | 1600 | 14400 | 3200/6400/4800 | effect only | 43 builds, 2400-23200, med 13600 | OK |
| 12 | Superior Duration (Mid) | 3200 (net 1600) | 16000 | 3200/8000/4800 | bullet resist 2.5 | 22 builds, 14400-64000, med 30400 | OK - 1600 net upgrade; others 14.4k-64.0k |
| 13 | Superior Cooldown (Mid) | 3200 (net 1600) | 17600 | 3200/9600/4800 | effect only | 46 builds, 8000-41600, med 25600 | OK - upgrade of Compress Cooldown |
| 14 | Mystic Vulnerability (Mid) | 1600 | 19200 | 3200/11200/4800 | spirit resist 5.0 | 27 builds, 3200-24800, med 14400 | OK |
| 15 | Diviner's Kevlar (Mid) | 6400 | 25600 | 3200/11200/11200 | SP 6.3 | 6 builds, 28800-53600, med 45600 | WATCH - 25.6k, earliest of 7 |
| 16 | Boundless Spirit (Mid) | 6400 (net 4800) | 30400 | 3200/16000/11200 | SP 4.7, HP 11.7 | 38 builds, 23200-59200, med 36000 | OK - upgrade of Improved Spirit |
| 17 | Echo Shard (Late) | 6400 | 36800 | 3200/22400/11200 | bullet resist 0.8, spirit resist 0.8 | 9 builds, 17600-56000, med 35200 | OK - 36.8k, imbue on Borrowed Decree |
| 18 | Escalating Exposure (Late) | 6400 (net 4800) | 41600 | 3200/27200/11200 | spirit resist 2.7 | 28 builds, 21600-62400, med 35200 | OK - upgrade of Mystic Vulnerability |
| 19 | Magic Carpet (Late) | 6400 | 48000 | 3200/33600/9600 | SP 2.2, HP 19.5 | 1 builds, 24800-24800, med 24800 | OK (sells Spirit Lifesteal) |
| 20 | Spirit Burn (Late) | 6400 | 54400 | 3200/40000/9600 | effect only | 24 builds, 28800-56000, med 41600 | WATCH - last item 54.4k |

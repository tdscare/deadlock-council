# mokrill: Rizuhble's Whack-A-Mole Mo (no desc)

Cost-efficiency audit. Verdict: **0 hard flags, 1 colour gap, 1 minor**

walk1 flags: none. 4.8k invest crossings (souls spent): gun never, spirit @4800, health @11200. Core ends 49600 souls, 12 slots.

## Swap / Instead-of / sell-for boxes (re-walked)
- No "Swap"/"Instead of" box in this build.
- Counters sell Torment Pulse (spirit 36800 -> 33600). Rich: Spirit Burn<-Tankbuster, Scourge<-Superior Duration, Witchmail<-Fortitude (health +3200), Mercurial Magnum is an upgrade: spirit 4.8k @4.8k and health 4.8k @11.2k stay.

## Flags
- GAP gun invest is 0 (spirit 4.8k @4.8k, health 4.8k @11.2k). Kieran wants every colour at 4.8k on most heroes; this is a decision, not a hard fault.
- WATCH Duration Extender (20.8k) idles 21.6k souls until Superior Duration (42.4k, 1600 net). Others: holliday_spirit 5.6k, drifter_spirit 1.6k.

## Proposed fix
- Optional: Superior Duration right after Duration Extender. Walked: spirit 16k @22.4k (was 23.2k), health 8k @37.6k (was 36.0k), 4.8k spikes unchanged.

## Items in buy order
Invest column = gun/spirit/health souls spent after the buy. Stats are per 1000 souls of the item's full price. "Other builds" = same item elsewhere in data.js (souls at purchase from the walk).

| # | Item (box) | Price | Souls after | Invest g/s/h | Stats per 1000 | Other builds | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Extra Spirit (Early) | 800 | 800 | 0/800/0 | SP 12.5 | 42 builds, 800-19200, med 1600 | OK |
| 2 | Mystic Burst (Early) | 800 | 1600 | 0/1600/0 | effect only | 24 builds, 800-20000, med 4000 | OK - T1 idle until Tankbuster (23.2k); thresholds are the a7 audit |
| 3 | Quicksilver Reload (Early) | 1600 | 3200 | 0/3200/0 | fire rate % 6.3 | 11 builds, 3200-17600, med 8000 | OK - Mercurial Magnum rich upgrade |
| 4 | Cold Front (Early) | 1600 | 4800 | 0/4800/0 | spirit resist 3.8 | 5 builds, 4800-20800, med 5600 | OK - Arctic Blast late |
| 5 | Sprint Boots (Early) | 800 | 5600 | 0/4800/800 | sprint m/s 2.5 | 39 builds, 800-20800, med 8800 | OK |
| 6 | Enduring Speed (Early) | 1600 (net 800) | 6400 | 0/4800/1600 | move m/s 1.3 | 28 builds, 6400-21600, med 9600 | OK - Juggernaut Slot locked |
| 7 | Extra Health (Early) | 800 | 7200 | 0/4800/2400 | HP 262.5 | 20 builds, 1600-35200, med 8800 | OK |
| 8 | Healbane (Early) | 1600 | 8800 | 0/4800/4000 | SP 4.4 | 12 builds, 8000-19200, med 11200 | OK - named sell for Colossus |
| 9 | Fortitude (Mid) | 3200 (net 2400) | 11200 | 0/4800/6400 | HP 117.2, move m/s 0.5 | 20 builds, 8000-43200, med 12800 | OK - upgrade of Extra Health |
| 10 | Torment Pulse (Mid) | 3200 | 14400 | 0/8000/6400 | HP 31.3 | 8 builds, 4800-22400, med 13600 | OK - 14.4k; named sell (counters) |
| 11 | Compress Cooldown (Mid) | 1600 | 16000 | 0/9600/6400 | effect only | 43 builds, 2400-23200, med 13600 | OK |
| 12 | Improved Spirit (Mid) | 1600 (net 800) | 16800 | 0/10400/6400 | SP 11.3, HP 46.9, sprint m/s 0.6 | 36 builds, 1600-32000, med 6400 | OK - upgrade of Extra Spirit |
| 13 | Mystic Expansion (Mid) | 800 | 17600 | 0/11200/6400 | effect only | 29 builds, 1600-28000, med 8800 | OK |
| 14 | Mystic Vulnerability (Mid) | 1600 | 19200 | 0/12800/6400 | spirit resist 5.0 | 27 builds, 3200-24800, med 14400 | OK |
| 15 | Duration Extender (Mid) | 1600 | 20800 | 0/14400/6400 | effect only | 22 builds, 3200-25600, med 16000 | WATCH - idle 21.6k souls before its upgrade |
| 16 | Tankbuster (Mid) | 3200 (net 2400) | 23200 | 0/16800/6400 | HP 15.6 | 24 builds, 12000-32000, med 17600 | OK - upgrade of Mystic Burst |
| 17 | Superior Cooldown (Mid) | 3200 (net 1600) | 24800 | 0/18400/6400 | effect only | 46 builds, 8000-41600, med 25600 | OK - upgrade of Compress Cooldown |
| 18 | Boundless Spirit (Mid) | 6400 (net 4800) | 29600 | 0/23200/6400 | SP 4.7, HP 11.7 | 38 builds, 23200-59200, med 36000 | OK - upgrade of Improved Spirit |
| 19 | Colossus (Late) | 6400 | 36000 | 0/23200/11200 | weapon dmg % 2.3 | 8 builds, 32800-46400, med 38400 | OK - 36.0k, full 6400 (Fortitude consumed Extra Health) (sells Healbane) |
| 20 | Escalating Exposure (Late) | 6400 (net 4800) | 40800 | 0/28000/11200 | spirit resist 2.7 | 28 builds, 21600-62400, med 35200 | OK - upgrade of Mystic Vulnerability |
| 21 | Superior Duration (Late) | 3200 (net 1600) | 42400 | 0/29600/11200 | bullet resist 2.5 | 22 builds, 14400-64000, med 26400 | WATCH - 42.4k (others 14.4k-64.0k, med 26.4k) |
| 22 | Greater Expansion (Late) | 3200 (net 2400) | 44800 | 0/32000/11200 | spirit resist 3.1 | 28 builds, 16000-46400, med 28800 | OK - 44.8k (others 16.0k-46.4k) |
| 23 | Arctic Blast (Late) | 6400 (net 4800) | 49600 | 0/36800/11200 | spirit resist 1.6 | 2 builds, 20800-32000, med 32000 | OK - upgrade of Cold Front |

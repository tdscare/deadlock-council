# Cost-efficiency audit: kelvin (Rizuhble's Brain Freeze Kelvin)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@4800, health@10400. End of core: 48000 souls, gun 0 / spirit 28800 / health 19200, 12 slots.

Result: INFO gun 0; LOW Infuser (T4) @20.8k earliest in data.js (others median 41.6k)
Minimal fix: none required; if gun 4.8k wanted cheapest is 6 T1s or Headhunter + a T2 (needs 2 slots)

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Extra Charge | 800 | s1 | utility | 0/800/0 | OK (info: bought 800 vs median 2400 in 31 other builds, no action) |
| 2 | 1600 | Extra Spirit | 800 | s1 | SP 12.5 | 0/1600/0 | OK |
| 3 | 4800 | Torment Pulse | 3200 | s3 | HP 31 | 0/4800/0 | OK: 4.8k: 3200 = 100 hp + 18% melee resist + pulse 25+0.23xSP; spirit 4.8k lands here (tanky damage-dealer). [vs 8 other builds: median 14400, min 5600 victor, max 22400 apollo] |
| 4 | 5600 | Extra Regen | 800 | v1 | utility | 0/4800/800 | OK (info: bought 5600 vs median 1600 in 18 other builds, no action) |
| 5 | 6400 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 0/5600/800 | OK |
| 6 | 7200 | Healing Booster | 800 | v2 | utility | 0/5600/1600 | OK |
| 7 | 8800 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 0/5600/3200 | OK |
| 8 | 10400 | Healbane | 1600 | v2 | SP 4.4 | 0/5600/4800 | OK: 10.4k fresh T2, named sell (Spirit Burn, counters). |
| 9 | 12000 | Mystic Vulnerability | 1600 | s2 | TR% 5.0 | 0/7200/4800 | OK |
| 10 | 13600 | Compress Cooldown | 1600 | s2 | utility | 0/8800/4800 | OK |
| 11 | 14400 | Mystic Expansion | 800 | s1 | utility | 0/9600/4800 | OK (info: bought 14400 vs median 8800 in 29 other builds, no action) |
| 12 | 16000 | Duration Extender | 1600 | s2 | utility | 0/11200/4800 | OK |
| 13 | 20800 | Infuser | 4800 | v4 | SP 5.6 HP 16 TR% 1.6 | 0/11200/9600 | FLAG LOW: 20.8k, 4800 paid (Spirit Lifesteal consumed). Ratio 0.5. Kelvin beam ticks fit it (rule: lots of separate spirit hits); health 4.8k @10.4k is already online, so OK. [vs 7 other builds: median 41600, min 16800 victor, max 47200 mcginnis_ult] |
| 14 | 23200 | Rapid Recharge | 2400 | s3 | utility | 0/13600/9600 | OK |
| 15 | 28000 | Escalating Exposure | 4800 | s4 | TR% 2.7 | 0/18400/9600 | OK |
| 16 | 29600 | Superior Cooldown | 1600 | s3 | utility | 0/20000/9600 | OK |
| 17 | 32800 | Bullet Resilience | 3200 | v3 | BR% 9.4 | 0/20000/12800 | OK |
| 18 | 37600 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 0/24800/12800 | OK |
| 19 | 44000 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 0/24800/19200 | OK |
| 20 | 46400 | Greater Expansion | 2400 | s3 | TR% 3.1 | 0/27200/19200 | OK (info: bought 46400 vs median 28800 in 28 other builds, no action) |
| 21 | 48000 | Superior Duration | 1600 | s3 | BR% 2.5 | 0/28800/19200 | OK (info: bought 48000 vs median 26400 in 22 other builds, no action) |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 0, spirit 28800, health 19200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- Spikes: spirit @4.8k, health @10.4k; end health 19.2k.
- Gun invest 0 for the build.
- Gun / spirit / health 4.8k: gun NEVER (end 0), spirit @4800, health @10400.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

# Cost-efficiency audit: bebop_bomb (Rizuhble's Kaboom Bot Bebop)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun never, spirit@6400, health@13600. End of core: 51200 souls, gun 0 / spirit 38400 / health 12800, 12 slots.

Result: MED gun 0 (no gun item at all, 4.8k never); LOW Mystic Expansion @16.8k (cheap Sticky Bomb imbue bought late)
Minimal fix: No clean fix: gun 4.8k needs two slots (T3 3.2k + T2 1.6k); tested Headhunter + Opening Rounds in place of Trophy Collector + Enduring Speed = gun 4.8k @10.4k but 13 slots and health 4.8k slips to 33.6k. Recommend accept gun 0 for this pure-spirit build; Mystic Expansion next to Compress Cooldown is the only change

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | Mystic Burst | 800 | s1 | utility | 0/800/0 | OK: First item, 800. Sticky Bomb = 85+1.5x9.2 = 99 at SP 9.2 (>80) so it procs from the start; feeds Tankbuster @16.0k (Sticky Bomb 85+1.5x99 = 234 > 165). [vs 24 other builds: median 4000, min 800 viscous_damage, max 20000 yamato] |
| 2 | 1600 | Spirit Strike | 800 | s1 | utility | 0/1600/0 | OK (info: bought 1600 vs median 3200 in 12 other builds, no action) |
| 3 | 2400 | Sprint Boots | 800 | v1 | utility | 0/1600/800 | OK (info: bought 2400 vs median 8800 in 39 other builds, no action) |
| 4 | 3200 | Extra Spirit | 800 | s1 | SP 12.5 | 0/2400/800 | OK (info: bought 3200 vs median 1600 in 42 other builds, no action) |
| 5 | 4000 | Trophy Collector | 800 | v2 | utility | 0/2400/1600 | OK: 4.0k, early, passive souls payoff starts at once; named sell exists (Magic Carpet). [vs 13 other builds: median 9600, min 5600 bebop_support, max 19200 rem] |
| 6 | 4800 | Improved Spirit | 800 | s2 | SP 11.3 HP 47 | 0/3200/1600 | OK |
| 7 | 6400 | Compress Cooldown | 1600 | s2 | utility | 0/4800/1600 | OK (info: bought 6400 vs median 14400 in 43 other builds, no action) |
| 8 | 8000 | Enduring Speed | 1600 | v2 | utility | 0/4800/3200 | OK: Slow hero; upgrade Juggernaut in Slot locked. |
| 9 | 10400 | Spirit Snatch | 2400 | s3 | HP 23 | 0/7200/3200 | OK |
| 10 | 13600 | Veil Walker | 3200 | v3 | SP 1.9 HP 39 | 0/7200/6400 | OK |
| 11 | 16000 | Tankbuster | 2400 | s3 | HP 16 | 0/9600/6400 | OK |
| 12 | 16800 | Mystic Expansion | 800 | s1 | utility | 0/10400/6400 | FLAG LOW: 800 at 16.8k, imbue on Sticky Bomb (range/radius), then Greater Expansion @38.4k. Others buy it median 8.8k (ratio 1.9). Bought next to Compress Cooldown it costs nothing in spikes (spirit 4.8k stays @6.4k; health 4.8k 13.6k>14.4k). [vs 29 other builds: median 8800, min 1600 paradox_bomb, max 28000 viscous] |
| 13 | 18400 | Superior Cooldown | 1600 | s3 | utility | 0/12000/6400 | OK |
| 14 | 24800 | Echo Shard | 6400 | s4 | BR% 0.8 TR% 0.8 | 0/18400/6400 | OK |
| 15 | 31200 | Witchmail | 6400 | v4 | SP 2.2 TR% 3.4 | 0/18400/12800 | OK |
| 16 | 36000 | Boundless Spirit | 4800 | s4 | SP 4.7 HP 12 | 0/23200/12800 | OK |
| 17 | 38400 | Greater Expansion | 2400 | s3 | TR% 3.1 | 0/25600/12800 | OK |
| 18 | 44800 | Mystic Reverb | 6400 | s4 | utility | 0/32000/12800 | OK |
| 19 | 51200 | Spirit Burn | 6400 | s4 | utility | 0/38400/12800 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 0, spirit 38400, health 12800. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- No gun item: gun invest 0 for the whole build. Rule "no token investments" means commit or skip, so 0 is consistent; flagged only because Kieran wants 4.8k in every colour on most heroes.
- Mercurial Magnum: game slot is Tech (spirit). walk1 and the spirit invest bonus count it as spirit; only Kieran's own counting treats it as gun.
- Gun / spirit / health 4.8k: gun NEVER (end 0), spirit @6400, health @13600.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).

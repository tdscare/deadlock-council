# mcginnis_ult - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Monster Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Extra Spirit | T1 | s | 800 | 800 | 800 | 0 | 2 |
| 2400 | Extra Stamina | T1 | v | 800 | 800 | 800 | 800 | 3 |
| 3200 | Mystic Expansion | T1 | s | 800 | 800 | 1600 | 800 | 4 |
| 4800 | Compress Cooldown | T2 | s | 1600 | 800 | 3200 | 800 | 5 |
| 6400 | Duration Extender | T2 | s | 1600 | 800 | 4800 | 800 | 6 |
| 7200 | Sprint Boots | T1 | v | 800 | 800 | 4800 | 1600 | 7 |
| 8000 | Enduring Speed (from Sprint Boots) | T2 | v | 800 | 800 | 4800 | 2400 | 7 |
| 10400 | Stamina Mastery (from Extra Stamina) | T3 | v | 2400 | 800 | 4800 | 4800 | 7 |
| 12000 | Mystic Slow | T2 | s | 1600 | 800 | 6400 | 4800 | 8 |
| 12800 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 800 | 7200 | 4800 | 8 |
| 14400 | Mystic Vulnerability | T2 | s | 1600 | 800 | 8800 | 4800 | 9 |
| 16000 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 800 | 10400 | 4800 | 9 |
| 17600 | Debuff Reducer | T2 | v | 1600 | 800 | 10400 | 6400 | 10 |
| 19200 | Spirit Lifesteal | T2 | v | 1600 | 800 | 10400 | 8000 | 11 |
| 24000 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 800 | 15200 | 8000 | 11 |
| 28800 | Unstoppable (from Debuff Reducer) | T4 | v | 4800 | 800 | 15200 | 12800 | 11 |
| 33600 | Lightning Scroll (from Mystic Slow) | T4 | s | 4800 | 0 | 20000 | 12800 | 10 |
| 35200 | Superior Duration (from Duration Extender) | T3 | s | 1600 | 0 | 21600 | 12800 | 10 |
| 37600 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 0 | 24000 | 12800 | 10 |
| 42400 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 0 | 28800 | 12800 | 10 |
| 47200 | Infuser (from Spirit Lifesteal) | T4 | v | 4800 | 0 | 28800 | 17600 | 10 |
| 53600 | Diviner's Kevlar | T4 | v | 6400 | 0 | 28800 | 24000 | 11 |
| 60000 | Refresher | T4 | s | 6400 | 0 | 35200 | 24000 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800
- spirit: 800@1600, 1600@3200, 2400@4800, 3200@4800, 4800@6400, 6400@12000, 8000@14400, 11200@24000, 16000@33600, 22400@37600, 28800@42400
- vitality: 800@2400, 1600@7200, 2400@8000, 3200@10400, 4800@10400, 6400@17600, 8000@19200, 11200@28800, 16000@47200, 22400@53600

## Flags

1. **LOW** Boundless Spirit, Lightning Scroll, Superior Duration, Greater Expansion: Boundless Spirit is bought at 42.4k, behind Lightning Scroll (33.6k, 4,800 for a 150 hit + stun on the ult), Superior Duration (35.2k, 1,600, 0 SP) and Greater Expansion (37.6k, 2,400, 0 SP). Boundless is +30 SP, +15% spirit power, +75 HP for 4,800 net (6.3 SP per 1,000 plus the multiplier). Spirit 28.8k (the 100 SP tier) lands at 42.4k whatever the order, so the order only decides when the +30 SP/+15% starts.
   - Fix: Put Boundless Spirit right after Unstoppable (33.6k, 8.8k souls earlier); Lightning Scroll, Superior Duration, Greater Expansion follow. Re-walked: every spirit/health spike time is unchanged (s6.4k 12.0k, s8k 14.4k, s11.2k 24.0k, s16k 33.6k, v4.8k 10.4k).

## OK / notes

- Spirit 4.8k at 6.4k vs 4.8k minimum: 1,600 off-colour (Monster Rounds 800 = named sell for Lightning Scroll; Extra Stamina 800 = Stamina Mastery component, health 4.8k at 10.4k). Round 21 put Extra Stamina ahead of the imbues so Heavy Barrage is unlocked when they are bought (sp.js: ult T1 at 3.2k). Accepted.
- Counters box sells Mystic Slow, which is unbought at the 'Get after Stamina Mastery' point: spirit 6.4k moves 12.0k to 16.0k with a 3,200 vitality counter and Lightning Scroll then costs 6,400 instead of 4,800. That is the price of the counter, not a dip (spirit stays above 4.8k).

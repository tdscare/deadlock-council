# sinclair_bolt - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Spirit | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Extra Charge | T1 | s | 800 | 0 | 1600 | 0 | 2 |
| 2400 | Mystic Burst | T1 | s | 800 | 0 | 2400 | 0 | 3 |
| 3200 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 0 | 3200 | 0 | 3 |
| 4800 | Duration Extender | T2 | s | 1600 | 0 | 4800 | 0 | 4 |
| 5600 | Sprint Boots | T1 | v | 800 | 0 | 4800 | 800 | 5 |
| 6400 | Trophy Collector (from Sprint Boots) | T2 | v | 800 | 0 | 4800 | 1600 | 5 |
| 9600 | Veil Walker | T3 | v | 3200 | 0 | 4800 | 4800 | 6 |
| 12000 | Rapid Recharge (from Extra Charge) | T3 | s | 2400 | 0 | 7200 | 4800 | 6 |
| 12800 | Mystic Expansion | T1 | s | 800 | 0 | 8000 | 4800 | 7 |
| 14400 | Superior Duration (from Duration Extender) | T3 | s | 1600 | 0 | 9600 | 4800 | 7 |
| 16800 | Tankbuster (from Mystic Burst) | T3 | s | 2400 | 0 | 12000 | 4800 | 7 |
| 18400 | Enchanter's Emblem | T2 | v | 1600 | 0 | 12000 | 6400 | 8 |
| 20800 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 0 | 14400 | 6400 | 8 |
| 22400 | Compress Cooldown | T2 | s | 1600 | 0 | 16000 | 6400 | 9 |
| 28800 | Diviner's Kevlar | T4 | v | 6400 | 0 | 16000 | 12800 | 10 |
| 33600 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 0 | 20800 | 12800 | 10 |
| 40000 | Vortex Web | T4 | s | 6400 | 0 | 27200 | 12800 | 11 |
| 41600 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 0 | 28800 | 12800 | 11 |
| 48000 | Spirit Burn | T4 | s | 6400 | 0 | 35200 | 12800 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: none
- spirit: 800@800, 1600@1600, 2400@2400, 3200@3200, 4800@4800, 6400@12000, 8000@12800, 11200@16800, 16000@22400, 22400@40000, 28800@41600
- vitality: 800@5600, 1600@6400, 2400@9600, 3200@9600, 4800@9600, 6400@18400, 8000@28800, 11200@28800

## Flags

1. **LOW** Diviner's Kevlar, Boundless Spirit: Diviner's Kevlar is the first T4 (28.8k, 6,400 vitality): no passive stats, only 1,000 barrier and +40 SP for 20s when the ult is cast (Audience Participation copies an enemy ult and its cooldown), versus Boundless Spirit's permanent +30 SP/+15% for 4,800 at 33.6k.
   - Fix: Boundless Spirit before Kevlar (28.8k vs 33.6k); health 12.8k tier then lands 33.6k instead of 28.8k. Optional.

## OK / notes

- Spirit 4.8k at exactly 4,800 souls (0 off-colour), health 4.8k at 9.6k (Veil Walker). Mystic Burst at 2.4k: Vexing Bolt max 120 + 1.86 x 30.5 = 177 > 80 (ok). Tankbuster 16.8k ok. Spirit Burn 48.0k last.
- Trophy Collector (T2) is a named sell (Mystic Reverb); Enchanter's Emblem is a named sell (Escalating Exposure, counters).
- Counters sell Enchanter's Emblem (unbought at 'Get after Veil Walker'): only the counter's cost shifts spirit 16k/22.4k tiers; health 4.8k kept.

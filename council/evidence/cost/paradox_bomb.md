# paradox_bomb - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Spirit | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Mystic Expansion | T1 | s | 800 | 0 | 1600 | 0 | 2 |
| 2400 | Extra Stamina | T1 | v | 800 | 0 | 1600 | 800 | 3 |
| 3200 | Arcane Surge (from Extra Stamina) | T2 | s | 800 | 0 | 3200 | 0 | 3 |
| 4800 | Spirit Lifesteal | T2 | v | 1600 | 0 | 3200 | 1600 | 4 |
| 6400 | Duration Extender | T2 | s | 1600 | 0 | 4800 | 1600 | 5 |
| 9600 | Veil Walker | T3 | v | 3200 | 0 | 4800 | 4800 | 6 |
| 10400 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 0 | 5600 | 4800 | 6 |
| 12000 | Mystic Vulnerability | T2 | s | 1600 | 0 | 7200 | 4800 | 7 |
| 13600 | Compress Cooldown | T2 | s | 1600 | 0 | 8800 | 4800 | 8 |
| 15200 | Superior Duration (from Duration Extender) | T3 | s | 1600 | 0 | 10400 | 4800 | 8 |
| 16800 | Slowing Hex | T2 | s | 1600 | 0 | 12000 | 4800 | 9 |
| 20000 | Warp Stone | T3 | v | 3200 | 0 | 12000 | 8000 | 10 |
| 22400 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 0 | 14400 | 8000 | 10 |
| 28800 | Echo Shard | T4 | s | 6400 | 0 | 20800 | 8000 | 11 |
| 30400 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 0 | 22400 | 8000 | 11 |
| 35200 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 0 | 27200 | 8000 | 11 |
| 40000 | Infuser (from Spirit Lifesteal) | T4 | v | 4800 | 0 | 27200 | 12800 | 11 |
| 44800 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 0 | 32000 | 12800 | 11 |
| 49600 | Vortex Web (from Slowing Hex) | T4 | s | 4800 | 0 | 36800 | 12800 | 11 |
| 56000 | Spirit Burn | T4 | s | 6400 | 0 | 43200 | 12800 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: none
- spirit: 800@800, 1600@1600, 2400@3200, 3200@3200, 4800@6400, 6400@12000, 8000@13600, 11200@16800, 16000@28800, 22400@30400, 28800@44800
- vitality: 800@2400, 1600@4800, 2400@9600, 3200@9600, 4800@9600, 6400@20000, 8000@20000, 11200@40000

## Flags

1. **MED** Spirit Lifesteal: Spirit Lifesteal (vitality, 1,600) is the 5th item at 4.8k, between Arcane Surge and Duration Extender, so spirit 4.8k lands at 6.4k instead of 4.8k (1,600 souls late). Other builds buy it at a median 14.4k (31 builds, slot #10). Health 4.8k is reached by Veil Walker at 9.6k either way (Spirit Lifesteal 1,600 + Veil Walker 3,200).
   - Fix: Move Spirit Lifesteal after Duration Extender (or after Veil Walker). Re-walked: spirit 4.8k 6.4k to 4.8k, health 4.8k stays 9.6k, every later spike unchanged.
2. **LOW** Veil Walker: Rich box: Focus Lens sells Veil Walker, taking vitality from 12,800 to 9,600 (loses the 11.2k tier; 4.8k kept).
   - Fix: Optional: sell Warp Stone for Focus Lens instead and let Cheat Death sell Veil Walker; both keep vitality at 9,600+.

## OK / notes

- Arcane Surge (T2) has no upgrade; it is the named sell in the Divine Barrier rich note, so the rule is met.
- Five T4 in a row (Escalating Exposure 35.2k to Spirit Burn 56.0k) all after 30k: allowed. Echo Shard 28.8k is a single early T4.
- Thresholds spot-checked: Spirit Burn 500 in 5s at 56.0k with SP 200 (grenade 35 + 0.3 x SP per pulse); no change.

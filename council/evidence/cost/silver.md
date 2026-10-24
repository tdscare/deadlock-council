# silver - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Restorative Shot | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Close Quarters | T1 | w | 800 | 1600 | 0 | 0 | 2 |
| 2400 | Melee Lifesteal | T1 | v | 800 | 1600 | 0 | 800 | 3 |
| 4000 | Stalker | T2 | w | 1600 | 3200 | 0 | 800 | 4 |
| 7200 | Hunter's Aura | T3 | w | 3200 | 6400 | 0 | 800 | 5 |
| 8000 | Grit | T1 | v | 800 | 6400 | 0 | 1600 | 6 |
| 8800 | Spirit Shielding (from Grit) | T2 | v | 800 | 6400 | 0 | 2400 | 6 |
| 11200 | Lifestrike (from Melee Lifesteal) | T3 | v | 2400 | 6400 | 0 | 4800 | 6 |
| 13600 | Point Blank (from Close Quarters) | T3 | w | 2400 | 8800 | 0 | 4800 | 6 |
| 16800 | Express Shot | T3 | w | 3200 | 12000 | 0 | 4800 | 7 |
| 18400 | Duration Extender | T2 | s | 1600 | 12000 | 1600 | 4800 | 8 |
| 20000 | Slowing Hex | T2 | s | 1600 | 12000 | 3200 | 4800 | 9 |
| 23200 | Berserker | T3 | w | 3200 | 15200 | 3200 | 4800 | 10 |
| 24800 | Debuff Reducer | T2 | v | 1600 | 15200 | 3200 | 6400 | 11 |
| 29600 | Unstoppable (from Debuff Reducer) | T4 | v | 4800 | 15200 | 3200 | 11200 | 11 |
| 31200 | Superior Duration (from Duration Extender) | T3 | s | 1600 | 15200 | 4800 | 11200 | 11 |
| 37600 | Inhibitor | T4 | v | 6400 | 15200 | 4800 | 17600 | 12 |
| 44000 | Frenzy | T4 | w | 6400 | 20800 | 4800 | 17600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@1600, 2400@4000, 3200@4000, 4800@7200, 6400@7200, 8000@13600, 11200@16800, 16000@44000
- spirit: 800@18400, 1600@18400, 2400@20000, 3200@20000, 4800@31200
- vitality: 800@2400, 1600@8000, 2400@8800, 3200@11200, 4800@11200, 6400@24800, 8000@29600, 11200@29600, 16000@37600

## Flags

1. **MED** Phantom Strike, Slowing Hex: Rich box: Phantom Strike sells Slowing Hex. Silver's whole spirit colour is Duration Extender + Superior Duration + Slowing Hex = 4,800 (spirit 4.8k, 38 SP bonus, reached at 31.2k). Selling Slowing Hex drops spirit to 3,200 and the 4.8k tier is gone (38 to 19 SP bonus).
   - Fix: Phantom Strike sells Berserker instead (re-walked: weapon 17,600, spirit 4,800, vitality 24,000, no tier lost). Silencer already sells Stalker and Colossus sells Point Blank.

## OK / notes

- Weapon 4.8k and 6.4k both at 7.2k (Hunter's Aura, 3,200 on top of Stalker); health 4.8k at 11.2k (Lifestrike). 'Lost lane?' reorder (Lifestrike right after Stalker): Lifestrike at 6.4k, Hunter's Aura 9.6k, so gun 4.8k/6.4k 7.2k to 9.6k and vitality 3.2k 11.2k to 6.4k; 4.8k vitality stays 11.2k. A fair lost-lane trade; no spike disappears.
- Counters sell Stalker (w2): spirit 4.8k 31.2k to 34.4k only because the counter costs 3,200; no dip.
- Restorative Shot (800, sold for Frenzy at 44.0k, last core buy): allowed by the 'sell-later, bought first' rule.

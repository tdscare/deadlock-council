# vyper - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Spirit | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 0 | 1600 | 0 | 1 |
| 3200 | Quicksilver Reload | T2 | s | 1600 | 0 | 3200 | 0 | 2 |
| 4800 | Cold Front | T2 | s | 1600 | 0 | 4800 | 0 | 3 |
| 6400 | Opening Rounds | T2 | w | 1600 | 1600 | 4800 | 0 | 4 |
| 7200 | Close Quarters | T1 | w | 800 | 2400 | 4800 | 0 | 5 |
| 8000 | Rapid Rounds | T1 | w | 800 | 3200 | 4800 | 0 | 6 |
| 9600 | Bullet Lifesteal | T2 | v | 1600 | 3200 | 4800 | 1600 | 7 |
| 10400 | Sprint Boots | T1 | v | 800 | 3200 | 4800 | 2400 | 8 |
| 11200 | Enduring Speed (from Sprint Boots) | T2 | v | 800 | 3200 | 4800 | 3200 | 8 |
| 12800 | Spirit Lifesteal | T2 | v | 1600 | 3200 | 4800 | 4800 | 9 |
| 15200 | Burst Fire (from Rapid Rounds) | T3 | w | 2400 | 5600 | 4800 | 4800 | 9 |
| 17600 | Point Blank (from Close Quarters) | T3 | w | 2400 | 8000 | 4800 | 4800 | 9 |
| 22400 | Mercurial Magnum (from Quicksilver Reload) | T4 | s | 4800 | 8000 | 9600 | 4800 | 9 |
| 25600 | Leech (from Bullet Lifesteal+Spirit Lifesteal) | T4 | v | 3200 | 8000 | 9600 | 8000 | 8 |
| 32000 | Spiritual Overflow | T4 | w | 6400 | 14400 | 9600 | 8000 | 9 |
| 38400 | Frenzy | T4 | w | 6400 | 20800 | 9600 | 8000 | 10 |
| 44800 | Ricochet | T4 | w | 6400 | 27200 | 9600 | 8000 | 11 |
| 51200 | Unstoppable | T4 | v | 6400 | 27200 | 9600 | 14400 | 12 |
| 56000 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 27200 | 14400 | 14400 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@6400, 1600@6400, 2400@7200, 3200@8000, 4800@15200, 6400@17600, 8000@17600, 11200@32000, 16000@38400, 22400@44800
- spirit: 800@800, 1600@1600, 2400@3200, 3200@3200, 4800@4800, 6400@22400, 8000@22400, 11200@56000
- vitality: 800@9600, 1600@9600, 2400@10400, 3200@11200, 4800@12800, 6400@25600, 8000@25600, 11200@51200

## Flags

1. **MED** Boundless Spirit: Spirit Vyper buys Boundless Spirit last (56.0k, the latest of any build except victor), after Spiritual Overflow, Frenzy, Ricochet and Unstoppable. Spirit invest sits at 9,600 from 22.4k to 56.0k, so the 11.2k spirit tier (59 vs 52 SP) and Boundless's +30 SP/+15% arrive 27k souls late on the build whose style is 'more spirit invest'.
   - Fix: Move Boundless Spirit (Improved Spirit is owned, 4,800 net) to right after Leech (30.4k). Re-walked: spirit 11.2k 56.0k to 30.4k, gun 11.2k 32.0k to 36.8k, gun 16k 38.4k to 43.2k, no 4.8k moves.
2. **MED** Cold Front: Counters box sells Cold Front for every counter. Spirit is exactly 4,800 (Extra Spirit -> Improved Spirit 1,600 + Quicksilver Reload 1,600 + Cold Front 1,600) at 4.8k, so selling it drops spirit to 3,200 and the 4.8k tier is gone from 16.0k to 25.6k (until Mercurial Magnum); it also conflicts with the Arctic Blast upgrade in the rich box.
   - Fix: Counters sell Bullet Lifesteal (vitality for vitality; re-walked: no tier lost, Leech then costs 4,800 instead of 3,200). Gun 4.8k only shifts by the counter's cost.
3. **LOW** Mercurial Magnum, Leech, Spiritual Overflow, Frenzy, Ricochet, Unstoppable: Seven T4 in a row from 22.4k to 56.0k (Mercurial Magnum, Leech, Spiritual Overflow, Frenzy, Ricochet, Unstoppable, Boundless); only two come before 30k, but slot count is 9 at 22.4k and 8 after Leech, so slots stay empty for 30k+ souls.
   - Fix: No change required if Boundless moves up; if empty slots matter, a 3,200 vitality item (Fortitude-class) fits at ~26k.

## OK / notes

- Spirit 4.8k at 4.8k with 0 off-colour souls (best possible). Weapon 4.8k at 15.2k (Burst Fire) after 9,600 off-colour; health 4.8k at 12.8k.
- Opening Rounds (T2) is a named sell (Silencer); Cold Front/Arctic Blast and Enduring Speed/Juggernaut are the other T2s with named upgrades.

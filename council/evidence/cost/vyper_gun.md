# vyper_gun - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Close Quarters | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Rapid Rounds | T1 | w | 800 | 1600 | 0 | 0 | 2 |
| 2400 | Grit | T1 | v | 800 | 1600 | 0 | 800 | 3 |
| 4000 | Intensifying Magazine | T2 | w | 1600 | 3200 | 0 | 800 | 4 |
| 6400 | Burst Fire (from Rapid Rounds) | T3 | w | 2400 | 5600 | 0 | 800 | 4 |
| 7200 | Spirit Shielding (from Grit) | T2 | v | 800 | 5600 | 0 | 1600 | 4 |
| 8800 | Bullet Lifesteal | T2 | v | 1600 | 5600 | 0 | 3200 | 5 |
| 9600 | Extra Stamina | T1 | v | 800 | 5600 | 0 | 4000 | 6 |
| 12000 | Stamina Mastery (from Extra Stamina) | T3 | v | 2400 | 5600 | 0 | 6400 | 6 |
| 13600 | Split Shot | T2 | w | 1600 | 7200 | 0 | 6400 | 7 |
| 16000 | Point Blank (from Close Quarters) | T3 | w | 2400 | 9600 | 0 | 6400 | 7 |
| 17600 | Quicksilver Reload | T2 | s | 1600 | 9600 | 1600 | 6400 | 8 |
| 24000 | Ricochet | T4 | w | 6400 | 16000 | 1600 | 6400 | 9 |
| 28800 | Mercurial Magnum (from Quicksilver Reload) | T4 | s | 4800 | 16000 | 6400 | 6400 | 9 |
| 33600 | Vampiric Burst (from Bullet Lifesteal) | T4 | v | 4800 | 16000 | 6400 | 11200 | 9 |
| 40000 | Silencer | T4 | w | 6400 | 22400 | 6400 | 11200 | 10 |
| 46400 | Lucky Shot | T4 | w | 6400 | 28800 | 6400 | 11200 | 11 |
| 52800 | Unstoppable | T4 | v | 6400 | 28800 | 6400 | 17600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@1600, 2400@4000, 3200@4000, 4800@6400, 6400@13600, 8000@16000, 11200@24000, 16000@24000, 22400@40000, 28800@46400
- spirit: 800@17600, 1600@17600, 2400@28800, 3200@28800, 4800@28800, 6400@28800
- vitality: 800@2400, 1600@7200, 2400@8800, 3200@8800, 4800@12000, 6400@12000, 8000@33600, 11200@33600, 16000@52800

## Flags

1. **MED** Split Shot: Counters box sells Split Shot, unbought at 'Get after Stamina Mastery', for every counter. That removes 1,600 of weapon invest permanently: weapon 16k tier moves 24.0k to 41.6k, 22.4k tier 40.0k to 48.0k and the 28.8k tier (reached by Lucky Shot at 46.4k) is never reached; it also deletes the Split Shot + Ricochet pairing the build is named for.
   - Fix: Counters sell Spirit Shielding (vitality for vitality; re-walked: no tier lost, only the counter's cost shifts spirit 28.8k to 32.0k). Rich Spellbreaker still sells Spirit Shielding, so give Spellbreaker Bullet Lifesteal.
2. **LOW** Ricochet, Mercurial Magnum, Vampiric Burst, Silencer, Lucky Shot, Unstoppable: Six T4 in a row from 24.0k to 52.8k (Ricochet 6,400 at 24.0k, then 4,800, 4,800, 6,400, 6,400, 6,400) with slots at 9 until Silencer. Two before 30k and four after is borderline against 'late 4-5 in a row is fine'.
   - Fix: Optional: put a 3,200 item (Fortitude / Veil Walker class) between Mercurial Magnum and Vampiric Burst.

## OK / notes

- Weapon 4.8k and 6.4k both at 6.4k (800 off-colour: Grit). Health 4.8k at 12.0k. Spirit 4.8k only at 28.8k via Mercurial Magnum, counted as a gun item by rule.
- Quicksilver Reload (T2, 17.6k) is a fresh T2 late but it is the Mercurial Magnum component 6k later; allowed.

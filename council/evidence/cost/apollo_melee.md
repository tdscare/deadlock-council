# apollo_melee - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Melee Lifesteal | T1 | v | 800 | 0 | 0 | 800 | 1 |
| 2400 | Melee Charge | T2 | w | 1600 | 1600 | 0 | 800 | 2 |
| 3200 | Extra Regen | T1 | v | 800 | 1600 | 0 | 1600 | 3 |
| 4000 | Healing Booster (from Extra Regen) | T2 | v | 800 | 1600 | 0 | 2400 | 3 |
| 7200 | Hunter's Aura | T3 | w | 3200 | 4800 | 0 | 2400 | 4 |
| 9600 | Lifestrike (from Melee Lifesteal) | T3 | v | 2400 | 4800 | 0 | 4800 | 4 |
| 10400 | Close Quarters | T1 | w | 800 | 5600 | 0 | 4800 | 5 |
| 11200 | Grit | T1 | v | 800 | 5600 | 0 | 5600 | 6 |
| 12000 | Reactive Barrier (from Grit) | T2 | v | 800 | 5600 | 0 | 6400 | 6 |
| 13600 | Stalker | T2 | w | 1600 | 7200 | 0 | 6400 | 7 |
| 16000 | Point Blank (from Close Quarters) | T3 | w | 2400 | 9600 | 0 | 6400 | 7 |
| 19200 | Berserker | T3 | w | 3200 | 12800 | 0 | 6400 | 8 |
| 24000 | Crushing Fists (from Melee Charge) | T4 | w | 4800 | 17600 | 0 | 6400 | 8 |
| 27200 | Spirit Resilience | T3 | v | 3200 | 17600 | 0 | 9600 | 9 |
| 33600 | Witchmail | T4 | v | 6400 | 17600 | 0 | 16000 | 10 |
| 40000 | Phantom Strike | T4 | v | 6400 | 17600 | 0 | 22400 | 11 |
| 44800 | Indomitable (from Reactive Barrier) | T4 | v | 4800 | 17600 | 0 | 27200 | 11 |
| 51200 | Unstoppable | T4 | v | 6400 | 17600 | 0 | 33600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@2400, 1600@2400, 2400@7200, 3200@7200, 4800@7200, 6400@13600, 8000@16000, 11200@19200, 16000@24000
- spirit: none
- vitality: 800@800, 1600@3200, 2400@4000, 3200@9600, 4800@9600, 6400@12000, 8000@27200, 11200@33600, 16000@33600, 22400@40000, 28800@51200

## Flags

1. **LOW** Healing Booster: Healing Booster (Extra Regen upgrade, 800 net) is bought before Hunter's Aura, so the weapon 4.8k tier (Melee Charge 1,600 + Hunter's Aura 3,200) lands at 7.2k instead of 6.4k. It is not a lane fix (Extra Regen already covers the lane).
   - Fix: Move Healing Booster after Lifestrike. Re-walked: gun 4.8k 7.2k to 6.4k, health 4.8k stays 9.6k, nothing else moves.

## OK / notes

- Melee Charge is the 2nd item (2.4k) but its payoff is satisfied: the note needs Riposte's longer stun (T2) and sp.js shows Riposte T2 at 2.4k (tiers [0,2,0,-1]). Crushing Fists is not early: 24.0k, 4,800 net on top of the owned Melee Charge (billy 26.4k, sinclair 36.8k, abrams_melee 14.4k).
- Hunter's Aura at 7.2k is the cheapest route to weapon 4.8k and 6.4k is next at 13.6k (Stalker).
- Counters sell Stalker (unbought when 'Get after Lifestrike' is reached): gun 6.4k 13.6k to 17.6k for a 3,200 counter; no dip.

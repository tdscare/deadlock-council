# celeste_carry - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | High-Velocity Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Extra Regen | T1 | v | 800 | 800 | 0 | 800 | 2 |
| 2400 | Opening Rounds (from High-Velocity Rounds) | T2 | w | 800 | 1600 | 0 | 800 | 2 |
| 4000 | Kinetic Dash | T2 | w | 1600 | 3200 | 0 | 800 | 3 |
| 5600 | Swift Striker | T2 | w | 1600 | 4800 | 0 | 800 | 4 |
| 6400 | Extra Health | T1 | v | 800 | 4800 | 0 | 1600 | 5 |
| 8000 | Quicksilver Reload | T2 | s | 1600 | 4800 | 1600 | 1600 | 6 |
| 8800 | Mystic Regeneration | T1 | s | 800 | 4800 | 2400 | 1600 | 7 |
| 11200 | Radiant Regeneration (from Mystic Regeneration) | T3 | s | 2400 | 4800 | 4800 | 1600 | 7 |
| 12000 | Healing Booster (from Extra Regen) | T2 | v | 800 | 4800 | 4800 | 2400 | 7 |
| 14400 | Fortitude (from Extra Health) | T3 | v | 2400 | 4800 | 4800 | 4800 | 7 |
| 19200 | Mercurial Magnum (from Quicksilver Reload) | T4 | s | 4800 | 4800 | 9600 | 4800 | 7 |
| 20000 | Extra Charge | T1 | s | 800 | 4800 | 10400 | 4800 | 8 |
| 22400 | Rapid Recharge (from Extra Charge) | T3 | s | 2400 | 4800 | 12800 | 4800 | 8 |
| 24000 | Spirit Lifesteal | T2 | v | 1600 | 4800 | 12800 | 6400 | 9 |
| 28800 | Spiritual Overflow (from Spirit Lifesteal) | T4 | w | 4800 | 11200 | 12800 | 4800 | 9 |
| 32000 | Spirit Rend | T3 | w | 3200 | 14400 | 12800 | 4800 | 10 |
| 38400 | Unstoppable | T4 | v | 6400 | 14400 | 12800 | 11200 | 11 |
| 41600 | Toxic Bullets | T3 | w | 3200 | 17600 | 12800 | 11200 | 12 |
| 48000 | Witchmail | T4 | v | 6400 | 16000 | 12800 | 17600 | 12 |
| 54400 | Spellslinger | T4 | w | 6400 | 20800 | 12800 | 17600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@2400, 2400@4000, 3200@4000, 4800@5600, 6400@28800, 8000@28800, 11200@28800, 16000@41600
- spirit: 800@8000, 1600@8000, 2400@8800, 3200@11200, 4800@11200, 6400@19200, 8000@19200, 11200@22400
- vitality: 800@1600, 1600@6400, 2400@12000, 3200@14400, 4800@14400, 6400@24000, 8000@38400, 11200@38400, 16000@48000

## Flags

1. **HIGH** Kinetic Dash: Counters box sells Kinetic Dash for every counter. This is the gun-carry build and its weapon 4.8k tier is exactly 4,800 (High-Velocity 800 + Opening Rounds 800 + Kinetic Dash 1,600 + Swift Striker 1,600, reached at 5.6k). Taking out any of those drops weapon invest to 3,200 (46% to 18% weapon damage) until Spiritual Overflow: re-walked, weapon 4.8k lost from 17.6k to 32.0k (Metal Skin, Bullet/Spirit Resilience, Dispel, Counterspell) and 20.8k to 35.2k (Plated Armor, Ethereal Shift).
   - Fix: The counters sell Healing Booster (vitality, same colour as the counters; re-walked clean: no tier lost). Healing Tempo in Slot locked then costs 6,400 instead of 4,800, or swap that line for Juggernaut/Transcendent if wanted. Kinetic Dash stays.
2. **LOW** Spiritual Overflow: Spiritual Overflow upgrades Spirit Lifesteal (vitality) into a weapon item: vitality 6.4k tier lost at 28.8k, regained at 38.4k (Unstoppable). Health 4.8k is untouched.
   - Fix: None needed; Unstoppable is already in the right place.

## OK / notes

- Weapon 4.8k at 5.6k with 800 off-colour; health 4.8k at 14.4k (Fortitude) after 9,600 off-colour: gun carry takes the damage spike first, matches the priority rule.
- Extra Charge 20.0k -> Rapid Recharge 22.4k are for Radiant Daggers (AbilityCharges 1): kit-valid, T1 bought late as a component.

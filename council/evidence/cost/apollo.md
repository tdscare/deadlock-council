# apollo - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Spirit | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Mystic Burst | T1 | s | 800 | 0 | 1600 | 0 | 2 |
| 2400 | Mystic Expansion | T1 | s | 800 | 0 | 2400 | 0 | 3 |
| 4000 | Compress Cooldown | T2 | s | 1600 | 0 | 4000 | 0 | 4 |
| 4800 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 0 | 4800 | 0 | 4 |
| 6400 | Spirit Lifesteal | T2 | v | 1600 | 0 | 4800 | 1600 | 5 |
| 7200 | Extra Regen | T1 | v | 800 | 0 | 4800 | 2400 | 6 |
| 8000 | Healing Booster (from Extra Regen) | T2 | v | 800 | 0 | 4800 | 3200 | 6 |
| 9600 | Enchanter's Emblem | T2 | v | 1600 | 0 | 4800 | 4800 | 7 |
| 12000 | Tankbuster (from Mystic Burst) | T3 | s | 2400 | 0 | 7200 | 4800 | 7 |
| 13600 | Mystic Vulnerability | T2 | s | 1600 | 0 | 8800 | 4800 | 8 |
| 16000 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 0 | 11200 | 4800 | 8 |
| 16800 | Extra Stamina | T1 | v | 800 | 0 | 11200 | 5600 | 9 |
| 19200 | Stamina Mastery (from Extra Stamina) | T3 | v | 2400 | 0 | 11200 | 8000 | 9 |
| 22400 | Torment Pulse | T3 | s | 3200 | 0 | 14400 | 8000 | 10 |
| 24000 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 0 | 16000 | 8000 | 10 |
| 28800 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 0 | 20800 | 8000 | 10 |
| 33600 | Leech (from Spirit Lifesteal) | T4 | v | 4800 | 0 | 20800 | 12800 | 10 |
| 40000 | Spirit Burn | T4 | s | 6400 | 0 | 27200 | 12800 | 11 |
| 46400 | Mystic Reverb | T4 | s | 6400 | 0 | 33600 | 12800 | 12 |
| 51200 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 0 | 38400 | 12800 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: none
- spirit: 800@800, 1600@1600, 2400@2400, 3200@4000, 4800@4800, 6400@12000, 8000@13600, 11200@16000, 16000@24000, 22400@40000, 28800@46400
- vitality: 800@6400, 1600@6400, 2400@7200, 3200@8000, 4800@9600, 6400@19200, 8000@19200, 11200@33600

## Flags

1. **LOW** Stamina Mastery: Rich box: Ethereal Shift sells Stamina Mastery: vitality 12,800 to 9,600 (loses the 11.2k tier; 4.8k kept).
   - Fix: Optional: sell Torment Pulse (spirit) for Ethereal Shift, as the Echo Shard line already does; Echo Shard then sells Tankbuster.

## OK / notes

- Spirit 4.8k at exactly 4,800 souls, 0 off-colour souls: cheapest possible. Health 4.8k at 9.6k (Enchanter's Emblem).
- Mystic Burst second item (1.6k): Disengaging Sigil 85 + 1.3 x 25.4 SP = 118 > 80 at tier 0. Tankbuster 12.0k: Flawless Advance perfect hit 65+65 (T3) + 1.55 x 104 SP = 291 > 165.
- Extra Regen 7.2k -> Healing Booster 8.0k (net 800) and Spirit Lifesteal 6.4k are the only greens before the health spike and they are what reaches 4.8k vitality at 9.6k; Healing Tempo is the named Slot-locked upgrade. Five T4 in a row from 28.8k: allowed.

# lash - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Mystic Burst | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Headshot Booster | T1 | w | 800 | 800 | 800 | 0 | 2 |
| 2400 | Extra Spirit | T1 | s | 800 | 800 | 1600 | 0 | 3 |
| 3200 | Extra Charge | T1 | s | 800 | 800 | 2400 | 0 | 4 |
| 4000 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 800 | 3200 | 0 | 4 |
| 5600 | Cold Front | T2 | s | 1600 | 800 | 4800 | 0 | 5 |
| 7200 | Mystic Shot | T2 | w | 1600 | 2400 | 4800 | 0 | 6 |
| 8000 | Extra Stamina | T1 | v | 800 | 2400 | 4800 | 800 | 7 |
| 9600 | Enchanter's Emblem | T2 | v | 1600 | 2400 | 4800 | 2400 | 8 |
| 12000 | Stamina Mastery (from Extra Stamina) | T3 | v | 2400 | 2400 | 4800 | 4800 | 8 |
| 14400 | Tankbuster (from Mystic Burst) | T3 | s | 2400 | 2400 | 7200 | 4800 | 8 |
| 16800 | Headhunter (from Headshot Booster) | T3 | w | 2400 | 4800 | 7200 | 4800 | 8 |
| 17600 | Mystic Expansion | T1 | s | 800 | 4800 | 8000 | 4800 | 9 |
| 19200 | Compress Cooldown | T2 | s | 1600 | 4800 | 9600 | 4800 | 10 |
| 22400 | Warp Stone | T3 | v | 3200 | 4800 | 9600 | 8000 | 11 |
| 27200 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 4800 | 14400 | 8000 | 11 |
| 29600 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 4800 | 16800 | 8000 | 11 |
| 31200 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 4800 | 18400 | 8000 | 11 |
| 37600 | Spirit Burn | T4 | s | 6400 | 4800 | 24800 | 8000 | 12 |
| 44000 | Mystic Reverb | T4 | s | 6400 | 4800 | 30400 | 8000 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@1600, 1600@7200, 2400@7200, 3200@16800, 4800@16800
- spirit: 800@800, 1600@2400, 2400@3200, 3200@4000, 4800@5600, 6400@14400, 8000@17600, 11200@27200, 16000@29600, 22400@37600, 28800@44000
- vitality: 800@8000, 1600@9600, 2400@9600, 3200@12000, 4800@12000, 6400@22400, 8000@22400

## Flags

1. **MED** Mystic Burst: Mystic Burst is the very first item (800). At 800 souls SP is 9.2: Ground Strike is 60 + 0.79 x 9.2 = 67 and Flog 65 + 0.85 x 9.2 = 73, both under the 80 threshold (Grapple, the way to add the 5.5 per metre height bonus, only unlocks at 1.6k). At 1.6k SP 11.4 it is still 69/75. It first works at 2.4k (SP 26.5: 81 and 87.5).
   - Fix: Buy it after Extra Spirit (3rd item). Zero cost; re-walked, every spike time is identical (spirit 4.8k 5.6k, gun 4.8k 16.8k, health 4.8k 12.0k).
2. **MED** Cheat Death, Mystic Shot, Lightning Scroll, Headhunter: Rich box sells break the weapon 4.8k tier (Mystic Shot 1,600 + Headhunter 3,200 = exactly 4,800 at 16.8k): Cheat Death sells Mystic Shot (gun 4,800 to 3,200) and Lightning Scroll sells Headhunter (gun 4,800 to 1,600).
   - Fix: Cheat Death sells Warp Stone (vitality for vitality, clean; the Majestic Leap swap box covers the same slot). Lightning Scroll sells Greater Expansion (spirit, clean).
3. **LOW** Enchanter's Emblem: Counters: Ethereal Shift (spirit) sells Enchanter's Emblem (vitality): vitality 8,000 to 6,400 and the 4.8k tier lost from 20.8k to 28.8k; Witchmail (rich) sells the same Emblem.
   - Fix: Ethereal Shift sells Cold Front (spirit for spirit).

## OK / notes

- Swap box 'Swap for Warp Stone': Majestic Leap is vitality T3 3,200, same as Warp Stone: re-walked identical (s4.8k 5.6k, w4.8k 16.8k, v4.8k 12.0k, v8k 22.4k).
- Mystic Shot (7.2k) comes right after the spirit 4.8k spike (5.6k) as the rule requires. Headshot Booster (800) is held 15k souls for Headhunter (16.8k), named upgrade.
- Counters sell Enchanter's Emblem: gun 4.8k shifts 16.8k to 20.0k (counter cost), nothing dips.

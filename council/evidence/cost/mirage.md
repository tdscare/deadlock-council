# mirage - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Spirit | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 2400 | Compress Cooldown | T2 | s | 1600 | 0 | 2400 | 0 | 2 |
| 4000 | Mystic Vulnerability | T2 | s | 1600 | 0 | 4000 | 0 | 3 |
| 4800 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 0 | 4800 | 0 | 3 |
| 6400 | Spirit Shredder | T2 | w | 1600 | 1600 | 4800 | 0 | 4 |
| 8000 | Healbane | T2 | v | 1600 | 1600 | 4800 | 1600 | 5 |
| 11200 | Dispel Magic | T3 | v | 3200 | 1600 | 4800 | 4800 | 6 |
| 14400 | Toxic Bullets | T3 | w | 3200 | 4800 | 4800 | 4800 | 7 |
| 15200 | Headshot Booster | T1 | w | 800 | 5600 | 4800 | 4800 | 8 |
| 17600 | Headhunter (from Headshot Booster) | T3 | w | 2400 | 8000 | 4800 | 4800 | 8 |
| 18400 | Extended Magazine | T1 | w | 800 | 8800 | 4800 | 4800 | 9 |
| 24800 | Ricochet | T4 | w | 6400 | 15200 | 4800 | 4800 | 10 |
| 25600 | Titanic Magazine (from Extended Magazine) | T2 | w | 800 | 16000 | 4800 | 4800 | 10 |
| 27200 | Spirit Rend (from Spirit Shredder) | T3 | w | 1600 | 17600 | 4800 | 4800 | 10 |
| 33600 | Inhibitor | T4 | v | 6400 | 17600 | 4800 | 11200 | 11 |
| 38400 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 17600 | 9600 | 11200 | 11 |
| 40000 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 17600 | 11200 | 11200 | 11 |
| 44800 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 17600 | 16000 | 11200 | 11 |
| 51200 | Leech | T4 | v | 6400 | 17600 | 16000 | 17600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@6400, 1600@6400, 2400@14400, 3200@14400, 4800@14400, 6400@17600, 8000@17600, 11200@24800, 16000@25600
- spirit: 800@800, 1600@2400, 2400@2400, 3200@4000, 4800@4800, 6400@38400, 8000@38400, 11200@40000, 16000@44800
- vitality: 800@8000, 1600@8000, 2400@11200, 3200@11200, 4800@11200, 6400@33600, 8000@33600, 11200@33600, 16000@51200

## Flags

1. **LOW** Mystic Reverb, Toxic Bullets, Siphon Bullets, Headhunter, Cheat Death, Spirit Rend: Three rich sells take gun invest from 17,600 to 14,400 (loses the 16k tier): Mystic Reverb sells Toxic Bullets, Siphon Bullets sells Headhunter, Cheat Death sells Spirit Rend. Mirage is a gun hybrid with 4.8k at 14.4k, so no 4.8k is lost, only the 16k step.
   - Fix: Where a spirit/vitality item is free to sell (Healbane and Dispel Magic are already used), keep one gun sell at most; otherwise accept.

## OK / notes

- Spirit 4.8k at exactly 4,800 (Extra Spirit, Compress Cooldown, Mystic Vulnerability, Improved Spirit): cheapest possible. Gun 4.8k at 14.4k (Toxic Bullets), health 4.8k at 11.2k (Healbane + Dispel Magic).
- 'Lost lane?' reorder (Ricochet right after Toxic Bullets, 20.8k instead of 24.8k): re-walked, gun 6.4k/8k/11.2k move 17.6k/17.6k/24.8k to 20.8k/20.8k/20.8k, Headshot Booster/Headhunter 4,000 later; no spike lost. Ricochet 6,400 at ~20 min respects the 'no 6.4k before ~20 min' rule.
- Counters sell Titanic Magazine (unbought at 'Get after Healbane'): gun 16k tier 25.6k to 29.6k-32.8k; no dip.

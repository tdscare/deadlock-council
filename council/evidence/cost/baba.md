# baba - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Extra Charge | T1 | s | 800 | 0 | 800 | 0 | 1 |
| 1600 | Mystic Regeneration | T1 | s | 800 | 0 | 1600 | 0 | 2 |
| 2400 | Rapid Rounds | T1 | w | 800 | 800 | 1600 | 0 | 3 |
| 3200 | Spirit Strike | T1 | s | 800 | 800 | 2400 | 0 | 4 |
| 5600 | Radiant Regeneration (from Mystic Regeneration) | T3 | s | 2400 | 800 | 4800 | 0 | 4 |
| 6400 | Grit | T1 | v | 800 | 800 | 4800 | 800 | 5 |
| 7200 | Reactive Barrier (from Grit) | T2 | v | 800 | 800 | 4800 | 1600 | 5 |
| 8800 | Titanic Magazine | T2 | w | 1600 | 2400 | 4800 | 1600 | 6 |
| 12000 | Fortitude | T3 | v | 3200 | 2400 | 4800 | 4800 | 7 |
| 14400 | Burst Fire (from Rapid Rounds) | T3 | w | 2400 | 4800 | 4800 | 4800 | 7 |
| 16000 | Spirit Lifesteal | T2 | v | 1600 | 4800 | 4800 | 6400 | 8 |
| 18400 | Rapid Recharge (from Extra Charge) | T3 | s | 2400 | 4800 | 7200 | 6400 | 8 |
| 19200 | Extra Spirit | T1 | s | 800 | 4800 | 8000 | 6400 | 9 |
| 21600 | Spirit Snatch (from Spirit Strike) | T3 | s | 2400 | 4800 | 10400 | 6400 | 9 |
| 23200 | Compress Cooldown | T2 | s | 1600 | 4800 | 12000 | 6400 | 10 |
| 24800 | Mystic Vulnerability | T2 | s | 1600 | 4800 | 13600 | 6400 | 11 |
| 29600 | Spiritual Overflow (from Spirit Lifesteal) | T4 | w | 4800 | 11200 | 13600 | 4800 | 11 |
| 31200 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 11200 | 15200 | 4800 | 11 |
| 32000 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 11200 | 16000 | 4800 | 11 |
| 36800 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 11200 | 20800 | 4800 | 11 |
| 41600 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 11200 | 25600 | 4800 | 11 |
| 48000 | Ricochet | T4 | w | 6400 | 17600 | 25600 | 4800 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@2400, 1600@8800, 2400@8800, 3200@14400, 4800@14400, 6400@29600, 8000@29600, 11200@29600, 16000@48000
- spirit: 800@800, 1600@1600, 2400@3200, 3200@5600, 4800@5600, 6400@18400, 8000@19200, 11200@23200, 16000@32000, 22400@41600
- vitality: 800@6400, 1600@7200, 2400@12000, 3200@12000, 4800@12000, 6400@16000

## Flags

1. **MED** Healbane, Fortitude: Counters box sells Fortitude. Healbane (T2, 1,600) replacing Fortitude (T3, 3,200) leaves vitality at 3,200, so health 4.8k is lost (16.0k-17.6k) and lost again at 31.2k when Spiritual Overflow consumes Spirit Lifesteal. Baba's vitality is exactly 4,800 for the whole game, so any cheaper counter breaks it. (Metal Skin, Counterspell, Dispel, Plated Armor, Unstoppable are all >= 3,200 and keep it.)
   - Fix: Healbane sells Reactive Barrier (T2 for T2; re-walked clean). Indomitable (rich) is the Reactive Barrier upgrade, so list Healbane as 'sell Reactive Barrier, or Fortitude if it has already been upgraded'; simplest is to move Healbane out of Counters into a vs-healer note.
2. **LOW** Spiritual Overflow: Spiritual Overflow (29.6k) takes 1,600 out of vitality, so the 6.4k vitality tier is lost for good (vitality 4,800 at end).
   - Fix: None; accepted trade for a gun-hybrid.
3. **LOW** Spirit Rend: Rule G (outside cost): Spirit Rend is T3 in the 'I'm rich as fuck' box (T4 only) and is not an upgrade of anything in the build.
   - Fix: Replace with a T4 or drop.

## OK / notes

- Spirit 4.8k at 5.6k (800 off-colour), health 4.8k at 12.0k (Fortitude), gun 4.8k at 14.4k (Burst Fire): damage spike, health spike, then gun: matches the priority rule.
- Titanic Magazine (T2, 8.8k) is a named sell (Leech); Reactive Barrier is upgraded by Indomitable in rich.

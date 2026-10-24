# warden - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | High-Velocity Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Rapid Rounds | T1 | w | 800 | 1600 | 0 | 0 | 2 |
| 2400 | Extended Magazine | T1 | w | 800 | 2400 | 0 | 0 | 3 |
| 3200 | Opening Rounds (from High-Velocity Rounds) | T2 | w | 800 | 3200 | 0 | 0 | 3 |
| 4000 | Titanic Magazine (from Extended Magazine) | T2 | w | 800 | 4000 | 0 | 0 | 3 |
| 4800 | Swift Striker (from Rapid Rounds) | T2 | w | 800 | 4800 | 0 | 0 | 3 |
| 6400 | Quicksilver Reload | T2 | s | 1600 | 4800 | 1600 | 0 | 4 |
| 8000 | Battle Vest | T2 | v | 1600 | 4800 | 1600 | 1600 | 5 |
| 8800 | Sprint Boots | T1 | v | 800 | 4800 | 1600 | 2400 | 6 |
| 10400 | Bullet Lifesteal | T2 | v | 1600 | 4800 | 1600 | 4000 | 7 |
| 11200 | Enduring Speed (from Sprint Boots) | T2 | v | 800 | 4800 | 1600 | 4800 | 7 |
| 12800 | Fleetfoot | T2 | w | 1600 | 6400 | 1600 | 4800 | 8 |
| 14400 | Spirit Lifesteal | T2 | v | 1600 | 6400 | 1600 | 6400 | 9 |
| 16000 | Bullet Resist Shredder | T2 | s | 1600 | 6400 | 3200 | 6400 | 10 |
| 20800 | Mercurial Magnum (from Quicksilver Reload) | T4 | s | 4800 | 6400 | 8000 | 6400 | 10 |
| 24000 | Spirit Resilience | T3 | v | 3200 | 6400 | 8000 | 9600 | 11 |
| 28800 | Vampiric Burst (from Bullet Lifesteal) | T4 | v | 4800 | 6400 | 8000 | 14400 | 11 |
| 33600 | Spiritual Overflow (from Spirit Lifesteal) | T4 | w | 4800 | 12800 | 8000 | 12800 | 11 |
| 40000 | Siphon Bullets | T4 | v | 6400 | 12800 | 8000 | 19200 | 12 |
| 46400 | Spellslinger | T4 | w | 6400 | 19200 | 8000 | 17600 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@1600, 2400@2400, 3200@3200, 4800@4800, 6400@12800, 8000@33600, 11200@33600, 16000@46400
- spirit: 800@6400, 1600@6400, 2400@16000, 3200@16000, 4800@20800, 6400@20800, 8000@20800
- vitality: 800@8000, 1600@8000, 2400@8800, 3200@10400, 4800@11200, 6400@14400, 8000@24000, 11200@28800, 16000@40000

## Flags

1. **LOW** Fleetfoot: Counters box sells Fleetfoot, which is unbought at the 'Get after Enduring Speed' point and is the only purchase that takes weapon invest from 4,800 to 6,400: any counter in its place moves gun 6.4k from 12.8k to 35.2k (Plated Armor/Unstoppable 38.4k), 22k souls without the tier, and spirit 4.8k 20.8k to 22.4k-25.6k.
   - Fix: Sell Battle Vest or Bullet Lifesteal (vitality) instead; the Spellslinger line already sells Battle Vest, so use Bullet Lifesteal for counters (Vampiric Burst then costs 6,400).
2. **LOW** Bullet Resist Shredder: Rich: Crippling Headshot sells Bullet Resist Shredder, taking spirit from 8,000 to 6,400 (loses the 8k tier).
   - Fix: Sell Opening Rounds there and let Armor Piercer sell Bullet Resist Shredder, or accept.

## OK / notes

- Weapon 4.8k at 4.8k with 0 off-colour souls (HVR, Rapid Rounds, Extended Magazine, Opening Rounds, Titanic Magazine, Swift Striker): the six T1/T2 gun items are all named sells or consumed.
- Health 4.8k at 11.2k (Enduring Speed) is right for a fighty gun hero. Four T4 in a row from 28.8k (Vampiric Burst, Spiritual Overflow, Siphon Bullets, Spellslinger): allowed.
- Mercurial Magnum counts as a gun item (4,800 net at 20.8k).

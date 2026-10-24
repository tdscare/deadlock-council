# celeste - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | High-Velocity Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Opening Rounds (from High-Velocity Rounds) | T2 | w | 800 | 1600 | 0 | 0 | 1 |
| 2400 | Extra Regen | T1 | v | 800 | 1600 | 0 | 800 | 2 |
| 3200 | Mystic Regeneration | T1 | s | 800 | 1600 | 800 | 800 | 3 |
| 4000 | Mystic Expansion | T1 | s | 800 | 1600 | 1600 | 800 | 4 |
| 6400 | Radiant Regeneration (from Mystic Regeneration) | T3 | s | 2400 | 1600 | 4000 | 800 | 4 |
| 7200 | Mystic Burst | T1 | s | 800 | 1600 | 4800 | 800 | 5 |
| 8000 | Healing Booster (from Extra Regen) | T2 | v | 800 | 1600 | 4800 | 1600 | 5 |
| 8800 | Grit | T1 | v | 800 | 1600 | 4800 | 2400 | 6 |
| 9600 | Spirit Shielding (from Grit) | T2 | v | 800 | 1600 | 4800 | 3200 | 6 |
| 11200 | Restorative Locket | T2 | v | 1600 | 1600 | 4800 | 4800 | 7 |
| 14400 | Torment Pulse | T3 | s | 3200 | 1600 | 8000 | 4800 | 8 |
| 16800 | Greater Expansion (from Mystic Expansion) | T3 | s | 2400 | 1600 | 10400 | 4800 | 8 |
| 18400 | Spirit Lifesteal | T2 | v | 1600 | 1600 | 10400 | 6400 | 9 |
| 20000 | Suppressor | T2 | s | 1600 | 1600 | 12000 | 6400 | 10 |
| 21600 | Mystic Vulnerability | T2 | s | 1600 | 1600 | 13600 | 6400 | 11 |
| 24000 | Tankbuster (from Mystic Burst) | T3 | s | 2400 | 1600 | 16000 | 6400 | 11 |
| 27200 | Superior Cooldown | T3 | s | 3200 | 1600 | 19200 | 6400 | 12 |
| 33600 | Witchmail | T4 | v | 6400 | 0 | 19200 | 12800 | 12 |
| 38400 | Escalating Exposure (from Mystic Vulnerability) | T4 | s | 4800 | 0 | 24000 | 12800 | 12 |
| 43200 | Spiritual Overflow (from Spirit Lifesteal) | T4 | w | 4800 | 6400 | 24000 | 11200 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@1600, 2400@43200, 3200@43200, 4800@43200, 6400@43200
- spirit: 800@3200, 1600@4000, 2400@6400, 3200@6400, 4800@7200, 6400@14400, 8000@14400, 11200@20000, 16000@24000, 22400@38400
- vitality: 800@2400, 1600@8000, 2400@8800, 3200@9600, 4800@11200, 6400@18400, 8000@33600, 11200@33600

## Flags

1. **MED** Restorative Locket: Restorative Locket (vitality, 1,600) at 11.2k: no SP, no HP (TechResist 8; active heals teammates 16 + 0.45 x SP per stack). It exists to complete health 4.8k. Enchanter's Emblem costs the same 1,600, is the same vitality colour and gives +15 SP and +18 spirit resist on a spirit build (9.4 SP per 1,000). Boundless in the rich box sells Locket, so it is dead weight until then.
   - Fix: Swap Restorative Locket for Enchanter's Emblem (and the rich note 'Sell Enchanter's Emblem for this'). Re-walked: s4.8k 7.2k, v4.8k 11.2k, v6.4k 18.4k, all identical.
2. **LOW** Spiritual Overflow, Extra Spirit, Boundless Spirit: The core has no Extra Spirit / Improved Spirit chain and Boundless Spirit is only in the rich box (it would cost 6,400 without Improved Spirit). SP at the end of core is 137 (baba 148, apollo 195). Spiritual Overflow, last core buy at 43.2k, gives +6 SP flat and its +30 SP only while shots are building it up; 'Star Spammer' shoots little.
   - Fix: No change without same-style evidence from current top Celeste builds; if they run Extra Spirit -> Improved Spirit -> Boundless, those replace Spiritual Overflow (weapon 4.8k at 43.2k exists only because of it).
3. **LOW** Rapid Recharge: Rule G (outside cost): Rapid Recharge is T3 but sits in the 'I'm rich as fuck' box (T4 only).
   - Fix: Drop it or replace with a T4 pricier version.

## OK / notes

- Spirit 4.8k at 7.2k vs 4.8k minimum: 2,400 off-colour (HVR 800 + Opening Rounds 800 lane items, sold for Witchmail; Extra Regen 800 -> Healing Booster). Mystic Burst at 7.2k: Radiant Daggers 55 + 15 (T2) + 0.63 x 58 SP = 106 > 80 (ok). Tankbuster 24.0k: Daggers 125 + 0.63 x 114 = 197 > 165 (ok).
- Counters sell Suppressor (s2, a named sell): weapon 4.8k (only reached via Spiritual Overflow) moves 43.2k to 46.4k; no spirit/vitality dip.

# sinclair - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | Monster Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Extra Health | T1 | v | 800 | 800 | 0 | 800 | 2 |
| 3200 | Stalker | T2 | w | 1600 | 2400 | 0 | 800 | 3 |
| 5600 | Cultist Sacrifice (from Monster Rounds) | T3 | w | 2400 | 4800 | 0 | 800 | 3 |
| 6400 | Grit | T1 | v | 800 | 4800 | 0 | 1600 | 4 |
| 8800 | Fortitude (from Extra Health) | T3 | v | 2400 | 4800 | 0 | 4000 | 4 |
| 9600 | Reactive Barrier (from Grit) | T2 | v | 800 | 4800 | 0 | 4800 | 4 |
| 11200 | Melee Charge | T2 | w | 1600 | 6400 | 0 | 4800 | 5 |
| 12800 | Enduring Speed | T2 | v | 1600 | 6400 | 0 | 6400 | 6 |
| 13600 | Sprint Boots | T1 | v | 800 | 6400 | 0 | 7200 | 7 |
| 16000 | Shadow Weave (from Sprint Boots) | T3 | w | 2400 | 9600 | 0 | 6400 | 7 |
| 17600 | Duration Extender | T2 | s | 1600 | 9600 | 1600 | 6400 | 8 |
| 19200 | Superior Duration (from Duration Extender) | T3 | s | 1600 | 9600 | 3200 | 6400 | 8 |
| 20800 | Cold Front | T2 | s | 1600 | 9600 | 4800 | 6400 | 9 |
| 24000 | Point Blank | T3 | w | 3200 | 12800 | 4800 | 6400 | 10 |
| 27200 | Hollow Point | T3 | w | 3200 | 16000 | 4800 | 6400 | 11 |
| 32000 | Arctic Blast (from Cold Front) | T4 | s | 4800 | 16000 | 9600 | 6400 | 11 |
| 36800 | Crushing Fists (from Melee Charge) | T4 | w | 4800 | 20800 | 9600 | 6400 | 11 |
| 40000 | Alchemical Fire | T3 | w | 3200 | 22400 | 9600 | 6400 | 11 |
| 46400 | Colossus | T4 | v | 6400 | 22400 | 9600 | 12800 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@3200, 2400@3200, 3200@5600, 4800@5600, 6400@11200, 8000@16000, 11200@24000, 16000@27200, 22400@40000
- spirit: 800@17600, 1600@17600, 2400@19200, 3200@19200, 4800@20800, 6400@32000, 8000@32000
- vitality: 800@1600, 1600@6400, 2400@8800, 3200@8800, 4800@9600, 6400@12800, 8000@46400, 11200@46400

## Flags

1. **MED** Lifestrike, Hollow Point: 'Swap for Hollow Point' -> Lifestrike changes colour (weapon to vitality). Re-walked with the swap applied (Lifestrike is 3,200 here, Melee Lifesteal is not owned): weapon 4.8k/6.4k/8k/11.2k are unchanged (5.6k/11.2k/16.0k/24.0k) but the weapon 16k tier moves 27.2k to 36.8k and the 22.4k tier (Alchemical Fire at 40.0k) is never reached in core (19,200 end vs 22,400); vitality 8k moves 46.4k to 27.2k. The Hunter's Aura swap is weapon-for-weapon, same price, nothing moves.
   - Fix: Put the Lifestrike line against a vitality/spirit item or against the last weapon item: 'Swap for Alchemical Fire'. Re-walked with Lifestrike in place of Alchemical Fire (40.0k): the 16k weapon tier stays 27.2k, only the late 22.4k tier is lost, and vitality 8k moves to 40.0k.
2. **MED** Cultist Sacrifice, Stalker: Counters box sells Cultist Sacrifice for all six counters. Sinclair's weapon 4.8k is exactly Monster Rounds 800 + Stalker 1,600 + Cultist 2,400 = 4,800 at 5.6k; selling Cultist after Fortitude (8.8k) drops weapon to 1,600 and the 4.8k tier is gone from 12.0k to 19.2k (T3 counters) or 15.2k to 22.4k (T4 counters). Selling Stalker instead dips 12.0k-14.4k.
   - Fix: Counters sell Reactive Barrier (or Fortitude): vitality for vitality, re-walked clean (only the counter's cost shifts spirit 4.8k 20.8k to 24.0k).
3. **MED** Crushing Fists: Crushing Fists (Melee Charge upgrade, 4,800 net) is bought at 36.8k, the latest of any build that has it (apollo_melee 24.0k, billy 26.4k, venator 32.0k), after Cold Front, Point Blank, Hollow Point and Arctic Blast. Melee Charge has been held since 11.2k, and Kieran's Sinclair line is 'Melee Charge -> Crushing Fists'. It is not early either (T4, after the Cultist + health spikes).
   - Fix: Move Crushing Fists before Arctic Blast (32.0k). Re-walked: Arctic Blast 32.0k to 36.8k (spirit 6.4k/8k tier 32.0k to 36.8k); every weapon/vitality spike unchanged.

## OK / notes

- Weapon 4.8k at 5.6k (800 off-colour: Extra Health), health 4.8k at 9.6k. Cultist at 5.6k (the note says by about 8 minutes; fine).
- Enduring Speed is bought at full price (12.8k) before Sprint Boots because Sprint Boots is then consumed by Shadow Weave (2,400 net); total 4,800 for both either way.
- Rich: Kevlar/Phantom Strike sells Hollow Point/Cultist drop the 22.4k weapon tier only; Echo Shard sells Alchemical Fire (gains spirit 11.2k + 16k).

# doorman_support - cost audit (chunk 2)

## Core walk (buy order, net cost, invest per colour)

| souls | item | tier | col | cost | w | s | v | slots |
|---|---|---|---|---|---|---|---|---|
| 800 | High-Velocity Rounds | T1 | w | 800 | 800 | 0 | 0 | 1 |
| 1600 | Opening Rounds (from High-Velocity Rounds) | T2 | w | 800 | 1600 | 0 | 0 | 1 |
| 2400 | Extra Charge | T1 | s | 800 | 1600 | 800 | 0 | 2 |
| 3200 | Healing Rite | T1 | v | 800 | 1600 | 800 | 800 | 3 |
| 4000 | Grit | T1 | v | 800 | 1600 | 800 | 1600 | 4 |
| 6400 | Rapid Recharge (from Extra Charge) | T3 | s | 2400 | 1600 | 3200 | 1600 | 4 |
| 8000 | Compress Cooldown | T2 | s | 1600 | 1600 | 4800 | 1600 | 5 |
| 8800 | Sprint Boots | T1 | v | 800 | 1600 | 4800 | 2400 | 6 |
| 9600 | Guardian Ward (from Grit) | T2 | v | 800 | 1600 | 4800 | 3200 | 6 |
| 10400 | Trophy Collector (from Sprint Boots) | T2 | v | 800 | 1600 | 4800 | 4000 | 6 |
| 12000 | Enchanter's Emblem | T2 | v | 1600 | 1600 | 4800 | 5600 | 7 |
| 15200 | Heroic Aura | T3 | w | 3200 | 4800 | 4800 | 5600 | 8 |
| 16800 | Slowing Hex | T2 | s | 1600 | 4800 | 6400 | 5600 | 9 |
| 17600 | Extra Spirit | T1 | s | 800 | 4800 | 7200 | 5600 | 10 |
| 18400 | Improved Spirit (from Extra Spirit) | T2 | s | 800 | 4800 | 8000 | 5600 | 10 |
| 20800 | Rescue Beam (from Healing Rite) | T3 | v | 2400 | 4800 | 8000 | 8000 | 10 |
| 24000 | Warp Stone | T3 | v | 3200 | 4800 | 8000 | 11200 | 11 |
| 25600 | Superior Cooldown (from Compress Cooldown) | T3 | s | 1600 | 4800 | 9600 | 11200 | 11 |
| 30400 | Vortex Web (from Slowing Hex) | T4 | s | 4800 | 4800 | 14400 | 11200 | 11 |
| 35200 | Divine Barrier (from Guardian Ward) | T4 | v | 4800 | 4800 | 14400 | 16000 | 11 |
| 38400 | Knockdown | T3 | s | 3200 | 4800 | 17600 | 16000 | 12 |
| 43200 | Boundless Spirit (from Improved Spirit) | T4 | s | 4800 | 4800 | 22400 | 16000 | 12 |
| 49600 | Cheat Death | T4 | v | 6400 | 3200 | 22400 | 22400 | 12 |

## Spikes (first soul total each invest tier is reached)

- weapon: 800@800, 1600@1600, 2400@15200, 3200@15200, 4800@15200
- spirit: 800@2400, 1600@6400, 2400@6400, 3200@6400, 4800@8000, 6400@16800, 8000@18400, 11200@30400, 16000@38400, 22400@43200
- vitality: 800@3200, 1600@4000, 2400@8800, 3200@9600, 4800@12000, 6400@20800, 8000@20800, 11200@24000, 16000@35200, 22400@49600

## Flags

1. **MED** Rescue Beam, Healing Rite: Rescue Beam, the support's signature heal, arrives at 20.8k (slot #16) after Heroic Aura (15.2k), Slowing Hex and Extra Spirit/Improved Spirit; the other support builds buy it at 5.6k (dynamo), 9.6k (viscous) and 12.8k (paige_support). Healing Rite is held 17.6k souls (800, named upgrade). Rescue Beam is also the cheapest vitality step (2,400 net).
   - Fix: Move Rescue Beam to right after Trophy Collector (12.8k vs 20.8k). Re-walked: health 4.8k 12.0k to 12.8k, health 6.4k/8k 20.8k to 12.8k/14.4k, gun 4.8k (Heroic Aura) 15.2k to 17.6k, spirit 6.4k 16.8k to 19.2k.
2. **LOW** Cheat Death, Opening Rounds: Core note on Cheat Death sells Opening Rounds: weapon invest is exactly 4,800 (HVR/Opening Rounds 1,600 + Heroic Aura 3,200), so the sell drops it to 3,200 and the 4.8k weapon tier is lost for good at 49.6k.
   - Fix: Cheat Death sells Enchanter's Emblem, Trophy Collector, Rescue Beam or Warp Stone (all clean on re-walk). Mind the rich-box overlaps: Refresher sells Emblem, Witchmail sells Trophy Collector, Cursed Relic sells Warp Stone; so use Rescue Beam-free choice Warp Stone only if Cursed Relic sells something else.
3. **LOW** Knockdown: Counters sell Knockdown (unbought at 'Get after Guardian Ward'): spirit 22.4k tier (Boundless at 43.2k) is never reached (19,200).
   - Fix: Accept, or sell Slowing Hex-class spirit T2 only if one is unbought; no clean sell exists without losing the 22.4k tier.

## OK / notes

- Swap box 'Swap for Heroic Aura' -> Alchemical Fire: weapon T3 3,200 for weapon T3 3,200 in the same slot; re-walked identical for every colour and every spike (s4.8k 8.0k, v4.8k 12.0k, w4.8k 15.2k). OK.
- Spirit 4.8k at 8.0k (3,200 off-colour: Healing Rite, Grit, HVR/Opening Rounds), health 4.8k at 12.0k.

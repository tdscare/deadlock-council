# viscous_damage - Rizuhble's Goo Punch Viscous (Damage Viscous)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spirit 4.8k @4800 is the minimum possible; health @11200. Improved Spirit is bought far too late (19200).

**Spike positions (first souls total at which invest >= 4800):**  {"s":4800,"v":11200,"w":27200} end 49600

## Flags (1)

1. **MED** - Improved Spirit: Improved Spirit is an 800 upgrade of the Extra Spirit owned since 1600 and is the best item per soul in the game (+18 spirit, +75 HP = 22.5 spirit/k, 93.8 HP/k) but is bought @19200, 17.6k souls after Extra Spirit. Re-walked with Improved Spirit right after Compress Cooldown (@5600): spirit 4.8k stays @4800 (then 5600), health 4.8k moves 11200 -> 12000, gun @27200 unchanged.
   - Minimal fix: Move Improved Spirit to just after Compress Cooldown.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Mystic Burst (s1) | 0 | 800 | 0 | OK | - |
| 1600 | Early | +800 | Extra Spirit (s1) | 0 | 1600 | 0 | OK | TechPower=10(12.5/k) |
| 2400 | Early | +800 | Mystic Expansion (s1) | 0 | 2400 | 0 | OK | - |
| 3200 | Early | +800 | Spirit Strike (s1) | 0 | 3200 | 0 | OK | - |
| 4800 | Early | +1600 | Compress Cooldown (s2) | 0 | 4800 | 0 | OK | - |
| 5600 | Early | +800 | Melee Lifesteal (v1) | 0 | 4800 | 800 | OK | - |
| 6400 | Early | +800 | Extra Health (v1) | 0 | 4800 | 1600 | OK | BonusHealth=210(262.5/k) |
| 8000 | Early | +1600 | Melee Charge (w2) | 1600 | 4800 | 1600 | OK | BulletResist=6(3.8/k) |
| 10400 | Mid | +2400 | Lifestrike (v3) | 1600 | 4800 | 4000 | OK | BonusHealth=125(52.1/k) |
| 11200 | Mid | +800 | Grit (v1) | 1600 | 4800 | 4800 | OK | - |
| 13600 | Mid | +2400 | Spirit Snatch (s3) | 1600 | 7200 | 4800 | OK | BonusHealth=75(31.3/k) |
| 16000 | Mid | +2400 | Tankbuster (s3) | 1600 | 9600 | 4800 | OK | BonusHealth=50(20.8/k) |
| 17600 | Mid | +1600 | Superior Cooldown (s3) | 1600 | 11200 | 4800 | OK | - |
| 18400 | Mid | +800 | Spirit Shielding (v2) | 1600 | 11200 | 5600 | OK | TechResist=18(22.5/k) |
| 19200 | Mid | +800 | Improved Spirit (s2) | 1600 | 12000 | 5600 | FLAG MED | TechPower=18(22.5/k) BonusHealth=75(93.8/k) |
| 20000 | Mid | +800 | Extra Charge (s1) | 1600 | 12800 | 5600 | OK | - |
| 22400 | Late | +2400 | Greater Expansion (s3) | 1600 | 15200 | 5600 | OK | TechResist=10(4.2/k) |
| 27200 | Late | +4800 | Crushing Fists (w4) | 6400 | 15200 | 5600 | OK | BulletResist=12(2.5/k) |
| 29600 | Late | +2400 | Fortitude (v3) | 6400 | 15200 | 8000 | OK | BonusMoveSpeed=1.5m(0.6/k) BonusHealth=375(156.3/k) |
| 32000 | Late | +2400 | Rapid Recharge (s3) | 6400 | 17600 | 8000 | OK | - |
| 36800 | Late | +4800 | Boundless Spirit (s4) | 6400 | 22400 | 8000 | OK | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |
| 43200 | Late | +6400 | Mystic Reverb (s4) | 6400 | 28800 | 8000 | OK | - |
| 49600 | Late | +6400 | Spirit Burn (s4) | 6400 | 35200 | 8000 | OK | - |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Tankbuster @16000 precedes Spirit Burn @49600.
- Fortitude (+2400 via Extra Health) is late (29600) but Extra Health @6400 supplies early HP: fine.
- Crushing Fists, Melee Charge: Crushing Fists (+4800 @27200) is late and follows Melee Charge (bought @8000 for the Puddle Punch note): timing OK. Gun 4.8k only arrives with it (@27200).

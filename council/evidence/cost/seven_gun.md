# seven_gun - Rizuhble's Static Shock Seven (Gun-spirit Seven)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Mostly OK. All three colours reach 4.8k (gun 7200, spirit 11200, health 14400). Two cheap improvements.

**Spike positions (first souls total at which invest >= 4800):**  {"w":7200,"s":11200,"v":14400} end 44800

## Flags (2)

1. **LOW** - Enchanter's Emblem: Emblem (v2, 1600, no HP, 9.4 spirit/k) is bought before Cultist Sacrifice, so the gun 4.8k lands at 7200 instead of 5600 (re-walked: Monster Rounds, HV, Opening Rounds, Extra Spirit, Cultist, then Emblem gives gun 4.8k @5600, spirit @11200, health @14400 unchanged).
   - Minimal fix: Move Enchanter's Emblem to right after Cultist Sacrifice.
2. **LOW** - Boundless Spirit: Boundless is paid in full (+6400 @44800) because Improved Spirit is never owned. Improved Spirit (1600, +18 spirit, +75 HP, 11.3 spirit/k) is credited 100% toward Boundless, so owning it from mid game costs 0 net souls. Slots still fit (12th slot is reached at Unstoppable and Improved Spirit is absorbed by Boundless).
   - Minimal fix: Buy Improved Spirit around 12-17k (after Spirit Lifesteal); Boundless then costs +4800.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Monster Rounds (w1) | 800 | 0 | 0 | OK | - |
| 1600 | Early | +800 | High-Velocity Rounds (w1) | 1600 | 0 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 2400 | Early | +800 | Opening Rounds (w2) | 2400 | 0 | 0 | OK | TechPower=7(8.8/k) BaseAttackDamagePercent=8(10.0/k) |
| 3200 | Early | +800 | Extra Spirit (s1) | 2400 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 4800 | Early | +1600 | Enchanter's Emblem (v2) | 2400 | 800 | 1600 | FLAG LOW | TechPower=15(9.4/k) TechResist=18(11.3/k) |
| 7200 | Early | +2400 | Cultist Sacrifice (w3) | 4800 | 800 | 1600 | OK | BonusHealth=50 (+4x ELevelUpBoons)(20.8/k) BaseAttackDamagePercent=10 (+0.8x ELevelUpBoons)(4.2/k) |
| 8800 | Early | +1600 | Duration Extender (s2) | 4800 | 2400 | 1600 | OK | - |
| 11200 | Early | +2400 | Surge of Power (s3) | 4800 | 4800 | 1600 | OK | BonusMoveSpeed=1.75m(0.7/k) |
| 12800 | Mid | +1600 | Spirit Lifesteal (v2) | 4800 | 4800 | 3200 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 13600 | Mid | +800 | Sprint Boots (v1) | 4800 | 4800 | 4000 | OK | - |
| 14400 | Mid | +800 | Enduring Speed (v2) | 4800 | 4800 | 4800 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 17600 | Mid | +3200 | Tesla Bullets (w3) | 8000 | 4800 | 4800 | OK | - |
| 19200 | Mid | +1600 | Mystic Vulnerability (s2) | 8000 | 6400 | 4800 | OK | TechResist=8(5.0/k) |
| 22400 | Mid | +3200 | Toxic Bullets (w3) | 11200 | 6400 | 4800 | OK | - |
| 27200 | Mid | +4800 | Escalating Exposure (s4) | 11200 | 11200 | 4800 | OK | TechResist=17(3.5/k) |
| 33600 | Late | +6400 | Unstoppable (v4) | 11200 | 11200 | 11200 | OK | BonusHealth=125(19.5/k) |
| 38400 | Late | +4800 | Spiritual Overflow (w4) | 17600 | 11200 | 9600 | OK | TechPower=6(1.3/k) BonusHealth=90(18.8/k) BonusFireRate=25(5.2/k) |
| 44800 | Late | +6400 | Boundless Spirit (s4) | 17600 | 17600 | 9600 | FLAG LOW | TechPower=30(4.7/k) BonusHealth=75(11.7/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Tesla Bullets (17600) sits after the spirit 4.8k (11200): correct for a spirit-scaling gun item.
- Counters "Sell Opening Rounds" does not break the gun spike at that point (gun is 17600 by then).
- Unstoppable 6400 (@33600) is bought without Debuff Reducer (stepping stone, 1600, 90 HP) - fine, it is the note-carrying active.

# geist - Rizuhble's Life Leech Gun Geist (Gun tank Geist)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Gun 6400, health 12800 (sustain hero: allowed), spirit 18400. Leech arrives late with no lifesteal before it.

**Spike positions (first souls total at which invest >= 4800):**  {"w":6400,"v":12800,"s":18400} end 43200

## Flags (2)

1. **MED** - Leech: Leech is paid in full (6400 @34400): Bullet Lifesteal and Spirit Lifesteal (3200 total, 100% credited) are never bought, so a gun-tank hero has no lifesteal until 34k (Kieran: sustain must exist).
   - Minimal fix: Buy Bullet Lifesteal + Spirit Lifesteal around 13-18k; Leech then +3200.
2. **MED** - Spellslinger: Spellslinger (6400 @24800) is conditional fire rate (1.7/k).
   - Minimal fix: Move to rich or replace.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Monster Rounds (w1) | 800 | 0 | 0 | OK | - |
| 1600 | Early | +800 | Extra Regen (v1) | 800 | 0 | 800 | OK | BonusHealthRegen=2.5(3.1/k) |
| 2400 | Early | +800 | Mystic Regeneration (s1) | 800 | 800 | 800 | OK | BonusHealth=50(62.5/k) |
| 3200 | Early | +800 | Extra Stamina (v1) | 800 | 800 | 1600 | OK | - |
| 4000 | Early | +800 | Kinetic Dash (w2) | 2400 | 800 | 800 | OK | BonusFireRate=25(31.3/k) BonusClipSize=6(7.5/k) |
| 6400 | Early | +2400 | Cultist Sacrifice (w3) | 4800 | 800 | 800 | OK | BonusHealth=50 (+4x ELevelUpBoons)(20.8/k) BaseAttackDamagePercent=10 (+0.8x ELevelUpBoons)(4.2/k) |
| 8800 | Mid | +2400 | Radiant Regeneration (s3) | 4800 | 3200 | 800 | OK | BonusMoveSpeed=1.75m(0.7/k) BonusHealth=90(37.5/k) |
| 9600 | Mid | +800 | Healing Booster (v2) | 4800 | 3200 | 1600 | OK | BonusHealthRegen=3(3.8/k) |
| 12800 | Mid | +3200 | Spirit Resilience (v3) | 4800 | 3200 | 4800 | OK | TechResist=30(9.4/k) |
| 16000 | Mid | +3200 | Berserker (w3) | 8000 | 3200 | 4800 | OK | BulletResist=8(2.5/k) |
| 16800 | Mid | +800 | Extra Charge (s1) | 8000 | 4000 | 4800 | OK | - |
| 18400 | Mid | +1600 | Bullet Resist Shredder (s2) | 8000 | 5600 | 4800 | OK | BaseAttackDamagePercent=9(5.6/k) BulletResist=9(5.6/k) |
| 24800 | Mid | +6400 | Spellslinger (w4) | 14400 | 5600 | 4800 | FLAG MED | BonusFireRate=11(1.7/k) |
| 28000 | Mid | +3200 | Blood Tribute (w3) | 17600 | 5600 | 4800 | OK | TechResist=8(2.5/k) BonusFireRate=35(10.9/k) BonusMoveSpeed=2.0m(0.6/k) |
| 34400 | Late | +6400 | Leech (v4) | 17600 | 5600 | 11200 | FLAG MED | TechPower=12(1.9/k) BaseAttackDamagePercent=12(1.9/k) BonusHealth=180(28.1/k) |
| 36800 | Late | +2400 | Rapid Recharge (s3) | 17600 | 8000 | 11200 | OK | - |
| 43200 | Late | +6400 | Refresher (s4) | 17600 | 14400 | 11200 | OK | TechResist=14(2.2/k) BulletResist=15(2.3/k) |

## Swap / reorder boxes re-walked

Boxes found: Counters. Results are in the flags above (re-walk numbers quoted there).

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Kinetic Dash consumes Extra Stamina: gun +1600, vitality -800.
- Spirit Resilience: Spirit Resilience (v3 3200 @12800) has 0 HP (9.4 resist/k) and is the health 4.8k item.

# venator_grenade - Rizuhble's Holy Hand Grenade (Grenade Venator)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Efficient: gun 4.8k @4800 (the minimum possible), health @9600. Spirit never reaches 4.8k (3200).

**Spike positions (first souls total at which invest >= 4800):**  {"w":4800,"v":9600} end 49600

## Flags (2)

1. **LOW** - Extra Charge, Rapid Recharge: Spirit invest is only 3200 (Extra Charge -> Rapid Recharge), 1600 short of 4.8k, for the whole build.
   - Minimal fix: Swap Recharging Rush (w2 1600, sold for Ricochet anyway) for Improved Spirit (1600, +18 spirit, +75 HP): spirit 4800, gun still 11200+; needs a kit check that Recharging Rush is not needed for the grenade.
2. **LOW** - Vampiric Burst, Ballistic Enchantment: Both bought in full (Vampiric Burst 6400 without Bullet Lifesteal, Ballistic Enchantment 3200 without Mystic Expansion). The skipped T1/T2s are credited 100% so owning them earlier costs 0 net, and Bullet Lifesteal (1600, 90 HP, 6% weapon damage) gives sustain from mid game (Kieran: sustain must exist).
   - Minimal fix: Buy Bullet Lifesteal around 13-18k; Vampiric Burst then +4800.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | High-Velocity Rounds (w1) | 800 | 0 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 1600 | Early | +800 | Close Quarters (w1) | 1600 | 0 | 0 | OK | - |
| 2400 | Early | +800 | Monster Rounds (w1) | 2400 | 0 | 0 | OK | - |
| 4800 | Early | +2400 | Cultist Sacrifice (w3) | 4800 | 0 | 0 | OK | BonusHealth=50 (+4x ELevelUpBoons)(20.8/k) BaseAttackDamagePercent=10 (+0.8x ELevelUpBoons)(4.2/k) |
| 6400 | Early | +1600 | Battle Vest (v2) | 4800 | 0 | 1600 | OK | BulletResist=18(11.3/k) BaseAttackDamagePercent=18(11.3/k) BonusFireRate=7(4.4/k) |
| 7200 | Early | +800 | Extra Health (v1) | 4800 | 0 | 2400 | OK | BonusHealth=210(262.5/k) |
| 9600 | Early | +2400 | Fortitude (v3) | 4800 | 0 | 4800 | OK | BonusMoveSpeed=1.5m(0.6/k) BonusHealth=375(156.3/k) |
| 12800 | Mid | +3200 | Berserker (w3) | 8000 | 0 | 4800 | OK | BulletResist=8(2.5/k) |
| 16000 | Mid | +3200 | Hollow Point (w3) | 11200 | 0 | 4800 | OK | BaseAttackDamagePercent=35(10.9/k) BonusHealth=125(39.1/k) |
| 17600 | Mid | +1600 | Recharging Rush (w2) | 12800 | 0 | 4800 | OK | BaseAttackDamagePercent=10(6.3/k) |
| 18400 | Mid | +800 | Extra Charge (s1) | 12800 | 800 | 4800 | FLAG LOW | - |
| 21600 | Mid | +3200 | Ballistic Enchantment (w3) | 16000 | 800 | 4800 | FLAG LOW | - |
| 24000 | Mid | +2400 | Rapid Recharge (s3) | 16000 | 3200 | 4800 | FLAG LOW | - |
| 30400 | Mid | +6400 | Vampiric Burst (v4) | 16000 | 3200 | 11200 | FLAG LOW | BonusHealth=100(15.6/k) BulletResist=10(1.6/k) BaseAttackDamagePercent=6(0.9/k) |
| 36800 | Late | +6400 | Silencer (w4) | 21600 | 3200 | 11200 | OK | TechResist=12(1.9/k) |
| 43200 | Late | +6400 | Inhibitor (v4) | 21600 | 3200 | 17600 | OK | BonusHealth=150(23.4/k) BaseAttackDamagePercent=10(1.6/k) |
| 49600 | Late | +6400 | Crippling Headshot (w4) | 27200 | 3200 | 17600 | OK | BonusHealth=125(19.5/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Late 6.4k run (Vampiric Burst 30400, Silencer 36800, Inhibitor 43200, Crippling Headshot 49600) starts at 30k: allowed.
- Fortitude (+2400 via Extra Health) hits health 4.8k before Berserker: correct order for an in-your-face grenade hero.

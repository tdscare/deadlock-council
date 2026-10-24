# violet_spirit - Rizuhble's Happy Little Splats (Spirit Violet)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spirit 5600 and health 9600 are efficient. Gun is 0 for the whole build. Boundless is paid in full.

**Spike positions (first souls total at which invest >= 4800):**  {"s":5600,"v":9600} end 46400

## Flags (2)

1. **LOW** - Boundless Spirit: Boundless paid in full (+6400 @35200); Improved Spirit (1600, 18 spirit, 75 HP) is a free stepping stone that would give +18 spirit from ~10k.
   - Minimal fix: Buy Improved Spirit before Mystic Burst/Radiant Regeneration; Boundless then +4800.
2. **LOW** - Extra Spirit: Gun never gets any invest (0).
   - Minimal fix: Policy call for a spirit build.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 0 | FLAG LOW | TechPower=10(12.5/k) |
| 1600 | Early | +800 | Extra Regen (v1) | 0 | 800 | 800 | OK | BonusHealthRegen=2.5(3.1/k) |
| 2400 | Early | +800 | Extra Charge (s1) | 0 | 1600 | 800 | OK | - |
| 3200 | Early | +800 | Mystic Regeneration (s1) | 0 | 2400 | 800 | OK | BonusHealth=50(62.5/k) |
| 5600 | Early | +2400 | Surge of Power (s3) | 0 | 4800 | 800 | OK | BonusMoveSpeed=1.75m(0.7/k) |
| 6400 | Early | +800 | Grit (v1) | 0 | 4800 | 1600 | OK | - |
| 7200 | Early | +800 | Healing Booster (v2) | 0 | 4800 | 2400 | OK | BonusHealthRegen=3(3.8/k) |
| 8000 | Early | +800 | Spirit Shielding (v2) | 0 | 4800 | 3200 | OK | TechResist=18(22.5/k) |
| 9600 | Mid | +1600 | Spirit Lifesteal (v2) | 0 | 4800 | 4800 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 10400 | Mid | +800 | Mystic Burst (s1) | 0 | 5600 | 4800 | OK | - |
| 12800 | Mid | +2400 | Radiant Regeneration (s3) | 0 | 8000 | 4800 | OK | BonusMoveSpeed=1.75m(0.7/k) BonusHealth=90(37.5/k) |
| 14400 | Mid | +1600 | Enchanter's Emblem (v2) | 0 | 8000 | 6400 | OK | TechPower=15(9.4/k) TechResist=18(11.3/k) |
| 16800 | Mid | +2400 | Rapid Recharge (s3) | 0 | 10400 | 6400 | OK | - |
| 18400 | Mid | +1600 | Compress Cooldown (s2) | 0 | 12000 | 6400 | OK | - |
| 20000 | Mid | +1600 | Mystic Vulnerability (s2) | 0 | 13600 | 6400 | OK | TechResist=8(5.0/k) |
| 22400 | Mid | +2400 | Tankbuster (s3) | 0 | 16000 | 6400 | OK | BonusHealth=50(20.8/k) |
| 24000 | Late | +1600 | Superior Cooldown (s3) | 0 | 17600 | 6400 | OK | - |
| 28800 | Late | +4800 | Escalating Exposure (s4) | 0 | 22400 | 6400 | OK | TechResist=17(3.5/k) |
| 35200 | Late | +6400 | Boundless Spirit (s4) | 0 | 28800 | 6400 | FLAG LOW | TechPower=30(4.7/k) BonusHealth=75(11.7/k) |
| 41600 | Late | +6400 | Spirit Burn (s4) | 0 | 35200 | 6400 | OK | - |
| 46400 | Late | +4800 | Infuser (v4) | 0 | 35200 | 11200 | OK | TechPower=6(1.3/k) BonusHealth=100(20.8/k) TechResist=10(2.1/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Surge of Power (+2400 @5600) brings spirit 4.8k with only Extra Regen diverted: efficient.
- Tankbuster @22400, Spirit Burn @41600: order fine.

# vindicta_sniper - Rizuhble's Heaven Sent Headshots (Sniper Vindicta)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spirit 5600, health 9600 are efficient. Gun only reaches 4.8k at the very end (56000, Spiritual Overflow). Core is long (56000).

**Spike positions (first souls total at which invest >= 4800):**  {"s":5600,"v":9600,"w":56000} end 56000

## Flags (1)

1. **LOW** - Spiritual Overflow: Gun 6400 appears only with Spiritual Overflow @56000 (practically never).
   - Minimal fix: Policy call for a spirit build.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 1600 | Early | +800 | Mystic Burst (s1) | 0 | 1600 | 0 | OK | - |
| 2400 | Early | +800 | Sprint Boots (v1) | 0 | 1600 | 800 | OK | - |
| 3200 | Early | +800 | Extra Charge (s1) | 0 | 2400 | 800 | OK | - |
| 5600 | Early | +2400 | Rapid Recharge (s3) | 0 | 4800 | 800 | OK | - |
| 6400 | Early | +800 | Enduring Speed (v2) | 0 | 4800 | 1600 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 9600 | Early | +3200 | Counterspell (v3) | 0 | 4800 | 4800 | OK | BonusMoveSpeed=1.75m(0.5/k) BonusHealth=50(15.6/k) |
| 10400 | Mid | +800 | Improved Spirit (s2) | 0 | 5600 | 4800 | OK | TechPower=18(22.5/k) BonusHealth=75(93.8/k) |
| 12000 | Mid | +1600 | Mystic Vulnerability (s2) | 0 | 7200 | 4800 | OK | TechResist=8(5.0/k) |
| 14400 | Mid | +2400 | Tankbuster (s3) | 0 | 9600 | 4800 | OK | BonusHealth=50(20.8/k) |
| 16000 | Mid | +1600 | Compress Cooldown (s2) | 0 | 11200 | 4800 | OK | - |
| 17600 | Mid | +1600 | Spirit Lifesteal (v2) | 0 | 11200 | 6400 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 20800 | Mid | +3200 | Surge of Power (s3) | 0 | 14400 | 6400 | OK | BonusMoveSpeed=1.75m(0.5/k) |
| 25600 | Mid | +4800 | Escalating Exposure (s4) | 0 | 19200 | 6400 | OK | TechResist=17(3.5/k) |
| 32000 | Late | +6400 | Diviner's Kevlar (v4) | 0 | 19200 | 12800 | OK | TechPower=40(6.3/k) |
| 33600 | Late | +1600 | Superior Cooldown (s3) | 0 | 20800 | 12800 | OK | - |
| 38400 | Late | +4800 | Boundless Spirit (s4) | 0 | 25600 | 12800 | OK | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |
| 44800 | Late | +6400 | Mystic Reverb (s4) | 0 | 32000 | 12800 | OK | - |
| 51200 | Late | +6400 | Lightning Scroll (s4) | 0 | 38400 | 12800 | OK | BonusHealth=50(7.8/k) |
| 56000 | Late | +4800 | Spiritual Overflow (w4) | 6400 | 38400 | 11200 | FLAG LOW | TechPower=6(1.3/k) BonusHealth=90(18.8/k) BonusFireRate=25(5.2/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Tankbuster @14400 follows Mystic Burst. Four 6.4k buys from 32000 allowed.
- Lightning Scroll: Lightning Scroll bought in full (Mystic Slow not owned) @51200; Mystic Slow (1600, slow) is credited fully.
- Surge of Power: Surge of Power paid in full (3200 @20800): Extra Spirit was consumed by Improved Spirit @10400.

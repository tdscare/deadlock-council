# victor - Rizuhble's Aura Farming Victor (Spirit Victor)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spikes are good (spirit 5600 with only 800 diverted, health 9600: health before big damage as required for an in-your-face hero). Boundless Spirit is last (59200).

**Spike positions (first souls total at which invest >= 4800):**  {"s":5600,"v":9600} end 59200

## Flags (3)

1. **MED** - Boundless Spirit: Boundless (+4800, upgrade of owned Improved Spirit, 6.3 spirit/k plus 15% spirit power) is the LAST buy @59200, after Juggernaut (0 spirit), Spirit Burn (0 spirit) and Witchmail (2.2/k). Other spirit builds in this set buy it at 26-38k (median ~35k). Spirit Burn's 500 threshold also benefits from the extra spirit.
   - Minimal fix: Move Boundless to right after Scourge (36800 -> Boundless @41600, spirit 4.8k/health spikes unchanged).
2. **LOW** - Juggernaut: Juggernaut (+4800 @41600) in core; Kieran lists it as a Slot-locked upgrade. Melee resist is plausible for Victor but it pays 0 spirit.
   - Minimal fix: Move to Slot locked with Healing Tempo or justify.
3. **LOW** - Torment Pulse: Gun invest is 0 for the whole build (never 4.8k). Cheapest way if wanted: HV -> Opening Rounds + Monster Rounds -> Cultist Sacrifice = 4800.
   - Minimal fix: Policy call: spirit-aura Victor may skip gun entirely.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Regen (v1) | 0 | 0 | 800 | OK | BonusHealthRegen=2.5(3.1/k) |
| 1600 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 800 | OK | TechPower=10(12.5/k) |
| 2400 | Early | +800 | Improved Spirit (s2) | 0 | 1600 | 800 | OK | TechPower=18(22.5/k) BonusHealth=75(93.8/k) |
| 5600 | Early | +3200 | Torment Pulse (s3) | 0 | 4800 | 800 | FLAG LOW | BonusHealth=100(31.3/k) |
| 6400 | Mid | +800 | Healing Booster (v2) | 0 | 4800 | 1600 | OK | BonusHealthRegen=3(3.8/k) |
| 8000 | Mid | +1600 | Spirit Lifesteal (v2) | 0 | 4800 | 3200 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 8800 | Mid | +800 | Sprint Boots (v1) | 0 | 4800 | 4000 | OK | - |
| 9600 | Mid | +800 | Enduring Speed (v2) | 0 | 4800 | 4800 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 11200 | Mid | +1600 | Mystic Vulnerability (s2) | 0 | 6400 | 4800 | OK | TechResist=8(5.0/k) |
| 12000 | Mid | +800 | Mystic Expansion (s1) | 0 | 7200 | 4800 | OK | - |
| 16800 | Mid | +4800 | Infuser (v4) | 0 | 7200 | 9600 | OK | TechPower=6(1.3/k) BonusHealth=100(20.8/k) TechResist=10(2.1/k) |
| 18400 | Mid | +1600 | Compress Cooldown (s2) | 0 | 8800 | 9600 | OK | - |
| 23200 | Mid | +4800 | Escalating Exposure (s4) | 0 | 13600 | 9600 | OK | TechResist=17(3.5/k) |
| 25600 | Mid | +2400 | Greater Expansion (s3) | 0 | 16000 | 9600 | OK | TechResist=10(4.2/k) |
| 28800 | Mid | +3200 | Warp Stone (v3) | 0 | 16000 | 12800 | OK | BulletResist=30(9.4/k) |
| 30400 | Mid | +1600 | Superior Cooldown (s3) | 0 | 17600 | 12800 | OK | - |
| 36800 | Late | +6400 | Scourge (s4) | 0 | 24000 | 12800 | OK | TechResist=40(6.3/k) BonusHealth=100(15.6/k) |
| 41600 | Late | +4800 | Juggernaut (v4) | 0 | 24000 | 17600 | FLAG LOW | BonusHealthRegen=8(1.7/k) BonusMoveSpeed=2.5m(0.5/k) |
| 48000 | Late | +6400 | Spirit Burn (s4) | 0 | 30400 | 17600 | OK | - |
| 54400 | Late | +6400 | Witchmail (v4) | 0 | 30400 | 24000 | OK | TechPower=14(2.2/k) TechResist=22(3.4/k) |
| 59200 | Late | +4800 | Boundless Spirit (s4) | 0 | 35200 | 24000 | FLAG MED | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Infuser (+4800 @16800) consumes the owned Spirit Lifesteal: correct credit. Escalating Exposure +4800 upgrades Mystic Vulnerability.
- Witchmail @54400 is late as required.

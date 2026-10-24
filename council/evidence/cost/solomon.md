# solomon - Rizuhble's Come Here My Pawns (AoE damage Solomon)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spirit and health spikes land (8000 / 12000). Gun never reaches 4.8k (1600 only). Core is the longest in the chunk (56000).

**Spike positions (first souls total at which invest >= 4800):**  {"s":8000,"v":12000} end 56000

## Flags (2)

1. **MED** - High-Velocity Rounds, Opening Rounds: Gun invest is a token 1600 (HV + Opening Rounds) that is never added to; Opening Rounds is sold for a counter. It also delays the spirit 4.8k: spirit lands @8000 although 4800 souls of spirit items (Extra Spirit, Improved Spirit, Compress, Superior Cooldown) would do it. Kieran wants every stat at 4.8k on most characters.
   - Minimal fix: Either (a) commit gun to 4.8k with a w3 (Hollow Point/Berserker, +3200) after Warp Stone, or (b) drop HV+Opening Rounds for spirit items (Mystic Burst/Improved Spirit first): spirit 4.8k @6400-ish and no token gun.
2. **LOW** - Echo Shard: Echo Shard is the 12th core item at 56000 (6400 for 5 spirit resist and 5 bullet resist, 0.8/k; value is the active only). Kieran: Echo Shard usually belongs in the rich box. Core is 56000 souls.
   - Minimal fix: Move Echo Shard to the rich box; end core at Divine Barrier (49600) with another stat item or leave 11 slots only if a cheaper 12th fits.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 1600 | Early | +800 | High-Velocity Rounds (w1) | 800 | 800 | 0 | FLAG MED | BaseAttackDamagePercent=8(10.0/k) |
| 2400 | Early | +800 | Opening Rounds (w2) | 1600 | 800 | 0 | FLAG MED | TechPower=7(8.8/k) BaseAttackDamagePercent=8(10.0/k) |
| 3200 | Early | +800 | Grit (v1) | 1600 | 800 | 800 | OK | - |
| 4000 | Early | +800 | Extra Stamina (v1) | 1600 | 800 | 1600 | OK | - |
| 4800 | Early | +800 | Improved Spirit (s2) | 1600 | 1600 | 1600 | OK | TechPower=18(22.5/k) BonusHealth=75(93.8/k) |
| 6400 | Early | +1600 | Compress Cooldown (s2) | 1600 | 3200 | 1600 | OK | - |
| 8000 | Early | +1600 | Superior Cooldown (s3) | 1600 | 4800 | 1600 | OK | - |
| 8800 | Mid | +800 | Mystic Expansion (s1) | 1600 | 5600 | 1600 | OK | - |
| 12000 | Mid | +3200 | Warp Stone (v3) | 1600 | 5600 | 4800 | OK | BulletResist=30(9.4/k) |
| 12800 | Mid | +800 | Guardian Ward (v2) | 1600 | 5600 | 5600 | OK | BonusMoveSpeed=2.75m(3.4/k) |
| 14400 | Mid | +1600 | Mystic Vulnerability (s2) | 1600 | 7200 | 5600 | OK | TechResist=8(5.0/k) |
| 15200 | Mid | +800 | Mystic Burst (s1) | 1600 | 8000 | 5600 | OK | - |
| 17600 | Mid | +2400 | Tankbuster (s3) | 1600 | 10400 | 5600 | OK | BonusHealth=50(20.8/k) |
| 20000 | Late | +2400 | Greater Expansion (s3) | 1600 | 12800 | 5600 | OK | TechResist=10(4.2/k) |
| 22400 | Late | +2400 | Stamina Mastery (v3) | 1600 | 12800 | 8000 | OK | - |
| 27200 | Late | +4800 | Escalating Exposure (s4) | 1600 | 17600 | 8000 | OK | TechResist=17(3.5/k) |
| 32000 | Late | +4800 | Boundless Spirit (s4) | 1600 | 22400 | 8000 | OK | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |
| 38400 | Late | +6400 | Spirit Burn (s4) | 1600 | 28800 | 8000 | OK | - |
| 44800 | Late | +6400 | Mystic Reverb (s4) | 1600 | 35200 | 8000 | OK | - |
| 49600 | Late | +4800 | Divine Barrier (v4) | 1600 | 35200 | 12800 | OK | BonusMoveSpeed=2.75m(0.6/k) |
| 56000 | Late | +6400 | Echo Shard (s4) | 1600 | 41600 | 12800 | FLAG LOW | TechResist=5(0.8/k) BulletResist=5(0.8/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Spirit invest crossings: 4.8k @8000, 6.4k @14400... Tankbuster @17600 comes after its Mystic Burst component. Spirit Burn @38400 follows Tankbuster (enabler first).
- Four 6400-class buys run from 38400 (Spirit Burn, Mystic Reverb, Divine Barrier +4800, Echo Shard): allowed after ~30k.
- Mystic Burst: Mystic Burst (800) is bought @15200 only as the stepping stone for Tankbuster @17600; fine, but it is the same T1 that other builds buy in lane for its immediate damage.

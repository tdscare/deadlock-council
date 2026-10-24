# venator - Rizuhble's Exorcism By Fist (Melee Venator)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** OK on timing: gun 4.8k @6400, health @10400; Crushing Fists is late (32000) and sits after its Melee Charge (4000). Spirit 4.8k only @27200.

**Spike positions (first souls total at which invest >= 4800):**  {"w":6400,"v":10400,"s":27200} end 46400

## Flags (2)

1. **LOW** - Juggernaut: Juggernaut (+4800 @46400: 25% melee resist, 50% slow resist, 8 regen, 0.5 move speed/k) is the 12th core item while Kieran puts Juggernaut in the Slot-locked box (tiny-gain expensive upgrade). Kit reason exists (melee resist for a melee hero) but the Slot-locked box holds only Transcendent Cooldown.
   - Minimal fix: Keep if justified by melee resist, else move to Slot locked and end core at Echo Shard.
2. **LOW** - Echo Shard: Echo Shard (6400, 0.8/k) in Late core @41600 for Gutshot only; Kieran: usually rich. Spirit items on Gutshot total 12.8k (Compress, Expansion, Superior, Greater, Echo).
   - Minimal fix: Move to rich if a better 12th item exists.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Melee Lifesteal (v1) | 0 | 0 | 800 | OK | - |
| 1600 | Early | +800 | Close Quarters (w1) | 800 | 0 | 800 | OK | - |
| 2400 | Early | +800 | Monster Rounds (w1) | 1600 | 0 | 800 | OK | - |
| 4000 | Early | +1600 | Melee Charge (w2) | 3200 | 0 | 800 | OK | BulletResist=6(3.8/k) |
| 6400 | Early | +2400 | Cultist Sacrifice (w3) | 5600 | 0 | 800 | OK | BonusHealth=50 (+4x ELevelUpBoons)(20.8/k) BaseAttackDamagePercent=10 (+0.8x ELevelUpBoons)(4.2/k) |
| 8000 | Early | +1600 | Battle Vest (v2) | 5600 | 0 | 2400 | OK | BulletResist=18(11.3/k) BaseAttackDamagePercent=18(11.3/k) BonusFireRate=7(4.4/k) |
| 10400 | Early | +2400 | Lifestrike (v3) | 5600 | 0 | 4800 | OK | BonusHealth=125(52.1/k) |
| 12800 | Early | +2400 | Point Blank (w3) | 8000 | 0 | 4800 | OK | BonusHealth=75(31.3/k) |
| 13600 | Mid | +800 | Sprint Boots (v1) | 8000 | 0 | 5600 | OK | - |
| 14400 | Mid | +800 | Enduring Speed (v2) | 8000 | 0 | 6400 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 16000 | Mid | +1600 | Compress Cooldown (s2) | 8000 | 1600 | 6400 | OK | - |
| 19200 | Mid | +3200 | Hunter's Aura (w3) | 11200 | 1600 | 6400 | OK | BonusHealth=100(31.3/k) |
| 20000 | Mid | +800 | Mystic Expansion (s1) | 11200 | 2400 | 6400 | OK | - |
| 23200 | Mid | +3200 | Warp Stone (v3) | 11200 | 2400 | 9600 | OK | BulletResist=30(9.4/k) |
| 24800 | Mid | +1600 | Superior Cooldown (s3) | 11200 | 4000 | 9600 | OK | - |
| 27200 | Mid | +2400 | Greater Expansion (s3) | 11200 | 6400 | 9600 | OK | TechResist=10(4.2/k) |
| 32000 | Late | +4800 | Crushing Fists (w4) | 16000 | 6400 | 9600 | OK | BulletResist=12(2.5/k) |
| 35200 | Late | +3200 | Spirit Resilience (v3) | 16000 | 6400 | 12800 | OK | TechResist=30(9.4/k) |
| 41600 | Late | +6400 | Echo Shard (s4) | 16000 | 12800 | 12800 | FLAG LOW | TechResist=5(0.8/k) BulletResist=5(0.8/k) |
| 46400 | Late | +4800 | Juggernaut (v4) | 16000 | 12800 | 17600 | FLAG LOW | BonusHealthRegen=8(1.7/k) BonusMoveSpeed=2.5m(0.5/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Melee Charge (T2, 4000) is held 28k souls before Crushing Fists but pays immediately (+10% melee, +25 heavy melee): fine. Crushing Fists is not a first item here.
- No fresh T2 after ~13k.

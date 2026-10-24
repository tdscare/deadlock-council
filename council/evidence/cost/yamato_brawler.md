# yamato_brawler - Rizuhble's Hook Line Sashimi (Brawler Yamato)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Gun 6400, health 9600 are timely; spirit 4.8k @32000. The melee-damage item arrives last.

**Spike positions (first souls total at which invest >= 4800):**  {"w":6400,"v":9600,"s":32000} end 38400

## Flags (4)

1. **MED** - Melee Charge: Melee Charge (T2 1600, +10% melee, +25 heavy melee) is bought @24800, after Hunter's Aura (w3), Express Shot (w3) and Berserker (w3), i.e. 9600 souls of bullet items first for a melee build. It is a free stepping stone (100% credited toward Crushing Fists) so buying it in Early/Mid costs 0 net. Crushing Fists stays at 29600 (not a first item).
   - Minimal fix: Move Melee Charge to right after Lifestrike (~10k).
2. **LOW** - Express Shot, High-Velocity Rounds: HV (800) + Express Shot (+2400) = 3200 for 8% weapon damage and a double shot (3.3% /k) at 17600-20000 in a melee build; HV is a fresh T1 at 17.6k.
   - Minimal fix: Kit check: drop for a spirit/melee stat item if the shot isn't used.
3. **LOW** - Colossus: Colossus bought in full (6400) vs yamato +5600: Extra Health (lane box) is sold, not upgraded.
   - Minimal fix: Keep the lane Extra Health and upgrade it (slots allow only if sold elsewhere).
4. **LOW** - Leech: Rich Leech sells Bullet Resist Shredder: spirit 4800 -> 3200.
   - Minimal fix: Sell something else.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Restorative Shot (w1) | 800 | 0 | 0 | OK | BaseAttackDamagePercent=6(7.5/k) |
| 1600 | Early | +800 | Melee Lifesteal (v1) | 800 | 0 | 800 | OK | - |
| 2400 | Early | +800 | Close Quarters (w1) | 1600 | 0 | 800 | OK | - |
| 4000 | Early | +1600 | Stalker (w2) | 3200 | 0 | 800 | OK | BonusHealth=50(31.3/k) BonusMoveSpeed=1.5m(0.9/k) |
| 4800 | Early | +800 | Grit (v1) | 3200 | 0 | 1600 | OK | - |
| 6400 | Early | +1600 | Recharging Rush (w2) | 4800 | 0 | 1600 | OK | BaseAttackDamagePercent=10(6.3/k) |
| 8800 | Early | +2400 | Lifestrike (v3) | 4800 | 0 | 4000 | OK | BonusHealth=125(52.1/k) |
| 9600 | Early | +800 | Extra Regen (v1) | 4800 | 0 | 4800 | OK | BonusHealthRegen=2.5(3.1/k) |
| 10400 | Mid | +800 | Healing Booster (v2) | 4800 | 0 | 5600 | OK | BonusHealthRegen=3(3.8/k) |
| 11200 | Mid | +800 | Spirit Strike (s1) | 4800 | 800 | 5600 | OK | - |
| 12800 | Mid | +1600 | Bullet Resist Shredder (s2) | 4800 | 2400 | 5600 | OK | BaseAttackDamagePercent=9(5.6/k) BulletResist=9(5.6/k) |
| 16000 | Mid | +3200 | Hunter's Aura (w3) | 8000 | 2400 | 5600 | OK | BonusHealth=100(31.3/k) |
| 16800 | Mid | +800 | Reactive Barrier (v2) | 8000 | 2400 | 6400 | OK | - |
| 17600 | Mid | +800 | High-Velocity Rounds (w1) | 8800 | 2400 | 6400 | FLAG LOW | BaseAttackDamagePercent=8(10.0/k) |
| 20000 | Mid | +2400 | Express Shot (w3) | 10400 | 2400 | 6400 | FLAG LOW | BaseAttackDamagePercent=8(3.3/k) |
| 23200 | Mid | +3200 | Berserker (w3) | 13600 | 2400 | 6400 | OK | BulletResist=8(2.5/k) |
| 24800 | Late | +1600 | Melee Charge (w2) | 15200 | 2400 | 6400 | FLAG MED | BulletResist=6(3.8/k) |
| 29600 | Late | +4800 | Crushing Fists (w4) | 19200 | 2400 | 6400 | OK | BulletResist=12(2.5/k) |
| 32000 | Late | +2400 | Spirit Snatch (s3) | 19200 | 4800 | 6400 | OK | BonusHealth=75(31.3/k) |
| 38400 | Late | +6400 | Colossus (v4) | 19200 | 4800 | 12800 | FLAG LOW | BaseAttackDamagePercent=15(2.3/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): I'm:Leech <- sell Bullet Resist Shredder: s 4800->3200 LOSES 4.8k

## Checked, no change needed

- Crushing Fists (+4800 @29600) comes after Melee Charge and gun 4.8k: correct timing.

# vindicta - Rizuhble's Drive-By Vindicta (Gun Vindicta)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Gun 4.8k @4800 (minimum), health 12800 (mobile hero, allowed). Spellslinger is poor value; Burst Fire lost its component.

**Spike positions (first souls total at which invest >= 4800):**  {"w":4800,"v":12800,"s":16000} end 46400
**Mercurial Magnum accounting:** final invest in-game slots: gun 25600 / spirit 9600 / vit 11200; Magnum counted as gun: gun 32000 / spirit 3200 / vit 11200

## Flags (2)

1. **MED** - Spellslinger: Spellslinger (w4 6400 @36800) BonusFireRate 11, up to 6 stacks, built only by casts; 1.7 fire rate/k, versus Spiritual Overflow 5.2/k, Blood Tribute 10.9/k. A gun Vindicta casts rarely.
   - Minimal fix: Replace with Spiritual Overflow/Ricochet-class item (rich) or move Spellslinger to rich.
2. **LOW** - Burst Fire, Swift Striker: Burst Fire pays 3200 in full because Swift Striker consumed the Rapid Rounds component; Swift Striker is later sold. Net waste 800.
   - Minimal fix: Skip Swift Striker (Rapid Rounds -> Burst Fire +2400).

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | High-Velocity Rounds (w1) | 800 | 0 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 2400 | Early | +1600 | Long Range (w2) | 2400 | 0 | 0 | OK | - |
| 3200 | Early | +800 | Sharpshooter (w3) | 3200 | 0 | 0 | OK | BaseAttackDamagePercent=10(12.5/k) BonusMoveSpeed=-0.7m(-0.9/k) |
| 4000 | Early | +800 | Rapid Rounds (w1) | 4000 | 0 | 0 | OK | BonusFireRate=9(11.3/k) |
| 4800 | Early | +800 | Extended Magazine (w1) | 4800 | 0 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 5600 | Early | +800 | Extra Charge (s1) | 4800 | 800 | 0 | OK | - |
| 7200 | Early | +1600 | Bullet Lifesteal (v2) | 4800 | 800 | 1600 | OK | BonusHealth=90(56.3/k) BaseAttackDamagePercent=6(3.8/k) |
| 9600 | Early | +2400 | Rapid Recharge (s3) | 4800 | 3200 | 1600 | OK | - |
| 12800 | Mid | +3200 | Counterspell (v3) | 4800 | 3200 | 4800 | OK | BonusMoveSpeed=1.75m(0.5/k) BonusHealth=50(15.6/k) |
| 13600 | Mid | +800 | Sprint Boots (v1) | 4800 | 3200 | 5600 | OK | - |
| 14400 | Mid | +800 | Enduring Speed (v2) | 4800 | 3200 | 6400 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 16000 | Mid | +1600 | Quicksilver Reload (s2) | 4800 | 4800 | 6400 | OK | BonusFireRate=10(6.3/k) |
| 16800 | Mid | +800 | Swift Striker (w2) | 5600 | 4800 | 6400 | FLAG LOW | BonusFireRate=20(25.0/k) |
| 17600 | Mid | +800 | Titanic Magazine (w2) | 6400 | 4800 | 6400 | OK | BaseAttackDamagePercent=14(17.5/k) |
| 19200 | Mid | +1600 | Spirit Lifesteal (v2) | 6400 | 4800 | 8000 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 24000 | Mid | +4800 | Mercurial Magnum (s4) | 6400 | 9600 | 8000 | OK | TechPower=7(1.5/k) BonusFireRate=22(4.6/k) |
| 27200 | Late | +3200 | Burst Fire (w3) | 9600 | 9600 | 8000 | FLAG LOW | BonusFireRate=10(3.1/k) BonusMoveSpeed=1.25m(0.4/k) |
| 30400 | Late | +3200 | Leech (v4) | 9600 | 9600 | 11200 | OK | TechPower=12(3.8/k) BaseAttackDamagePercent=12(3.8/k) BonusHealth=180(56.3/k) |
| 36800 | Late | +6400 | Spellslinger (w4) | 16000 | 9600 | 11200 | FLAG MED | BonusFireRate=11(1.7/k) |
| 40000 | Late | +3200 | Blood Tribute (w3) | 19200 | 9600 | 11200 | OK | TechResist=8(2.5/k) BonusFireRate=35(10.9/k) BonusMoveSpeed=2.0m(0.6/k) |
| 46400 | Late | +6400 | Lucky Shot (w4) | 25600 | 9600 | 11200 | OK | - |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Counterspell (v3 3200 @12800) lands the health 4.8k and is the first Mid buy as Kieran asks (pure gun Vindicta still needs Counterspell).
- Leech +3200 uses both stepping stones.
- Titanic Magazine, Swift Striker: Two sell-named T2s (Swift Striker, Titanic Magazine) hold slots; fine.

# victor_gun - Rizuhble's It's Alive And Armed (Gun Victor)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Gun 4.8k @5600 (800 diverted) and health @9600 are ideal. Spirit only counts via Mercurial Magnum. Two late-build cost issues.

**Spike positions (first souls total at which invest >= 4800):**  {"w":5600,"v":9600,"s":20800} end 51200
**Mercurial Magnum accounting:** final invest in-game slots: gun 27200 / spirit 9600 / vit 14400; Magnum counted as gun: gun 33600 / spirit 3200 / vit 14400

## Flags (4)

1. **MED** - Spellslinger: Spellslinger (w4 6400 @33600): BonusFireRate 11 with up to 6 stacks, built only by casting an ability/item in combat, 1.7 fire rate/k at one stack versus Frenzy 2.3/k, Spiritual Overflow 5.2/k. Victor gun casts few abilities.
   - Minimal fix: Replace with a higher fire-rate-per-soul item from the same box (e.g. Ricochet/Lucky Shot) or keep only if stacks are shown reachable.
2. **LOW** - Leech, Spiritual Overflow: Leech costs +4800 instead of +3200: its Spirit Lifesteal component was already consumed by Spiritual Overflow @27200, so only Bullet Lifesteal is credited (+1600 wasted). Overflow and Leech compete for the same component.
   - Minimal fix: Buy Leech before Overflow, or accept +1600 and say so; same issue in wraith.
3. **LOW** - Healing Tempo: Healing Tempo (+4800 @44800) is in Late core; Kieran treats it as a Slot-locked upgrade in most games (35 fire rate only when you or an ally is healed by an active heal, not lifesteal).
   - Minimal fix: Move to Slot locked unless Victor's active heals are shown to trigger it often.
4. **LOW** - Mercurial Magnum: Spirit 4.8k appears only through Magnum (Tech slot in the game files); under Kieran's rule that Magnum counts as gun, spirit is 1600-3200 and never 4.8k.
   - Minimal fix: Report accounting choice to Kieran; no fix needed if Magnum is treated as spirit.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | High-Velocity Rounds (w1) | 800 | 0 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 1600 | Early | +800 | Extra Regen (v1) | 800 | 0 | 800 | OK | BonusHealthRegen=2.5(3.1/k) |
| 2400 | Early | +800 | Opening Rounds (w2) | 1600 | 0 | 800 | OK | TechPower=7(8.8/k) BaseAttackDamagePercent=8(10.0/k) |
| 3200 | Early | +800 | Extended Magazine (w1) | 2400 | 0 | 800 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 4000 | Early | +800 | Titanic Magazine (w2) | 3200 | 0 | 800 | OK | BaseAttackDamagePercent=14(17.5/k) |
| 4800 | Early | +800 | Rapid Rounds (w1) | 4000 | 0 | 800 | OK | BonusFireRate=9(11.3/k) |
| 5600 | Early | +800 | Swift Striker (w2) | 4800 | 0 | 800 | OK | BonusFireRate=20(25.0/k) |
| 6400 | Mid | +800 | Healing Booster (v2) | 4800 | 0 | 1600 | OK | BonusHealthRegen=3(3.8/k) |
| 7200 | Mid | +800 | Sprint Boots (v1) | 4800 | 0 | 2400 | OK | - |
| 8000 | Mid | +800 | Enduring Speed (v2) | 4800 | 0 | 3200 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 9600 | Mid | +1600 | Bullet Lifesteal (v2) | 4800 | 0 | 4800 | OK | BonusHealth=90(56.3/k) BaseAttackDamagePercent=6(3.8/k) |
| 11200 | Mid | +1600 | Quicksilver Reload (s2) | 4800 | 1600 | 4800 | OK | BonusFireRate=10(6.3/k) |
| 14400 | Mid | +3200 | Berserker (w3) | 8000 | 1600 | 4800 | OK | BulletResist=8(2.5/k) |
| 16000 | Mid | +1600 | Compress Cooldown (s2) | 8000 | 3200 | 4800 | OK | - |
| 20800 | Mid | +4800 | Mercurial Magnum (s4) | 8000 | 8000 | 4800 | FLAG LOW | TechPower=7(1.5/k) BonusFireRate=22(4.6/k) |
| 22400 | Mid | +1600 | Spirit Lifesteal (v2) | 8000 | 8000 | 6400 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 27200 | Mid | +4800 | Spiritual Overflow (w4) | 14400 | 8000 | 4800 | FLAG LOW | TechPower=6(1.3/k) BonusHealth=90(18.8/k) BonusFireRate=25(5.2/k) |
| 33600 | Mid | +6400 | Spellslinger (w4) | 20800 | 8000 | 4800 | FLAG MED | BonusFireRate=11(1.7/k) |
| 38400 | Late | +4800 | Leech (v4) | 20800 | 8000 | 9600 | FLAG LOW | TechPower=12(2.5/k) BaseAttackDamagePercent=12(2.5/k) BonusHealth=180(37.5/k) |
| 40000 | Late | +1600 | Superior Cooldown (s3) | 20800 | 9600 | 9600 | OK | - |
| 44800 | Late | +4800 | Healing Tempo (v4) | 20800 | 9600 | 14400 | FLAG LOW | BonusFireRate=35(7.3/k) BonusMoveSpeed=1.25m(0.3/k) TechResist=10(2.1/k) BonusHealthRegen=6(1.3/k) |
| 51200 | Late | +6400 | Frenzy (w4) | 27200 | 9600 | 14400 | OK | BonusHealth=160(25.0/k) BonusFireRate=15(2.3/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Quicksilver Reload (1600 @11200) is held 9.6k souls before Magnum: fine.
- Five untouched T2s (Opening Rounds, Titanic Magazine, Swift Striker, Enduring Speed...) are all sell/upgrade-named.

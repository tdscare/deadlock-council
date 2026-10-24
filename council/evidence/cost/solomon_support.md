# solomon_support - Rizuhble's Protect The King (Support Solomon)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Base build lands all three 4.8k (spirit 8800, health 11200, gun 18400 via Heroic Aura). The "Swap for Heroic Aura: Knockdown" box breaks the gun 4.8k (HIGH).

**Spike positions (first souls total at which invest >= 4800):**  {"s":8800,"v":11200,"w":18400} end 41600

## Flags (2)

1. **HIGH** - Heroic Aura: SWAP RE-WALK. Base: gun 1600 (HV+OR) + Heroic Aura 3200 = 4800 @18400. With Knockdown (Tech, spirit) instead: gun stays 1600 for the whole build (4.8k never), spirit jumps 4800 -> 8000 @18400 (and 19200 at the end). A swap into a different colour; also not the same job (Heroic Aura = team bullet resist + fire rate, Knockdown = single-target stun). Walk with Knockdown: spirit 4.8k @8800, health @11200, gun NEVER; end 41600.
   - Minimal fix: Make the swap a gun-colour T3 with the same 3200 cost (Hollow Point or Berserker; re-walked: spirit @8800, health @11200, gun @18400 unchanged) when the team has no gun carries, and move Knockdown to the Counters box ("flyers keep getting away") where it sells Enchanter's Emblem.
2. **LOW** - Opening Rounds: Rich box "Refresher - Sell Opening Rounds for this" drops gun from 4800 to 3200 and loses the gun 4.8k (and the Heroic Aura spike) the build just paid 3200 for.
   - Minimal fix: Make Refresher sell a non-gun item (e.g. Trophy Collector or Enchanter's Emblem).

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 1600 | Early | +800 | Healing Rite (v1) | 0 | 800 | 800 | OK | - |
| 2400 | Early | +800 | High-Velocity Rounds (w1) | 800 | 800 | 800 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 3200 | Early | +800 | Opening Rounds (w2) | 1600 | 800 | 800 | FLAG LOW | TechPower=7(8.8/k) BaseAttackDamagePercent=8(10.0/k) |
| 4000 | Early | +800 | Grit (v1) | 1600 | 800 | 1600 | OK | - |
| 4800 | Early | +800 | Extra Stamina (v1) | 1600 | 800 | 2400 | OK | - |
| 5600 | Early | +800 | Improved Spirit (s2) | 1600 | 1600 | 2400 | OK | TechPower=18(22.5/k) BonusHealth=75(93.8/k) |
| 7200 | Early | +1600 | Compress Cooldown (s2) | 1600 | 3200 | 2400 | OK | - |
| 8800 | Mid | +1600 | Superior Cooldown (s3) | 1600 | 4800 | 2400 | OK | - |
| 11200 | Mid | +2400 | Healing Nova (v3) | 1600 | 4800 | 4800 | OK | - |
| 12800 | Mid | +1600 | Healing Booster (v2) | 1600 | 4800 | 6400 | OK | BonusHealthRegen=3(1.9/k) |
| 13600 | Mid | +800 | Sprint Boots (v1) | 1600 | 4800 | 7200 | OK | - |
| 14400 | Mid | +800 | Trophy Collector (v2) | 1600 | 4800 | 8000 | OK | - |
| 15200 | Mid | +800 | Guardian Ward (v2) | 1600 | 4800 | 8800 | OK | BonusMoveSpeed=2.75m(3.4/k) |
| 18400 | Mid | +3200 | Heroic Aura (w3) | 4800 | 4800 | 8800 | FLAG HIGH | BonusFireRate=26(8.1/k) BulletResist=17(5.3/k) |
| 20000 | Mid | +1600 | Enchanter's Emblem (v2) | 4800 | 4800 | 10400 | OK | TechPower=15(9.4/k) TechResist=18(11.3/k) |
| 26400 | Late | +6400 | Cursed Relic (s4) | 4800 | 11200 | 10400 | OK | - |
| 29600 | Late | +3200 | Warp Stone (v3) | 4800 | 11200 | 13600 | OK | BulletResist=30(9.4/k) |
| 34400 | Late | +4800 | Boundless Spirit (s4) | 4800 | 16000 | 13600 | OK | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |
| 36800 | Late | +2400 | Stamina Mastery (v3) | 4800 | 16000 | 16000 | OK | - |
| 41600 | Late | +4800 | Divine Barrier (v4) | 4800 | 16000 | 20800 | OK | BonusMoveSpeed=2.75m(0.6/k) |

## Swap / reorder boxes re-walked

Boxes found: Swap for Heroic Aura. Results are in the flags above (re-walk numbers quoted there).

Sell-for checks (counters and rich boxes): I'm:Refresher <- sell Opening Rounds: w 4800->3200 LOSES 4.8k

## Checked, no change needed

- Healing Nova (+2400) lands the health 4.8k right after the spirit 4.8k: good for a support.
- Trophy Collector (+800 over Sprint Boots) @14400: right for a pure support per Kieran.
- Slot-locked Healing Tempo (+4800, 35 fire rate) triggers off Nova/Rite casts (not lifesteal): ok.
- Stamina Mastery: Stamina Mastery (+2400 @36800) has no HP (2 stamina, 18% stamina CDR); fine as a late upgrade of Extra Stamina but it is only vitality invest.

# violet - Rizuhble's Bob Ross Has A Glock (Gun hybrid Violet)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Good: spirit 6400, gun 9600, health 14400 with two damage spikes first. Mercurial Magnum is bought straight (no Quicksilver) as Kieran specified. Low flags only.

**Spike positions (first souls total at which invest >= 4800):**  {"s":6400,"w":9600,"v":14400} end 43200
**Mercurial Magnum accounting:** final invest in-game slots: gun 4800 / spirit 28800 / vit 9600; Magnum counted as gun: gun 11200 / spirit 22400 / vit 9600

## Flags (2)

1. **LOW** - Healbane, Enchanter's Emblem: Healbane (1600, 0 HP, 4.4 spirit/k) and Emblem (1600, no HP) put 3200 of the health 4.8k into items with no HP; Healbane is also sold for Escalating Exposure. The health 4.8k @14400 would otherwise come from Extra Health/Fortitude (210 / 375 HP).
   - Minimal fix: Optional: Healbane -> Extra Health + Fortitude path if more HP is wanted.
2. **LOW** - Opening Rounds: All six counters sell Opening Rounds: gun drops 4800 -> 3200 and the gun 4.8k is lost in the game's own accounting (Magnum counted as gun keeps it at 11200).
   - Minimal fix: Make counters sell Recharging Rush or Mystic Shot instead, or confirm Magnum counts as gun.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Extra Spirit (s1) | 0 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 1600 | Early | +800 | High-Velocity Rounds (w1) | 800 | 800 | 0 | OK | BaseAttackDamagePercent=8(10.0/k) |
| 2400 | Early | +800 | Opening Rounds (w2) | 1600 | 800 | 0 | FLAG LOW | TechPower=7(8.8/k) BaseAttackDamagePercent=8(10.0/k) |
| 3200 | Early | +800 | Extra Charge (s1) | 1600 | 1600 | 0 | OK | - |
| 5600 | Early | +2400 | Surge of Power (s3) | 1600 | 4000 | 0 | OK | BonusMoveSpeed=1.75m(0.7/k) |
| 6400 | Early | +800 | Mystic Burst (s1) | 1600 | 4800 | 0 | OK | - |
| 8000 | Early | +1600 | Mystic Shot (w2) | 3200 | 4800 | 0 | OK | - |
| 9600 | Early | +1600 | Recharging Rush (w2) | 4800 | 4800 | 0 | OK | BaseAttackDamagePercent=10(6.3/k) |
| 11200 | Mid | +1600 | Enchanter's Emblem (v2) | 4800 | 4800 | 1600 | FLAG LOW | TechPower=15(9.4/k) TechResist=18(11.3/k) |
| 12800 | Mid | +1600 | Healbane (v2) | 4800 | 4800 | 3200 | FLAG LOW | TechPower=7(4.4/k) |
| 14400 | Mid | +1600 | Spirit Lifesteal (v2) | 4800 | 4800 | 4800 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 16000 | Mid | +1600 | Improved Spirit (s2) | 4800 | 6400 | 4800 | OK | TechPower=18(11.3/k) BonusHealth=75(46.9/k) |
| 22400 | Late | +6400 | Mercurial Magnum (s4) | 4800 | 12800 | 4800 | OK | TechPower=7(1.1/k) BonusFireRate=22(3.4/k) |
| 24800 | Late | +2400 | Rapid Recharge (s3) | 4800 | 15200 | 4800 | OK | - |
| 29600 | Late | +4800 | Boundless Spirit (s4) | 4800 | 20000 | 4800 | OK | TechPower=30(6.3/k) BonusHealth=75(15.6/k) |
| 32000 | Late | +2400 | Tankbuster (s3) | 4800 | 22400 | 4800 | OK | BonusHealth=50(20.8/k) |
| 38400 | Late | +6400 | Spirit Burn (s4) | 4800 | 28800 | 4800 | OK | - |
| 43200 | Late | +4800 | Infuser (v4) | 4800 | 28800 | 9600 | OK | TechPower=6(1.3/k) BonusHealth=100(20.8/k) TechResist=10(2.1/k) |

## Swap / reorder boxes re-walked

No Swap / Instead of / reorder boxes in this build.

Sell-for checks (counters and rich boxes): Counters:Spirit Resilience <- sell Opening Rounds: w 4800->3200 LOSES 4.8k
   Counters:Bullet Resilience <- sell Opening Rounds: w 4800->3200 LOSES 4.8k
   Counters:Counterspell <- sell Opening Rounds: w 4800->3200 LOSES 4.8k
   Counters:Dispel Magic <- sell Opening Rounds: w 4800->3200 LOSES 4.8k
   Counters:Knockdown <- sell Opening Rounds: w 4800->3200 LOSES 4.8k
   Counters:Cursed Relic <- sell Opening Rounds: w 4800->3200 LOSES 4.8k

## Checked, no change needed

- Mystic Shot (@8000) is right after the spirit 4.8k (6400) as Kieran requires.
- Tankbuster @32000 precedes Spirit Burn @38400 (enabler first).

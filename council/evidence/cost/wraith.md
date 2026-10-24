# wraith - Rizuhble's Pick A Card Wraith

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Gun 4.8k @6400 and spirit @10400 are efficient; health 4.8k lands very late (21600). The "Lost lane?" reorder is questionable.

**Spike positions (first souls total at which invest >= 4800):**  {"w":6400,"s":10400,"v":21600} end 53600
**Mercurial Magnum accounting:** final invest in-game slots: gun 27200 / spirit 9600 / vit 16000; Magnum counted as gun: gun 33600 / spirit 3200 / vit 16000

## Flags (4)

1. **MED** - Ricochet: LOST-LANE REORDER RE-WALK. Moving Ricochet to right after Tesla Bullets puts a single 6400 buy @12800 (Kieran: no 6400s until ~20 min) and delays the spirit 4.8k from 10400 to 16800 (Quicksilver 14400, Surge 16800); health stays @21600. When behind, the player has the fewest souls, so the 6400 is the least affordable buy at that point.
   - Minimal fix: Remove the box (base order already buys Ricochet third) or reword to a cheaper reorder (Spirit Lifesteal/Bullet Lifesteal before Ricochet).
2. **LOW** - Enduring Speed: Health 4.8k only @21600: damage spikes then Ricochet (16800) and greens right after, which Kieran allows for farming builds, but it is the latest health spike in the chunk.
   - Minimal fix: If a safer game plan is wanted move Spirit Lifesteal + Bullet Lifesteal before Ricochet.
3. **LOW** - Leech, Spiritual Overflow: Leech costs +4800 (Spirit Lifesteal consumed by Spiritual Overflow @34400): 1600 more than with both components.
   - Minimal fix: Buy Leech first or accept.
4. **LOW** - Spirit Shredder, Reactive Barrier: Fresh T2 purchases at 23200-24800 (Reactive Barrier, Spirit Shredder). Spirit Shredder is the component of Spirit Rend (47200), Reactive Barrier of rich Indomitable, so both are upgraded/named, but they are fresh T2s in the Mid box.
   - Minimal fix: Move Spirit Shredder earlier (it is credited toward Spirit Rend anyway).

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Monster Rounds (w1) | 800 | 0 | 0 | OK | - |
| 1600 | Early | +800 | Rapid Rounds (w1) | 1600 | 0 | 0 | OK | BonusFireRate=9(11.3/k) |
| 2400 | Early | +800 | Extra Spirit (s1) | 1600 | 800 | 0 | OK | TechPower=10(12.5/k) |
| 3200 | Early | +800 | Swift Striker (w2) | 2400 | 800 | 0 | OK | BonusFireRate=20(25.0/k) |
| 6400 | Early | +3200 | Tesla Bullets (w3) | 5600 | 800 | 0 | OK | - |
| 8000 | Early | +1600 | Quicksilver Reload (s2) | 5600 | 2400 | 0 | OK | BonusFireRate=10(6.3/k) |
| 10400 | Early | +2400 | Surge of Power (s3) | 5600 | 4800 | 0 | OK | BonusMoveSpeed=1.75m(0.7/k) |
| 16800 | Mid | +6400 | Ricochet (w4) | 12000 | 4800 | 0 | FLAG MED | BonusFireRate=18(2.8/k) |
| 18400 | Mid | +1600 | Spirit Lifesteal (v2) | 11200 | 4800 | 1600 | OK | TechPower=6(3.8/k) BonusHealth=90(56.3/k) |
| 20000 | Mid | +1600 | Bullet Lifesteal (v2) | 11200 | 4800 | 3200 | OK | BonusHealth=90(56.3/k) BaseAttackDamagePercent=6(3.8/k) |
| 20800 | Mid | +800 | Sprint Boots (v1) | 11200 | 4800 | 4000 | OK | - |
| 21600 | Mid | +800 | Enduring Speed (v2) | 11200 | 4800 | 4800 | FLAG LOW | BonusMoveSpeed=2.0m(2.5/k) |
| 23200 | Mid | +1600 | Reactive Barrier (v2) | 11200 | 4800 | 6400 | FLAG LOW | - |
| 24800 | Mid | +1600 | Spirit Shredder (w2) | 12800 | 4800 | 6400 | FLAG LOW | - |
| 29600 | Late | +4800 | Mercurial Magnum (s4) | 12800 | 9600 | 6400 | OK | TechPower=7(1.5/k) BonusFireRate=22(4.6/k) |
| 34400 | Late | +4800 | Spiritual Overflow (w4) | 19200 | 9600 | 4800 | FLAG LOW | TechPower=6(1.3/k) BonusHealth=90(18.8/k) BonusFireRate=25(5.2/k) |
| 39200 | Late | +4800 | Leech (v4) | 19200 | 9600 | 9600 | FLAG LOW | TechPower=12(2.5/k) BaseAttackDamagePercent=12(2.5/k) BonusHealth=180(37.5/k) |
| 45600 | Late | +6400 | Inhibitor (v4) | 19200 | 9600 | 16000 | OK | BonusHealth=150(23.4/k) BaseAttackDamagePercent=10(1.6/k) |
| 47200 | Late | +1600 | Spirit Rend (w3) | 20800 | 9600 | 16000 | OK | BonusHealth=75(46.9/k) |
| 53600 | Late | +6400 | Silencer (w4) | 27200 | 9600 | 16000 | OK | TechResist=12(1.9/k) |

## Swap / reorder boxes re-walked

Boxes found: Lost lane?. Results are in the flags above (re-walk numbers quoted there).

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Tesla Bullets @6400 pays immediately for early farm (Kieran: Wraith early farm); its spirit scaling is minor (0.19x).
- Spirit Lifesteal note sells Monster Rounds: walked, gun 12000 -> 11200.

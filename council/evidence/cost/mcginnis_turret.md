# mcginnis_turret - Rizuhble's Tower Defence Nan (Turret McGinnis)

Cost-efficiency audit (round: cost agent, chunk 1). Souls figures come from the buy walk of data.js as of today (net cost = tier price minus owned components, sells in item notes applied). Invest columns are g(un)/s(pirit)/v(itality) in souls.

**Verdict:** Spirit 5600 / health 10400 are efficient, but the Heroic Aura swap breaks the spirit spike (HIGH) and Transcendent Cooldown sits in core.

**Spike positions (first souls total at which invest >= 4800):**  {"s":5600,"v":10400} end 45600

## Flags (3)

1. **HIGH** - Mystic Slow: SWAP RE-WALK. Heroic Aura (w3 3200) replaces Mystic Slow (s2 1600): spirit 4.8k moves from 5600 to 13600 (+8000 souls), health 4.8k from 10400 to 12000, gun ends 4000 (still short of 4.8k) and 3200 after Spirit Burn sells Monster Rounds; total +1600. Lightning Scroll (rich, upgrade of Mystic Slow) loses its component. Different job and colour.
   - Minimal fix: Make the swap replace Healbane instead (re-walked: spirit 5600, health 10400 unchanged, gun 4000) or drop the swap.
2. **MED** - Transcendent Cooldown: Transcendent Cooldown (+3200 @45600): +5% cooldown reduction over Superior Cooldown (1.6% per 1000 souls), the textbook Slot-locked item, but it is the 12th core item.
   - Minimal fix: Move it to Slot locked; core still has 12 slots (Boundless is the 12th).
3. **MED** - Boundless Spirit: Boundless bought in full (+6400 @42400); Improved Spirit (1600) not owned.
   - Minimal fix: Buy Improved Spirit early; Boundless +4800.

## Per item, in buy order (FLAG = see list above; OK = cost and timing fine)

Souls = cumulative core souls after the buy. +cost is the net price. Stat/k is stat per 1000 net souls.

| souls | box | +cost | item | gun | spirit | vit | status | stats |
|---|---|---|---|---|---|---|---|---|
| 800 | Early | +800 | Monster Rounds (w1) | 800 | 0 | 0 | OK | - |
| 1600 | Early | +800 | Extra Charge (s1) | 800 | 800 | 0 | OK | - |
| 3200 | Early | +1600 | Mystic Slow (s2) | 800 | 2400 | 0 | FLAG HIGH | BonusHealth=50(31.3/k) |
| 4000 | Early | +800 | Mystic Expansion (s1) | 800 | 3200 | 0 | OK | - |
| 5600 | Early | +1600 | Compress Cooldown (s2) | 800 | 4800 | 0 | OK | - |
| 7200 | Early | +1600 | Enchanter's Emblem (v2) | 800 | 4800 | 1600 | OK | TechPower=15(9.4/k) TechResist=18(11.3/k) |
| 8000 | Early | +800 | Extra Stamina (v1) | 800 | 4800 | 2400 | OK | - |
| 10400 | Early | +2400 | Stamina Mastery (v3) | 800 | 4800 | 4800 | OK | - |
| 12000 | Mid | +1600 | Mystic Vulnerability (s2) | 800 | 6400 | 4800 | OK | TechResist=8(5.0/k) |
| 13600 | Mid | +1600 | Healbane (v2) | 800 | 6400 | 6400 | OK | TechPower=7(4.4/k) |
| 16000 | Mid | +2400 | Rapid Recharge (s3) | 800 | 8800 | 6400 | OK | - |
| 16800 | Mid | +800 | Sprint Boots (v1) | 800 | 8800 | 7200 | OK | - |
| 17600 | Mid | +800 | Enduring Speed (v2) | 800 | 8800 | 8000 | OK | BonusMoveSpeed=2.0m(2.5/k) |
| 18400 | Mid | +800 | Mystic Regeneration (s1) | 800 | 9600 | 8000 | OK | BonusHealth=50(62.5/k) |
| 20000 | Mid | +1600 | Superior Cooldown (s3) | 800 | 11200 | 8000 | OK | - |
| 22400 | Mid | +2400 | Radiant Regeneration (s3) | 800 | 13600 | 8000 | OK | BonusMoveSpeed=1.75m(0.7/k) BonusHealth=90(37.5/k) |
| 27200 | Late | +4800 | Escalating Exposure (s4) | 800 | 18400 | 8000 | OK | TechResist=17(3.5/k) |
| 29600 | Late | +2400 | Greater Expansion (s3) | 800 | 20800 | 8000 | OK | TechResist=10(4.2/k) |
| 36000 | Late | +6400 | Spirit Burn (s4) | 0 | 27200 | 8000 | OK | - |
| 42400 | Late | +6400 | Boundless Spirit (s4) | 0 | 33600 | 8000 | FLAG MED | TechPower=30(4.7/k) BonusHealth=75(11.7/k) |
| 45600 | Late | +3200 | Transcendent Cooldown (s4) | 0 | 36800 | 8000 | FLAG MED | - |

## Swap / reorder boxes re-walked

Boxes found: Swap for Mystic Slow. Results are in the flags above (re-walk numbers quoted there).

Sell-for checks (counters and rich boxes): no sell drops a 4.8k spike

## Checked, no change needed

- Stamina Mastery: Health 4.8k @10400 uses Stamina Mastery (+2400, no HP).
- Monster Rounds: Only gun is 800 (Monster Rounds), sold for Spirit Burn.

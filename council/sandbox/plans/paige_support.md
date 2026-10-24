# paige_support (Paige) sandbox plan
Final 12: Trophy Collector, Opening Rounds, Rescue Beam, Knockdown, Rapid Recharge, Superior Cooldown, Divine Barrier, Greater Expansion, Superior Duration, Boundless Spirit, Cursed Relic, Lightning Scroll

## Uncertain slots (substitutes; every slot also tested with none)
- Rescue Beam -> Healing Nova, none: heal source
- Knockdown -> Silence Wave, Disarming Hex, none: peel tool
- Opening Rounds -> Swift Striker, none: note: sell for counter
- Cursed Relic -> Scourge, none: carry-curse
- Lightning Scroll -> Echo Shard, none: late

## Economy / early game
- Support: Healing Rite, Grit lane; Trophy Collector late (~12k). Low souls expected.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 2 0.5 > cast 3 0.6 > wait 1.2 > cast 1 0.6 > fire 3 > A:Knockdown > cast 4 1.0 > # PLANNED allyhp 40
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Score: ally survives same burst; ally bot must be damaged; plot armor duration 5s. Peel vs diving enemy (Knockdown).
- Stacks: Plot Armor barrier up/down.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Plot Armor barrier on ally (125 +1.5x spirit); Rallying Charge heal 125 +1.6x. Items: Healing Rite 300 +1.1x spirit over 20s, Rescue Beam 20%/0.2s, Guardian Ward, Divine Barrier.
- Heal items in build (auto from item data): Rescue Beam. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
paige_support_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), paige_support_heal, paige_support_timeline, paige_support_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

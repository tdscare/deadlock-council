# rem (Rem) sandbox plan
Final 12: Opening Rounds, Trophy Collector, Healing Nova, Rapid Recharge, Healing Booster, Echo Shard, Divine Barrier, Tankbuster, Heroic Aura, Superior Cooldown, Greater Expansion, Boundless Spirit

## Uncertain slots (substitutes; every slot also tested with none)
- Heroic Aura -> Spirit Rend, none: swap box
- Tankbuster -> Scourge, Silence Wave, none: carries Tag Along heal?
- Opening Rounds -> Swift Striker, none: Rem gun is weak: spike?
- Echo Shard -> Refresher, Superior Duration, none: jump back on
- Healing Booster -> Extra Regen, none: kit heal amp

## Economy / early game
- Support with passive helpers: Trophy Collector economy; Lil Helpers collect boxes. Low souls.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 1 0.4 > cast 1 0.4 > cast 2 0.5 > A:Divine Barrier > cast 3 0.3 > cast 4 2.0 > A:Echo Shard > # PLANNED allyhp 40
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Needs ally bot at ~40% HP; Naptime 1.9s channel through walls; stun by ult knocks off Tag Along (Unstoppable).
- Stacks: Pillow CD reduction 0/1/2 hits; hop count 1/3.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Tag Along: burst 15% missing HP +0.03x spirit then 42 +0.4x spirit hps for 2s to you and ally, once per ally hop; Lil Helpers heal burst; Pillow none. Items: Healing Nova 325 +6x spirit over 2s, Healing Booster (+20% amp), Divine Barrier, Guardian Ward barrier.
- Heal items in build (auto from item data): Healing Nova, Healing Booster. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
rem_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), rem_heal, rem_timeline, rem_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

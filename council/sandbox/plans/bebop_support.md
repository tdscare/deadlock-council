# bebop_support (Bebop) sandbox plan
Final 12: Bullet Resist Shredder, Trophy Collector, Fortitude, Heroic Aura, Spirit Snatch, Hunter's Aura, Veil Walker, Superior Cooldown, Boundless Spirit, Witchmail, Vortex Web, Unstoppable

## Uncertain slots (substitutes; every slot also tested with none)
- Heroic Aura -> Spirit Rend, none: only valid with gun heroes on team; test with an ally gun bot
- Hunter's Aura -> Healing Tempo, none: must stay within 15m of hooked victim
- Veil Walker -> Warp Stone, Majestic Leap, none: engage tool
- Bullet Resist Shredder -> Mystic Vulnerability, Spirit Shredder, none: team value only if ally damage is measured
- Trophy Collector -> Healing Booster, Enchanter's Emblem, none: economy item of a support

## Economy / early game
- Support: less souls than a carry; Trophy Collector (speed + passive souls) is the economy item. Extra Spirit > Spirit Strike early so the lane partner still gets the shred.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Unstoppable > cast 3 0.6 > cast 1 0.6 > fire 3 > cast 2 0.5 > cast 4 3.0
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Needs an ALLY bot gun hero shooting the same target (score = ally damage dealt with and without shred). Score team outcomes, not own dps. Hook cancelled by stun: Unstoppable listed. 40% accuracy for the ally too.
- Stacks: n/a (shred on/off, hook cooldown reset).
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Uppercut T3: 18% missing HP; Hyper Beam T3 lifesteal; uppercut/hook can target allies. Items: Fortitude regen (OOC), Veil Walker heal.
- Heal items in build (auto from item data): Veil Walker. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
bebop_support_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), bebop_support_heal, bebop_support_timeline, bebop_support_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

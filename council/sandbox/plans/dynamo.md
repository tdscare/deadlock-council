# dynamo (Dynamo) sandbox plan
Final 12: Rescue Beam, Headhunter, Trophy Collector, Rapid Recharge, Heroic Aura, Enchanter's Emblem, Warp Stone, Superior Cooldown, Greater Expansion, Superior Duration, Healing Tempo, Boundless Spirit

## Uncertain slots (substitutes; every slot also tested with none)
- Rescue Beam -> Healing Nova, Warp Stone, none: TEST_MATRIX: not to be rushed in lane; ult/ally survival score
- Heroic Aura -> Spirit Rend, none: valid only with gun heroes on team
- Headhunter -> Hollow Point, none: heal 4%/headshot but support hits few headshots
- Enchanter's Emblem -> Spirit Shielding, Reactive Barrier, none: minor spirit/regen item
- Healing Tempo -> Cursed Relic, Divine Barrier, none: only pays when Aurora heals allies in combat

## Economy / early game
- Support: Extra Charge + Headshot Booster so Kinetic Pulse still hurts early (stomps); Trophy Collector economy item (~8k). Lane damage must exist before Rescue Beam. Healing Rite/Extra Regen cover lane regen.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 3 5.0 > cast 1 0.6 > fire 2 > A:Warp Stone > cast 4 2.75 > # PLANNED allyhp 30 (ally starts at 30% hp, 4 bots in 8m)
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Score outcomes: does ally survive the same burst (bot Haze shooting ally + spirit hit) with Aurora vs Rescue Beam vs Nova; ult coverage (7m radius, 9m T1) with 1 vs 4 enemies. CC: Singularity pulled by stun: Unstoppable listed. Quantum Entanglement escapes.
- Stacks: Heal amp items 0/1/2; Healing Tempo condition (healed ally fire rate) on/off.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Rejuvenating Aurora 30 +0.4x spirit hps for 5s to self and allies within 8m (T3 +2.5% max HP/s, usable while moving); Rescue Beam item 20% per 0.2s; Healing Rite 300 +1.1x spirit over 20s; Healing Booster/Tempo amplify. Headhunter 4%/headshot.
- Heal items in build (auto from item data): Rescue Beam, Headhunter, Healing Tempo. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
dynamo_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), dynamo_heal, dynamo_timeline, dynamo_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

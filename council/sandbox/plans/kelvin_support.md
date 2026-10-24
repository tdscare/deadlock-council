# kelvin_support (Kelvin) sandbox plan
Final 12: Trophy Collector, Enchanter's Emblem, Healbane, Rapid Recharge, Superior Cooldown, Warp Stone, Boundless Spirit, Healing Tempo, Cursed Relic, Refresher, Greater Expansion, Superior Duration

## Uncertain slots (substitutes; every slot also tested with none)
- Trophy Collector -> Healing Booster, none: economy item; Healing Booster is a comp of Tempo already
- Enchanter's Emblem -> Spirit Shielding, none: tiny
- Healbane -> Spirit Resilience, none: note: sell for third counter
- Warp Stone -> Majestic Leap, none: engage vs dome range 8m
- Cursed Relic -> Scourge, Rescue Beam, none: who gets it
- Healing Tempo -> Divine Barrier, none: only with ally heal in combat

## Economy / early game
- Support: Trophy Collector (speed+souls) is the economy item; Extra Charge, Extra Regen, Healing Booster lane.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 1 0.5 > cast 2 1.0 > cast 3 3.0 > A:Warp Stone > cast 4 0.5 > fire 2 > # PLANNED allyhp 30
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Score: ally survival vs same burst with dome on ally; dome radius 10m; enemy bots running; CC: stun before dome (Unstoppable).
- Stacks: Heal amps 0/1/2 (Booster, Tempo).
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Frost Grenade heal 60 +0.8x spirit (T1 +30, T3 +0.9 scaling) in cloud; Frozen Shelter regen 90 +0.2x spirit (T2 65 more). Items: Healing Booster (+20%), Healing Tempo (+25%, +6 regen), Enchanter/Trophy regen OOC only.
- Heal items in build (auto from item data): Healbane, Healing Tempo. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
kelvin_support_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), kelvin_support_heal, kelvin_support_timeline, kelvin_support_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

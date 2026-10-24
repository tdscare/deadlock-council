# infernus_dash (Infernus) sandbox plan
Final 12: Swift Striker, Rapid Recharge, Enduring Speed, Dispel Magic, Superior Duration, Spiritual Overflow, Escalating Exposure, Unstoppable, Echo Shard, Spirit Burn, Indomitable, Cheat Death

## Uncertain slots (substitutes; every slot also tested with none)
- Swift Striker -> Active Reload, Recharging Rush, none: gun speed item on dash build
- Rapid Recharge -> Superior Cooldown, none: cleanse + extra charges
- Dispel Magic -> Counterspell, Silence Wave, none: dispel on Flame Dash; counters
- Superior Duration -> Greater Expansion, Superior Cooldown, none: trail duration
- Cheat Death -> Divine Barrier, Diviner's Kevlar, none: dash-into-ult survival

## Economy / early game
- Dash: Sprint Boots > Rapid Rounds; farms with Flame Dash trail on camps; no souls item.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Duration Extender > cast 2 1.0 > fire 2 > cast 1 0.6 > A:Echo Shard > cast 2 1.0 > fire 2 > A:Unstoppable > cast 4 0.5 > fire 4
- repeats 2x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Flame Dash charges 2 (T3). Dash into 5-bot ring then ult. Test vs stun to ult (Unstoppable popped first), vs enemies running away (does trail damage land).
- Stacks: Dash trail duration with/without Duration Extender; Echo Shard second dash.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Concussive Combustion T2 explosion lifesteal; Napalm T2 lifesteal on coated; Items: Spirit Lifesteal 13%, Spiritual Overflow, Dispel Magic heal 250 on use, Cheat Death. Reactive Barrier.
- Heal items in build (auto from item data): Dispel Magic, Spiritual Overflow. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
infernus_dash_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), infernus_dash_heal, infernus_dash_timeline, infernus_dash_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

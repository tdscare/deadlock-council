# dynamo_damage (Dynamo) sandbox plan
Final 12: Headhunter, Recharging Rush, Enduring Speed, Warp Stone, Tankbuster, Rapid Recharge, Superior Cooldown, Mercurial Magnum, Unstoppable, Mystic Reverb, Spirit Burn, Refresher

## Uncertain slots (substitutes; every slot also tested with none)
- Recharging Rush -> Swift Striker, Active Reload, none: doc says not early on slow-firing heroes; Dynamo gun rate low
- Headhunter -> Hollow Point, Burst Fire, none: gun item on a pulse build
- Mercurial Magnum -> Spiritual Overflow, Lucky Shot, none: gun/spirit active; Pulse is the damage source
- Warp Stone -> Majestic Leap, Fortitude, none: engage into ult
- Refresher -> Echo Shard, Superior Duration, none: late rich-box style slot

## Economy / early game
- Stomp: Headshot Booster, Mystic Burst, Extra Charge give a second pulse; needs pulse damage to farm waves (2 charges clears camps). No Cultist: pulse farms. 8k = Headshot Booster, Mystic Burst, Extra Charge, Headhunter; health spike with Tankbuster/Unstoppable ~14k.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Mystic Reverb > cast 1 0.5 > cast 1 0.5 > fire 2 > A:Warp Stone > A:Unstoppable > cast 4 2.75 > cast 1 0.5 > fire 2
- repeats 2x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Pulse = 2 charges with Extra Charge, Quicksilver Reload on pulse; Kinetic Pulse T2 15% bullet resist shred for gun. Test vs 0/realistic spirit resist. Ult pull range 7m; 5-bot ring. Unstoppable popped before ult.
- Stacks: Charges full/1/0 at start of rotation.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Kit: Aurora (only with ability 3, not skilled in this order). Items: Headhunter, Mystic Reverb 8% lifesteal (22% imbued ability), Spirit Burn anti-heal. Almost no sustain: test low HP survival.
- Heal items in build (auto from item data): Headhunter, Mystic Reverb. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
dynamo_damage_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), dynamo_damage_heal, dynamo_damage_timeline, dynamo_damage_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

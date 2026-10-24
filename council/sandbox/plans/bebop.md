# bebop (Bebop) sandbox plan
Final 12: Stalker, Bullet Resist Shredder, Headhunter, Enduring Speed, Veil Walker, Hunter's Aura, Spirit Snatch, Fortitude, Siphon Bullets, Vampiric Burst, Crippling Headshot, Witchmail

## Uncertain slots (substitutes; every slot also tested with none)
- Siphon Bullets -> Leech, Infuser, none: VB already in; second lifesteal source may be redundant
- Hunter's Aura -> Hollow Point, Burst Fire, none: aura only matters vs solo isolated carry; weapon alternative
- Stalker -> Swift Striker, Active Reload, none: T2 gun item; Stalker needs hook/uppercut to set up
- Veil Walker -> Warp Stone, Majestic Leap, none: gap closer vs walk-up; two valid engage items

## Economy / early game
- Gun bully: farms by gun + Sticky Bomb on camps (bomb stacks permanently); no souls item needed. Spirit Strike first (T1 that works on uppercut), Stalker + Headshot Booster ~4-5k, health spike Fortitude ~14k.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 3 0.6 > cast 1 0.6 > fire 3 > cast 3 0.6 > cast 2 0.5 > A:Vampiric Burst > fire 3 > cast 4 3.0
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Hook is cancelled by stun/silence: Unstoppable is in counters. Uppercut T2 gives +30% weapon damage 9s with 2x range and a spin-up: gun time must follow uppercut. Run vs a bot that dashes away after hook (Dynamo/Shiv) via planned 'enemy runs' op.
- Stacks: Bomb permanent stacks 0/5/20 (planned 'stack' op via kill credits); uppercut buff on/off.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Uppercut T3: restores 18% missing HP on hero hit and resets hook; Hyper Beam T3: 65% lifesteal of beam damage on heroes; sticky bomb none. Items: Headhunter (4% per headshot, scales spirit), Veil Walker (85 +8x spirit heal on veil), Siphon, VB, Fortitude regen OOC.
- Heal items in build (auto from item data): Headhunter, Veil Walker, Siphon Bullets, Vampiric Burst. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
bebop_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), bebop_heal, bebop_timeline, bebop_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

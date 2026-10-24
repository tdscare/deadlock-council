# ratking (Rat King) sandbox plan
Final 12: Opening Rounds, Cultist Sacrifice, Fortitude, Enduring Speed, Fleetfoot, Return Fire, Berserker, Ballistic Enchantment, Siphon Bullets, Superior Cooldown, Point Blank, Colossus, Witchmail  (13 items: Colossus note says sell Opening Rounds)

## Uncertain slots (substitutes; every slot also tested with none)
- Cultist Sacrifice -> none, Healing Rite: souls item; test at 8k (farm) not full
- Fleetfoot -> Kinetic Dash, Slowing Bullets, none: speed
- Return Fire -> Metal Skin, none: only vs real gun hero
- Siphon Bullets -> Leech, Vampiric Burst, none: sustain slot; max HP steal grows cape barrier
- Berserker -> Burst Fire, none: weapon damage scales grenade, fire rate doesn't

## Economy / early game
- Hard time farming (cape tank): Cultist Sacrifice ~8:00 (already in). Lane: Sprint Boots, Extra Health. Souls from Rat Swarm on waves is weak.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 3 0.5 > cast 2 0.5 > wait 1.5 > cast 1 0.5 > fire 3 > # PLANNED resetcd (grenade CD 26s, swarm 24s)
- repeats 2x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Need enemy shooting the player (Haze gun + spirit tick) to test Return Fire/cape barrier cap 250/hit; low HP start tests barrier not heal. Grenade scales weapon damage (+0.6x): no fire-rate items (see swaps).
- Stacks: Rats attached 0/2/5 (bullet resist shred) before grenade; barrier up/down.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: No lifesteal in kit; Royal Pestments is a barrier (max HP scaled), Return Fire deflects bullets. Items: Siphon Bullets (2.5% max HP), Fortitude, regen OOC, Colossus.
- Heal items in build (auto from item data): Siphon Bullets. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
ratking_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), ratking_heal, ratking_timeline, ratking_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

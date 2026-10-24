# ratking_grenade (Rat King) sandbox plan
Final 12: Cultist Sacrifice, Titanic Magazine, Battle Vest, Enduring Speed, Fortitude, Hollow Point, Ballistic Enchantment, Superior Cooldown, Greater Expansion, Echo Shard, Witchmail, Colossus

## Uncertain slots (substitutes; every slot also tested with none)
- Battle Vest -> Bullet Resist Shredder, none: swap box already: below 65% HP
- Hollow Point -> Burst Fire, none: weapon damage scales grenade
- Titanic Magazine -> Intensifying Magazine, none: weapon dmg source
- Echo Shard -> Mystic Reverb, Refresher, none: grenade second cast
- Cultist Sacrifice -> none: economy

## Economy / early game
- Grenade lobber: Cultist Sacrifice ~8:00; Extended/Monster Rounds scale grenade; Ballistic Enchantment.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 2 0.5 > wait 1.5 > cast 1 0.5 > fire 3 > cast 3 0.5 > fire 2 > # PLANNED resetcd
- repeats 2x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Order: rats first, then grenade (bullet resist shred); realistic resist 20%.
- Stacks: Rats 0/2/5 before grenade.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: No heal. Barrier from Royal Pestments; Battle Vest regen OOC; Hollow Point regen OOC; Fortitude.
- Heal items in build (auto from item data): none. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
ratking_grenade_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), ratking_grenade_heal, ratking_grenade_timeline, ratking_grenade_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

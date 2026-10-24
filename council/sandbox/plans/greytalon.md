# greytalon (Grey Talon) sandbox plan
Final 12: Enchanter's Emblem, Stamina Mastery, Tankbuster, Sharpshooter, Recharging Rush, Rapid Recharge, Surge of Power, Boundless Spirit, Superior Cooldown, Indomitable, Spirit Burn, Mystic Reverb

## Uncertain slots (substitutes; every slot also tested with none)
- Recharging Rush -> Swift Striker, Active Reload, none: note: sell it for counter; one-arrow hero fires slowly
- Sharpshooter -> Hollow Point, none: Charged shot not a bullet: does gun item scale it?
- Stamina Mastery -> Fortitude, none: stamina for arrow dodging
- Indomitable -> Unstoppable, Counterspell, none: CC answer: charged shot cancelled by stun
- Enchanter's Emblem -> Spirit Shielding, Healing Booster, none: tiny spirit item

## Economy / early game
- One-arrow: farms by arrow on camps/waves; Extra Charge gives 2 arrows; no souls item. 8k ~ Extra Charge, Mystic Burst, HV, Extra Spirit. Cultist Sacrifice optional only if lane is lost.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Surge of Power > A:Mystic Reverb > cast 3 0.5 > cast 1 2.5 > cast 1 2.5 > cast 4 2.0 > fire 1
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Hold arrow to full charge; accuracy: arrow hit rate 100/50/40 matters hugely (aim 'miss' variants). Spirit Snare (3) arms 2s then trips; Owl T3 kills under 22% HP: set enemy to 20%. Resist runs: Spirit Burn threshold. Infuser rejected (one hit).
- Stacks: Charge 0/half/full; arrows 1/2 (Extra Charge); owl-kill spirit stacks 0/1/3.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: None in kit except Rain of Arrows T3 (spirit/bullet lifesteal while airborne, not on this build's order). Items: Mystic Reverb 8% lifesteal (22% imbued ability), Indomitable barrier, regen OOC.
- Heal items in build (auto from item data): Mystic Reverb. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
greytalon_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), greytalon_heal, greytalon_timeline, greytalon_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

# greytalon_gun (Grey Talon) sandbox plan
Final 12: Swift Striker, Hollow Point, Enduring Speed, Stamina Mastery, Sharpshooter, Surge of Power, Burst Fire, Mercurial Magnum, Lucky Shot, Vampiric Burst, Ricochet, Spiritual Overflow

## Uncertain slots (substitutes; every slot also tested with none)
- Hollow Point -> Tesla Bullets, Berserker, none: gun hero: fire-rate item choices
- Swift Striker -> Active Reload, Recharging Rush, none: note says sell for a counter late
- Mercurial Magnum -> Capacitor, Glass Cannon, none: late slot: damage vs utility
- Spiritual Overflow -> Leech, Infuser, none: lifesteal duplicate with Bullet/Spirit Lifesteal and VB
- Vampiric Burst -> Leech, none: popped airborne; value if Rain of Arrows fires 5 split bullets

## Economy / early game
- Gun carry: HV>Rapid Rounds>Extra Stamina first, farm by gun; Rain of Arrows jump clears waves. No souls item.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Surge of Power > cast 2 0.3 > A:Vampiric Burst > fire 4 > fire 2 > cast 1 1.5 > fire 2 > cast 4 2.0
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Airborne window 4s: fire only in it and on ground separately; accuracy 40% hurts airborne multishot spread. VB popped airborne. Unstoppable vs Rain cancel (counters).
- Stacks: Airborne vs grounded; Lucky Shot proc; Ricochet bounce count with 1 vs 5 enemies.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Rain of Arrows T3 (this build skills 2 first): +30% bullet lifesteal, +30% spirit lifesteal, +30% evasion while airborne. Items: Bullet Lifesteal 13%, Spirit Lifesteal 13%, VB 13% (+70% active), Spiritual Overflow 13% + 10%, Hollow Point regen OOC. Many sources: needs source isolation.
- Heal items in build (auto from item data): Vampiric Burst, Spiritual Overflow. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
greytalon_gun_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), greytalon_gun_heal, greytalon_gun_timeline, greytalon_gun_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

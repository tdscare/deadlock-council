# infernus (Infernus) sandbox plan
Final 12: Improved Spirit, Toxic Bullets, Healbane, Swift Striker, Titanic Magazine, Superior Duration, Burst Fire, Spirit Rend, Escalating Exposure, Leech, Spiritual Overflow, Ricochet

## Uncertain slots (substitutes; every slot also tested with none)
- Leech -> Infuser, Vampiric Burst, none: Leech lifesteal 28% on gun AND spirit; Infuser needs separate spirit hits
- Toxic Bullets -> Hollow Point, Tesla Bullets, none: Healbane + Toxic both anti-heal; Napalm T3 too
- Titanic Magazine -> Intensifying Magazine, none: note: sell for a second counter
- Swift Striker -> Active Reload, Recharging Rush, none: fire rate vs Afterburn stack rate
- Healbane -> Spirit Rend, Spirit Lifesteal, none: Healbane+Spirit Rend both; threshold chain for Spirit Burn

## Economy / early game
- Gun burner: Afterburn builds from hits; Extra Spirit > Rapid Rounds. Napalm farms camps. No souls item; 8k = Extra Spirit, Rapid Rounds, Duration Extender, Improved Spirit(?).
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- fire 2 > cast 1 0.6 > fire 3 > cast 4 0.5 > fire 4 > cast 2 0.5 > fire 2
- repeats 2x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Afterburn builds per hit then refreshed by abilities: rotation fires first, ability refresh after. Needs enemy still for 17s buildup. Spirit threshold chain (Mystic Vulnerability>Spirit Rend>Escalating Exposure) tested vs spirit resist 0/15/30. 5-bot ring for Combustion radius 12m. Concussive stuns self? no.
- Stacks: Afterburn 0/50%/full; Napalm coated on/off.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Napalm T2: +15% lifesteal vs coated target; Concussive Combustion T2: explosion lifesteal; Afterburn none. Items: Bullet Lifesteal 13%, Spirit Lifesteal 13%, Spirit Rend 10%, Leech 28%/28%, Spiritual Overflow 13%+10%, Healbane 275 on kill.
- Heal items in build (auto from item data): Healbane, Spirit Rend, Leech, Spiritual Overflow. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
infernus_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), infernus_heal, infernus_timeline, infernus_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

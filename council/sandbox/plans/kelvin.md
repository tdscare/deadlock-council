# kelvin (Kelvin) sandbox plan
Final 12: Torment Pulse, Healing Booster, Healbane, Infuser, Rapid Recharge, Escalating Exposure, Superior Cooldown, Bullet Resilience, Boundless Spirit, Witchmail, Greater Expansion, Superior Duration

## Uncertain slots (substitutes; every slot also tested with none)
- Infuser -> Leech, Vampiric Burst, none: Infuser needs separate spirit hits: beam ticks every 0.1s
- Healbane -> Spirit Lifesteal, Spirit Rend, none: note: sell for counter
- Torment Pulse -> Spirit Shielding, Healing Rite, none: tank in-face item
- Bullet Resilience -> Spirit Resilience, Plated Armor, none: armor counters
- Healing Booster -> Extra Regen, none: amplifies kit heals

## Economy / early game
- Tanky damage: Extra Charge first (grenade charges); beam farms waves; Extra Spirit. Lane fixer Extra Health. No souls item.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Infuser > cast 1 0.5 > cast 1 0.5 > cast 3 5.0 > fire 1.5 > cast 4 0.5 > fire 2
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Beam slows more with time (2s to max): rotation holds beam 5s. Hold beam on target while being shot (low HP). 1 vs 5 enemies: beam T3 splits; grenade AoE. Frozen Shelter purge T3. Self-heal from own grenade: confirm.
- Stacks: Beam slow 0/1s/2s (max).
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Frost Grenade heal 60 +0.8x spirit to allies in cloud (self?), Frozen Shelter +90 regen +0.2x spirit regen within dome; Ice Path none. Items: Healing Booster amp, Infuser 70% imbue lifesteal, Spirit Lifesteal 13%, Healbane 275 on kill, Boundless/Improved regen OOC.
- Heal items in build (auto from item data): Healing Booster, Healbane, Infuser. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
kelvin_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), kelvin_heal, kelvin_timeline, kelvin_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

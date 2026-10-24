# seven (Seven) sandbox plan
Final 12: Arcane Surge, Surge of Power, Cultist Sacrifice, Healbane, Enduring Speed, Escalating Exposure, Superior Duration, Unstoppable, Superior Cooldown, Infuser, Greater Expansion, Diviner's Kevlar

## Uncertain slots (substitutes; every slot also tested with none)
- Infuser -> Leech, Vampiric Burst, none: Infuser pop in storm; separate spirit hits from storm ticks
- Healbane -> Counterspell, none: note: sell for counter
- Arcane Surge -> Duration Extender, none: imbue before 3
- Unstoppable -> Dispel Magic, Counterspell, none: Seven needs Unstoppable (TEST_MATRIX)
- Diviner's Kevlar -> Spirit Resilience, Witchmail, none: late armor

## Economy / early game
- Early farm: Monster Rounds, Surge of Power on Power Surge, Cultist Sacrifice (or Mystic Vulnerability on lost lane); ult build.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Arcane Surge > A:Surge of Power > cast 3 0.3 > fire 3 > cast 2 0.3 > cast 1 0.3 > cast 1 0.3 > fire 2 > A:Unstoppable > cast 4 7.0 > A:Infuser > fire 1
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Storm Cloud 7s: enemies in LOS only; test 1 vs 5 bots, bots running; enemy needs line of sight. Ability stuns (Static Charge 0.9s). Spirit resist 0/realistic.
- Stacks: Power Surge chain bounces vs 1/4/5 targets.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: None in kit. Items: Spirit Lifesteal 13%, Infuser 70% imbued + 13% passive, Healbane 275 on kill, Cultist regen OOC.
- Heal items in build (auto from item data): Healbane, Infuser. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
seven_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), seven_heal, seven_timeline, seven_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

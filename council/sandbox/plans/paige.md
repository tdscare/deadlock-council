# paige (Paige) sandbox plan
Final 12: Opening Rounds, Express Shot, Trophy Collector, Fortitude, Rapid Recharge, Tankbuster, Surge of Power, Guardian Ward, Greater Expansion, Superior Cooldown, Escalating Exposure, Boundless Spirit

## Uncertain slots (substitutes; every slot also tested with none)
- Opening Rounds -> Swift Striker, none: HV>Opening is her agreed gun spike
- Express Shot -> Burst Fire, none: gun hybrid; skills spells mostly
- Tankbuster -> Silence Wave, none: Dragon 90ish damage hits
- Fortitude -> Healing Rite, Spirit Shielding, none: health spike with Extra Health
- Guardian Ward -> Reactive Barrier, none: barrier/regen

## Economy / early game
- AoE farmer: Captivating Read + dragon clear waves/camps; Trophy Collector economy; speed: Sprint Boots. No Cultist.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Surge of Power > cast 3 0.6 > wait 1.2 > cast 1 0.6 > fire 3 > cast 2 0.5 > cast 4 1.0 > fire 2
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Immobilize 1s then dragon damage; enemies dash out? CC: stun on Captivating Read cast cancels it: Unstoppable. 5-bot ring for AoE; cooldown synergy (Compress on dragon).
- Stacks: n/a; rooted vs not rooted target.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Rallying Charge heals allies 125 +1.6x spirit; Plot Armor grants barrier (up to 125 +1.5x). No self heal in kit. Items: Guardian Ward barrier 250, Grit barrier, Fortitude (OOC regen).
- Heal items in build (auto from item data): none. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
paige_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), paige_heal, paige_timeline, paige_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

# danny (Danny) sandbox plan
Final 12: Opening Rounds, Sharpshooter, Enchanter's Emblem, Stamina Mastery, Tankbuster, Surge of Power, Greater Expansion, Diviner's Kevlar, Boundless Spirit, Superior Cooldown, Spirit Burn, Indomitable

## Uncertain slots (substitutes; every slot also tested with none)
- Sharpshooter -> Hollow Point, Burst Fire, none: only reason is Chimera landing scaling with weapon damage; unverified that Sharpshooter (range/long-shot item) raises that stat
- Stamina Mastery -> Fortitude, Warp Stone, none: no damage; slot is a movement/survival guess for the dive
- Spirit Burn -> Escalating Exposure, Mystic Reverb, none: burn needs a 500-damage threshold; dive hits are few big hits

## Economy / early game
- Dive hero, gun is secondary: farms with Strix Salvo (cheap 1) and gun; no kit income. Cultist Sacrifice not needed (8k reached by HV>Opening>Sharpshooter>Grit). Spirit spike (Improved Spirit onward) after the 4.8k gun spike.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Surge of Power > cast 1 0.8 > cast 3 2.0 > fire 2 > cast 2 4.5 > fire 1.5 > # PLANNED enemyhp 45 (ult bonus only under 50%) > cast 4 1.5 > fire 2
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- CC: stuns/silences cancel the flight; answers = Reactive Barrier, Indomitable, Unstoppable (counters box). Run once with enemy Haze putting a sleep dagger on Danny mid-flight. Dive hits need the target within ~8m radius on landing: use 1 bot at 350u and the 5-bot ring at 600u. Dive self-damage (10% max HP) is the low-HP stress.
- Stacks: Salvo marks 0/1/3 on target before the dive; ult at enemy HP 70%/45%/20%.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Chimera T2: heal 150 on hero hit (no self-damage); no other kit healing. Self-damage 10% max HP on Chimera if no hero hit.
- Heal items in build (auto from item data): none. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
danny_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), danny_heal, danny_timeline, danny_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

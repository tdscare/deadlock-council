# haze (Haze) sandbox plan
Final 12: Active Reload, Swift Striker, Titanic Magazine, Fortitude, Ricochet, Siphon Bullets, Burst Fire, Lucky Shot, Rapid Recharge, Vampiric Burst, Silencer, Healing Tempo

## Uncertain slots (substitutes; every slot also tested with none)
- Titanic Magazine -> Mercurial Magnum, Spiritual Overflow, none: note: sell late
- Active Reload -> Counterspell, none: note: sell late for counter
- Burst Fire -> Surge of Power, Blood Tribute, none: swap box
- Vampiric Burst -> Leech, none: swap box vs anti-heal
- Siphon Bullets -> Leech, none: build farm item, sell?

## Economy / early game
- Early farm then fight: Ricochet, Active Reload; 'farm until Siphon Bullets'. Haze farms by gun and Bullet Dance; Healing Booster core.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 2 0.3 > A:Vampiric Burst > A:Surge of Power > cast 1 0.3 > fire 4 > cast 4 3.5 > fire 2
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Smoke first (T3 lifesteal active) then dagger (doesn't break invis) then fire: fixation stacks 40 max, 3 per headshot; accuracy 40-50%; body/head mix. Disarm/CC: smoke dispels. Bullet Dance perfect accuracy.
- Stacks: Fixation 0/20/40; Siphon stacks 0/10/max.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Smoke Bomb T3: +50% bullet lifesteal 5s, dispel; Fixation none; Bullet Dance none. Items: Active Reload 16%, Bullet Lifesteal 13%, VB 13% (+70% active), Siphon 2.5% max HP, Healing Booster (+20% amp, +3 regen), Healing Tempo (+25%, +6 regen), Fortitude OOC. Many lifesteal sources: full source isolation.
- Heal items in build (auto from item data): Active Reload, Siphon Bullets, Vampiric Burst, Healing Tempo. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
haze_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), haze_heal, haze_timeline, haze_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.

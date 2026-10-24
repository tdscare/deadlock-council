# wraith (Wraith) sandbox plan
Abilities: Card Trick, Project Mind, Full Auto, Telekinesis  order [1, 1, 3, 2, 3, 4, 1, 3, 2, 2, 3, 1, 4, 4, 2, 4]
Core 12 used in scenarios (first 12 final items in build order): Monster Rounds, Swift Striker, Tesla Bullets, Surge of Power, Ricochet, Enduring Speed, Reactive Barrier, Mercurial Magnum, Spiritual Overflow, Leech, Inhibitor, Spirit Rend
Beyond 12 / optional (not loaded): Silencer

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Leech -> Infuser, Vampiric Burst, none: sustain slot
- Inhibitor -> Siphon Bullets, Armor Piercer, none: T4 slot
- Silencer -> Crippling Headshot, Lucky Shot, none: T4 slot
- Reactive Barrier -> Counterspell, Dispel Magic, none: Dispel stops slowing hex on teleport

## Economy
Card Trick/Full Auto farm well (rules: early farm then AoE gun); Cultist not needed.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Monster Rounds, Extra Spirit, Swift Striker, Tesla Bullets, Quicksilver Reload
- 12k (12000 spent): Monster Rounds, Swift Striker, Tesla Bullets, Quicksilver Reload, Surge of Power, Spirit Lifesteal
- 20k (20000 spent): Monster Rounds, Swift Striker, Tesla Bullets, Quicksilver Reload, Surge of Power, Ricochet, Spirit Lifesteal, Bullet Lifesteal
- 30k (29600 spent): Monster Rounds, Swift Striker, Tesla Bullets, Surge of Power, Ricochet, Spirit Lifesteal, Bullet Lifesteal, Enduring Speed, Reactive Barrier, Spirit Shredder, Mercurial Magnum
- full (53600 spent): Monster Rounds, Swift Striker, Tesla Bullets, Surge of Power, Ricochet, Enduring Speed, Reactive Barrier, Mercurial Magnum, Spiritual Overflow, Leech, Inhibitor, Spirit Rend
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Card Trick heart cards heal (HeartHeal, T2 +75/+0.5 scaling); Full Auto none
- Item Spiritual Overflow: AbilityLifestealPercentHero=13, BonusSpiritLifesteal=10
- Item Leech: AbilityLifestealPercentHero=28, BulletLifestealPercent=28
- Item Spirit Rend: AbilityLifestealPercentHero=10
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
fire 2, cast 3 0.2, fire 5, cast 1 0.3, cast 1 0.3, cast 1 0.3, cast 2 0.8, cast 4 1.3
Order reasons: imbue/proc items loaded on ability index (assumed) {'Surge of Power': 0, 'Quicksilver Reload': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Reactive Barrier (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- wraith_early.txt
- wraith_swap1.txt
- wraith_swap1_rev.txt
- wraith_swap2.txt
- wraith_swap2_rev.txt
- (skipped swap Silencer: not a final core item - beyond first 12 finals)
- wraith_swap4.txt
- wraith_swap4_rev.txt
- wraith_heal.txt
- wraith_heal_rev.txt

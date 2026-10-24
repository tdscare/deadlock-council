# viscous_damage (Viscous) sandbox plan
Abilities: Splatter, The Cube, Puddle Punch, Goo Ball  order [1, 1, 3, 2, 3, 4, 3, 1, 3, 1, 4, 4, 2, 2, 4, 2]
Core 12 used in scenarios (first 12 final items in build order): Lifestrike, Spirit Snatch, Tankbuster, Superior Cooldown, Spirit Shielding, Greater Expansion, Crushing Fists, Fortitude, Rapid Recharge, Boundless Spirit, Mystic Reverb, Spirit Burn

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Lifestrike -> Fury Trance, none: melee sustain
- Spirit Snatch -> Decay, Torment Pulse, none: spirit melee damage
- Fortitude -> Metal Skin, Spirit Resilience, none: survival
- Crushing Fists -> Colossus, none: T4 melee slot

## Economy
Splatter (1) clears waves; Trophy Collector/souls from support play; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Mystic Burst, Extra Spirit, Mystic Expansion, Spirit Strike, Compress Cooldown, Melee Lifesteal, Extra Health, Melee Charge
- 12k (12000 spent): Mystic Burst, Mystic Expansion, Spirit Strike, Compress Cooldown, Extra Health, Melee Charge, Improved Spirit, Lifestrike, Grit
- 20k (20000 spent): Mystic Expansion, Extra Health, Melee Charge, Improved Spirit, Lifestrike, Spirit Snatch, Tankbuster, Superior Cooldown, Spirit Shielding, Extra Charge
- 30k (29600 spent): Improved Spirit, Lifestrike, Spirit Snatch, Tankbuster, Superior Cooldown, Spirit Shielding, Extra Charge, Greater Expansion, Crushing Fists, Fortitude
- full (49600 spent): Lifestrike, Spirit Snatch, Tankbuster, Superior Cooldown, Spirit Shielding, Greater Expansion, Crushing Fists, Fortitude, Rapid Recharge, Boundless Spirit, Mystic Reverb, Spirit Burn
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: The Cube regen 40+0.3x spirit /s for 3s (+PostCubeBuff T3); Puddle Punch T2 +60% lifesteal on hit; Goo Ball none
- Item Lifestrike: LifestealHeal=120 (+1.75x spirit), LifestealHealPercent=35 (+0.5x spirit)
- Item Mystic Reverb: AbilityLifestealPercentHero=8, ImbueAbilityLifesteal=22
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 3 0.3, cast melee 0.6, cast melee 0.6, cast melee 0.6, cast 1 0.3, cast 2 0.4, cast 4 11, cast melee 0.6, cast melee 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 2, 'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- viscous_damage_early.txt
- viscous_damage_swap1.txt
- viscous_damage_swap1_rev.txt
- viscous_damage_swap2.txt
- viscous_damage_swap2_rev.txt
- viscous_damage_swap3.txt
- viscous_damage_swap3_rev.txt
- viscous_damage_swap4.txt
- viscous_damage_swap4_rev.txt
- viscous_damage_heal.txt
- viscous_damage_heal_rev.txt

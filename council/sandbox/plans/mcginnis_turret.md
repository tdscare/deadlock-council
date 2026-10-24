# mcginnis_turret (Forge) sandbox plan
Abilities: Mini Turret, Medicinal Specter, Spectral Wall, Heavy Barrage  order [1, 3, 1, 2, 1, 4, 1, 3, 3, 2, 2, 3, 2, 4, 4, 4]
Core 12 used in scenarios (first 12 final items in build order): Monster Rounds, Mystic Slow, Enchanter's Emblem, Stamina Mastery, Healbane, Rapid Recharge, Enduring Speed, Superior Cooldown, Radiant Regeneration, Escalating Exposure, Greater Expansion, Spirit Burn
Beyond 12 / optional (not loaded): Boundless Spirit

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Radiant Regeneration -> Restorative Locket, none: regen alongside Specter
- Mystic Slow -> Slowing Hex, none: utility
- Healbane -> Spirit Sap, none: T2 slot

## Economy
Turret + gun farms camps; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Monster Rounds, Extra Charge, Mystic Slow, Mystic Expansion, Compress Cooldown, Enchanter's Emblem, Extra Stamina
- 12k (12000 spent): Monster Rounds, Extra Charge, Mystic Slow, Mystic Expansion, Compress Cooldown, Enchanter's Emblem, Stamina Mastery, Improved Spirit
- 20k (20000 spent): Monster Rounds, Mystic Slow, Mystic Expansion, Compress Cooldown, Enchanter's Emblem, Stamina Mastery, Improved Spirit, Mystic Vulnerability, Healbane, Rapid Recharge, Enduring Speed, Mystic Regeneration
- 30k (28800 spent): Monster Rounds, Mystic Slow, Mystic Expansion, Enchanter's Emblem, Stamina Mastery, Improved Spirit, Healbane, Rapid Recharge, Enduring Speed, Superior Cooldown, Radiant Regeneration, Escalating Exposure
- full (42400 spent): Monster Rounds, Mystic Slow, Enchanter's Emblem, Stamina Mastery, Healbane, Rapid Recharge, Enduring Speed, Superior Cooldown, Radiant Regeneration, Escalating Exposure, Greater Expansion, Spirit Burn
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Medicinal Specter: 25+0.3x spirit regen /s for 6.5s in 6m (turret heal mult 1.0); no lifesteal in kit
- Item Radiant Regeneration: HealingPerCast=65 (+1.7x spirit), Regeneration=4 (+0.035x spirit), RegenerationDuration=7
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, cast 3 0.3, cast 2 0.3, fire 6, cast 4 8
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 0, 'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- mcginnis_turret_early.txt
- mcginnis_turret_swap1.txt
- mcginnis_turret_swap1_rev.txt
- mcginnis_turret_swap2.txt
- mcginnis_turret_swap2_rev.txt
- mcginnis_turret_swap3.txt
- mcginnis_turret_swap3_rev.txt
- mcginnis_turret_heal.txt
- mcginnis_turret_heal_rev.txt

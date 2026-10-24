# yamato (Yamato) sandbox plan
Abilities: Power Slash, Flying Slash, Crimson Slash, Shadow Transformation  order [1, 1, 3, 2, 2, 4, 2, 3, 3, 2, 1, 1, 3, 4, 4, 4]
Core 12 used in scenarios (first 12 final items in build order): Restorative Shot, Stalker, Spirit Snatch, Healing Booster, Lifestrike, Recharging Rush, Spirit Lifesteal, Torment Pulse, Boundless Spirit, Tankbuster, Mystic Reverb, Spirit Burn
Beyond 12 / optional (not loaded): Colossus

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Restorative Shot -> Kinetic Dash, Fleetfoot, none: first-bought dead-end item
- Colossus -> Juggernaut, Leech, none: T4 tank slot
- Torment Pulse -> Spirit Resilience, Fury Trance, none: aura vs defence

## Economy
Power Slash/Crimson Slash farm; grapple roams; no Cultist.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Restorative Shot, Melee Lifesteal, Spirit Strike, Stalker, Improved Spirit, Healing Booster, Extra Health
- 12k (12000 spent): Restorative Shot, Stalker, Improved Spirit, Spirit Snatch, Healing Booster, Lifestrike
- 20k (20000 spent): Restorative Shot, Stalker, Improved Spirit, Spirit Snatch, Healing Booster, Lifestrike, Recharging Rush, Spirit Lifesteal, Extra Health, Torment Pulse, Mystic Burst
- 30k (27200 spent): Restorative Shot, Stalker, Spirit Snatch, Healing Booster, Lifestrike, Recharging Rush, Spirit Lifesteal, Extra Health, Torment Pulse, Boundless Spirit, Tankbuster
- full (45600 spent): Restorative Shot, Stalker, Spirit Snatch, Healing Booster, Lifestrike, Recharging Rush, Spirit Lifesteal, Torment Pulse, Boundless Spirit, Tankbuster, Mystic Reverb, Spirit Burn
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Crimson Slash heals 55+1.04x spirit if it hits a hero (T2 +6% max HP); Shadow Transformation MaxHealthRegen 15 and heal on kill
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Lifestrike: LifestealHeal=120 (+1.75x spirit), LifestealHealPercent=35 (+0.5x spirit)
- Item Spirit Lifesteal: AbilityLifestealPercentHero=13
- Item Mystic Reverb: AbilityLifestealPercentHero=8, ImbueAbilityLifesteal=22
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 2 0.3, cast 3 0.4, cast melee 0.6, cast 1 1.5, cast 4 1.5, cast 1 1.5, cast 3 0.4, cast melee 0.6, cast melee 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {'Recharging Rush': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build:  (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- yamato_early.txt
- yamato_swap1.txt
- yamato_swap1_rev.txt
- (skipped swap Colossus: not a final core item - beyond first 12 finals)
- yamato_swap3.txt
- yamato_swap3_rev.txt
- yamato_heal.txt
- yamato_heal_rev.txt

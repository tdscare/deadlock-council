# yamato_brawler (Yamato) sandbox plan
Abilities: Power Slash, Flying Slash, Crimson Slash, Shadow Transformation  order [3, 3, 2, 1, 2, 4, 3, 3, 2, 4, 4, 1, 2, 4, 1, 1]
Core 12 used in scenarios (first 12 final items in build order): Restorative Shot, Close Quarters, Stalker, Recharging Rush, Lifestrike, Healing Booster, Bullet Resist Shredder, Hunter's Aura, Reactive Barrier, Express Shot, Berserker, Crushing Fists
Beyond 12 / optional (not loaded): Spirit Snatch, Colossus

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Bullet Resist Shredder -> Mystic Vulnerability, none: shred choice
- Berserker -> Hollow Point, none: gun item on melee hero (test at 0/1/max stacks)
- Reactive Barrier -> Debuff Reducer, none: stun answer
- Express Shot -> Point Blank, none: gun slot

## Economy
Power Slash/Crimson Slash farm; grapple roams; no Cultist.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Restorative Shot, Melee Lifesteal, Close Quarters, Stalker, Grit, Recharging Rush, Healing Booster
- 12k (12000 spent): Restorative Shot, Close Quarters, Stalker, Grit, Recharging Rush, Lifestrike, Melee Charge, Healing Booster
- 20k (19200 spent): Restorative Shot, Close Quarters, Stalker, Recharging Rush, Lifestrike, Melee Charge, Healing Booster, Spirit Strike, Bullet Resist Shredder, Hunter's Aura, Reactive Barrier, High-Velocity Rounds
- 30k (29600 spent): Restorative Shot, Close Quarters, Stalker, Recharging Rush, Lifestrike, Healing Booster, Spirit Strike, Bullet Resist Shredder, Hunter's Aura, Reactive Barrier, Express Shot, Berserker, Crushing Fists
- full (38400 spent): Restorative Shot, Close Quarters, Stalker, Recharging Rush, Lifestrike, Healing Booster, Bullet Resist Shredder, Hunter's Aura, Reactive Barrier, Express Shot, Berserker, Crushing Fists
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Crimson Slash heals 55+1.04x spirit if it hits a hero (T2 +6% max HP); Shadow Transformation MaxHealthRegen 15 and heal on kill
- Item Lifestrike: LifestealHeal=120 (+1.75x spirit), LifestealHealPercent=35 (+0.5x spirit)
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 2 0.3, cast melee 0.6, cast melee 0.6, cast 3 0.4, cast melee 0.6, cast 1 1.5, cast 4 1.5, cast 3 0.4, cast melee 0.6, cast melee 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Reactive Barrier (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- yamato_brawler_early.txt
- yamato_brawler_swap1.txt
- yamato_brawler_swap1_rev.txt
- yamato_brawler_swap2.txt
- yamato_brawler_swap2_rev.txt
- yamato_brawler_swap3.txt
- yamato_brawler_swap3_rev.txt
- yamato_brawler_swap4.txt
- yamato_brawler_swap4_rev.txt
- yamato_brawler_heal.txt
- yamato_brawler_heal_rev.txt

# mcginnis (Forge) sandbox plan
Abilities: Mini Turret, Medicinal Specter, Spectral Wall, Heavy Barrage  order [3, 2, 3, 1, 1, 1, 4, 2, 2, 3, 2, 3, 1, 4, 4, 4]
Core 12 used in scenarios (first 12 final items in build order): Monster Rounds, Intensifying Magazine, Swift Striker, Battle Vest, Enduring Speed, Escalating Resilience, Fleetfoot, Mercurial Magnum, Berserker, Vampiric Burst, Spiritual Overflow, Spirit Resilience

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Vampiric Burst -> Leech, Infuser, none: sustain
- Escalating Resilience -> Fortitude, none: survival
- Spiritual Overflow -> Frenzy, Crippling Headshot, none: T4
- Fleetfoot -> Kinetic Dash, none: mobility

## Economy
Turret + gun farms camps; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Monster Rounds, Extended Magazine, Intensifying Magazine, Swift Striker, Battle Vest, Quicksilver Reload
- 12k (11200 spent): Monster Rounds, Extended Magazine, Intensifying Magazine, Swift Striker, Battle Vest, Quicksilver Reload, Enduring Speed, Bullet Lifesteal
- 20k (20000 spent): Monster Rounds, Intensifying Magazine, Swift Striker, Battle Vest, Quicksilver Reload, Enduring Speed, Bullet Lifesteal, Escalating Resilience, Fleetfoot, Spirit Lifesteal, Berserker
- 30k (29600 spent): Monster Rounds, Intensifying Magazine, Swift Striker, Battle Vest, Enduring Speed, Escalating Resilience, Fleetfoot, Spirit Lifesteal, Mercurial Magnum, Berserker, Vampiric Burst
- full (37600 spent): Monster Rounds, Intensifying Magazine, Swift Striker, Battle Vest, Enduring Speed, Escalating Resilience, Fleetfoot, Mercurial Magnum, Berserker, Vampiric Burst, Spiritual Overflow, Spirit Resilience
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Medicinal Specter: 25+0.3x spirit regen /s for 6.5s in 6m (turret heal mult 1.0); no lifesteal in kit
- Item Vampiric Burst: ActiveBonusLifesteal=70, BulletLifestealPercent=13
- Item Spiritual Overflow: AbilityLifestealPercentHero=13, BonusSpiritLifesteal=10
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, cast 3 0.3, cast 2 0.3, fire 6, cast 4 8
Order reasons: imbue/proc items loaded on ability index (assumed) {'Quicksilver Reload': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build:  (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- mcginnis_early.txt
- mcginnis_swap1.txt
- mcginnis_swap1_rev.txt
- mcginnis_swap2.txt
- mcginnis_swap2_rev.txt
- mcginnis_swap3.txt
- mcginnis_swap3_rev.txt
- mcginnis_swap4.txt
- mcginnis_swap4_rev.txt
- mcginnis_heal.txt
- mcginnis_heal_rev.txt

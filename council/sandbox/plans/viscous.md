# viscous (Viscous) sandbox plan
Abilities: Splatter, The Cube, Puddle Punch, Goo Ball  order [1, 1, 2, 3, 2, 4, 2, 1, 2, 3, 4, 3, 4, 1, 3, 4]
Core 12 used in scenarios (first 12 final items in build order): Healing Booster, Improved Spirit, Rescue Beam, Trophy Collector, Rapid Recharge, Enchanter's Emblem, Superior Cooldown, Magic Carpet, Tankbuster, Greater Expansion, Echo Shard, Divine Barrier

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Rescue Beam -> Healing Nova, none: ally-save outcome (needs allies op)
- Magic Carpet -> Cursed Relic, none: T4 slot
- Divine Barrier -> Spellbreaker, Unstoppable, none: CC/burst answer

## Economy
Splatter (1) clears waves; Trophy Collector/souls from support play; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Healing Rite, Extra Charge, Compress Cooldown, Healing Booster, Improved Spirit, Mystic Burst, Sprint Boots
- 12k (12000 spent): Extra Charge, Compress Cooldown, Healing Booster, Improved Spirit, Mystic Burst, Rescue Beam, Trophy Collector, Mystic Expansion
- 20k (19200 spent): Healing Booster, Improved Spirit, Mystic Burst, Rescue Beam, Trophy Collector, Mystic Expansion, Guardian Ward, Rapid Recharge, Enchanter's Emblem, Superior Cooldown
- 30k (28000 spent): Healing Booster, Improved Spirit, Rescue Beam, Trophy Collector, Mystic Expansion, Guardian Ward, Rapid Recharge, Enchanter's Emblem, Superior Cooldown, Magic Carpet, Tankbuster
- full (41600 spent): Healing Booster, Improved Spirit, Rescue Beam, Trophy Collector, Rapid Recharge, Enchanter's Emblem, Superior Cooldown, Magic Carpet, Tankbuster, Greater Expansion, Echo Shard, Divine Barrier
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: The Cube regen 40+0.3x spirit /s for 3s (+PostCubeBuff T3); Puddle Punch T2 +60% lifesteal on hit; Goo Ball none
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Rescue Beam: HealPercentAmount=20
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 2 0.4, cast 1 0.3, cast 3 0.3, cast 1 0.3, fire 2, cast 4 11
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 2, 'Mystic Expansion': 0, 'Compress Cooldown': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge, Divine Barrier (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- viscous_early.txt
- viscous_swap1.txt
- viscous_swap1_rev.txt
- viscous_swap2.txt
- viscous_swap2_rev.txt
- viscous_swap3.txt
- viscous_swap3_rev.txt
- viscous_heal.txt
- viscous_heal_rev.txt

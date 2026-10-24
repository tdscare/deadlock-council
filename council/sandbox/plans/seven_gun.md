# seven_gun (Gigawatt) sandbox plan
Abilities: Lightning Ball, Static Charge, Power Surge, Storm Cloud  order [3, 3, 1, 1, 2, 3, 4, 3, 2, 4, 1, 4, 1, 2, 2, 4]
Core 12 used in scenarios (first 12 final items in build order): Opening Rounds, Cultist Sacrifice, Enchanter's Emblem, Duration Extender, Surge of Power, Enduring Speed, Tesla Bullets, Toxic Bullets, Escalating Exposure, Unstoppable, Spiritual Overflow, Boundless Spirit

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Toxic Bullets -> Spirit Rend, Alchemical Fire, none: gun DoT/heal-cut vs spirit-resist shred for Power Surge + Storm Cloud damage
- Cultist Sacrifice -> Monster Rounds, none: economy item: soul gain vs slot
- Unstoppable -> Divine Barrier, Spellbreaker, none: CC answer; run with knockdown/stun applied while Storm Cloud channels

## Economy
Weak early farmer; Lightning Ball (1) clears waves, Power Surge (3) needs Surge of Power/Duration Extender early. Cultist Sacrifice belongs ~8:00 (rules: Seven early farm then Cultist).
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Opening Rounds, Extra Spirit, Cultist Sacrifice, Enchanter's Emblem, Sprint Boots
- 12k (12000 spent): Opening Rounds, Cultist Sacrifice, Enchanter's Emblem, Duration Extender, Surge of Power, Sprint Boots
- 20k (19200 spent): Opening Rounds, Cultist Sacrifice, Enchanter's Emblem, Duration Extender, Surge of Power, Spirit Lifesteal, Enduring Speed, Improved Spirit, Tesla Bullets
- 30k (28800 spent): Opening Rounds, Cultist Sacrifice, Enchanter's Emblem, Duration Extender, Surge of Power, Spirit Lifesteal, Enduring Speed, Improved Spirit, Tesla Bullets, Toxic Bullets, Escalating Exposure
- full (44800 spent): Opening Rounds, Cultist Sacrifice, Enchanter's Emblem, Duration Extender, Surge of Power, Enduring Speed, Tesla Bullets, Toxic Bullets, Escalating Exposure, Unstoppable, Spiritual Overflow, Boundless Spirit
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none in kit (no self-heal on any ability); Storm Cloud T1 gives bullet resist only
- Item Spiritual Overflow: AbilityLifestealPercentHero=13, BonusSpiritLifesteal=10
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 3 0.3, cast 2 0.4, cast 1 0.5, fire 4, {A:Unstoppable}, cast 4 7
Order reasons: imbue/proc items loaded on ability index (assumed) {'Surge of Power': 2, 'Duration Extender': 2, 'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Unstoppable (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- seven_gun_early.txt
- seven_gun_swap1.txt
- seven_gun_swap1_rev.txt
- seven_gun_swap2.txt
- seven_gun_swap2_rev.txt
- seven_gun_swap3.txt
- seven_gun_swap3_rev.txt
- seven_gun_heal.txt
- seven_gun_heal_rev.txt

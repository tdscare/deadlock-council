# vindicta_sniper (Hornet) sandbox plan
Abilities: Stake, Flight, Crow Familiar, Assassinate  order [1, 1, 3, 2, 4, 4, 4, 3, 3, 2, 2, 1, 3, 4, 1, 2]
Core 12 used in scenarios (first 12 final items in build order): Rapid Recharge, Enduring Speed, Counterspell, Tankbuster, Surge of Power, Escalating Exposure, Diviner's Kevlar, Superior Cooldown, Boundless Spirit, Mystic Reverb, Lightning Scroll, Spiritual Overflow

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Lightning Scroll -> Refresher, Cursed Relic, none: T4
- Diviner's Kevlar -> Spellbreaker, Divine Barrier, none: spirit burst answer
- Spiritual Overflow -> Spellslinger, none: T4
- Counterspell -> Dispel Magic, none: answer

## Economy
Pure gun farm is fine from air with Flight; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (7200 spent): Mystic Burst, Rapid Recharge, Enduring Speed, Improved Spirit
- 12k (12000 spent): Mystic Burst, Rapid Recharge, Enduring Speed, Counterspell, Improved Spirit, Mystic Vulnerability
- 20k (19200 spent): Rapid Recharge, Enduring Speed, Counterspell, Improved Spirit, Mystic Vulnerability, Tankbuster, Spirit Lifesteal, Superior Cooldown
- 30k (27200 spent): Rapid Recharge, Enduring Speed, Counterspell, Improved Spirit, Tankbuster, Spirit Lifesteal, Surge of Power, Escalating Exposure, Superior Cooldown
- full (56000 spent): Rapid Recharge, Enduring Speed, Counterspell, Tankbuster, Surge of Power, Escalating Exposure, Diviner's Kevlar, Superior Cooldown, Boundless Spirit, Mystic Reverb, Lightning Scroll, Spiritual Overflow
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none in kit (Flight, Stake, Crow, Assassinate do not heal)
- Item Mystic Reverb: AbilityLifestealPercentHero=8, ImbueAbilityLifesteal=22
- Item Spiritual Overflow: AbilityLifestealPercentHero=13, BonusSpiritLifesteal=10
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 3 0.3, cast 1 0.4, cast 2 0.3, fire 4, cast 4 1.5, fire 2
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 0, 'Surge of Power': 3}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge, Counterspell (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- vindicta_sniper_early.txt
- vindicta_sniper_swap1.txt
- vindicta_sniper_swap1_rev.txt
- vindicta_sniper_swap2.txt
- vindicta_sniper_swap2_rev.txt
- vindicta_sniper_swap3.txt
- vindicta_sniper_swap3_rev.txt
- vindicta_sniper_swap4.txt
- vindicta_sniper_swap4_rev.txt
- vindicta_sniper_heal.txt
- vindicta_sniper_heal_rev.txt

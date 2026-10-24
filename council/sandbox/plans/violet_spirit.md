# violet_spirit (Artist) sandbox plan
Abilities: Living Ink, Flow State, Still Life, Abstract Landscape  order [1, 1, 3, 2, 3, 4, 1, 3, 1, 2, 2, 4, 4, 3, 2, 4]
Core 12 used in scenarios (first 12 final items in build order): Surge of Power, Healing Booster, Spirit Shielding, Radiant Regeneration, Enchanter's Emblem, Rapid Recharge, Tankbuster, Superior Cooldown, Escalating Exposure, Boundless Spirit, Spirit Burn, Infuser

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Radiant Regeneration -> Restorative Locket, none: regen item with Healing Booster
- Infuser -> Leech, none: last sustain slot
- Spirit Shielding -> Counterspell, none: spirit defence

## Economy
Living Ink bullets + Flow State clear waves; no Cultist needed unless lane is lost.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Extra Charge, Mystic Regeneration, Surge of Power, Healing Booster, Spirit Shielding
- 12k (12000 spent): Extra Charge, Mystic Regeneration, Surge of Power, Healing Booster, Spirit Shielding, Spirit Lifesteal, Improved Spirit, Mystic Burst
- 20k (20000 spent): Surge of Power, Healing Booster, Spirit Shielding, Spirit Lifesteal, Improved Spirit, Mystic Burst, Radiant Regeneration, Enchanter's Emblem, Rapid Recharge, Compress Cooldown
- 30k (25600 spent): Surge of Power, Healing Booster, Spirit Shielding, Spirit Lifesteal, Improved Spirit, Radiant Regeneration, Enchanter's Emblem, Rapid Recharge, Mystic Vulnerability, Tankbuster, Superior Cooldown
- full (46400 spent): Surge of Power, Healing Booster, Spirit Shielding, Radiant Regeneration, Enchanter's Emblem, Rapid Recharge, Tankbuster, Superior Cooldown, Escalating Exposure, Boundless Spirit, Spirit Burn, Infuser
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Still Life T2 health regen per collected sketch; Abstract Landscape T2 gives allies 25% ability lifesteal; Living Ink hits cut cooldowns (no heal)
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Radiant Regeneration: HealingPerCast=65 (+1.7x spirit), Regeneration=4 (+0.035x spirit), RegenerationDuration=7
- Item Infuser: AbilityLifestealPercentHero=70, AbilityLifestealPercentHeroPassive=13
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, fire 1.5, cast 2 0.3, cast 2 0.3, cast 3 2.6, fire 2, cast 4 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {'Surge of Power': 0, 'Extra Charge': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- violet_spirit_early.txt
- violet_spirit_swap1.txt
- violet_spirit_swap1_rev.txt
- violet_spirit_swap2.txt
- violet_spirit_swap2_rev.txt
- violet_spirit_swap3.txt
- violet_spirit_swap3_rev.txt
- violet_spirit_heal.txt
- violet_spirit_heal_rev.txt

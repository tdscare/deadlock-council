# violet (Artist) sandbox plan
Abilities: Living Ink, Flow State, Still Life, Abstract Landscape  order [1, 1, 3, 2, 1, 4, 1, 3, 3, 4, 4, 2, 2, 2, 3, 4]
Core 12 used in scenarios (first 12 final items in build order): Opening Rounds, Surge of Power, Mystic Shot, Recharging Rush, Enchanter's Emblem, Healbane, Mercurial Magnum, Rapid Recharge, Boundless Spirit, Tankbuster, Spirit Burn, Infuser

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Healbane -> Spirit Shielding, none: cheap T2 swap candidate vs kit-less sustain
- Mystic Shot -> Slowing Bullets, none: weapon-tree item that scales off spirit
- Infuser -> Leech, none: last sustain slot
- Rapid Recharge -> Counterspell, none: CC/cooldown slot

## Economy
Living Ink bullets + Flow State clear waves; no Cultist needed unless lane is lost.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Opening Rounds, Extra Charge, Surge of Power, Mystic Burst, Mystic Shot
- 12k (11200 spent): Opening Rounds, Extra Charge, Surge of Power, Mystic Burst, Mystic Shot, Recharging Rush, Enchanter's Emblem
- 20k (18400 spent): Opening Rounds, Surge of Power, Mystic Burst, Mystic Shot, Recharging Rush, Enchanter's Emblem, Healbane, Spirit Lifesteal, Improved Spirit, Rapid Recharge
- 30k (29600 spent): Opening Rounds, Surge of Power, Mystic Burst, Mystic Shot, Recharging Rush, Enchanter's Emblem, Healbane, Spirit Lifesteal, Mercurial Magnum, Rapid Recharge, Boundless Spirit
- full (43200 spent): Opening Rounds, Surge of Power, Mystic Shot, Recharging Rush, Enchanter's Emblem, Healbane, Mercurial Magnum, Rapid Recharge, Boundless Spirit, Tankbuster, Spirit Burn, Infuser
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Still Life T2 health regen per collected sketch; Abstract Landscape T2 gives allies 25% ability lifesteal; Living Ink hits cut cooldowns (no heal)
- Item Infuser: AbilityLifestealPercentHero=70, AbilityLifestealPercentHeroPassive=13
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, fire 1.5, cast 2 0.3, cast 2 0.3, cast 3 2.6, fire 2, cast 4 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {'Surge of Power': 0, 'Extra Charge': 0, 'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- violet_early.txt
- violet_swap1.txt
- violet_swap1_rev.txt
- violet_swap2.txt
- violet_swap2_rev.txt
- violet_swap3.txt
- violet_swap3_rev.txt
- violet_swap4.txt
- violet_swap4_rev.txt
- violet_heal.txt
- violet_heal_rev.txt

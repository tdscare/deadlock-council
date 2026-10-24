# mina (Vampirebat) sandbox plan
Abilities: Rake, Sanguine Retreat, Love Bites, Nox Nostra  order [3, 1, 1, 2, 1, 3, 4, 3, 1, 2, 2, 3, 2, 4, 4, 4]
Core 12 used in scenarios (first 12 final items in build order): Stamina Mastery, Reactive Barrier, Dispel Magic, Swift Striker, Spirit Sap, Boundless Spirit, Tankbuster, Spirit Burn, Superior Cooldown, Greater Expansion, Infuser, Mercurial Magnum

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Dispel Magic -> Counterspell, none: CC/spirit answer
- Infuser -> Leech, Vampiric Burst, none: sustain
- Mercurial Magnum -> Refresher, none: last slot
- Spirit Sap -> Slowing Hex, none: T2 utility

## Economy
Rake clears troopers (heals per kill) and Love Bites bursts; no Cultist expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Mystic Burst, Quicksilver Reload, Mystic Expansion, Improved Spirit, Extra Stamina, Reactive Barrier, Rapid Rounds
- 12k (11200 spent): Mystic Burst, Quicksilver Reload, Mystic Expansion, Improved Spirit, Stamina Mastery, Reactive Barrier, Swift Striker
- 20k (19200 spent): Mystic Burst, Quicksilver Reload, Mystic Expansion, Improved Spirit, Stamina Mastery, Reactive Barrier, Dispel Magic, Swift Striker, Spirit Sap, Compress Cooldown, Spirit Lifesteal
- 30k (28000 spent): Quicksilver Reload, Mystic Expansion, Stamina Mastery, Reactive Barrier, Dispel Magic, Swift Striker, Spirit Sap, Spirit Lifesteal, Boundless Spirit, Tankbuster, Superior Cooldown
- full (46400 spent): Stamina Mastery, Reactive Barrier, Dispel Magic, Swift Striker, Spirit Sap, Boundless Spirit, Tankbuster, Spirit Burn, Superior Cooldown, Greater Expansion, Infuser, Mercurial Magnum
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Rake: heal per kill 25+0.3x spirit and missing-health damage (steal-life ability, hit lifesteal value NOT verified from data); Love Bites burst adds no heal
- Item Infuser: AbilityLifestealPercentHero=70, AbilityLifestealPercentHeroPassive=13
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
fire 2, cast 1 0.5, fire 1.5, cast 2 0.7, fire 2, cast 4 3
Order reasons: imbue/proc items loaded on ability index (assumed) {'Quicksilver Reload': 0, 'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Reactive Barrier, Dispel Magic (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- mina_early.txt
- mina_swap1.txt
- mina_swap1_rev.txt
- mina_swap2.txt
- mina_swap2_rev.txt
- mina_swap3.txt
- mina_swap3_rev.txt
- mina_swap4.txt
- mina_swap4_rev.txt
- mina_heal.txt
- mina_heal_rev.txt

# vindicta (Hornet) sandbox plan
Abilities: Stake, Flight, Crow Familiar, Assassinate  order [3, 3, 2, 2, 1, 2, 4, 3, 4, 2, 3, 1, 1, 4, 4, 1]
Core 12 used in scenarios (first 12 final items in build order): Sharpshooter, Rapid Recharge, Counterspell, Enduring Speed, Swift Striker, Titanic Magazine, Mercurial Magnum, Burst Fire, Leech, Ricochet, Blood Tribute, Lucky Shot

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Leech -> Infuser, Vampiric Burst, none: sustain
- Blood Tribute -> Glass Cannon, Lucky Shot, none: T3-4 gun slot
- Ricochet -> Crippling Headshot, none: T4
- Counterspell -> Dispel Magic, Metal Skin, none: answers

## Economy
Pure gun farm is fine from air with Flight; Cultist not expected.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Sharpshooter, Rapid Rounds, Extended Magazine, Extra Charge, Bullet Lifesteal, Sprint Boots
- 12k (12000 spent): Sharpshooter, Extended Magazine, Bullet Lifesteal, Rapid Recharge, Enduring Speed, Swift Striker
- 20k (19200 spent): Sharpshooter, Bullet Lifesteal, Rapid Recharge, Counterspell, Enduring Speed, Quicksilver Reload, Swift Striker, Titanic Magazine, Spirit Lifesteal
- 30k (27200 spent): Sharpshooter, Bullet Lifesteal, Rapid Recharge, Counterspell, Enduring Speed, Swift Striker, Titanic Magazine, Spirit Lifesteal, Mercurial Magnum, Burst Fire
- full (46400 spent): Sharpshooter, Rapid Recharge, Counterspell, Enduring Speed, Swift Striker, Titanic Magazine, Mercurial Magnum, Burst Fire, Leech, Ricochet, Blood Tribute, Lucky Shot
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none in kit (Flight, Stake, Crow, Assassinate do not heal)
- Item Leech: AbilityLifestealPercentHero=28, BulletLifestealPercent=28
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 3 0.3, cast 1 0.4, cast 2 0.3, fire 4, cast 4 1.5, fire 2
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 0, 'Quicksilver Reload': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge, Counterspell (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- vindicta_early.txt
- vindicta_swap1.txt
- vindicta_swap1_rev.txt
- vindicta_swap2.txt
- vindicta_swap2_rev.txt
- vindicta_swap3.txt
- vindicta_swap3_rev.txt
- vindicta_swap4.txt
- vindicta_swap4_rev.txt
- vindicta_heal.txt
- vindicta_heal_rev.txt

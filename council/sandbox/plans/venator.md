# venator (Priest) sandbox plan
Abilities: Consecrating Grenade, Gutshot, Hex-Lined Snap Trap, Ira Domini  order [2, 2, 3, 1, 2, 4, 3, 2, 3, 4, 4, 1, 4, 3, 1, 1]
Core 12 used in scenarios (first 12 final items in build order): Cultist Sacrifice, Battle Vest, Lifestrike, Point Blank, Hunter's Aura, Warp Stone, Superior Cooldown, Greater Expansion, Crushing Fists, Spirit Resilience, Echo Shard, Juggernaut

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Hunter's Aura -> Torment Pulse, Return Fire, none: melee in-your-face aura choice
- Lifestrike -> Fury Trance, Spirit Resilience, none: melee sustain vs plain survival
- Echo Shard -> Refresher, none: late slot (ult 160s CD vs grenade/trap recharge)

## Economy
Struggles to farm (rules): Cultist Sacrifice ~8:00 belongs; grenade (burn AoE) clears waves.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Melee Lifesteal, Close Quarters, Melee Charge, Cultist Sacrifice, Battle Vest
- 12k (12000 spent): Close Quarters, Melee Charge, Cultist Sacrifice, Battle Vest, Lifestrike, Enduring Speed
- 20k (20000 spent): Melee Charge, Cultist Sacrifice, Battle Vest, Lifestrike, Point Blank, Enduring Speed, Compress Cooldown, Hunter's Aura, Mystic Expansion
- 30k (27200 spent): Melee Charge, Cultist Sacrifice, Battle Vest, Lifestrike, Point Blank, Enduring Speed, Hunter's Aura, Warp Stone, Superior Cooldown, Greater Expansion
- full (46400 spent): Cultist Sacrifice, Battle Vest, Lifestrike, Point Blank, Hunter's Aura, Warp Stone, Superior Cooldown, Greater Expansion, Crushing Fists, Spirit Resilience, Echo Shard, Juggernaut
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none in kit (Ira Domini bonus is damage to vampires); heals come only from items
- Item Lifestrike: LifestealHeal=120 (+1.75x spirit), LifestealHealPercent=35 (+0.5x spirit)
- Item Juggernaut: BonusHealthRegen=8
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 3 0.3, cast 2 0.4, cast melee 0.6, cast melee 0.6, cast melee 0.6, cast 1 0.3, cast 4 0.3, cast melee 0.6, cast melee 0.6
Order reasons: imbue/proc items loaded on ability index (assumed) {'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Warp Stone (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- venator_early.txt
- venator_swap1.txt
- venator_swap1_rev.txt
- venator_swap2.txt
- venator_swap2_rev.txt
- venator_swap3.txt
- venator_swap3_rev.txt
- venator_heal.txt
- venator_heal_rev.txt

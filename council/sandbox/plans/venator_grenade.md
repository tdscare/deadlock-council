# venator_grenade (Priest) sandbox plan
Abilities: Consecrating Grenade, Gutshot, Hex-Lined Snap Trap, Ira Domini  order [1, 1, 2, 3, 1, 4, 1, 3, 2, 2, 4, 4, 3, 4, 2, 3]
Core 12 used in scenarios (first 12 final items in build order): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Fortitude, Berserker, Hollow Point, Recharging Rush, Ballistic Enchantment, Rapid Recharge, Vampiric Burst, Silencer
Beyond 12 / optional (not loaded): Inhibitor, Crippling Headshot

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Cultist Sacrifice -> Monster Rounds, none: Venator struggles to farm
- Vampiric Burst -> Leech, Infuser, none: sustain slot
- Hollow Point -> Headhunter, Spirit Rend, none: gun damage T3 choice
- Crippling Headshot -> Lucky Shot, Glass Cannon, none: T4 gun damage slot

## Economy
Struggles to farm (rules): Cultist Sacrifice ~8:00 belongs; grenade (burn AoE) clears waves.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Extra Health, Extra Charge
- 12k (12000 spent): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Fortitude, Bullet Lifesteal, Extra Charge
- 20k (20000 spent): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Fortitude, Berserker, Hollow Point, Bullet Lifesteal, Recharging Rush, Extra Charge
- 30k (25600 spent): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Fortitude, Berserker, Hollow Point, Bullet Lifesteal, Recharging Rush, Ballistic Enchantment, Rapid Recharge
- full (49600 spent): High-Velocity Rounds, Close Quarters, Cultist Sacrifice, Battle Vest, Fortitude, Berserker, Hollow Point, Recharging Rush, Ballistic Enchantment, Rapid Recharge, Vampiric Burst, Silencer
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none in kit (Ira Domini bonus is damage to vampires); heals come only from items
- Item Vampiric Burst: ActiveBonusLifesteal=70, BulletLifestealPercent=13
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, cast 3 0.3, cast 2 0.4, fire 3, cast 4 0.3, fire 4
Order reasons: imbue/proc items loaded on ability index (assumed) {'Recharging Rush': 0, 'Extra Charge': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- venator_grenade_early.txt
- venator_grenade_swap1.txt
- venator_grenade_swap1_rev.txt
- venator_grenade_swap2.txt
- venator_grenade_swap2_rev.txt
- venator_grenade_swap3.txt
- venator_grenade_swap3_rev.txt
- (skipped swap Crippling Headshot: not a final core item - beyond first 12 finals)
- venator_grenade_heal.txt
- venator_grenade_heal_rev.txt

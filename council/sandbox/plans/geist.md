# geist (Ghost) sandbox plan
Abilities: Essence Bomb, Life Drain, Malice, Soul Exchange  order [3, 2, 3, 1, 2, 2, 4, 2, 3, 3, 4, 4, 4, 1, 1, 1]
Core 12 used in scenarios (first 12 final items in build order): Kinetic Dash, Cultist Sacrifice, Radiant Regeneration, Healing Booster, Spirit Resilience, Berserker, Bullet Resist Shredder, Spellslinger, Blood Tribute, Leech, Rapid Recharge, Refresher

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Leech -> Infuser, Vampiric Burst, none: sustain on top of Life Drain
- Refresher -> Transcendent Cooldown, none: ult reset value
- Blood Tribute -> Crippling Headshot, none: T4
- Cultist Sacrifice -> Monster Rounds, none: economy

## Economy
Essence Bomb farms but costs 30% max HP; Cultist (in 'geist') ~8:00 fixes heavy HP cost; check regen covers bomb self-damage.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Mystic Regeneration, Kinetic Dash, Cultist Sacrifice, Healing Booster, Extra Charge
- 12k (12000 spent): Kinetic Dash, Cultist Sacrifice, Radiant Regeneration, Healing Booster, Extra Charge, Bullet Resist Shredder
- 20k (20000 spent): Kinetic Dash, Cultist Sacrifice, Radiant Regeneration, Healing Booster, Spirit Resilience, Berserker, Extra Charge, Bullet Resist Shredder, Bullet Lifesteal
- 30k (28000 spent): Kinetic Dash, Cultist Sacrifice, Radiant Regeneration, Healing Booster, Spirit Resilience, Berserker, Extra Charge, Bullet Resist Shredder, Bullet Lifesteal, Spirit Lifesteal, Spellslinger
- full (43200 spent): Kinetic Dash, Cultist Sacrifice, Radiant Regeneration, Healing Booster, Spirit Resilience, Berserker, Bullet Resist Shredder, Spellslinger, Blood Tribute, Leech, Rapid Recharge, Refresher
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Life Drain heals (24+0.32x spirit per second, LifeDrainHealthMult 100, 2.5s); Soul Exchange swaps health % with the enemy (big heal when you are low and they are not); Essence Bomb/Malice cost you health (SelfDamage 30%/9%)
- Item Radiant Regeneration: HealingPerCast=65 (+1.7x spirit), Regeneration=4 (+0.035x spirit), RegenerationDuration=7
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Leech: AbilityLifestealPercentHero=28, BulletLifestealPercent=28
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, cast 3 0.4, cast 3 0.4, cast 2 2.5, fire 2, cast 4 0.3
Order reasons: imbue/proc items loaded on ability index (assumed) {'Extra Charge': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Rapid Recharge (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- geist_early.txt
- geist_swap1.txt
- geist_swap1_rev.txt
- geist_swap2.txt
- geist_swap2_rev.txt
- geist_swap3.txt
- geist_swap3_rev.txt
- geist_swap4.txt
- geist_swap4_rev.txt
- geist_heal.txt
- geist_heal_rev.txt

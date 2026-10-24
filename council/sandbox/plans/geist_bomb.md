# geist_bomb (Ghost) sandbox plan
Abilities: Essence Bomb, Life Drain, Malice, Soul Exchange  order [1, 1, 3, 2, 1, 3, 4, 1, 3, 3, 2, 2, 4, 4, 2, 4]
Core 12 used in scenarios (first 12 final items in build order): Radiant Regeneration, Healing Booster, Spirit Resilience, Tankbuster, Superior Cooldown, Greater Expansion, Leech, Boundless Spirit, Escalating Exposure, Mystic Reverb, Spirit Burn, Echo Shard

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Leech -> Infuser, Vampiric Burst, none: sustain
- Echo Shard -> Refresher, none: late slot
- Spirit Resilience -> Counterspell, none: defence

## Economy
Essence Bomb farms but costs 30% max HP; Cultist (in 'geist') ~8:00 fixes heavy HP cost; check regen covers bomb self-damage.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Mystic Burst, Radiant Regeneration, Mystic Expansion, Improved Spirit, Healing Booster
- 12k (12000 spent): Radiant Regeneration, Mystic Expansion, Improved Spirit, Healing Booster, Spirit Lifesteal, Tankbuster
- 20k (20000 spent): Radiant Regeneration, Mystic Expansion, Improved Spirit, Healing Booster, Spirit Lifesteal, Spirit Resilience, Tankbuster, Mystic Vulnerability, Superior Cooldown
- 30k (27200 spent): Radiant Regeneration, Improved Spirit, Healing Booster, Spirit Resilience, Tankbuster, Mystic Vulnerability, Superior Cooldown, Greater Expansion, Leech
- full (56000 spent): Radiant Regeneration, Healing Booster, Spirit Resilience, Tankbuster, Superior Cooldown, Greater Expansion, Leech, Boundless Spirit, Escalating Exposure, Mystic Reverb, Spirit Burn, Echo Shard
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Life Drain heals (24+0.32x spirit per second, LifeDrainHealthMult 100, 2.5s); Soul Exchange swaps health % with the enemy (big heal when you are low and they are not); Essence Bomb/Malice cost you health (SelfDamage 30%/9%)
- Item Radiant Regeneration: HealingPerCast=65 (+1.7x spirit), Regeneration=4 (+0.035x spirit), RegenerationDuration=7
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Leech: AbilityLifestealPercentHero=28, BulletLifestealPercent=28
- Item Mystic Reverb: AbilityLifestealPercentHero=8, ImbueAbilityLifesteal=22
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 1 0.3, cast 3 0.4, cast 3 0.4, cast 2 2.5, fire 2, cast 4 0.3
Order reasons: imbue/proc items loaded on ability index (assumed) {'Mystic Expansion': 0}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build:  (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- geist_bomb_early.txt
- geist_bomb_swap1.txt
- geist_bomb_swap1_rev.txt
- geist_bomb_swap2.txt
- geist_bomb_swap2_rev.txt
- geist_bomb_swap3.txt
- geist_bomb_swap3_rev.txt
- geist_bomb_heal.txt
- geist_bomb_heal_rev.txt

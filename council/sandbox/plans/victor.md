# victor (Frank) sandbox plan
Abilities: Pain Battery, Jumpstart, Aura of Suffering, Shocking Reanimation  order [3, 3, 1, 2, 3, 4, 1, 3, 1, 2, 2, 1, 4, 4, 2, 4]
Core 12 used in scenarios (first 12 final items in build order): Torment Pulse, Healing Booster, Infuser, Escalating Exposure, Greater Expansion, Warp Stone, Superior Cooldown, Scourge, Boundless Spirit, Juggernaut, Spirit Burn, Witchmail

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Infuser -> Leech, Vampiric Burst, none: sustain slot; healing attribution needed
- Torment Pulse -> Spirit Sap, Radiant Regeneration, none: aura synergy with Aura of Suffering
- Scourge -> Cursed Relic, Focus Lens, none: T4 slot

## Economy
Poor wave clear; Aura of Suffering (3) farms but self-damages 70%: needs regen/Healing Booster. Cultist optional - test.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Improved Spirit, Torment Pulse, Healing Booster, Spirit Lifesteal
- 12k (12000 spent): Improved Spirit, Torment Pulse, Healing Booster, Spirit Lifesteal, Enduring Speed, Mystic Vulnerability, Mystic Expansion
- 20k (20000 spent): Improved Spirit, Torment Pulse, Healing Booster, Enduring Speed, Mystic Vulnerability, Mystic Expansion, Infuser, Superior Cooldown
- 30k (28800 spent): Improved Spirit, Torment Pulse, Healing Booster, Enduring Speed, Infuser, Compress Cooldown, Escalating Exposure, Greater Expansion, Warp Stone
- full (59200 spent): Torment Pulse, Healing Booster, Infuser, Escalating Exposure, Greater Expansion, Warp Stone, Superior Cooldown, Scourge, Boundless Spirit, Juggernaut, Spirit Burn, Witchmail
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Pain Battery T3 heals 15% of missing HP and needs >=40% stored damage; Jumpstart: 100+1.2x spirit regen over 4.5s but costs 15% current HP; Aura of Suffering self-damages (no heal); Shocking Reanimation revive at 50% HP
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
- Item Infuser: AbilityLifestealPercentHero=70, AbilityLifestealPercentHeroPassive=13
- Item Juggernaut: BonusHealthRegen=8
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
hurtme 300, cast 1 0.5, cast 2 0.4, cast 3 6, fire 2
Order reasons: imbue/proc items loaded on ability index (assumed) {'Mystic Expansion': 2, 'Compress Cooldown': 2}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Warp Stone (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- victor_early.txt
- victor_swap1.txt
- victor_swap1_rev.txt
- victor_swap2.txt
- victor_swap2_rev.txt
- victor_swap3.txt
- victor_swap3_rev.txt
- victor_heal.txt
- victor_heal_rev.txt

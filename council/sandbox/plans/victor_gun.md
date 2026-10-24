# victor_gun (Frank) sandbox plan
Abilities: Pain Battery, Jumpstart, Aura of Suffering, Shocking Reanimation  order [2, 2, 1, 3, 2, 4, 1, 2, 3, 1, 4, 4, 3, 1, 4, 3]
Core 12 used in scenarios (first 12 final items in build order): Opening Rounds, Titanic Magazine, Swift Striker, Enduring Speed, Berserker, Mercurial Magnum, Spiritual Overflow, Spellslinger, Leech, Superior Cooldown, Healing Tempo, Frenzy

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Leech -> Infuser, Vampiric Burst, none: sustain slot (already tested once: inconclusive on healing)
- Frenzy -> Glass Cannon, Crippling Headshot, none: T4 gun slot
- Spellslinger -> Silencer, none: late slot

## Economy
Poor wave clear; Aura of Suffering (3) farms but self-damages 70%: needs regen/Healing Booster. Cultist optional - test.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Opening Rounds, Titanic Magazine, Swift Striker, Healing Booster, Enduring Speed
- 12k (11200 spent): Opening Rounds, Titanic Magazine, Swift Striker, Healing Booster, Enduring Speed, Bullet Lifesteal, Quicksilver Reload
- 20k (19200 spent): Opening Rounds, Titanic Magazine, Swift Striker, Healing Booster, Enduring Speed, Bullet Lifesteal, Quicksilver Reload, Berserker, Spirit Lifesteal, Superior Cooldown
- 30k (28800 spent): Opening Rounds, Titanic Magazine, Swift Striker, Healing Booster, Enduring Speed, Bullet Lifesteal, Berserker, Mercurial Magnum, Spiritual Overflow, Superior Cooldown
- full (51200 spent): Opening Rounds, Titanic Magazine, Swift Striker, Enduring Speed, Berserker, Mercurial Magnum, Spiritual Overflow, Spellslinger, Leech, Superior Cooldown, Healing Tempo, Frenzy
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: Pain Battery T3 heals 15% of missing HP and needs >=40% stored damage; Jumpstart: 100+1.2x spirit regen over 4.5s but costs 15% current HP; Aura of Suffering self-damages (no heal); Shocking Reanimation revive at 50% HP
- Item Spiritual Overflow: AbilityLifestealPercentHero=13, BonusSpiritLifesteal=10
- Item Leech: AbilityLifestealPercentHero=28, BulletLifestealPercent=28
- Item Healing Tempo: BonusHealthRegen=6, HealAmpCastPercent=25, HealAmpRegenPercent=25
- Item Frenzy: BulletLifestealPercent=10
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 2 0.4, fire 3, hurtme 300, cast 1 0.5, cast 3 6, fire 2
Order reasons: imbue/proc items loaded on ability index (assumed) {'Compress Cooldown': 2}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build:  (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- victor_gun_early.txt
- victor_gun_swap1.txt
- victor_gun_swap1_rev.txt
- victor_gun_swap2.txt
- victor_gun_swap2_rev.txt
- victor_gun_swap3.txt
- victor_gun_swap3_rev.txt
- victor_gun_heal.txt
- victor_gun_heal_rev.txt

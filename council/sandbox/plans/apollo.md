# apollo sandbox plan (Rizuhble's Parry Potter Apollo)
Hero enum `Fencer` (UNVERIFIED: internal id hero_fencer exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Disengaging Sigil, 2=Riposte, 3=Flawless Advance, 4=Itani Lo Sahn.

Final 12 used in scenarios: Healing Booster, Enchanter's Emblem, Tankbuster, Greater Expansion, Stamina Mastery, Torment Pulse, Superior Cooldown, Boundless Spirit, Leech, Spirit Burn, Mystic Reverb, Escalating Exposure

## Uncertain slots and substitutes
- Enchanter's Emblem: swap with Improved Spirit, Spirit Lifesteal, Superior Cooldown and none. Why uncertain: Mid T3 spirit/cd; Apollo cds are long (Sigil 12s, Lunge 26s, Riposte 22s) - maybe cooldown beats amp.
- Torment Pulse: swap with Healing Booster, Reactive Barrier, Spirit Shielding and none. Why uncertain: Sell-for-counter slot; Apollo is in melee range so aura could be decent.

## Economy
Spirit-poke/gap-close hero with a gun; farms with gun + Sigil on waves. No Cultist; Grit in lane-loss box. Check cooldown rates at 8k (Compress Cooldown only).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Mystic Burst, Mystic Expansion, Compress Cooldown, Improved Spirit, Spirit Lifesteal, Healing Booster
- 12k (12000 souls): Mystic Expansion, Compress Cooldown, Improved Spirit, Spirit Lifesteal, Healing Booster, Enchanter's Emblem, Tankbuster
- 20k (19200 souls): Compress Cooldown, Improved Spirit, Spirit Lifesteal, Healing Booster, Enchanter's Emblem, Tankbuster, Mystic Vulnerability, Greater Expansion, Stamina Mastery
- 30k (28800 souls): Spirit Lifesteal, Healing Booster, Enchanter's Emblem, Tankbuster, Mystic Vulnerability, Greater Expansion, Stamina Mastery, Torment Pulse, Superior Cooldown, Boundless Spirit
- full (51200 souls): Healing Booster, Enchanter's Emblem, Tankbuster, Greater Expansion, Stamina Mastery, Torment Pulse, Superior Cooldown, Boundless Spirit, Leech, Spirit Burn, Mystic Reverb, Escalating Exposure
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `apollo_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.8`: Sigil (leap back; T1 +25% fire rate for 8s)
- `hold 3 0.55`: Lunge: hold 0.525s then release inside the 0.25s perfect window; stab 1
- `hold 3 0.55`: recast (2 stacks) perfect stab 2
- `fire 2.5`: gun while sigil fire rate buff is up
- `cast 4 2.0`: Itani: only when enemy <50% HP (bonus +60%): see conditions - script uses enemyhp 45
- #@ enemyhp 45 (before ult only)
- Note: Riposte needs an incoming hit to parry (60 dmg threshold): needs bot to shoot/melee; planned op `parry` with bot attack. Not in script.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `apollo_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stun/silence stops lunge and ult windup).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Flawless Advance T1: heals 35 on Perfect Hit vs hero
- kit: Riposte T3: 75% bullet/spirit/melee lifesteal vs the Riposte target for 13s
- kit: Ultimate: target cannot heal
- item: Healing Booster (HealAmpCastPercent, HealAmpRegenPercent, BonusHealthRegen)
- item: Leech (AbilityLifestealPercentHero, BulletLifestealPercent)
- item: Mystic Reverb (AbilityLifestealPercentHero, ImbueAbilityLifesteal)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`apollo_heal.txt`): full, noheal_items, minus_Healing Booster, minus_Leech, minus_Mystic Reverb, only_Healing Booster, only_Leech, only_Mystic Reverb, cand_Spirit Lifesteal at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_cc.txt`

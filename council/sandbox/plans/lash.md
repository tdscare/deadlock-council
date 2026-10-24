# lash sandbox plan (Rizuhble's Elbow Drop Lash)
Hero enum `Lash` (UNVERIFIED: internal id hero_lash exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Ground Strike, 2=Grapple, 3=Flog, 4=Death Slam.

Final 12 used in scenarios: Cold Front, Mystic Shot, Enchanter's Emblem, Stamina Mastery, Tankbuster, Headhunter, Warp Stone, Boundless Spirit, Greater Expansion, Superior Cooldown, Spirit Burn, Mystic Reverb

## Uncertain slots and substitutes
- Cold Front: swap with Slowing Hex, Extra Stamina, Mystic Shot and none. Why uncertain: Early cheap slow; sold later? it feeds Arctic Blast rich.
- Warp Stone: swap with Majestic Leap, Enduring Speed, Reactive Barrier and none. Why uncertain: Build note names Majestic Leap swap: test it, plus none.

## Economy
Slam combos farm waves with Ground Strike from height; Flog heals 16% of damage vs non-heroes - decent farm sustain. No Cultist.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Headshot Booster, Mystic Burst, Mystic Expansion, Improved Spirit, Cold Front, Mystic Shot, Extra Stamina
- 12k (12000 souls): Headshot Booster, Mystic Burst, Mystic Expansion, Improved Spirit, Cold Front, Mystic Shot, Enchanter's Emblem, Stamina Mastery
- 20k (19200 souls): Mystic Expansion, Improved Spirit, Cold Front, Mystic Shot, Enchanter's Emblem, Stamina Mastery, Tankbuster, Headhunter, Extra Charge, Compress Cooldown
- 30k (29600 souls): Cold Front, Mystic Shot, Enchanter's Emblem, Stamina Mastery, Tankbuster, Headhunter, Extra Charge, Compress Cooldown, Warp Stone, Boundless Spirit, Greater Expansion
- full (44000 souls): Cold Front, Mystic Shot, Enchanter's Emblem, Stamina Mastery, Tankbuster, Headhunter, Extra Charge, Warp Stone, Boundless Spirit, Greater Expansion, Superior Cooldown, Spirit Burn, Mystic Reverb
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `lash_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.6`: Grapple up to a high point (Extra Charge: a second grapple gets higher)
- `cast 2 0.6`: 2nd grapple
- `cast 1 0.8`: Ground Strike dive: damage scales with height fallen (per meter up to 25m)
- `cast 3 0.5`: Flog (heals)
- `cast 4 2.6`: Death Slam: needs lock-on 2.3s channel, lifted enemy 14m throw
- `fire 1`
- Note: Height is required: harness needs a high anchor (planned `aimoff` pitch up + a grapple point); unverified in dl_midtown. Ground-strike damage depends on fall height, so log height.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `lash_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns/sleeps before slam).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Flog: heals % of damage dealt (16% non-hero, 40% vs heroes with T3)
- kit: Items
- item: Headhunter (HealPercentPerHeadshot)
- item: Mystic Reverb (AbilityLifestealPercentHero, ImbueAbilityLifesteal)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`lash_heal.txt`): full, noheal_items, minus_Headhunter, minus_Mystic Reverb, only_Headhunter, only_Mystic Reverb at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/lash_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/lash_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/lash_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/lash_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/lash_cc.txt`

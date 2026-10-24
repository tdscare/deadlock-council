# vyper sandbox plan (Rizuhble's Snake Oil Vyper)
Hero enum `Viper` (UNVERIFIED: internal id hero_viper exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Screwjab Dagger, 2=Lethal Venom, 3=Slither, 4=Petrifying Bola.

Final 12 used in scenarios: Cold Front, Opening Rounds, Enduring Speed, Burst Fire, Point Blank, Mercurial Magnum, Leech, Boundless Spirit, Spiritual Overflow, Frenzy, Ricochet, Unstoppable

## Uncertain slots and substitutes
- Quicksilver Reload: swap with Rapid Rounds, Extended Magazine, Burst Fire and none. Why uncertain: Early gun slot; Vyper is spirit-invest - is any gun item worth it before spirit?
- Burst Fire: swap with Intensifying Magazine, Close Quarters, Rapid Rounds and none. Why uncertain: Mid gun slot again.

## Economy
Spirit dagger/poke with dagger stacks; farm: Extra Spirit then Improved Spirit; daggers (2 charges) farm waves. No Cultist.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (7200 souls): Improved Spirit, Quicksilver Reload, Cold Front, Opening Rounds, Rapid Rounds
- 12k (12000 souls): Improved Spirit, Quicksilver Reload, Cold Front, Opening Rounds, Rapid Rounds, Bullet Lifesteal, Enduring Speed, Spirit Lifesteal
- 20k (17600 souls): Improved Spirit, Quicksilver Reload, Cold Front, Opening Rounds, Bullet Lifesteal, Enduring Speed, Spirit Lifesteal, Burst Fire, Point Blank
- 30k (25600 souls): Improved Spirit, Cold Front, Opening Rounds, Enduring Speed, Burst Fire, Point Blank, Mercurial Magnum, Leech
- full (54400 souls): Cold Front, Opening Rounds, Enduring Speed, Burst Fire, Point Blank, Mercurial Magnum, Leech, Boundless Spirit, Spiritual Overflow, Frenzy, Ricochet, Unstoppable
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `vyper_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.4`: Lethal Venom first (delay 3s; damage up with missing health: use after daggers to make it hurt? Venom triggers after 3s, so cast, then daggers)
- `cast 1 0.5`: Dagger 1
- `cast 1 0.5`: Dagger 2 (stacks: +damage, -bullet resist per stack)
- `fire 2.5`: gun on slowed target
- `cast 4 0.4`: Bola: petrify blocks all damage 2.2s - do NOT shoot during petrify; wait
- `wait 2.3`
- `fire 2`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `vyper_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (cannot slide in while stunned).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit; Slither barrier; Lethal Venom -40% enemy healing
- item: Leech (AbilityLifestealPercentHero, BulletLifestealPercent)
- item: Spiritual Overflow (AbilityLifestealPercentHero, BonusSpiritLifesteal)
- item: Frenzy (BulletLifestealPercent)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`vyper_heal.txt`): full, noheal_items, minus_Leech, minus_Spiritual Overflow, minus_Frenzy, only_Leech, only_Spiritual Overflow, only_Frenzy at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_cc.txt`

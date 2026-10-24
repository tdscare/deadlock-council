# vyper_gun sandbox plan (Rizuhble's Ricochet Rattler)
Hero enum `Viper` (UNVERIFIED: internal id hero_viper exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Screwjab Dagger, 2=Lethal Venom, 3=Slither, 4=Petrifying Bola.

Final 12 used in scenarios: Intensifying Magazine, Burst Fire, Spirit Shielding, Stamina Mastery, Split Shot, Point Blank, Ricochet, Mercurial Magnum, Vampiric Burst, Silencer, Lucky Shot, Unstoppable

## Uncertain slots and substitutes
- Split Shot: swap with Close Quarters, Point Blank, Quicksilver Reload and none. Why uncertain: Mid gun; Ricochet already later - is Split Shot worth it?
- Spirit Shielding: swap with Reactive Barrier, Grit, Extra Health and none. Why uncertain: Early armor.

## Economy
Gun Vyper with Split Shot farm (build note). Check ammo at 8k: Rapid Rounds+Grit+Intensifying Magazine.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Intensifying Magazine, Burst Fire, Spirit Shielding, Bullet Lifesteal
- 12k (11200 souls): Intensifying Magazine, Burst Fire, Spirit Shielding, Bullet Lifesteal, Stamina Mastery
- 20k (17600 souls): Intensifying Magazine, Burst Fire, Spirit Shielding, Bullet Lifesteal, Stamina Mastery, Split Shot, Point Blank, Quicksilver Reload
- 30k (28800 souls): Intensifying Magazine, Burst Fire, Spirit Shielding, Bullet Lifesteal, Stamina Mastery, Split Shot, Point Blank, Ricochet, Mercurial Magnum
- full (52800 souls): Intensifying Magazine, Burst Fire, Spirit Shielding, Stamina Mastery, Split Shot, Point Blank, Ricochet, Mercurial Magnum, Vampiric Burst, Silencer, Lucky Shot, Unstoppable
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `vyper_gun_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.4`: Venom (bullets also build it up at T3)
- `cast 1 0.5`: Dagger
- `cast 1 0.5`: Dagger
- `fire 3`: gun
- `cast 4 0.4`: Bola
- `wait 2.3`
- `fire 2`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `vyper_gun_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (slide).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Bullet Lifesteal/Vampiric Burst (Late), Silencer none
- item: Vampiric Burst (ActiveBonusLifesteal, BulletLifestealPercent)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`vyper_gun_heal.txt`): full, noheal_items, minus_Vampiric Burst, only_Vampiric Burst at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_gun_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_gun_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_gun_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_gun_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/vyper_gun_cc.txt`

# paradox sandbox plan (Rizuhble's Clock Sniper Paradox)
Hero enum `Chrono` (UNVERIFIED: internal id hero_chrono exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Pulse Grenade, 2=Time Wall, 3=Kinetic Carbine, 4=Paradoxical Swap.

Final 12 used in scenarios: Sharpshooter, Headhunter, Veil Walker, Express Shot, Tankbuster, Hollow Point, Superior Cooldown, Stamina Mastery, Mystic Reverb, Indomitable, Glass Cannon, Crippling Headshot

## Uncertain slots and substitutes
- Veil Walker: swap with Warp Stone, Fortitude, Healing Booster and none. Why uncertain: 4.8k health spike item; Veil Walker only works if Time Wall is up and walked through. Does a plain health item win?
- Express Shot: swap with Quicksilver Reload, Burst Fire, Rapid Rounds and none. Why uncertain: Gun T3 slot for burst between Carbines; ammo/reload may matter more at 40% accuracy.

## Economy
Gun sniper: farms with gun at range; no Cultist. Check ammo at 8k (HV Rounds + Long Range only): constant reloading? Mystic Burst at 7.2k adds spirit.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Sharpshooter, Headhunter, Reactive Barrier
- 12k (11200 souls): Sharpshooter, Headhunter, Reactive Barrier, Veil Walker
- 20k (19200 souls): Sharpshooter, Headhunter, Reactive Barrier, Veil Walker, Express Shot, Tankbuster, Compress Cooldown, Extra Stamina
- 30k (26400 souls): Sharpshooter, Headhunter, Reactive Barrier, Veil Walker, Express Shot, Tankbuster, Hollow Point, Superior Cooldown, Stamina Mastery
- full (50400 souls): Sharpshooter, Headhunter, Veil Walker, Express Shot, Tankbuster, Hollow Point, Superior Cooldown, Stamina Mastery, Mystic Reverb, Indomitable, Glass Cannon, Crippling Headshot
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `paradox_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.5`: Pulse Grenade first: stacking damage amp vs victim (4%/pulse stack, 8s)
- `cast 2 0.5`: Time Wall: friendly bullets +30% damage (T2) and Veil Walker target; shoot through it
- `hold 3 2.6`: Kinetic Carbine fully charged (2.5s max, T3 hold 3.5s) - damage scales with charge
- `fire 2`: Express Shot / gun through the wall
- `cast 4 0.6`: Swap last (T3 10% max HP damage, barrier) when closed in
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `paradox_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Dispel Magic (slow/hex stops dashes).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit (Swap barrier is not healing)
- item: Headhunter (HealPercentPerHeadshot)
- item: Veil Walker (HealOnVeil)
- item: Mystic Reverb (AbilityLifestealPercentHero, ImbueAbilityLifesteal)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`paradox_heal.txt`): full, noheal_items, minus_Headhunter, minus_Veil Walker, minus_Mystic Reverb, only_Headhunter, only_Veil Walker, only_Mystic Reverb, cand_Healing Booster at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_cc.txt`

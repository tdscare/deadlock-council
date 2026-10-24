# celeste_carry sandbox plan (Rizuhble's Glitter Gun Celeste)
Hero enum `Unicorn` (UNVERIFIED: internal id hero_unicorn exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Light Eater, 2=Dazzling Trick, 3=Radiant Daggers, 4=Shining Wonder.

Final 12 used in scenarios: Kinetic Dash, Radiant Regeneration, Healing Booster, Fortitude, Mercurial Magnum, Rapid Recharge, Spiritual Overflow, Spirit Rend, Unstoppable, Toxic Bullets, Witchmail, Spellslinger

## Uncertain slots and substitutes
- Swift Striker: swap with Rapid Rounds, Quicksilver Reload, Burst Fire and none. Why uncertain: Gun T2 fire rate slot sold for Spellslinger; check ammo/rate.
- Fortitude: swap with Healing Booster, Extra Health, Reactive Barrier and none. Why uncertain: Mid health item; Celeste is not a roamer - is Fortitude justified (heal OOC only)?

## Economy
Gun carry with Daggers fire-rate stacks (+9%/stack T3). HVR first. Ammo check at 8k: fire rate items without mag.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Extra Regen, Opening Rounds, Kinetic Dash, Swift Striker, Extra Health, Quicksilver Reload
- 12k (12000 souls): Opening Rounds, Kinetic Dash, Swift Striker, Extra Health, Quicksilver Reload, Radiant Regeneration, Healing Booster
- 20k (20000 souls): Opening Rounds, Kinetic Dash, Swift Striker, Radiant Regeneration, Healing Booster, Fortitude, Mercurial Magnum, Extra Charge
- 30k (28800 souls): Opening Rounds, Kinetic Dash, Swift Striker, Radiant Regeneration, Healing Booster, Fortitude, Mercurial Magnum, Rapid Recharge, Spiritual Overflow
- full (54400 souls): Opening Rounds, Kinetic Dash, Swift Striker, Radiant Regeneration, Healing Booster, Fortitude, Mercurial Magnum, Rapid Recharge, Spiritual Overflow, Spirit Rend, Unstoppable, Toxic Bullets, Witchmail, Spellslinger
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `celeste_carry_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 1.6`: Daggers first: fire-rate stack buff (6 stacks max, 30s)
- `cast 1 0.5`: Light Eater cone
- `fire 2.5`: gun on blasted at stacks
- `cast 3 1.6`: 2nd charge: stacks
- `fire 2`
- `cast 4 2.0`: ult
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `celeste_carry_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Light Eater 18% spirit lifesteal on blasted
- kit: Radiant/Mystic Regeneration; Fortitude (OOC heal %)
- item: Radiant Regeneration (HealingPerCast, Regeneration)
- item: Healing Booster (HealAmpCastPercent, HealAmpRegenPercent, BonusHealthRegen)
- item: Spiritual Overflow (AbilityLifestealPercentHero, BonusSpiritLifesteal)
- item: Spirit Rend (AbilityLifestealPercentHero)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`celeste_carry_heal.txt`): full, noheal_items, minus_Radiant Regeneration, minus_Healing Booster, minus_Spiritual Overflow, minus_Spirit Rend, only_Radiant Regeneration, only_Healing Booster, only_Spiritual Overflow, only_Spirit Rend at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_carry_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_carry_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_carry_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_carry_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_carry_cc.txt`

# celeste sandbox plan (Rizuhble's Healthy Glow Celeste)
Hero enum `Unicorn` (UNVERIFIED: internal id hero_unicorn exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Light Eater, 2=Dazzling Trick, 3=Radiant Daggers, 4=Shining Wonder.

Final 12 used in scenarios: Radiant Regeneration, Healing Booster, Spirit Shielding, Enchanter's Emblem, Torment Pulse, Greater Expansion, Suppressor, Tankbuster, Superior Cooldown, Witchmail, Escalating Exposure, Spiritual Overflow

## Uncertain slots and substitutes
- Mystic Burst: swap with Improved Spirit, Spirit Lifesteal, Extra Spirit and none. Why uncertain: Early T1 spirit item; is the first spike best as Burst or Lifesteal when Light Eater already lifesteals?
- Suppressor: swap with Enchanter's Emblem, Superior Cooldown, Tankbuster and none. Why uncertain: Mid slot sold for a counter; does the silence tool give more than amp?

## Economy
Spirit caster with gun + Light Eater DOT cone: farms waves in cone + gun. High-Velocity/Opening Rounds early are the gun farm. No Cultist; check 8k (HVR+Opening Rounds+Extra Regen+Mystic Regen).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Opening Rounds, Mystic Expansion, Radiant Regeneration, Mystic Burst, Healing Booster
- 12k (11200 souls): Opening Rounds, Mystic Expansion, Radiant Regeneration, Mystic Burst, Healing Booster, Spirit Shielding, Enchanter's Emblem
- 20k (20000 souls): Opening Rounds, Radiant Regeneration, Mystic Burst, Healing Booster, Spirit Shielding, Enchanter's Emblem, Torment Pulse, Greater Expansion, Spirit Lifesteal, Suppressor
- 30k (27200 souls): Opening Rounds, Radiant Regeneration, Healing Booster, Spirit Shielding, Enchanter's Emblem, Torment Pulse, Greater Expansion, Spirit Lifesteal, Suppressor, Mystic Vulnerability, Tankbuster, Superior Cooldown
- full (43200 souls): Opening Rounds, Radiant Regeneration, Healing Booster, Spirit Shielding, Enchanter's Emblem, Torment Pulse, Greater Expansion, Suppressor, Tankbuster, Superior Cooldown, Witchmail, Escalating Exposure, Spiritual Overflow
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `celeste_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.5`: Light Eater first: blasted targets take extra on bullet hit and give you lifesteal (cone 10m)
- `cast 3 1.6`: Radiant Daggers (beam, 1.4s fuse): spirit amp stack +7%/hit (max 6); repeat for stacks 0/1/max
- `fire 1.5`: gun on blasted target
- `cast 2 0.5`: Dazzling Trick (barrier; explode = silence)
- `cast 4 2.0`: Shining Wonder, ult
- `fire 1.5`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `celeste_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns before cast).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Light Eater: 18% spirit lifesteal on targets blasted (8s, +0.05x spirit duration)
- kit: Radiant Regeneration / Mystic Regeneration items
- item: Radiant Regeneration (HealingPerCast, Regeneration)
- item: Healing Booster (HealAmpCastPercent, HealAmpRegenPercent, BonusHealthRegen)
- item: Spiritual Overflow (AbilityLifestealPercentHero, BonusSpiritLifesteal)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`celeste_heal.txt`): full, noheal_items, minus_Radiant Regeneration, minus_Healing Booster, minus_Spiritual Overflow, only_Radiant Regeneration, only_Healing Booster, only_Spiritual Overflow, cand_Spirit Lifesteal at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/celeste_cc.txt`

# baba sandbox plan (Rizuhble's Glock Granny Baba)
Hero enum `Baba` (UNVERIFIED: internal id hero_baba exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Threadsap, 2=Granny Long Legs, 3=Baba's Brew, 4=Feed The Birds.

Final 12 used in scenarios: Radiant Regeneration, Reactive Barrier, Titanic Magazine, Fortitude, Burst Fire, Rapid Recharge, Spirit Snatch, Spiritual Overflow, Superior Cooldown, Boundless Spirit, Escalating Exposure, Ricochet

## Uncertain slots and substitutes
- Rapid Recharge: swap with Quicksilver Reload, Compress Cooldown, Extra Stamina and none. Why uncertain: Cleanse + cooldown; Baba cds are long (Threadsap 6s charge, Brew, ult 150s?).
- Spirit Snatch: swap with Spirit Lifesteal, Improved Spirit, Mystic Vulnerability and none. Why uncertain: Mid spirit T2; Threadsap already steals spirit.

## Economy
Gun hero with spirit steal: Threadsap on creeps? Steals enemy HERO spirit only (stolen spirit effectiveness 175%), so farm is gun-only; Extra Charge/Rapid Rounds first. Check 8k: Extra Charge+Mystic Regen+Rapid Rounds.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (7200 souls): Extra Charge, Rapid Rounds, Spirit Strike, Radiant Regeneration, Reactive Barrier
- 12k (12000 souls): Extra Charge, Rapid Rounds, Spirit Strike, Radiant Regeneration, Reactive Barrier, Titanic Magazine, Fortitude
- 20k (19200 souls): Spirit Strike, Radiant Regeneration, Reactive Barrier, Titanic Magazine, Fortitude, Burst Fire, Spirit Lifesteal, Rapid Recharge, Extra Spirit
- 30k (29600 souls): Radiant Regeneration, Reactive Barrier, Titanic Magazine, Fortitude, Burst Fire, Rapid Recharge, Extra Spirit, Spirit Snatch, Compress Cooldown, Mystic Vulnerability, Spiritual Overflow
- full (48000 souls): Radiant Regeneration, Reactive Barrier, Titanic Magazine, Fortitude, Burst Fire, Rapid Recharge, Spirit Snatch, Spiritual Overflow, Superior Cooldown, Boundless Spirit, Escalating Exposure, Ricochet
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `baba_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.5`: Threadsap first: steals spirit -> every bullet deals extra magic damage (8 +0.26x spirit per bullet)
- `fire 1.0`: bullets while holding stolen spirit
- `cast 3 0.6`: Baba's Brew on target (cycle barrier/silence/burn)
- `cast 2 0.6`: Granny Long Legs (speed, resist)
- `cast 4 6.8`: Feed The Birds: channel 6.5s, bread stacks to max at 3.5s; do not break channel
- `fire 1.5`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `baba_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns cancel ult channel).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Granny Long Legs T3: +50% melee lifesteal and 30% resists
- kit: Baba's Brew soothing phase = barrier, not heal
- kit: Mystic/Radiant Regeneration; Fortitude
- item: Radiant Regeneration (HealingPerCast, Regeneration)
- item: Spiritual Overflow (AbilityLifestealPercentHero, BonusSpiritLifesteal)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`baba_heal.txt`): full, noheal_items, minus_Radiant Regeneration, minus_Spiritual Overflow, only_Radiant Regeneration, only_Spiritual Overflow, cand_Spirit Lifesteal at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_cc.txt`

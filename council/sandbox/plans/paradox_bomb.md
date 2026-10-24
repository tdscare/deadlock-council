# paradox_bomb sandbox plan (Rizuhble's Time Bomb Paradox)
Hero enum `Chrono` (UNVERIFIED: internal id hero_chrono exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Pulse Grenade, 2=Time Wall, 3=Kinetic Carbine, 4=Paradoxical Swap.

Final 12 used in scenarios: Arcane Surge, Veil Walker, Superior Duration, Warp Stone, Greater Expansion, Echo Shard, Superior Cooldown, Escalating Exposure, Infuser, Boundless Spirit, Vortex Web, Spirit Burn

## Uncertain slots and substitutes
- Warp Stone: swap with Slowing Hex, Superior Duration, Healing Booster and none. Why uncertain: Mid mobility slot sold for a counter; it only exists to get away after the grenade.
- Arcane Surge: swap with Improved Spirit, Mystic Burst, Spirit Lifesteal and none. Why uncertain: Early spirit amp that needs a dash-jump before the grenade - does the ready-timing actually happen?

## Economy
Spirit grenade farms waves; Extra Spirit / Mystic Expansion first. No Cultist; check 8k: Extra Spirit+Mystic Expansion+Extra Stamina only.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (6400 souls): Extra Spirit, Mystic Expansion, Arcane Surge, Duration Extender, Spirit Lifesteal
- 12k (12000 souls): Mystic Expansion, Arcane Surge, Duration Extender, Spirit Lifesteal, Veil Walker, Improved Spirit, Mystic Vulnerability
- 20k (20000 souls): Mystic Expansion, Arcane Surge, Spirit Lifesteal, Veil Walker, Improved Spirit, Mystic Vulnerability, Compress Cooldown, Superior Duration, Slowing Hex, Warp Stone
- 30k (28800 souls): Arcane Surge, Spirit Lifesteal, Veil Walker, Improved Spirit, Mystic Vulnerability, Compress Cooldown, Superior Duration, Slowing Hex, Warp Stone, Greater Expansion, Echo Shard
- full (56000 souls): Arcane Surge, Veil Walker, Superior Duration, Warp Stone, Greater Expansion, Echo Shard, Superior Cooldown, Escalating Exposure, Infuser, Boundless Spirit, Vortex Web, Spirit Burn
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `paradox_bomb_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.4`: Pulse Grenade (Arcane Surge: dash-jump immediately before)
- `cast 1 0.4`: Echo Shard second grenade right after, so stacks pile up (once Echo Shard owned)
- `cast 2 0.5`: wall for bullets/slow
- `cast 3 2.6`: Carbine
- `cast 4 0.6`: Swap
- `fire 2`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `paradox_bomb_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Dispel Magic (slows/hexes).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit; Spirit Lifesteal (early) and Infuser (late) are the sole sustain
- item: Veil Walker (HealOnVeil)
- item: Infuser (AbilityLifestealPercentHero, AbilityLifestealPercentHeroPassive)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`paradox_bomb_heal.txt`): full, noheal_items, minus_Veil Walker, minus_Infuser, only_Veil Walker, only_Infuser, cand_Healing Booster, cand_Spirit Lifesteal at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_bomb_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_bomb_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_bomb_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_bomb_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/paradox_bomb_cc.txt`

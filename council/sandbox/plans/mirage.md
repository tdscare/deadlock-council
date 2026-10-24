# mirage sandbox plan (Rizuhble's Target Practice Mirage)
Hero enum `Mirage` (UNVERIFIED: internal id hero_mirage exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Fire Scarabs, 2=Dust Devil, 3=Djinn's Mark, 4=Traveler.

Final 12 used in scenarios: Healbane, Dispel Magic, Toxic Bullets, Ricochet, Escalating Exposure, Superior Cooldown, Inhibitor, Spirit Rend, Titanic Magazine, Boundless Spirit, Headhunter, Leech

## Uncertain slots and substitutes
- Titanic Magazine: swap with Extended Magazine, Rapid Rounds, Headhunter and none. Why uncertain: Marks proc per shot (2.75s per target cooldown): do we need ammo at all?
- Healbane: swap with Healing Booster, Extra Regen, Spirit Lifesteal and none. Why uncertain: Early anti-heal sold later; Scarabs already steals life.

## Economy
Gun+marks: farms with gun; marks only work on heroes. No Cultist. Extra Spirit first; Compress Cooldown on Djinn's Mark.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Compress Cooldown, Mystic Vulnerability, Improved Spirit, Spirit Shredder, Healbane
- 12k (11200 souls): Compress Cooldown, Mystic Vulnerability, Improved Spirit, Spirit Shredder, Healbane, Dispel Magic
- 20k (16000 souls): Compress Cooldown, Mystic Vulnerability, Improved Spirit, Spirit Shredder, Healbane, Dispel Magic, Toxic Bullets, Headshot Booster, Extended Magazine
- 30k (28800 souls): Improved Spirit, Spirit Shredder, Healbane, Dispel Magic, Toxic Bullets, Headshot Booster, Extended Magazine, Ricochet, Escalating Exposure, Superior Cooldown
- full (51200 souls): Healbane, Dispel Magic, Toxic Bullets, Ricochet, Escalating Exposure, Superior Cooldown, Inhibitor, Spirit Rend, Titanic Magazine, Boundless Spirit, Headhunter, Leech
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `mirage_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.4`: Fire Scarabs (life steal, -20% target damage)
- `cast 2 0.8`: Dust Devil (lift, evasion after)
- `fire 2.8`: marks apply once per 2.75s per target; marks double (up to 4 stacks, 5s)
- `fire 2.8`
- `fire 2.8`
- `cast 3 0.4`: active: consume all marks (do this right after 3-4 marks)
- `cast 4 0.1`: skip Traveler (map teleport)
- Note: Marks need >=2 shots 2.75s apart; keep accuracy >0 to apply.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `mirage_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (silences stop combo).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Fire Scarabs: steals life (DPS lifesteal, up to 100 stacks, 5s) on the target
- kit: Dust Devil evasion (not heal)
- item: Healbane (HealOnKill)
- item: Spirit Rend (AbilityLifestealPercentHero)
- item: Headhunter (HealPercentPerHeadshot)
- item: Leech (AbilityLifestealPercentHero, BulletLifestealPercent)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`mirage_heal.txt`): full, noheal_items, minus_Healbane, minus_Spirit Rend, minus_Headhunter, minus_Leech, only_Healbane, only_Spirit Rend, only_Headhunter, only_Leech, cand_Healing Booster, cand_Extra Regen, cand_Spirit Lifesteal at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/mirage_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mirage_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mirage_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mirage_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mirage_cc.txt`

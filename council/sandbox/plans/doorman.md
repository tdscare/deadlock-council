# doorman sandbox plan (Rizuhble's Early Checkout Doorman)
Hero enum `Doorman` (UNVERIFIED: internal id hero_doorman exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Call Bell, 2=Doorway, 3=Luggage Cart, 4=Hotel Guest.

Final 12 used in scenarios: Opening Rounds, Rapid Recharge, Spirit Lifesteal, Enchanter's Emblem, Guardian Ward, Tankbuster, Boundless Spirit, Superior Cooldown, Spirit Burn, Greater Expansion, Vortex Web, Cheat Death

## Uncertain slots and substitutes
- Spirit Lifesteal: swap with Healing Booster, Improved Spirit, Extra Regen and none. Why uncertain: Upgrades to Infuser in rich; early sustain vs damage.
- Grit: swap with Extra Health, Reactive Barrier, Spirit Shielding and none. Why uncertain: Early armor slot.

## Economy
Burst Bell/Cart farms waves; High-Velocity Rounds early gun. No Cultist. Check 8k: HVR+Extra Charge+Mystic Burst(7.2k?).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (7200 souls): Mystic Burst, Opening Rounds, Mystic Expansion, Rapid Recharge, Grit
- 12k (11200 souls): Mystic Burst, Opening Rounds, Mystic Expansion, Rapid Recharge, Spirit Lifesteal, Enchanter's Emblem, Guardian Ward
- 20k (18400 souls): Opening Rounds, Mystic Expansion, Rapid Recharge, Spirit Lifesteal, Enchanter's Emblem, Guardian Ward, Slowing Hex, Improved Spirit, Tankbuster, Compress Cooldown
- 30k (24800 souls): Opening Rounds, Mystic Expansion, Rapid Recharge, Spirit Lifesteal, Enchanter's Emblem, Guardian Ward, Slowing Hex, Tankbuster, Boundless Spirit, Superior Cooldown
- full (44800 souls): Opening Rounds, Rapid Recharge, Spirit Lifesteal, Enchanter's Emblem, Guardian Ward, Tankbuster, Boundless Spirit, Superior Cooldown, Spirit Burn, Greater Expansion, Vortex Web, Cheat Death
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `doorman_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.4`: Call Bell (impact + explosion, -40% accuracy, slow)
- `cast 1 0.4`: 2nd bell charge (Extra Charge/T1)
- `cast 3 0.6`: Luggage Cart (60 +0.75 spirit, wall impact stun)
- `fire 1.5`: gun while accuracy-debuffed
- `cast 4 1.8`: Hotel Guest: 1s channel, 7m range; best at close range
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `doorman_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns cancel Hotel Guest).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit; Doorway barrier (T2)
- item: Spirit Lifesteal (AbilityLifestealPercentHero)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`doorman_heal.txt`): full, noheal_items, minus_Spirit Lifesteal, only_Spirit Lifesteal, cand_Healing Booster, cand_Extra Regen at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_cc.txt`

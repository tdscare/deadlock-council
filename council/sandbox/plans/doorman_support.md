# doorman_support sandbox plan (Rizuhble's Concierge Doorman)
Hero enum `Doorman` (UNVERIFIED: internal id hero_doorman exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Call Bell, 2=Doorway, 3=Luggage Cart, 4=Hotel Guest.

Final 12 used in scenarios: Opening Rounds, Rapid Recharge, Trophy Collector, Rescue Beam, Enchanter's Emblem, Heroic Aura, Superior Cooldown, Vortex Web, Divine Barrier, Knockdown, Boundless Spirit, Cheat Death

## Uncertain slots and substitutes
- Healing Rite: swap with Extra Regen, Healing Booster, Grit and none. Why uncertain: Early heal item for a support: does it affect ally survival?
- Trophy Collector: swap with Sprint Boots, Enduring Speed, Veil Walker and none. Why uncertain: Pure-support economy item (rule).

## Economy
Pure support: souls from Trophy Collector passive + assists; farm is poor. Consider Cultist? Rule says Trophy Collector is needed; test economy at ~8k: income vs a farm item.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Opening Rounds, Healing Rite, Grit, Rapid Recharge, Compress Cooldown
- 12k (10400 souls): Opening Rounds, Healing Rite, Rapid Recharge, Compress Cooldown, Guardian Ward, Trophy Collector
- 20k (20000 souls): Opening Rounds, Rapid Recharge, Compress Cooldown, Guardian Ward, Trophy Collector, Rescue Beam, Enchanter's Emblem, Heroic Aura, Slowing Hex, Extra Spirit
- 30k (25600 souls): Opening Rounds, Rapid Recharge, Guardian Ward, Trophy Collector, Rescue Beam, Enchanter's Emblem, Heroic Aura, Slowing Hex, Improved Spirit, Warp Stone, Superior Cooldown
- full (49600 souls): Opening Rounds, Rapid Recharge, Trophy Collector, Rescue Beam, Enchanter's Emblem, Heroic Aura, Warp Stone, Superior Cooldown, Vortex Web, Divine Barrier, Knockdown, Boundless Spirit, Cheat Death
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `doorman_support_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 0.6`: Luggage Cart (alt-cast on mate in the real game: alt target ally; script casts on enemy)
- `cast 2 0.8`: Doorway (barrier T2 first pass)
- `cast 1 0.4`: Call Bell
- `cast 4 1.8`: Hotel Guest
- `fire 1.5`
- Note: Support scoring needs an ally bot; planned `ally` op.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `doorman_support_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Rescue Beam (item) heals ally; Guardian Ward; Heroic Aura
- kit: none in kit
- item: Rescue Beam (HealPercentAmount)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`doorman_support_heal.txt`): full, noheal_items, minus_Rescue Beam, only_Rescue Beam, cand_Healing Rite, cand_Extra Regen, cand_Healing Booster, cand_Veil Walker at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_support_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_support_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_support_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_support_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/doorman_support_cc.txt`

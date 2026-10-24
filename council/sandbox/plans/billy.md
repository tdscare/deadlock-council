# billy sandbox plan (Rizuhble's Mosh Pit Billy)
Hero enum `Punkgoat` (UNVERIFIED: internal id hero_punkgoat exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Bashdown, 2=Rising Ram, 3=Blasted, 4=Chain Gang.

Final 12 used in scenarios: Lifestrike, Enduring Speed, Fortitude, Rapid Recharge, Spirit Resilience, Reactive Barrier, Crushing Fists, Close Quarters, Colossus, Siphon Bullets, Cheat Death, Unstoppable

## Uncertain slots and substitutes
- Cultist Sacrifice: swap with Extra Regen, Healing Rite, Restorative Shot and none. Why uncertain: Rule: Billy cannot farm; Cultist ~8:00. Test economy by souls-gained, not damage.
- Lifestrike: swap with Restorative Shot, Healing Booster, Extra Regen and none. Why uncertain: Heal-on-melee lane fixer; light punches and troopers trigger it. Test at low HP.

## Economy
Billy has an abysmal lane; Cultist Sacrifice at ~8:00 on a big camp (build). Lifestrike works on light melee and troopers. Check at 8k (Melee Lifesteal 800+Monster Rounds 1600+Grit 1600+Extra Health 800+Lifestrike 3200=8000).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Grit, Extra Health, Lifestrike, Cultist Sacrifice
- 12k (12000 souls): Grit, Lifestrike, Cultist Sacrifice, Enduring Speed, Fortitude
- 20k (20000 souls): Grit, Lifestrike, Cultist Sacrifice, Enduring Speed, Fortitude, Melee Charge, Rapid Recharge, Spirit Resilience
- 30k (26400 souls): Lifestrike, Cultist Sacrifice, Enduring Speed, Fortitude, Rapid Recharge, Spirit Resilience, Reactive Barrier, Crushing Fists, Close Quarters
- full (51200 souls): Lifestrike, Cultist Sacrifice, Enduring Speed, Fortitude, Rapid Recharge, Spirit Resilience, Reactive Barrier, Crushing Fists, Close Quarters, Colossus, Siphon Bullets, Cheat Death, Unstoppable
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `billy_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.6`: Rising Ram (T1 +% weapon dmg burst; cd -50% on hit)
- `cast melee 1.2`: heavy melee
- `cast 3 0.5`: Blasted: melee extends, bullets amplified (+10%/17%) vs wrecked
- `fire 1.2`: bullets at wrecked
- `cast melee 1.2`: heavy (extends Blasted)
- `cast 1 0.8`: Bashdown
- `cast 4 2.8`: Chain Gang (needs 2+ enemies for value)
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `billy_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns before reaching).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Melee hits restore ammo (Blasted); Rising Ram T3 +% max HP 11s (buff not heal)
- kit: Items: Melee Lifesteal, Lifestrike, Colossus bonus health
- item: Lifestrike (LifestealHeal, LifestealHealPercent)
- item: Siphon Bullets (HealthStealPctHero)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`billy_heal.txt`): full, noheal_items, minus_Lifestrike, minus_Siphon Bullets, only_Lifestrike, only_Siphon Bullets, cand_Extra Regen, cand_Healing Rite, cand_Restorative Shot, cand_Healing Booster at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/billy_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/billy_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/billy_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/billy_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/billy_cc.txt`

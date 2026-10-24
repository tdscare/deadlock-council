# apollo_melee sandbox plan (Rizuhble's Curb Stomp Apollo)
Hero enum `Fencer` (UNVERIFIED: internal id hero_fencer exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Disengaging Sigil, 2=Riposte, 3=Flawless Advance, 4=Itani Lo Sahn.

Final 12 used in scenarios: Hunter's Aura, Lifestrike, Healing Booster, Stalker, Point Blank, Berserker, Crushing Fists, Spirit Resilience, Witchmail, Phantom Strike, Indomitable, Unstoppable

## Uncertain slots and substitutes
- Stalker: swap with Hunter's Aura, Berserker, Point Blank and none. Why uncertain: T2 melee-chase slot, also sold later; Apollo gap-closes with lunge so Stalker may be redundant.
- Lifestrike: swap with Restorative Shot, Healing Booster, Extra Regen and none. Why uncertain: Lost-lane plan; sustain item choice. Needs low HP.

## Economy
Melee: Melee Lifesteal / Lifestrike feed on troopers - good farm sustain. No Cultist. Melee Charge first for heavy after Riposte.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (6400 souls): Melee Lifesteal, Melee Charge, Extra Regen, Hunter's Aura
- 12k (12000 souls): Melee Charge, Hunter's Aura, Lifestrike, Healing Booster, Close Quarters, Reactive Barrier
- 20k (19200 souls): Melee Charge, Hunter's Aura, Lifestrike, Healing Booster, Reactive Barrier, Stalker, Point Blank, Berserker
- 30k (27200 souls): Hunter's Aura, Lifestrike, Healing Booster, Reactive Barrier, Stalker, Point Blank, Berserker, Crushing Fists, Spirit Resilience
- full (51200 souls): Hunter's Aura, Lifestrike, Healing Booster, Stalker, Point Blank, Berserker, Crushing Fists, Spirit Resilience, Witchmail, Phantom Strike, Indomitable, Unstoppable
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `apollo_melee_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 0.6`: Lunge to close (Melee Charge/Close Quarters stack)
- `cast melee 0.5`: light melee (Lifestrike short cd)
- `cast melee 1.2`: heavy melee - after Riposte stun, with Melee Charge
- `cast 1 0.8`: Sigil
- `cast melee 1.2`: heavy
- `fire 1.5`
- Note: Riposte stun then heavy melee needs a parry event: planned op.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `apollo_melee_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns stop approach).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Flawless Advance T1: 35 per Perfect Hit
- kit: Riposte T3: 75% lifesteal vs target 13s (melee included)
- item: Lifestrike (LifestealHeal, LifestealHealPercent)
- item: Healing Booster (HealAmpCastPercent, HealAmpRegenPercent, BonusHealthRegen)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`apollo_melee_heal.txt`): full, noheal_items, minus_Lifestrike, minus_Healing Booster, only_Lifestrike, only_Healing Booster, cand_Restorative Shot, cand_Extra Regen at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_melee_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_melee_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_melee_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_melee_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/apollo_melee_cc.txt`

# silver sandbox plan (Rizuhble's Pub Brawl Silver)
Hero enum `Werewolf` (UNVERIFIED: internal id hero_werewolf exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Slam Fire, 2=Boot Kick, 3=Entangling Bola, 4=Lycan Curse.

Final 12 used in scenarios: Hunter's Aura, Stalker, Spirit Shielding, Lifestrike, Point Blank, Express Shot, Slowing Hex, Berserker, Unstoppable, Superior Duration, Inhibitor, Frenzy

## Uncertain slots and substitutes
- Restorative Shot: swap with Healing Booster, Extra Regen, Lifestrike and none. Why uncertain: Bought FIRST, sold for Frenzy; is its heal/poke worth a slot early vs plain sustain? Test at low HP.
- Spirit Shielding: swap with Reactive Barrier, Grit, Fortitude and none. Why uncertain: Armor T2 held to late for Diviner's Kevlar; what armor survives best against gun+spirit?

## Economy
Melee-gun bruiser: Restorative Shot + Melee Lifesteal farm waves in melee. No Cultist. Slam Fire gives bonus weapon dmg vs troopers/neutrals (fast camps).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Restorative Shot, Close Quarters, Melee Lifesteal, Hunter's Aura, Stalker, Grit
- 12k (11200 souls): Restorative Shot, Close Quarters, Hunter's Aura, Stalker, Spirit Shielding, Lifestrike
- 20k (20000 souls): Restorative Shot, Hunter's Aura, Stalker, Spirit Shielding, Lifestrike, Point Blank, Express Shot, Duration Extender, Slowing Hex
- 30k (29600 souls): Restorative Shot, Hunter's Aura, Stalker, Spirit Shielding, Lifestrike, Point Blank, Express Shot, Duration Extender, Slowing Hex, Berserker, Unstoppable
- full (44000 souls): Restorative Shot, Hunter's Aura, Stalker, Spirit Shielding, Lifestrike, Point Blank, Express Shot, Slowing Hex, Berserker, Unstoppable, Superior Duration, Inhibitor, Frenzy
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `silver_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.5`: Boot Kick: marks target (3s)
- `fire 0.8`: shoot the mark - bonus damage, removes mark
- `cast 3 0.5`: Bola (slow, no movement abilities)
- `cast 1 0.5`: Slam Fire: instantly reloads, 3 shots at +300% rate; all 3 must hit (+2.5%/7% current HP) - aim rule
- `fire 0.5`: 3 shots
- `cast melee 1.2`: heavy melee
- `cast 4 0.8`: Lycan if rage full (auto at max); may not fill in 40s - pre-fill with hurtme: rage scales with damage dealt/taken
- Note: Lycan rage cannot be forced; log whether it triggered per block.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `silver_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (knockdown/stuns).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Lycan Curse: heals 30% missing health on transform; passive rage fills faster at low HP
- kit: Items only otherwise
- item: Lifestrike (LifestealHeal, LifestealHealPercent)
- item: Frenzy (BulletLifestealPercent)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`silver_heal.txt`): full, noheal_items, minus_Lifestrike, minus_Frenzy, only_Lifestrike, only_Frenzy, cand_Restorative Shot, cand_Healing Booster, cand_Extra Regen at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/silver_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/silver_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/silver_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/silver_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/silver_cc.txt`

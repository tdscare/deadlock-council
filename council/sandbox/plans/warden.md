# warden sandbox plan (Rizuhble's No Witnesses Warden)
Hero enum `Warden` (UNVERIFIED: internal id hero_warden exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Alchemical Flask, 2=Willpower, 3=Binding Word, 4=Last Stand.

Final 12 used in scenarios: Opening Rounds, Titanic Magazine, Swift Striker, Enduring Speed, Fleetfoot, Bullet Resist Shredder, Mercurial Magnum, Spirit Resilience, Vampiric Burst, Spiritual Overflow, Siphon Bullets, Spellslinger

## Uncertain slots and substitutes
- Bullet Lifesteal: swap with Spirit Lifesteal, Healing Booster, Extra Regen and none. Why uncertain: Mid sustain choice: it upgrades to Vampiric Burst late. Test at low HP.
- Fleetfoot: swap with Extra Stamina, Slowing Hex, Reactive Barrier and none. Why uncertain: Mobility mid slot (Sprint Boots+Enduring Speed+Fleetfoot): three speed items - which pays off?

## Economy
Gun carry with strong 1v1: gun farms; no Cultist. Extended Magazine/Rapid Rounds early. Check 8k.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Opening Rounds, Titanic Magazine, Swift Striker, Quicksilver Reload, Battle Vest
- 12k (11200 souls): Opening Rounds, Titanic Magazine, Swift Striker, Quicksilver Reload, Battle Vest, Bullet Lifesteal, Enduring Speed
- 20k (16000 souls): Opening Rounds, Titanic Magazine, Swift Striker, Quicksilver Reload, Battle Vest, Bullet Lifesteal, Enduring Speed, Fleetfoot, Spirit Lifesteal, Bullet Resist Shredder
- 30k (28800 souls): Opening Rounds, Titanic Magazine, Swift Striker, Battle Vest, Enduring Speed, Fleetfoot, Spirit Lifesteal, Bullet Resist Shredder, Mercurial Magnum, Spirit Resilience, Vampiric Burst
- full (46400 souls): Opening Rounds, Titanic Magazine, Swift Striker, Battle Vest, Enduring Speed, Fleetfoot, Bullet Resist Shredder, Mercurial Magnum, Spirit Resilience, Vampiric Burst, Spiritual Overflow, Siphon Bullets, Spellslinger
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `warden_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 0.5`: Binding Word: enemy must stay put 2.8s; trap then +bullet dmg (T1 +20%?)
- `cast 1 0.5`: Flask: -25% weapon damage, slow, T3 fire-rate slow
- `fire 2.5`: shoot the trapped target
- `cast i1 0.3`: Vampiric Burst while target is trapped (Late)
- `cast 2 0.3`: Willpower barrier
- `cast 4 8.2`: Last Stand heal channel (needs low HP to show healing)
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `warden_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (Last Stand T3 gives Unstoppable; before that stuns catch you as you walk in).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Last Stand: pulses heal 75% of damage to heroes (10% non-hero), 6s after 2s charge, +50% resists
- kit: Bullet Lifesteal/Vampiric Burst; Siphon Bullets
- item: Vampiric Burst (ActiveBonusLifesteal, BulletLifestealPercent)
- item: Spiritual Overflow (AbilityLifestealPercentHero, BonusSpiritLifesteal)
- item: Siphon Bullets (HealthStealPctHero)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`warden_heal.txt`): full, noheal_items, minus_Vampiric Burst, minus_Spiritual Overflow, minus_Siphon Bullets, only_Vampiric Burst, only_Spiritual Overflow, only_Siphon Bullets, cand_Bullet Lifesteal, cand_Spirit Lifesteal, cand_Healing Booster, cand_Extra Regen at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/warden_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/warden_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/warden_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/warden_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/warden_cc.txt`

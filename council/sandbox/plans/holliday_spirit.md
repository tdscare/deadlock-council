# holliday_spirit (Holliday, enum `Astro` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: holliday_spirit_swap1, holliday_spirit_swap2, holliday_spirit_heal (runnable now, existing ops), holliday_spirit_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Tankbuster: vs Torment Pulse, Spirit Snatch, Surge of Power, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Recharging Rush: vs Mystic Shot, Opening Rounds, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Rapid Recharge (next: Recharging Rush; 1 bought)
- ~12k: Rapid Recharge, Recharging Rush (next: Stamina Mastery; 2 bought)
- ~20k: Recharging Rush, Stamina Mastery, Duration Extender, Mystic Vulnerability, Tankbuster, Superior Duration (next: Compress Cooldown; 7 bought)
- ~30k: Mystic Vulnerability, Tankbuster, Superior Duration, Compress Cooldown, Boundless Spirit, Superior Cooldown (next: Spirit Burn; 10 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 4 0.6']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.3', 'cast 1 0.3', 'fire 1', 'cast 3 0.2', 'fire 1'].
Two kegs back to back (2 charges), shoot to detonate, Crackshot, Lasso opener. Tankbuster only procs off Crackshot/Lasso (keg 159 < 165): must show the swap result with Tankbuster vs none under the full rotation.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Kit: none; Items: Trophy Collector (souls), Extra Health, Fortitude; no lifesteal item in core
Item heal sources in the full build: Headshot Booster, Trophy Collector, Tankbuster, Boundless Spirit, Superior Cooldown, Spirit Burn, Fortitude.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

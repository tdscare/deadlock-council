# holliday (Holliday, enum `Astro` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: holliday_swap1, holliday_swap2, holliday_heal (runnable now, existing ops), holliday_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Fortitude: vs Metal Skin, Veil Walker, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Glass Cannon: vs Crippling Headshot, Armor Piercer, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Headhunter (next: Fortitude; 1 bought)
- ~12k: Headhunter, Fortitude, Bullet Lifesteal (next: Bullet Resist Shredder; 3 bought)
- ~20k: Headhunter, Fortitude, Bullet Lifesteal, Bullet Resist Shredder, Long Range, Rapid Recharge (next: Stamina Mastery; 6 bought)
- ~30k: Bullet Lifesteal, Bullet Resist Shredder, Long Range, Rapid Recharge, Stamina Mastery, Lucky Shot (next: Glass Cannon; 8 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 3 0.2', 'cast 4 0.6']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.3', 'cast 1 0.3', 'fire 2', 'cast 3 0.2'].
Crackshot on headshot (T3: -6s CD per headshot, bullet resist reduction), shoot barrels to detonate, Lasso opener. Check body/head mix since Crackshot CD relies on headshots.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Kit: none (no lifesteal); Items: Bullet Lifesteal, Fortitude, Vampiric Burst, Extra Health
Item heal sources in the full build: Headhunter, Fortitude, Glass Cannon, Vampiric Burst.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

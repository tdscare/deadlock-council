# abrams_melee (Abrams, enum `Atlas` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: abrams_melee_swap1, abrams_melee_swap2, abrams_melee_heal (runnable now, existing ops), abrams_melee_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Spirit Snatch: vs Torment Pulse, Burst Fire, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Lifestrike: vs Spirit Lifesteal, Bullet Lifesteal, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Melee Charge, Stalker, Lifestrike (next: Bullet Resist Shredder; 3 bought)
- ~12k: Melee Charge, Stalker, Lifestrike, Bullet Resist Shredder (next: Point Blank; 4 bought)
- ~20k: Stalker, Lifestrike, Bullet Resist Shredder, Point Blank, Spirit Snatch, Hunter's Aura (next: Crushing Fists; 7 bought)
- ~30k: Bullet Resist Shredder, Point Blank, Spirit Snatch, Hunter's Aura, Crushing Fists, Berserker (next: Spirit Resilience; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 2 0.8', 'cast 4 0.8']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast melee 0.4', 'cast melee 0.4', 'cast melee 0.4', 'cast 2 0.8'].
Charge into wall for a guaranteed heavy, then punches (Lifestrike/Melee Charge/Crushing Fists), ult after. Heal sources are item-dominated: run the heal blocks.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Infernal Resilience: melee lifesteal +18% at T2, regen 13%/9% of damage taken; Siphon Life (low priority, T1 only late); Melee Lifesteal, Lifestrike (light melee longer CD, troopers), Restorative Shot
Item heal sources in the full build: Restorative Shot, Stalker, Lifestrike, Enduring Speed, Point Blank, Spirit Snatch, Hunter's Aura, Spirit Resilience, Colossus.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

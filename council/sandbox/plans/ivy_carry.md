# ivy_carry (Ivy, enum `Tengu` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: ivy_carry_swap1, ivy_carry_swap2, ivy_carry_heal (runnable now, existing ops), ivy_carry_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Intensifying Magazine: vs Opening Rounds, Fleetfoot, Swift Striker, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Fortitude: vs Metal Skin, Veil Walker, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Tesla Bullets, Intensifying Magazine (next: Active Reload; 2 bought)
- ~12k: Tesla Bullets, Intensifying Magazine, Active Reload (next: Fortitude; 3 bought)
- ~20k: Tesla Bullets, Intensifying Magazine, Active Reload, Fortitude, Stamina Mastery, Headhunter (next: Capacitor; 6 bought)
- ~30k: Fortitude, Stamina Mastery, Headhunter, Capacitor, Bullet Resist Shredder, Siphon Bullets (next: Silencer; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: none. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.3', 'fire 2', 'cast 3 1.0', 'fire 2'].
Thorns first (applies Bullet Resist Shredder via spirit damage), fire for ~2.4s clip, Stone Form for stun/heal.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Kudzu T2 bullet lifesteal 15%+8 (T3 always active, 50% when not connected); Stone Form heal; Items: Siphon Bullets (late), Inhibitor
Item heal sources in the full build: Monster Rounds, Active Reload, Fortitude, Headhunter, Siphon Bullets, Inhibitor.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

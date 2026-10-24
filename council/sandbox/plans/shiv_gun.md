# shiv_gun (Shiv, enum `Shiv` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: shiv_gun_swap1, shiv_gun_swap2, shiv_gun_heal (runnable now, existing ops), shiv_gun_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Hunter's Aura: vs Burst Fire, Point Blank, Hollow Point, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Bullet Lifesteal: vs Spirit Lifesteal, Healing Booster, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- NOTES: swap2: 'Bullet Lifesteal' not a final item (consumed by upgrade); skipped

## Economy and price points
- ~8k: Express Shot, Battle Vest (next: Radiant Regeneration; 2 bought)
- ~12k: Express Shot, Battle Vest, Radiant Regeneration (next: Dispel Magic; 3 bought)
- ~20k: Battle Vest, Radiant Regeneration, Dispel Magic, Bullet Resist Shredder, Hunter's Aura, Fleetfoot (next: Bullet Lifesteal; 7 bought)
- ~30k: Dispel Magic, Bullet Resist Shredder, Hunter's Aura, Fleetfoot, Bullet Lifesteal, Berserker (next: Lucky Shot; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 3 0.2']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['fire 2', 'cast 1 0.3', 'fire 1.5', 'cast 2 0.5', 'cast 4 0.5'].
Gun builds rage; knife applies Bullet Resist Shredder only if a hit counts (bleed-only is unverified, test with and without a knife first).

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Radiant/Mystic Regeneration; Items: Bullet Lifesteal, Restorative Shot, Vampiric Burst (late)
Item heal sources in the full build: Restorative Shot, Battle Vest, Radiant Regeneration, Dispel Magic, Hunter's Aura, Vampiric Burst, Inhibitor.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

# billy_damage (Billy, enum `Punkgoat` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: billy_damage_swap1, billy_damage_swap2, billy_damage_heal (runnable now, existing ops), billy_damage_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Spirit Snatch: vs Hunter's Aura, Burst Fire, Fleetfoot, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Silencer: vs Lucky Shot, Glass Cannon, Crippling Headshot, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Stalker, Cultist Sacrifice (next: Lifestrike; 2 bought)
- ~12k: Stalker, Cultist Sacrifice, Lifestrike, Melee Charge (next: Bullet Resist Shredder; 4 bought)
- ~20k: Cultist Sacrifice, Lifestrike, Melee Charge, Bullet Resist Shredder, Spirit Snatch, Point Blank (next: Crushing Fists; 7 bought)
- ~30k: Melee Charge, Bullet Resist Shredder, Spirit Snatch, Point Blank, Crushing Fists, Rapid Recharge (next: Berserker; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is in this build. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 4 0.5']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 2 0.8', 'cast 3 0.5', 'cast 1 0.6', 'cast melee 0.4', 'cast melee 0.4'].
Ram first (closes gap, CD halves on hit), Blasted active, Bashdown (light melee -> Lifestrike/Spirit Strike/Snatch procs; Bashdown T3 heavy), then punches; Chain Gang (175s CD) once at block start. Cultist: 6.4k at ~8:00, test only its buff (+30 weapon, +50 HP) by giving it; income effect needs the timeline sim.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Blasted: melee hits reload ammo (no heal); Rising Ram T3: +max HP buff on hero hit (not a heal); Chain Gang: none
Item heal sources in the full build: Stalker, Cultist Sacrifice, Lifestrike, Spirit Shielding, Spirit Snatch, Point Blank, Colossus, Scourge.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

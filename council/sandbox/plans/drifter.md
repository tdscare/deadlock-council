# drifter (Drifter, enum `Drifter` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: drifter_swap1, drifter_swap2, drifter_heal (runnable now, existing ops), drifter_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Hollow Point: vs Burst Fire, Weighted Shots, Berserker, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Battle Vest: vs Spirit Shielding, Weapon Shielding, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Stalker, Kinetic Dash (next: Bullet Lifesteal; 2 bought)
- ~12k: Stalker, Kinetic Dash, Bullet Lifesteal, Lifestrike (next: Battle Vest; 4 bought)
- ~20k: Kinetic Dash, Bullet Lifesteal, Lifestrike, Battle Vest, Point Blank, Hunter's Aura (next: Hollow Point; 7 bought)
- ~30k: Lifestrike, Battle Vest, Point Blank, Hunter's Aura, Hollow Point, Vampiric Burst (next: Lucky Shot; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 4 1.2']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 2 0.3', 'cast 2 0.3', 'cast 1 0.6', 'cast melee 0.4', 'fire 2'].
Eternal Night makes targets isolated (Bloodscent amp 15%), Stalker's Mark then recast to blink behind, Rend close range (<8m bonus), melee, shoot.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Bloodscent T2: heal 24% of missing health + stamina on isolated hero kill (kill-gated, hard to test); Items: Melee Lifesteal, Bullet Lifesteal, Lifestrike (maxed Rend counts heavy), Vampiric Burst, Leech (rich)
Item heal sources in the full build: Stalker, Trophy Collector, Lifestrike, Battle Vest, Point Blank, Hunter's Aura, Hollow Point, Vampiric Burst.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

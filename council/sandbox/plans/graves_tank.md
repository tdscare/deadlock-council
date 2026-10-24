# graves_tank (Graves, enum `Necro` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: graves_tank_swap1, graves_tank_swap2, graves_tank_heal (runnable now, existing ops), graves_tank_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Torment Pulse: vs Decay, Radiant Regeneration, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Spirit Lifesteal: vs Bullet Lifesteal, Healing Booster, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- NOTES: swap2: 'Spirit Lifesteal' not a final item (consumed by upgrade); skipped

## Economy and price points
- ~8k: Mystic Vulnerability, Torment Pulse, Enchanter's Emblem (next: Stamina Mastery; 3 bought)
- ~12k: Mystic Vulnerability, Torment Pulse, Enchanter's Emblem, Stamina Mastery, Spirit Shredder (next: Toxic Bullets; 5 bought)
- ~20k: Enchanter's Emblem, Stamina Mastery, Spirit Shredder, Toxic Bullets, Spirit Lifesteal, Spirit Resilience (next: Escalating Resilience; 8 bought)
- ~30k: Spirit Shredder, Toxic Bullets, Spirit Lifesteal, Spirit Resilience, Escalating Resilience, Escalating Exposure (next: Superior Cooldown; 10 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: none. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 2 0.8', 'cast 1 0.4', 'fire 2'].
Hands to immobilize in melee range, Jar, shoot; Torment Pulse needs enemies within 9m.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Jar T1 pickup heal; Items: Spirit Lifesteal, Extra Regen, Leech/Siphon Bullets late
Item heal sources in the full build: Extra Regen, Torment Pulse, Enchanter's Emblem, Spirit Shredder, Toxic Bullets, Spirit Resilience, Escalating Resilience, Superior Cooldown, Siphon Bullets, Scourge, Leech.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

# nurse (Nurse Harrow, enum `Nurse` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: nurse_swap1, nurse_swap2, nurse_heal (runnable now, existing ops), nurse_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Burst Fire: vs Hunter's Aura, Heroic Aura, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Toxic Bullets: vs Spirit Rend, Hollow Point, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Compress Cooldown (next: Surge of Power; 1 bought)
- ~12k: Compress Cooldown, Surge of Power, Burst Fire (next: Spirit Lifesteal; 3 bought)
- ~20k: Surge of Power, Burst Fire, Spirit Lifesteal, Debuff Reducer, Superior Cooldown, Toxic Bullets (next: Guardian Ward; 7 bought)
- ~30k: Spirit Lifesteal, Debuff Reducer, Superior Cooldown, Toxic Bullets, Guardian Ward, Boundless Spirit (next: Unstoppable; 9 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 2 0.3']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.4', 'cast 3 0.5', 'fire 2', 'cast 4 1.5'].
Needs a friendly target for needles/Vapors/Overflow: request planned op `ally`. Leeches must be picked up (wait after jar). Vapors on self also tests the numb/crash trade.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Leech Therapy: pickup heals health drained + permanent spirit power; Healing Needles: heal allies 25+0.2x per shot; Wretched Vapors: healing effectiveness +20% T2; Items: Spirit Lifesteal -> Spiritual Overflow (procs on friendly hits), Vampiric Burst, Healing Tempo, Healing Booster
Item heal sources in the full build: Superior Cooldown, Toxic Bullets, Guardian Ward, Boundless Spirit, Unstoppable, Vampiric Burst, Spiritual Overflow, Healing Tempo.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

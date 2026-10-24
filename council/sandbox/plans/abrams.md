# abrams (Abrams, enum `Atlas` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: abrams_swap1, abrams_swap2, abrams_heal (runnable now, existing ops), abrams_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Healing Booster: vs Spirit Lifesteal, Restorative Locket, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Spirit Snatch: vs Torment Pulse, Radiant Regeneration, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Arcane Surge, Duration Extender, Healbane (next: Enduring Speed; 3 bought)
- ~12k: Arcane Surge, Duration Extender, Healbane, Enduring Speed, Compress Cooldown (next: Spirit Snatch; 5 bought)
- ~20k: Enduring Speed, Compress Cooldown, Spirit Snatch, Superior Duration, Superior Cooldown, Mystic Vulnerability (next: Greater Expansion; 9 bought)
- ~30k: Spirit Snatch, Superior Duration, Superior Cooldown, Mystic Vulnerability, Greater Expansion, Witchmail (next: Scourge; 11 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 4 0.8']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.5', 'cast 2 0.8', 'cast 3 0.2', 'fire 2'].
Seismic Impact (leap, unstoppable at T3) opens, then Siphon (imbued: Duration Extender, Mystic Expansion, Compress Cooldown), Shoulder Charge, shoot. Incoming damage matters: Infernal regen needs damage taken.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Siphon Life: HealingFactor 70% of damage (35% non-hero), 0.25s ticks, 4s; Infernal Resilience: BonusHealthRegen 1 + regens 13% of damage taken over 20s (T2 melee lifesteal 18, T3 +9%)
Item heal sources in the full build: Healing Booster, Enduring Speed, Spirit Snatch, Superior Cooldown, Scourge, Boundless Spirit, Healbane.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

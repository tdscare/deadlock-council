# mokrill (Mo & Krill, enum `Krill` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: mokrill_swap1, mokrill_swap2, mokrill_heal (runnable now, existing ops), mokrill_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Torment Pulse: vs Decay, Radiant Regeneration, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Tankbuster: vs Surge of Power, Spirit Snatch, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Quicksilver Reload, Cold Front (next: Fortitude; 2 bought)
- ~12k: Quicksilver Reload, Cold Front, Fortitude (next: Torment Pulse; 3 bought)
- ~20k: Cold Front, Fortitude, Torment Pulse, Compress Cooldown, Mystic Vulnerability, Duration Extender (next: Superior Duration; 7 bought)
- ~30k: Mystic Vulnerability, Duration Extender, Superior Duration, Healbane, Tankbuster, Superior Cooldown (next: Boundless Spirit; 11 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: none. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 3 0.4', 'cast 1 0.5', 'cast 4 2.6', 'cast 1 0.5', 'fire 1'].
Sand Blast disarm first, Scorn (imbues stack: Quicksilver, Compress, Mystic Expansion, radius 9m), Combo needs 4m (fetch close) and channels 2.4s (T3 longer). Burrow (2) for gap/armor.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Scorn: heals on damage dealt, 120% vs heroes, 35% vs non-hero (main sustain); Combo T1: +100% lifesteal on hit; Items: Healbane, Fortitude
Item heal sources in the full build: Enduring Speed, Fortitude, Torment Pulse, Tankbuster, Superior Cooldown, Boundless Spirit, Colossus, Healbane.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

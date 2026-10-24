# ivy (Ivy, enum `Tengu` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: ivy_swap1, ivy_swap2, ivy_heal (runnable now, existing ops), ivy_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Heroic Aura: vs Rescue Beam, Healing Nova, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Rapid Recharge: vs Surge of Power, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Titanic Magazine, Headhunter (next: Heroic Aura; 2 bought)
- ~12k: Titanic Magazine, Headhunter (next: Heroic Aura; 2 bought)
- ~20k: Titanic Magazine, Headhunter, Heroic Aura, Rapid Recharge, Compress Cooldown, Healbane (next: Healing Tempo; 6 bought)
- ~30k: Heroic Aura, Rapid Recharge, Compress Cooldown, Healbane, Healing Tempo, Duration Extender (next: Cursed Relic; 8 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: none. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.3', 'cast 3 1.0', 'cast 2 0.3', 'fire 2', 'cast 1 0.3'].
Needs a friendly teammate for Kudzu/Air Drop/Headhunter pass-down; a solo run tests 50% bonuses only. Request planned op `ally <Hero>` (second bot on my team).

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Kudzu Connection: shares healing (35%+) with tethered ally, T2 +bullet lifesteal 15%+0.15x spirit (needs ally for full bonus, 50% alone); Stone Form: heal % of max HP (MaxHealthRegen 6); Items: Healing Booster, Healing Tempo, Headhunter heals
Item heal sources in the full build: Headhunter, Enduring Speed, Healing Tempo, Superior Cooldown, Divine Barrier, Siphon Bullets, Healbane.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

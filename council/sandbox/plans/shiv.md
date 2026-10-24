# shiv (Shiv, enum `Shiv` unverified) sandbox plan
Source: gen/mk_plan.py. Scenarios in /mnt/user-data/outputs/dwpkg2/scenarios/: shiv_swap1, shiv_swap2, shiv_heal (runnable now, existing ops), shiv_cond (needs planned ops reset/accuracy/enemies/resist).

## Uncertain slots and substitutes (final-item names; same tier unless noted)
- Enchanter's Emblem: vs Healing Booster, Guardian Ward, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).
- Decay: vs Torment Pulse, Surge of Power, none. Uncertain because its value depends on the rotation/conditions below (see audit gen/ac_out3.md for threshold margins).

## Economy and price points
- ~8k: Radiant Regeneration, Compress Cooldown, Enchanter's Emblem (next: Spirit Lifesteal; 3 bought)
- ~12k: Radiant Regeneration, Compress Cooldown, Enchanter's Emblem, Spirit Lifesteal (next: Torment Pulse; 4 bought)
- ~20k: Enchanter's Emblem, Spirit Lifesteal, Torment Pulse, Mystic Vulnerability, Superior Cooldown, Rapid Recharge (next: Healbane; 8 bought)
- ~30k: Mystic Vulnerability, Superior Cooldown, Rapid Recharge, Healbane, Decay, Leech (next: Dispel Magic; 11 bought)
- Souls: farm with kit as in notes; Cultist Sacrifice (6.4k, 170% bonus souls on one camp, 270s CD, +30 weapon power, +50 HP) is not in this build; candidate only if the hero cannot farm (unverified for this hero), swap target = lowest-value early T1/T2 item. Sandbox cannot measure income: run each price point as `souls <n>` + the items owned at that point and compare damage/ammo/cooldown/HP.
- Run block at 8k, 12k, 20k, 30k and full with the same rotation; report cooldown readiness before the next cycle, ammo reloads, HP lost per cycle.

## Rotation (scenario ops)
Opener once per block: ['cast 3 0.2']. Cycle (x2, `fetch 350` before each op, `hurtme 150` after): ['cast 1 0.3', 'cast 1 0.3', 'cast 2 0.5', 'cast 4 0.5', 'cast melee 0.3'].
Knives x2 (2 charges, stacking bleed), dash (CD -2s per hero hit at T3), Killing Blow when target <18% (200 dmg; recast 16s after a kill), melee builds rage. Full rage unlocks echo dash, so build rage before the dash.

## Heal sources (game data; see TEST_MATRIX Healing attribution)
Kit: Bloodletting: defers 25% damage, active clears 30% of deferred (not a heal); Radiant/Mystic Regeneration, Spirit Lifesteal, Leech, Healbane
Item heal sources in the full build: Radiant Regeneration, Enchanter's Emblem, Spirit Shielding, Torment Pulse, Superior Cooldown, Decay, Leech, Dispel Magic, Mystic Reverb, Spirit Burn, Healbane.
Blocks (_heal): all heal items, each one removed (leave-one-out), all removed = baseline. Marginal healing of any slot item = (block with item) - (baseline), read from damage csv heal events by source if logged, else by removal. Start at hurtme 800, repeat hurtme 150 per op so HP stays low; add a high-HP run (heal full, no hurtme) to show the cap.

## Conditions
Accuracy 100/50/40 and body/head mix (planned `accuracy`, and head-only vs body-only aimoff pitch); 1 enemy vs 4-5 (`enemies 4`); incoming gun+spirit damage via `hurtme` now, planned `enemies` shooting back later; low HP start (done); stacks 0/1/max where the build has them (Berserker, Escalating items, Essence Theft ramp, Metal/rage); resist runs `resist 0 0` vs `resist 20 20` for shred items; CC: apply stun/silence via the bot (planned) and check answers named in the Counters box (Unstoppable, Dispel, Counterspell). 3 passes, order fwd/rev/fwd already in each file; discard the first block (warm-up).

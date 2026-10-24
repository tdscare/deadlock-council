VALID: yes (instrument checks: build 06:00 post location patch; arena SETUP/POS VERIFY ok at every block start; abilities read back with `abilist` before each measurement; 1 run per cell, deterministic hits)
# Grey Talon (Orion) foundation checks F7/F9, run 2026-10-24 06:13-06:16, scenario gt_f7_f9 (= autorun/scenarios/gt_f7_f9_charge_bits.txt). MEASURED.
Charged Shot (Signature1), 4 charge attempts 1.5 s apart (6 s window), enemy Haze 350u, 100% hit, read-back bits confirmed by `abil` log lines.

| block | bits (read back) | item | hits in window | damage per hit | timing |
|---|---|---|---|---|---|
| A | 1 | none | 1 | 136 | - |
| B | 1 | Extra Charge | 2 | 150 | 2nd hit 5.0 s after 1st |
| C | 3 | none | 1 | 136 | - |
| D | 7 | Extra Charge | 2 | 204 | 5.0 s apart |
| E | 15 | Extra Charge | 2 | 274 | 1.65 s apart |
| F | 15 | none | 1 | 246 | - |

Findings
- F9 schema CONFIRMED: bit0 = unlocked, 3 = T1, 7 = T2, 15 = T3. T2 adds +54 damage (150 -> 204 with EC), T3 adds +70 more (204 -> 274) and cuts the between-charge time from ~5 s to ~1.65 s; both consistent with the written kit (T2 +54, T3 +1.0x). `unlock 7` earlier = T2, NOT T3; full tier = 15.
- F7 CONFIRMED: Extra Charge adds a second charge to a 1-charge ability (A 1 hit vs B 2 hits, 5.0 s between). It also raises per-hit damage: 136 -> 150 (+10.3%) at bits 1 and 246 -> 274 (+11.4%) at bits 15 (the item's spirit power adds to the ability).
- T1 (bits 3) showed no extra charge and no damage change vs bits 1 in this ability (C = A): whatever Charged Shot T1 gives is not visible in hits/damage here (unresolved: may be cooldown or charge time; not measured).
- Wraith Full Auto cross-check (bitstest, FA cooldown by `cast 3` then abilist cd flag): bits 1 -> still cooling after 38 s; bits 3 -> ready at 26 s (FA T1 = -20 s cooldown from 45 s ~ 25 s) MEASURED. bits 7/15 not run (a foreign hero select and shop purchases hit the client at 06:06-06:09, aborting the block; see interference note).
What would make this wrong: single run per cell (damage is deterministic so identical repeats are expected, not verified); `abil` writes UpgradeBits directly, so this does not test the game's point-spend rules.
## Check (2) ability-point queue (unlock B while A's next tier is unaffordable): NOT RUN. Needs the real point-spend path (client upgrade command or UI); `abil` bypasses it. UNTESTABLE with current ops.
## Interference (record): at 06:06:40 and 06:06:56 CLIENTCMD `selecthero hero_punkgoat` and at 06:08-06:09 many `buyitem`/`sellitem` client commands appeared in plugin.log while bitstest was running (not issued by the scenario); my hero became PunkGoat and setup timed out. Something else is driving the game client. Blocks overlapping 06:06-06:11 are INVALID. Please keep the client free during runs.

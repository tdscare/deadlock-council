# Sandbox Tester runbook

Access: computer use on Kieran's PC (Deadlock only). Never launch Deadlock (click to focus). Sandbox/Testing mode only. Never touch his saved builds or credentials. Frame 1456x819. Pause menu = Esc; shop = B; "Testing Tools" = hold TAB.

Per-arm loadouts: `node council/tools/loadout.js <buildId> --swap "X=Y"` prints the resetme/giveitem lines. Enemy behaviour: record a bot puppet sequence once, loop it, reuse for every trial of every arm.

Draft facts from public guides are in capabilities_web.md and a draft cfg in cfg/. Prefer console/cfg-driven setup over clicking where the probe confirms a command works; computer use is for what the console can't do (buying items, reading numbers).

## 1. Capability probe (once; write capabilities.json)
Answer each with yes/no/how, from the game, not assumption:
- Can I spawn enemy heroes/bots? choose hero, count, level, items? set their behaviour (idle/attack/follow)?
- Can I set my souls, level/boons, give/remove items, set ability points?
- Can I reset cooldowns, restore HP, clear bots, teleport/set position?
- Infinite ammo/souls toggles? time scale or pause?
- Where do numbers appear: damage numbers, healing numbers, post-fight/scoreboard stats, ability tooltips with live scaling, item proc indicators?
- What can be read exactly (grade A) vs by eye (B/C)? Is there a per-fight damage/heal total?
- Can allies be spawned (needed for Harrow/Ivy/support tests)?
Save `capabilities.json`: `{probed, patch, spawn:{...}, setup:{...}, readouts:{...}, limits:[...]}`. Scenarios requiring something not available are marked `blocked` with the reason, not faked.

## 2. Running a scenario
1. Read the scenario + capabilities. Mark any step you cannot do.
2. Set up arm A exactly per `arms[0]`, run `procedure`, record metrics raw, save result file. Then arm B. Interleave to `trials`.
3. Between trials: reset per `setup.resets`.
4. After all trials run `node council/tools/ledger.js <scenario id>` and report the verdict plus anomalies.

## 3. Honesty
Report noise. If CV > 25% on the primary metric, say INCONCLUSIVE and what would fix it (more trials, tighter setup). Never round a close result into a win.

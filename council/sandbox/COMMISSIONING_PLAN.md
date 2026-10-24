# Background testing: commissioning plan (one approval)
Nothing runs until Kieran approves. Build used: 4b24b567 (already compiled, hash-verified, already deployed). No rebuilds unless something blocks. Not a competitive-match moment; a casual game, idle desktop or browsing is fine.

## What Kieran does
1. Double-click launcher_hidden.vbs once (starts the hidden supervisor). That is the only start action.
2. If he has Deadlock open, join the server once when I tell him it is up (his own client, as before). This is needed only because a real client is the only thing the current build accepts as a session (see Phase 1). Not needed for Phase 1's window test.
Everything else I do through the plugin and supervisor request files. No mouse, keyboard or focus from me.

## Phase 1, safety smoke test (10-15 min)
- Start the server hidden (v5 launcher; telemetry and probe_windows running). Pass: no visible window from deadworks/cmd/powershell/dotnet/wscript, MainWindowHandle 0, no foreground change caused by our processes. Only changes tied to our PIDs or new windows we own count. Kieran Alt-Tabbing is ignored.
- Server stable 10 min: frame summaries normal (avg ~15.6 ms, no frame over 250 ms), plugin loads, PAUSE still in place, queue.json unchanged (26 done kept).
- Session handling: his client joins, connect-assist picks the hero, session gate reports a valid session. Then an abort control test: sbx_q pause and stop.req both work.
- Unattended input source decision: default = real client with the gate (the only path in the verified build). Headless (Server.CreateFakeClient as the tested hero) is checked with existing bot commands for 3 min: can a bot be the caster, take hits and run the same ops. If yes it is recorded as the preferred next step, but making it the session source needs a plugin change (new build, asked separately). If the real client disconnects, the gate pauses safely and the task is refunded; reconnecting is still manual until headless is done. Honest limit: fully unattended reconnect is NOT solved by this run.
- Fix only real blockers. Any window or focus change from us = stop, fix, ask again.

## Phase 2, small real batch (15-30 min, about 3-4 tasks)
Picked by readiness and value from the saved pending tasks (all are Council hypotheses feeding hero builds):
1. disc:T2_97edcd8e6a, Viscous: does Echo Shard let The Cube be cast twice, and what the second cast does (decides the Echo Shard imbue combo).
2. disc:T4_da3e1d605b, Nurse: whether Lurking Terrors blocks item actives such as Rusted Barrel while channelling.
3. disc:T5_2f170e43b3, Viscous: does Crushing Fists boost Puddle Punch (heavy-melee bonus from ability damage). Previous attempt hit a harness slot-check bug, so I send the prepared retry first.
4. If time: act:ar2, then cap:test1.
For each I report: mechanic, what was measured, valid or invalid, effect on the hero build or hypothesis. Checks per task: clean start state (statecheck), real triggers/hits recorded, session key unchanged, timeouts honoured. Failed or interrupted runs are never evidence. Concurrently: telemetry plus frame summaries; target = no stutter reported, no frame over 250 ms, server CPU modest. Not zero usage.
Caveat: these tasks cast through plugin ops and are tick-based, so they should not depend on usercmd arrival. The timing-invalidation code (HostLoad) is not in this build, so validity is checked after the fact from frame summaries and the unfocused-client stats.

## Phase 3, continuous operation
If Phases 1-2 pass (no windows, stable, trustworthy results, Kieran notes no stutter): lift PAUSE and run the queue continuously inside these limits: hidden launch only, server BelowNormal, one task at a time, builds only through the maintenance protocol, telemetry on. No per-experiment approval. Autonomous recovery: server restart max 3/hour, refunded aborts, retries with backoff, defer expensive work under load. Stop and ask for: new plugin deploy, environment/launch changes, anything needing focus or input, a window/focus change from us, more than 3 crashes/hour.

## Abort and rollback
Abort on: any window/focus change from our processes, Kieran says stop or reports stutter, frame over 250 ms or avg over 18 ms for 30 s, crash marker, session-gate failure. Abort action: write PAUSE, sbx_q maint begin, stop.req, telemetry/probe are read-only. Rollback: queue.json restored from the pre-run snapshot, deployed DLL untouched, old scripts untouched (new files live in staged_v5).

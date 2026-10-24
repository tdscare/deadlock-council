# Queue runner demo - results (replaces the checklist)

VALID: yes (demo infrastructure test; 9 required tasks + 2 extra, results produced by the plugin queue runner, not by hand)
SCOPE: queue/runner behaviour only. No game-balance measurement. Built into plugin SandboxTester; commands only via sbx_q / sbx_cmd files; no mouse/keyboard/focus input sent.
ENV: client was foreground for part of the run, background for the rest (see FG lines in plugin.log). Not a measurement environment.
Log: E:\deadworks-server\sbx_logs\plugin.log (excerpts below are verbatim, local time = UTC+1)

## Result table

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| A | 9-task demo runs to completion with client connected | PASS (7 done, demo:broken and demo:wall blocked by design, demo:fg needs-foreground by design; plus demo:int1 done) | TASK-RESULT lines below |
| B | Validity checks hold (unknown op, exceptions, VERIFY fail, human input, forced external, setup verify) | PASS | demo:broken -> `VALID=no 1x unknown op` |
| C | Results written per attempt + final | PASS | results\<task>.json and .aN.json; sha256 list in queue_demo_final_sha256.txt |
| D | Reconciliation total = sum of states | PASS | `reconciled total=9=sum-of-states`, later `total=23=sum-of-states` |
| E | Mid-run interruption via plugin reload (sbx_build) resumes, nothing lost, attempt refunded | PASS | rz_final#1 -> reload -> rz_final#2, `QR LOAD ... orphanedRunningReset=1`, later VALID=yes; same for arena_smoke2, int1 |
| F | Second controller refused / takeover protection | PASS | `QR TASK-ABORT demo:rz_inc#1 another controller took over refund=True`, resumed after lock freed; `QR FORCED takeover ... owner=claude-orchestrator-LLM-session-2` only via explicit `sbx_q start force` |
| G | External sbx_scenario/raw refused while runner active | PASS | `QR REFUSED queue-file line 'sbx_scenario smoke' ... reason=runner active (RUNNING demo:rz_final ...)` (also `raw selecthero`, `sbx_souls 1`) |
| H | Broken scenarios blocked after 3 attempts with reasons | PASS | demo:broken x3 `1x unknown op`; demo:wall x3 `wall-time limit 8s exceeded refund=False`; progress.txt: `BLOCKED demo:broken after 3 attempts: 1x unknown op` |
| I | Foreground-only step never run unattended | PASS | `QR TASK-NEEDS-FOREGROUND demo:fg reason=qdemo_fg.txt line 3: step 'click' needs OS input / foreground`; no attempt consumed |
| J | No client -> pause, not fail | PASS | `QR TASK-PAUSED demo:rz_acc reason=no client connected` (attempt not consumed), resumed 13:15 |
| K | Completed results byte-identical vs backup | PASS | sha256 of every completed result json recorded in queue_demo_final_sha256.txt; `X.json` equals `X.aN.json` for each done task (identical hashes, e.g. demo_smoke 8f71ce7a..., demo_rz_final 23d71d28...) |
| L | Stale-lock takeover without OS action | NOT TESTED (only forced takeover covered); lock logic reviewed in code (15 s heartbeat staleness) | - |

## Log excerpts

```
12:42:00.346 QR TASK-START demo:smoke#1 scenario=smoke
12:42:16.363 QR TASK-RESULT demo:smoke#1 VALID=yes
12:42:17.318 QR TASK-START demo:rz_final#1 scenario=rz_final
12:42:38.337 QR LOAD isReload=True active=True tasks=7 orphanedRunningReset=1 foreignController=none     <- plugin reload mid-run (sbx_build)
12:42:43.453 QR TASK-START demo:rz_final#2 scenario=rz_final                                           <- resumed, attempt refunded
12:42:52.387 QR REFUSED queue-file line 'sbx_scenario smoke' origin=file:qr_ext1.txt reason=runner active (RUNNING demo:rz_final attempt 2/3 ...); prefix the line with 'force' or run 'sbx_q pause' first
12:43:09.478 QR TASK-RESULT demo:rz_final#2 VALID=yes
12:43:18.517 QR TASK-ABORT demo:rz_inc#1 another controller took over refund=True
12:46:51.231 QR TASK-PAUSED demo:rz_acc reason=no client connected
13:15:44.794 QR TASK-END demo:rz_acc#2 why=end step
13:15:59.812 QR TASK-RESULT demo:broken#1 VALID=no 1x unknown op   (also #2 13:16:56, #3 13:18:08)
13:16:09.803 QR TASK-ABORT demo:wall#1 wall-time limit 8s exceeded refund=False   (also #2 13:17:06, #3 13:18:18)
13:21:59.639 QR FORCED takeover of controller lock (owner=claude-orchestrator-LLM-session-2 pid=99999 hb=2099-01-01 ...)
13:25:34.366 QR TASK-NEEDS-FOREGROUND demo:fg reason=qdemo_fg.txt line 3: step 'click' needs OS input / foreground
13:03:02.382 QR LOAD ... tasks=9 reconciled total=9=sum-of-states
```

## Honest notes
- demo:rz_final attempt 1 and arena_smoke2 attempt 1 were killed by plugin reload (sbx_build) - refunded as designed, not failures.
- demo:rz_acc paused 28 min waiting for the client (client was not connected), then completed on resume.
- Stale-lock takeover (row L) not exercised.
- After these demos, the runner was extended (display, metadata lint, prio). Non-demo tasks without a `meta` header are now REJECTED as anonymous (5 Stage-0/pilot tasks were rejected on first load and re-queued after meta headers were added; 13:54 log).

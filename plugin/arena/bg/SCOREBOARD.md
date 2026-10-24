# SANDBOX SCOREBOARD (commissioning 2026-10-24; Kieran approved COMMISSIONING_PLAN.md)
Rule: counts only if valid (clean start, real triggers/hits, valid session, completed). Failed/interrupted/invalid never count. Max 3 attempts per task.
## Phase status
- Phase 1: PASS (hidden launch: no windows/focus change from our PIDs; server stable; session valid; connect-assist team 2 + Haze only; pause control verified). Headless: not testable without a plugin change.
- Phase 2: in progress, PAUSED at 20:04 after the first batch (see blockers).
- Phase 3: not started.
## Valid experiments since commissioning: 2
1. p2:act_ar2 (20:00) VALID: Active Reload. Haze base reload 2.406 s; second press at 1.10 s after the first press = 1.203 s reload (50 percent) and an Active Reload buff for 7.0 s; presses at 0.9/1.0/1.3/1.4/1.5 s gave no speed-up (2.38-2.45 s). Narrow timing window (between 1.0 and 1.3 s, about 46 percent of the reload). Feeds any Haze build using upgrade_active_reload.
2. p2:cap_test1 (20:01) VALID but harness capability check only (ally spawn / scripted casts / real vs artificial damage); not a build result; its md lacks readbacks, so what it proved is not yet reported.
## Invalid (not counted): disc:T5_2f170e43b3 attempt 1 (cast3 never triggered, 0 of 1), disc:T5_77785e7cae attempt 1 (cast1 never triggered); T5_2f attempt 2 aborted by pause (refunded).
## Blocker: ability casts via the cast op have NEVER registered (13 historical ACT summaries: every castN = count 0). Gun/reload/melee forcing works. Suspected cause (unproven): forced ability buttons only set the held bit (Buttonstate1) with no press edge. Fix needs a plugin change (new build) = approval. 4 of the 6 remaining real tasks (T5 x2, T2 x2, T4) are cast tasks and would burn their 3 attempts invalid.
## Host impact (telemetry, task window 19:45-20:03 local): total CPU mean 29 percent (max 46), deadworks 0.33 percent of machine (max 2.8), available RAM min 4.5 GB, disk max 11 percent, run queue max 1, foreground = ChatGPT throughout. Server long frames in the task window: 14 (max 701 ms once at ~19:59:54, cause unknown), versus 95 in the 2000 s before when he was connecting. No stutter reported yet.

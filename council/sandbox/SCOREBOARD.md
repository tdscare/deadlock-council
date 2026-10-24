# SANDBOX SCOREBOARD (commissioning 2026-10-24; updated 22:00 local)
Rule: counts only if valid (clean start, real triggers/hits, valid session, completed, game versions match, no overlapping server spike on timing-sensitive tasks). Invalid/aborted never count. Max 3 attempts per task.

## Phase status
Phase 1 PASS. Phase 2 in progress (queue running unattended, one task at a time). Phase 3 not started.
Deployed build: 5DA596D0 (cast-fix, hot-reloaded twice with the queue paused). Known-good 4B24B567 kept at SandboxTester\known_good_4B24B567.

## A. Original preserved results: 26 (untouched, produced before commissioning)

## B. New VALID gameplay measurements since commissioning: 2
1. Haze Active Reload (p2:act_ar2, 20:00-20:01, server frames clean). PRELIMINARY, n=1 per delay:
   second press after the first press -> result
   - 0.8 s none (earlier run, n=1) | 0.9 none (n=1) | 1.0 none (n=1) | 1.10 REGISTERED: reload 1.203 s of base 2.406 s plus a 7.0 s buff (n=1) | 1.2 effect (earlier run, n=1) | 1.3 none (n=1) | 1.4 none (n=1) | 1.5 none (n=1) | 1.6 none (earlier run, n=1)
   - Only supported statement: effect seen at 1.10 and 1.2, not at 1.0 or 1.3, so the window lies somewhere inside (1.0, 1.3). Its width/edges are NOT established; needs repeated trials near 1.0-1.3.
2. Rend vs Crushing Fists (v14:T5_77785e7cae, 21:48-21:55, build 5DA596D0, client 6819 / server 6819): 12 REGISTERED casts, 54 hits, A/B/A/B at 100/150/250 units, identical every block:
   - Rend "Ability" damage 133.9 both ways (unchanged).
   - Rend "Melee"-type damage 136.9 -> 204.1 with the item (x1.491). The item also adds its own 51.0 Melee line per cast.
   - Per cast total 270.8 -> 389.0 (+43.6 percent). Hunger melee part 20.5 -> 30.6.
   - So the item bonus applies to the melee-typed part of ability damage, not the ability-typed part.
   - Replicated by the second complete run (disc:T5_77785e7cae#2, 22:02-22:09): same 12 casts, 54 hits, identical values. Tier: CONTROLLED SANDBOX RESULT, same server session. Does NOT show build value or purchase timing.

## C. Harness capability check: p2:cap_test1 -> file produced, capabilities UNVERIFIED (no readbacks). NOT a finding, not counted as a measurement.

## D. Invalid attempts (not counted)
- disc:T5_77785e7cae attempt (19:51): cast1 never triggered (false invalidation; Rend did fire, event names were empty - fixed in 5DA596D0).
- disc:T5_2f170e43b3 attempt 1 (19:44): cast3 never triggered.
- Crushing Fists is counted as ONE invalid attempt (19:51) plus one aborted run (E); the 2 attempts Kieran saw = these.
## E. Aborted / refunded (not attempts): T5_2f #2 at 20:00 (paused), v14:T5_77785e7cae at 21:46 (paused for the build swap).

## BLOCKED by tester limitation (not evidence about the items): all Viscous tasks. disc:T5_2f170e43b3 (Puddle Punch) blocked after 3 attempts; disc:T2_97edcd8e6a (Viscous slot 2) blocked before use. Cause below.

## Cast fix: VERIFIED for Drifter slot 1 (Rend): ACT SUMMARY count=12, cooldown start on drifter_blood_blast, damage read back. NOT working for Viscous slot 3 (viscous_telepunch): forced cast gives no event and no cooldown start in 4 consecutive blocks (CASTDIAG cd=False before and after). Press-edge hypothesis not supported (Drifter works with the same op). Per-ability prechecks (22:09-22:22, each tested with cast, hold and ExecuteAbilityBySlot): Haze slot 2 FIRES, Nurse slot 4 FIRES; Viscous slot 2 and slot 3 never fire by any path. So it is Viscous-specific, not the press edge and not the input path. Needs a plugin-side readout of ability cast conditions (new build, approval) to go further.

## Server timing (offline check, frame_validity.py): server stdout is 19:00 onward only. Spikes >=250 ms: 19:06:03 (495), 19:38:50 (617), 19:59:46 (701), 21:45:36 (595). None fall inside a completed or aborted measurement window except 19:59:46, which sat in the hero-swap phase of the aborted T5_2f #2 (not counted). act_ar2 (20:00:19-20:01:28) and cap_test1 had no frame >76 ms: clean.

## Host impact (telemetry, 19:45-20:03): total CPU mean 29 percent (max 46), deadworks 0.33 percent of machine, RAM available min 4.5 GB. No stutter reported.

## Open defect: "cdreset each" soft reset leaves all abilities on cooldown, so every soft reset escalates to a hard reset (hero swap), which is slow and is where the load hitches occur.

## Soft-reset defect, now measured: after 'cdreset each' viscous_telepunch reads onCd=True start=11429.8 end=12129.8 (700 s). ResetCooldown() STARTS a maximal cooldown instead of clearing it. Candidate fix for the next maintenance deploy: set CooldownStart=0 and CooldownEnd=0 (fresh pawns read 0/0, onCd=False). Not deployed.

## 22:50 v15 deploy (build 33D1B53F, source 99191142; hot reload, queue paused, known-good 5DA596D0 kept on the PC and hash-verified)
- Session valid, server stable, BUILDVER 6819/6819 match, Haze smoke bomb casts still register.
- Cooldown fix PASS: after 'cdreset each' stillOnCooldown=0, STATE onCooldown=[] (was all abilities, 700 s). Soft reset now clears items and item buffs; it still (correctly) escalates when a real temporary buff outlasts the 6 s wait (Smoke Bomb invisibility), then verifies the hard reset against the baseline.
- Viscous cast: still NOT registered. Readout shows all four abilities unlocked, bits=15, no cooldown, not channeling/toggled, pawn hp full, no unusual modifiers; ExecuteAbility(flags 0 and 1) returns 0 with no cooldown start. The state readout gives no cause. (RemainingCharges/MaxCharges read garbage; unusable.)
- Item active press (Echo Shard, un-imbued, probe): also no effect via ExecuteAbility. Imbue itself reads back OK (isImbued, imbuedInto smoke_bomb). Echo Shard / Nurse item tasks failed 'item never triggered' x3: blocked on the item-activation path, not on casts.
- Queue is empty of runnable work. Research direction: user examples are tier user-reported (validated/user_reported.json); pipeline re-ranked by tools/rerank_v2.py (ranked_v2.txt): 110 hypotheses collapse to 5 relation classes (Echo Shard x98, heavy-melee x8, ITEMS_DISABLED x2, T1 x1, T3 x1). Hypothesis supply, not sandbox time, is now the limit.

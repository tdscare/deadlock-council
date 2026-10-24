# Background-focus reliability test: DESIGN (not run; needs Kieran to switch windows by hand)

Question: does a Deadlock client that is NOT the focused window (another app in front) change what our scenarios measure? Tests only Deadlock vs a neutral app (Notepad/Explorer/browser). Overwatch is never a test target and nothing here touches it. No agent focuses, clicks or types: Kieran changes focus himself.

## What in our pipeline depends on the client
- Scenario buttons/aim are injected server-side into the client's usercmds (`UcBody`, PERF counter `usercmd n`; ~5 cmds per server tick in the 12:44 runs: n=14434 over tick n=2886). Fewer/later client cmds = fewer shots.
- Camera is steered by `SetCameraAngles` (applied by the client at its own frame rate).
- Damage per hit and hit/miss come from the server (`OnTakeDamage`, accseed-driven miss windows), so they should not change unless the cmd stream does.

## Source2 unfocus behaviour (found in `game\bin\win64\engine2.dll`, `inputsystem.dll`, `tier0.dll` strings; defaults NOT readable from files)
- `engine_no_focus_sleep` (+ `engine_no_focus_sleep_vconsole_suppress`: "when VConsole is in the foreground don't trigger engine_no_focus_sleep"); status line format `App active: %s, %dms inactive sleep` = a per-frame sleep when the window is inactive. This is the main suspect (fewer client frames -> fewer usercmds).
- `fps_max`, `fps_max_ui`, `fps_max_tools` ("tools mode and a window other than the game window has focus" = editor only, not the game). There is NO `fps_max_unfocused` in this build.
- `SetDisableFocusBasedPriorityBoost` / "Disable focus based priority boost" (Windows scheduler boost for the foreground process).
- `Plat_SetFullscreenMinimizeOnFocusLoss` + SDL `SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS`, SDL focus-lost/minimized events (inputsystem): in exclusive fullscreen focus loss can minimize the window and stop rendering. Use windowed/borderless for this test.
- Server side (`deadworks.exe`, our tick) has the same engine code but nobody is "unfocused" there; `sv_hibernate_when_empty 0` is already set.
- Not in game files, to be checked on the PC: Windows Graphics Settings power throttling (EcoQoS) for background apps.

## Kieran sets up (once)
1. Deadlock in borderless/windowed. In its console read (just type the name, it prints the value): `engine_no_focus_sleep`, `fps_max`, `fps_max_ui`. Send the values.
2. Neutral second app (not Overwatch) to put in front; keep it visible (arm B) and also minimized (arm C, optional).
3. No other game running during the test; same Windows power plan for all arms.

## Arms and protocol
- A = Deadlock focused (control). B = Deadlock behind a visible other app. C (optional) = Deadlock minimized. D (optional) = B with `engine_no_focus_sleep 0` typed by Kieran (isolates the cvar).
- Identical seeded scenario `bg_focus` (to write from existing ops): `setup Frank Haze`, `accseed 1234`, `accuracy 0.7 0.5`, then 5 blocks of `fetch 350; cast reload 2.5; fire 20; acclog; mark blkN`. Same hero/items/seed every trial.
- 6 trials per arm, interleaved A,B,A,B... (a queue task per trial; Kieran flips focus between trials while the queue is PAUSEd, then deletes PAUSE and leaves the PC alone).
- Record arm in task id (`bg:A1`, `bg:B1`, ...); the runner cannot detect focus, the id is the record.

## Metrics (per 20 s block) and where they come from
| metric | source | note |
|---|---|---|
| usercmds per tick, per second | `PERF tick n= ... usercmd n=` (plugin.log, per run) | baseline ~5.0/tick |
| usercmd gaps, late (>2 ticks = 31 ms) and dropped (tick with 0 cmds) | NEEDS new instrumentation in `UcBody` (gap histogram); not present today | code change, do before first run |
| server tick intervals | `PERF tick avg/max`, `PERF slow hook`, server_stdout `Avg Frame` lines | server-side control (should be flat) |
| shots fired / 20 s | `acclog` EVENTS `GunFired:me=` | primary |
| damage per hit | damage csv, Bullet rows (body 34.8 baseline) | must be equal |
| hits / shots | `dmgHitsOnEnemy`, `BulletHit` vs `GunFired` | accseed makes it comparable |
| dps and CV | csv damage sum / 20 s per block; CV across 5 blocks and 6 trials | grade B needs CV < 15% (SCHEMA) |

## Decision rule (fixed before running)
B (and C/D) are "equivalent" to A if: shots/20 s within 2% of A's mean and outside A's range only if A's own CV allows; damage per hit identical; usercmds/tick within 5%; dropped ticks <0.5%; dps CV not above A's CV + 5 points. Otherwise the arm is flagged "background-sensitive" and all queue runs must be done focused (or with the cvar fix if arm D restores equivalence).

## Open
- cvar default values unknown until Kieran prints them (could not read `machine_convars.vcfg`: hardlinked, tool refuses).
- `usercmd n` counter semantics (cmds vs batches) should be confirmed in code when adding the gap histogram.

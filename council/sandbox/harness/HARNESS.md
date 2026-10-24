# Sandbox harness (cfg-driven setup + log-parsed results)
Status 2026-10-22: written from public docs only, nothing run in game. Command registry with sources: `commands.json` (CONFIRMED = named in a public source; UNVERIFIED = no source or sources disagree). Generated cfg lines are tagged the same way.

## Architecture without -insecure (research 2026-10-22; nothing run in game)
Recommendation: ordinary secure client, built-in Hero Sandbox (or Custom Match with "Enable Cheats", solo + bots), cfg via `exec`/autoexec, results from console log/condump. No gameplay-script mod. Remove `-insecure`; matchmaking untouched.
CONFIRMED (public source):
- Console + cheat-flagged cmds work in Hideout, Sandbox, Explore NYC and cheat-enabled custom games; "will not work in standard multiplayer matches"; `citadel_hero_testing_enabled` shows the Testing Tools menu without cheats, its functions need cheats (deadlock.wiki/Console_commands). No source mentions `-insecure` for Sandbox/cheats (deadlock.wiki, gameboost.com/blog/deadlock-console-commands, deadlockhandbook.com/modes/sandbox all silent).
- Custom Match has an "Enable Cheats" toggle and easy/medium/hard bots (dexerto.com/gaming/how-to-make-custom-lobbies-in-deadlock-2899778; deadlockhandbook.com/modes/bot-and-custom-matches, updated 2026-10-08). `private_lobby_create` opens it (siege.gg, 2024).
- Limit: in Custom Match with cheats, replicated cvars (e.g. `sv_airaccelerate`) are refused "only server operator can change"; rcon to 127.0.0.1 failed; practice-bot cvars on dl_midtown gave broken physics/lag (forums.playdeadlock.com thread 109576, 2026-02-16 and replies to 2026-08-25). So prefer Sandbox for tests; Custom Match is plan B.
- VDC flags: cheat = `citadel_enable_fast_cooldowns`, `citadel_give_gold`, `citadel_allow_purchasing_anywhere`, `bot_puppet/mimic*`, `bot_kick_all`, `citadel_bot_playrecording`, `citadel_spawn_nearby_neutrals`. NOT cheat-flagged: `citadel_create_unit`, `citadel_spawn_practice_bots*`, `citadel_hero_testing_*`, `condump` (release). (developer.valvesoftware.com List_of_Deadlock_console_commands_and_variables)
- `-insecure` general Source meaning: client skips VAC and cannot join VAC-secured servers (modlock README: "Clients run with -insecure and cannot join VAC-secured servers"; Steam guide id=1112593117 is L4D2). No Deadlock source says what it does to the matchmaking queue; it is also unneeded for the loading routes below.
- cfg: `game\citadel\cfg\autoexec.cfg`, launch `-console -exec autoexec`; `exec <file>` works in cfg dir (deadlock.wiki). Bot-match cfgs exist (`exec citadel_botmatch_practice_6v6`).
- Mods: VPK in `game\citadel\addons` plus a `gameinfo.gi` SearchPaths edit (esports.net/wiki/guides/deadlock-mod-install; github 7liv/compylock; docs.deadlockmods.app FAQ). Loads on own client only. FAQ: Valve currently allows client mods that give no unfair advantage; "check Valve's current mod policy". Steam verify/updates overwrite gameinfo.gi. Custom maps: files in `game\citadel\maps`, `map <name>` (oneesports.gg guide, which also says add `-dev`; UNVERIFIED necessity). Asset mods only (textures, sounds, UI textures, models; deadlockmodding.pages.dev guides). No Valve Workshop Tools / Hammer / SDK for Deadlock found (VDC has a stub page only; geosirius.ifz.ru article is speculative, low reliability).
- Server-side scripting exists but needs a SEPARATE server: modlock (github.com/paralin/modlock; WASM mods in TS/Luau/Python; `onDamage`/`onDamaged` events, `spawnNpc`; `build/server.log`; local server then joins with the game; mods have no file access) and Deadworks (deadworks.net, C# plugins, dedicated server from a separate install via SteamCMD app 1422450, ~35 GB, launch `deadworks.exe -dedicated -console -dev -insecure -allow_no_lobby_connect`, clients `connect ip:27067`). The `-insecure` there is on the SERVER; docs do not state whether a normal secure client may join. Not our route unless cfg+log fails.
UNVERIFIED (probe must settle):
- Whether Sandbox cheats/console work with no `-insecure` (Kieran uses it; reason unknown, nothing public says it is required).
- `con_logfile`, `-condebug` output location, timestamps. Panorama `$.Msg` printing to console (general Source 2 knowledge, no Deadlock source). Panorama/VScript cannot write files (mods have no file access per modlock; VDC cl_script_* cvars are generic Source 2, cheat-flagged, no Deadlock docs).
- Whether VPK addons/edited gameinfo.gi block or flag matchmaking or sandbox (no source). Avoid addons for the harness: not needed.
- Whether any cfg can run on sandbox load: autoexec runs at game start, not at map load. Known options: `exec` by hand (one command), alias/bind chains (F-keys). Auto-exec on map load = no source; `+exec`/`map` launch args UNVERIFIED.
First in-game probe (no -insecure, normal launch `-console -condebug`): enter Sandbox; F7; `sv_cheats` (read value; does `sv_cheats true` error?); `exec probe` (echo/alias markers, `giveitem`, `citadel_create_unit hero_haze 3`, `citadel_enable_fast_cooldowns`, `condump`); `con_logfile sbx_probe.log` then search game folder for it and `console.log`; shoot bot then check condump for damage lines; back to Hideout and queue to confirm matchmaking still works. If any cheat command refuses without -insecure, record the exact error text; only then consider `-insecure` and restarting between test sessions.

## Files on Kieran's PC (Windows; defaults, verify)
- Game: `C:\Program Files (x86)\Steam\steamapps\common\Deadlock\` (or the Steam library you installed to; Steam > Deadlock > Manage > Browse local files)
- Cfg dir: `<Deadlock>\game\citadel\cfg\`  (copy generated `sbx_*.cfg` + `probe.cfg` here, flat; `exec` is relative to this dir)
- Log candidates (PROBE 2): `<Deadlock>\game\citadel\sbx_console.log` (con_logfile), `<Deadlock>\game\citadel\console.log` (-condebug), `condumpNN.*` from `condump`. Search the Deadlock folder for the newest file if none is there.
- Launch options (NO `-insecure`, see next section): `-console -condebug` (add `-exec autoexec` only if you want setup on start). `-console`/`-exec autoexec` documented (deadlock.wiki); `-condebug` UNVERIFIED for Deadlock (only VDC mention: it no longer makes Cvarlist print the list).
- Console: F7 (enable "Dev command console" in options).

## Generate and parse (on any machine with node)
```
node harness/gen_cfg.js scenarios/<id>.json --out out/<id> [--enemy-hero Haze] [--enemy-team 3] [--spawn "x y z"]
node harness/parse_log.js <console.log|condumpNN> --scenario scenarios/<id>.json --patch <patch> --out results [--manual manual.json]
node harness/test.js     # unit tests (synthetic input, temp dir)
```
Parser output = results/<date>_<scenario>_<arm>_t<n>.json per SCHEMA.md. Metrics found in the log are grade A. Metric not printed = `value:null, grade:null`, listed under `notes`/`missing` (never a guess); fill by hand via `--manual` (`{"<scenario> <arm> <n>":{"metric":{"value":..,"grade":"B","evidence":"shot.png"}}}`). Time metrics need timestamps in the log; without them they are null. Line formats in `patterns.json` are GUESSES until PROBE 7 gives a real sample.

## Order of commands the tester runs
1. Launch with options above, open Sandbox (hero testing), pick the scenario hero. Open console (F7).
2. `exec sbx_common` (cheats, fast cooldowns, damage meter, logging attempts, F9 = condump).
3. `exec sbx_<id>`, then `arm_<armA>` (resetme, souls, giveitem lines).
4. Aim at open ground, `t_<armA>_1` (resets, spawns enemies, binds F8, prints `SBXMARK START`).
5. Play the procedure. When done (kill/death/cap) press F8 (prints `SBXMARK END`, condump).
6. Switch arm: `arm_<armB>`, `t_<armB>_1`, ... interleaved A,B,A,B (order printed by gen_cfg and in the master cfg).
7. Copy the log/condump files to the harness machine, run parse_log. Screenshots only for metrics listed missing.

## PROBE (first minutes in game: `exec probe`, read console, then fill YES/NO)
| # | Test | Unlocks if YES | If NO |
|---|---|---|---|
| 1 | `echo`/`alias` print `SBXMARK PROBE 1 ...` | markers | everything breaks; use screenshots |
| 2 | Is `sbx_probe.log` created (con_logfile)? else relaunch `-condebug`, find console.log. Do lines carry timestamps? | continuous log file | rely on `condump` (F9 / F8) which dumps only the visible buffer (~241 lines per VDC): dump often |
| 3 | `dump_hero_names` output | fix ids in hero_names.json | |
| 4 | `giveitem upgrade_improved_spirit`, `giveitem upgrade_magic_reach 2`: item present? imbue on ability 3? What does `resetme` clear? | arm loadouts by cfg | buy in shop; loadout.js lines are then a checklist |
| 5 | `citadel_give_gold 5000` adds souls? `givelevelupgold 5` exists (sources contradict)? Level from souls? | souls/level | set via kingme/infinite_money, note boons by eye |
| 6 | `citadel_create_unit hero_haze 3`: enemy or ally? bot_brain_disable_movement/attacks stand it still? | enemy spawn + stand-still | use Sandbox panel; record a puppet loop for behaviour |
| 7 | After shooting the bot, `condump`: any damage lines (try `debug_takedamage_summaries true`)? Paste sample into `samples/` and edit patterns.json | grade A damage | damage = hud_damagemeter DPS x time or pop-up screenshots (grade B) |
| 8 | Healing / kill / death lines in the dump? | heal, kills, TTK | read from screen, B |
| 9 | `getpos`, move, `setpos <values>` returns you? | fixed start position | stand on a marked spot |
| 10 | `citadel_enable_fast_cooldowns` (1s or 2s) | cooldown reset | accepted per Kieran |
Not covered by any documented command: ability point allocation, bot ability-cast args (`citadel_bot_use_ability*`), recorded loop playback (`citadel_bot_playrecording` arg), host_timescale, `wait`. Ability order and recorded enemy loops stay manual (UI).

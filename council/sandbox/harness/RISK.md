# Ban / anti-cheat risk for sandbox testing (researched 2026-10-23)

Bottom line: no public report found of any ban, warning or VAC flag caused by Sandbox, console/cheat commands or cfg files. Absence of reports is not proof; Valve has published nothing on it. Nothing below was tested in game.

## Confirmed (source, date)
- Console + cheat commands are an intended feature of Hideout, Sandbox, Explore NYC and cheat-enabled custom games; "Commands that require cheats will not work in standard multiplayer matches." deadlock.wiki/Console_commands (undated). The page has no ban/VAC warning.
- Valve's VAC doc describes detection as foreign processes hooked into game binaries; it says VAC does not detect content hacks; it says nothing on sv_cheats, console, cfgs or offline play. developer.valvesoftware.com/wiki/Valve_Anti-Cheat (CS-focused, undated).
- Deadlock has an anti-cheat, added in the Sep 26 2024 update; players vote ban or frog. dexerto.com (updated Sep 27 2024), labs.invenglobal.com (Oct 7 2024). Both say unclear whether it is VAC. Pre-release 2024; nothing newer found from Valve.
- `-insecure`: modlock README: "Clients run with -insecure and cannot join VAC-secured servers" (github.com/paralin/modlock, undated). Forum users (Sep/Oct 2024, forums.playdeadlock.com thread 25611) say it disables VAC and you "wouldn't be able to matchmake"; user claims only.
- Mods (VPK + gameinfo.gi): Mod Manager FAQ: "Deadlock currently allows client-side modifications that don't affect gameplay balance or provide unfair advantages"; advises checking Valve's current policy (docs.deadlockmods.app/using-mod-manager/faq, undated). deadlockskins.gg (undated, mod-hosting site, biased): "no confirmed bans for client-side cosmetic mods", Valve "has not published anything specific".
- Demo parsers exist and work offline on .dem files: boon (boon.readthedocs.io; `damage` dataset = "all recorded damage events" incl. hero/objective/trooper/neutral, filter `attacker_hero_id`/`victim_hero_id`; GOTV demos may lack some pawns), deadem (npm 2.0.0; reads entities such as `m_iHeroDamage`; says not all game state is preserved), source2-demo (github.com/Rupas1k/source2-demo). Parsing a file never touches the game process.

## Contradictory / unconfirmed (flagged)
- CONTRADICTION on bans for console/skins: forums.playdeadlock.com/threads/get-perma-banned-for-no-reason.49413 (Nov 2024 to May 2025): users speculate a perma-ban followed a console command (survey popup/healthbar) or custom skins ("many streamers using custom skins had been banned" - unsourced). Another user in the same thread was banned with no console changes and no skins. No Valve reply, cause never confirmed. Steam forum (Sep 2025): one user says skin bans 48h-permanent, another says impossible; both unsourced. Treat as unproven but not zero.
- Cheat-seller sites (gcscheats.com, deadlockcheats.net) claim Deadlock uses VAC with account bans; commercial bias, not Valve.
- Not found anywhere: Valve statement on Sandbox/console/cfg/mod bans; whether Deadlock's secure-client check punishes `-insecure` or `-condebug`; whether Sandbox is a separate non-secure server (unconfirmed, though cheats working there suggests it is a local listen server).
- Not found: Deadlock-specific confirmation of `record`/demo commands in sandbox (deadlock.wiki/Commands lists none); `condump`/console log exist per our commands.json, `-condebug` unverified for Deadlock.
- Boon FAQ does not say whether a damage row is a single hit.

## Risk ranking (lowest first)
1. (d) Offline demo parsing: none. Reads files only; also reads match demos you already have. Caveat: you need a .dem, and only the recording step (below) carries any risk; per-hit coverage unconfirmed.
2. (c) Local dedicated/listen server for scripted tests (modlock-host style, `-insecure` client): very low for the account IF the client never touches matchmaking/public servers; `-insecure` is the standard Source way to stay out of VAC. Highest effort (modlock is third party, separate server, entity coverage partial). Risk: forgetting to remove `-insecure` is not a ban issue per sources, but it blocks matchmaking.
3. (b) autoexec/exec cfgs: very low. Plain Source config; same commands a player types. No report of cfg bans. Only the one speculative thread about a specific console command. Keep cfgs out of live matches (cheat cmds are refused there anyway).
4. (a) In-game console in Sandbox with cheats: low. It is a Valve-built feature, VAC looks at process tampering not cvars, no ban report found. Highest of the four only because of the unexplained 2024 ban threads and no Valve statement.
Not ranked but riskier than all: gameplay-changing VPK/gameinfo.gi mods or anything injected/hooked into the game process (VAC's actual target); a Panorama UI addon to read damage falls here.

## Recommendation
- Use the normal client, no `-insecure`, no mods: Sandbox + `exec` cfgs + console log (ranking a/b). Never run cheat commands, mods or tools in or right before a matchmade game; do tests on a separate session; do not stream with modified files.
- For per-hit data prefer offline demo parsing (boon) over screenshots or UI addons. First verify with a one-off: can a Sandbox/custom-match session produce a .dem, and does boon's `damage` give per-hit rows? Unknown until tried.
- If Kieran wants zero uncertainty on the main account, run tests on a throwaway second account (account-based bans per cheat-seller claim only; unconfirmed) and still keep the main untouched.
- Ask Valve support / Deadlock Discord (official dev replies) if a firm answer is needed; none exists publicly.

# Sandbox capabilities — from public guides + Kieran's in-game knowledge (probe must still confirm)

## Corrections from Kieran (Oct 22)
- Hitting an enemy shows damage number pop-ups: in-game damage feedback exists (readable on screen, grade B with repeats).
- 1–2s cooldowns (No Cooldown toggle / fast cooldowns) are fine; no true reset needed.
- Item give commands exist: `giveitem upgrade_<code>` (imbue items take a 0–3 ability index after the name). Codes for all 194 items: `item_commands.json`; generate a trial loadout with `node council/tools/loadout.js <buildId> [--swap "A=B"]`.
- Bots can already be scripted in game: puppet a bot, record its actions, loop the replay, toggle bots to cast an ability/item every few seconds (e.g. bot flies up, casts, you Counterspell, repeat); recordings copy as share codes (undeadlock.com/game/bots). So enemy behaviour for scenarios can be recorded once and replayed identically.
- Still unknown: per-fight damage/heal totals. Options to test: sum pop-ups by repeated screenshots; DPS meter x time; HP bar sampling; a Panorama UI addon that listens to damage events (unverified, UI mods are known to be possible).
Sources: deadlockhandbook.com/modes/sandbox, lockbuilds.com/deadlock-console-commands, docs.deadlockmods.app/modding. Fetched Oct 22 2026.

Console: enable "Dev command console", F7. Cheat commands need Sandbox/Hideout/custom lobby with `sv_cheats true`. Startup scripts: `game\citadel\cfg\autoexec.cfg` + launch options `-console -exec autoexec`.

| Need | Command / panel |
|---|---|
| Spawn enemy/ally hero | Sandbox panel (hero + team, appears at crosshair); `citadel_create_unit <hero>` (allied dummy); `dump_hero_names` |
| Bots copy/puppet | `bot_mimic_target`, `bot_puppet_target`, `bot_mimic 0; bot_puppet 0`; remove all `bot_kick_all` |
| Practice bots | `citadel_spawn_practice_bots true`, `..._count <n>` |
| Level / souls / points | `givelevelupgold <n>` (35 = max), `kingme` (1.2M souls, all abilities), `citadel_hero_testing_infinite_money true`, `giveallupgrades`, `resetme` |
| Items | buy at Curiosity Shop anywhere; `citadel_allow_purchasing_anywhere true`, `citadel_unlock_flex_slots` (no give-item command listed) |
| Health | `healthpct <0-100>`, `hurtme`, `lethaldamageme`; no-death toggle `citadel_enable_no_hero_death` |
| Cooldowns | panel "No Cooldown" (1s) / `citadel_enable_fast_cooldowns` (2s) — NO true cooldown reset command listed (matters for tests) |
| Ammo | panel "No Reload" |
| Camps | `citadel_spawn_nearby_neutrals` |
| Readouts | `hud_damagemeter true` (your DPS next to crosshair); damage multipliers `citadel_dps_multiplier`, `citadel_weapon_damage_multiplier` |
| Time | `host_timescale 1.0`, `host_timescale_inc/dec` |

Gaps to probe: giving souls precisely, setting a specific item list by command, per-fight damage/heal totals, healing numbers, console log to file, damage taken meter.
Modding docs show asset-level mods (VPK addons, Source 2 tools); no evidence of gameplay scripting.

## Consequence for the Sandbox Tester
1. Most setup (level, souls, spawns, health, camps, timescale) can be driven by console/cfg instead of clicking — more repeatable than computer use.
2. Item loadouts must be bought in the shop (or via the build's own buy flow) — the probe must find a faster route.
3. Measurement is the hard part: `hud_damagemeter` gives DPS only. Healing/taken/survival need screen reading or a log. Look for a console log file (`-condebug`) before building a mod.
4. A real "mod" may be impractical (no gameplay scripting found); the likely best design is cfg scripts + a small screen/log reader. Verify, don't assume.

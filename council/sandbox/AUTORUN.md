# Autonomous sandbox (works as of 2026-10-23)
No human input needed once the server and client are up.
1. Server: write `dl_midtown` to E:\deadworks-server\ctl\restart.req (supervisor rebuilds plugin, restarts server, 12 slots, 2 real practice bots).
2. Client: click game, F7, type `connect localhost:27067`, Return, F7. (Steam "Continue" prompt only if the game is closed.) Auto-setup puts me on Amber at mid lane with 50k souls and a bot Haze (enemy) 350u away.
3. Drive via file queue: drop `E:\deadworks-server\sbx_cmd\<new name>.txt` containing `sbx_scenario <name>`; scenarios live in E:\deadworks-server\scenarios\<name>.txt. Plugin code hot-rebuilds with a queue file containing `sbx_build` (~2 s).
4. Results: sbx_logs\damage_*.csv + samples_<scenario>_*.csv; `python3 autorun/tools/analyze.py damage.csv samples.csv`.
Scenario ops: setup <MyHero> <EnemyHero> | clear | give <class> | souls n | mark <label> | aimoff yaw pitch | fire s | cast <1-4|i1-i4|melee> s | heal | hurtme n | wait s | end. Hero names are the Heroes enum (Victor = Frank).
Gotchas: use `mark none` around resets so setup healing isn't counted; items are removed by AbilityName; device_commit_files writes can be stale, recommit until size matches; aim offset yaw +5.5 / pitch +3 is calibrated for 350u only; bullets must hit the enemy hero for hit-based procs.

## Realism ops (added 2026-10-24; Realism.cs; all verified on the live server unless marked)
Scenario syntax (one op per line, `#` comments). Hero names: see sbx_logs\hero_enum.txt (`setup` now aborts the scenario with "unknown hero name" instead of silently using Haze).

CLEAN STATE
- `hardreset` : THE reset between blocks. Swaps to another hero and back (fresh pawns for BOTH player and enemy bot): no items, no buffs/debuffs (Mercurial Magnum etc.), cooldowns/charges at factory state (start=0,end=0), full HP, back at mid lane, `unlock 7`, `basemods`, `mark none` re-issued. Costs ~10 s. Verified: items=0, CD listing all 0/0, enemy items gone.
- `reset [respawn]` : soft reset without a new pawn: removes all items from player AND enemies, removes non-baseline modifiers (needs `basemods` once after setup), full heal. Does NOT touch cooldowns. Use `hardreset` when cooldowns/charges matter.
- `basemods` : snapshot current modifier names (player and enemy) as "intrinsic"; `mods` logs current modifier names of both; `cds` logs every ability's CooldownStart/End/UpgradeBits.
- DANGER (cause of the broken Pain Battery -2e9 / Jumpstart 1200 s / ult 1200 s cooldowns on 2026-10-24): `ResetAllAbilityCooldowns`, `ResetAbilityCooldown(slot)` and `ability.ResetCooldown()` write garbage into the `ability_frank_shocktarget2` (Pain Battery) fields (end=7e9) and, after `unlock 15`, wrote end=2*now (1193 s cooldowns) on other abilities. The old `reset` called them. They are no longer called by `reset`. `cdreset each` remains (guarded: skips items, shocktarget*, insane values) but prefer `hardreset`. Fresh pawn after a hero swap fixes already-broken cooldowns.
- `unlock <bits>` now defaults to 7 (3 upgrade tiers); do not use 15.

ENEMIES
- `enemies <n> <radius> [waitSeconds]` : keep n bots (main target first at `fetch` distance, others on a ring of that radius), kept alive/re-fetched every 0.5 s. `enemies 1` removes the extras. Bots never shoot (attacks disabled), `fetch` moves the whole group.
- `fetch [dist]` : place main enemy `dist` units ahead (default 350, remembered; use 100-150 for melee). NOTE: aimoff 5.5 3 is calibrated for 350 only.
- `egod [off] [hp]` / `ekeep <floor>` / `ehp <n>` : enemy health keep-alive. Default floor 0.9 (health restored to max whenever it drops below 90%, checked every frame), so bots effectively never die. `ekeep 0.3` for execute-threshold tests. `ehp n` sets a fixed health pool. (The Godmode entity flag is NOT used: it suppresses damage events.)
- `eitem <class>` / `eclear` : give/remove items on all enemies (works: eitem upgrade_pristine_emblem verified). `eresist gun|spirit <pct>` / `eresist off` : scales damage on enemy players inside OnTakeDamage (fallback; logged damage is already reduced). Some class names fail (`upgrade_bullet_armor` returns null for both sides) - check "FAILED" in plugin.log.

ACCURACY / AIM
- `accuracy <p> [headFrac] [headPitch] [missDeg]` : per 170 ms window, hit with probability p else offset aim by ~missDeg (default 10) degrees yaw and +-missDeg/2 pitch (use 3-5 for "small offset" misses); hit windows use head aim (extra pitch headPitch, default -3) with probability headFrac. `acclog` prints ACC windows, enemy hits (OnTakeDamage), GunFired/BulletHit event counts. Counters reset by `accuracy`.
- `cast reload <s>` refills the magazine (empty mag after a block = no shots; reload before each `fire`). Also `cast jump|duck|alt|zip|i5`.
- `hold <slot> <s>` : hold an ability key for s seconds (charge/channel), e.g. `hold 1 2.0`, `hold i1 1`.
- `move <fwd> <left> <s>` : steer for s seconds (fwd/left -1..1) while aiming at the main target; combine with `cast` afterwards (casts and moves are sequential, not simultaneous).

HEALTH / DAMAGE
- `lowhp <pct>` : sets player HP to pct and every frame clamps it back down to pct (so heals are never capped by max HP; below 3% it is lifted back to pct). `lowhp 0` stops it.
- Heal logging: `sbx_logs\heals_<scenario>_<time>.csv` (HealthTaken events on the player: requested, applied, caster designer/ability, and the list of active modifiers at that moment) and at scenario end / `healsum` in plugin.log: `HEALSRC <event>|<caster>|<ability>: n requested applied` plus `healDiffObserved` (sum of positive HP jumps between frames). Use `healreset` between blocks. Isolating a source = run the same block with that item removed and subtract.
- `incoming gun|spirit <dps>` / `incoming off` : every 100 ms the enemy bot deals dps*dt damage to the player (CitadelDamageType Bullet or Ability, attacker = enemy), mitigated by the player's resists; appears in damage csv as victim=player. Disables the "heal to full below 15%" safety.
- `hurtme <n>` as before.

NOT POSSIBLE / NOT DONE
- Reading or setting ability charge counts or cooldown values reliably: the CooldownStart/End/Charges readers return garbage for some abilities (shocktarget2 etc.). Cooldown state is only trustworthy on a fresh pawn.
- Stack presets (Berserker, Celeste, Grey Talon owl, Drifter): no stack API; reach them by playing (hurtme/lowhp for health-based stacks, `fire`/casts for kill stacks). Not implemented.
- Simultaneous move+cast, "use active X first" are just `cast i1 ...` before the rotation.

### Realism ops: verification status (2026-10-24, live server)
- hardreset: WORKS (cds: all start=0 end=0, bits=7; items=0; enemy items gone). reset (soft): items + non-baseline modifiers removed (Mercurial Magnum/ethereal modifiers gone after next tick), HP full. Cooldown APIs are NOT used (see DANGER).
- enemies n r: WORKS for create/remove (fake clients created to n, extras removed on `enemies 1`); ring placement not independently confirmed.
- egod/ekeep/ehp: WORKS (ehp 50000 sticks above max 829). Godmode flag: do not use (suppresses damage events; code clears it).
- eitem: WORKS (Bullet Resilience on bot: 34.8 -> 24.4 per bullet). eresist gun 50: 34.8 -> 17.4. `upgrade_tech_armor` and `upgrade_bullet_armor` return null (check class names).
- lowhp: WORKS (lowhp 40 with Leech+Opening Rounds fired 5 s: healDiffObserved=724 HP, not capped). HealthTaken/UnitHealed events fire but carry no amounts (requested=0 applied=0): healing is measured by `healDiffObserved`; per-source attribution needs item isolation (run again without the item and subtract).
- incoming gun|spirit: WORKS (gun 100 dps: HP 1695 -> 1682 -> 1672 ... per 100 ms tick). Written to damage csv as attacker=player(team 3), ability "incoming", dmg_type Bullet/Ability, damage = actual HP lost (Hurt bypasses the OnTakeDamage csv log).
- accuracy: WORKS mechanically (100%: 23/23 hits; 50%: ~20-25% of shots hit with the old 250 ms window, window now 170 ms and camera refresh 40 ms - re-measure with `acclog`; compare "dmgHitsOnEnemy" to GunFired). Head vs body is NOT yet calibrated: pitch -3..-14 relative to the calibrated aim produced no extra damage type (WeakpointBonus never seen; body bullet = 34.8) - headshots may need aiming higher at other distances or are not flagged as WeakpointBonus. Use `accuracy p 0` (body only) for now.
- An empty magazine produces no shots: put `cast reload 2.5` before each `fire` block.
- hold, move, fetch <dist>, cast i5/reload/jump: implemented and compile; hold/move not yet exercised on a hero that needs them.
- Test scenarios: autorun/scenarios/rz_*.txt (rz_hard, rz_misc, rz_inc, rz_enemies, rz_acc, rz_head, rz_cd, rz_cd2).

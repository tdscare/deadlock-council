# Range / multi-target / moving-target scenario fields (plugin ops + meta). Owner: sandbox operator. SCHEMA.md is not edited.

Status 2026-10-24 17:00 local: ops are written and deployed as PC SOURCE (E:\deadworks-server\SandboxTester\Range.cs); they have NOT run live yet (the game server crashed, see CONTINUE.md). Nothing here is a measured result.

## Plain-text scenario ops (scenarios\*.txt)
| op | meaning | verification (invalid block, not invalid run) |
|---|---|---|
| `rng <dist_u> [tol_u=20]` | enemy 0 straight ahead at <dist> units | horizontal distance within tol and height offset <= 60u, re-placed up to 4x, else `RANGE BLOCK <label> INVALID: ...` |
| `layout <n> <dist_u> <spacing_u> [ring\|line]` | n enemies. enemy 0 (the aimed primary target) at <dist>; the others <spacing> units from enemy 0: ring = circle around enemy 0, line = sideways line (+y, -y, +2y ...) | `layoutcheck` (auto): enemy 0 distance, spacing of every other enemy, count; re-placed up to 6x else block INVALID |
| `strafe <amp_u> <period_s> [all]` / `strafe off` | enemy 0 (or all) moves left-right sinusoid +-amp, teleport-driven at 25 Hz (bots do not walk; this is a position script, not enemy AI) | distance checks are skipped while strafing (logged "instantaneous") |
| `rngreset` | zero per-target tally and shot/hit counters | |
| `rngreport <label> [minhit=NN]` | per-target lines + totals; single target blocks with hit rate < NN% are INVALID | see measured lines below |
| `rngsummary` | counts valid/invalid blocks; run FAILS only if no block was valid | |
| `hzarm` | re-arm the Haze stack read (next damage row records start stacks) | |
Existing ops used with these: `fetch`, `enemies`, `hardreset`, `statecheck`, `give`, `mark`, `fire`, `cast`, `moddump`.
In layouts the camera aims at enemy 0, not at the nearest enemy. Ring geometry: for n=5 the four ring members are at 90/180/270/0 degrees around enemy 0, i.e. two are nearer to the player, two farther, two to the side; their spacing to each other is 1.41 x spacing. Positions are recorded per target (LAYOUT lines).

## Measured lines (appear in the result "measured" block; prefix RANGE / LAYOUT / STRAFE / RESET / STATE)
- `RANGE verify <label> want=<u> horiz=<u> dist3D=<u> dz=<u> tol=<u> => OK|OUT`
- `LAYOUT t<i> idx=<entity> dist3D=<u> horiz=<u> dz=<u> fromEnemy0=<u> hp=<hp>`
- `RANGE <label> target<i>(primary|secondary) dist3D=<u> damage=<our damage> hits=<n> lethalHits=<n> byAbility=<name=dmg;...>`
- `RANGE <label> totals primaryDamage secondaryDamage primaryHits secondaryHits targetsHit=<k>/<n> lethalHits gunShots bulletHits hitRate secs`
- `RANGE BLOCK <label> VALID | INVALID: <reason>`  (analysis must drop INVALID blocks)
- `RESET method=hard|soft ...`, `STATE <label> items=[..] tiers=.. extraMods=[..] onCooldown=[..] chargesNotFull=[..] lastHazeStacks=.. targetHp=.. => MATCHES expected | differs`
Damage is counted once per victim per damage event (no splash/bounce double count). Misses are not damage. Kills are NOT reported: enemies are kept above a health floor (egod), so `lethalHits` (event damage >= victim health) is the proxy.

## Meta fields (planner/strategy agent writes these; all optional unless noted)
- `meta ranges <u1,u2,...>`  distances in game units for a sweep. Per hero: true point blank (60), melee/contact (~100-150), item threshold just inside and just outside (bracket the edge; the unit scale is NOT verified: GAPS says 15 m is about 500-600 u, Abrams probe says ~39.4 u/m, so bracket 450-700 for a 15 m item), medium (~900), long (~1300+). Planner emits one `rng` block per distance.
- `meta range_expect <item> IN <u>|OUT <u>`  labels what the block should show (item active IN / inactive OUT). An OUT block that shows the effect, or an IN block that does not, is reported as "threshold different from assumed", not as a malfunction.
- `meta layouts <name:n/dist/spacing/shape;...>` e.g. `1_target:1/350/0;3_tight:3/350/150/ring;5_wide:5/350/800/ring`. Use real item/ability radii for spacing (inside radius, at radius, 2x radius).
- `meta moving <name:amp/period;...>` e.g. `strafe150_2s:150/2`; always include a stationary control block before and after (A-B-A).
- `meta per_condition yes`  every measured block label is `<TAG>|<arm>|<condition>|<aim>`; the planner builds the per-phase contribution profile (laning, farming, roaming, duelling, teamfighting, objectives, utility, survivability) from separate condition rows; the plugin never pools conditions.
- `meta reset_policy hard|soft` (default: soft only when `cond_start_stacks` and `stack_track` both say none/n-a; otherwise hard = fresh pawn). Soft reset is verified by `statecheck` and falls back to hard.
Example scenario files: sc_range/rng_cq_haze.txt (Close Quarters sweep 60..1300u, A/B interleaved + A repeats), rng_multi_ricochet_haze.txt (1/3/5 enemies, tight/medium/wide, A-B-A per layout), rng_strafe_haze.txt (stationary, 2 strafes, stationary repeat), state_stacks_haze.txt (Fixation stacks built, control without reset, after reset). Generator: arena/sc_range/gen.py.

## Limits (do not fabricate around these)
- Enemy movement = scripted teleports of fake-client pawns; real hit registration against teleporting pawns is untested. The strafe scenario exists to find out; a hit rate that is implausibly low or 0 means the method is unsupported, not that the gun misses.
- Minion waves and neutral camps: the plugin switches lane troopers and neutrals OFF (ApplyRules). There is no op to spawn waves/camps, so wave-clear speed / souls-per-time cannot be measured now; generic_camp_clear.json is a design only. Needs an API probe (spawn npc / enable trooper spawners) before any farming number is claimed.
- Unit scale (units per metre) is unverified; every sweep reports units, metres are derived and labelled "assumed".
- Kills cannot be counted (health floor); useful-damage / TTK must be modelled from measured damage per target, labelled MODELLED.
- Raw-distance blocks vs "practical" range (uptime, reaching range, disengage) are NOT measurable here; they stay modelled.
- point_worldtext (CPointWorldText.Create) CRASHES the game server (access violation 0xC0000005, 2026-10-24 16:53Z). Never use it.

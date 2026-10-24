# Deadlock Sandbox Tester: full test specification (for review)

Purpose: this documents what an automated tester checks on 81 Deadlock item builds (44 heroes, listed in data.js), and how. Please review it as an adversarial reviewer: find (1) mechanics or conditions that are not tested but should be, (2) places where the method would produce misleading numbers, (3) contradictions or errors in the rules, (4) anything the tester cannot do that makes a verdict unsafe.

Status at time of writing (Oct 24 2026, 04:10): the harness exists and runs scenarios on a private Deadworks server joined from a stock client, but NO hero's results are valid yet. Earlier runs (Victor swaps) were inconclusive. The client keeps being dropped by the server (NETWORK_DISCONNECT_OVERFLOW, server spending hundreds of ms processing input) and a fix is in progress. Headshots are not yet calibrated. Treat everything below as the intended standard plus known gaps, not as verified capability.

Structure: 1. Standard (rules). 2. Harness and method (ops, procedure). 3. Known gaps found by a red-team pass (GAPS). 4. Per-hero play models (how each hero is actually played and what a test must model).

---

# 1. STANDARD (TEST_MATRIX.md)

# Sandbox test standard (Kieran, Oct 23-24). Agents work all of this out themselves; Kieran should never have to say "go test X".
Agents continuously audit and test EVERY build (all heroes), pick uncertain items and substitutes on their own, and report what is best.

## What to test, decided by the agent (not asked)
1. Every uncertain item or slot: list all similar substitutes (same job, same tier) and test them (Leech vs Infuser vs Vampiric Burst vs Bullet Lifesteal; Recharging Rush vs Extra Charge vs neither on Grey Talon arrows; etc.). Also test "none".
2. Hero economy: how does this hero make souls? (Billy cannot farm well -> Cultist Sacrifice, ~8:00; check every hero.) Time purchases to real clock (~7k souls at 8:00).
3. Early game feel at low price points: ~8k, 10-12k (laning), then 20k, 30k, full 12. Check: cooldowns back fast enough, enough health, enough damage, enough ammo (Haze Assassin: Tesla Bullets for farm but no mag -> constantly reloading; fix with spirit or ammo item), health spike present, damage taken when shot. Early-support heroes (Dynamo, Solomon) must still do damage early (Dynamo stomps); don't rush Rescue Beam in lane.
4. Support/utility: score outcomes not raw numbers (does the ally survive the same burst: Healing Nova vs Rescue Beam; ult range/coverage).

## Realism rules
- Accuracy: players hit ~40-50% of shots. Run 100%, 50% and 40% hit rates, and a body/head mix (not only headshots). Report whether the winner changes.
- Enemies: not one dummy. Surround with 4-5 bots at close range for aura/AoE items (Infuser, Healing Aura, Nova...), shoot one. Also single-target. Report both; a 5-bot aura test alone is not realistic.
- Incoming damage: spirit AND gun damage on the player, at realistic rates; test low HP states (Pain Battery, Berserker self-damage, lifesteal/heal only matter when below max HP: start low and keep damaged).
- Stacking mechanics: test at 0, 1 and max stacks (Berserker). Report each.
- CC: hard CC and soft CC against the build. What answers do we have (Unstoppable, Reactive Barrier, Dispel, Rapid Recharge cleanse, Warp Stone)? Seven needs Unstoppable (knockdown/outrange/stuns); Haze may not care about disarm (Rapid Recharge on 2); Wraith values Dispel (slowing hex stops TP). Decide per hero, test with CC applied.
- Range-limited items (Infuser etc.): how does the hero get in range and stay there (speed, Warp Stone, Phantom Strike, Mystic Expansion)? Test with enemies that run away.
- Enemy never dies: infinite/regenerating health or resist items; re-fetch before every burst. Enemies also buy resists: run vs 0 and vs realistic bullet/spirit resist; resist-shred items (Bullet Resist Shredder, Escalating Exposure, Mystic Vulnerability, Tankbuster) judged only in resist runs.

## Clean state between blocks
Full reset every block: remove ALL items, respawn/refresh player (new pawn if needed), reset cooldowns, clear buffs (Mercurial Magnum and other long actives persist otherwise), wait out cooldowns, heal. Randomize/counterbalance block order and repeat >=3 times (first block runs low: warm-up effect observed: first variant 773/797 dps in both orders).

## Optimal rotations per hero (agent derives from the kit, never a flat key-mash)
Ability order and timing matter: e.g. Haze needs knife before ult for Surge of Power; Danny flies up, 2, then ult when enemy < half HP (bonus damage); Seven Lightning Ball charges; Grey Talon arrow charges; Victor Berserker stacks. Keep imbue/proc conditions satisfied in the script. Verify each rotation against the kit data before using.

## Coverage
Every hero/build, including Deadman Danny and all alt builds, then re-run on each patch (new items/heroes) automatically.

## Findings so far
- Victor gun, Leech/Infuser/Vampiric Burst swap, full build, both orders (Oct 24): damage VB > Infuser ~ none > Leech; healing no separable difference (regen/other heals dominate); first-block warm-up bias. Inconclusive on healing: needs low-HP start, bullet-only, accuracy runs.

## Healing attribution (Kieran, Oct 24): the "nothing in the slot" block still healed ~107 hps (vs 88-114 with Leech/Infuser/VB), so other sources dominate
Victor's own healing: Pain Battery (heals 15% of MISSING health, scales with spirit), Jumpstart (15% of max HP), Spiritual Overflow (built-in spirit lifesteal), Healing Tempo (more healing), Frenzy (bullet lifesteal), plus regen. Any build has kit lifesteal + other items; list every heal source of the hero/build from game data first.
- Measure a baseline block with the slot empty AND with each other heal source isolated, then report the marginal healing of the slot item (item minus baseline), at several HP levels (start low and stay low so healing is not capped by max HP).
- Log healing by source where possible (or isolate via item removal); never read a raw hps total as the item's effect.
- Pain Battery-type effects only matter when low: test at low HP; Berserker-type stacks at 0/1/max.

## Hero-aware testing (Kieran, Oct 24 night) - understand how each hero's abilities interact with the thing being tested
- Read the kit before designing the test. Examples: Abrams gets regen while actively taking damage (Healing Booster) and Witchmail gives cooldown: lifesteal items tested only by shooting at low HP will wrongly look worse. Rend does 134+137 from range but +55% heavy melee damage and silence up close: measure at the range the hero actually uses it. Shiv's knives multiply damage per knife in and by rage: test with and without building rage and decide if building rage is viable. Victor Berserker stacks.
- Support/utility: measure downtime. Rem's build is built on Healing Nova + Echo Shard + her 2: what can she do (damage? heal? anything for the team) while all are on cooldown? Fewer idle seconds = better. Report idle time per hero.
- Engage/catch/escape: how does the hero catch targets, slow them, debuff late when enemies have lots of resistance; how does it deal with fast/escape heroes (Mina, Vindicta flying)? Danny needs to reach Vindicta in the sky while she shoots him; how? Test with mobile/ranged enemies, not just a standing bot.
- Ults and sustain are tested too, not only gun/ability damage.

## Test hygiene (hard requirement)
- Enemy bots get god mode (never die). Before EVERY block wipe both sides: remove all items from player AND enemies, clear debuffs/buffs, reset cooldowns/charges, reload/respawn, then give the new build.
- Do this for every item, every hero, every build; run overnight autonomously; report in the morning what is optimal vs not, with changes proposed to data.js (never auto-apply removals without verification).

## Price points and buy order (Kieran, Oct 24 01:43)
- Test at 10k, 18k, 24k, 30k souls (and full 12), not at spikes only. At each: damage, fire rate, ammo, health, cooldowns, feel.
- Buy the build LEFT TO RIGHT exactly as in data.js (Early, Mid, Late box order, components then upgrades as a player would). Never cherry-pick "good" items or random pairs; people follow the order, so the tested loadout at N souls = the items bought in order up to N.

## Order and hero-specific play (Kieran, Oct 24 01:49)
- Test heroes alphabetically: Abrams, Apollo, Baba, Bebop, Billy, Calico, Celeste, then on through the roster and Deadman Danny.
- Every plan must model how the hero is actually played, not stand-still-and-press. Per hero, the planner reads the kit and writes the positioning/rotation, including what a real player can't do (e.g. stand in a whole dash trail).
- Miss shots by aiming slightly above or to the side of the target. No big mouse flicks.
- Actives (Alchemical Fire, Paradox Focus Lens etc.): use them first in the rotation, at the right moment (Focus Lens pays 30% of damage dealt on expire). Every item's interaction is checked, not just passives.
- Souls: for each hero decide whether the build needs souls and how it gets them (Trophy, Cultist, farming ability). Weak farmers (Deadman Danny) need an explicit answer, as does an assassin build that doesn't need souls.
- Range/economy questions per hero (e.g. Lash): does the ult reach, does it need earlier points, Greater/Mystic Expansion earlier, Trophy for range.

Per hero notes:
- Abrams: melee build, must be in punching range. Test tanky Abrams vs several enemies, some gun, some spirit.
- Apollo: 3 lunges forward (can miss a target straight ahead, aim/steer); 1 lunges him backwards, so position shifts.
- Baba: 2 gives a unique melee; steals spirit power, so test against spirit heroes.
- Calico: invulnerable AoE around herself, must be next to an enemy. Gloom Bombs and dash are easy to miss.
- Celeste: build stacks on 3 before ult.
- Drifter: no isolated damage unless he ults the target; starts with no isolated stack, so early numbers read low (note it).
- Grey Talon: damage grows per owl kill.
- Infernus: dash leaves afterburn; nobody stands in it the whole duration, so don't credit full-duration damage.
- Kelvin: extra damage while riding the ice path, but the path moves him off his aim.
- Lash: damage scales with height; see range questions above.
- Deadman Danny: poor farm; assassin pattern is 2 slam then ult.

## Additions (Kieran, Oct 24 02:24)
- Price points: add a lane checkpoint at ~5k souls (very early game) and a full-build (12 items) checkpoint, besides 10k/18k/24k/30k.
- Stack mechanics are everywhere, not just Berserker/Celeste. Model every one the build uses:
  - Hit-based amps: Celeste 3 (damage amp per hit), Pocket Barrage, Ballistic Enhancement imbued on an ability (+20% per target hit, scales with multiple targets: 40/60/80), Celeste Radiant Daggers (+7% spirit per hit, max 6 stacks), Glass Cannon, Fiery, etc. Read each item/ability for its stack rule; hit one vs several targets accordingly.
  - Berserker: weapon damage up as you take damage; 120 damage taken = 1 stack, max 10, 10 s window. Taking damage while stacked refreshes the window; if the window lapses all stacks reset to 0. Self-damage keeps them (Geist Daggers, Vampiric Burst, maybe others; towers and troopers may also give stacks).
  - Weapon quirks: Danny's charging gun, McGinnis ramping Fiery. Read every hero's gun.
  - Drive stacks with real play (hit with the ability, take incoming damage) or lowhp/hurtme/incoming; test 0 / partial / max.
- Accuracy: mix headshots and body shots using a realistic high-rank average (Eternus-level; best guess if no source, state the figure). Not body-only.
- Healing by source: the game's end-of-match stats screen has graphs for healing by type, regen by type, damage by type, souls by source. Try to read it (or the equivalent data in-game); otherwise subtract with/without runs.
- Read every hero and every ability/item in the game (parallel sub-agents) before planning, then keep testing.

## Confounds: kit first, Occam's razor (Kieran, Oct 24 03:59)
- Before crediting a damage difference to an item, a headshot, or a build, check the hero's own kit for the simple explanation: gun that ramps per hit (stacking damage per bullet landed, charge-up, spin-up, Fiery ramp), ability stacks, passive resets/decays, cooldown state, ammo/reload state.
- Every block must start from the same kit state: wait out stack decay / reset timers (verify stacks are zero via modifiers or a fixed idle period from the kit data), cooldowns ready, full ammo, same distance. Order effects (the first block low, a later block high) are the first suspect, not the item.
- Measure in a way that separates them: report damage per shot by consecutive-hit index (shot 1, 5, 10...) and by head/body, so ramping and headshots are visible separately. Compare items at the same stack count, not the same elapsed time.
- Write the likely kit explanation for every result next to the number, and only credit an item/build when the kit explanation is ruled out (counterbalanced order, equal stacks).
- Figure out each hero individually; none is generic. Time-in-effect confounds: Victor's aura does more damage the longer it stays up, so an item tested for longer looks better only because the target was in the aura longer. Every comparison uses identical durations and identical time-in-effect (aura/DoT/channel/ramp age), and per-second numbers are reported against effect age. The hero in the log was Haze (the enemy bot default); the player's hero is whatever the build is for, never assumed.

## Boons, ability points, distance (Kieran, Oct 24 04:06)
- Test with the boons and ability points a player has at that soul level, not max. At each checkpoint set hero level (boons: HP, damage, etc.) and spend ability points in the build's listed order (data.js ability order, `abil` per slot) so each tier does what it does at that point. Verify with a log of level, max HP and per-ability tier at every checkpoint. Current tester state (unlock 7 = all abilities max everywhere) is wrong for every checkpoint below full build.
- Distance: for close-range abilities and items (melee, Calico, Abrams, shotguns, point-blank effects) the enemy is moved to the ability's effective range (use `fetch <dist>`/enemy placement), not left at 350 units. Take the range from the kit data per ability; range-limited items (Long Range vs Close Quarters) are tested at both ends.


---

# 2. HARNESS AND METHOD (AUTORUN.md)

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


---

# 3. KNOWN GAPS (GAPS.md, red-team pass; [U] = unverified in game)

# Sandbox Tester gaps (what Kieran has NOT told us yet)
Derived independently from audit/items_full.json, audit/hero_*.txt, data.js builds (81 builds, 44 heroes) and the ops in AUTORUN.md. Anything not in TEST_MATRIX.md. Ranked by (wrongness of result x number of builds hit). Confidence: H = read straight from data, M = inferred from data + AUTORUN, U = from game knowledge, verify in game first.
Coverage counts below are builds in data.js whose core boxes contain the item.

## A. Setup errors that can invalidate whole result sets

**1. Imbues are never applied (ops list has no imbue op).** [M] 67 of 81 builds have imbue items (Compress Cooldown, Mystic Expansion, Duration Extender, Echo Shard, Surge of Power, Mystic Reverb, Quicksilver/Mercurial, Ballistic Enchantment; `imb` field in builds_ov.json). AUTORUN ops: `give <class>`, `cast iN`; nothing assigns an item to an ability. Un-imbued, these items give 0 (Surge: no spirit, Reverb/Echo: nothing, Compress: no CDR). Whole spirit builds then look worse than gun builds.
- Why current tests mislead: any "spirit vs gun" or "with/without imbue item" result is suspect.
- Fix: op `imbue <item> <abilitySlot>` (or confirm `give` auto-imbues; check via `cds` and an ability stat); verify by effect, e.g. Mystic Expansion changes ability radius, Compress changes recast interval.
- Also check [U]: can several items imbue ONE ability? 20 builds do exactly that (e.g. graves_ult: Duration+Compress+Echo all on 4; mcginnis_ult x4; apollo Expansion+Compress+Reverb on 3; dynamo_damage 4 items on 1). If the game allows only one imbue per ability, those builds are impossible; if it allows many, test that effects stack and that Echo Shard still doubles correctly with Compress (ImbuedCooldownMultiplier 100).

**2. Ability points and hero level are not tied to souls.** [M] `unlock` defaults to 7 (all 3 tiers of ALL abilities). Real players at 5k/10k/18k have only the abilities and tiers the `order` array has bought so far (e.g. abrams order 3312224444111332: Infernal Resilience first). Haze plan already says "unlock 8/10/13/16/18 is an assumption". Also many item stats scale with level boons (`ELevelUpBoons`: Headhunter 75 (+4x), Cultist 50 (+4x) HP and +0.8x weapon %, Spirit Shielding 300 (+5x), Majestic Leap 200 (+12x), Express Shot 125 (+2x)), plus base HP/weapon damage per level.
- Why misleading: early checkpoints (5k, 10k) have far too much power, ults and T3s available; late stats may be off if `souls n` does not move level.
- Fix: scenario table per price point: souls -> level/boons -> ability points -> tier of each ability from `order` prefix (T1/T2/T3 costs in points, [U] about 1/2/5). Add op `level n` / `abilitypoints <order string>`. Verify at each checkpoint by reading base HP and weapon damage and compare with the game's known level table.
- Also verify [U] that `give` applies shop category bonuses (walk_*.txt shows per-category spirit/health/gun bonuses by souls spent: "souls 4800 | gun 0 spirit 4000 health 800"). If items are granted instead of bought, those bonuses may be missing.

**3. Range of the target (350 u) sits inside close-range thresholds.** [M] Long Range 40% and Sharpshooter 60% need target beyond 15 m; Close Quarters 20% and Point Blank 50% apply within 15 m. 15 m is roughly 590-790 u depending on unit scale [U], so a bot at 350 u is "close" for every test. Hits 6 builds (long range) and 15 builds (close). Also bullet damage falloff by distance [U] and spread (unmeasured).
- Why misleading: gun builds with Long Range/Sharpshooter (greytalon, vindicta, paradox, holliday, danny) never get the bonus; Close Quarters/Point Blank builds always get it. AUTORUN also warns aim offsets are calibrated only for 350 u.
- Fix: run each gun/range-item build at 3 distances (5 m, 12 m, 25 m) and weight by the build's play distance (see playstyle/<hero>.md); recalibrate `aimoff` per distance; log measured distance in m.

**4. Enemy HP floor keeps the target at 90-100% always.** [M] `egod` default floor 0.9 restores HP whenever below 90%. Items/abilities keyed to target HP: Opening Rounds (>50% bonus, 16 builds), Danny Close The Deal (+75% under 50%), Ira Domini execute (8%), Guided Owl LowHealthEnemyThresholdPct 22, Rake +6% missing HP and trooper execute, Tankbuster/Decay/Toxic (current or max HP %), Healbane HealOnKill 275, Shiv Killing Blow, Spirit Burn thresholds (500 dmg in 5 s).
- Why misleading: Opening Rounds overvalued, every execute/low-HP bonus reads 0.
- Fix: `ehp` profile op: bot HP follows a real fight curve (100% -> 0% over the build's kill time, then reset), or measure time-to-kill from full HP on a finite-HP bot (e.g. 3500 HP at 30k) and report damage split above/below 50%/25%/8%.

**5. Kill and pickup mechanics can never trigger.** [M] Bots never die: Bebop Sticky Bomb (+2.5% per kill, permanent), Guided Owl (+8 spirit per kill, user notes grows per owl kill), Glass Cannon (+7% fire rate per kill, 3 builds), Healbane (275 heal on kill), Yamato Shadow Transformation kill extension (2 s) and heal, Mina Rake HealPerKill 25, Violet Still Life sketches (permanent stats on pickup), Trophy Collector (14 builds, needs kill/assist, stacks to 16), Shocking Reanimation (only fires on lethal damage; `lowhp` is clamped >= 3%), Cheat Death (lethal-damage immunity).
- Why misleading: kill-scaled builds look like their base kit; revive/immunity items read 0.
- Fix: op `ekill` (kill bot then respawn at hp) so kill stacks/Trophy can be driven explicitly; op `lethal` (deal lethal hit) for Cheat Death/Reanimation; report "no-kill" and "after N kills" columns, never one number.

## B. Incoming damage / CC / healing realism

**6. `incoming` is a stream of tiny ticks, not discrete hits.** [M] `incoming gun 100 dps` deals dps*0.1 each 100 ms via Hurt (bypasses OnTakeDamage csv). Items keyed to per-hit size or to bullets: Witchmail (hits >= 75), Spellbreaker (hit >= 175), Spirit Shielding (225 in 3.5 s, ok cumulative), Plated Armor (30% deflect per bullet, 50% proc deflect), Return Fire (fires at attacker per damage), Rat King Royal Pestments (per-hit cap, 15% return fire), Counterspell/parry, Metal Skin (bullet-only), Escalating Resilience (bullets that HIT), Bullet/Spirit Resilience (resist applies, fine). Also unknown [U]: does `Hurt` feed damage-taken hooks (Berserker 120/stack, Pain Battery charge, Infernal Resilience regen, Infuser?). 11 builds with Witchmail/Spellbreaker, 25+ with Pain Battery-like or Berserker interplay.
- Why misleading: threshold and per-bullet defensive items read 0 or wrong; Berserker/Pain Battery/Infernal Resilience may not charge at all.
- Fix: `incoming` profiles: gun = N shots/s of X damage (e.g. 12 rps x 35 headless/body mix), spirit = bursts of 150-300 plus DoT ticks; ideally real bot fire (bots' attack is disabled; allow it for a "shoot back" block). First verify with one scenario that Berserker stacks, Pain Battery charge and Infernal Resilience regen appear after `incoming` and after `hurtme`.

**7. No way to apply CC, slows, silence, disarm, sleep, root to the player.** [H] TEST_MATRIX demands CC runs but AUTORUN has no op. Counters in 28 builds: Unstoppable, Dispel Magic, Reactive Barrier, Debuff Reducer, Indomitable, Enduring Speed, Juggernaut, Warp Stone, Divine Barrier, Metal Skin. Channels at risk: Bebop Hyper Beam 11 s, Seven Storm Cloud 7 s, Dynamo Singularity 2.75 s, Rem Naptime 1.9 s, Kelvin Arctic Beam 5 s, Rescue Beam 2.5 s, Infernus ult 3.25 s fuse (uninterruptible), Haze Bullet Dance, Yamato Power Slash 1.4 s charge, Grey Talon charge.
- Fix: ops `ecc stun|slow|silence|disarm|sleep|root|knockdown <s>` (apply directly via modifier or via an enemy cast), plus metric "channel completion rate" and "damage landed within the first X s after CC cleanup".

**8. Anti-heal on the player is absent, so Leech is zero by construction.** [H] Leech: "Reduces the effect of enemy applied healing reduction" (28% spirit+bullet lifesteal otherwise ordinary). Real enemies carry anti-heal: Healbane -35%, Toxic Bullets -35, Inhibitor -40, Crippling Headshot -35, Spirit Burn -70, Decay -50, Napalm -33, Consecrating Grenade -30 (25 builds buy such items). Cheat Death gives -60% heal amp itself. The Oct 24 Victor finding (Leech worst) is explained: bot applies no anti-heal. Also `eitem` anti-heal items only proc when the bot shoots (it does not).
- Fix: op `eheal <pct>` applying the heal-amp penalty modifier directly to the player (35/70%); rerun Leech vs Infuser vs VB with 0/35/70%.

**9. Fortitude / out-of-combat regen are scored in the wrong state.** [M] `OutOfCombatHealthRegen` appears on 25 items used, Fortitude (21 builds) needs 10 s without damage then regens 2.25%/s up to the 75% threshold with +375 HP; `incoming` keeps you permanently in combat, and `lowhp` clamps HP every frame which defeats HP-gated items: Enchanter's Emblem, Battle Vest, Hollow Point (above 65%), Bullet/Spirit Resilience (below 50%), Frenzy (below 50%), Healbane, Berserker bonus.
- Why misleading: fight-only runs give 0 for the entire between-fights recovery game that these items are for; lowhp runs give 0 for all above-threshold bonuses.
- Fix: scenario "fight-rest cycle": 8 s fight with incoming, 25 s rest (no incoming), measure HP at next engage and total HP gained; and HP sweeps (100% -> 40% over the fight) instead of clamping, reported by HP band.

**10. Allies absent: support and aura items are scored without allies.** [M] Heroic Aura, Guardian Ward, Divine Barrier, Rescue Beam, Healing Rite/Nova, Scourge on ally, Plot Armor, Tag Along (15% missing HP burst, hop once per ally), Spiritual Overflow on Nurse (procs when she heals teammates), Healing Tempo (buff on healed target), Spirit Shredder (allies get lifesteal), Rem pillow/cooldowns. AUTORUN: `incoming` only hits the player; 2 practice bots only. TESTER.md leaves "can allies be spawned" unanswered.
- Fix: spawn an ally bot (or the second bot as friendly) with its own `incoming` and `lowhp`; score ally survival time and ally HP healed, plus idle time. If impossible, mark all support builds BLOCKED rather than scoring selfheal only.

## C. Measurement bias (damage CSV / heal diff / timing)

**11. Delayed and over-time damage is cut off or leaks into the next label.** [M] Blocks are labelled by `mark`. DoTs/delays: Spirit Burn (8 s burn), Toxic bleed (4 s), Decay 12 s, Afterburn/Napalm burn 3-8 s, Mystic Reverb (3 s delay), Static Charge (3.5 s), Sticky Bomb (3.5 s fuse), Concussive (3.25 s), Captivating Read (1.25 s), Focus Lens (35% paid on expiry after 4.5 s), Pain Battery bolts, Rakes. If the next `mark` comes before they land, the first block loses it and the next block is polluted (this is a candidate cause of the observed "first block runs low", which was blamed on warm-up).
- Fix: `tail <s>` (default 12 s) with no input before every mark change; attribute damage by source tag; report "damage within block" and "damage within block + tail" separately.

**12. Burst-window/charge-up/cooldown-gated items measured in short windows.** [H] Mystic Burst/Tankbuster (charge 14 s, then needs an ability hit >80/>165; 25 builds), Quicksilver (18 s charge)/Mercurial (14 s) (imbued ability charges over time, 12 s buff after use), Spirit Burn (500 dmg in 5 s, 20 s immunity per enemy, 25 builds), Love Bites (10 s per target, Mina), Recharging Rush (200 dmg in 3.5 s, 25 s), Express Shot (8 s), Headshot Booster/Headhunter (8 s), Silencer immunity 10 s, Mystic Shot 8 s, Spellbreaker 9 s, Spirit Shielding 45 s, Reactive Barrier 55 s, Witchmail, Cultist 270 s. After `hardreset` they start uncharged; inside a 5-10 s block they proc once at most.
- Why misleading: rewards/penalises items depending on whether the block length matches their cooldown; a flat DPS number hides that.
- Fix: report two scenarios: "first engagement from full charge" (wait 15 s after setup) and "repeated engagements every 25-30 s", scored as damage per full cycle including ult and cooldown downtime; add warm-up wait that matches the longest charge-up in the build.

**13. Proc randomness vs sample size.** [H] Tesla 15%, Lucky Shot 25%, Armor Piercer 55%, Capacitor 20%, Headshot-gated procs, Silencer/Inhibitor/Toxic build-ups. 25 shots at 15% = 3.75 +- 1.8 procs (CV ~ 48%); the 3 repeats in the matrix cannot separate a 10% item.
- Fix: compute needed shots from proc rate (>= 200 shots per arm for a 15% proc), or report confidence interval and "INCONCLUSIVE" per TESTER.md rule.

**14. Build-up items are nonlinear in hit pattern.** [M] Silencer (1.04/shot, decays over 5 s), Inhibitor 0.77, Toxic 1.28, Spiritual Overflow 1.08 (needs continuous hits for bonus fire rate/spirit/lifesteal), Love Bites 18.4, Glass Cannon 1.2, Afterburn 8.1%/hit, Intensifying Magazine (needs 2.5 s continuous fire, resets on stop/reload). `accuracy` flips per 170 ms window randomly; real misses cluster (you lose the target for 1-2 s, then spray). Same mean accuracy, different build-up.
- Fix: add streak mode (hit for 1.5-3 s, miss for 1-2 s) and compare to random-window mode; report both for build-up items.

**15. Reload / ammo lifecycle.** [M] Empty mag = no shots; `cast reload 2.5` is placed before `fire`. Items that change reload/mag: Titanic +100%, Extended +30%, Lucky Shot +30%, Quicksilver/Mercurial refill on use, Express Shot uses 2 ammo, Vampiric Burst adds ammo (ActiveReloadPercent 75), Spellslinger reload speed -10%/stack, Active Reload (needs timed press in the highlighted segment; 4 builds + VB), Fleetfoot/Kinetic Dash (+6 ammo until next reload). A `fire 10` block either stops when the mag empties (no reload downtime) or silently excludes reload time.
- Fix: continuous fire with auto-reload (count reload downtime); a scripted Active Reload press as "perfect timing" upper bound and as a 0-benefit lower bound; report mags per fight.

**16. Hit-rate model is gun-only; abilities always hit.** [H] `accuracy` affects bullets. Stationary bots never dodge projectile abilities: Bebop hook, Strix Salvo missiles, Charged Shot / owl, Lightning Ball, Stake, Sticky Bomb, Gloom Bombs, Pulse Grenade, Time Wall, Rook, bishop. Bullet speed items (High-Velocity Rounds +60%, in 24 builds; Opening Rounds, Armor Piercer, Express Shot velocity, Sharpshooter) have no value against a standing target at short range.
- Fix: `emove` op: bot strafes/jumps/dashes on a recorded pattern (TESTER.md mentions recording; AUTORUN has no op), plus per-ability expected hit-rate table (hook ~50-70%, skillshots ~60%, ult ~80% [U]); report ability damage x hit-rate.

**17. No enemy aggression: no interrupts, no pressure, no peel.** [M] Bots never shoot: nothing cancels channels or the Rejuvenating/Rescue/Arctic channels, nothing triggers Riposte (needs melee), Counterspell parry, Plated Armor, Return Fire, Spirit Shielding. Also Hunter's Aura / Suppressor / Silencer / Inhibitor / Juggernaut slow enemy fire rate and damage output: invisible in damage CSV because the enemy has no output.
- Fix: enable bot attacks in a "shoot-back" block with realistic fire and score player survival/time-to-die, not only damage dealt. Debuff-on-enemy-damage items (list above) are only scoreable this way.

## D. Item interactions inside the same build

**18. Stacking rules of same-category debuffs are unverified.** [U] Bullet resist shred: Bullet Resist Shredder -10, Hunter's Aura -10 (x2 vs one enemy), Hollow Point -10, Crushing Fists -5/stack (max 6), Stalker -6, Alchemical Fire -7, Jettison -15, Armor Piercer ignores. Spirit shred: Mystic Vulnerability -8 / Escalating Exposure 4.5% per stack to 12, Spirit Strike -6, Snatch -12, Rend -8, Shredder -8, Sap -9, Focus Lens -9. Anti-heal: -35/-40/-70/-50 combos. Fire rate slows, move slows. Are they additive, max-only, or diminishing? Builds stack 3-5 shreds (abrams_melee, billy_damage, calico_gun). Fire-rate bonuses (Rapid Rounds 9, Swift Striker 20, Burst 10/32, Active Reload 25, VB 34, Spellslinger 6x11, Blood Tribute 35, Frenzy 15/40, Ricochet 18, Spiritual Overflow 25) and CDR (Compress 18, Superior 20, Transcendent 25, Enchanter 5, Spellslinger 5, Witchmail 7) may cap.
- Fix: apply items one by one then in pairs; measure bullet damage per hit on a resist-bearing bot (`eitem` resist), shots/s, observed cooldown recast time. Cooldown readers return garbage (AUTORUN), so measure by observed recast times in the damage CSV.

**19. Resist/debuff application order and non-stacking procs.** [M] Hunter's Aura needs the target within 15 m and halves with a second enemy (5-bot ring vs single flips the item). Escalating Exposure proc cooldown 0.7 s, 12 stacks; Spirit Burn per-enemy cooldown; Mystic Regeneration stacks on different heroes only; Fixation and Ballistic scale by target count/target identity; Siphon Bullets proc cooldown 1.2 s with ring vs single. Report each item at 1 target and at 3-5 where it counts target identity.

**20. Self-damage and recoil are not netted.** [H] Danny Chimera 10% max HP + self-stun 1.3 s on whiff, Close The Deal both take fall damage; Bebop Sticky Bomb SelfDamage 20%; Victor Jumpstart 15% current HP and Aura 70%/15 dps self; Geist bombs; Blood Tribute 50 HP/s; Glass Cannon -13% max HP. Raw `healDiffObserved` ignores it.
- Fix: report net sustain = healing - self-damage, and Berserker/Pain Battery stacks credited from self-damage where the game does (user said yes for Geist Daggers/VB).

**21. Soul economy items are untested.** [M] Cultist Sacrifice (11 builds): needs a target NPC, 170% bonus souls, 270 s cooldown, 160 s buff: +30% NPC weapon power, +1 ability charge, +12% range/radius, +HP; the buff is NOT permanent and is absent if the active was never used. Monster Rounds (+25% NPC damage), Trophy Collector (-15% damage vs NPC, up to 16 stacks of +16 gold/min), Rake trooper execute, Arctic Beam souls, Restorative Shot (NPC 20 vs hero 50), Lifestrike/Melee Lifesteal/Siphon Life non-hero effectiveness 30-40%, Alchemical/Spirit Burn/Toxic half vs NPC. Only 1 of 35 scenarios (generic_camp_clear) covers camps.
- Fix: scenario with trooper wave + camp; metric souls per minute and camp clear time at each checkpoint; Cultist block with eat then 160 s of buff, then expiry.

## E. Build-order / data validation

**22. 12-slot cap and sells.** [M] walk_*.txt shows 12 slots max everywhere, but builds hold 16-24 items; "Sell X for Y" lives in free text. "Full 12" is ambiguous (which items are sold, when). Tested loadouts at late checkpoints must follow the sell notes or the walk's own slot accounting; upgrades consume components (Mercurial uses Quicksilver, Leech uses Bullet+Spirit Lifesteal), so `give` of a component and its upgrade double counts.
- Fix: generate loadout per checkpoint from the walk, apply upgrades by removing components, apply listed sells, assert <= 12 slots.

**23. Disabled/dead items.** [H] items_full has 18 items with `disabled: true` (e.g. Ammo Scavenger, Glass Cannon v2). Checked: no data.js build uses them. Add this check to the patch-rerun (new patches re-enable/disable items).

## F. Utility items scored as zero

**24. Mobility and utility have no metric.** [M] Extra Stamina, Stamina Mastery (21 builds), Sprint Boots, Enduring Speed, Juggernaut, Slowing Hex, Vortex Web, Warp Stone, Veil Walker (needs a veil in the map), Kinetic Dash, Arcane Surge (needs dash-jump before the cast; stamina), Fleetfoot, Burst Fire speed, Majestic Leap, Magic Carpet, Colossus (slow aura + resist), Trophy range. Damage CSV shows 0.
- Fix: chase/kite scenario: bot flees at hero speed; metric = time to close 30 m, time in range, stamina-gated dash count, escape time; fight engage latency. This also covers matrix "enemies that run away".

## G. Hero-specific quirks from the data (each needs a line in its plan)

| Hero | Quirk (data) | Test change |
|---|---|---|
| Abrams | Shoulder Charge wall stun; Siphon Life heals only from damage (70% hero / 35% NPC) within 8 m; Infernal Resilience regen = 13% of damage taken over 20 s | wall in map; ring within 8 m; incoming profile |
| Bebop | Hyper Beam 11 s at 1.8 m/s, cast delay 1 s, beam damage by distance (BeamCloseDamagePercent 75 [U]); hook skillshot; Sticky Bomb diminishes after 60 hits / 7 kills | beam hit-time; bomb stacks via `ekill` |
| Danny | Chimera overheats at 5 s; whiff = self-stun 1.3 s + 10% HP; ult +75% under 50% HP; jettison vents jetpack | enemy HP profile; whiff column |
| Dynamo/Rem/Kelvin/Viscous | heal numbers scale with spirit and need allies; Aurora 5 s channel (interruptible) | ally + CC ops |
| Grey Talon | Charged Shot hold has no cap; Snare needs enemy to walk in (arm 2 s); owl +8 spirit/kill; Rain gives multishot only airborne | moving bot, kills, airborne window |
| Haze | Bullet Dance auto-aims (accuracy setting irrelevant for 3.5 s); Fixation is per target and expires 6 s; sleeping target is a free target; Smoke breaks on attack | target switching; sleeping vs awake |
| Infernus | Napalm gives +16% damage taken from him; Afterburn T3 trades spirit damage -35%; Concussive 3.25 s fuse, stun at end | bomb dwell probability; napalm first |
| Mina | Love Bites 10 s per-target cooldown; headshots x1.5 buildup; bat count grows with each bite | 10+ s windows; headshot model |
| Paige | Rallying Charge damage grows with distance (600 m cast range); Plot Armor needs ally | long-distance ult scenario |
| Rat King | Pestments barrier 15% max HP and per-hit cap; Return Fire 15% per bullet; grenade scales with weapon damage (gun items count) | discrete incoming hits |
| Seven | Static Charge delay 3.5 s, needs target to stay; Storm Cloud no damage without LOS, radius 10->30 m over 3.5 s, channel 7 s; Power Surge once per burst | CC op, LOS, dwell |
| Venator | Gutshot wall bonus within 7 m; Ira Domini 3 stakes, execute < 8% HP, 15 s window | wall, HP profile |
| Victor | Pain Battery needs stored damage = 40% max HP; Jumpstart self-damage; Reanimation on lethal | incoming profile + `lethal` |
| Violet | Living Ink cuts cooldowns per hit; Still Life needs sustained look and drops pickups | pickup/kill, hit counting |
| Wraith | Card Trick resource comes from bullet hits (4), crits (6), melee; Full Auto adds magic damage per bullet | couples gun accuracy to ability damage |
| Yamato | Power Slash charge stages (30/50/100%); Shadow Transformation extends on kill | charge time, `ekill` |
| Billy/Sinclair/Pocket/Geist/Rat King/Seven/Venator | Cultist Sacrifice must be used on an NPC | see #21 |
| Melee builds (Abrams, Apollo, Billy, Drifter, Silver, Venator, Viscous, Yamato, Calico) | light vs heavy melee have different cooldown multipliers (Lifestrike x1.5, Spirit Strike x2, Melee Charge/Crushing Fists need heavy) and `cast melee` is one op | add `melee light|heavy`, mix by playstyle |

## H. Not yet derivable (unknown from data)
- Heroes without hero_*.txt data (Apollo, Baba, Billy, Calico, Celeste, Doorman, Drifter, Geist, Graves, Holliday, Ivy, Lash, McGinnis, Mirage, Mo & Krill, Nurse, Pocket, Shiv, Silver, Sinclair, Vyper, Warden): abilities were not extracted, so quirks above are limited to what builds and user notes say. Extract these before planning those heroes.
- Whether `souls n` recalculates level (see #2) and whether the map has walls/LOS/veils at the bot position (see #7, #24).

## Tester ops needed (summary)
`imbue`, `level`/`abilitypoints`, `distance m` (recalibrated aim), `ehp` profile or finite-HP bot, `ekill`, `lethal`, discrete `incoming` profiles, `ecc`, `eheal`, ally bot + `allyinc`, `emove`, `tail`, streak accuracy, auto-reload fire, `melee light|heavy`, NPC/camp spawn, shoot-back mode.


---

# 4. PER-HERO PLAY MODELS (playstyle/*.md; heroes without ability extracts are marked uncertain)

# Abrams
Builds: abrams (tank), abrams_melee (melee)

**Real play.** Frontline brawler. Walks into the enemy cluster and stays inside 8 m so Siphon Life keeps ticking; Infernal Resilience turns damage taken into regen (13% of incoming over 20 s), so he WANTS to be shot. Tank: Scourge on self as he ults in. Melee: Colossus popped as he commits.

**Rotation.** Tank: Scourge self > Shoulder Charge (pin to wall = stun) > Siphon Life on while hit > Seismic Impact (leap 6 m, 1.6 s stun, 9 m radius) when 2+ are grouped. Melee: Charge into wall > heavy melee (Melee Charge/Crushing Fists) > light melee spam (Lifestrike, Melee Lifesteal) > Berserker stacks from damage taken.

**Souls/economy.** Farms by punching camps/troopers (melee build heals off NPCs at 30-40%). No scaling farm tool.

**Test must model.** Enemies must be shooting him (incoming discrete hits), a wall behind the target for Charge stun, heavy vs light melee mix, ring of 3-5 within 8 m for Siphon (it heals per target-damage), Berserker 0/mid/max.

**Uncertain.** Charge speed/turn and wall availability in the sandbox map (uncertain).


# Apollo
Builds: apollo (spirit), apollo_melee (melee)

**Real play.** Dueling skirmisher. Riposte (2) parries melee/wins trades; Flawless Advance (3) lunges forward and Disengaging Sigil (1) throws him backwards (user note), so spacing shifts every cast. Spirit build stacks Mystic Burst/Tankbuster/Reverb on one imbued ability; melee build punches after Riposte stun.

**Rotation.** Spirit: engage with 3, 1 to create distance/damage, 2 when they melee/burst, ult at close range. Melee: Riposte > (stun) > heavy melee via Melee Charge > light melee; Witchmail + Lifestrike sustain.

**Souls/economy.** Normal laner; no special farm tool. Spirit build relies on ability farming.

**Test must model.** Lunges move him off-aim: steer/re-aim after each cast; target moves; Riposte needs the enemy to melee (needs enemy attack op).

**Uncertain.** Which ability the user means for 'lunge forward/back' follows his note, not verified in data (uncertain).


# Baba
Builds: baba (gun/spirit hybrid), baba_tank (tank)

**Real play.** Spirit-lifesteal bruiser. Threadsap (1) steals spirit power (user note: tests need spirit-heroes), Granny Long Legs (2) gives a unique melee, Baba's Brew (3), Feed The Birds (4). Glock build shoots with Burst Fire/Spiritual Overflow/Ricochet; tank build sits in fights with Torment Pulse/Healing Booster/Radiant Regeneration.

**Rotation.** Cast abilities constantly (Radiant Regeneration heals per cast, Mystic Regeneration stacks on different heroes), weave bullets between casts; ult when grouped.

**Souls/economy.** Gun farm; Extra Charge and CDR let her spam spells. No special economy.

**Test must model.** Cast-heal items need a rotation that actually casts on cooldown; steal effect needs a spirit-using enemy; Granny melee range; tank build needs incoming damage.

**Uncertain.** Ability details from data.js only (no hero file); treat numbers as unverified.


# Bebop
Builds: bebop (1v1 lane bully), bebop_bomb (spirit bomb), bebop_support (wingman)

**Real play.** Hook-and-punch brawler. Grapple Arm (3) pulls the first thing hit (allies too), Exploding Uppercut (1) tosses and detonates on landing, Sticky Bomb (2) gets permanent bonus damage per hit/kill (2.5%/kill, 1%/hit; halves after 7 kills/60 hits), Hyper Beam (4) is an 11 s channel at 1.8 m/s move speed (cast delay 1 s).

**Rotation.** Hook > uppercut (Bullet Resist Shredder drops on the landing) > bomb > shoot; ult when the team is in or the target cannot leave; Unstoppable first on support build.

**Souls/economy.** Gun/ability farm; bomb stacks need hero hits and kills, which come from fights, not farm.

**Test must model.** Hook is a skillshot (50-70% hit in real play): script hook miss/hit mix; bomb stacks only come from hero hits/kills (bots never die); beam needs target to stay in 70 m line and he is slowed; solo vs side-lane gun carry uses Hunter's Aura x2 (single enemy).

**Uncertain.** BeamCloseRadius/BeamCloseDamagePercent meaning (75% damage inside 5 m?) is a guess.


# Billy
Builds: billy (tank), billy_damage (damage)

**Real play.** Melee rusher with no good clear, so Cultist Sacrifice (~8:00, ~7k souls, eat a big camp) is part of the build. Bashdown (1), Rising Ram (2), Blasted (3), Chain Gang (4, ult: chains them in). Colossus popped as he chains.

**Rotation.** Ram/Bashdown to close > light/heavy punches (Lifestrike, Melee Lifesteal, Crushing Fists, Spirit Strike on Bashdown) > Chain Gang to hold targets in his melee range; Berserker on damage build.

**Souls/economy.** Cultist Sacrifice is mandatory timing (170% bonus souls on eaten NPC, 270 s cooldown, 160 s buff). Sell it late for Cheat Death in tank build.

**Test must model.** Cultist must be USED on an NPC (needs a camp creep in sandbox); buff is 160 s of every 270 s, not permanent; melee only (not shooting); Berserker needs incoming damage.

**Uncertain.** Rising Ram/Blasted details not in the data; assumed from the build notes.


# Calico
Builds: calico (spirit melee/bombs), calico_gun (gun)

**Real play.** Assassin cat. Leaping Slash (2) jumps in, Gloom Bombs (1) are thrown (easy to miss, user note), Ava (3), Return to Shadows (4) ult. User note: invulnerable AoE around herself so she must be next to the enemy. Spirit build slashes in, pops Cold Front to slow, then bombs; gun build uses Close Quarters/Point Blank/Split Shot at short range.

**Rotation.** Spirit: Scourge on self > slash in > Cold Front > bombs > melee/Ava > ult. Gun: close range shooting with lifesteal, Glass Cannon snowball.

**Souls/economy.** Gun farm for gun build; spirit build farms with bombs.

**Test must model.** Enemy must be adjacent; bombs and slash need moving-target miss rate; Glass Cannon stacks need kills (never happen in sandbox).

**Uncertain.** Ava/Return to Shadows details are from user note only.


# Celeste
Builds: celeste (spirit healer), celeste_carry (gun carry)

**Real play.** Spirit caster with stacking daggers. User note: build stacks on ability 3 (Radiant Daggers +7% spirit/hit up to 6 stacks) before the ult. Healing build heals via Radiant Regeneration/Healing Booster/Tempo; carry build uses Quicksilver/Mercurial on Radiant Daggers and shoots.

**Rotation.** Build 3 stacks by hitting with daggers on a target, then Shining Wonder (4); Light Eater (1) and Dazzling Trick (2) fill. Carry: weave bullets with Kinetic Dash resets.

**Souls/economy.** Normal laner; Mystic Regeneration stacks on different heroes.

**Test must model.** Hit-count stacks (0/3/6) with 1 and several targets; mix of bullets and spells; Mercurial/Quicksilver imbued on 3 and charged (14-18 s).

**Uncertain.** Light Eater/Dazzling Trick unknown from data.


# Danny
Builds: danny (dive), danny_gun (gun-spirit)

**Real play.** Jetpack diver. Chimera Mk1 (2): fly, overheat after 5 s, dive explosion launches nearby enemies; if no hero is hit you stun yourself 1.3 s and take 10% max HP. Close The Deal (4) grabs an enemy (10 m), both take fall damage, +75% on enemies under 50% HP. Strix Salvo (1) marks, charged gun consumes marks. User note: poor farmer; assassin pattern 2 slam then ult.

**Rotation.** Dive build: Salvo marks > Chimera dive into the target > Jettison Fuel (3, 2 s spray, backblast knocks him back) > ult when enemy < 50%. Gun build: charged gun shots (charge ramp) + Jettison Fuel imbued Surge/Duration.

**Souls/economy.** Weak farm; assassin builds must pick fights. Needs explicit answer to souls (no Trophy/Cultist in dive build).

**Test must model.** Enemy must be under 50% for ult bonus (not at 90% floor); dive can miss (self-stun); Danny takes self damage; fly to reach Vindicta and survive her shots; charging gun warm-up.

**Uncertain.** Charged gun mechanics from user note, not data.


# The Doorman
Builds: doorman (DPS), doorman_support (support)

**Real play.** Utility caster. Luggage Cart (3) carries a mate/self into a fight, Doorway (2) is a portal, Call Bell (1), Hotel Guest (4) ult. Support build puts Guardian Ward/Rescue Beam on the mate he is about to cart, Knockdown on the carry then carts a mate in as the stun lands. DPS build is a short-cooldown spirit spammer (Compress/Expansion on Call Bell).

**Rotation.** Support: ward mate > Knockdown target > cart mate in > ult. DPS: Call Bell spam with Mystic Burst/Tankbuster, Slowing Hex to hold.

**Souls/economy.** Normal laner. Trophy Collector on support.

**Test must model.** Ally required (cart, ward, beam); enemy must stay still for Knockdown (2 s delay); cooldown cycling.

**Uncertain.** Doorway/Hotel Guest mechanics unknown from data; mark uncertain.


# Drifter
Builds: drifter (gun), drifter_spirit (spirit melee)

**Real play.** Stalker/isolator. User notes: no isolated damage unless he ults the target (Eternal Night); starts with no isolated stack so early numbers read low. Rend (1) maxed counts as heavy melee (heals via Lifestrike, triggers Spirit Snatch). Gun build uses Melee Lifesteal+bullet lifesteal, Close Quarters/Point Blank, Hunter's Aura; spirit build Cold Front/Arctic Blast, Tankbuster, Escalating Exposure.

**Rotation.** Mark target (2) > Bloodscent > Rend to max > melee/gun; ult to isolate. Retreat when Stalker's wound runs out.

**Souls/economy.** Trophy Collector; melee/gun farm.

**Test must model.** Isolated vs non-isolated target, full Rend charge before damage counts, melee range, 0 vs max stacks.

**Uncertain.** Rend stack count and isolation rules from user notes only.


# Dynamo
Builds: dynamo (support), dynamo_damage (stomp damage)

**Real play.** Short-cooldown stomper. Kinetic Pulse (1) travels along ground (16 m, 1 s toss; 2 charges at T1). Quantum Entanglement (2) is untargetable teleport that can carry allies. Rejuvenating Aurora (3) 5 s channel heal, can dash/melee while channeling. Singularity (4): 2.75 s channel pull. Support build ults with Warp Stone to teleport into the pack first. User note: Dynamo must still stomp early; don't rush Rescue Beam in lane.

**Rotation.** Pulse for damage in lane; ult: Warp Stone > Unstoppable (damage build) > Singularity with Compress/Duration imbued; Aurora for team sustain.

**Souls/economy.** Trophy Collector; early stomps. Damage build farms with pulse charges.

**Test must model.** Pulse is a linear projectile (miss when target strafes); channel ults can be interrupted (needs CC op); allies required to score Aurora/Rescue Beam.

**Uncertain.** Heal numbers for Aurora from data; ally mechanics not simulated.


# Lady Geist
Builds: geist (gun tank), geist_bomb (bomb)

**Real play.** Self-damaging bruiser: her own bombs hurt her (build notes), so Spirit Resilience cuts that; Blood Tribute drains 50 HP/s for fire rate. Essence Bomb (1), Life Drain (2), Malice (3), Soul Exchange (4). Gun build: Cultist Sacrifice for souls, Berserker (self-damage keeps stacks), Leech. Bomb build: spirit damage with Mystic Burst/Tankbuster/Reverb/Echo on bombs.

**Rotation.** Life Drain on a close target to heal, bombs thrown while draining, Malice, ult to swap souls.

**Souls/economy.** Cultist Sacrifice on gun build.

**Test must model.** Net sustain after self-damage; Berserker fed by own damage; Cultist must be used on NPC.

**Uncertain.** Her ability numbers not in hero files.


# Graves
Builds: graves (gun), graves_tank (tank), graves_ult (ult/ghouls)

**Real play.** Summoner/zombie hero. Jar of Dead (1), Grasping Hands (2), Essence Theft (3), Borrowed Decree (4) summons ghouls (Heroic Aura buffs them). Gun build is a Tesla/Toxic/Ricochet shooter with Surge on Jar; tank build Escalating Resilience (gun hits ~10/s, fills in ~3 s) and Siphon Bullets; ult build stacks Compress+Duration+Echo on Borrowed Decree with Arcane Surge dash-jump first.

**Rotation.** Ult build: dash-jump (Arcane Surge) > ult with imbues > Refresher; keep ghouls alive. Gun: Jar then shoot, Capacitor on the target before the ult.

**Souls/economy.** Gun farm; ghoul summons help.

**Test must model.** Ghoul count and lifetime; ult duration extenders; hit-based stacks vs one/many targets.

**Uncertain.** Decree/ghoul numbers not in data.


# Grey Talon
Builds: greytalon (spirit arrow), greytalon_gun (gun)

**Real play.** Long-range sniper. Charged Shot (1) is held to charge (no max channel), pierces enemies, 4 s charge cooldown (1 s at T3). Rain of Arrows (2) launches him up with +weapon damage and 5x multishot while airborne. Spirit Snare (3) trap arms in 2 s and can be detonated by a charged shot. Guided Owl (4) 1.5 s cast, 20 s steer, stuns 0.75 s, +8 spirit permanently per hero killed. Gun build: Quicksilver/Surge on Rain of Arrows, Burst/Ricochet.

**Rotation.** Place snare, charge shot into snare/target at 15 m+, Rain of Arrows to escape or dive-shoot, owl at range for kill stacks (damage grows per owl kill, user note).

**Souls/economy.** Gun farm with arrows.

**Test must model.** Range 15 m+ for Long Range/Sharpshooter; owl kills stack (bots never die); charge time sets rate; trap needs a walking target.

**Uncertain.** Owl stack timing from user note.


# Haze
Builds: haze (tanky healer), haze_assassin (assassin)

**Real play.** Invisible gun carry. Smoke Bomb (2) invisible 8 s, attacking breaks it; Sleep Dagger (1) does NOT break invis and sleeps (wakes on damage); Fixation (3) +bullet damage per hit on one target (3 stacks per headshot, 40 max, 6 s); Bullet Dance (4) 3.5 s auto-fire at nearby enemies with perfect accuracy. User note: farm until Siphon Bullets then fight; Haze Assassin with Tesla Bullets reloads constantly. Rotation: knife before ult for Surge of Power; Smoke T3 then Vampiric Burst for the big heal.

**Rotation.** Assassin: smoke > dagger (Surge imbued) > Fixation stacking with headshots > ult > Capacitor on fleeing target. Healer: smoke T3 lifesteal + Vampiric Burst, Healing Booster/Tempo amplify.

**Souls/economy.** Healer build farms (Ricochet, Active Reload) until Siphon Bullets; assassin builds need no souls early.

**Test must model.** Fixation 0/20/40 stacks per target, target switching resets; headshot ratio; sleep target means free hits; magazine/reload cycle; Smoke dispels CC.

**Uncertain.** Bullet Dance perfect accuracy ignores the accuracy setting.


# Holliday
Builds: holliday (gun), holliday_spirit (spirit pick)

**Real play.** Sharpshooter/cowboy. Powder Keg (1), Bounce Pad (2), Crackshot (3), Spirit Lasso (4: pulls a target in). Gun build is Long Range/Sharpshooter headshots at 15 m+; spirit build picks a target and lassos with Cursed Relic first. Bounce Pad is a mobility/escape tool.

**Rotation.** Gun: headshot rounds from range, Powder Keg on grouped; spirit: Cursed Relic > Lasso > Reverb/Duration imbued ult then burst.

**Souls/economy.** Gun farm; Trophy on spirit build.

**Test must model.** Distance > 15 m, headshot ratio (Headshot Booster/Headhunter), lasso needs LOS and range.

**Uncertain.** Crackshot/lasso numbers not in data.


# Infernus
Builds: infernus (gun), infernus_dash (dash)

**Real play.** Burn caster. Napalm (1) projectile with 20 m range, 2 charges, target takes +16% damage from Infernus (+17% at T2). Flame Dash (2) leaves a trail (4 s); user note: nobody stands in it the whole time. Afterburn (3): bullets build burn, abilities refresh it, hits extend (T3: spirit damage -35% for more DPS). Concussive Combustion (4): 3.25 s fuse, not interruptible, 12 m radius stun 1.25 s.

**Rotation.** Napalm first (amp), shoot to build burn, dash through the pack with Echo/Duration on dash, ult at the middle then survive (Cheat Death). Gun build is lifesteal+Toxic gunner.

**Souls/economy.** Gun farm with Afterburn.

**Test must model.** Trail and burn credited for realistic dwell (not full duration); ult requires targets to stay within 12 m for 3.25 s; Napalm +16% window applies to rest of rotation.


# Ivy
Builds: ivy (support), ivy_carry (gun carry)

**Real play.** Tether support/carry. Entangling Thorns (1) puts Bullet Resist Shredder on them (drop it before shooting), Kudzu Connection (2) tether (headshot heals pass down to the mate), Stone Form (3), Air Drop (4) carries a mate. Support: Headhunter/Healing Booster/Rescue Beam. Carry: Tesla/Intensifying Magazine/Capacitor/Silencer/Inhibitor.

**Rotation.** Support: tether mate, thorns, air drop in/out. Carry: thorns > shoot (shred applied) with Intensifying Magazine ramp (2.5 s continuous fire).

**Souls/economy.** Gun farm; Monster Rounds on carry.

**Test must model.** Ally required; continuous-fire ramp resets on reload/stop; headshots for Headhunter.

**Uncertain.** Stone Form/Air Drop mechanics from build notes.


# Kelvin
Builds: kelvin (tank damage), kelvin_support (support)

**Real play.** Frost caster. Frost Grenade (1, 2 charges, heals allies in cloud), Ice Path (2: movement path, 8 s; user note: extra damage riding it but it moves him off aim), Arctic Beam (3: 5 s, slows and cuts fire rate, 25 m), Frozen Shelter (4: dome, allies regen, objectives invulnerable). Tank: Torment Pulse/Infuser. Support: Healing Booster/Tempo, Cursed Relic, Warp Stone.

**Rotation.** Grenade to zone > beam on target while riding ice path > dome when team is being pressed.

**Souls/economy.** Ability farm; Trophy on support.

**Test must model.** Beam needs sustained tracking (misses reset ramp); ice path changes position; ally healing scored by survival.


# Lash
Builds: lash

**Real play.** Dive assassin. Ground Strike (1), Grapple (2), Flog (3), Death Slam (4). User note: damage scales with height; second grapple (Extra Charge) gets higher before slam. Mystic Expansion x4 on Ground Strike, Warp Stone.

**Rotation.** Grapple up > Ground Strike slam from height > Flog > Death Slam on grouped enemies.

**Souls/economy.** Ability farm; check whether ult reaches (range question in matrix).

**Test must model.** Height of slam, ult range/radius, Death Slam coverage with 3-5 enemies.

**Uncertain.** Ability numbers not in hero files.


# McGinnis
Builds: mcginnis (gun), mcginnis_turret (turret), mcginnis_ult (barrage)

**Real play.** Turret engineer. Mini Turret (1), Medicinal Specter (2: heal), Spectral Wall (3), Heavy Barrage (4). Gun: Intensifying Magazine/Berserker/Spiritual Overflow, user note: ramping Fiery. Turret: spirit cooldown spam. Ult: Mystic Expansion+Compress+Duration x4 on Barrage.

**Rotation.** Drop turret in position, shoot from behind wall; Specter to heal; Barrage on stationary group.

**Souls/economy.** Monster Rounds farm; turrets farm too.

**Test must model.** Turret needs placement and dwell; ult pattern vs moving enemies; ramp-up continuous fire.

**Uncertain.** Ramp mechanic from user note.


# Mina
Builds: mina

**Real play.** Bat assassin. Rake (1, 16 s, hits up to 6, executes troopers < 60%, damage +6% missing HP), Sanguine Retreat (2: 0.65 s untargetable, recast within 4 s), Love Bites (3: bullets add spirit damage, bite after build-up, 10 s per-target cooldown, headshots build 1.5x), Nox Nostra (4: 75 bats, 150 s). Mina is hard to catch (mobile). Pop Infuser with ult.

**Rotation.** Rake > shoot (build bite) > bite pops > retreat > ult; Spirit Sap before burst.

**Souls/economy.** Rake farms troopers (execute) ; bat count grows with Love Bites triggers over the game.

**Test must model.** Per-target 10 s cooldown (short blocks undercount), headshots matter, bat-count growth, escape from catchers.


# Mirage
Builds: mirage

**Real play.** Marker gunner. Fire Scarabs (1), Dust Devil (2), Djinn's Mark (3: marks stack faster with Compress Cooldown; Ricochet puts marks on two more), Traveler (4: teleport ult). Toxic, Inhibitor, Spirit Rend.

**Rotation.** Mark with 3 across targets while shooting, scarabs for burst, Dust Devil to disengage, Traveler to rotate.

**Souls/economy.** Gun farm; Cultist not in build.

**Test must model.** Mark stacks 0/partial/max across several targets; Ricochet multi-target.

**Uncertain.** Numbers not in hero files.


# Mo & Krill
Builds: mokrill

**Real play.** Burrow brawler. Scorn (1), Burrow (2), Sand Blast (3), Combo (4: grabs someone, Colossus popped when Combo'd in the middle of them). Torment Pulse/Fortitude tanky spirit.

**Rotation.** Burrow in > Sand Blast > Combo the carry in the middle > Colossus.

**Souls/economy.** Ability farm.

**Test must model.** Burrow travel/emerge, Combo requires target in range; Colossus window.

**Uncertain.** Mechanics from build notes only.


# Nurse Harrow
Builds: nurse

**Real play.** Spirit healer-gunner. Leech Therapy (1), Wretched Vapors (2), Healing Needles (3: bounce with Ricochet to more teammates; Surge imbued), Lurking Terrors (4). Spiritual Overflow procs when she heals teammates; Vampiric Burst popped on needles then swap back (each use adds ammo past mag).

**Rotation.** Needles on team while shooting, Vapors on enemies, Unstoppable before the ult.

**Souls/economy.** Gun farm.

**Test must model.** Allies required (needle heal, Overflow proc); ammo past mag via VB; heal scored on ally survival.


# Paige
Builds: paige (AoE), paige_support (support)

**Real play.** Dragon mage. Bookwyrm (1: dragon, 33 s, charges), Plot Armor (2: ally barrier 125+1.5xspirit, 5 s, +25% weapon damage + 15% spirit damage), Captivating Read (3: 30 m, 1.25 s delay, root 1 s), Rallying Charge (4: 210 s, 600 m, knights amplified by distance travelled). Support: Rescue Beam, Knockdown, Cursed Relic on their carry.

**Rotation.** Read on grouped, dragon, Plot Armor on carry; ult across the map at long distance.

**Souls/economy.** Normal farm.

**Test must model.** Ult damage is distance-dependent (350 u bot under-measures); ally for Plot Armor; 1.25 s delayed detonation (target must stay).


# Paradox
Builds: paradox (sniper), paradox_bomb (bomb)

**Real play.** Time sniper / bomber. Pulse Grenade (1), Time Wall (2), Kinetic Carbine (3: weapon), Paradoxical Swap (4). Sniper: Long Range/Sharpshooter/Express Shot headshots at 15 m+. Bomb: Arcane Surge dash-jump before the grenade, throw second grenade straight after the first to pile up stacks (Echo), Slowing Hex/Vortex Web.

**Rotation.** Bomb: dash-jump > grenade > grenade (Echo) > carbine; Swap to reposition.

**Souls/economy.** Gun farm.

**Test must model.** Distance > 15 m; Arcane Surge window; grenade stacks vs moving enemy.


# Pocket
Builds: pocket

**Real play.** Spirit skirmisher. Barrage (1), Flying Cloak (2), Enchanter's Satchel (3), Affliction (4). Restorative Shot, Cultist Sacrifice (biggest camp), Majestic Leap for escape/dive, Tankbuster, Ethereal Shift late.

**Rotation.** Barrage (user note: hit-based amp stacks) > Cloak to reposition > Affliction; Leap in/out.

**Souls/economy.** Cultist Sacrifice early (use on biggest camp monster).

**Test must model.** Barrage stacks on one vs several targets; Cultist needs NPC; leap/escape.

**Uncertain.** Ability numbers not in data.


# Rat King
Builds: ratking (tank), ratking_grenade (grenade)

**Real play.** Gun-scaling thrower. Scrap Grenade (1: 3 detonations, damage scales with weapon damage, can be meleed away), Rat Swarm (2: rats bite; enemies shake rats off by dashing), Royal Pestments (3: barrier 15% max HP, per-hit damage cap, 15% return fire), Rule Ratannia (4: 2 s banner charge, 20 m, 160 s). Tank: Cultist, Berserker, Siphon Bullets (max HP raises cape barrier). Grenade: Ballistic Enchantment on grenade, Echo.

**Rotation.** Cape on > grenade (Ballistic imbue: +20 weapon power per unique hero hit) > swarm > shoot; ult banner when team is together.

**Souls/economy.** Cultist Sacrifice early.

**Test must model.** Weapon damage items raise grenade damage; Ballistic stacks scale with 1/2/3 heroes; barrier absorbs discrete hits; Return Fire needs enemy attacks.


# Rem
Builds: rem

**Real play.** Backpack medic. Pillow Toss (1: hit reduces other cooldowns by 5 s), Tag Along (2: jump to ally, heal burst 15% missing + HoT, hop once per ally, Echo to re-jump), Lil Helpers (3), Naptime (4: 1.9 s gaze channel, sleep, damage on wake). Self-cast Divine Barrier while napping lands on the mate. User note: measure idle downtime.

**Rotation.** Pillow to cut cooldowns, Tag Along to a damaged ally, Healing Nova, ult from behind walls (pierces).

**Souls/economy.** Trophy Collector; helpers collect boxes.

**Test must model.** Ally with missing HP; idle seconds metric; pillow hit rate; Nova + Echo + 2 cycle.


# Seven
Builds: seven (ult), seven_gun (gun)

**Real play.** Lightning mage. Lightning Ball (1), Static Charge (2: 3.5 s delay then stun in 5 m, needs target to stay), Power Surge (3: bullets proc chain shock once per burst), Storm Cloud (4: 7 s channel, radius 10->30 m over 3.5 s, no damage out of LOS). Ult build: Arcane Surge dash-jump then 3 or ult, Unstoppable before ult (nobody cancels the storm), Infuser once they are in the storm. Gun build uses Power Surge + Tesla/Toxic. User note: Seven needs Unstoppable.

**Rotation.** Static Charge a target > Ball > Power Surge (Surge imbued) while shooting > ult in a spot with LOS.

**Souls/economy.** Cultist Sacrifice on both builds.

**Test must model.** Channel interruption (CC), LOS in sandbox map, enemies staying inside cloud, Power Surge duration 10 s uptime.


# Shiv
Builds: shiv (spirit), shiv_gun (gun)

**Real play.** Knife assassin. Serrated Knives (1: damage multiplies per knife in the target and by rage; user note), Slice and Dice (2), Bloodletting (3), Killing Blow (4: execute-style). Spirit: Decay, Leech, Torment Pulse, Reverb on dash. Gun: Restorative Shot, Berserker, Close Quarters.

**Rotation.** Build rage with knives/ability hits, dash in with 2, Killing Blow on low-HP target.

**Souls/economy.** Mystic Regeneration; farm with knives.

**Test must model.** Knife count and rage 0/mid/max; Killing Blow low-HP condition (needs enemy below threshold, not 90% floor).


# Silver
Builds: silver

**Real play.** Werewolf bruiser. Slam Fire (1), Boot Kick (2), Entangling Bola (3), Lycan Curse (4). Restorative Shot, Close Quarters, Melee Lifesteal, Hunter's Aura, Stalker, Express Shot, Berserker, Unstoppable, Frenzy late.

**Rotation.** Close in, bola to hold, melee+short-range gun, Lycan form on ult for burst and sustain.

**Souls/economy.** Melee/gun farm.

**Test must model.** Close range under 15 m, Berserker 0/mid/max, melee heavy/light.

**Uncertain.** Ability numbers from names only.


# Sinclair
Builds: sinclair (melee), sinclair_bolt (bolt)

**Real play.** Magician. Vexing Bolt (1), Spectral Assistant (2), Rabbit Hex (3: Cold Front just before so they cannot walk out), Audience Participation (4). Melee build: Shadow Weave invisible approach, hex then punch; Cultist. Bolt build: Vortex Web pull, hex, bolt; Trophy Collector with assists from range.

**Rotation.** Melee: stealth in > Cold Front > Hex > punches (Crushing Fists). Bolt: pull together, hex, bolt chain.

**Souls/economy.** Cultist on melee; Trophy on bolt.

**Test must model.** Stealth approach needs real map; hex area stay; bolts can be dodged.


# Solomon
Builds: solomon (AoE), solomon_support (support)

**Real play.** Chess-piece caster. Setup Bishop (1: persists indefinitely, move, diagonal squares), Kingside Knight (2: ally barrier, stamina; self-cast = king), Rook Battery (3: rooks reflect off walls, split), Develop Queen (4: crash, squares, leap, recall). Support: Healing Nova/Rite, Cursed Relic. Mystic Burst works because bishop impact (120) > 80 threshold. User note: early support must still do damage.

**Rotation.** Place bishop on lane, move it for damage, knight an ally, rooks along lanes, queen when grouped.

**Souls/economy.** Normal farm.

**Test must model.** Pieces need placement time and enemy walking into squares; ally for knight; cooldown refund 50% on bishop move.


# Venator
Builds: venator (melee), venator_grenade (grenade)

**Real play.** Exorcist. Consecrating Grenade (1: burn, anti-heal), Gutshot (2: shotgun blast, push, wall bonus and stun within 7 m of a wall, self pushback), Hex-Lined Snap Trap (3: 2 charges), Ira Domini (4: crossbow, 3 stakes, last executes < 8% HP, 15 s). Melee build uses Gutshot + melee; grenade build scales on weapon damage with Ballistic Enchantment.

**Rotation.** Gutshot against a wall > melee/Lifestrike; trap to hold; ult stakes on the carry.

**Souls/economy.** Cultist Sacrifice both builds.

**Test must model.** Wall behind target; execute needs enemy below 8% (not floor 90%); weapon damage scaling of abilities.


# Victor
Builds: victor (spirit), victor_gun (gun)

**Real play.** Zombie bruiser. Pain Battery (1: charges from ANY damage taken, needs stored damage worth 40% of max HP to fire, 7 bolts), Jumpstart (2: self-damage 15% current HP, then regen+speed), Aura of Suffering (3: 8 s, hurts self 70% of the dealt), Shocking Reanimation (4: on lethal damage, revive after 3 s, 240 s). Heals: Pain Battery, Jumpstart, Spiritual Overflow, Healing Tempo, Frenzy, Healing Booster. User finding: slot-empty block still healed ~107 hps.

**Rotation.** Absorb damage to fill battery, Jumpstart when low, Aura on in melee range, fire bolts when full; ult when dying.

**Souls/economy.** Normal farm; Torment Pulse.

**Test must model.** Needs incoming damage worth 40% max HP; net sustain after self damage; low-HP state; ult needs a lethal-hit op.


# Vindicta
Builds: vindicta (gun), vindicta_sniper (sniper)

**Real play.** Aerial sniper. Stake (1), Flight (2: flies), Crow Familiar (3), Assassinate (4: headshot ult). User note: Danny must reach her in the sky while she shoots. Gun build Long Range/Sharpshooter + Quicksilver/Mercurial + Burst; sniper build Tankbuster/Surge/Reverb on ult.

**Rotation.** Fly up, shoot from 15 m+, stake to pin, ult on a low-HP target; Counterspell for big abilities.

**Souls/economy.** Gun farm.

**Test must model.** Airborne shooting, headshots, range 15 m+, ult needs lasting line of sight.


# Violet
Builds: violet (hybrid), violet_spirit (spirit)

**Real play.** Painter mage. Living Ink (1: empower next 3 bullets, steerable; each hero hit cuts cooldowns 1.5 s, half for items), Flow State (2: refreshed by any other ability cast), Still Life (3: stare at a hero; completed sketch drops a pickup giving permanent stats), Abstract Landscape (4: ink dome, silence on leave). Gun hybrid: Mercurial on Living Ink, Recharging Rush.

**Rotation.** Empower bullets > hit heroes to cut cooldowns > Flow State chain > Still Life then ult.

**Souls/economy.** Sketch pickups need kills/completions.

**Test must model.** Sketch completion + pickup is a growth mechanic not testable with immortal bots.


# Viscous
Builds: viscous (support), viscous_damage (damage)

**Real play.** Goo brawler. Splatter (1: puddles slow, allies slide faster), The Cube (2: restorative, regen 40+0.3 spirit, 3 s), Puddle Punch (3: remote fist, scales with melee damage in damage build), Goo Ball (4: 11 s, 35% resist, stun on impact). Damage build: melee items on Puddle Punch + Goo Ball. Support: Rescue Beam, Rapid Recharge, Magic Carpet.

**Rotation.** Splatter to zone, Cube a hurt mate, punch, roll in with ball.

**Souls/economy.** Normal farm.

**Test must model.** Ally in cube; punch parry window; ball hit-stun needs target not dodging.


# Vyper
Builds: vyper (spirit), vyper_gun (gun)

**Real play.** Snake duelist. Screwjab Dagger (1), Lethal Venom (2), Slither (3: slide, Unstoppable first), Petrifying Bola (4). Spirit: Mercurial/Quicksilver, Close Quarters/Point Blank, Frenzy. Gun: Split Shot for clear, Intensifying Magazine, Ricochet, Silencer.

**Rotation.** Slide in (Unstoppable), bola, short-range burst; Split Shot on waves.

**Souls/economy.** Split Shot farm.

**Test must model.** Short range under 15 m; slide path; Unstoppable cannot be used while stunned.

**Uncertain.** Ability numbers from names only.


# Warden
Builds: warden

**Real play.** Gun controller. Alchemical Flask (1), Willpower (2), Binding Word (3: holds target, Vampiric Burst popped while they are stuck), Last Stand (4). Gun lifesteal build with Mercurial/Quicksilver on 1.

**Rotation.** Binding Word > Vampiric Burst + full mag > Flask; Spiritual Overflow for sustained.

**Souls/economy.** Gun farm.

**Test must model.** Held target for Binding duration; ammo/reload cycle.

**Uncertain.** Ability numbers from names only.


# Wraith
Builds: wraith

**Real play.** Gunner with cards. Card Trick (1: cards generated by bullet hits 4 each, crits 6, melee; a random suit effect), Project Mind (2: teleport 25 m, 0.75 s delay), Full Auto (3: 5 s, +20% fire rate, 2+0.045spirit magic dmg per bullet), Telekinesis (4: lift, slam 13 m, 150 s). Dispel valued (slowing hex stops teleport, user note). Build: Ricochet, lifesteal, Mercurial on Card Trick.

**Rotation.** Shoot to fill cards, throw cards, Full Auto in fights, TP to escape/dive, Telekinesis on the carry.

**Souls/economy.** Gun farm; Monster Rounds early.

**Test must model.** Card economy depends on accuracy/crits; TP vs hex; ricochet multi-target.


# Yamato
Builds: yamato (spirit), yamato_brawler (brawler)

**Real play.** Sword assassin. Power Slash (1: channel 1.4 s to full, partial on early release; strong bullet resist while charging), Flying Slash (2: grapple to enemy), Crimson Slash (3: heal on hit, fire rate slow 30%), Shadow Transformation (4: 5 s, abilities refreshed and 60% faster, immunity, heal and extend on kill). User note: shadow form with kill extends.

**Rotation.** Flying Slash in > Crimson > Power Slash full charge > ult; brawler adds melee and Restorative Shot.

**Souls/economy.** Melee/ability farm.

**Test must model.** Full-charge vs partial, kill extension (bots never die), melee vs spell mix.




---

# 5. KIERAN'S STATED REQUIREMENTS FROM MEMORY (testing project notes, verbatim)

- Wants the Deadlock build system expanded into a proper AI Council of specialist agents that research, theorycraft, create, test and improve builds and check each other's work before a build is finalised; keep the existing build website, import system, rules, preferences and progress.
- Wants a dedicated Sandbox Tester that tests in Deadlock's Sandbox (damage, healing, survivability, movement, cooldowns, item interactions) in realistic play (e.g. Victor vs three enemies, Wraith Ricochet with Leech vs Vampiric Burst), not single abilities on one dummy; results should feed back to challenge bad item choices.
- Expects to eventually have a mod that works inside Deadlock for the testing; won't have Claude test in-game while he's playing something else (e.g. Overwatch).
- Sandbox knowledge he gave: hitting enemies shows damage number pop-ups (usable as feedback), 1-2s cooldowns are fine (no true reset needed), item give commands exist, and bots can already be scripted in game (e.g. a bot flies up and casts an ability on a loop).
- Duo testing = duo builds: two heroes played together by a pair of players, each build tuned to the other's kit so the two have synergies. His example pairings (Dynamo + Ivy, Mo & Krill + Bebop, Danny + Haze, Bebop Hunter's Aura isolate) were off-the-top-of-his-head guesses, not the optimum; Claude should come up with its own pairs from the stats and kits. Duo builds must be separate builds, one per character in the pair, never replacing a hero's main build.
- Duo bar: combos must be reliable in real play, not fiddly (e.g. Vindicta + Haze sleep is a gimmick since any hit wakes the target; Dynamo + Victor aura is nice-to-have, not a real combo); each pair's builds should actually change because of the partner. Real duo combo = start from what a hero struggles with, pair a hero whose kit solves exactly that (e.g. Doorman needs to push people through his doors, so Venator/Graves trap and finish them; Mo & Krill can't ult into the whole enemy team safely, so Bebop's hook is the escape). Cross-shred pairs (Victor+Haze, Seven+Holliday) were rejected.
- Wants item questions tested vs 1, 2 and 5 enemies (e.g. Infuser vs Leech on Victor: burst vs consistent healing), plus damage testing and checks of proc thresholds (Tank Buster, Mystic Burst) and cooldown reality (Surge of Power); wants Reddit/TikTok scoured for unique interactions to test (e.g. Ricochet on the new hero's healing bullets).
- Wants a cost-efficiency sub-agent that checks value per soul and buy timing, and compares when other builds buy an item (e.g. Crushing Fist is good but shouldn't be the first item); swaps like Knockdown for Heroic Aura on support Bebop were rejected because they drop gun investment below 4.8k.
- Wants Council model switching kept (cheap models for simple work).
- -insecure didn't work for him; decided to go with Deadworks (private local server) for the sandbox, installed on his E drive.
- Sandbox tests must not be best case: test items at different price points/soul totals (e.g. Infuser may win early, Leech late), with realistic aim (not all headshots), against enemy bullet/spirit resists (so resist-shred items get judged), on full builds with same-tier swaps, for every hero not just Victor; support heroes (Viscous, Dynamo) judged on outcomes like whether an ally survives and ult range (e.g. Healing Nova vs Rescue Beam), not raw healing numbers.
- Sub-agents must decide what to test themselves (uncertain items, same-tier substitutes, how the hero makes souls, CC answers, realistic ~40-50% accuracy, multi-enemy and incoming-damage conditions, other healing sources in the build, optimal ability rotations) and keep auditing/testing every hero and build; he shouldn't have to say "go test X".
- Sandbox checkpoints: ~5k (lane), 10k, 18k, 24k, 30k souls and full build, buying the build strictly left to right in its listed order (not cherry-picked items); test heroes alphabetically; mix headshots and body shots at a realistic high-rank accuracy; model stacking/ramping mechanics and each hero's real positioning (melee range, lunges, actives used first).


## 5b. Build-writing rules the builds are held to (RULES_KIERAN.md; condensed from his stated rules)

# Kieran's stated build rules (oldest first; when two conflict, the LATER one wins)

- Build order must hit soul-investment spikes per colour (weapon/vitality/spirit) — 4.8k is the one that matters (weapon: 800→9%, 1.6k→12%, 2.4k→15%, 3.2k→18%, 4.8k→46%), so race to 4.8k in the build's main colour rather than collecting small steps across colours; then 6.4k/8k/16k; don't overshoot a threshold and don't spend randomly between them.
- Priority: damage spike first, then the 4.8k health spike, then keep investing damage, then more health. A few cheap greens early (Extra Health, Extra Regen, Grit, melee lifesteal) are fine if they fix a lane problem.
- Greens/off-colour items early are fine when they fix a hero's weakness (Enduring Speed on slow heroes, Grit on close-range heroes, High-Velocity on slow-bullet heroes).
- Early lane items can be sold later once the real build is online.
- Core categories are bought left-to-right; optional categories must say the problem they solve or when to buy them. Items like Enduring Speed are core or not in — never an optional.
- Don't buy fresh T2s late; late buys should be T3/T4 or upgrades of owned T1/T2s.
- Swaps must name what they replace. Don't take his item suggestions as gospel — check stats and say when an item is bad.
- Spike totals count souls actually spent in that colour: an upgrade over an owned component adds only the difference.
- Weapon-tree items that deal spirit damage (Mystic Shot) scale off spirit invest, so buy them right after the spirit spike.
- Never copy an item from another hero's build without checking it against THIS hero's kit numbers (threshold items need an ability that clears the threshold; charge items need a charge ability).
- Multiple imbue items can go on the same ability and all apply.
- Threshold items chain: Tankbuster's bonus helps reach Spirit Burn's 500, so order the enabler first.
- Before building, scan the FULL item list tier by tier against the kit, not just items seen in other builds.
- Soul income ~1k/min early: no 6400s until ~20 min; fill gaps with 800/1600/3200 items that give stats now. Snowball items (Glass Cannon, Boundless) go after you have the fire rate/health to use them.
- Dislikes Restorative Shot and Weakening Headshot (later: Restorative Shot is fine on shotgun heroes like Pocket, Shiv, Abrams, but bought FIRST since it's sold later).
- Mercurial Magnum counts as a gun item for his purposes.
- Health-spike timing depends on the kit: heroes with built-in sustain/escapes (Viscous, Calico, Vindicta, Geist, Mo & Krill, Shiv) can push the 4.8k health spike to ~14–16k; fighty heroes without kit sustain (Abrams) go green right after the first damage spike (~11–12k).
- No random untouched 800s: a cheap item must be upgraded later or be an optional that solves a lane problem; prefers Extra Regen over Healing Rite; skip regen items on heroes with built-in healing.
- Heroes with abysmal lanes (Billy, Drifter, Rem-types) can take several cheap lane-fixers first, then race the spike; items that heal but add damage (Lifestrike, Restorative Shot) count as damage items for this.
- Assume slot-lock early (3 flex slots locked until a Walker, can be 20 min): every T1/T2 must be upgraded later or have a named replacement it gets sold for.
- No long run of 6.4ks before ~30k: one, two or three back to back is fine; late (≥~30k) 4–5 in a row is fine; the problem is a long early/mid run (Boundless → Mercurial Magnum → Spirit Burn → Infuser). Core cost has no target.
- Counters/armors on every build (vs gun carry, flyer, spirit burst, on-hit comps).
- Sustain must actually exist in a build (Siphon alone isn't sustain).
- Wording: simple, player-facing, no commanding; "shred" means reducing bullet resist; no tick/proc jargon; say "your gun", never shotgun/beam/laser.
- Split Shot + Ricochet: each split applies its own Ricochet — used on gun Graves.
- Layout: Early/Lane · L-R, Mid · L-R, Late · L-R, then optional boxes; swap boxes named for what they replace; if Dispel Magic is in, Divine Barrier is listed as its rich upgrade.
- Upgrades are never written "X over Y"; don't list a stepping-stone armor if the answer is to wait for the T4; no AI phrasing.
- "I'm rich as fuck" holds tier-4 items only, and only pricier versions of something the build already does (Healbane→Spirit Burn, Counterspell→Divine Barrier, Cold Front→Arctic Blast, Refresher when the ult matters). "Slot locked" (no box description) holds only tiny-gain expensive upgrades (Transcendent Cooldown, Healing Tempo in most games, Juggernaut), never early items; Echo Shard usually in rich, not Slot locked. Counters box sits beside Late; every box one row (split long rows into two boxes); a lane "pick 1" box beside Early says clearly when to pick.
- Past 12 slots, the note says what to sell for it. Notes never mention bugs.
- Never agree with his item changes blindly — check real numbers and push back when he's wrong.
- Any farming build can take its damage spikes and rush Ricochet before the health spike, but greens must start right after; leaving health very late is bad.
- Core (Early/Mid/Late) fills all 12 slots by itself. Counters desc: "Dying after X? Buy what is killing you, cheapest first. Not dying? Skip. Sell Y for it." Premise (Oct 22): the Counters box is a menu, not a sequence: buy one only when you keep dying, pick by what is killing you (each item note names the threat), cheapest items first in the box; still dying, add the next; expensive ones (Spirit Resilience etc.) come once the next core spike is in; not dying, skip all of it.
- Notes never explain proc conditions/thresholds; the builder guarantees them via order and timing.
- Build names describe the playstyle; names that just restate the hero's theme are wrong.
- Don't overshoot a spike by a lot before the next spike (8k or 10.4k spirit before any health is wrong); a bit over is fine when cheap items that land it exactly don't suit the hero.
- If a build delays a spike, the extra items must fix the missing spike's problem. In-your-face heroes (Bebop, Abrams, Billy, Victor, Yamato) need the health spike before more big damage; mobile heroes (Vindicta, Holliday) can delay it.
- Items must match the playstyle: no Torment Pulse on squishy back-line heroes (it's for tanks in their face); no Escalating Resilience on burst/poke heroes; no melee items on flying heroes; kiting heroes with Sprint Boots also want Enduring Speed.
- Cultist Sacrifice is strong on heroes that struggle to farm (Pocket, Billy, often Venator), ~8 min. Pocket wants Majestic Leap or Warp Stone.
- Research: top ~10 public builds per hero that match the style (skip other styles); common items, spike order, trends. Don't call a build bad only because public builds differ when it serves the chosen style.
- Losing-lane box: survival items only (Extra Regen, Healing Rite, Grit), never damage items.
- Fortitude is not a default: fine mainly on roamers (Calico, Mo & Krill, Haze, Holliday, Bebop) or with a kit reason (Rat King's 3 barrier scales with max health; support Paige roams).
- Item reasons must be worked out from the kit.
- No item is a template default: Infuser is for heroes with lots of separate spirit hits (bad on one-arrow Grey Talon); Glass Cannon is bad on small-magazine heroes (Drifter).
- Builds already agreed / made in game are the base (his in-game Haze: Healing Booster core, Siphon Bullets to proc Healing Tempo).
- Older playstyle list (now = the MAIN build; variants cover other styles): Abrams tanky; Baba shotgun/gun not melee; Bebop gun (1v1); Billy tanky; Calico bursty; Celeste copy current top builds; Danny dive+ult (keep 4.8k gun spike HV→Opening Rounds→Sharpshooter from his in-game build); Drifter gun; Dynamo full support; Graves gun (Ricochet/Capacitor/Toxic/Split Shot); Grey Talon 1-arrow; Haze tanky healer; Holliday gun; Infernus gun; Ivy support (Headhunter + Healing Tempo); Kelvin damage-orientated; Geist gun/tank hybrid; Lash slam; McGinnis gun; Mina high burst; Mirage gun hybrid with mark damage; Paige speedy AoE; Paradox gun/carbine (long range sniper); Pocket burst ult; Rat King super tanky, damage from grenade only (weapon damage scales grenade, fire rate doesn't matter), Return Fire a must; Rem support (Heroic Aura, Trophy Collector); Seven ult build with early farm (Surge of Power/Arcane Surge on his 3 early, Escalating Exposure/Mystic Vulnerability or Cultist early, then Infuser/Unstoppable); Shiv = Spirit Shiv (dash); Sinclair melee/punch (Rabbit Backshots: Cultist, Melee Charge→Crushing Fists, situational Infuser/Unstoppable vs Seven, Warp Stone/Majestic Leap vs Lash/Dynamo); Solomon AoE damage; Doorman high burst DPS; Venator (main) per current build; Victor gun hybrid; Vindicta pure gun; Violet gun-hybrid (Mercurial Magnum straight, no Quicksilver; Surge of Power, Tankbuster, Spirit Burn good because her 1 resets actives); Viscous support (Echo Shard on cube mid/late, Rescue Beam, Trophy Collector, some 1/fist damage); Vyper more spirit invest; Warden gun; Wraith early farm then AoE gun (Leech, Ricochet, Tesla); Yamato grapple early (Stalker, Spirit Snatch, Recharging Rush, Healing Booster, Torment Pulse, Melee Lifesteal) into the 1-build late (Boundless, Spirit Burn, Mystic Reverb, Tankbuster).
- Trophy Collector is probably needed on pure-support builds (move speed + passive souls).
- Notes on imbue upgrades never say "keep it on X".
- Audit ability orders against top builds of the SAME style. Abrams: ult maxed much earlier than last; his 1 low priority.
- Rich-box items must only be pricier versions of something actually in the build.
- A build's style doesn't ban other items (pure gun Vindicta still needs Counterspell; gun Bebop still buys spirit items to scale the bomb).
- Ability orders copy what popular builds do; cheap high-value T1s get taken early across abilities (Paige: unlock 2 or 1, T1 Plot Armor, T1 on the 3, then the 1).
- Threshold items must proc when bought (Violet's 1 does ~64 when Mystic Burst bought, under 80). Threshold maths: boons +1.1 spirit/level, spirit invest bonus, items, imbues, tier scaling; never statue buffs. Witchmail late; Recharging Rush not early on slow-firing heroes; Tankbuster a bit later; Mystic Reverb minimum 100.
- Paige: HV → Opening Rounds early, Grit and Express Shot in lane, Trophy Collector; no Mystic Vulnerability; Tankbuster good; Knockdown not core.
- Make the calls yourself when data supports them. Use only data from after the latest patch that changed the hero/item.
- No token investments: commit with supporting items or drop it. Support lane items help the lane partner.
- When he points out a mistake, hunt that problem type across every build.
- Imbues go on the ability cast most often / that benefits most (Haze Surge of Power on the dagger).
- Swaps solve the same problem (colour can differ: Healbane → Spirit Burn), but walk the build to check spikes still land.
- Sell-later dead-end items (Restorative Shot) bought first or not at all; never the same item twice; no "Worth a try" boxes.
- Builds are for new players: triggers and notes concrete ("lots of gun carries on your team"); Heroic Aura only when the team actually has gun carries.
- Item notes only when needed: niche tips (Focus Lens before Danny's dive; Haze smoke works as a dispel, hence Rapid Recharge), item changes how you play (Bebop with Hunter's Aura hunts solo side-lane gun carries), situational conditions (Rat King Return Fire only vs a real gun hero), plus sell/swap info. Otherwise EMPTY.
- Separate named builds per viable style (usually two per hero) instead of pivot boxes; reorder-only answers go in one empty box whose description says the reorder.
- Haze tanky build: Burst Fire core; Surge of Power on the dagger as a swap for Burst Fire, never on Bullet Dance.
- Lifestrike procs on light melee too (longer cooldown) and on troopers; Abrams' Shoulder Charge pins into a wall for a guaranteed heavy, so earlier Lifestrike is a valid lost-lane plan on Abrams.
- Pick rates only count from builds of the same style.
- Build descriptions: short style label only ("Speedy AoE Paige", "Tanky Abrams"), blank if it's how the hero is always played; never spikes, item explanations, how-to or false claims. Gun Bebop named like "1v1 Beast Bebop". Box captions equally short.
- Drifter makes souls from picks (Bloodscent): Trophy Collector fits, Monster Rounds doesn't.
- Item relevance (Oct 22): every item must raise something this build's damage sources actually use (grenade/ability/weapon scaling); range, headshot, fire-rate or projectile items on ability-damage builds are wrong (e.g. Trash Lobber Rat King: Close Quarters to Point Blank, not Long Range/Sharpshooter/High-Velocity Rounds).


## 5c. Checklist (CHECKLIST.md)

# Final audit (round 14) — zero mistakes allowed

SP = /tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad. Run from SP. Touch ONLY files for your assigned build ids: read a14/in/<id>.js, write a14/out/<id>.js (always, even if unchanged) and a14/log/<id>.md. Never write anywhere else, never loop over other files.

Kieran (Oct 20, 00:26): "One final audit. If there is a single problem, I will be very, very mad." He has repeatedly found mistakes after we said builds were audited. Your job: find EVERY problem in your builds, as a new-player-facing expert who has checked every claim against the game files and same-style public builds. Take as long as needed. Decide and fix yourself; never leave a question.

## Sources of truth
- Game files (current, build 6795, Oct 17): items `python3 -I audit_D_q.py "<Item>"` (stats, components, desc), abilities `python3 -I ab.py <class>` (classes in audit/hero_<id>.txt or new/hero_hero_<codename>.txt; charges, cooldowns, scaling, tier upgrades), hero stats in gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata.
- Tools: `node a3/walk1.js <f>` (buy walk; must be FLAGS: none), `node a12/check.js <f>` (CHECK12: none, except colour-change swap lines you have walked and justify in the log), `node a7/sp.js <f> <orderString>` (spirit power and ability tiers at every buy).
- Same-style public builds only (post-patch, see a8/PATCH.md for dates): lockbuilds.com builds of that style, deadlocklabs, mobalytics filtered by the ability maxed first, tracklock pro matches only where the item set matches the style. A hero-wide pick rate is NOT evidence (Melee Charge 74% on Apollo comes from melee Apollo players).
- Kieran's rules: a14/RULES_KIERAN.md (his stated rules, oldest first) and a5/RULES.md. When rules conflict, the LATER one wins. The latest rules (Oct 19–20) override older ones:
  - separate builds per style replace pivots; his older "playstyle per hero" list now describes the MAIN build, the variants are the other styles;
  - item notes ONLY when needed (niche tip/interaction, item changes how you play, situational condition, what to sell once past 12 slots, what a swap replaces, Slot locked "Upgrade of X."); otherwise the note is EMPTY "";
  - build desc = short style label only ("Speedy AoE Paige", "Tanky Abrams"), or "" if it's how the hero is always played; never spikes, item explanations, how-to, or false claims;
  - names "Rizuhble's <style-describing name>"; the style must be obvious; ≤32 chars.

## Check EVERY one of these for EVERY item, note, box, desc, name and the ability order
A. Kit fit: the item's effect actually applies to how THIS build does damage/survives (read item desc + ability data). No range items on close-range heroes, no Duration Extender on infinite/channelled effects, no charge items on abilities without charges (AbilityCharges in ab.py), no proc items whose trigger the damage source can't meet (e.g. Lucky Shot needs bullets — Violet's Living Ink isn't bullets), no melee items on a flying hero, no token investments (one lone item of a damage type).
B. Same-style evidence: every item is used by builds of THIS style or justified by kit numbers you state in the log. Hero-wide rates don't count. Check the obvious better item for each job (Wraith anti-heal = Inhibitor, not Toxic Bullets; Drifter gets souls from picks → Trophy Collector, not Monster Rounds farming).
C. Imbues on the right ability: the one cast most often / whose number the item actually raises (Haze Surge of Power on dagger, never ult; Calico Compress on bombs). State cooldowns/scaling in the log.
D. Thresholds met at the buy point (a7/THRESH.md + ADDITIONS): Mystic Burst >80, Tankbuster >165, Spirit Burn 500 in 5s, Mystic Reverb 100, Recharging Rush 200 in 3.5s, Witchmail late, Tankbuster not rushed; use sp.js with this build's order.
E. Spikes: race to 4.8k in the main colour; health spike timing per hero (fighty heroes ~11–12k, sustain/escape heroes later), no big overshoot before the next spike; recount upgrades as the difference.
F. No long run (3+) of 6.4k buys before ~30k souls; no fresh T2s late; core fills 12 slots by itself; ≤8 items per box; every T1/T2 is upgraded later or has a named sell; sell-later dead-end items (Restorative Shot) bought first.
G. No item twice in one build. Rich box = T4 only and only pricier versions of things the build has. Slot locked = only tiny-gain expensive upgrades, notes "Upgrade of X.". Counters on every build with the required desc format ("Get after X if you need it. Ahead? Skip it until you feel like you're dying. Sell Y for it."), and the X and Y named must be in the build. If Dispel Magic is in, Divine Barrier is its rich upgrade. Losing-lane box = survival items only.
H. Swaps / situational boxes: concrete trigger a new player can check ("2+ of Shiv, Lash, Infernus, Vindicta"), each note says what it replaces, same job; walk the swapped build and confirm spikes. "Lost lane?" empty reorder boxes only if the reorder genuinely helps (verify mechanics: Lifestrike procs on light melee too and on troopers).
I. Every note and counter note is TRUE: verify each mechanic it claims in the game files (Dispel Magic doesn't answer damage like Geist's bomb; Unstoppable blocks stun/silence/sleep/root/disarm, not knockbacks; Spirit Resilience lists only heroes with real ticking spirit damage; spell Vyper). Hero names in counters must actually do what the note says. Empty every note that isn't one of the allowed kinds. No AI phrasing, no proc/threshold explanations, "your gun" not shotgun/beam/laser.
J. Ability order: copies what same-style popular builds actually do (state the source), and it must support the build's thresholds/imbues.
K. Name/desc/box captions per the latest rules above. Desc never explains. Box captions short.
L. Playstyle: the build is genuinely its named style (spirit Apollo has no melee items; support builds help the team; tank builds are tanky), and the variant pair is clearly different builds.

## Output
- a14/out/<id>.js: the corrected build (same JSON shape; keep id, hero, hk, abil, tg if present). Add one "Round 14:" line to `changes` summarising fixes.
- a14/log/<id>.md: for EVERY item in the build, one line: `<Item> (<box>): OK — <evidence: same-style source or kit number>` or `FIXED — <what and why>`. Then lines for: ability order (source), desc/name, each box caption, each note kept (why it's allowed + where verified), walk1/check.js/sp.js results. A reviewer will re-check your log line by line against the game files, so every claim must be verifiable.
- Final message: per build id, the list of fixes (or "no fixes") — nothing else.

## Specific known points
- Kelvin main build must be "tank damage-dealer Kelvin" (Kieran's words): damage but genuinely tanky; the existing one ends at only 11.2k health.
- Imbue items may keep a short "On <ability>." note.
- Existing builds' items may still rest on hero-wide rates from round 12: re-source every item from same-style builds.
- Builds with no published same-style ability order: find one (mobalytics filtered by max-first ability, lockbuilds builds that show orders); kit-based orders must be justified in the log.
- Rem's health 4.8k now lands at 17.6k after Echo Shard moved to 14.4k: check that's acceptable for a support (who must survive), fix if not.

## Standing checks added Oct 22 (every build, every agent; reviewer FAILS the build if any is missed)
M. Item relevance: each item raises a stat this build's damage sources actually scale with (abilities.vdata scaling), not just "gun" or "spirit" by colour.
N. Swap / "sell X for Y" / Counters boxes re-walked with the change applied: no colour that reached 4.8k in the base may drop below it.
O. Counters box: menu premise (buy only when dying, by killer, cheapest first); no T3 items in the rich box; Glass Cannon never on a health/tank build.
P. Buy timing: each item sits after the items that make it pay off (cost-efficiency agent output attached).

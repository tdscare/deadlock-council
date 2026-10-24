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
- UPDATE 2026-10-24: base reload time is in game data (m_reloadDuration, VERIFIED) so `cast reload 2.5` must be replaced by the hero value (Wraith 2.82); the 2.5 s was an assumption.
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

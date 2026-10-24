# verified_P6: Ivy carry/tether with a partner

Sources: `ab.py` on tengu classes and partner classes; abilities.vdata (citadel_ability_tengu_airlift @102?-ish block "citadel_ability_tengu_airlift", citadel_ability_tangotether @100522); citadel_heroes_english.txt lines 2567-2643; heroes.vdata hero_tengu (Ivy's internal name is TENGU). Items via audit_D_q.py.
Notation: 1 m = 39.37 u. "UNVERIFIABLE" = engine behaviour not in the data files; test given.

## 1. Ivy abilities (verified)

| Ability (class) | CD | Duration / range / cast | Numbers | Tier upgrades (T1/T2/T3) | Spirit / item scaling |
|---|---|---|---|---|---|
| Entangling Thorns (tengu_urn) | 32, charges 1, 5 between | dur 4, radius 6m, cast delay 0.2, tick 0.25 | DPS 40 (+0.55x ETechPower), slow 28% | T1 +1 charge; T2 +2m radius, +0.5 DPS scale; T3 enemies in thorns for TimeToEntangle 2s are immobilised +1.6s (EntangleDuration) | ETechPower (DPS), ETechRadius/Duration/Cooldown as item stats |
| Kudzu Connection (tangotether) | 37 | dur 12, cast range 16m (AbilityCastRange, ETechRange), TotalTetherTargets 1, instant cast (delay 0) | BonusFireRate 10 (+0.18x ETechPower); BulletLifestealPercent 15 (+0.15x healing-spirit scale); TetherSharedHealPct 35 (+0.85x ELevelUpBoons); MoveWhileShooting/Zoomed penalty reduction 100%; HealingPerGlub 20 (use not explained in files) | T1 MoveSpeedBonus +2m; T2 BonusFireRate +8, BulletLifesteal +8 (so 18% / 23% base); T3 AbilityDuration -13 and AbilityCooldown -37 = always active, no cooldown ("Ability is always active") | Fire rate and lifesteal scale with spirit; replicated heal scales with LEVEL (boons, 0.85 per boon), NOT spirit. Boons are ~+1.1 spirit/level per RULES, so heal share = 35 + 0.85 x boons (e.g. 10 boons = 43.5%) |
| Stone Form (tengu_stone_form) | 40 (T3 ups list -25 CD at one tier) | dur 3, lift 1.0s, radius 5.75m, cast 0.25 | Damage 75 (+0.6x), stun 0.75s, regen 6% max HP | T-ups: MaxHealthRegen +6, CD -25, StunDuration +0.75, Damage +1.5 scale (listed in file order) | ETechPower |
| Air Drop (tengu_airlift, ult) | 100; "reduced by 30% when used on allies" (CooldownReductionPctOnOthers 30) = 70 | AbilityDuration 21 (ETechDuration), cast range 22m (ETechRange), AbilityCastDelay 0.1, AllyCastDelay 0.1, fly speed base 393.7u (10m/s) to 866u (22m/s), fly height 80u-1720u (2m-43.7m), InterruptCooldown 3.5 | ExplodeDamage 115 (+0.7x ETechPower), radius 16m start to 20m (OnLandDamageRadiusStart/OnLandDamageRadius, ETechRadius); AllyOutgoingDamagePercent -20 (all damage multiplier, while lifted); AirDropOutgoingDamagePercent +20 for BuffDuration 8s for BOTH after fly ends | T1 barrier 300 (+0.7x ETechPower) to Ivy and ally on fly end; T2 slow 32% for 3s on enemies hit; T3 silence 3s on enemies hit, ExplodeDamage scale +1.5x (total 2.2x) and barrier scale +1.0x (total 1.7x) | ETechPower (explosion, barrier), ETechDuration (21s flight, 8s buff, 3s slow/silence), ETechRange (22m grab), ETechRadius (20m), ETechCooldown |

Ult cost per rules: 1/1/2/5; T1 barrier, T2 slow, T3 silence+damage.

## 2. Q3 first: does Air Drop carry enemies? REFUTED (allies only)

File text (abilities.vdata, citadel_ability_tengu_airlift):
- `m_nAbilityTargetTypes = "CITADEL_UNIT_TARGET_HERO_FRIENDLY"` with `CITADEL_ABILITY_BEHAVIOR_ALLOW_SELF_CAST`.
- `m_GrabModifier ... m_bApplyDragStateFlagsToEnemies = false`.
- Loc `citadel_ability_tengu_airlift_desc`: "Grab an ally and take flight with them. Drop your ally to cause an explosion... You and your ally gain increased Outgoing Damage when flying ends. Cooldown reduced by 30% when used on allies. Taking damage briefly disables using the ability. While lifted, your ally cannot attack and deals -20% damage."
- Quip: "Death from Above! Fly and drop an ally on enemies".
- Enemies are only hit by the drop explosion, slow (T2) and silence (T3). Ivy can also self-cast (ALLOW_SELF_CAST, "AirDropSelfCastDelay" label): flies solo and drops a bomb (m_HoldBombEffect).
- Correction to cards_g3: "partner with enemy-targeted effects can deal 80%" is wrong; the -20% is `MODIFIER_VALUE_ALL_DAMAGE_MULTIPLIER` (all outgoing damage including ability damage), not a targeting thing.

## 3. Q1: what works on the carried ally

Grab modifier on the ally (`modifier_airlift_grab`): `m_nEnabledStateMask = ABILITY_MOVEMENT | SHOOTING_DISABLED | MELEE_DISABLED`; `m_bBreakOnParentStunned = false`; `m_bDurationReducible = true` and `m_bDurationReducibleByCrowdControlDiminish = true`; `m_flAllyGrabCancelTime = 1.0`; pulls via EDragPull_SpringDamped, offset -120u below Ivy.
- Nothing in the mask is SILENCED, DISARMED-for-abilities, COMMAND_RESTRICTED or BUSY_WITH_ACTION. Ivy herself has SHOOTING/MELEE/DASH/JUMP/DUCK disabled (flying modifier) and her ult itself is the only thing marked BUSY.
- Ally's interrupt list only comes from each ability's own `m_bitsInterruptingStates` (STUNNED for Singularity, Hyper Beam, Telekinesis, Power Slash; IMMOBILIZED|STUNNED|ASLEEP for Quantum Entanglement, Project Mind, Flying Slash).
- So by FILE: ability casts are NOT blocked; bullets and melee ARE (hard flag). Anything fed by bullets is dead during carry. Whether the engine still lets a state-ABILITY_MOVEMENT unit start ability channels or movement abilities is UNVERIFIABLE-FROM-FILES.
- All outgoing damage -20% for the whole lift (ability damage too); post-drop +20% for 8s.

Per partner (cast list, ability data from ab.py):

| Partner | In-flight usable by flags | Dead by flag/design | Cannot-tell (test) |
|---|---|---|---|
| Dynamo | Kinetic Pulse (stomp 115+1.55x, cd 26, range 16m, cast 0.42), Rejuvenating Aurora (30+0.4x /s, 5s channel, 8m share) | Gun | Singularity (see below), Quantum Entanglement (ABILITY_MOVEMENT clash) |
| Seven | Lightning Ball (75+0.5x DPS, 4.25m, cd 26), Static Charge (15m range, 3.5s delay, stun 0.9, radius 5m), Storm Cloud (cd 205, 95+0.6x DPS, final radius 30m, 7s) | Power Surge (needs bullet procs: "Occurs once per burst shot") | Storm Cloud vs ABILITY_MOVEMENT (it has own flight control 1.5m, T3 +4m) |
| Bebop | Hyper Beam (cd 120, cast 1.0, channel 11, DPS 160+2.511x, length 70m, interrupt STUNNED only), Sticky Bomb (6m range, fuse 3.5) | Gun, melee | Hyper Beam while lifted; Hook/Uppercut can target allies (friendly hook, TossDurationFriendly 0.3) |
| Vindicta | Stake, Crow Familiar, Flight is redundant (already flies 13s, T2 +10s) | Gun | Assassinate (a scoped weapon shot; if it uses weapon fire, SHOOTING_DISABLED blocks it) |
| Wraith | Telekinesis (cd 150, cast 0.45, channel 1.25, lift 2s, range 10m, damage 100+1.0x), Project Mind (teleport 25m, cast 0.75) | Card Trick resource: CardResourcePerBulletHit 4, PerCrit 6, PerLightMelee 10 -> no bullets/melee means no new cards (cards already held can be thrown), Full Auto (bullets) | Project Mind vs ABILITY_MOVEMENT; Telekinesis range from the air |
| Yamato | Power Slash (cd 12, charge 1.4+0.2, 22m, full 145+1.85x), Crimson Slash (cd 16, 55+1.036x heal), Flying Slash (cast 26m, T3 can grapple allies) | Melee | Shadow Transformation (UNSTOPPABLE, STATUS_IMMUNE, invulnerable 1.5s channel: may break the grab); grapple while grabbed |

Singularity detail (Dynamo ult, citadel_ability_self_vacuum): cd 250, channel 2.75 (3.5 at T2), cast 0.2, `VacuumRadius 7m` (+2m T1 = 9m), DPS 75 (+0.28x ETechPower), T3 +6% max-health DPS, TickRate 0.25, `ChannelMoveSpeed 0`, TARGETING_SHAPE_SPHERE, SELF location, flags CHANNELLED | EXCLUSIVE_USE | CASTABLE_WHILE_BUSY, interrupt STUNNED only. The pull is a caster-centred aura (`modifier_vacuumaura`), so the pull sphere is centred on Dynamo. Arithmetic: sphere reaches only 7-9m; Ivy flies at 2-43.7m height. Pull only touches enemies if Dynamo is within 7m (9m) of them. At the drop moment the blast radius is 16-20m (bigger than the pull), so pulled enemies are already inside. Damage under carry 75 x 0.8 = 60 + spirit. Cooldown mismatch 250 vs 70 (ally Air Drop). Q1 answer for "Singularity pull radius from the air": cast is not blocked by any flag; whether it can start/hold the channel while being dragged, and the 3D pull reach, is UNVERIFIABLE (see S1).

## 4. Q2: what Kudzu Connection shares

- Text (loc): "Connect with a nearby ally to gain bonuses, replicated healing, and ignore the move speed penalty while shooting. Receive 50% of Bonuses with no connection. Connection requires line of sight." Quip: "Empower yourself and a nearby ally."
- Bonuses carried by `citadel_modifier_tangotether_tether_receiver` (state COOP_TETHER_ACTIVE): BonusFireRate, BulletLifestealPercent, MoveSpeedBonus, move-while-shooting and move-while-zoomed penalty reduction 100%. So: fire rate, bullet lifesteal, top speed, no shooting slow. "Replicated healing" = TetherSharedHealPct (35% + 0.85 per boon).
- Not in the files: which heal sources replicate (bullet lifesteal, Headhunter heal, item active heals, Healing Nova), and which direction (Ivy's heals to ally only, or both ways). The build text says "Headhunter... your tether passes the heal on" and "Healing Tempo: every heal you pass down the tether gives your carry fire rate and speed". Facts from items: Healing Tempo (T4): "Applying to yourself or an ally grants the target ... Does not apply on innate Regen or passive Bullet/Spirit Lifesteals"; BonusFireRate 35, BonusMoveSpeed 1.25m, BuffDuration 7, AbilityCooldown 1. Headhunter: HealPercentPerHeadshot 4 (+0.06x), HeadShotBonusDamage 75 (+4x boons), AbilityCooldown 8. Whether tether-replicated heal counts as "applying to an ally" for Tempo: UNVERIFIABLE.
- Geometry: cast range 16m, lock-on state COOP_TETHER_LOCKED_TARGET, MinConnectTime 2.0s, disconnect buffer 100u (2.5m), TargetAwayDistance 250u (6.3m), CandidateCloser 400u (10m). With no connection: 50% bonuses.
- Duration 12 / cd 37 base; T3 removes both (always active). Slows do not break connection per build note ("Enduring Speed"), not from file.
- Item multipliers: Mystic Expansion/Greater Expansion (ETechRange) on 16m; Superior Duration on 12s (becomes irrelevant at T3 always-on); Cooldown items on 37s (irrelevant at T3).

## 5. Candidate pair arithmetic

Ivy flight window 21s; buff after drop 8s; Ivy ult cd 70 (ally cast).

| Pair | Setup window | Payoff need | Result |
|---|---|---|---|
| Ivy+Bebop beam | 21s carry | cast 1.0 + channel 11 = 12s; spare 9s. Starting the cast 1.0s before the drop puts channel second 1-9 inside the +20% buff (8s x1.2 + 3s x1.0) vs carried -20% | Survives on arithmetic if beam can be channelled while lifted (S2). Beam DPS 160+2.511x: x0.8 under carry, x1.2 after |
| Ivy+Seven | 21s | Storm Cloud 7s (+7 T2) channel, ExpandTime 3.5s, radius 10m to 30m: cloud outranges the 16-20m drop blast. Static Charge delay 3.5s lands inside window (apply before the drop; stun 0.9, radius 5m, 7m T1) | Survives (cloud covers drop zone; Static timing fits with 17.5s spare). Power Surge is dead while carried |
| Ivy+Dynamo | 21s | Singularity 2.75s channel + 0.2 cast (3.5s T2), cd 250 vs 70: 3.6x mismatch; pull sphere 7-9m only | Marginal: needs the in-air cast test; ult mismatch means Singularity usable once per ~3.5 Air Drops. Quantum (cd 20, brings allies within AllyDistance 13m) is Dynamo's movement: unknown clash |
| Ivy+Vindicta | 21s | Assassinate full charge 1.0s, 2 charges 2.5s apart, range 1000m, cd 55; ally-carry makes Flight redundant | Arithmetic fine (two shots in 3.5s inside 21s), x0.8 under carry; dies if SHOOTING_DISABLED blocks scoped shot (S4). Flight redundancy kills the pair's flight synergy |
| Ivy+Wraith | 21s | Telekinesis cast 0.45 + channel 1.25 = 1.7s, lift 2s; drop silence 3s (T3) / slow 3s (T2) overlap; Card/Full Auto need bullets | Thin: Wraith loses gun, cards, Full Auto for 21s. Only Telekinesis and Project Mind remain |
| Ivy+Yamato | 21s | Power Slash 1.6s per cast, cd 12 (8 at T2): 2 slashes (3 at cd 8) inside 21s at x0.8; Flying Slash T3 can hook allies (range 41m T3) | Survives on arithmetic; Shadow Transformation cd 150 unlikely to line up with 70s ult cd |

## 6. Sandbox scenarios (UNVERIFIABLE-FROM-FILES)

- S1 Singularity in flight: Dynamo carried at (a) 2m, (b) 6m, (c) 15m altitude over 3 bots; cast Singularity; record: starts channel? holds 2.75s? pulls bots? DPS shown (expected x0.8)?
- S2 Hyper Beam in flight: Bebop carried; cast beam at flight t=0 and t=20; does the beam channel hold while dragged, does it end at the drop, damage per tick before (x0.8) and after (x1.2).
- S3 Quantum Entanglement / Project Mind / Flying Slash while grabbed: does the ability fire, does it break the grab (m_flAllyGrabCancelTime 1.0 suspect).
- S4 Assassinate and card throws while grabbed: scoped shot allowed? Wraith held cards throwable?
- S5 Kudzu: heal replication direction and sources (Headhunter, Healing Nova, Mending items); does a replicated heal trigger Healing Tempo on the partner; measure with 0/10/20 boons to confirm 35+0.85/boon.
- S6 Does Shadow Transformation or any UNSTOPPABLE/STATUS_IMMUNE on the ally end the carry.
- S7 Is the -20% applied to ability damage (expected yes: ALL_DAMAGE_MULTIPLIER) and does it persist after the drop until +20% starts.

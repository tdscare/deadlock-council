# P4 Clump then AoE payoff: verified numbers and interaction answers

Sources: `ab.py <class>` on abilities.vdata, new/hero_hero_punkgoat.txt, new/hero_hero_lash.txt, audit/hero_{dynamo,seven,infernus,paige,mina}.txt, new/hero_hero_{synth,astro}.txt, heroes.vdata (Billy EMaxMoveSpeed 7.0 m/s; used as the generic base speed, other heroes not checked).
Upgrade bonuses are ADDITIVE (e.g. Seven ShockRadius 5m + 7m = 12m). T1/T2/T3 assigned from the *_t1/t2/t3_desc keys; where a tier desc is missing, the order of the `ups` list is used (marked [order]).
All times are seconds from pressing the ability (t=0) unless stated. "Hold" = time enemies cannot just walk away.

## 1. Clump (setup) abilities

| Ability (class) | CD base / T-values | Cast / channel | Hold mechanic (verified) | Radius / range | Damage | Tier ups |
|---|---|---|---|---|---|---|
| Billy Chain Gang (ability_punkgoat_tether) | AbilityCooldown 175; T2 -40 = 135 | AbilityPostCastDuration 0.2 | Tether AbilityDuration 2.8, then yank: PullDuration 0.8, PullDistance 4m, PullTrackCasterDuration 0.5. During tether: no movement abilities, MoveSpeedSlowMaxPct 35 / MinPct 25. Rope breaks after RopeSnapNoLOSDuration 0.5s without LOS. NOT a stun: enemies can still shoot/cast. Pull arrives about t=3.6 (2.8+0.8). | AbilityCastRange 12m (T3 +5 = 17m), RopeLength 2.0m, RopeSoftEdgeLength 4.5m, RopeSnapDistance 45m | Damage 120 (+0.7 spirit) on yank; DPS 45 (+0.9 spirit) tick 0.25 | T1 +40% BulletResist and TechResist (Billy, while waiting-to-pull); T2 CD -40; T3 +5m range, UnstoppablePerHero 1.3s (Billy gets 1.3s unstoppable per hero pulled) |
| Dynamo Singularity (citadel_ability_self_vacuum) | AbilityCooldown 250, no CD upgrade | AbilityCastDelay 0.2, AbilityChannelTime 2.75 (ends about t=2.95) | modifier_vacuumaura_target: label "stunned", AG2 action "lifted", flag MODIFIER_STATE_MOD_NO_CLEANSE (cannot be cleansed). Pulls enemies in radius. Target types: heroes AND minions AND creeps. Dynamo is CHANNELLED + EXCLUSIVE_USE. | VacuumRadius 7m (T1 +2 = 9m) | DPS 75 (+0.28 spirit), TickRate 0.25 = 206 over 2.75s | T1 +2m radius; T2 +0.75s channel = 3.5s (ends about t=3.7); T3 DPSPercentHealth 6 (per-second % health; the unit is not shown in file) [order] |
| Lash Death Slam (citadel_ability_lash_ultimate) | AbilityCooldown 170; T2 -35 = 135 [order] | AbilityCastDelay 0.3, AbilityChannelTime 2.3 (lift starts about t=2.6). Lock needs TimeToGainLockonStack 0.7s in cone (LockonConeAngle 40), lose lock after 2s out of cone (LosingLockGraceTime 0.4). Press again to throw early. | After latch: UpBoostSpeed 400, LiftHeight 6m, BoostTime 1.0, HangTime 0.6 = 1.6s airborne and stunned (modifier "modifier_state_stunned", m_bDurationReducible=false), then SlamSpeed 1600 into ground. Slam leaves SlowPercent 40 for SlowDuration 4. | AbilityCastRange 20m (T3 +6 = 26m), ImpactRadius 6m, AbilityUnitTargetLimit 6, ThrowDistance 14m (+0.14 spirit; T1 +12 = 26m), ThrowStraightDuration 1.5 | ImpactDamage 105 (+0.975 spirit) | T1 ThrowDistance +12m [order]; T2 CD -35 [order]; T3 StunDuration 1.2 on enemies in radius + range +6m |
| Lash Ground Strike (citadel_ability_lash_down_strike) | 18; T1 -10 = 8 | CastDelay 0.15 | T2 knockup (StompBounceHeight 400, TossDuration 1) + slow 40% 3s | Radius 10m | StompDamage 60 (+0.79 spirit) + 5.5/m primary (25m); T3 +120% per meter | |
| Dynamo Kinetic Pulse (citadel_ability_stomp) | 26, charges 1 (T1 +1), 5s between charges | CastDelay 0.42 | T2 -15% bullet resist, 24% slow, 4s. Toss values (TossDuration 1, ClimbHeight 1m) exist: lift effect not confirmed. | StompRange 16m (T3 +4 = 20m), StompWidth 5.5m | 115 (+1.55 spirit); T3 +135 | |

Billy and Dynamo are not stuns in the same sense: Billy = slow + movement-ability lock, then pull. Dynamo and Lash = true stun-lift.

## 2. Partner payoffs (all verified numbers)

| Partner ability | CD | Delay | Radius | Damage / effect | Spirit scaling | Tier ups |
|---|---|---|---|---|---|---|
| Seven Static Charge (citadel_ability_static_charge) | 42; T1 -20 = 22 [order] | CastDelay 0.2 + ShockDelay 3.5 = detonates t_c+3.7. Charge is a modifier on the TARGET hero (cast range 15m), blast centred on the carrier at detonation. | ShockRadius 5m (T2 +7 = 12m) | StunDuration 0.9 (T3 +0.9 = 1.8) + Damage 35 (T3 +160 = 195) | Damage 0.792 | T1 CD; T2 radius + cast range +5m (20m); T3 stun + damage [order] |
| Seven Storm Cloud (citadel_ability_storm_cloud) | 205 | channel 7s (T2 +7 = 14s) | InitialRadius 10m (T2 +5), grows over ExpandTime 3.5s to Radius 30m (T2 +10) | DPS 95 (T3 +65 = 160) tick 0.3; needs LOS | 0.6 | Lightning strike: LightningStrikeRadius 7m, delay 0.25, damage 75, KNOCKBACK 500 (pushes enemies OUT of a clump) |
| Pocket Barrage (synth_barrage) | 32; T2 -16 = 16 | CastDelay 0.3 + channel 2.0 = 2.3 | Radius 4.5m per impact (T3 +3 = 7.5m) | 4 projectiles x 32 = 128 (T1 +16 each = 192); slow 24% 1.5s; AmpPercentPerStack 6 (T3 +4) for 15s on hero hit | 0.465 per projectile | T1 dmg; T2 CD; T3 amp + radius |
| Pocket Affliction (synth_affliction) | 170; T1 -35 = 135 | CastDelay 0.6; debuff applied to enemies in radius at cast, lasts DebuffDuration 10 (T2 +3 = 13s) | Radius 9m (T2 +4 = 13m) | DPS 32 tick 0.5 = 320 (T3 DPS 45 = 585 over 13s; heal block); non-lethal, no item procs, CanBePurged=1 | 0.21 (T3 +0.1 = 0.31) | T1 CD; T2 duration + radius; T3 DPS + heal block |
| Infernus Concussive Combustion (ability_fire_bomb) | 190; T2 -65 = 125 | ExplodeDelay 3.25, cannot be interrupted once cast, centred on Infernus | Radius 12m (T3 +10 = 22m) | Damage 125 (T1 +100 = 225); StunDuration 1.25 (T3 +0.9 = 2.15) | listed as 0.975 | T1 dmg; T2 CD + 100% lifesteal; T3 stun + radius |
| Infernus Napalm (ability_incendiary_projectile) | 25, charges 1 (T1 +1), 6s between | CastDelay 0.1 | cast range 20m | 40 (+0.6 spirit); slow 28% 4s; IncomingDamagePercentFromCaster 16 for 8s (T3 +17 = 33% and -33% healing) | 0.6 | |
| Paige Bookwyrm (ability_bookworm_dragonfire) | 33; T1 -12 = 21 | CastDelay 0.1 + StartupDelay 0.3; dragon flies DragonTravelRange 20m (T3 +12) at DragonRangePerSecond 500 | trail Radius 4m (T2 +1); DragonSearchRadius 8.5m; DragonConeRange 5m | Damage 60 (T3 +100); trail DPS 30 tick 0.3, GroundFlameDuration 3s (T2 +2 = 5s), DebuffDuration 1.5 (T3 DPS +30) | dmg 1.3, DPS 0.3 | T2 +1 charge (7s between) |
| Paige Captivating Read (ability_bookworm_aoemagic) | 30; T1 -14 | CastDelay 0.15, DetonationDelay 1.25, ImmobilizeDuration 1.0 (T2 +1 = 2.0) | Radius 7.5m (T3 +2), CastRange 30m | Damage 90 (+1.3 spirit); slow 36%; T3 -18% spirit resist 6s | 1.3 | |
| Holliday Powder Keg (ability_explosive_barrel) | 28; T1 -10 = 18; charges 2 (T2 +1 = 3), 7.5s between (T3 -5 = 2.5s) | CastDelay 0.125, TossDuration 0.4, ArmTime 0.1; the file has NO explode-delay value; shot or melee detonates early | Radius 6m | ImpactDamage 40 (T3 +40 = 80); burn 13.3/s for 3s = 40 (T3 26.7/s = 80), stacks per barrel; BarrelLifetime 8 | impact 0.525 (T3 +0.25), DPS 0.175 (T3 +0.083) | |
| Mina Rake (ability_vampirebat_steallife) | 16 | CastDelay 0.1 | 10m cone, TargetingConeAngle 60, limit 6 targets | 60 (+1.0x EStatsCount); T1 +60; MissingHealthDamagePercentage 6 | | |
| Mina Nox Nostra (ability_vampirebat_batswarm) | 150; T1 -45 = 105 | CastDelay 0.5; BatCount 75 at BatPerSecond 30 = 2.5s release, ends about t=3.0 | CastRange 40m, TargetingConeAngle 20, UnitTargetLimit 12, MaxBatTargets 2 | Damage 4.6 per bat (+0.094 spirit); Love Bites procs on heroes add BonusBatsPerProc 2 (max +50); T3 adds CurrentHealthPercent | 0.094 | |
| Mina Love Bites (ability_vampirebat_lovebites) | PerTargetCooldown 10 (T3 -5) | BuildUpDuration 5; abilities add buildup (BuildUpPerBat 20, per dagger 30) | single target | MagicDamagePerBullet 4 (+0.09); burst BonusDamage 45 (+1.85 spirit) | 1.85 | |

## 3. Window arithmetic per pair (control window vs payoff)

Hold windows (from setup press, base / with listed upgrade):
- Billy: pull complete t=3.6 (tether 2.8 + pull 0.8). Enemies are slowed 25-35% and cannot dash/teleport, but are not stunned.
- Dynamo Singularity: stunned-lifted until t=2.95 (T2 3.7).
- Lash Death Slam: stunned and airborne t=2.6 to 4.2 (2.3 latch + 0.3 cast + 1.6 lift), plus slam travel, plus 40% slow 4s, plus T3 stun 1.2 on landing.

| Pair | Payoff timing | Arithmetic | Result |
|---|---|---|---|
| Billy + Seven Static Charge | det = t_c+3.7 | Det lands inside tether+pull (0..3.6) for t_c up to -0.1. Aligned best: cast charge at t_c=-0.1..0 (sync with Billy). Carrier is yanked, so blast centred on its landing spot; others pulled around Billy within PullDistance 4m, ShockRadius 5m (12m T2). Stun 0.9 starts right after pull ends (+0.1s spare): total hold 3.6+0.9 = 4.5 | SURVIVES (timing 0.1 spare, one-way sensitive) |
| Billy + Seven Storm Cloud | channel 7s | No clump needed (InitialRadius 10m). Billy hold covers 3.6 of 7s (51%). Lightning strike knocks enemies away. | Weak (no clump synergy) |
| Billy + Pocket Affliction | applies at 0.6 | Cast any time 0..3.0 with enemies within 9m of Pocket; Pocket must stand within 9m of enemies' landing zone near Billy | SURVIVES (loose timing) |
| Billy + Pocket Barrage | 2.3 channel | Fits tether 2.8 with 0.5 spare. Impact positions are not in file | UNVERIFIABLE (impact placement) |
| Billy + Infernus Combustion | explosion t_b+3.25 | Within hold if t_b between -3.25 and +0.35. Radius 12m (22m T3) around Infernus covers pulled group if Infernus within 8m of Billy. Stun 1.25 starts at hold end (explosion at 3.6 gives total 4.85). Without the chain, 7 m/s slowed 35% = 4.55 m/s x 3.25 = 14.8m flight vs 12m radius; tether RopeLength 2m might leash them (unverified) | SURVIVES (needs the leash test) |
| Billy + Paige Bookwyrm | trail 3s | Trail DPS 30 for 3s; slowed 25-35% enemies stay; tether covers 3.6. Path is a straight line 20m | UNVERIFIABLE (dragon orientation) |
| Billy + Holliday Keg | unknown delay | Barrel radius 6m vs pulled cluster within 4m of Billy fits. Lifetime 8, detonation by Billy's melee is possible (BarrelLightMeleeForceForward 1400) | UNVERIFIABLE (fuse delay) |
| Billy + Mina | Rake cone 60 / Nox 3.0s | Rake hits 6 targets within 10m: pulled group fits. Nox release 2.5s + 0.5 cast = 3.0 < 3.6 | SURVIVES (arithmetic) |
| Dynamo + Seven Static Charge | det t_c+3.7 vs end 2.95 | To land inside the hold: t_c <= s-0.75 (T2 Sing: t_c <= s). If det exactly at drop (t_c = s-0.75): hold 2.95 + stun 0.9 = 3.85 (T3 4.75). Charged target is pulled to the centre, others inside 7m radius: ShockRadius 5m may miss the 7m rim (T2 12m covers) | SURVIVES only with T1 Seven +2 level; base radius 5 < 7 (partial) |
| Dynamo + Seven Storm Cloud | 7s | No clump need; Sing covers 2.95 of 7s | Weak |
| Dynamo + Pocket Affliction | 0.6 cast | Pocket within 2m of Dynamo (9m minus 7m) to catch rim; cast any time during 2.95 | SURVIVES |
| Dynamo + Pocket Barrage | 2.3 | Fits 2.95 (0.65 spare). Impact radius 4.5m vs 7m clump: not all | UNVERIFIABLE (placement) |
| Dynamo + Infernus Combustion | 3.25 | Explosion inside hold only if t_b <= s-0.3 (T2 Sing: t_b <= s+0.45). At the edge: control 2.95 + 1.25 stun = 4.2 (T3 stun 2.15: 5.1). Radius 12m covers whole 7m clump | SURVIVES (Infernus must press first by 0.3s) |
| Dynamo + Paige Bookwyrm | 0.4 + flight | 7m clump; dragon trail 4m is a line; ground aura vs lifted enemies unverified | UNVERIFIABLE |
| Dynamo + Holliday Keg | unknown delay | Barrel 6m vs clump toward centre fits; fuse unknown | UNVERIFIABLE |
| Dynamo + Mina | Rake / Nox | Rake cone 10m; Nox release ends at 3.0 vs Sing 2.95 (0.05 short) | Marginal |
| Lash + Seven Static Charge | det t_c+3.7 vs 2.6..4.2 | t_c from -1.1 to +0.5 relative to Lash press (1.6s window). Det at 4.2 extends to 5.1; Lash T3 stun 1.2 overlaps (max, not sum) | SURVIVES; redundant with Lash T3 stun |
| Lash + Pocket Barrage | 2.3 | Lift is 1.6 < 2.3: can't cover whole channel; lifted victims at 6m vs 4.5m impact sphere; then they land in 6m zone with 40% slow 4s. Better after the slam | Weak/UNVERIFIABLE |
| Lash + Pocket Affliction | 0.6 | Slam clump + 40% slow 4s: apply at land. Affliction 9m radius covers 6m ImpactRadius | SURVIVES |
| Lash + Infernus Combustion | 3.25 | Explosion inside lift if t_b in Lash press -0.65..+0.95 (1.6s window). Stun 1.25 on landing overlaps Lash T3 stun 1.2 | SURVIVES; stun overlaps |
| Lash + Paige/Holliday/Mina | | Lifted 6m: ground-based trail/barrel radius 6m likely miss; Rake cone 10m ok | UNVERIFIABLE |

## 4. Interaction questions

Q1. How long are enemies kept inside the payoff?
- Billy: 3.6s tether+pull, slow only (VERIFIED from AbilityDuration 2.8, PullDuration 0.8). Exact enemy position during tether: UNVERIFIABLE (RopeLength 2m / SoftEdge 4.5m may be a leash).
- Dynamo: 2.75s (3.5 T2) stun-lift, NO_CLEANSE (VERIFIED).
- Lash: 1.6s airborne stun + landing slow 4s + T3 1.2s stun (VERIFIED), after a 2.6s latch where enemies are not controlled.

Q2. Is pulled/slammed position inside payoff radius?
- Billy: pulled toward Billy, PullDistance 4m: inside Seven 5m / Pocket 4.5m / Holliday 6m / Infernus 12m if the partner is within a few metres of Billy. Final cluster size UNVERIFIABLE.
- Dynamo: singularity radius 7m (9m T1). Pull to centre vs rim: UNVERIFIABLE; Seven base 5m and Pocket Barrage 4.5m may miss the 7m rim.
- Lash: thrown ThrowDistance 14m (26m T1) from Lash then slammed; landing zone ImpactRadius 6m; whether all 6 victims land in one point UNVERIFIABLE. Distance away may exceed partner range.

Q3. Do partner payoffs apply to enemies in the air/held?
- VERIFIED absent: no INVULNERABLE / UNTARGETABLE / hidden state in the data of Singularity, Lash lift or Chain Gang modifiers. Singularity states only MOD_NO_CLEANSE; Lash enemy debuff only ABILITY_MOVEMENT_DEBUFF (modifier classes are code, so engine states are possible).
- UNVERIFIABLE: geometry. Lash lifts 6m (LiftHeight); radius checks of Barrage (4.5m), Keg (6m), ground aura of Bookwyrm (modifier_dragonfire_ground_aura) may fail at height.

## 5. Sandbox tests to settle UNVERIFIABLE items
1. Billy Chain Gang, enemy bots set to run away: measure distance from Billy at t=2.8 (leash?) and cluster radius at t=3.6.
2. Dynamo Singularity: measure bot spread (centre vs rim) at t=2.9, and height of lifted bots.
3. Lash Death Slam on 3 bots in a 90 degree spread: measure landing spread vs 6m ImpactRadius and distance from Lash.
4. Seven charge cast at -0.1/0/+0.5 relative to Billy, and at t_c = s-0.75 relative to Dynamo, count bots stunned.
5. Pocket Barrage while bots are held: where do 4 projectiles land, who gets stacks (enemy or Pocket).
6. Holliday keg fuse time and whether it hits lifted (Lash) bots.
7. Paige dragon vs lifted bot; trail ground aura on airborne.
8. Infernus bomb during Chain Gang with bots running: how many escape the 12m.

## Summary of survivors
- Survive on arithmetic: Billy+Seven (0.1s margin), Billy+Infernus (needs leash test), Billy+Pocket Affliction, Billy+Mina, Dynamo+Infernus (Infernus presses 0.3s first), Dynamo+Pocket Affliction, Lash+Seven, Lash+Infernus, Lash+Pocket Affliction.
- Die/weak: Storm Cloud with any (no clump need and knockback), Lash+Barrage (1.6s lift < 2.3s), Dynamo+Seven at base radius (5m < 7m).
- Unverifiable: Paige and Holliday with all three (fuse, aura height, orientation).

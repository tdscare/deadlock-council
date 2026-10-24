# P1 verified: long-range payoff (Vindicta / Grey Talon) + hard hold

Source: `python3 -I ab.py <class>` on abilities.vdata, heroes.vdata slot map, a7/levels.json, `node a7/sp.js a7/new_{vindicta,greytalon}.js` (current builds, real SP per buy). Tier = order of the `ups` list (T1,T2,T3), cross-checked with the _tN_desc text. Stage-A card errors are listed at the end.

## 1. Payoffs (the snipers)

| Ability (class) | CD | Timing | Damage | Tiers | Spirit scaling |
|---|---|---|---|---|---|
| Vindicta Assassinate (citadel_ability_hornet_snipe) | 55; 2 charges, 2.5 between (AbilityCooldownBetweenCharge) | No AbilityCastDelay. TimeToFullCharge 1.0s scoped; MinChargeDamagePercent 50; MoveSpeed 4m scoped; Range 1000; ShotRadius 4.0 | Damage 90; <50% HP: +LowHealthEnemyDamageBonus 90; HeadshotBonus +20 | T1 CD -15 (40); T2 low-HP bonus +80 (170); T3 WeaponDamageBonusPerKill +4 | 90 +0.93xSP; bonus +2.3xSP |
| Grey Talon Charged Shot (ability_charged_shot) | 17; 1 charge, 4 between (AbilityCooldownBetweenCharge) | AbilityCastDelay 0.5, then channel until release (9999), ChannelMoveSpeed 1.5m; **charge-to-full time is NOT in the files** | Damage 80, pierces, hit-once | T1 +1 charge; T2 Damage +54 (134); T3 between-charge -3 (1s) and scale +1.0 | 80 +1.0xSP (T3: 2.0x) |
| GT Guided Owl (ability_guided_arrow) | 125 | CastDelay 1.5, channel up to 20, flight time not in file; ExplosionRadius 12m; StunDuration 0.75 | Damage 230 | T1 +85; T2 CD -40 (85); T3 execute <22% HP | 230 +0.937xSP; +8 SP per hero kill |
| GT Spirit Snare (ability_immobilize_trap) | 34 | ArmTime 2.0, TripTime 0.5, Lifetime 22, trigger Radius 6.5m, TetherRadius 6m, TetherDuration 2.25; SlowPercent 24; glitch state = DISARMED+SILENCED+MUTED (items blocked) | Damage 25 | T1 CD -20 (14); T2 BulletArmorReduction -15% for DebuffDuration 10s; T3 TetherDuration +1 (3.25), Radius +1.5m | none |
| Vindicta Stake (citadel_ability_hornet_chain) | 40 | CastDelay 0.2; CaptureRadius 9m; ChainLength 9m; ChainDuration 1.75; SlowPercent 40; chain = disarm modifier + FireRateSlow | Damage 40 | T1 +45 dmg; T2 CD -22 (18); T3 chain +0.75 (2.5), radius +2m | 40 +0.5xSP |
| Vindicta Crow (citadel_ability_hornet_sting) | 32 | DebuffDuration 5; BulletResistReduction -6, TechArmorDamageReduction -6 | Impact 40; bleed 2.2% current HP/s | T1 heal -35%; T2 CD -16 (16), bleed +0.5%; T3 +2s, resists -8 more (-14/-14) | impact 40 +0.744xSP |

Facts about the two snipers vs a held target:
- Assassinate charge is the shooter's own scope time (desc: "fully charged after TimeToFullCharge of being scoped"). It does not need the target held. Pre-scope during the setup and fire when the hold lands. VERIFIED from desc.
- Neither sniper ability carries DAMAGE_DOESNT_WAKE_FROM_SLEEP (only Sleep Dagger, Smoke Bomb, Shiv/Fathom defer-damage and Lil Helpers do), so both wake a sleeper.
- Damage type (spirit vs bullet) is not in the vdata. Both scale only with ETechPower and Vindicta's build text treats Assassinate as spirit damage. So Haze T1 `BulletResistReduction` and Snare T2 `BulletArmorReduction` probably do NOT touch them. UNVERIFIABLE (Sandbox test S7).
- Vindicta full-charge hit at her real SP (sp.js), with the Rem wake threshold at the same souls (100 + 3.1 x boons, boons = std levels, 1.1 SP each):

| souls | SP | Assassinate full | uncharged (50%) | low-HP extra | Rem wake threshold | GT Charged Shot (tier) |
|---|---|---|---|---|---|---|
| 3200 | 7.7 | 97 | 49 | +108 | 122 | 113 (T1, SP 32.7) |
| 5600 | 18.0 | 107 | 53 | +211 | 131 | 147 (T1, SP 67) |
| 9600 | 35.5 | 123 | 62 | +252 | 147 | n/a |
| 10400 | n/a | n/a | n/a | n/a | 150 | 223 (T2, SP 88.6) |
| 14400 | 66.0 | 151 | 76 | +322 | 162 | 334 (T3, SP 100) |
| 24000 | 100.6 | 184 | 92 | +401 | 181 | n/a |
| 38400 | 133.2 | 214 | 107 | +476 | 199 | 499 at 48000 (SP 182) |

## 2. Holds / setups

| Partner ability (class) | CD (T) | What it does mechanically | Duration | Range / radius | Damage-break? | Stationary? | Scaling |
|---|---|---|---|---|---|---|---|
| Haze Sleep Dagger (ability_sleep_dagger) | 30 (T3 -17 = 13) | Sleep state (IS_ASLEEP); AbilityCastDelay 0.2; MinimumSleepTime 0.2; wakes SleepWakeUpDelay 0.1 +0.002xHaze SP after ANY damage (desc). Dagger's own hit is flagged DAMAGE_DOESNT_WAKE. Does not break Haze invis; does not interrupt channels | SleepDuration 2.75; T2 +1 = 3.75 | single target (AbilityUnitTargetLimit 1) | YES, any damage | SleepMoveSpeed 1.5m (still drifts, not rooted) | dagger 65 +2.2xSP; wake delay scales with SP |
| Haze T1/T3 on-wake | | T1 BulletResistReduction -10 for 6s on wake-up (bullet+melee resist only); T3 slow 40%, dash -45% for 3s on wake | | | | | |
| Rem Naptime (ability_familiar_ability01) | 200 (T3 -55 = 145) | Gaze ch.: CastDelay 0.18, AbilityChannelTime 1.9. During channel enemies only slowed 20% (MoveSpeedAndDashSlowPct), no movement abilities, still can act. At channel end SleepDuration 4.0 (state asleep, SleepMoveSpeed 1.5m), MinSleepTime 0.5. Wakes early if damage >= SleepDamageThreshold 100 +3.1xELevelUpBoons. Wake hit AwakeDamage 120 +1.6xSP. Pierces walls | sleep 4.0; T2 4.75 | CastRange 24m; Radius 19m (T2 22m); target type ALL_ENEMY | threshold-based (see table) | channel: no; sleep: 1.5 m/s drift | AwakeDamage 120 +1.6xSP |
| Naptime tiers | | T1 -stamina on wake, no stamina regen; T2 +0.75s, +3m; T3 CD -55, unstoppable + resist 50% while channelling (resist is on Rem) | | | | | |
| Rem Pillow Toss (ability_familiar_ability02) | 25 (T1 -7 = 18); T3 +1 charge, 8 between | Projectile, CastDelay 0.3, Radius 5m; FadingSlowPercent 36 for EffectDuration 3.0; T2 +2m, FireRateSlow 35; hit cuts other CDs by CDReduceOnPillowHit 5 | slow 3.0 | CastRange 40m | n/a | NOT a hold, slow only | 75 +1.6xSP; T3 +100 |
| Mo & Krill Combo (ability_ult_combo) | 150 (T2 -30 = 120) | Target mod `modifier_ult_combo_target` (loc name "stunned"): spring-damped drag to Mo, world-fixed offset (m_flTargetPosDistance 100, range 20). Target mod not duration-reducible. Interrupted if Mo is STUNNED. Kill within m_flKillCheckWindow 3.0 of end gives Mo BonusHealthOnKill 40 +2xboons | AbilityChannelTime 2.4; T3 +0.7 = 3.1 | AbilityCastRange 4.0m, hero enemy only, single | no break-on-damage field exists; no target-side mitigation field | held at fixed offset from Mo (moves only if Mo can move; unknown) | DPS 40 +0.6xSP; T3 +40 DPS, +0.4 scale; T1 100% lifesteal, T2 Mo +50 bullet resist (Mo's own) |
| Graves Grasping Hands (ability_necro_zombiewall) | 34 (T3 -14 = 20) | Wall ZombieWallLength 14m, ZombieWallDeployTime 0.6, GroundAuraPopDelay 1.1, AbilityDuration 5, CastRange 24m. Enemy crossing gets modifier_citadel_root ImmobilizeDuration 1.0 + TetherDuration 1 (TetherRadius 0.1m = hard hold) + SlowPercent 40, Damage 90 | root 1.0; T3 +0.75 = 1.75; wall T1 +2s (7), T2 +10m (24) | | no break field | yes, root + 0.1m tether | 90 +1.6xSP; T2 +90 |
| Venator Snap Trap (ability_priest_beartrap) | 28 (T1 -11 = 17); 2 charges, 8 between; T3 +1 | Trap ArmTime 0.5, Lifetime 30, trigger Radius 2m, springs on first enemy touch; modifier_priest_immobilize ImmobilizeDuration 1.25, TetherDuration 0.6 (TetherRadius 0.3m); RevealDuration 6 (debuff mask VISIBLE_TO_ENEMY + GLOW_THROUGH_WALLS_TO_ENEMY) | root 1.25; T2 +1.0 = 2.25 | CastDelay 0.2 | no break field | yes, root | 80 +2.2xSP; T3 +30% damage from Venator on revealed |
| Apollo Itani Lo Sahn (ability_fencer_ultimate) | 145 (T2 -35 = 110) | Cast: CastDelay 1.5, dash DashRange 27m (T1 +8), DashRadius 7m. Target mod: HEALING_DISABLED, DISARMED, SILENCED, MUTED, DASH_DISABLED, no cleanse; TimeScaleDebuff 70; **IncomingDamageReductionPercent 70**; Apollo invulnerable CasterLockDuration 1.8 | DebuffDuration 1.8 | | reduction 70% on victim | slowed to 30% time (not rooted) | ImpactDamage 70 +0.77xSP, DelayedDamage 200 +2.6xSP at expiry; <50% HP +60% (T2 +50 = 110%) |
| Doorman Hotel Guest (ability_doorman_hotel) | 140 (T1 -20 = 120) | Targets HERO_ENEMY only (ally use REFUTED). Channel 1.0 (cannot cancel), PostCast 0.7, CastRange 7m. TimeSlowPercentage 100 for TimeSlowDuration 1.0 (pre-teleport freeze). Victim gets OUT_OF_GAME + IGNORED_BY_NPC_TARGETING + DO_NOT_DRAW (m_NoDrawModifier), returns at original position | AbilityDuration 6.5 (no upgrade) | | target is out of play, cannot be shot | n/a | Damage 75 +1.0x; LateCheckoutDamage 125 +1.5x, T2 Damage +150, LateCheckoutStun 1.5 on failure |

## 3. Arithmetic per candidate pair (hold window vs payoff timing)

Payoff times: Assassinate 1.0s scope (0 cast delay) -> pre-scope = 0 needed; worst case scope starts when hold lands. GT Charged Shot 0.5s cast + UNKNOWN charge (S1).

| Pair | Hold window | Vindicta scope 1.0 | Spare (scope after hold) | Q1 damage breaks hold / full damage | Q2 long enough | Q3 stationary | Verdict |
|---|---|---|---|---|---|---|---|
| Haze Sleep | 2.75 (3.75 T2) | fits | 1.75 (2.75 T2); minus wake delay 0.1+0.002xHaze SP after the first hit | First hit wakes target 0.1-0.3s later; hit itself lands in full (no mitigation field). Second shot lands on a waking/awake target | Yes for one shot; Vindicta's second shot needs another 1.0s scope so only shot 1 is guaranteed | drifts 1.5 m/s, cannot act | SURVIVES (one guaranteed shot). Haze T1 shred only starts after waking and is bullet/melee resist, so it does nothing for shot 1 |
| Rem Naptime | channel 1.9 (slow only) then sleep 4.0 (4.75 T2) | fits | 3.0 after sleep starts (4.0s sleep - 1.0) | Wakes only if ONE hit (assumed per hit) >= 100+3.1xboons. Assassinate full 97/107/123/151/184/214 vs 122/131/147/162/181/199: below threshold until ~24k souls; uncharged never. GT Charged Shot 113-147 at T1 exceeds 122-131 early; T2+ (223+) always wakes | Yes | asleep drift 1.5 m/s; channel phase target mobile (80% speed) | SURVIVES for Vindicta mid-game (full shot < threshold until ~24k); GT T2+ always wakes it (still a free 134+ hit). CD 200 (145) one-use per fight |
| Rem Pillow Toss | slow 36% for 3.0 | n/a | n/a | n/a | not a hold | no | DIES as a hold (slow only). Keep only as Naptime CD cutter (-5s per hit) |
| Mo&Krill Combo | 2.4 (3.1 T3) | fits | 1.4 (2.1 T3) | no break field; no target mitigation field. Kill credit/HP window 3.0 after end | Yes, but Mo must be inside 4m | dragged to fixed offset from Mo; stationary iff Mo is | SURVIVES on arithmetic; CD 150 (120). Needs S4 to settle damage-through-hold |
| Graves Grasping Hands | 1.0 (1.75 T3) | fits only with pre-scope | 0.0 (0.75 T3) | root, no break field | Marginal before T3; enemy must walk through wall (deploy 0.6 + pop 1.1) | hard root | SURVIVES only with pre-scope or T3 (1.75). Wall cannot be forced onto a target |
| Venator Snap Trap | 1.25 (2.25 T2) | fits | 0.25 (1.25 T2) | root; reveal 6s | Yes, T2 comfortably | hard root | SURVIVES (T2). Needs enemy to step on it (arm 0.5) |
| Apollo ult | 1.8 | fits | 0.8 | **70% damage reduction on victim for the 1.8s**: shot lands at 30% inside the window; at expiry delayed 200+2.6xSP | cast delay 1.5 + dash | not rooted (time scale -70) | DIES as hold+shot. Only workable as "fire at expiry" (0 spare, race with delayed hit) |
| Doorman Hotel | 6.5 but target is OUT_OF_GAME | n/a | n/a | cannot be shot while away; ally targeting refused | n/a | removed | DIES as sniper payoff (it removes the target; only return/failed checkout stun 1.5 T2 gives a 0.5 spare window) |
| GT own Snare (self-pair) | tether 2.25 (3.25 T3), radius 6m | Charged Shot 0.5 + unknown | n/a | tether, not a root: target can move inside 6m | Charged shot detonates trap early (ChargedShotHitRadiusScale 30) | no | note only |

## 4. Interaction questions

| Question | Result |
|---|---|
| Does sniper damage break sleep? | Haze: VERIFIED yes (desc, SleepWakeUpDelay 0.1+0.002xSP, min 0.2). Rem: depends on SleepDamageThreshold 100+3.1xboons; per-hit vs cumulative UNVERIFIABLE (S2). Stun/root/Combo/trap/wall: no break-on-damage field in vdata (only 11 `Break` hits, all `BreakOnParentStunned`), so presumed not broken; UNVERIFIABLE until S3 |
| Full damage on held target? | VERIFIED no mitigation field on Sleep, Naptime, Combo, wall, trap. REFUTED for Apollo (70%). Hotel: target cannot be hit while out of game |
| Hold long enough for scope/charge + cast? | Vindicta 1.0s: Haze 2.75, Rem 4.0, Combo 2.4, Trap 1.25, wall 1.0 (0 spare), Apollo 1.8 (but cut). GT Charged Shot: unknown charge time (S1) |
| Stationary or just unable to act? | Root: wall (tether 0.1m), trap. Sleep: drifts 1.5 m/s. Naptime channel: not held (80% speed). Combo: dragged to Mo. Apollo: time-scaled 30%. Snare/Stake: tethers (6m/9m radius), not stationary |
| Can an ally action trigger/extend the hold? | Hotel: ally cannot be target (HERO_ENEMY). Combo: single target, Mo within 4m. Snare detonation by Charged Shot is GT's own only. No file field lets sniper damage extend any hold |

## 5. Sandbox scenarios (UNVERIFIABLE-from-files items)

- S1: GT Charged Shot: time cast->full charge, damage vs charge fraction (decides GT fit for every hold below 1.5s).
- S2: Rem Naptime: sleeping dummy, one Assassinate / one Charged Shot hit at known SP; does wake depend on per-hit or cumulative damage; does early wake still trigger AwakeDamage.
- S3: Wall root, Trap root, Combo: shoot target mid-hold; does root/stun persist, is damage full.
- S4: Combo: damage dealt to held target by ally during channel; does Mo moving move the target.
- S5: Apollo ult: shot at 0.5s and at 1.8s+0.05; confirm 30% and ordering vs delayed damage.
- S6: Hotel: shot at target during the 1.0s TimeSlow channel and after return; confirm untargetable at 6.5s.
- S7: Does Haze/Snare bullet-resist shred raise Assassinate / Charged Shot damage (damage type).
- S8: Assassinate second shot: min time between shot 1 and 2 with 1.0s rescope.

## 6. Stage-A card corrections

- Rem Naptime: card cd 0 -> real 200 (145 T3); sleep base 4.0 (card "not in file").
- Rem Pillow Toss: card cd 8 -> real 25 (18 T1); 8 is between-charge delay only after T3 charge.
- Haze Sleep Dagger: card cd missing -> 30 (13 T3).
- Venator trap: card says charge delay 8; T1 CD -11 (17), T3 +1 charge (3 total).
- Guided Owl: card cd missing -> 125 (85 T2), Damage 230 +0.937xSP, T1 +85.
- Hotel Guest: card "ally use unverified" -> REFUTED (HERO_ENEMY).
- Vindicta Crow: card -6%/-6% matches; Stake cd 40 (18 T2).

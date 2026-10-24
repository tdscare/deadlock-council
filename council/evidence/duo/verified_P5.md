# verified_P5: Mo & Krill Combo hold + payoff

Sources: abilities.vdata (ab.py, tiers_p5.py), heroes.vdata (hero_krill), items via audit_D_q.py. S = spirit. "Tn" = ability upgrade tier. Unit note: 1m = 39.37u is an ASSUMPTION used only to turn vdata units (u) into metres; the vdata expresses Combo range in m (4.0m) but hook offset in u (100).

## 1. Mo & Krill, raw facts

| Ability (class) | CD | Duration / cast | Range / radius | Damage + scaling | Tiers T1 / T2 / T3 |
|---|---|---|---|---|---|
| Combo (ability_ult_combo) | 150 (AbilityCooldown, scaled by ETechCooldown) | AbilityCastDelay 0 (instant), AbilityChannelTime 2.4 (scaled by EChannelDuration and ETechDuration) | AbilityCastRange 4.0m (scaled by ETechRange), UnitTargetLimit 1, cone ConeAngle 120 / ConeHalfWidth 40, target type HERO_ENEMY only | DPS 40 (+0.6 x ETechPower), is ability damage. Kill within channel or KillCheckWindow 3.0s after: BonusHealthOnKill 40 (+2 x ELevelUpBoons) permanent max HP | T1 LifeStealPercentOnHit +100 (scaled EHealingOutput) / T2 AbilityCooldown -30 (=120), BulletResist +50 (Mo only, ConditionallyApplied) / T3 AbilityChannelTime +0.7 (=3.1), DPS +40 (=80), scale +0.4 (=1.0 x S) |
| Scorn (ability_intimidate) | 13 | AbilityCastDelay 0.2, ChannelMoveSpeed 1.3m | Radius 9m | Damage 50 (+0.75 S); heal DamageHealMult 1.2 vs hero, DamageHealMultNonHero 0.35 | T1 Damage +35 (=85) / T2 CD -5 (=8), Radius +1 (=10) / T3 DamageBonus +15 (%), DebuffDuration 16. Debuff modifier MODIFIER_ATTRIBUTE_MULTIPLE, "OVERHEAD_DRAW_FOR_CASTER_ONLY", text says {hero_name} deals +15%. Mo-only wording |
| Burrow (ability_burrow) | 40 | CastDelay 1.0, ChannelTime 5 | Radius 5m, UpForce 250, TossDuration 1 (knock-up on emerge), SpinDuration 1.5, SpinSlowPercent 8 for 0.3s | DPS 75 (+1.488 S). BulletResist 60, TechResist 30 while under. BonusMoveSpeed 5m/s; EnemyDamageSpeedPenalty 0.5, SpeedLostDuration 1 | T1 DPS +50 / T2 ChannelTime +4 (=9), Radius +2 (=7m) / T3 CD -20 (=20), BonusMoveSpeed +4 (=9) |
| Sand Blast (ability_throw_sand) | 40 | CastDelay 0.15, disarm AbilityDuration 2.5 | AbilityCastRange 25m, InitialWidth 5m +0.5m/m | Damage 40, no spirit scaling listed | T1 Damage +50, Range +5m / T2 Slow 24%, GroundDashReduction -26% / T3 CD -25 (=15), Duration +1.5 (=4.0), blocks stamina |

Mo base: EMaxHealth 930, EMaxMoveSpeed 8 m/s. Burrowed 13 m/s (T3 17), minus damage penalty.

## 2. Combo mechanics (answers Q1)

| Question | Finding | Status |
|---|---|---|
| Does target stay stationary? | m_TargetModifier modifier_ult_combo_target contains a modifier_drag_custom (modifier_ult_combo_attach): EDragOffset_WorldFixed, EDragPull_SpringDamped, m_flTargetPosDistance 100u (range 20u) = target is spring-pulled to a fixed world point about 100u (about 2.5m) in front of Mo. m_bZeroVelocityOnEnd false (keeps velocity when it ends). m_bBreakOnParentStunned false (target being stunned by a partner does not end the hold). | VERIFIED |
| Is it a stun? | Modifier localisation "modifier_citadel_stunned", icon class "stunned", StatusEffectPriority 50, HUD centre. NO m_nEnabledStateMask on the target modifier in vdata, so the stun flag is set in code (CCitadel_Modifier_UltCombo_Target). Target modifier m_bDurationReducible=false (debuff resist does not shorten), but the attach drag is m_bDurationReducibleByCrowdControlDiminish=true | stun nature UNVERIFIABLE-FROM-FILES |
| Untargetable / invulnerable? | No untargetable, invulnerable or damage-immunity flag anywhere in the Combo block. Partner damage therefore not blocked on the data | VERIFIED (absence); in-game confirm |
| Does damage break the hold? | No break condition on damage in vdata. Only Mo being STUNNED interrupts (m_bitsInterruptingStates = MODIFIER_STATE_STUNNED, same as the hook). Channel is MODIFIER_STATE_BUSY_WITH_ACTION | VERIFIED |
| Can an ALLY extend it? | AbilityChannelTime scales with EChannelDuration / ETechDuration of MO only. No ally hook in vdata. Items: Duration Extender (imbue) BonusAbilityDurationPercent 22, Superior Duration 28 (applied to Mo) | VERIFIED no ally extension |
| Can ally CC be stacked on it? | Possible but diminish applies to the drag (CC diminish flag true). Exact diminish curve not in these files | UNVERIFIABLE |
| Kill reward | Mo gets permanent HP only if the kill falls inside channel + 3.0s. m_bCasterCountsAsAssister=false for killcheck modifier, so the partner's killing blow still counts for Mo (killcheck is a Mo-owned modifier on the target) | VERIFIED structure; credit by partner killing blow = UNVERIFIABLE, test in sandbox |

### Combo window arithmetic (own damage, Mo only)
| Tier | Window | Own damage |
|---|---|---|
| base | 2.4s | 96 + 1.44 S |
| T3 | 3.1s | 248 + 3.1 S (80 DPS, 1.0 scaling) |
| T3 + Duration Extender (+22%) | about 3.78s | about 302 + 3.8 S (assumes multiplier applies to total) |
| T3 + Superior Duration (+28%) | about 3.97s | about 318 + 4.0 S |

Range with imbues: 4m x 1.20 (Mystic Expansion TechRangeMultiplier 20) = 4.8m; Greater Expansion 30 = 5.2m. Mo's current build puts Expansion on Scorn, not Combo, so the 4m is the real number unless re-imbued.

## 3. Getting within 4m (answers Q2)

| Route | Numbers | Result |
|---|---|---|
| Mo's own Burrow | CastDelay 1.0, 13 m/s under ground (8+5; 17 at T3), channel 5s (9s at T2). Emerge knocks up enemies in Radius 5m (7m T2) for TossDuration 1 | Mo can close ~13m of gap in 1.0s after the 1.0s delay. Whether a tossed (airborne) target can be Combo'd while in the toss is UNVERIFIABLE; sandbox: emerge and press Combo at 0.0s / 0.5s / 1.0s after emerge |
| Bebop hook to Mo | citadel_ability_hook pulls the target to BEBOP: m_flReturnPositionForwardOffset 100u (about 2.5m in front of Bebop), m_flCloseEnoughDistance 30u, ReturnSpeed 2000u/s. It cannot deliver an enemy to Mo. It lands the enemy about 2.5m from Bebop, so Mo must stand within about 1.5m of Bebop (inside 4m, assuming 39.37u/m) | VERIFIED: pulls to Bebop, REFUTED: pulls to Mo |
| Hook target types | m_nAbilityTargetTypes HERO (incl. allies), TROOPER_ENEMY, NEUTRAL. FriendlyHookIgnoreRange 8m (allies inside 8m ignored). Hook can also be thrown at Mo (pulls Mo to Bebop) | VERIFIED |
| Hook restriction after landing | RestrictionDuration 0.5s: slow (SlowPercent 72), movement input disabled, dash disabled, air jumps disabled. Combo has CastDelay 0 | 0.5s window for Mo to press Combo, no cast delay: fits |
| Bebop Uppercut | EnemyHeroTossVelocity 20m, TossDuration 0.5, on-land damage 75 (+0.6) in OnLandDamageRadius 14m, ExplodeDebuffDuration 5. Can be used on allies (TossDurationFriendly 0.3, TossVelocity 25m) | Throws an ally Mo toward target (distance depends); mechanically UNVERIFIABLE |
| Vindicta Stake | ChainLength 9m, CaptureRadius 9m, EnemyDragSpeed 1000, SlowPercent 40, ChainDuration 1.75 (+0.75 T3 =2.5) | Restricts to 9m, does NOT bring within 4m. Whether stake drags to the stake point (could be at Mo's feet): UNVERIFIABLE; sandbox: plant at Mo's feet, measure ending distance |
| Grey Talon Spirit Snare | TetherRadius 6m, Radius 6.5m, ArmTime 2.0, TripTime 0.5, TetherDuration 2.25 (+1 T3), curse silences, disarms, stops item use. Trap placed at Mo: enemy ends up inside 6m of the trap, not necessarily within 4m of Mo | partially fits; 6m tether > 4m range |
| Warden Binding Word | Cast range 15m, EscapeTime 2.8, EscapeRange 20m, ImmobilizeDuration 1.75 (+0.75 T2 = 2.5) | Target immobilized in place at 2.8s: gives Mo 1.0 + travel time to approach before it lands |

## 4. Partner payoff numbers inside the window (answers Q3)

| Partner ability | Cd (tier) | Damage | In-window total | Fits? |
|---|---|---|---|---|
| Bebop Hyper Beam (citadel_ability_bebop_laser_beam) | 120 (T1 -20 = 100) | DPS 160 (+2.511 S); T2 +108 = 268; T3 lifesteal 65% hero. CastDelay 1.0, ChannelTime 11, BeamCloseDamagePercent 75 (within BeamCloseRadius 5m: meaning UNVERIFIABLE) | 2.4s: 384 / 643 (T2) + 6.03 S. 3.1s: 496 / 831 (T2) + 7.78 S. If the beam is started when Combo is pressed only (window - 1.0s cast) = 1.4s: 224 / 375 + 3.5 S. So start the beam about 1.0s before Combo | Yes if beam is started first. The beam outlasts the window (11s) |
| Bebop Sticky Bomb (citadel_ability_sticky_bomb) | 18 (T1 -8 = 10) | 85 (+1.5 S); T2 +85 = 170. FuseTime 3.5, Radius 8m, CastRange 6m. Permanent stacks +2.5% (+0.01 S) per kill, +1% per hit | One bomb. Explosion falls inside a 2.4s window if attached 1.1 to 3.5s before Combo (0.4 to 3.5 for 3.1s window) | Yes, but must be pre-applied |
| Bebop Hook T1 | 23 (T3 -11.5) | BulletAmp +20% weapon damage vs victim, 6s | Bebop weapon only | does not amplify beam (spirit) |
| Vindicta Assassinate (citadel_ability_hornet_snipe) | 55 (T1 -15 = 40), 2 charges, 2.5s between | 90 (+0.93 S), full charge TimeToFullCharge 1.0 (MinChargeDamagePercent 50); under LowHealthEnemyThresholdPct 50 adds 90 (+2.3 S), T2 +80 | One fully charged shot fits (1.0 charge + shot, spare 1.4s of 2.4). Second shot needs 2.5s between charges, so not in window unless first shot pre-fired. Held target is fixed, hit guaranteed | Yes for 1 shot |
| Vindicta Crow (citadel_ability_hornet_sting) | 32 (T2 -16 = 16) | Impact 40 (+0.744), bleed DotHealthPercent 2.2 (+0.5 T2) of current HP per 1s tick for 5s (+2 T3), resist -6 / -8 T3 | 2 to 3 bleed ticks | Yes |
| Grey Talon Charged Shot (ability_charged_shot) | 17, 1 charge (+1 T1), 4s between charges (-3 T3) | 80 (+1.0 S); T2 +54; T3 +1.0 scale (=134 + 2.0 S) | Charge time not in file | UNVERIFIABLE timing |
| Grey Talon Owl (ability_guided_arrow) | 125 (T2 -40) | 230 (+0.937 S), T1 +85; StunDuration 0.75, ExplosionRadius 12m, CastDelay 1.5 | Stun overlaps an existing hold, so redundant on target | damage only |
| Pocket Affliction (synth_affliction) | 170 (T1 -35 = 135) | DPS 32 (+0.21 S) per DamageInterval 0.5; duration 10 (+3), radius 9 (+4); T3 +13 DPS, +0.1 scale, prevents healing. NON-LETHAL, no item procs | 2.4s: 77 + 0.50 S; T3 (45, 0.31): 108 + 0.74 S | Fits, but cannot kill so cannot take the kill-check |
| Pocket Barrage (synth_barrage) | 32 (T2 -16) | 4 projectiles x 32 (+0.465 S), T1 +16 each; amp 6% per stack (+4 T3) 15s; ChannelTime 2.0 | 128 + 1.86 S (192 + 1.86 S T1) | Fits, 2.0s channel inside 2.4 |
| Seven Static Charge (citadel_ability_static_charge) | 42 (T1 -20) | 35 (+0.79 S), T3 +160; ShockDelay 3.5, stun 0.9 (+0.9 T3) | Detonates 3.5s after apply; time to land inside the window | Fits if applied 1.1 to 3.5s before |
| Seven Power Surge (ability_power_surge) | 50 (T1 -18) | 10 (+0.14 S) per chain x ChainCount 4, ChainTickRate 0.2; T3 TechResistDebuff -15% (DebuffDuration), Duration 10 | per-bullet; T3 spirit resist shred applies to Mo's Combo spirit damage (scaled DPS) | Plausible, shred ownership UNVERIFIABLE |
| Seven Storm Cloud (citadel_ability_storm_cloud) | 205 | DPS 95 (+0.6 S), DamageInterval 0.3, T3 +65; channel 7, radius 10 to 30m | 2.4s: 228 + 1.44 S; 3.1s: 294 + 1.86 S (no T3 DPS) | Fits but CD 205 vs Combo 150/120 |
| Warden Binding Word (ability_warden_lock_down) | 34 (T3 -14) | 110 (+2.437 S); immobilize 1.75 (+0.75 T2 = 2.5); T1 +20% bullet dmg 5s; T3 silence | Immobilize covers 1.75/2.4 = 73% of base window; T2 2.5s covers 2.4 fully (0.1 spare); 2.5/3.1 = 81% of T3 window | Fits only with T2 |

### DoT items on a held target
| Item | Numbers | In 2.4s window |
|---|---|---|
| Alchemical Fire | CD 30, Duration 5, Radius 10m, tick 0.5. DPS 45 (+0.2 S), DPSIncrease 7 (+0.04 S) per second, DPSMax 95 (+0.4 S), bullet resist -7% | Average DPS about 53 over 2.4s = about 128 + 0.6 S (ramp-per-second assumed). Target held at a fixed point so it cannot leave the puddle |
| Toxic Bullets | DotHealthPercent 1.9 (+0.006 S) max HP over DotDuration 4, BuildUpPerShot 1.28, heal reduction -35% | Needs build-up; slow in 2.4s |
| Spirit Burn | Trigger DamageThreshold 500 within 5s; Explosion 50, DPS 24 (+0.06 S) 8s, heal -70%, ImmunityDuration 20 | Beam T2 (643 in 2.4s) trips it in the window |
| Mystic Vulnerability / Escalating Exposure | TechArmorDamageReduction -8 / MagicIncreasePerStack 4.5 x MaxStacks 12 | Amplify Combo and partner spirit damage; applies on spirit damage taken |

## 5. Pair verdicts (arithmetic only)

| Pair | Verdict | Arithmetic |
|---|---|---|
| Mo + Bebop | SURVIVES (setup works, but not as written in the card) | Hook pulls to BEBOP not Mo: Mo must stand within about 1.5m of Bebop. Restriction 0.5s vs Combo cast delay 0 fits. Beam 1.0s cast before, Sticky Bomb 1.1 to 3.5s before. Window dmg: Beam T2 643 + Combo 96 + bomb 170 (+ spirit) = about 909 + S terms in 2.4s |
| Mo + Warden | SURVIVES narrowly | Binding Word 2.8s lead covers Burrow (1.0 + travel at 13 m/s). Needs Warden T2 (2.5s immobilize) to cover a 2.4s Combo; Combo already stuns, so Warden adds a pre-pin and approach time rather than hold |
| Mo + Seven | SURVIVES as damage partner | Static Charge detonates in window if pre-applied; no pull. Power Surge T3 resist shred is the only shared multiplier |
| Mo + Vindicta | WEAK | Stake gives 9m tether, not 4m. Assassinate 1 shot fits (1.0 charge, 1.4s spare); second does not fit |
| Mo + Grey Talon | WEAK | Snare 6m tether vs 4m range; Owl stun redundant; Charged Shot timing unknown |
| Mo + Pocket | DIES | Affliction 77 + 0.5 S in window, non-lethal, no procs; adds nothing Combo-specific; Barrage is the only fit (2.0s channel) |

## 6. Sandbox scenarios to settle UNVERIFIABLE items
1. Bebop hooks an enemy while Mo stands 1m, 2m, 3m from Bebop: record distance from Mo at landing, and whether Combo cannot be pressed.
2. Combo on a target while a partner shoots it: confirm partner damage lands and the hold does not break.
3. Press Combo at 0.0 / 0.5 / 1.0s after Burrow emerge on a tossed target.
4. Partner killing blow inside the 3s kill-check: does Mo get BonusHealthOnKill.
5. Stack Warden immobilize / Talon tether / Seven stun with Combo: measure total hold time (diminish).
6. Hyper Beam damage at 3m / 6m range (BeamCloseDamagePercent 75).
7. Scorn debuff DamageBonus: does a partner deal +15% to a debuffed target (text says Mo only).

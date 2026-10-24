# P2 Brawler + sustain/zone partner: verified (abilities.vdata via ab.py, heroes.vdata)

Tier mapping follows the order of m_vecPropertyUpgrades (T1,T2,T3) cross-checked against the *_tN_desc text. "spirit" = per point of spirit power (x spirit). Items not run: no item is needed for these numbers (items listed only where the stat names say what scales).

## 1. Brawlers

| Ability | CD base (T1/T2/T3) | Duration / cast | Radius / range | Mechanic | Values (T1/T2/T3) | Spirit scaling |
|---|---|---|---|---|---|---|
| Victor Aura of Suffering (painaura) | AbilityCooldown 2 (no tier change) | AbilityDuration 8 channel (scales EChannelDuration, ETechDuration), DebuffDuration 0.5 (T1 +0.5) | Radius 8m (T3 +1 = 9m) | Channel: tick 0.25s dmg to enemies in radius, ramps MinDPS to MaxDPS; also hits Victor (SelfDPS 15, SelfDamagePercentage 70). Slow + dash slow; no stun. Damage is not blocked by being hit; it is a channel (BUSY_WITH_ACTION), so Victor is stuck channelling | T1 SlowPercent 20 + EnemyDashSlowPercent -22; T2 MinDPS +6, MaxDPS +34; T3 IncomingDamagePercent +15 (enemies take +15% from everyone) and Radius +1 | MinDPS 13 (+0.15x), MaxDPS 58 (+0.72x). Tooltip also lists OutgoingDamagePercent (value 0 in file, enemy outgoing amp unverified) and MinRadius/MaxRadius (radius may ramp: unverified) |
| Victor Pain Battery (shocktarget2) | 2 | CastDelay 0.35, post 0.2 | 28m, 7 bolts, 40deg | Needs stored damage taken (StoredDamageHealthPercentRequired 40, BatteryGenerationPercent 100); 1 hit/target | T1 slow 32% for 2s; T2 Damage +50; T3 heals 15% of missing HP | Damage 100 (+1.6x) |
| Victor Jumpstart (selfzap) | 30 (T2 -8 = 22) | 4.5s, channel 0.35 | self | Self-hit 15% current HP, then BonusMoveSpeed 3m and regen | TotalHealthRegen 100 (+1.2x), T2 +70; T3 +1 charge (8s between), 50% debuff resist | 1.2x |
| Victor Shocking Reanimation (revive) | 240 (T3 -95) | channel 3 + 0.5 delay, respawn 50% HP | 18m | Triggers on lethal damage; slow 120 diminishing 3s; T3 stun 1.5 | Damage 200 (+2.0x), T3 +175 | 2.0x |
| Abrams Siphon Life (bull_heal) | 42 (T1 -20 = 22) | 4s (T2 +2) | Radius 8m (T3 +2m) | Drains enemies nearby; heals HealingFactor 70% of damage to heroes, 35% to non-heroes | DPS 22 (+0.6x); T3 DPS +18 and +0.12x | 0.6x (0.72x T3) |
| Abrams Shoulder Charge (bull_charge) | 33 (T3 -18 = 15) | AbilityDuration 1.4 | ChargeRadius 2.2m; speed 18.75 to 30 m/s (about 30+ m travelled) | Pushes one hero; wall hit stuns. Base collide stop 0.3s | T1 slow 32% for 3s; T2 wall stun 0.8; T3 +1.5 weapon dmg 6s on hero collide | Damage 30 (+1.4x) |
| Abrams Infernal Resilience (beefy) | passive | RegenIncomingDamagePercent 13 over 20s | - | Heals 13% of damage taken over time | T1 +200 max HP; T2 18% melee lifesteal; T3 +9% regen, +20% debuff resist | none |
| Abrams Seismic Impact (bull_leap) | 215 (T1 -30) | TossSpeed 450 | Impact 9m (T3 +6 = 15m) | Leap and slam: stun StunDuration 1.6 (T2 +0.8 = 2.4); T3 5s unstoppable on cast | Damage 100 (+2.325x) | 2.325x |
| Billy Bashdown (punkgoat_ult) | 35 (T1 -10 = 25) | channel 0.3, post 0.3 | wave grows 0.5 to 8m | Toss 0.4s, pull down 0.75s (PullDownRange 3m): enemies lifted then dragged down, so a brief hold, not a lasting stun | T2 +1 charge, +2m cast range; T3 -3s between charges, 50% heavy melee dmg | Damage 35 (+1.1x) |
| Billy Rising Ram (goatflip) | 32 (T3 -13 = 19), -50% on impact (ReduceCooldownOnHitPct 50) | AbilityDuration 0.3 (T2 0.4) | ChargeSpeed 1200 | Carries one enemy up (TimeGoingUpEnemy 0.2, AirControlDebuffDuration 1.5s, dash -70%) | T1 +25% weapon dmg 5s; T3 +10% max HP 16s | Damage 40 (+1.9x) |
| Billy Blasted | 27 | 8s (melee extends: heavy 4.5s, light 2.8s, max 35s) | - | Melee reloads ammo, marks wrecked: BulletDamageAmp 10 for 7s | T1 +2.25m speed; T2 +1 Bashdown charge, amp +7; T3 +50 melee bonus HP | MaxHealthMelee 70 (+0.6x) |
| Billy Chain Gang (tether) | 175 (T2 -40) | 2.8s, pull 4m over 0.8s | 12m (T3 +5) | Enemies cannot use movement abilities, slowed 25-35%, then yanked to Billy. Breaks after 0.5s without line of sight | T1 +40 bullet/spirit resist while active; T3 +1.3s unstoppable per hero pulled | Damage 120 (+0.7x), DPS 45 (+0.9x) |
| Yamato Power Slash | 12 (T2 -4 = 8) | charge 1.4s, post 0.2; BulletResist 60 while channelling | 22m line, width 4 (T3 +8m) | Hold enemy still needed to land the full 1.4s | T1 slow 32% 3s; T3 +150 dmg and +0.5x | Full 145 (+1.85x); short/medium charge 30%/50% |
| Yamato Flying Slash | 36 (T1 -18 = 18) | slow 2.5s, 40% | 26m (T3 +15 = 41m) | Pulls Yamato to an enemy. T3: can grapple allies = Yamato moves to the ally, ally does not move; +1 charge (5s between) | T2 +35 spirit power for 6s | none |
| Yamato Crimson Slash | 16 (T3 -10 = 6) | cast 0.3, post 0.4 | 13m cone | FireRateSlow 30% for 4s; heal if hero hit | HealFixedHealth 55 (+1.036x); T1 +30% melee 4s; T2 +6% max HP heal; T3 CD and scaling +0.4x | 1.036x heal, damage 55 (+0.37x, T3 +0.6x) |
| Yamato Shadow Transformation | 150 | 5s (T2 +3) | self | Immune to negative effects, +30 bullet/spirit resist (T3 +30 each), kill extends 2s | - | - |

Brawler bases (heroes.vdata): Victor 800 HP, regen 1.5, speed 6.3; Billy 820 HP, regen 2.0, speed 7.0; Abrams 800 HP, regen 1.5, speed 6.4; Yamato 730 HP, regen 1.0, speed 8.2.

## 2. Partners

| Ability | CD (tiers) | Duration / cast | Radius / range | Mechanic | Values by tier | Spirit scaling |
|---|---|---|---|---|---|---|
| Kelvin Frost Grenade | 30 (T2 -10); 2 charges, 7s between | cloud 4s slow, cast 0.1 | 6.5m (T3 +2 = 8.5) | Heals allies in cloud and slows enemies 32% for 4s (SlowDuration). AuraSlowAmount -75 unexplained | T1 Damage +30, HealAmount +30; T2 stamina regen frozen; T3 radius, heal +0.9x, dmg +0.8x | HealAmount 60 (+0.8x), Damage 60 (+0.6x). Heal looks flat per application (per-tick vs once unverified) |
| Kelvin Ice Path | 50 (T2 -25) | trail 8s, aura 18s | ModifierRadius 5m | Allies on the trail get MoveSpeedBonus 2m, SprintSpeedBonus 2m, shooting-speed penalty removed. Enemies can also walk it | T1 +2m speed, +35 bullet resist for Kelvin; T3 +35% and +20 spirit for Kelvin | Kelvin only |
| Kelvin Arctic Beam | 28 (T3 -13) | 5s | 25m x 1.1m | Slow ramps to 24% min / 16% max, fire rate -20% max over 2s (MaxSlowTime), dash -18% | T1 max slow 20, fire-rate slow 25; T2 DPS +20 (+0.6x); T3 2 extra beams within 10m | DPS 45 (+0.38x) |
| Kelvin Frozen Shelter | 185 (T1 -20) | 5s (T2 +1.5 = 6.5), cast 0.2 | cast range 8m on self or an ally hero; Radius 10m, BlockerScaleFactor 115 | Dome (impenetrable per text) around the target: allies BonusHealthRegen 90, enemies slowed 28% (and FireRateSlow modifier); EnemyDragSpeed 1000; a freeze_debuff (-100% time scale) aura exists on the modifier and conditions are not readable | T3 purge non-ult debuffs on cast, regen +65 (155) and +1.0x | 90 (+0.2x), T3 +1.0x = 1.2x |
| Dynamo Kinetic Pulse | 26; 1 charge (T1 +1, 5s between) | cast 0.42 | 16m x 5.5m (T3 20m) | Lifts target; T2 -15% bullet resist plus 24% slow 4s | Damage 115 (+1.55x), T3 +135 | 1.55x |
| Dynamo Quantum Entanglement | 20 (T2 -6) | 1.4s, untargetable, cast range 10m (T1 +6) | AllyDistance 13m | Teleports Dynamo and nearby allies (within 13m) untargetable | T3 debuffs -50%, +1 charge | none |
| Dynamo Rejuvenating Aurora | 48 (T2 -20) | channel 5s (T2 +1s); T3 NoChannel | ShareWithFriendsRadius 8m | Heals Dynamo and allies within 8m, can dash and melee while channelling | HealingPerSecond 30 (+0.4x); T1 +4m speed for 8s; T3 +2.5% max HP per second | 0.4x |
| Dynamo Singularity | 250 | channel 2.75 (T2 +0.75, direction of change not stated in file), cast 0.2 | VacuumRadius 7m (T1 +2 = 9m) | Pulls enemies in toward Dynamo while channelling; Dynamo is not made untargetable | DPS 75 (+0.28x), T3 +6% health DPS | 0.28x |
| Baba Baba's Brew | 27 (T2 -14) | channel 1.0, BrewTime 1.5; locks: Barrier at 2.5, Silence 3.5, Fire 4.5 | cast 12m, Radius 6m (T1 +3 = 9m) | Thrown pot cycles barrier, silence, burn. Barrier 8s, silence 3s, burn 8s with -15% spirit resist | T3 +33% effectiveness (barrier, burn, silence) | CombatBarrier 90 (+0.7x), burn 12/s (+0.152x) |
| Baba Threadsap | 28 (T2 -12), T3 +1 charge | explode 0.9s | 35m, burst 3.5m | T3 on hit pulls enemies 7m over 0.6s | - | - |
| Baba Granny Long Legs | 32 (T2 -7) | 10s | Radius 8m | Heavy melee ground pound: knock up 0.3s, 50% slow 4s, 75 (+0.6x) | T3 +15 resists | 0.6x |
| Ivy Kudzu Connection | 37 (T3 effectively always on) | 12s, range 16m, min connect 2s | line of sight needed | Ally receives BonusFireRate, BulletLifestealPercent, move-while-shooting; Ivy receives 50% when not connected. TetherSharedHealPct 35 (+0.85x per level boon, not spirit) = replicated healing | BonusFireRate 10 (+0.18x), lifesteal 15%; T2 +8 and +8; T1 +2m | 0.18x fire rate |
| Ivy Entangling Thorns | 32 | 4s, cast 0.2 | 6m (T2 +2) | Slow 28%; T3 immobilise after 2s inside for +1.6s | DPS 40 (+0.55x), T2 +0.5x | 0.55x |
| Ivy Stone Form / Air Drop | 40 / 100 | Air Drop 21s carry | 22m | Ally lifted cannot attack and deals -20% damage; explosion 115 (+0.7x), r 16-20m, T3 silence | T1 barrier 300 | - |
| Solomon Kingside Knight | 25 (T1 -8 = 17) | 7s barrier, cast 0.15 | cast 28m; Move 13m with invulnerability, move CD 10 | Barrier on ally (double on self-cast as king, no stamina). T3 two allies within 20m and self debuff removal on move | CombatBarrier 80 (+0.8x), T2 +80 and +1 stamina | 0.8x |
| Solomon Setup Bishop / Rook Battery | 12 / 33 | bishop slow 30% fading, rook immobilise 1s (T3 +0.5) | 20m / 12m | Slow and rook immobilise setups | Bishop DPS 30 (+0.7x); Rook 50 (+1.3x), CombatBarrier 100 | see table |
| Rem Tag Along | 40 (T1 -8) | AbilityDuration 5.5, cast 0.5 | 23m | Rem jumps onto an ally, both get burst MissingHealthBurstPct 15 (+0.03x) then HealingPerSecond 42 (+0.4x) for 2s; Rem follows wherever the ally goes (attached); knocked off by stun from an ultimate | T2 +35% barrier, item range, duration while napping; T3 +15% and +35 spirit; healing scaling +0.34x, burst +0.016x | heal 0.4x (0.74x T3) |
| Rem Pillow Toss / Lil Helpers / Naptime | 25 / - / ult | Pillow slow 36% 3s, r 5m; helpers burst heal | - | Pillow hit reduces other CDs 5s; Naptime 19m sleep after 1.9s channel | Pillow 75 (+1.6x) | - |

## 3. Interaction questions (per pair)

Q1 Does partner healing/shield stack with the brawler's own, and spirit scaling:
- Heals are separate HoT/barrier sources (BonusHealthRegen, HealAmount, HealingPerSecond, CombatBarrier); nothing in the files caps or de-duplicates them. Per-point spirit: Kelvin grenade +0.8 heal, Shelter +0.2 (+1.2 at T3), Dynamo Aurora +0.4/s, Rem +0.4/s (0.74 T3), Solomon barrier +0.8, Baba barrier +0.7. Brawler self-heals do not scale off partner spirit; they scale off the brawler's own (Yamato 1.036, Victor Jumpstart 1.2, Abrams 0.6 damage-based drain).
- Result: VERIFIED that scaling uses the partner's spirit, UNVERIFIABLE-FROM-FILES that heal sources add rather than overwrite (e.g. does a barrier replace or add to a barrier). Sandbox: brawler at 50% HP, apply Dome plus Aurora plus own heal; log HP per second and barrier total.

Q2 Do partner slows/zones keep enemies inside the brawler's 8-9m aura:
- Victor Radius 8m (9m T3). Kelvin Arctic Beam max slow 16-20% plus Victor's 20% do not stack to a hold: enemies still move; slows reduce speed but nothing pins them. Dynamo Singularity pulls enemies in to Dynamo at VacuumRadius 7m (9m T1) for 2.75s channel; if Victor stands within about 1m (8m radius minus 7m) to 2m of Dynamo, every pulled enemy ends inside Victor's 8m aura (and the 3.5s pull + aura is a 2.75s of 8s channel overlap). Baba Threadsap T3 pull 7m over 0.6s lands enemies 7m closer; fits in Victor's 8m if cast from near Victor. Solomon rook immobilise 1s (T3 1.5s): hold, but only 1-1.5s of the 8s ramp. Ivy Thorns T3 immobilise 1.6s after 2s inside. Frozen Shelter dome 10m x 1.15 and slow 28%: dome encloses an 8-9m aura fully if centred on the brawler, but whether enemies inside are trapped, pushed out (EnemyDragSpeed 1000) or frozen (-100% time-scale modifier exists) is UNVERIFIABLE-FROM-FILES. Sandbox: Victor in Shelter with 2 enemy dummies; record if they are pushed out, whether Aura ticks reach them, and whether the freeze_debuff applies.
- Aura damage ramp time MinDPS to MaxDPS is not given in the stat list (UNVERIFIABLE): measure seconds-to-max in sandbox; if the ramp is about 4s, only holds of 1-2.75s keep the ramp from restarting only if the ramp resets on leaving radius (also unverifiable).

Q3 Which partner effects follow a diving brawler:
- Follows: Rem Tag Along (23m, duration 5.5s, attached: dives with the brawler; knocked off by an ultimate stun); Ivy Kudzu (16m line of sight, 12s, bonuses at 50% when unconnected; min connect 2s); Kelvin Ice Path (18s aura, radius 5m, but a fixed trail, not following); Solomon Knight barrier (7s on the ally wherever he goes; Move 13m can reposition him; 28m cast).
- Does not follow: Baba Brew (thrown at 12m, fixed area 6-9m, cycle 2.5/3.5/4.5s); Dynamo Aurora (5s channel, 8m share, follows only if Dynamo follows; T3 no channel but still 8m); Kelvin grenade (fixed cloud 4s).
- Dive times: Abrams charge 1.4s covers about 30m+, outruns Aurora/Ice Path; Abrams leap stuns 1.6s (2.4 T2) at 9m; Billy ram 0.3s; Billy Chain Gang pulls 4m over 0.8s; Yamato Flying Slash 26m (41m T3, cast 0.2). Shelter dome position when cast on a moving ally (does it follow?) is UNVERIFIABLE; sandbox: cast on a running dummy, check whether dome stays or travels.
- Arithmetic: Rem 5.5s attach covers Abrams charge 1.4s + Siphon 4s = 5.4s (0.1s spare). Dynamo Singularity 2.75s (plus 0.2 cast) + Victor aura 8s: only 2.95s of 8s. Billy Chain Gang pulls over 0.8s inside a 2.8s hold, Kelvin Shelter lasts 5s (6.5s T2) vs 2.8s chain = 2.2s spare to bash.

## 4. Verdicts per pair (arithmetic only)

| Pair | Verdict | Reason |
|---|---|---|
| Victor + Dynamo | SURVIVES (needs test) | Singularity pulls into Victor's 8-9m aura; Aurora heals Victor's SelfDPS; Dynamo Pulse -15% resist stacks with aura +15% damage taken |
| Victor + Kelvin | SURVIVES (needs test) | Shelter regen 90-155/s covers aura self-damage, slow; zone behaviour unverified |
| Victor + Baba | SURVIVES | Brew barrier 90 (+0.7x) absorbs aura self-damage; Threadsap T3 pull 7m lands in aura |
| Victor + Rem | MARGINAL | Rem attach 5.5s fits a 8s aura channel only once refreshed; Rem items apply on Victor |
| Victor + Ivy / Solomon | MARGINAL | Ivy gives fire rate not zone; Solomon barrier 80+ 7s covers one aura cycle |
| Abrams + Rem | SURVIVES | Rem rides the charge, 5.4s window of 5.5s |
| Abrams + Dynamo / Kelvin | MARGINAL | Siphon radius 8m inside Shelter 10m; Aurora does not follow the 30m charge |
| Billy + Kelvin / Baba / Solomon | SURVIVES | Chain Gang 2.8s hold fits inside Shelter 5s and Brew barrier 8s; Solomon rook immobilise stacks hold |
| Yamato + Solomon / Rem | MARGINAL | Yamato grapples to ally (T3) so he follows partner, partner does not follow him |
| Anything with Ice Path as the follow tool | DIES | Trail is a fixed 8s path, not attached |

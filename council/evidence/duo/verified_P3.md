# P3 verified: spirit-resist shred and damage zones

Sources: `ab.py` / abilities.vdata (class in brackets), `tier.py`/`tier2.py` (per-tier upgrade lists read from m_vecAbilityUpgrades; tiers are T1/T2/T3 = 3 entries), localization citadel_heroes_english.txt, items via `audit_D_q.py`. AP cost to reach T3 = 1 unlock + 1 + 2 + 5 = 9 AP (T1 = 2 AP total, T2 = 4 AP total).
S = spirit power. "x S" = the `(+k x ETechPower)` scale.

## 0. Headline corrections to stage A

| Stage A claim | Verdict | Evidence |
|---|---|---|
| Graves "Borrowed Decree stacking spirit-resist reduction" | REFUTED | The stacking debuff (`MaxStacks 40`, `StackDuration 5`, `TechArmorDamageReductionPerStack -0.5`, `SlowPercentPerStack 0.5`) is a leftover copy of the removed **Wither & Die** (`ability_necro_wither`, same values, MaxStacks 40, StackDuration 4). `ability_necro_wither` is not in hero_necro slots (heroes.vdata: hauntingskull, zombiewall, fear, gravestone). In `ability_necro_gravestone` the 3 stack properties are never registered by any modifier (the gravestone/aura modifiers register nothing, zombie summon modifier registers only BonusHealthRegen and MoveSpeedPercent) and are absent from its tooltip (Active tooltip lists SummonHealth, SummonMeleeDamage, SummonLifetime, SlowDuration, ExplosionRadius, SummonFrequency, Damage, StatusEffectStun, SlowPercent, BonusHealthRegen, MoveSpeedPercent). Loc text desc_1/desc_2 mention ghouls, explosion damage and a brief slow only. |
| Seven Power Surge T3 = -15% spirit resist | VERIFIED | `TechResistDebuff -15` (T3), `DebuffDuration 10` (T3), registered as `MODIFIER_VALUE_TECH_RESIST_REDUCTION` on `modifier_power_surge_debuff`. |
| Paige Read T3 = -18% spirit resist, 6s | VERIFIED | `TechArmorDamageReduction -18`, `DebuffDuration 6` (T3), `MODIFIER_VALUE_TECH_RESIST_REDUCTION` on area-modifier debuff. Loc: "On Hit: Reduce Spirit Resist by X% for Ys". |
| Paige Bookwyrm / Mina Rake carry a resist debuff | REFUTED | `TechArmorDamageReduction` exists on both but base value 0 and no upgrade touches it (vestigial). |
| Paradox Pulse Grenade shreds | REFUTED in current data | Loc has "Spirit Resist Down" string but the ability has no resist property (only `TechPower`); its amp is "for Paradox against the victim" (caster-only). |
| Napalm T3 +16/17% amp helps a partner | REFUTED by name | `IncomingDamagePercentFromCaster 16 (+17 T3)`: from Infernus only. Same for Geist Malice (loc: "damage they take from you"), Paradox grenade amp, Pocket Barrage amp (Pocket's own). |

New find: Graves **Essence Theft** [ability_necro_fear] is the only spirit-resist number in his kit (see 1.3).

## 1. Carrier abilities

### 1.1 Seven (hero_gigawatt)

| Ability [class] | Cooldown | Duration / radius / cast | Mechanic | Spirit scaling | T1 | T2 | T3 |
|---|---|---|---|---|---|---|---|
| 3 Power Surge [ability_power_surge] | 50 | self buff `AbilityDuration` 10; cast delay 0.2; `ChainRadius` 10m, `ChainCount` 4, `ChainTickRate` 0.2 | Bullets proc shock on target, once per burst shot, bounces to enemies within 10m. Debuff `modifier_power_surge_debuff` carries the resist reduction (T3 only). Buff `m_bDurationExtendible = true`. Damage is the caster's chain damage. | `DamagePerChain` 10 (+0.14 x S); `BonusPerChain` 10 (+0.32 x S) | CD -18 (=32) | +3m move speed, +8 `BonusPerChain`, +8 `DamagePerChain`, +0.23 x S to both | `TechResistDebuff` -15, `DebuffDuration` 10 (debuff lasts 10s; buff `AbilityDuration` +10 = 20s) |
| 2 Static Charge [citadel_ability_static_charge] | 42 | cast range 15m; `ShockDelay` 3.5; `ShockRadius` 5m; `StunDuration` 0.9 | Delayed AoE stun + damage, not damage-broken (fuse is on target) | `Damage` 35 (+0.79 x S) | CD -20 (=22) | radius 7m, cast range +5 (=20m) | stun +0.9 (=1.8s), damage +160 |
| 1 Lightning Ball [citadel_ability_lightning_ball] | 26 (6 between charges) | `ShockRadius` 4.25m, lifetime 5, `TickRate` 0.1 | slows itself on hit; target slow only from T2 | `DPS` 75 (+0.5 x S) | +1 charge | `SlowPercent` 28, lifetime +1 | `DPS` +58.5, radius +1.75 (=6m) |
| 4 Storm Cloud [citadel_ability_storm_cloud] | 205 | channel 7; radius 10m -> 30m over `ExpandTime` 3.5; tick 0.3; needs LOS | Zone, Seven stationary (`FlightControlEnabled` 1.5m) | `DPS` 95 (+0.6 x S); strike 75 (+0.5 x S), 7m radius, 0.25s delay, knockback force 500, one per cast | `BulletResistOnActive` 55 | radius +10 (final), initial +5, channel +7 (=14) | `DPS` +65 (=160), flight 4m |

Power Surge arithmetic at T3: buff 20s / cooldown 32s = 62.5% buff uptime (assuming cooldown starts on cast; unverified). Debuff lingers 10s after last hit, so covered window per cast up to 30s if Seven keeps hitting the same target.

### 1.2 Paige (hero_bookworm)

| Ability [class] | Cooldown | Duration / radius / cast | Mechanic | Spirit scaling | T1 | T2 | T3 |
|---|---|---|---|---|---|---|---|
| 3 Captivating Read [ability_bookworm_aoemagic] | 30 | range 30m; radius 7.5m; cast delay 0.15; `DetonationDelay` 1.25; `Height` 8m | Placed area: slow (`SlowPercent` 36) during the delay, detonation does damage + **root** (`modifier_bookworm_immobilize`, `ImmobilizeDuration` 1.0). Resist debuff applied "On Hit" for `DebuffDuration`. Duration values scale with `ETechDuration` (`scale_function_tech_duration`). | `Damage` 90 (+1.3 x S) | CD -14 (=16) | root +1 (=2.0s) | `TechArmorDamageReduction` -18, `DebuffDuration` 6, radius +2 (=9.5m) |
| 1 Bookwyrm [ability_bookworm_dragonfire] | 33 (7 between charges) | range 20m, radius 4m, trail 3.0s, tick 0.3 | burning trail; no resist value (vestigial property 0) | hit 60 (+1.3 x S); `DPS` 30 (+0.3 x S) | CD -12 | trail +2, radius +1, +1 charge, +100 dmg, +30 DPS | range +12 |
| 4 Rallying Charge [ability_bookworm_knightcharge] | 210 | map-wide; stun 1.0 | heal/speed allies in 4m | 125 (+1.0 x S); heal 125 (+1.6 x S) | heal +150 | CD -45 | stun +0.5, damage amp +70 |

Read arithmetic at T3: debuff window 6s per 16s cooldown = 37.5% uptime on a target that stays inside 9.5m. Root 2.0s (T2) sits inside the first 2.0s of the 6s window (hit at t, root t..t+2, shred t..t+6).

### 1.3 Graves (hero_necro)

| Ability [class] | Cooldown | Duration / radius / cast | Mechanic | Spirit scaling | T1 | T2 | T3 |
|---|---|---|---|---|---|---|---|
| 2 Grasping Hands [ability_necro_zombiewall] | 34 | range 24m; wall 14m long, `AuraRadius` 0.75m; `ZombieWallDeployTime` 0.6; `GroundAuraPopDelay` 1.1; wall `AbilityDuration` 5 | Enemies walking through get root (`modifier_citadel_root`, `ImmobilizeDuration` 1.0, `TetherDuration` 1) + slow 40% for `DebuffDuration` 0.5. Caster's damage only. | `Damage` 90 (+1.6 x S); length +0.05 x S | duration +2 (=7s) | +90 damage, length +10m (=24m) | root +0.75 (=1.75s), +1 ghoul, CD -14 (=20) |
| 4 Borrowed Decree [ability_necro_gravestone] | 140 | range 20m; `AuraRadius` 8m; `AbilityDuration` 16; up to 3 stones; knockup radius 4m (`KnockupSpeed` 240); ghoul explosion 6.5m; `SlowPercent` 64 for `SlowDuration` 1.25; ghoul every `SummonFrequency` 4s; `GravestoneHealth` 100 (two heavy melees) | Zone producing ghouls that explode; slow + knockup on target. No resist reduction, no damage amp (see section 0). | `Damage` 115 (+1.27 x S); `SummonMeleeDamage` 40 (+0.5 x S) | CD -15 (=125), ghoul speed +25% | +10s (=26), spawn 3.7s | +5% current health on death |
| 3 Essence Theft [ability_necro_fear] | passive | `ShootDurationForMax` 4s of shooting the same target; `ProgressLossPerSecond` 1 (x`ProgressLossMultiplier` 2.3 after `DelayBeforeLoss` 0.5); `MaxStolenTargets` 3 | "Your weapon steals weapon damage and spirit resist over time, up to a maximum per target". `MaxStolenSpiritResist` 10 (css `tech_armor_down`), `MaxStolenAttackDamage` 25 (+0.25 x S). Buildup is on Graves' weapon (`modifier_necro_rampup`, overhead for caster only). | attack damage part only | spirit resist +5 (=15) | attack damage +20 | +1 target (=4), summons also apply |

Essence Theft: whether the 10-15% is removed from the enemy (usable by partners) or granted to Graves is UNVERIFIABLE from files (css class suggests enemy-side, "steals" suggests thief-side). If enemy-side it costs 2 AP for 15% versus 9 AP for Seven/Paige, but needs Graves shooting the same target for 4s.

## 2. Interaction questions

| Question | Verdict | Evidence / test |
|---|---|---|
| Q1a. Do resist reductions from different sources stack? | UNVERIFIABLE-FROM-FILES (engine code). Data shows all use the same type `MODIFIER_VALUE_TECH_RESIST_REDUCTION`: Power Surge -15, Read -18, Mystic Vulnerability -8 (+ -10 upgrade, 7s), Tech Shredders -8 (+ -10, 8s), Escalating Exposure -8, Spirit Snatch -12, Acolyte's Glove -6, and "MagicResistReduction" items (Spirit Sap -9, Focus Lens -9, Banshee Slugs -16). Same-name check: Seven and Paige use different property names and different modifiers, so they are not the same-source refresh case. | Sandbox S3-1 below. Models for the ratio of damage taken (vs no shred), target resist R: |
| Q1b. Additive vs multiplicative | UNVERIFIABLE; models differ a lot above R=20 | A = percentage points off R; B = each reduces the remaining resist by that fraction (R x (1-0.15) x (1-0.18)); C = independent damage amps. R=0: A 15% / 18% / 33% both, B 0, C 15% / 18% / 35.7%. R=20: A 18.7 / 22.5 / 41.2, B 3.7 / 4.5 / 7.6, C 15 / 18 / 35.7. R=40: A 25 / 30 / 55, B 10 / 12 / 20.2, C 15 / 18 / 35.7. Distinguish with a dummy at R=40: Both gives x1.55 (A), x1.20 (B), x1.357 (C). |
| Q2. Do shreds apply to ALLY spirit damage? | Structurally VERIFIED (not engine-confirmed). | The value is a plain target-side stat registered by a debuff modifier with no caster property; contrast `IncomingDamagePercentFromCaster` (Napalm), loc "damage they take from you" (Malice), "your SpiritDamage" (Escalating Exposure), and Tech Shredders loc "reduces the Spirit Resist of the target and grants **you and your allies** lifesteal" (item text names allies only for the lifesteal). Confirm with S3-2. |
| Q3a. Do zones (Wall, Decree, Storm Cloud) amplify allies' damage? | REFUTED | None of Grasping Hands, Decree, Storm Cloud carries a resist/amp value that is registered (Decree's stack values are orphaned; Storm Cloud has only `DPS`, `LightningStrike*`, `BulletResistOnActive` to Seven). Their damage is the caster's own. |
| Q3b. Do zone CC effects help allies? | VERIFIED | Root/slow/knockup are modifiers on the target: Wall root 1.0 (1.75 T3) / slow 40%; Decree slow 64% 1.25s, knockup radius 4m; Storm Cloud strike knockback 500 (pushes enemies out of the cloud, which is anti-synergy with a clumping partner). |
| Q3c. Does damage break the root? | UNVERIFIABLE | Root is `modifier_citadel_root` (Read and Wall); no damage-break flag in data. Test S3-3. |
| Q4. Timing: shred duration vs partner burst | See section 3. | Arithmetic only. |

## 3. Window arithmetic (Paige 6s / Seven 10s-20s) against partner bursts

Spirit damage a partner deals to one target in one rotation, raw (no hit-rate, no resist). Numbers T0 unless noted; `x S` as above.

| Partner | Sources (class) | Raw spirit damage per rotation | Cooldown / timing | Fits Paige 6s? | Fits Seven 10s? |
|---|---|---|---|---|---|
| Infernus | Napalm [ability_incendiary_projectile] 40 (+0.6 x S), cd 25; Afterburn [ability_afterburn] DPS 14 (+0.66 x S), burn 3s refreshed; Flame Dash trail [ability_flame_dash] DPS 30 (+0.7 x S), 4s, radius 4.5m, cd 38; Fire Bomb [ability_fire_bomb] 125 (+0.97 x S) (+100 T1), cd 190 (-65 T2), fuse 3.25, stun 1.25 (+0.9 T3), radius 12 (+10 T3) | ~425 + 11.0 x S over 10s (Afterburn 10s + trail 4s + Napalm + bomb) | Read hit tr+1.25, bomb lands tb+3.25: needs tb-tr in [-2.0, +4.0] for the bomb to be in the 6s window | Yes, 6.0s of slack on cast order; Afterburn covers 6s (84 + 3.96 x S) | Yes, full rotation |
| Pocket | Barrage [synth_barrage] 4 x (32 + 0.465 x S), channel 2s, cd 32 (-16 T2); Pulse [synth_pulse] 65 (+1.1 x S), cd 17; Affliction [synth_affliction] DPS 32 (+0.21 x S) tick 0.5 for 10s (+3 T2), radius 9 (+4), cd 170 (-35 T1) | ~513 + 5.1 x S | Affliction 10s DoT: Paige covers 6 of 10s (60% of ticks: 192 + 1.26 x S); Seven covers all 10s if debuff is up at cast | Barrage + Pulse yes; Affliction 60% | Yes |
| Paradox | Pulse Grenade [citadel_ability_chrono_pulse_grenade] 4 pulses x (35 + 0.3 x S), 0.8s apart, duration 3.2 (+1.6 T3 = 6 pulses), cd 32 (-12 T1); Swap [citadel_ability_chrono_swap] 150 (+1.1 x S), cd 110 (-30 T2), swap time 0.6-1.0s. Carbine is bullet damage (not shredded) | ~290 + 2.3 x S | Grenade 3.2s + Swap 1.0s = 4.2s fits 6s with 1.8s spare | Yes | Yes |
| Mina | Nox Nostra [ability_vampirebat_batswarm] 75 x (4.6 + 0.094 x S) at 30 bats/s = 2.5s release, `MaxBatTargets` 2, cd 150 (-45 T2); Love Bites [ability_vampirebat_lovebites] 45 (+1.85 x S) burst (needs build-up from damage, per-target cd 10, -5 T3), bullet 4 (+0.09 x S) | ~390 + 8.9 x S | Release 2.5s + one Love Bites inside 6s: 3.5s spare; lock-on cone 20deg needs target held (Read root 2.0s covers 80% of release) | Yes | Yes |
| Kelvin | Beam [ability_icebeam] DPS 45 (+0.38 x S) for 5s (T2 +20, +0.6 x S), cd 28; Grenade [ability_ice_grenade] 60 (+0.6 x S) (+30 T1), 2 charges 7s apart | ~285 + 2.5 x S | Beam 5s starts at root, fits 6s with 1s spare | Yes (needs beam start within 1s of hit) | Yes |
| Viscous | Splatter [viscous_goo_grenade] 55 (+0.7 x S); Goo Ball [viscous_goo_bowling_ball] 110 (+1.0 x S) per tick 0.25 (hit count unverified), stun 0.5; Puddle Punch 20 (+0.6 x light melee) | ~165 + 1.7 x S (Goo Ball counted once) | Goo Ball cd 150 and 11s duration | Yes | Yes |
| Geist | Essence Bomb [ability_blood_bomb] 90 (+1.22 x S), arming 0.65, radius 7 (+2); Life Drain [ability_life_drain] 24 (+0.3225 x S)/s x 2.5s; Malice [ability_blood_shards] 3 x (23 + 0.558 x S), 5 stacks | ~219 + 3.7 x S | Yes (all < 4s) | Yes | Yes |

Absolute gain per rotation from one shred = s% x raw (model A at R=0). Example, S=0: Seven 15% on Pocket = +77; Mina +59; Infernus +64; Kelvin +43; Paradox +44; Geist +33; Viscous +25. Paige 18% x the 6s-covered share is lower for DoT-heavy partners (Pocket Affliction 60%).

## 4. Pair verdicts (arithmetic only)

| Carrier | Surviving partners | Dying / weak | Reason |
|---|---|---|---|
| Graves (Decree/Wall) | none via Decree | all, as a shred source | No shred in Decree; zone CC only. Essence Theft (15% at T1, 2 AP, up to 4 targets) is UNVERIFIABLE until S3-2b says enemy-side. |
| Seven (Power Surge T3, 9 AP) | Pocket (10s Affliction fully covered), Mina (Nox Nostra), Infernus, Kelvin, Paradox, Geist | Viscous (raw spirit ~165 + 1.7 x S, gain ~25 per rotation at S=0 vs 77 on Pocket) | All fit the 10s debuff + 20s buff window; ranking is by raw shreddable spirit. Storm Cloud pushes enemies out of its own radius (knockback 500) and does not carry shred. |
| Paige (Read T3, 9 AP) | Mina, Infernus (Fire Bomb order slack 6.0s), Kelvin, Pocket (Barrage + Pulse), Paradox | Pocket Affliction only 60% covered; Viscous weak | 6s window per 16s cooldown (37.5%); Read root 2.0s helps Mina's cone lock and Kelvin's 1.1m beam. |
| Seven + Paige together | arithmetic only | n/a | -15 -18 = -33 if additive (+55% at R=40) or about +20% if B; Q1 decides. |

## 5. Sandbox scenarios to settle the open items

- S3-1 stacking model: dummy enemy with measured spirit resist R=40 (item loadout, read via damage numbers), one repeatable spirit hit (Kelvin Frost Grenade or a fixed-damage ability). Arms: no shred / Seven T3 / Paige T3 / both. Read ratio vs none: A 1.55, B 1.20, C 1.36 (both arm).
- S3-2a ally application: same dummy, Seven or Paige applies shred, an ALLY (separate account or ally bot) lands the same spirit hit. Expect ratio 1.25 (Seven alone at R=40) if ally-applied.
- S3-2b Graves Essence Theft: Graves shoots dummy 4s with T1 on the 3 (stack 15%), partner lands spirit hit; compare ratio to no-Graves hit. Also read Graves' own spirit resist in the stat screen.
- S3-3 root break: Paige Read T2 root 2.0s on a dummy that takes ally damage; check whether it ends early. Same for Graves Wall root.
- S3-4 duration/refresh: Seven T3 debuff after Power Surge ends (20s buff + 10s tail?) and whether the debuff refreshes on each shot; measure time until a probe spirit hit drops back to base ratio.
- S3-5 Decree control: enemy stands 16s in Decree, probe spirit hit at start and at 10s (expect ratio 1.0, confirming the orphaned stack values).

## 6. Not verifiable from files
Whether cooldown starts at cast or at buff end (Power Surge, Read); whether Seven's debuff lands on chain-bounce targets or only on the shot target; whether Essence Theft is enemy-side; whether root breaks on damage; Goo Ball hit count per second.

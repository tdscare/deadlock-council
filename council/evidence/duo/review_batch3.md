# Blind review, duo batch 3 (reviewer, 2026-10-22)

Sources: abilities.vdata build 6795 (raw blocks incl. scale functions and m_vecAbilityUpgrades), citadel_heroes_english.txt, `audit_D_q.py`, RULES_KIERAN.md, CHECKLIST.md, bases in council/work/b3base (diffed with rv2/diff.js). designs_batch3.json was read last. No sandbox results exist (council/sandbox/results is empty), so every partner interaction is untested.
Tools: walk1 FLAGS none on all 7. check.js CHECK12 none on all 7. sp.js run on all 7 and on their bases.

## Delta vs base (what the duo actually changes)
| build | base | change |
|---|---|---|
| mokrill_duo_bebophook | mokrill | Colossus out, Spirit Burn into Late (sells Healbane); order 1132124422133434 → 1132124424421333 (Combo T2/T3 at 7.2k/11.2k) |
| bebop_duo_mohook | bebop_bomb | **order only** 2231244413243311 → 2231244334324111 (Grapple T3 31.2k → 13.6k) |
| doorman_duo_push | doorman | Compress Cooldown Call Bell → Luggage Cart; Cart T3 16.8k → 10.4k, Call Bell T3 10.4k → 16.8k |
| venator_duo_doorman | venator | Warp Stone → Duration Extender on Snap Trap, + Superior Duration (46.4k), Phantom Strike out of rich; Snap Trap T3 one point earlier |
| graves_duo_doorman | graves_ult | Duration Extender Decree → Grasping Hands; Hands T3 one point earlier (9.6k) |
| pocket_duo_shiv | pocket | Mystic Expansion Barrage → Affliction |
| shiv_duo_pocket | shiv | **order only** (Killing Blow T2/T3 at 7.2k/10.4k, base T3 at 49.6k) |

## Verified mechanics (file lines)
- **Combo** (ability_ult_combo): cd 150, T2 -30 → 120 and +50% bullet resist, T3 +0.7 channel (2.4 → 3.1) +40 DPS +0.4x (80 + 1.0x SP). AbilityChannelTime scale = [EChannelDuration, ETechDuration]. `m_bitsInterruptingStates = MODIFIER_STATE_STUNNED` only. **ChannelMoveSpeed = 0**: Mo is stuck for the whole hold. Target drag: modifier_drag_custom, EDragOffset_WorldFixed, EDragPull_SpringDamped, m_flTargetPosDistance 100, **m_bChaseAtLeastSourceSpeed = false**.
- **Grapple Arm** (citadel_ability_hook): range 30m (T2 +30m), cd 23 (T3 -11.5), cast delay 0.1, HookImpactDelay 0.5, projectile 2850, m_flReturnSpeed 2000 (with a PullSpeedScaleCurve), FriendlyHookIgnoreRange 8m, hits the first hero/trooper/neutral in its path. modifier_citadel_hooktarget `m_nEnabledStateMask = ""`; the slow modifier gives movement-input/dash disabled, **no STUNNED**. ResetCooldownOnFriendlyHook 0.
- **Luggage Cart**: cd 30, T3 -15 → 15; T2 +25m range, +75 (+0.6x) wall damage; **T3 "StunDuration 1.25s Stun on wall impact"** (loc `ability_doorman_luggage_cart_t3_desc`, StunDuration tech_duration-scaled). Projectile speed 1000, PROJECTILE_PASS_THROUGH_WORLD.
- **Doorway**: m_bUseWallPlacement true, m_bPlaceNormalToSurface true: doors sit on walls. VERIFIED.
- **Snap Trap**: 2 charges (3 at T3), cd 28 → 17 (T1), arm 0.5, radius 2m, lifetime 30, root 1.25 +1.0 (T2), ImmobilizeDuration ETechDuration. **Gutshot**: WallStunDistance 7m, stun 0.6 +0.4 (T2), tech_duration-scaled.
- **Grasping Hands**: cd 34 → 20 (T3), duration 5 +2 (T1) ETechDuration, deploy 0.6 + GroundAuraPopDelay 1.1 = 1.7s to arm (VERIFIED), immobilize 1.0 +0.75 (T3) tech_duration, **AuraRadius 0.75m, TickRate 0.1**.
- **Borrowed Decree**: AbilityDuration 16 with `scale_function_multi_stats`, `m_vecScalingStats = [ "ETechPower", "ETechDuration" ]` (0.04 x SP). It scales with spirit power AND ability duration (same structure as Combo's channel). AuraRadius 8m (tech range), SlowPercent 64, SlowDuration 1.25, TickRate 0.4; "Enemies can destroy the gravestone with two heavy melees" (loc), GravestoneHealth 100.
- **Affliction**: cd 170 → 135 (T1), DebuffDuration 10 +3 (T2, ETechDuration), Radius 9 +4m (T2, ETechRange), T3 +13 DPS +0.1x (45 + 0.31x) and DisableHealing. "non-lethal and does not apply item procs" (loc). VERIFIED.
- **Killing Blow**: cd 145, T2 -25 → 120 (96 with Superior Cooldown), EnemyHealthPercent 18 (+3 buffer), T3 +10 → 28. RecastWindow 16 (ETechDuration). FailedExecuteCooldownPenalty 30. VERIFIED.
- **Upgrades go global**: Superior Cooldown "Reduces the Cooldown of your abilities", Superior Duration "Increases the duration of your abilities and items", Greater Expansion "...of your abilities and items". When the imbue's upgrade is bought, the imbue target stops mattering.

## Interaction answers
- Hook stuns Mo? **REFUTED**: no STUNNED on hook target or slow modifier; Combo only breaks on STUNNED. Channel is not broken by flags.
- Mo stuck? **VERIFIED**: ChannelMoveSpeed 0.
- Hook arrival vs hold: 20m = 0.1 + 0.28 + 0.5 + 0.39 = 1.27s (+0.3 reaction = 1.57); 30m = 1.6 (+0.3 = 1.9). T3 3.1s: fits with 1.2 to 1.5s spare. Base 2.4s: 0.5 to 0.8s spare, fails the 1.5s bar. Arithmetic OK. It assumes 39.4 units/m and a linear reel (the PullSpeedScaleCurve isn't linear).
- Held target comes with Mo? **UNVERIFIABLE, and the file argues against it**: the Combo drag is SpringDamped with m_bChaseAtLeastSourceSpeed = false, so at a 2000 u/s reel the target is not required to keep up. Sandbox duo_b3_mo_bebop_hookout decides it.
- Cart onto Snap Trap / through doors: **UNVERIFIABLE** (does a root stop the cart drag? does the cart pass portals?). Trap 2m radius at 25 m/s is about 0.16s inside, so it triggers, but the root may be overridden by the drag.
- Cart into wall + Gutshot: **VERIFIED from files**: Cart T3 wall stun 1.25s, then the target is at a wall, so Gutshot stuns 1.0s (T2). 2.25s of stun from the two kits, no trap needed.
- Cart through Grasping Hands: **high risk**: 0.75m aura and a 0.1s tick against a 25 m/s drag means about 0.06 to 0.1s inside the line, so 0 or 1 ticks. Root not guaranteed. UNVERIFIABLE.
- Decree duration "tied to spirit power so Duration Extender does nothing": **REFUTED** (ETechDuration is in m_vecScalingStats).
- Shiv 18 → 28% and 16s recast: **VERIFIED**. Affliction 13s × 1.22 (Pocket's Duration Extender) = 15.9s, then 16.6s with Superior Duration: covers the recast window.

## 4.8k-per-colour policy (final core, walk1; Mercurial Magnum = gun)
| build | gun | spirit | health | result |
|---|---|---|---|---|
| mokrill_duo_bebophook | 0 (Mercurial Magnum only in rich) | 43.2k | 4.8k (6.4k → 4.8k after selling Healbane at 36k) | FAIL gun (inherited) |
| bebop_duo_mohook | 0 | 38.4k | 12.8k | FAIL gun (inherited) |
| doorman_duo_push | 1.6k | 32.0k | 11.2k | FAIL gun (inherited) |
| venator_duo_doorman | 16.0k | 16.0k (4.8k at 23.2k) | 14.4k | OK |
| graves_duo_doorman | 3.2k (Heroic Aura) | 40.0k | 9.6k | FAIL gun (inherited) |
| pocket_duo_shiv | 4.8k (after selling Restorative Shot) | 25.6k | 14.4k | OK |
| shiv_duo_pocket | 0 | 35.2k | 12.8k | FAIL gun (inherited) |

---

## Pair B3-1 Mo & Krill + Bebop: DROP

### mokrill_duo_bebophook: REVISE
- Spirit Burn (Late, sells Healbane). Why not keep Colossus? Spirit Burn procs: Combo T3 at 36k = 80 + 164.1 = 244 DPS × 3.1 = 757 (≈590 after 30% resist) vs 500 in 5s. OK. It also replaces Healbane's -35% with -70% on the held target. But Colossus (35% bullet/spirit resist for 7s, 24% slow in 14m, cd 37) covers every Combo, and the hook only covers the ones where Bebop is 8–30m behind with a clear line. Removing it leaves health at **4.8k from 36k to the end** (base 10.4k). That breaks "then more health" and the in-your-face rule, all on an untested hook. **FAIL (E)**. Evidence: walk1 `Spirit Burn s4 | souls 36000 | ... health 4800`.
- Order (Combo T3 at 11.2k). Why not the base seemeta order? The 3.1s hold is the only version that fits the hook with ≥1.5s spare (2.4s: 0.83s). Cost: Burrow T3 11.2k → 16.8k, Scorn T3 14.4k → 24.8k. The arithmetic holds, but only if the target follows Mo, and the drag flag above argues it may not. Conditional OK, sandbox owed.
- Gun 0: FAIL on the policy. Fix: Mercurial Magnum (counts as gun, upgrade of the owned Quicksilver Reload) into core.
- Unchanged items, notes and counters: OK, same as the live build. The Counters X/Y (Fortitude, Torment Pulse) are in the build, and the counters desc matches the 81 live builds. Name "Grab And Go Mo" (25) and desc "Duo Mo for Bebop": OK.

### bebop_duo_mohook: DROP
- Only the ability order changes; no item changes. Why rush Grapple T3 (cd 23 → 11.5)? The design's own reason ("back long before Mo's 120s Combo") is already true at 23s: 23 < 120. **The rush gains nothing for this combo** and costs Sticky Bomb T3 (10.4k → 16.8k) and Hyper Beam T3 (16k → 24.8k) on a bomb build. T2 (+30m range) is irrelevant to the hook-out, because at 30m the hook already fits. **FAIL (Kieran's bar: the build must change for the partner, with a gain)**. The changes log's "base: last-maxed, ~45k" is false: base Grapple T3 is at 31.2k (sp.js).
- This is the "rescue hook" pattern consideredDropped rejected for Lash + Bebop, and the same "order only" reason it used to drop Warden. Inconsistent.
- Gun 0: FAIL on the policy (inherited).
- Pair: Bebop gets no real change and Mo pays all its late health for an untested drag. **DROP**. To retry: a Bebop change with a measured gain, and a sandbox pass showing the target follows Mo.

## Pair B3-2 Doorman + Venator: REVISE

### doorman_duo_push: REVISE
- Compress Cooldown on Cart (18.4k). Why not keep it on Call Bell? The Cart at 15s → 12.3s is real, but Superior Cooldown (global) replaces it at 24.8k. The duo change only lives **18.4k–24.8k**. Cost: Call Bell T3 moves 10.4k → 16.8k on the "DPS Doorman" build. Weak but true.
- The struggle "Cart and doors never hold" and the stated gain "~3.75s vs 0s from the push alone" are **FALSE**: Cart T3 (this build has it at 10.4k) stuns 1.25s on wall impact (`ability_doorman_luggage_cart_t3_desc`). **FAIL (I/gain stated)**. The verified combo is Cart into a wall (1.25s), then Gutshot (target already at a wall, 1.0s): 2.25s. The door/trap route is UNVERIFIABLE.
- Gun 1.6k: FAIL on the policy (inherited).
- Name "Room Service Doorman" (31), desc, notes ("On Luggage Cart."), counters (Grit/Opening Rounds in build): OK.

### venator_duo_doorman: REVISE
- **Counters desc "Get after Warp Stone if needed..."**: Warp Stone was removed from this build. **FAIL (G)**: X must be in the build.
- Duration Extender on Snap Trap: root 2.25 × 1.22 = 2.75s (ETechDuration, VERIFIED) for 21.6k–46.4k, then Superior Duration (global) 2.88s. The changes log's "x1.28 more late" is wrong: it's 1.28 instead of 1.22, not on top. Why not on Gutshot? Its stun is tech_duration-scaled, and the verified combo ends in a Gutshot wall stun (1.0 → 1.22s). The trap only helps if the cart can deliver onto it, which is unverified. Change the imbue to Gutshot, or prove the trap delivery in the sandbox.
- Warp Stone out. Why not keep the gap closer? The Cart (12.3–15s cd, one target, only when Doorman is near) does not replace a 16s self-teleport for a melee hero in every other fight. Not justified by numbers.
- Spirit Resilience note "Spirit damage that keeps ticking: Haze, Viper, Infernus, Mina, Mirage.": "Viper" is misspelt, "ticking" is jargon, and Haze has no lasting spirit damage. **FAIL (I)**. Inherited: the same line is in the live data.js venator build and must be fixed there too.
- Policy: OK. Name "Doorstop Venator" (27), desc: OK.
- Pair: the real file-backed combo (Cart T3 wall stun → Gutshot wall stun) exists but isn't what either build is tuned for. **REVISE**: rebuild the pair on the wall-stun chain, and fix the Counters X and the Spirit Resilience note.

## Pair B3-3 Doorman + Graves: DROP

### graves_duo_doorman: DROP
- Duration Extender Decree → Hands. The premise is **REFUTED**: Decree's AbilityDuration scales with `[ETechPower, ETechDuration]`. On Decree at 5.6k (SP 87): 19.5s → about 23.8s, +4.3s, which is one more SummonFrequency 4s cycle (2-ghoul bursts) per gravestone. On Hands: lifetime 7 → 8.5s and root 1.0 → 1.22 (T3 1.75 → 2.14). Both last only 5.6k–16k (Superior Duration is global). The ult build loses ult damage for a root that a 25 m/s cart drag may not even trigger (0.75m aura, 0.1s tick). **FAIL (A/gain)**. Evidence: vdata `m_vecScalingStats = [ "ETechPower", "ETechDuration" ]`.
- Hands T3 one point earlier (9.6k): harmless, but only matters for the failed premise.
- Gun 3.2k: FAIL on the policy (inherited).
- **LIVE graves_ult: no fix needed.** Duration Extender on Borrowed Decree works, and the "inherited issue" note in designs_batch3 is wrong. Don't touch data.js for this.
- Pair: Doorman's side is shared with B3-2 and adds nothing new. **DROP**.

## Pair B3-4 Pocket + Shiv: REVISE

### pocket_duo_shiv: REVISE
- Mystic Expansion Barrage → Affliction (16k–32.8k, then Greater Expansion is global). Affliction 13 → 15.6m (VERIFIED, ETechRange). Why not keep it on Barrage? Barrage is 4.5m (7.5m at T3) and is Pocket's burst. +20% radius is +44% area on the main damage. Affliction at 13m already covers a fight. The gain for Shiv (more enemies heal-blocked) is stated but small, and the change undoes the imbue from Kieran's in-game copy (the changes log says it follows "Kieran's copy (Cloak, Barrage)"). Weak. **FAIL (gain not shown to beat the cost)**.
- The rest is inherited and OK. The heal-block T3 is at 12k. Duration Extender was already on Affliction (15.9s). Policy OK. The changes log's "health 4.8k at 11.2k" is stale: walk1 shows 15.2k (Majestic Leap), which is fine for an escape hero.

### shiv_duo_pocket: REVISE
- Only the ability order changes (Killing Blow T3 49.6k → 10.4k). 18 → 28% is VERIFIED. Why rush it for Pocket specifically? +10% execute line helps solo just as much. Pocket's heal-block covers "heal back out", but Shiv already brings Healbane (18.4k), Decay -50% (21.6k) and Spirit Burn. Cost: Slice and Dice T3 13.6k → 18.4k on a dash build, Bloodletting T3 40.8k → 49.6k. **FAIL (Kieran's bar: no partner-specific build change; designs_batch3 dropped Warden for "order only")**.
- Inherited: the rich box holds **Superior Duration (T3)**: "I'm rich as fuck holds tier-4 items only" **FAIL (G)**, also live. Its note's "full rage ... last longer" claim is unverified.
- Gun 0: FAIL on the policy (inherited).
- Pair: the kits do fit (non-lethal drain plus a 28% execute plus a 13–16.6s heal-block against a 16s recast). But neither build really changes for the other. **REVISE**: give Shiv an item change that only pays off with Affliction, show Pocket's imbue gain against Barrage, and sandbox duo_b3_pocket_shiv_execute.

---

## Per-item CHECKLIST summary (FAILs only; every other item checked OK against base and files)
- Mo: E (no late health, 4.8k flat after 36k), policy gun 0.
- Bebop: Kieran's bar (order-only, zero gain), policy gun 0, changes log false (45k vs 31.2k).
- Doorman: I/gain (Cart T3 stun ignored, "0s" false), policy gun 1.6k.
- Venator: G (Counters X = Warp Stone not in build), I (Viper / ticking / Haze, also live), A (Warp Stone removal unjustified, imbue should be Gutshot).
- Graves: A/gain (premise refuted), policy gun 3.2k.
- Pocket: gain vs cost of moving the imbue off Barrage.
- Shiv: Kieran's bar (order-only), G (T3 Superior Duration in rich, also live), policy gun 0.

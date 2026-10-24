# Seven ult build (data.js id `seven`, "Power Outage Seven") - worked example of WEAKNESS_PROCESS L (with K, J, I, H)
Written 2026-10-24. No game or data.js changes. Proposed build: council/work/seven.js (walk1 FLAGS none, CHECK12 none).
Sources: data.js `seven` and `seven_gun`; audit/items_full.json via audit_D_q.py; abilities.vdata raw blocks (Storm Cloud, item duration/cooldown scale functions); heroes.vdata (hero_gigawatt: 730 HP, +41 HP and +1.1 spirit per boon); a7/levels.json (souls -> level/points); a3/walk1.js, a7/sp.js; model wx7/model.py + wx7/run.py + wx7/marg.py (scratchpad). No evidence/seven.json exists: no measured results, so nothing below is MEASURED and no verdict was flipped by a test.
Kieran's illustration ("Unstoppable + Infuser is very strong for his ult, but don't rush both") was treated as a hypothesis and recomputed.

## 0. Current-patch kit numbers that drive everything
| fact | value | source |
|---|---|---|
| Storm Cloud | channel 7 s, +7 s at T2 (14 s); radius 10 -> 30 m over 3.5 s, +10 m at T2; DPS 95 + 0.6x spirit, +65 at T3; tick 0.3 s; cooldown 205 s; T1 +55% bullet resist while channelling; no damage out of line of sight | abilities.vdata |
| Channel scaling | AbilityChannelTime scales with EChannelDuration + ETechDuration (duration items lengthen it) | abilities.vdata |
| What breaks the storm | `m_bitsInterruptingStates = MODIFIER_STATE_STUNNED` only. Silence does not (Silence Wave: "does not interrupt channeling"); knockback is not listed | abilities.vdata, item desc |
| Unstoppable | 6400 (Debuff Reducer component), active 5.5 s, cd 60 s, 125 HP, 25% status resist; "cannot be used while stunned"; duration scales with ETechDuration | items + vdata |
| Infuser | 6400 (Spirit Lifesteal component, so +4800 over it), active 7 s: +30 spirit and 70% spirit lifesteal; cd 30 s; passive 13% spirit lifesteal, +6 spirit, 100 HP, 10% spirit resist; duration scales with ETechDuration | items + vdata |
| Diviner's Kevlar | on ult cast: 1000 barrier and +40 spirit for 20 s (40 s cd); +15% duration, -10% ult cooldown | items |
| Escalating Exposure | +4.5% spirit amp per stack, 12 stacks, proc cooldown 0.7 s (scales with EItemCooldown), -8 spirit resist | items + vdata |
| Ability timing (order 1331234442431122) | ult unlocked 3.2k, T1 ~4.6k, T2 (14 s) 6.0k, T3 (+65 DPS) 11.2k; Power Surge T3 (-15% spirit resist, 20 s) 15.2k | sp.js / levels.json |

## K. Kit-first thesis
1. Engine: Storm Cloud is a 14-22 s, 40-60 m AoE channel whose only off-switch is a stun, with 55% bullet resist built in. Its damage = (160 + 0.6 x spirit) x seconds x (1 + amp) x resist factor, summed over every hero in line of sight. Buyable multipliers: spirit, duration, amp (Escalating Exposure), resist shred (Mystic Vulnerability, Power Surge T3), radius. Farm engine: Power Surge (chains to 4 targets, imbued by Surge of Power +28 spirit) + Lightning Ball (charges; Cultist gives +1) + Cultist souls.
2. Consequences: spirit/duration/amp are worth more than raw HP early (bullet damage already halved during the storm); the threats to the engine are stuns (end it) and spirit damage (not resisted by the T1 bonus). Insurance items have no damage value of their own, so they only pay once the storm is already big.
3. Thesis T-main: "Farm engine first (Arcane Surge + Surge of Power on Power Surge, Cultist ~8 min), health spike ~12.8k, then storm multipliers (MV/duration -> Escalating Exposure -> Superior Duration), then insurance (Unstoppable, Infuser, Kevlar)." Wrong if: an insurance item bought earlier keeps more storm damage than the multiplier it delays (needs stun frequency x damage kept > ~25-45% of storm, see L4).
4. Rival theses: R1 insurance-first (rush Unstoppable + Infuser after the health spike); R2 Kevlar-first insurance; R3 "hold them in" (Mystic Slow -> Lightning Scroll + Static Charge, so duration and stacks actually land on fleeing heroes); R4 gun-into-ult (that is `seven_gun`, context only: it uses Spirit Lifesteal for Spiritual Overflow, which competes with Infuser for the same component).

## A2 (short). Dependency chain for the combination
Storm compensates for no escape and a weak gun -> depends on an unbroken channel and on Seven surviving inside the fight -> countered by (a) any stun (only stun interrupts), (b) spirit burst/ticking spirit (T1 resist is bullet only), (c) line of sight, (d) walking out. Unstoppable answers (a) only for 5.5 s x duration and must be popped before the stun (can't be used while stunned). Infuser answers (b) through lifesteal, only while dealing damage, and is cut by anti-heal. Nothing in the pair answers (c)/(d). Stun frequency: at least 17 hero kits have a stun/sleep property (abilities.vdata name search, lower bound) and Knockdown appears in 7/81 Council builds, so most games contain a stun; how often it is aimed at Seven's storm is untestable.

## L1. Combinations found (recomputed)
| id | parts | mechanism | enables | conditions | numbers (current files) |
|---|---|---|---|---|---|
| C1 | Unstoppable + Storm | stun immunity during the channel | storm survives the first stun | popped before the stun; enemy can wait it out | covers 5.5 s of 14 s (39%) bare; 7.0 of 20.0 s with Superior Duration (31% of damage, EE ramp makes later seconds worth more); 7.9 of 22.1 s at full build (33%) |
| C2 | Infuser + Storm | 70% spirit lifesteal on every storm tick, +30 spirit | self-heal scaling with heroes in the cloud | items usable in channel [GAP]; AoE lifesteal not reduced [GAP]; no anti-heal | 7 s (9.0 s with SD, 10.0 s full); heal per storm ~1.8k per hero in the cloud at 24.8k state, ~3.5k at full; storm damage +3% |
| C3 | Unstoppable + Infuser | complementary, no shared mechanic | "can't be stopped, can't be killed" window | both popped before the ult | overlap is only the first 7-8 s; they do not amplify each other. The real multiplier for both is global duration (C4) |
| C4 | Superior Duration / Kevlar + C1/C2 + storm | ETechDuration lengthens storm AND item windows | longer protected window | Duration Extender (imbue) lengthens only the storm, so it LOWERS the protected share | Unstoppable 5.5 -> 7.0 -> 7.9 s; Infuser 7 -> 9 -> 10 s; storm 16.1 -> 20.0 -> 22.1 s (with dash-jump Arcane) |
| C5 | Escalating Exposure + storm length | 1 stack per 0.7 s from 0.3 s ticks, 12 stacks at ~7.7 s | +54% amp for the rest of the channel | target stays in the cloud | +43% storm damage per target at the 18.4k state (+2.0k), the largest marginal in the build |
| C6 | Kevlar + storm | on cast 1000 barrier, +40 spirit 20 s, +15% duration, -10% ult cd | damage and survival in one slot | 40 s cd | +23-26% storm per target, 1000 barrier, cd 205 -> 184 s |
| C7 | Cultist + Lightning Ball + storm | +12% radius/range on all abilities, +1 charge | ball farm with 3 charges; storm radius 44.8 -> 49.6 m | Cultist owned (core) | deterministic |
| C8 | Arcane Surge + Power Surge or storm | after a dash-jump: +20 spirit, +15% duration, +12% radius on next ability | farm burst or longer storm | dash-jump within 7 s; one ability per jump | Power Surge spirit 97 vs 58 at 5.6k; storm +15% length |
| C9 | Power Surge T3 + storm | surged targets -15% spirit resist 10 s | +15% storm on surged heroes | burst on them before ult; from 15.2k | free playstyle |
| C10 | Mystic Slow -> Lightning Scroll + storm (+Static Charge) | slow on every spirit tick; scroll 64% slow then 0.75 s stun after 3 s | keeps fleeing heroes inside, so C5/C4 actually pay | enemies try to leave | unmeasurable here (bots don't move) |
| C11 | Refresher + Kevlar/Unstoppable/Infuser (anti-synergy) | Refresher's second storm starts ~23 s after the first | double storm | Kevlar cd 40 s, Unstoppable 60 s, Infuser 30 s | storm 2 has no barrier, no +40 spirit, no Unstoppable; Infuser only from 30 s; damage still ~96% of storm 1 because EE stacks (12 s x 1.43) carry over |
| C12 | Transcendent Cooldown + EE + insurance cds | item CDR 25% shortens EE proc cooldown and item cds | EE plateau 7.7 -> 5.8 s; Unstoppable 45 s, Infuser 22.5 s | Slot-locked item | +1.5% storm; does not fix C11 (Kevlar 30 s > 23 s) |
| C13 | Healbane + storm | -35% healing on everyone the storm touches, 275 heal on kill | AoE anti-heal + kill heal for Seven | | core already |
| C14 | Storm T1 55% bullet resist vs Metal Skin/Plated Armor | overlap | gun counters worth less during the ult, spirit counters more | | info for the Counters menu, no change |
Out of scope: tier-5 items (Cloak of Opportunity blocks a stun and grants Unstoppable on a 12 s cd; Timeless Emblem +50% duration) are in the files but in no Council build or shop model.

## L2. Pricing each completion step
Marginal value at the moment of purchase, given what path R (proposed order) owns. Damage = storm damage per target per cast, enemy spirit resist 0, target in cloud the whole channel, dash-jump before the ult. Heal1/heal3 = heal over one storm with 1/3 heroes in the cloud.

| state (souls) | candidate | souls | storm/target | heal1 / heal3 | other |
|---|---|---|---|---|---|
| 12.8k (health spike done) | Infuser (upgrade) | 4800 | +130 (+4%) | +974 / +2921 | +10 HP |
| | Unstoppable (fresh) | 6400 | 0 | 0 | +125 HP, 5.5 s stun immunity (35% of storm damage guaranteed vs one stun) |
| | Kevlar | 6400 | +891 (+26%) | +116 / +348 | 1000 barrier, ult cd -21 s |
| | MV + Duration Extender + Compress (current next 3) | 4800 | +1150 (+33%) | +150 / +449 | spirit 6.4k/8k invest steps |
| 17.6k (mid done) | Escalating Exposure | 4800 | +2002 (+43%) | +260 / +781 | +9 spirit resist |
| | Infuser | 4800 | +140 (+3%) | +1100 / +3302 | |
| | Kevlar | 6400 | +1065 (+23%) | +138 / +416 | 1000 barrier |
| | Unstoppable | 6400 | 0 | 0 | 30% guaranteed |
| 24.8k (EE + SD done) | Infuser | 4800 | +218 (+3%) | +1792 / +5377 | window 9.0 s |
| | Kevlar | 6400 | +1645 (+23%) | +214 / +641 | 1000 barrier |
| | Unstoppable | 6400 | 0 | 0 | window 7.0 s of 20 s (31%) |
| | Superior Duration (from DE, already bought) | 1600 | +311 (+7%) | +40 / +121 | also lengthens every item window |
(a) Standalone parts: Spirit Lifesteal (1600: 13%, 90 HP, 6 spirit) is good alone and already core; Debuff Reducer (1600: 90 HP, 25% status resist) does not keep the channel (a shorter stun still interrupts), so the partial Unstoppable path buys nothing for the storm. (b) Marginal: Infuser's +4800 is almost pure active (passive stats over Spirit Lifesteal: +10 HP, +10 spirit resist). Unstoppable's value is zero unless a stun is aimed at the storm. (c) Same souls: until ~24.8k the damage multipliers (EE +43%, MV/DE/CC +33%) beat both insurance items by 10x in damage; Kevlar beats Infuser on damage and is the better single-target survival buy (1000 barrier vs ~1.8k heal that needs damage dealt). (d) Affordability at ~1k/min: 4.8k-6.4k each = 5-6 min of farm per item; the pair together is 11.2k extra (fresh Unstoppable 6.4k + 4.8k) = ~11 min with nothing else bought. (e) Later is better: both windows grow 28-43% once Superior Duration/Kevlar are owned, and Infuser's heal grows with spirit and EE (974 at 12.8k -> 1792 at 24.8k per hero). (f) Spikes/slots: rushing the pair puts 11.2k into health right after the 12.8k health spike (health 16k at 24k) while spirit sits at 4.8k invest from 5.6k to ~24.8k; slot lock not affected (both are T4).

## L3. Effect of the combination on the rest of the build
- Redundant with it: nothing fully. Kevlar overlaps Infuser on survival (barrier vs heal) but adds damage; Metal Skin/Plated Armor overlap the storm's own 55% bullet resist during the ult (Counters menu still needed out of the ult).
- Raised by it: Superior Duration (now lengthens 3 windows, not 1), Transcendent Cooldown (item cds), Healbane/Spirit Burn (enemy anti-heal does not matter to these; enemy anti-heal on Seven cuts Infuser).
- Lowered by it: Refresher (C11: second storm unprotected); Duration Extender as an imbue (lengthens the storm only, so the protected share falls).
- Without the pair: the build still has storm T1 bullet resist, Enduring Speed health spike, Healbane kill heal, Kevlar barrier; the missing piece is only the stun answer.

## L4. Whole-build paths at checkpoints (same souls, real levels/points)
Paths (all 46.4k, 12 slots, walked): CUR = data.js order (Arcane Surge in Late); R = CUR with Arcane Surge restored to Early (proposed); A = R but Infuser + Debuff Reducer -> Unstoppable right after Enduring Speed (rush); A2 = rush after the mid ult items; B = R with Infuser before Unstoppable; C = R with Kevlar before Unstoppable/Infuser.

| souls | lvl, tiers (ball,SC,PS,ult) | CUR | R | A (rush) | A2 | B | HP (R) |
|---|---|---|---|---|---|---|---|
| 5k | 10, 1/0/2/1 | 809 / storm 7.0 s | 1036 (+28%), 8.0 s | = R | = R | = R | 1099 |
| 10k | 16, 1/1/2/2 | 1691 | 2321 (+37%) | = R | = R | = R | 1545 |
| 18k | 24, 2/1/3/3 | 3955 | 4690 (+19%) | 3658 (-22% vs R), heal1 1443 | = R | = R | 1905 |
| 24k | 27, 2/1/3/3 | 6749 | 6749 | 3690 (-45%), heal1 1455, Unstoppable 5.5 s | 4871 (-28%), heal1 1724 | 6749 | 2040 |
| 30k | 30, 3/1/3/3 | 7286 | 7286 (5.2k unspent) | 4912 (-33%), heal1 1738 | 4912 (-33%) | 7504 (+3%), heal1 2749, heal3 8246 | 2175 |
| 46.4k | 35, 3/2/3/3 | 9302, heal1 3487, heal3 10461, barrier 1000, cd 144 s | same | same | same | same | 2535 |
Numbers: storm damage per target per cast; "= R" means same items at that soul count. Spirit 4.8k: CUR 13.6k, R/A/B 5.6k. Health 4.8k: CUR 11.2k, R 12.8k. Power Surge spirit (farm engine, with dash-jump): R 97 vs CUR 58 at 5.6k, 100 vs 61 at 8k, 120 vs 100 at 13.6k; equal from 18.4k.
When the pair "pays for itself": never in damage (it delays EE and duration by 6-11k souls); in survival it pays per storm only when (a) a stun is actually thrown during the first 5.5-7 s, or (b) 2+ heroes stay in the cloud while Seven is taking damage. A's survival gain at 18-24k is ~+1.4k heal per hero and a 5.5 s stun guard, bought with 22-45% of the storm and a later EE.

## L5. Verdicts
| synergy | verdict | grade | conf. | what would make it wrong | test |
|---|---|---|---|---|---|
| C1+C2 pair (Kieran's) | core later; keep Unstoppable 31.2k, Infuser 37.6k; do NOT rush | CALCULATED (damage cost) + UNTESTABLE-HIGH-RISK (stun value) | 75% on "don't rush" | enemy stuns land on most storms in the first 5 s and the storm is the only kill tool before 25k | L1, L2 (stun half UNSUPPORTED: no player-CC op, GAPS 7), L3 |
| Infuser before Unstoppable (path B) | candidate only; keep current | UNTESTABLE-HIGH-RISK (stun side), CALCULATED heal side | 45% | AoE lifesteal reduced or items not usable mid-channel (L1); stun-heavy enemy comps | L1, L3 |
| Kevlar before the pair (path C) | candidate only; keep current | CALCULATED for +23% and barrier; Kevlar's +15% duration being a passive is [GAP] | 50% | Kevlar duration bonus only applies while the buff is active; stun-heavy comps | L3 |
| C4 duration items x windows | core now (keep Superior Duration at 24.8k) | CALCULATED | 70% | duration % not additive / items not ETechDuration-scaled in play | L2 |
| C5 EE x storm length | core now (first 6.4k-class buy after mid) | CALCULATED | 70% | stacks per tick group or per second differ from 0.7 s | L5 |
| C6 Kevlar | core late (keep) | CALCULATED | 65% | as above | L3 |
| C7 Cultist radius/charge | core now (keep, ~8 min) | CALCULATED (deterministic stats) | 80% | | none needed |
| C8 Arcane Surge early | CHANGE: restore to Early before Surge of Power | CALCULATED | 75% | players don't dash-jump before Power Surge (then the gain is the invest step only, storm ~+10% at 10k) or a rule moved it that is not recorded | L4 (dash-jump op unverified) |
| C9 Power Surge T3 shred pre-ult | playstyle only, no note (notes never explain procs) | CALCULATED | 55% | debuff only on the shot target | L8 |
| C10 Mystic Slow / Lightning Scroll hold | situational hypothesis; no change (Lightning Scroll stays rich) | UNTESTABLE-HIGH-RISK | 35% | | L7 UNSUPPORTED (bots can't move) |
| C11 Refresher anti-synergy | keep Refresher rich-only and last | CALCULATED | 60% | Kevlar cd lower than modelled | L6 |
| C12 Transcendent + EE | Slot locked stays (+1.5%) | CALCULATED | 60% | | L5 arm EE_TC |
| Debuff Reducer -> Unstoppable partial | skip | CALCULATED | 55% | status resist shortens stuns below some engine threshold | none |
| C13 Healbane | core (keep) | CALCULATED | 60% | | none |
| Mystic/Greater Expansion radius (40 -> 50-62 m) | keep (cheap), low marginal: line of sight, not radius, is the usual limit | UNTESTABLE-HIGH-RISK | 45% | | none possible |

## J. Item roles (combination items)
| item | primary | secondary roles (from data) | grade |
|---|---|---|---|
| Unstoppable | stun guard for the storm | 125 HP, 25% status resist always; 5.5 s immunity to silence/sleep/root/disarm usable every fight (60 s cd) outside the ult; suppresses slows while active | CALCULATED |
| Infuser | storm self-heal | +30 spirit for Power Surge/ball fights every 30 s; 10% spirit resist; replaces Spirit Lifesteal passive 1:1 | CALCULATED |
| Diviner's Kevlar | barrier on ult | +40 spirit (+23% storm), +15% duration on all windows, -10% ult cd | CALCULATED |
| Superior Duration | longer storm | longer Unstoppable/Infuser/Power Surge/EE debuff, 8% bullet resist | CALCULATED |
| Escalating Exposure | storm amp | amp also on ball/Power Surge targets; 17% spirit resist | CALCULATED |
| Arcane Surge | longer/bigger next ability | +20 spirit on Power Surge farm casts, keeps Extra Stamina's stamina | CALCULATED |
| Cultist Sacrifice | souls | +12% radius/range on every ability, +1 ball charge, HP | CALCULATED |

## I. Practicality
- Buttons in the ult: dash-jump (Arcane) -> Unstoppable -> Infuser -> ult is 4 inputs inside ~7 s; Arcane's window is 7 s and "next ability" may be eaten by Power Surge if used first. Accept; the existing notes already describe the sequence.
- Pre-pop vs reactive Unstoppable: telegraphed stuns (Knockdown 2 s delay, Static Charge 3.5 s, Lightning Scroll 3 s) could be answered by popping Unstoppable when the mark appears, which covers the storm better than pre-popping. Untestable; no note (notes don't explain procs).
- Being behind: the proposed order is forgiving (farm engine online at 5.6k); the rush path is not (no damage growth 12.8k-24k).

## F. Regression of the proposed change (Arcane Surge to Early)
Walked: spirit 4.8k 13.6k -> 5.6k; health 4.8k 11.2k -> 12.8k (in-your-face rule: the storm gives 55% bullet resist and this was the audited state before the move: evidence/cost/seven.md "health @12.8k ... met within 1k"); Cultist 7.2k -> 8.0k (rule ~8 min); no 6.4k run change; no slot change; Counters "after Enduring Speed" still true; Lost-lane reorder still valid; walk1 FLAGS none, CHECK12 none. New weakness: 1.6k later health spike in a lost lane (the Losing-lane Extra Regen and Lost-lane reorder cover it).

## Tests (pre-registered, council/sandbox/scenarios/)
seven_L1_infuser_in_storm (runnable: autorun/scenarios/seven_L1_infuser_in_storm.txt), seven_L2_unstoppable_window (window runnable; stun half UNSUPPORTED), seven_L3_insurance_slot, seven_L4_arcane_early (needs a dash-jump op check), seven_L5_ee_ramp, seven_L6_refresher_second_storm, seven_L7_mystic_slow_hold (UNSUPPORTED), seven_L8_ps_shred_preult. Results: none yet (no evidence/seven.json); every pending verdict stays "keep current".

## Decisions recorded in council/work/seven.js changes
1. Arcane Surge restored to Early before Surge of Power (CALCULATED, 75%).
2. Unstoppable/Infuser/Kevlar order unchanged; rush rejected (CALCULATED damage cost); Infuser-first and Kevlar-first are PENDING L1/L3.
GAPs to close: items usable during the channel; AoE spirit lifesteal rate; Infuser 70% total vs +13%; Kevlar +15% duration passive or buff-only; duration % additive; does sleep interrupt (only STUNNED is listed); Arcane Surge on item casts.

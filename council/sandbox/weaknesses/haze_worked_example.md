> **STATUS: UNAPPROVED / UNVERIFIED (Kieran 05:42).** All numbers are from a hand-built fight model; confidence percentages are model outputs, not measured accuracy. The 6.7s vs 9.5s style figures are model outputs only. Do not adopt.

# Haze `haze` (Rizuhble's Victor Cosplay Haze): worked example of WEAKNESS_PROCESS K + A2, H, I, J, L
2026-10-24. Scope: build id `haze` only (`haze_assassin` out of scope). Nothing in data.js or the game was touched.
Sources: data.js `haze` (read-only), audit/items_full.json, audit/hero_haze.txt, gt/.../scripts/abilities.vdata (ability_smoke_bomb, ability_sleep_dagger, ability_stacking_damage, ability_bullet_flurry, citadel_weapon_haze_set), heroes.vdata `hero_haze`, a7/levels.json, sandbox GAPS.md / AUTORUN.md, results/README_victor_lifesteal_gun_only.md (the only measured lifesteal data), RULES_KIERAN.md, CHECKLIST.md.
Tools written for this file: `haze_model.py` (fight/heal model), `haze_runs.py` (comparisons; `python3 haze_runs.py` and `python3 haze_runs.py m2`), raw output `haze_runs.out`. Scenarios: `sandbox/scenarios/haze_*.json` (7). Proposed build: `council/work/haze.js`.
Evidence status: there is no `evidence/haze.json` and no Haze sandbox result. Every verdict below is pre-test: CALCULATED at best, UNTESTABLE-HIGH-RISK where mechanics are unknown. Kieran's framing is treated as a hypothesis, not a target.

Tags: [kit]/[item] = read from game data; [U] = mechanic not in the data, must be checked in game; [GAP] = number missing from extracted data; [A] = modelling assumption.

## 0. Data facts that change the analysis (found while checking Kieran's numbers)
1. Smoke Bomb T3 is the engine, and it arrives late. +50% bullet lifesteal for 5 s and "dispels non-ult debuffs" are both T3 (5 ability points). With the current order (3311234222341144) T3 lands at the 12th point = level 16 = 9.2k souls [kit + heroes.vdata level table]. Before ~9.2k Haze has no kit lifesteal at all. Any "the kit already heals, so greens can wait" argument only holds from 9.2k.
2. The 5 s lifesteal is `PostInvisBuffDuration` and scales with ETechDuration; the 50% scales with EHealingOutput [kit, abilities.vdata]. So duration items can stretch the window; heal-amp items probably raise the 50% [U whether HealAmpCastPercent feeds EHealingOutput].
3. Charges: T2 gives 2 charges with 7 s between uses; base cooldown 33 s [kit]. Extra Charge +1, Rapid Recharge +2 (total 4), -14% cooldown on charged abilities, -30% between-charge time (7 -> 4.9 s) [item]. If charges refill one at a time [U, normal Deadlock behaviour], charges raise how many smokes she has IN a fight, not the long-run rate: sustained rate is 1 smoke / 33 s (28.4 s with Rapid Recharge), i.e. 15-18% lifesteal uptime outside the burst.
4. Smoke T1 in data is +7 m/s invisible move speed (InvisMoveSpeedMod), not the cooldown its tooltip string names [kit; text mismatch].
5. Haze gains 0.5 spirit per level, not the generic 1.1 (heroes.vdata `MODIFIER_VALUE_TECH_POWER = 0.5`). a7/sp.js uses 1.1 for every hero, so its Haze spirit numbers are about +18 too high at level 36. Bullet damage grows +0.143 per level (5.26 -> 10.3 at level 36); the round-12 Burst Fire vs Surge sim used a flat 5.3 and understated weapon scaling.
6. Gun economy [kit]: 25 rounds, 0.105 s cycle (9.5 shots/s), 2.35 s reload, falloff from 787 u. With Titanic + Active Reload the clip is 55; at the build's +38-48% fire rate it empties in about 4 s. A 10-12 s fight is limited by magazine + reload, not fire rate (section I).
7. Fixation (her 3) adds a flat 0.31 per stack at T3 (+0.00035 x weapon-damage %), 80 stacks at T2 [kit]: about +25-28 per bullet at full stacks vs a base bullet of 9-10 x (1 + weapon %). Most of her bullet damage late is Fixation, which weapon-% items barely touch; hits per second (fire rate x accuracy) and staying on one target matter more.
8. Healing Tempo text: "Does not apply on innate Regen or passive Bullet/Spirit Lifesteals" [item]. Smoke T3 and Vampiric Burst both grant bullet lifesteal; whether either (or Siphon's max-HP steal) counts as a heal that triggers Tempo's +35% fire rate / +1.25 m/s for 7 s is unknown [U]. Kieran's in-game note says Siphon procs it. This one fact decides Tempo's whole value (section L).
9. Weapon investment bonus above 4.8k is not in the extracted data [GAP]; the model uses the spirit table scaled by 46/38 (11.2k -> 74%, matching the round-12 sim). Health investment bonuses are ignored [GAP]. Conclusions below were checked to not depend on these (they compare items inside the same colour or at equal investment).

## 1. Engine mechanics and hero identity map (K1, A2.1)
Engine candidates, ranked by how much buyable stats move them:
| mechanic [source] | scales with | why it is an engine |
|---|---|---|
| Smoke T3: +50% bullet lifesteal 5 s + dispel on cast, 2 charges, 33 s [kit] | bullet damage dealt (incl. Fixation and Ricochet bounces [U]), heal amp [U], ability/item duration, charges, cooldown | 78-82% of all her healing in a 12 s fight at 10-24k, ~50% at 41k+ (model). Also her only cleanse. |
| Fixation 80 stacks, flat bullet bonus [kit] | hits per second, accuracy, fire rate; magazine (losing time reloading loses stacks only after 11 s) | dominant damage source; makes fire rate + magazine worth more than weapon % |
| Bullet Dance: 3.5 s (+0.03 x spirit) auto-aim, +25% (+10% T2) fire rate, +7 (+7 T1) bullet damage, 16 m, 1 target per tick, 165 s (100 s at T3) [kit] | fire rate, bounces (Ricochet), spirit (duration), lifesteal (perfect accuracy = guaranteed heals) | her teamfight win button; with Ricochet it hits 3 heroes |
| Smoke invisibility 8 s (+0.1 x spirit), dagger does not break it [kit] | spirit, Rapid Recharge's +14 spirit for charged abilities | free engages / escapes; first shot from stealth |
| Sleep Dagger 2.75 s (+1 T2), T2 +15 Fixation stacks, 13 s at T3 [kit] | imbues (Surge of Power) | sets up stacks and a free target |

Identity map (strength -> compensates -> depends on):
| strength | compensates | depends on |
|---|---|---|
| Smoke lifesteal + cleanse | low HP (730 +33/level), no armour in kit | Smoke T3 bought (9.2k+), a charge available, not silenced/stunned at the moment she needs it, bullets landing on something |
| Invisibility | no dash/escape ability | not within 18 m (SpottedRadius), 1.5 s revealed when damaged, cast possible (silence/stun) |
| Ult perfect accuracy + Ricochet | hard to aim her small bullets under pressure; low burst | ult off cooldown (100-165 s), not interrupted (stun), targets within 16 m, ammo [U whether the ult uses magazine] |
| Fixation | low base damage | staying on one target; target switching restarts stacks |
| Farming with Ricochet | expensive build (52.8k core) | camps/waves with 3 units in 13 m |

## 2. Build thesis (K3) stated falsifiably
Thesis K (Kieran's framing, as a hypothesis): "Smoke T3 lifesteal (+charges/recharge) + heavy bullet damage => gun focus, rush Ricochet for farm, delay greens (Fortitude later), lifesteal items partly redundant."
Numbers that would make it wrong, and what the data/model says:
| falsifier | result | grade |
|---|---|---|
| F1: the engine is not online during the window where greens are delayed | TRUE for <9.2k (no Smoke T3). Ricochet-first (K1) at 10k has 4.8k items + 5.2k banked: dies in 6.7 s when focused vs 9.5 s for the current Fortitude-first order. From 12k the gap is small (9.2 vs 10.0 s) and K1 has +29% 1v1 damage and ~3x camp damage | CALCULATED, 60% |
| F2: extra bullet damage heals less than the same souls in health | TRUE per soul: at 12k Ricochet adds +116 healing (12 s) for 6.4k; Extra Health + Fortitude add +375 HP for 3.2k. "More damage = more healing" is real (heal/damage 0.46 at 10k, 1.19 at full) but it does not replace greens; Ricochet is justified by farming and the ult, not by healing | CALCULATED, 70% |
| F3: charges add sustained lifesteal | FALSE as stated: in one 12 s fight a third charge adds 0 healing (the 2 base charges already cover 10 of 12 s); Rapid Recharge adds +321 HP via 4.9 s between charges and -14% cooldown. Charges pay off in long fights, back-to-back fights and as extra cleanses | CALCULATED, 55% (assumes sequential refill [U]) |
| F4: kit lifesteal makes lifesteal ITEMS redundant | FALSE: Vampiric Burst stacks with smoke (50 + 13 + 70 = 133% in the window) and is the best 4.8k step at 41.6k (+752 damage, +2736 HP in focus) because of its fire rate and 75% ammo refill. Healing Booster/Tempo are the questionable ones (section L) | CALCULATED, 65% |
| F5: thesis collapses when smoke is denied | Partly TRUE: without smoke she dies 1.9-2.6 s sooner when focused at 10-24k; at 41.6k+ she goes from surviving 12 s to dying at 6.6 s. The engine needs a PREVENT layer (section 6) | CALCULATED, 55% |
Verdict on Thesis K: the gun-focus + Ricochet-farm + lifesteal-active part holds and matches the current build; the "delay greens because the kit heals" part is refuted before 9.2k and only weakly supported after it. Ricochet-first stays the lost-lane option, not the default.

## 3. Rival theses and baseline (K4)
All walked with the same model at equal souls (12 s fights, 50% accuracy, 20% head share of hits, 20% enemy bullet resist; "focus" = incoming 2x the current build's own 1v1 dps at that soul total; "camp" = 3 targets, 90% body hits, no resist). Model output: `haze_runs.out`.
| thesis | idea | 10k | 18k | 24k | 30k | 41.6k | 52.8k | result |
|---|---|---|---|---|---|---|---|---|
| CUR (data.js) | gun + Ricochet 14.4k + smoke engine + VB | dies 9.5 s | dies 8.1 s | dies 10.2 s | lives 17% HP | lives 14% | lives 21% | baseline of the comparison |
| K1 Ricochet before greens | Kieran's literal framing | dies 6.7 s | = CUR | = CUR | = CUR | = CUR | = CUR | worse at 10-12k, same after 14.4k; farm gain not modelled (no income data) |
| R1 spirit hybrid | Surge + Extra Charge/Rapid Recharge + Spiritual Overflow for ult duration; Ricochet at 24k | dies 8.1 s | dies 6.8 s | dies 7.9 s | dies 11.1 s | dies 5.2 s | dies 11.5 s | rejected: behind 14-41k in survival and 3-target damage (no Ricochet until 24k); only the ult is longer (+0.03 s per spirit; Haze gets only 0.5 spirit/level) |
| R2 duration smoke (unusual) | Duration Extender on smoke at 16k, Superior Duration + Frenzy late instead of Healing Booster/Tempo | dies 9.5 s | dies 7.7 s | dies 9.9 s | lives 8% | dies 11.2 s | lives 32% | rejected as a whole path (16k Duration Extender is weaker than either 1.6k green), but Superior Duration survives as a late candidate (section L) |
| K2 lifesteal-early | Bullet Lifesteal at 16k, no Healing Booster/Tempo, Superior Duration + Frenzy late | dies 9.5 s | dies 9.1 s | dies 10.6 s | lives 1% | dies 11.2 s | lives 32% | best 16-24k, worse 30-49k (no heal amp when VB+smoke heals are large): the 16k half survives, the "skip Healing Booster" half does not |
| B0 conventional | Burst Fire + Bullet Lifesteal early, Ricochet ~16-20k, Surge, Leech-style late (from earlier rounds' same-style pick rates; not re-fetched) | dies 8.8 s | dies 8.9 s | dies 8.6 s | dies 9.6 s | dies 10.7 s | dies 11.2 s | stronger fights at 12-18k (+300-400 1v1 damage), camp damage 320 vs 750; from 24k CUR wins on every metric. Farm-first pays off by ~24k |
| ADOPT | CUR with Bullet Lifesteal at 16k and Healing Booster at 27.2k (same items) | = CUR | dies 9.1 s | dies 10.6 s | = CUR | = CUR | = CUR | strictly >= CUR at every checkpoint |
| (ability order) smoke-first | 3,1,2,2,2,2,...: Smoke T3 at 6k instead of 9.2k | - | - | - | - | - | - | at 6-8k focus survival 10.4 s vs 6.4-7.4 s, 1v1 damage -19% (Fixation T0); equal from 9.2k. Interesting, not adopted (see verdicts) |

Unusual ideas tried and where they ended: Superior Duration stretching every timed window (smoke lifesteal, VB, Burst Fire, Active Reload, Fixation stacks) - live candidate; Duration Extender imbued on smoke - weaker than greens at 16k; smoke-first point order - live, untestable; Leech AND Vampiric Burst together (needs Bullet Lifesteal bought twice as a component) - modelled as "Leech for Healing Tempo", competitive only if Tempo never triggers; Frenzy (fire rate + 10% lifesteal + low-HP fire rate) for Healing Tempo - more damage, less survival.

## 4. Surviving theses: item set, order, soul-timed walk (K5-K6)
Main = ADOPT (current items, one reorder). Second = K1 order (already the "Lost lane?" box). Order string 3311234222341144 unchanged. Levels/points from heroes.vdata; spirit uses Haze's real 0.5/level.
ADOPT order: Rapid Rounds, Active Reload, Swift Striker, Extended Magazine, Titanic Magazine (gun 4.8k @ 4.8k) | Extra Health, Fortitude | Ricochet (14.4k) | Bullet Lifesteal (16k, health 4.8k) | Siphon Bullets | Burst Fire | Healing Booster (27.2k) | Extra Charge | Lucky Shot | Rapid Recharge | Vampiric Burst | Silencer | Healing Tempo (52.8k). walk1.js: FLAGS none; spikes gun @4.8k, health @16k; 12 slots; check.js: only the three pre-existing colour-change swap notices.
| checkpoint | level / tiers (dagger, smoke, fix, ult) | owned | HP / clip / weapon % / fire % | 1v1 12 s dmg, duel end HP, focus | 3 targets 12 s / ult 6 s vs 3 / camp dps |
|---|---|---|---|---|---|
| 5k | 10 / T1, T1, T2, unlocked | 3 gun items (Swift Striker, Active Reload, Titanic) | 1027 / 55 / 60 / 20 | 1011, dies in duel at ~11 s, focus 5.1 s | 1011 / 1243 / 212 |
| 9.2k | 16 / Smoke T3 here | + Extra Health, Fortitude | 1600 / 55 / 60 / 20 | engine online: duel end 821 HP | - |
| 10k | 16 / T1, T3, T2, unl | as 9.2k, 2k banked toward Ricochet | 1600 / 55 / 60 / 20 | 1086, 821 HP, focus 9.5 s | 1086 / 1345 / 227 |
| 18k | 24 / T2, T3, T3, T1 | + Ricochet, Bullet Lifesteal | 1954 / 55 / 94 / 38 | 1900, 1173 HP, focus 9.1 s | 4152 / 5749 / 764 |
| 24k | 27 / same | + Siphon Bullets | 2053 / 55 / 109 / 38 | 2037, 1662 HP, focus 10.6 s | 4463 / 6081 / 819 |
| 30k | 30 / T3, T3, T3, T1 | + Burst Fire, Healing Booster, Extra Charge | 2152 / 55 / 109 / 48 | 2610, 2287 HP, lives | 5687 / 8007 / 842 |
| 41.6k | 34 / ult T2 | + Lucky Shot, Rapid Recharge, Vampiric Burst | 2294 / 62 / 115 / 48 | 3774 (focus), lives 14% | 7562 / 11455 / 1562 |
| full 52.8k | 36 / all T3 | + Silencer, Healing Tempo | 2360 / 62 / 126 / 48 | 3961, lives 21% (48% if Tempo triggers off Siphon) | 8728 / 11982 / 1641 |
What is delayed and what it costs: the health 4.8k spike sits at 16k (Kieran's 14-16k window for sustain/escape heroes); spirit never reaches 4.8k (3.2k), so smoke/ult durations stay near base (ult 3.5 + 0.03 x ~29 spirit = 4.4 s at full). Early game (<9.2k) has no kit sustain: lane survival comes from Active Reload's 16% lifesteal window, Extra Health and invisibility only.

## 5. Item roles (J): every item in the build, all roles, overlaps
| item (price) | roles in THIS kit [data] | starts mattering | overlaps / conflicts | best alternative checked | grade |
|---|---|---|---|---|---|
| Rapid Rounds -> Swift Striker (800 -> 1.6k) | +20% fire rate (Fixation stacks faster, ult +rate), +0.75 sprint | at buy | fire rate is ammo-capped in long fights | none better at 800 for lane | CALCULATED |
| Active Reload (1.6k) | timed reload ends reload early; then +25% fire rate, +16% bullet lifesteal, +0.75 m/s for 7 s; +20% clip | at buy; the only lifesteal before 9.2k | sells late for a counter (note) | Bullet Lifesteal 1.6k (passive, no timing) | CALCULATED; timing reload is UNSUPPORTED in sandbox |
| Extended -> Titanic Magazine (800 -> 1.6k) | +100% clip, +14% weapon; most valuable gun stat here (build is magazine-bound) | at buy | - | - | CALCULATED |
| Extra Health -> Fortitude (800 -> 3.2k) | +375 HP; 2.25%/s regen after 10 s without damage (to 75%); +1.5 m/s | at buy (HP); regen between fights | regen role overlaps smoke-on-camp healing once Smoke T3 is in [U lifesteal vs NPCs is full rate] | Ricochet first (K1): -3 s focus survival at 10-12k | CALCULATED |
| Ricochet (6.4k) | 2 bounces at 65% within 13 m with procs; +18% fire rate; ult vs 3 heroes x2.8; bounce lifesteal [U]; Silencer build-up spread to 3 [U] | at buy: camp damage 227 -> 731 (x3.2) | none | Fortitude-first; Burst Fire+Bullet Lifesteal+Extra Health (+431 1v1, but 3-target +90 vs +1554) | CALCULATED; farming UNSUPPORTED in sandbox |
| Bullet Lifesteal (1.6k, now at 16k) | 13% bullet lifesteal (all fights, all targets), +90 HP, +6% weapon; component of VB | at buy | stacks with smoke/VB additively | Healing Booster at 16k (+133 HP/1k vs +204) | CALCULATED |
| Healing Booster (1.6k, now at 27.2k) | +20% heal amp (on lifesteal [U]), +3 regen, +1 OOC regen; Tempo component | grows with total healing; worth it once VB+smoke stack (30k+: keeps her alive where "skip" dies at 11.2 s) | amp vs flat lifesteal crossover at 65% average lifesteal | Bullet Lifesteal (earlier), Duration Extender | CALCULATED; amp-on-lifesteal measurable |
| Siphon Bullets (6.4k) | +15% weapon, +10% bullet resist; steals 2.5% of the target's max HP per hit every 1.2 s for 17 s (her max HP up, theirs down); possible Tempo trigger [U] | at buy: +702 HP in focus at 22.4k | with Healing Tempo (section L) | Leech (equal overall in the model) | CALCULATED (steal-as-heal [A]) |
| Burst Fire (3.2k) | +10% fire rate, +32% for 4.5 s on hero hit (9 s), +1.25 m/s, slide | at buy; front-loaded | fire rate capped by magazine: 0 gain in a 10 s window, about +25% over 12-20 s | Surge of Power on dagger (swap; not modelled correctly: Surge's fire rate stat is not in the model), Healing Tempo (needs trigger) | CALCULATED |
| Extra Charge -> Rapid Recharge (800 -> 3.2k) | 3 then 4 smokes per fight, 4.9 s between, -14% cooldown, +14 spirit on smoke (invis +1.4 s); more cleanses | Extra Charge alone: ~0 in one fight; RR +321 HP | overlaps Duration Extender (window length) and Superior Duration | Duration Extender (+175 HP for 1.6k, ~same per soul) | CALCULATED (sequential refill [U]) |
| Lucky Shot (6.4k) | 25% chance +100% weapon damage [U on whether Fixation's flat part is included], +30% clip | at buy | - | - | CALCULATED |
| Vampiric Burst (6.4k) | 13% lifesteal, +100 HP, +10% bullet resist, +6% weapon; active 5 s: +70% lifesteal, +34% fire rate, refill 75% ammo; works while silenced (item) | at buy: biggest single step | stacks with smoke (pop in the smoke window when the clip runs out) | Leech (section L) | CALCULATED; measured lifesteal % on Victor matches item text |
| Silencer (6.4k) | bullet build-up to 2.5 s silence (10 s immunity), +12% spirit resist, -25% spirit damage from victims; PREVENT layer vs kit CC | late | none | Frenzy (+758 20 s damage, +722 HP but no silence) | UNTESTABLE-HIGH-RISK (CC value not measurable; build-up time per shot [U]) |
| Healing Tempo (+4.8k over Healing Booster) | +25% amp, +6 regen, +4 OOC, +10% spirit resist; +35% fire rate +1.25 m/s 7 s when a qualifying heal lands | only if something triggers it | Siphon pairing | Leech / Superior Duration / Frenzy | UNTESTABLE until haze_tempo_trigger runs |

Redundancies found: (a) Extra Charge has no value in a single fight until Rapid Recharge; the cost audit already flagged it (bought 8.8k before its upgrade). (b) Fortitude's regen overlaps smoke-on-camp healing after 9.2k; its HP does not. (c) Healing Booster duplicates Bullet Lifesteal's job until total lifesteal is high (fixed by the reorder). (d) Fire-rate items overlap each other because the clip caps them (Swift Striker, Burst Fire, Ricochet, VB, Tempo all compete for the same ~4 s of firing).

## 6. Engine countered (A2.2-A2.4)
Counters that exist in the data (verified in items_full / Wraith A2 file): silence - Silencer, Focus Lens, Cursed Relic (also removes non-ult buffs and blocks items), Silence Wave, Grey Talon snare, Violet ult; stun/sleep - Knockdown, Lightning Scroll, Arctic Blast, many kit stuns (Smoke's cast is interrupted by stun: `m_bitsInterruptingStates = STUNNED`); anti-heal - Toxic Bullets -35%, Healbane -35%, Inhibitor -40%, Crippling Headshot -35%, Spirit Burn -70%, Decay -50%; gun denial - Metal Skin 5 s bullet immunity, Plated Armor, disarms (Phantom Strike, Cursed Relic); reveal - anyone within 18 m sees her, damage reveals for 1.5 s.
Ranked chains:
| rank | chain | frequency | lethality |
|---|---|---|---|
| HC1 | smoke covers low HP/no escape; silence or stun before she casts -> no lifesteal, no cleanse, no invisibility | high (most lobbies own silence or stun) | high: model -1.9 to -2.6 s focused at 10-24k; at 41.6k from living to 6.6 s |
| HC2 | lifesteal stack covers no armour; anti-heal cuts all of it | very high (anti-heal in most core builds) | medium: slow erosion |
| HC3 | gun drives damage AND healing; Metal Skin/disarm turns off both | medium (counter buys) | medium |
PREVENT: cast smoke first in every fight (before the silence/stun lands; dagger and items do not break invisibility); keep one charge in reserve for escape (charges make this possible: the real value of Extra Charge/Rapid Recharge); own Silencer on the main CC carrier; Unstoppable (Counters box; usable before a stun, not during it; blocks silence/stun/sleep/root/disarm 5.5 s).
RECOVER: the smoke dispel itself removes non-ult debuffs on cast, which includes anti-heal debuffs [U that heal-reduction counts as a dispellable debuff]. Build-up anti-heal (Toxic 1.28/shot, Inhibitor 0.77/shot) has to rebuild, and Spirit Burn has a 20 s per-enemy immunity, so a dispel at the start of the 5 s window likely keeps most of the window clean; Healbane and Crippling Headshot re-apply on the next hit. Divine Barrier (rich box) removes non-stun debuffs as an item.
SURVIVE: Vampiric Burst is an item active, so it still gives 83% lifesteal and the ammo refill while silenced; Siphon's max-HP steal is passive; Fortitude/Siphon/VB HP. Leech's "reduces enemy healing reduction" is a [GAP] amount.
Counter-the-counter: enemy waits for the smoke, then silences (answer: charges / Unstoppable); Cursed Relic strips buffs and blocks items (answer: none in build; Counters box has it as their tool, not ours); burst during the 1.5 s reveal.
Frequency check: HC1 justifies a playstyle rule (smoke first, keep a charge) and the existing Unstoppable counter; it does not justify more souls in core. HC2 does not justify swapping VB for Leech (section L).

## 7. Synergies and marginal value (L)
Combinations found (parts, mechanism, enables, conditions):
| combo | mechanism | enables | condition / numbers |
|---|---|---|---|
| Smoke T3 + Vampiric Burst (+ Active Reload + Bullet Lifesteal) | additive lifesteal 50 + 70 + 16 + 13 = 149% in one 5 s window; VB refills 75% of the clip inside it | burst heal larger than the damage she takes from 2 attackers (heal/damage 1.14 at 41.6k) | pop VB when the clip empties inside a smoke window |
| Siphon + Healing Tempo (Kieran) | Siphon's steal as a qualifying heal would keep Tempo's +35% fire rate up all fight | +1491 damage over 20 s and +880 HP at full, if it triggers | entirely [U]; scenario haze_tempo_trigger |
| Ricochet + Bullet Dance | auto-aim bullets bounce to 2 more heroes | ult vs 3 heroes 1345 -> 3936 at 12k (x2.9) | enemies within 13 m of the target |
| Ricochet + lifesteal (smoke/VB) | bounce damage healing [U] | 3-target fights heal x2.3 | [U] |
| Ricochet + Silencer | bounces "apply any bullet procs" -> silence build-up on 3 heroes [U] | multi-silence | UNTESTABLE |
| Fixation + fire rate + magazine | flat per-stack bonus; stacks come from hits | most of her damage | clip empties in ~4 s: magazine and refill items are the limit |
| Smoke dispel + anti-heal | cleanse at the start of the heal window | replaces part of Leech's anti-heal role | [U] |
| Superior Duration + every timed window (unusual) | +28% to smoke lifesteal (5 -> 6.4 s), VB, Burst Fire, Active Reload, Fixation stack time [U for items] | +762 damage (20 s) and +246 HP vs Healing Tempo, 3.2k cheaper (if Tempo does not trigger) | scenario haze_duration_windows |
| Cheat Death (rich box) vs lifesteal engine | -60% healing received during its immunity [item] | conflict | small: only during the 4.5 s save |
| Sleep Dagger + smoke + Fixation T2 | dagger from invisibility, +15 stacks, sleeping target = free hits | opener | none |

Healing Booster -> Healing Tempo priced step by step (paths at equal souls; `haze_runs.py`):
| path | 18k | 24k | 30k | 41.6k | 49.6k | 52.8k (Tempo does NOT trigger) | 52.8k (Tempo triggers off Siphon) |
|---|---|---|---|---|---|---|---|
| A rush: Tempo right after Healing Booster (22.4k), Siphon later | dies 8.1 s | dies 7.9 s | dies 10.3 s | dies 5.6 s | 345 HP | 499 HP, 5873 dmg/20 s | 1143 HP, 7364 |
| B current: Healing Booster 16k, Tempo last | dies 8.1 s | dies 10.2 s | 361 HP | 310 HP | 264 HP | 499 HP, 5873 | 1143 HP, 7364 |
| B2 ADOPT: Bullet Lifesteal 16k, Healing Booster 27.2k, Tempo last | dies 9.1 s | dies 10.6 s | 361 HP | 310 HP | 264 HP | 499 HP, 5873 | 1143 HP, 7364 |
| D skip both, Leech last | dies 9.1 s | dies 10.6 s | 23 HP | dies 11.2 s | dies 11.2 s | 840 HP, 6130 | 840 HP, 6130 |
| D2 skip both, Superior Duration last (3.2k cheaper) | dies 9.1 s | dies 10.6 s | 23 HP | dies 11.2 s | 745 HP, 6635 | 745 HP, 6635 | 745 HP, 6635 |
Reading: (a) rushing Tempo is wrong either way (it delays Siphon, its own trigger, and loses 24-41k); (b) Healing Booster is worth its 1.6k from 30k on (skipping it loses at 30-49k), but not at 16k where Bullet Lifesteal is better; (c) completing Tempo last is the best final buy ONLY if Siphon (or smoke/VB) triggers it; if nothing triggers it, Leech or Superior Duration beat it on damage and survival, and Superior Duration is 3.2k cheaper. Kieran's "Burst Fire gives comparable fire rate, sooner": confirmed at 28k: with a trigger, Tempo ~= Burst Fire + 3.2k extra souls (+43 dmg/20 s, +206 HP); without it, Burst Fire is far ahead. Burst Fire stays before Tempo.
Leech vs Vampiric Burst (Kieran's open question): VB wins at 41.6k and at full on every measure except ult damage (VB -> Leech at full: -481 burst 6 s, -1567 vs 3 targets, -2247 HP focused, dies at 7.4 s; Leech +739 ult from +12 spirit and constant lifesteal). Cause: VB's ammo refill and fire rate on a magazine-bound gun, plus 70% active stacking with smoke. Under -35% anti-heal VB's heal falls by 35% but its damage/ammo lead does not; Leech would need to cancel most of the penalty (amount [GAP]) to catch up. The Leech swap trigger ("they buy anti-heal") is therefore doubtful.

## 8. Practicality (I)
| problem | evidence | candidate fix | cost | grade | decision |
|---|---|---|---|---|---|
| Clip (55) empties in ~4 s; reload 2.35 s; fire-rate items compete for the same seconds | kit numbers; model: Burst Fire +0 in 10 s, ~+25% over 12-20 s | value refill/magazine (Titanic, Lucky Shot, VB refill) over more fire rate; reload before engaging so the smoke window is all shooting | 0 (order/playstyle) | CALCULATED 60% | keep items; no note (Kieran: notes only when needed; reloading is basic) |
| No kit sustain before 9.2k | ability table | smoke-first order (T3 at 6k); or accept | -19% damage at 6k | UNTESTABLE-HIGH-RISK 40% | leave order (Round 25 order is Kieran-approved style); flag for review |
| Farming: camp damage x3.2 at Ricochet | model | Ricochet-first when the lane is lost (existing box) | survival at 10-12k | CALCULATED 55% | keep |
| Buttons: smoke (2-4 charges), dagger, ult, VB active, Active Reload timing; Tempo/Siphon passive | build | none needed | - | - | acceptable for the style |
| Slot lock / sells | walk: 12 slots at Silencer; Active Reload sold for counters; Swift Striker sold for Frenzy | unchanged | - | - | OK |
| Forgiveness when behind | core is 52.8k; key spikes 14.4k (Ricochet), 22.4k (Siphon), 41.6k (VB) | Lost-lane box | - | - | OK |

## 9. Verdicts (E, H)
| decision | verdict | grade | confidence | what would make it wrong | deciding test |
|---|---|---|---|---|---|
| Overall thesis (gun + smoke engine + Ricochet farm) | keep as the main build | CALCULATED | 60% | sandbox shows smoke lifesteal much lower than 50% of bullet damage, or bounce/ult damage far below model | haze_ricochet_roles, haze_booster_vs_lifesteal |
| "Delay greens, Fortitude later" | reject as default; keep as Lost-lane order | CALCULATED | 60% | income data showing Ricochet 3 min earlier pays back the 10-12k weakness | UNSUPPORTED (no camp/income op) |
| Bullet Lifesteal 16k <-> Healing Booster 27.2k | CHANGE (pure reorder, same items/colour/spikes) | CALCULATED | 65% | Healing Booster amplifying lifesteal by far more than +20% | haze_booster_vs_lifesteal |
| Healing Booster | keep (now 27.2k) | CALCULATED | 60% | heal amp not applying to lifesteal (then it is worth ~+30 HP per 1k) | haze_booster_vs_lifesteal |
| Healing Tempo | keep, inconclusive; replace with Leech (or Superior Duration if its windows stretch) if nothing in the build triggers it | UNTESTABLE until tested | 50% | - | haze_tempo_trigger (decisive, existing ops `mods`/heals csv/acclog) |
| Rush Tempo before Siphon | reject | CALCULATED | 75% | - | - |
| Vampiric Burst core | keep | CALCULATED | 65% | Leech's anti-heal reduction near total and anti-heal present all fight | haze_vb_vs_leech (anti-heal arm UNSUPPORTED) |
| Leech swap "vs anti-heal" | keep box for now, flagged doubtful | UNTESTABLE-HIGH-RISK | 40% it helps | eheal op result | blocked: eheal |
| Ricochet at 14.4k | keep; valued on farm + fire rate + ult x2.9 + 3-target fights | CALCULATED | 70% | bounces not applying in ult | haze_ricochet_roles |
| Fortitude | keep (HP and early survival; regen overlaps smoke-on-camps) | CALCULATED | 60% | - | - |
| Siphon Bullets | keep | CALCULATED | 55% | steal not counting as healing/HP | haze_tempo_trigger (heal log) |
| Burst Fire | keep, before Tempo | CALCULATED | 60% | magazine test shows fire rate fully usable | haze_magazine_bound |
| Extra Charge / Rapid Recharge | keep (cleanses, multi-fight); Extra Charge alone is dead weight for 8.8k souls (cost audit's LOW flag stands) | CALCULATED | 55% | charges refilling in parallel | UNSUPPORTED (charge readers unreliable) |
| Silencer | keep | UNTESTABLE-HIGH-RISK | 50% | - | blocked: CC/bot shoot-back |
| Superior Duration (new idea) | candidate only, not added | UNTESTABLE until tested | 45% | item actives not extended | haze_duration_windows |
| Smoke-first ability order | not adopted | UNTESTABLE-HIGH-RISK | 40% | - | blocked: per-ability tier op (GAPS #2) |
| Spirit hybrid rival | reject for this build | CALCULATED | 70% | - | - |

## 10. Regression of the change (F)
Changed build (council/work/haze.js): walk1 FLAGS none; gun 4.8k @4.8k, health 4.8k @16k (Bullet Lifesteal is green like Healing Booster); 12 slots at Silencer; sp.js tiers unchanged; Healing Booster bought at 27.2k as a fresh T2, but it is upgraded later (Healing Tempo) and takes the slot the fresh T2 Bullet Lifesteal held, so no new late-T2 problem. Vampiric Burst still upgrades Bullet Lifesteal; Healing Tempo still upgrades Healing Booster. New weakness: none found; 16-27k gains +1.0 s / +0.4 s focused survival and +2% damage, 27k+ identical.
Unchanged notes worth a reviewer's look: Healing Booster's note "Buffs all your lifesteal, smoke T3 included." claims an unverified mechanic (amp on lifesteal) - keep or empty after haze_booster_vs_lifesteal; the Leech swap trigger (section 7).

## 11. Sandbox plan (existing ops only)
| scenario | runnable now | decides |
|---|---|---|
| haze_tempo_trigger | yes (give, lowhp, cast 2 / i1, fire, mods, acclog, healsum) | Healing Tempo keep/replace |
| haze_booster_vs_lifesteal | yes | reorder + Healing Booster value |
| haze_vb_vs_leech | yes, except the anti-heal arm (no eheal) | VB core |
| haze_duration_windows | yes (Superior Duration is not an imbue); Duration Extender UNSUPPORTED (no imbue op) | Superior Duration candidate |
| haze_ricochet_roles | yes for fight roles (enemies 3, cast 4); farming UNSUPPORTED | Ricochet roles |
| haze_magazine_bound | yes (scripted reloads); Active Reload timing UNSUPPORTED | fire rate vs magazine |
| haze_engine_countered | proxy only ("no smoke"); silence/stun (ecc), anti-heal (eheal), shoot-back UNSUPPORTED | A2 severity |
All scenarios inherit one limit: `unlock 7` gives all three tiers to every ability, so 5k-24k ability states cannot be reproduced; results are late-game relative comparisons.

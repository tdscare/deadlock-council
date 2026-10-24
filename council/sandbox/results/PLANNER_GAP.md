# PLANNER GAP list (build-optimisation experiments cannot show plain-English strategy yet)

Written 2026-10-24 14:10 local. Rule: BUILD-class experiments need meta player_title/player_what/player_why/player_short (<=60 chars each), strategy_source, and (isolated items inside a build investigation) feeds. None of the 81 builds has them; until the planner/theorycrafter supplies the reasoning, the screen shows a plain factual line only and `queue.js design-sweep` has set all 243 per-build tasks to paused-needs-design (they are not run).

## Root cause of the unreadable text
- Scenario meta fields were developer labels (kind, checkpoint 'stat floor', purpose 'validate the harness'); the display printed them verbatim.
- No strategic reasoning exists in machine-readable form: council/tools/gen_scenarios.js has real question/hypothesis for only 5 scenarios and `hypothesis:'defined per use'` placeholders for the generic templates; sandbox/plans/*.md are mechanical (items per soul total, rotations); no alternatives / tradeoffs / missing_evidence fields exist; the theorycrafter field names (agent a54eb22ad2fa86134) were not in sandbox/SCHEMA.md at 14:10.
- The 243 per-build tasks (81 builds x stage0-setup-truth, stage0-known-answer, plan-experiments) have no scenario files at all.

## Per build: what exists / what is missing (all missing: player_*, strategy_source, alternatives, tradeoffs, missing_evidence, scenario file)

| build | gen_scenarios question+hypothesis | weaknesses file |
|---|---|---|
| abrams | none | yes |
| abrams_melee | none | yes |
| apollo | none | none |
| apollo_melee | none | none |
| baba | none | none |
| baba_tank | none | none |
| bebop | none | none |
| bebop_bomb | none | none |
| bebop_support | none | none |
| billy | none | none |
| billy_damage | none | none |
| calico | none | none |
| calico_gun | none | none |
| celeste | none | none |
| celeste_carry | none | none |
| danny | none | none |
| danny_gun | none | none |
| doorman | none | none |
| doorman_support | none | none |
| drifter | none | none |
| drifter_spirit | none | none |
| dynamo | none | none |
| dynamo_damage | none | none |
| geist | none | none |
| geist_bomb | none | none |
| graves | none | none |
| graves_tank | none | none |
| graves_ult | none | none |
| greytalon | none | none |
| greytalon_gun | none | none |
| haze | haze_smoke_lifesteal_jumped | yes |
| haze_assassin | none | none |
| holliday | none | none |
| holliday_spirit | none | none |
| infernus | none | none |
| infernus_dash | none | none |
| ivy | none | none |
| ivy_carry | none | none |
| kelvin | none | none |
| kelvin_support | none | none |
| lash | none | none |
| mcginnis | none | none |
| mcginnis_turret | none | none |
| mcginnis_ult | none | none |
| mina | none | none |
| mirage | none | none |
| mokrill | none | none |
| nurse | harrow_burst_fire_ally | none |
| paige | none | none |
| paige_support | none | none |
| paradox | none | none |
| paradox_bomb | none | none |
| pocket | none | none |
| ratking | none | none |
| ratking_grenade | none | none |
| rem | none | none |
| seven | none | yes |
| seven_gun | none | none |
| shiv | none | none |
| shiv_gun | none | none |
| silver | none | none |
| sinclair | none | none |
| sinclair_bolt | none | none |
| solomon | none | none |
| solomon_support | none | none |
| venator | none | none |
| venator_grenade | none | none |
| victor | victor_vs_three, victor_sustain_three | yes |
| victor_gun | victor_vs_three | yes |
| vindicta | none | none |
| vindicta_sniper | none | none |
| violet | none | none |
| violet_spirit | none | none |
| viscous | none | none |
| viscous_damage | none | none |
| vyper | none | none |
| vyper_gun | none | none |
| warden | none | none |
| wraith | wraith_leech_vs_vampiric | yes |
| yamato | none | none |
| yamato_brawler | none | none |

## Interaction gaps recorded by abtimeline.py --interactions (2026-10-24; data-derived, not reasoned around)
Rule: an UNKNOWN cell is a gap with a queued test, not a judgement. Current open cells (Haze/Wraith worked examples):
- Haze Fixation x weapon % (Close Quarters, Point Blank, any % item): the per-stack bonus is a flat bullet-damage add (DamageBonusFixedPerStack, EBaseWeaponDamageIncrease); whether weapon % multiplies it is not in the data. Queued: haze:interaction:Close_Quarters_3_Fixation_T2_..., haze:interaction:Point_Blank_3_Fixation_T3_...
- Haze reload time: not in vdata (ASSUMED 2.5 s); decides magazine vs fire-rate items. Queued: haze:interaction:reload_probe. (Wraith's 2.82 s is MEASURED.)
- Bullet Dance ammo use (whether the ult consumes the magazine): not in data; priced both ways, it did not change any verdict, so no test was requested yet.
- Not determined anywhere: hit rate, headshot share, close-range share, ult target spread (ASSUMED in IA_P); timed fire-rate buffs (Kinetic Dash, Heroic Aura, Active Reload) are upper bounds; proc items without a damage value are counted, not priced.

## Gaps from discovery / remedy sets (2026-10-24, generated, not reasoned around)
- Ally-target cells (self-cast items while attached via an ally-attach ability; on-hit items triggered by bullets that hit allies): UNKNOWN in data and BLOCKED in the runner (no allied bot op, GAPS 10). Requests queued with `meta blocked_by`.
- Weapon-% bonuses on ordinary melee and on melee-scaled abilities: UNKNOWN in data (melee uses ELightMeleeDamage); melee requests queued (`cast melee`, 150u).
- Reach model (melee uptime vs move speed / slows) and the trade model behind remedy scores are ASSUMED; a chase scenario (flee bot, distance readback) would replace them.
- Score per 1000 souls favours cheap items when gains are non-linear; equal-souls bundles go through --strategy.
- Resist-shred formula below 0 resistance and proc/buff uptime for items without a stated cooldown are not modelled yet (listed as UNKNOWN cells when an item has them).

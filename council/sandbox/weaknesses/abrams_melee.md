# Weakness sweep: abrams_melee ("Rizuhble's Fists Of Law Abrams")
Solver: weakness-solver, 2026-10-24. Process: council/WEAKNESS_PROCESS.md. Sources: data.js (id abrams_melee), audit/items_full.json, audit/hero_abrams.txt, sandbox/GAPS.md, sandbox/playstyle/abrams.md, council/RULES_KIERAN.md, AUTORUN.md ops. data.js was not touched; nothing here is applied.
Tags: [kit] read from data, [GAP] number not in the data (measure it), [U] game knowledge to verify. Hero enum for `setup`: Atlas (hero_enum.txt).

## 0. Hero identity map and ranked dependency chains (WEAKNESS_PROCESS A2) and evidence grades (H)
Grades used: MEASURED (valid sandbox result above A/A noise; sandbox, not live game), CALCULATED (kit maths, assumptions stated), UNTESTABLE-HIGH-RISK (depends on positioning, travel time, enemy reaction, CC timing, stacking; confidence capped at 50%; verdict can only be keep current / situational note). No test in this file has been run yet, so nothing below is MEASURED; every verdict is CALCULATED or UNTESTABLE-HIGH-RISK and is worded accordingly.

### Identity map (melee build)
| strength [kit] | compensates for | dependency / condition | verified enemy counters (item/ability data) |
|---|---|---|---|
| Shoulder Charge (1.4 s, pin, wall stun, T1 slow) | no ranged poke, no other gap closer | cooldown [GAP], needs line to target, turn rate limited (TurnRateMax 140, side speed -65%), wall for stun | Silence Wave (3 s silence, 40 m), Cursed Relic (3.25 s interrupt/silence/disarm/no items, 20 m), Knockdown/stuns before cast, Slowing Hex (16% slow), dashing out of the path, Cold Front/Arctic Blast slows |
| Seismic Impact (leap, 9 m radius, 1.6 s stun, T3 5 s Unstoppable) | no hold on groups, CC vulnerability | cooldown [GAP], T3 for the Unstoppable | same silences/interrupts before it fires; spreading out |
| Lifestrike, Melee Lifesteal, Restorative Shot, Infernal Resilience regen | low health pool, no escape | melee contact with a hero (30-40% on NPCs); regen is 13% of damage taken over 20 s | Healbane -35%, Decay -50%, Spirit Burn -70%, Toxic Bullets (HealAmp penalties on receive and regen); kiting (no contact = no heal); burst larger than 20 s regen |
| Slows on hit (Lifestrike 48% 2.5 s, Point Blank 20% 2 s, Colossus 24% 7 s, Charge T1) | no way to follow a runner | first contact; slows may not stack [GAP #18] | Enduring Speed 25% / Juggernaut 50% / Fleetfoot 40% slow resist, dash/teleport/invulnerability (Ethereal Shift), Divine Barrier and Dispel Magic cleanse |
| Colossus (+35% resists, 24% slow, +30% melee, 7 s) | burst and kiting during commit | active, pop before contact | silence/Relic stops the item use; waiting out 7 s |
| Berserker (7 weapon power per 120 damage taken) | low damage ramp | damage taken, 10 s | kiting/denying hits; damage over time that does not stack |

### Ranked chains (frequency x lethality; frequency [U] from item prevalence, not measured)
1. Chain A: Charge/ult are the only engage; a silence, interrupt or hard CC before they fire (Silence Wave, Cursed Relic, stuns) leaves a melee hero walking at a kiter. Common (silence items are standard), lethal (no damage output without contact). PREVENT: bait the first CC with the cheaper ability, Enduring Speed 25% slow resist and Infernal T3 20% debuff resist shorten slows, Debuff Reducer (1.6k, not in build) shortens everything, fight near cover so they must come to you. RECOVER: Dispel Magic and Divine Barrier (menu/rich) remove non-stun debuffs; Phantom Strike (25 m, pull) as the second engage; Colossus pop is itself blocked by silence. SURVIVE: Colossus/Spirit Resilience/Lifestrike heal once in, Berserker stacks from damage taken. Enemy counters to the answers: cleanse on cooldown, a second silence, Unstoppable cannot be used while already stunned, Divine Barrier does not remove stuns, Cursed Relic stops item use (Colossus, Phantom Strike) too.
2. Chain B: sustain by melee contact; anti-heal plus kiting turns the build into low-health damage without sustain. Common (25 builds carry anti-heal), medium lethality. PREVENT: kill the healer first, Healbane in Counters menu; Leech reduces the effect of anti-heal (not in build). RECOVER: none cheap. SURVIVE: Infernal regen, Spirit/Bullet Resilience, Colossus. Counter to answers: anti-heal larger than Leech's reduction, burst faster than regen.
3. Chain C: slow-based retention; slow-resist items, dashes or cleanse remove the hold and the build cannot restart contact. Medium frequency, medium lethality. PREVENT: apply slows from two sources (Lifestrike + Point Blank), Crushing Fists stun at 6 stacks. RECOVER: Phantom Strike. SURVIVE: accept the lost target. Counter to answers: stacking rules unknown [GAP #18].
4. Chain D: damage before contact (gun poke, spirit burst) while approaching. PREVENT: Charge from range, cover. RECOVER: Warp Stone-type bullet resist (not in build). SURVIVE: Colossus, Spirit Resilience, Hunter's Aura -15%/-30% fire rate, counters menu. Counter: focus before the Charge comes up.

## 1. Build snapshot (what the sweep was run against)
Buy order (core, left to right), cumulative souls and colour spend (upgrades count only the difference; computed from items_full tiers 800/1.6k/3.2k/6.4k):
Restorative Shot 0.8k > Close Quarters 1.6k > Melee Lifesteal 2.4k > Melee Charge 4.0k > Stalker 5.6k (weapon 4.8k) > Lifestrike 8.0k > Sprint Boots 8.8k > Enduring Speed 9.6k (health 4.8k) > Spirit Strike 10.4k > Bullet Resist Shredder 12.0k > Point Blank 14.4k > Spirit Snatch 16.8k (spirit 4.8k) > Hunter's Aura 20.0k > Crushing Fists 24.8k > Berserker 28.0k > Spirit Resilience 31.2k > Extra Health 32.0k > Colossus 37.6k > Phantom Strike 44.0k.
Held at 12 slots after upgrades/sells (Restorative Shot -> Berserker): Lifestrike, Enduring Speed, Stalker, BRS, Point Blank, Spirit Snatch, Hunter's Aura, Crushing Fists, Berserker, Spirit Resilience, Colossus, Phantom Strike. Colour totals at 44k: weapon 18.4k, health 20.8k, spirit 4.8k.
Kit tools that already bear on reach/retention [kit]: Shoulder Charge (1.4 s, 18.75 -> 30 m/s [U units], pushes a hero, wall = stun, T1 slow 3 s, T2 wall stun +0.8 s, T3 -18 s cooldown); Seismic Impact (leap, 9 m radius [+6 m at T3], 1.6 s stun, T3 5 s Unstoppable on cast); Lifestrike (48% slow 2.5 s on any melee hit, light hits at 1.5x cooldown); Point Blank (20% slow 2 s on bullets within 15 m); Colossus (24% slow aura 14 m, -22% dash speed, 7 s); Hunter's Aura (-15% fire rate, doubled vs one enemy); Enduring Speed (+2 m/s, 25% slow resist); Infernal Resilience T3 (+20% debuff resist).
Kieran 13:06 (Round 20 update 2, in data.js changes): "Shoulder Charge slows and pins, Point Blank slows and the ult stuns, so the kit already catches people", which is why Weighted Shots was dropped. This sweep treats that as a hypothesis to confirm with tests, not as a ruling.

## 2. Shared test protocol (every block below uses it)
Block macro BLOCK(arm, N, D):
```
setup Atlas Haze            # once per scenario file
aimoff 5.5 3                # only calibrated for 350u; D != 350 needs `fetch` only (melee/ability aim is at the bot)
hardreset                   # fresh pawns, no items/buffs, cooldowns factory (AUTORUN)
souls N
give <arm class list, upgrades only, no components>
unlock 7                    # upper bound: all tiers (GAPS #2 says real order has fewer tiers early)
basemods
ekeep 1
ehp 50000
fetch D
mark <label>
... arm script ...
mark none
wait 1
```
Rules: arms run A,B,B,A counterbalanced, n=6 blocks per arm, A/A (base vs base) n=6 first to get the noise floor; an effect counts only if |delta| > max(2 x SD of A/A, one script chunk). Validity per PILOT 0.2: log hero, level, souls, items, stacks, enemy hp; mismatch = rerun. Item active slots: give actives one at a time in a fixed order and confirm `cast iN` maps (probe P4 below); `give` of upgrade classes only (GAPS #22).
Class names (item_commands.json): Lifestrike upgrade_boxing_glove; Enduring Speed upgrade_cardio_calibrator; Stalker upgrade_weapon_backstabber; BRS upgrade_bullet_resist_shredder; Point Blank upgrade_close_quarter_combat; Spirit Snatch upgrade_spirit_snatch; Hunter's Aura upgrade_bullet_armor_reduction_aura; Crushing Fists upgrade_crushing_fists; Berserker upgrade_berserker; Spirit Resilience upgrade_tech_purge; Colossus upgrade_colossus; Phantom Strike upgrade_phantom_strike; Warp Stone upgrade_warp_stone; Slowing Hex upgrade_containment; Mystic Slow upgrade_magic_slow; Fleetfoot upgrade_fleetfoot_boots; Majestic Leap upgrade_rocket_booster; Unstoppable upgrade_unstoppable; Debuff Reducer upgrade_debuff_reducer; Witchmail upgrade_absorbing_armor.
BASE11 (37.6k) = boxing_glove, cardio_calibrator, weapon_backstabber, bullet_resist_shredder, close_quarter_combat, spirit_snatch, bullet_armor_reduction_aura, crushing_fists, berserker, tech_purge, colossus.
BASE7 (20.0k) = boxing_glove, cardio_calibrator, weapon_backstabber, bullet_resist_shredder, close_quarter_combat, spirit_snatch, bullet_armor_reduction_aura.

### Probes (cheap, run once per patch, results gate the tests that depend on them)
- P0 unit calibration (m to u). `hardreset; souls 20000; unlock 0; fetch 150; ehp 50000; enemies 3 R` then `mark ring_R; cast 1 2; mark none` for R in {250,290,315,340,380,430}. Siphon radius is 8 m at unlock 0, so the cut between R that take Siphon damage and R that do not gives u per m (expected ~39.4 [U]; GAPS #3 implies 37-50). Needs Siphon unlocked (give no items). Status: RUNNABLE; ring placement was not independently confirmed (AUTORUN), so pass = a clean monotonic cut. All distances below use k = u per m from P0; provisional k = 39.4 (8 m = 315u, 12 m = 473u, 20 m = 788u, 28 m = 1103u).
- P1 hooks: do `incoming`/`hurtme` feed Infernal Resilience and Berserker? `hardreset; souls 30000; give upgrade_berserker; basemods; healreset; mark p1a; wait 5; incoming gun 300; wait 6; mods; incoming off; wait 8; healsum; mods; mark none`. Pass: `mods` lists a Berserker-stack modifier name and healDiffObserved in the 8 s after exceeds the p1a regen. Fail = Berserker and Infernal regen can never be scored with streams (GAPS #6); tests marked (H) become biased and say so. RUNNABLE.
- P2 reach envelope of the kit's own tools. For D in {10,15,20,25,30,35,40} m: `hardreset; souls 30000; unlock 7; fetch D*k; ehp 50000; mark r_ch_D; cast 2 1.8; mark none; wait 6` then the same with `cast 4 1.8` (Seismic) and `hold 2 1.8`. Hit = a damage row victim=enemy from the ability in the damage csv. Gives max effective range of Shoulder Charge and Seismic Impact [GAP: not in data]. RUNNABLE.
- P3 wall presence: `fetch 600; cast 2 1.8; mods` at the 350/600/900u gap in dl_midtown; a stun-type modifier name on the enemy means a wall was behind the bot. If never: Charge-wall stun, T2 wall stun and "Melee Charge pins them" cannot be tested (UNSUPPORTED, no wall op). RUNNABLE as a probe only.
- P4 slow/debuff presence and duration (names only, magnitude cannot be read; no velocity logging): for each source run `hardreset; give <item>; fetch 300; mark p4_X; <apply>; mods; wait 1; mods; wait 2; mods; wait 4; mods` with apply = `cast melee 0.4` (Lifestrike), `fire 1.5` (Point Blank at 10 m), `cast 2 1.8` (Charge), `cast i1 0.5` (Colossus, Phantom Strike, Warp Stone, Slowing Hex). Expect: slow modifier present after apply, gone by about the kit duration (Lifestrike 2.5 s, Point Blank 2 s, Colossus 7 s, Phantom Strike 3 s, Charge T1 3 s [kit]). Also confirms `cast i1` hits the item. RUNNABLE (names/duration); slow percentage and stacking of two slows (GAPS #18) UNSUPPORTED.

## 3. Weakness sweep (table form per WEAKNESS_PROCESS G)
Severity = how often x how costly (H/M/L). "Kit solves it?" is the first filter. Verdicts are provisional where the test is UNSUPPORTED and say so.

| id | weakness (category) | sev | evidence | remedies considered | chosen | cost | tests | verdict (confidence) | new weaknesses |
|---|---|---|---|---|---|---|---|---|---|
| M1 | Cannot catch mobile / flying / dashing targets (reach) | H early-mid, M late | Charge range-limited and on cooldown; build has no gap closer before Phantom Strike at 44k; Kieran's note says kit already catches; Phantom Strike note already tells the flyer/dasher case | Section 4 (all classes) | Keep core; playstyle note; Phantom Strike stays last (flyer trigger already in its note); Warp Stone/Slowing Hex as named fallbacks only | 0 souls now | P2, P4, R1, R2 (proxy), true flee UNSUPPORTED | LEAVE ALONE core + playstyle note (medium-low until P2/P4/R1) | Re-check if R1 shows Charge reach below about 20 m |
| M2 | Damage taken while approaching (survival / kiting) | M | Gun heroes shoot during the approach; Hunter's Aura needs 15 m; Colossus only 7 s | Warp Stone (30% bullet resist 6 s), Colossus pre-pop, Metal Skin (in Counters), Hunter's Aura, approach with Charge | Leave; counters menu already covers | none | R3 (HP lost before contact under `incoming gun`) | LEAVE ALONE (medium) | none |
| M3 | Burst / focus fire by 3-5 once in the fight (survival) | M-H mid | Health only 4.8k until 31.2k (no vitality between 9.6k and 31.2k other than Lifestrike/Enduring); rule says Abrams goes green right after first damage spike, done | Pull Spirit Resilience before Hunter's Aura; Extra Health/Toughness earlier; Witchmail (rich) | Keep order; counters menu; Spirit Resilience note already says buy earlier vs spirit | 0 | R4 survival curve (stream, flagged H) | LEAVE ALONE (low-medium; Hunter's Aura fire-rate slow is invisible in the sandbox so the comparison favours the swap) | A swap trades damage shred for health |
| M4 | CC: stun chains, silences, slows, disarm (CC/counterplay) | M | No `ecc` op; Unstoppable only in rich box; Infernal T3 +20% debuff resist, Enduring Speed 25% slow resist, ult T3 5 s Unstoppable | Debuff Reducer (1.6k, component of Unstoppable), Unstoppable (in rich), Juggernaut (slot locked), timing the ult | Leave; ult is the cleanse | 0 | UNSUPPORTED (need `ecc`); only `mods` check that ult cast gives an Unstoppable modifier (P5 below) | LEAVE ALONE, cannot determine (low) | Unstoppable is unusable once stunned, so it needs bait awareness |
| M5 | Enemy healing reduction on a sustain-by-melee hero (output/sustain) | M | Sustain comes from Lifestrike, Melee Lifesteal, Restorative Shot, Infernal regen; 25 builds buy anti-heal; no `eheal` op | Leech (T4, reduces effect of enemy anti-heal; Abrams has no spirit/bullet lifesteal otherwise), Dispel Magic, kill them first | Accept | 0 | UNSUPPORTED (`eheal`) | LEAVE ALONE, cannot determine (low) | Leech would cost a rich slot |
| M6 | Heavy-melee windup and downtime; light vs heavy mix (output) | M | `cast melee` has no light/heavy split (GAPS table); Lifestrike light = 1.5x cooldown, Spirit Strike/Snatch light worse | Melee Charge/Crushing Fists already core; Hex-Sealed Knuckles (T3, +heavy 200 spirit) | Leave | 0 | UNSUPPORTED (`melee light|heavy` op) for the split; total melee output measurable (R5) | LEAVE ALONE (low) | none |
| M7 | Wall dependence of Charge stun and "guaranteed heavy" (positioning) | M | Melee Charge note and Crushing Fists rely on walls; map walls unverified (playstyle note) | Position fights near walls; skip if no wall | Playstyle | 0 | P3 probe; wall effect itself UNSUPPORTED (no wall op) | LEAVE ALONE (low) | none |
| M8 | Berserker / stack dependence (snowball) | L-M | Berserker needs 120 damage taken per stack [kit], 10 s duration, 7 weapon power per stack, bought at 28k | Order earlier (needs damage to be useful), drop | Leave | 0 | P1 hook probe, then R4 with 0/mid/max stacks | LEAVE ALONE (low) | Stacks may not charge on `incoming` (P1) |
| M9 | Farming / economy: punch-camps only, no scaling farm tool (economy) | M | playstyle: heals off NPCs at 30-40%, Restorative Shot NPC 20 | Cultist Sacrifice (6.4k) if lane is lost, Extra Regen box already there | Leave; existing Losing lane box | 0 | UNSUPPORTED (no NPC/camp op; generic_camp_clear not in autorun/scenarios) | LEAVE ALONE (low) | none |
| M10 | Late slot lock and sell chain (economy/slot) | L | 19 buys fold to 12 slots; Phantom Strike is the 12th and the last buy at 44.0k | Move Phantom Strike ahead of Colossus when a flyer is on their team (already in its note) | Leave | 0 | none needed | LEAVE ALONE (medium) | none |
| M11 | Escape / disengage when losing (survival) | L-M | No dash-away; Colossus slow does not help leaving; rich box has Ethereal Shift (invuln 4 s) and Divine Barrier; Warp Stone and Majestic Leap are the only cheap options | Warp Stone (backwards), Majestic Leap (45 s, barrier 200), Ethereal Shift in rich | Leave | 0 | UNSUPPORTED (no chaser bots/damage output) | LEAVE ALONE (low) | none |
| M12 | Multiple enemies: heavy melee hits one; Siphon only T1 late (output/target count) | L-M | Siphon is low priority in this build; ult 9 m radius covers groups | Leave | Leave | 0 | R6 optional (ring of 3-5, ult + melee) | LEAVE ALONE (low) | none |

Sweep categories checked and rated below the bar: finishing kills (no execute need; melee burst + Lifestrike), ammo/reload (gun is secondary; Crushing Fists refills ammo), ramp-up (Berserker M8), range limits (M1), armour/resist scaling (BRS, Snatch, Aura shred in build; enemy resist runs `eresist gun 25/50` can be added to R5 with no new ops), objective fights/team needs (UNSUPPORTED: no ally ops).

## 3b. Evidence grade per verdict (H)
| id | verdict | grade | confidence | what would make this wrong |
|---|---|---|---|---|
| M1 | leave core; Phantom Strike stays last; playstyle note | UNTESTABLE-HIGH-RISK (chase, dashes, cleanse); reach and slow-presence parts CALCULATED until P2/P4/R1 run | <=50% | P2 shows Charge reach under about 20 m, P4 shows Lifestrike/Point Blank slows do not apply or do not stack, or R1 shows Warp Stone/Slowing Hex closing far more at 20k |
| M2 | leave | CALCULATED (R3 stream is a proxy) | 40% | R3 shows large HP loss before contact that Warp Stone's 30% resist halves |
| M3 | leave | UNTESTABLE-HIGH-RISK (focus fire, Hunter's Aura slow invisible, P1 hook unknown) | 35% | R4 time-to-die much lower at 20k than with Spirit Resilience pulled forward, with P1 passing |
| M4 | leave | UNTESTABLE-HIGH-RISK (no `ecc`) | 30% | any CC test op; Unstoppable window vs real stun chains |
| M5 | accept | UNTESTABLE-HIGH-RISK (no `eheal`) | 30% | `eheal` runs showing Lifestrike/Infernal heal falling below usefulness at -35% |
| M6-M12 | leave | CALCULATED or UNTESTABLE-HIGH-RISK as stated per row | <=40% | the per-row test named in section 3 |
Rule check: no row changes a core build, which is the only action allowed on these grades.

## 4. Deep dive: "catching mobile enemies" (M1), all remedy classes
Why it matters: the weakness is first contact, not retention. Once a melee hit lands, Lifestrike gives 48% slow for 2.5 s (any melee hit, light ones included) and Point Blank adds 20% for 2 s inside 15 m, so a ground target is held. What the build lacks is a gap closer before the first hit when Charge (cooldown [GAP], T3 -18 s) and Seismic Impact (leap range [GAP]) are down, and any answer to a target that is airborne or has a dash, teleport or slow resist.
Closing model (kit maths, assumptions explicit): gap G m, my speed v_me [GAP; Enduring Speed +2 m/s], their run v_them (7-8 m/s [U]). Walking closes G in G/(v_me - v_them) s only if v_me > v_them; otherwise never. A burst tool reduces G instantly by its reach r (Charge r_c [GAP, P2], Warp Stone 11 m, Phantom Strike 25 m cast range then a pull). Utility to damage: extra damage = (seconds of contact gained) x (measured melee DPS of the build, R5) x P(counterplay fails). Contact gained = time saved closing + hold time after the tool (slow x its duration, pull, disarm). Gain disappears when: the target has a dash/teleport/invulnerability off cooldown, my tool is on cooldown (Phantom Strike cooldown is not in the data [GAP]), line of sight breaks (Phantom Strike and Slowing Hex need a target), the enemy parries (Counterspell) or cleanses non-stun debuffs (Divine Barrier, Dispel Magic), or the slow is reduced by their Enduring Speed/Juggernaut (25%/50% slow resist) or my slow does not stack with theirs.

| class | candidate | cost / price point | what it removes | utility to damage and when the gain disappears | test | verdict |
|---|---|---|---|---|---|---|
| Item: gap closer + hold | Phantom Strike (in build, last) | 6.4k (swap for Colossus+Extra Health, exact tie), arrives 44k | Reach 25 m, pull to ground (flyers), 40% slow 3 s, disarm; the one tool that reaches an airborne target | Contact gained about 25 m of reach plus a 3 s hold; at 40% slow a 7.5 m/s runner moves 4.5 m/s, so a walker with Enduring Speed closes any gap under about 10 m in the hold. Gain gone on parry/cleanse, no line of sight, cooldown [GAP], and after 3 s | P4 (slow modifier + cast i1), R1 arm C | KEEP as is (medium) |
| Item: gap closer, no hold | Warp Stone | 3.2k; 20k arm = replaces Hunter's Aura (tie), 37.6k arm = replaces Spirit Resilience (tie) | 11 m forward teleport and 30% bullet resist for 6 s, so it doubles as approach armour (M2) and escape (M11) | Contact gained = 11/(v_me - v_them) s if the target keeps walking, else the whole chase; no hold, so a dash after the teleport undoes it; teleport is straight, so aim matters | R1 arms B and B20, R3 | Not added now; named fallback if R1 shows B20 beats base at 20k by more than noise and P2 shows Charge reach is short (low-medium) |
| Item: slow / movement lock | Slowing Hex | 1.6k, ties with BRS at 12k | 16% slow 3.5 s, silences their dash items and abilities, cast range 25 m, cooldown 29 s; the only cheap anti-dash | Gain gone if they have no dash (then 16% is small), on cooldown, no line of sight, cleansed (Dispel Magic) | R1 arm D, P4 | Not added (medium-low); best cheap anti-dasher if a hole shows |
| Item: slow aura | Colossus (in build, 37.6k) | 5.6k + Extra Health | 24% slow and -22% dash speed in 14 m for 7 s, plus 35% resists | Needs to be popped before contact (the active is the commit tool, note says pop as you ult in); lasts 7 s only | P4 | KEEP |
| Item: slow on hit | Lifestrike, Point Blank (in build) | in build | 48% and 20% slows after first contact | Applies after contact, so it keeps targets, does not start the chase | P4 | KEEP |
| Item: movement stats | Sprint Boots + Enduring Speed (in build); Fleetfoot (1.6k weapon colour, +3 m/s for 5 s), Kinetic Dash, Extra Stamina, Majestic Leap (3.2k, 45 s), Magic Carpet, Veil Walker | Enduring Speed already core at 9.6k; others cost a slot or an off-colour spike | +speed only closes a gap if v_me > v_them; Fleetfoot raises closing speed by about 40% for 5 s | Gain gone against equal-speed runners; Majestic Leap is a gap closer only vertically/over walls | R1 arm E (Fleetfoot, 1.6k tie with BRS; moves 1.6k from spirit to weapon and slips the spirit 4.8k from 16.8k to 18.4k) | Not added (low) |
| Ability use | Charge from max range (never walk up), ult for the stun, Seismic then Charge order, light punch first to apply the 48% slow, Crushing Fists stun at 6 stacks | free | Uses the kit's reach before items | Gain gone when both are on cooldown; the playstyle note already says Charge into wall | P2, R1 arms F (charge first), G (ult first) | CHANGE playstyle note (proposal, below) |
| Positioning | Funnel targets to walls/corners so Charge pins, approach from the side lane out of sight, fight inside cover | free | Removes the open-field chase | Gain gone when no wall near (P3) | P3 | playstyle |
| Target selection | Hit grounded, slow-resist-free targets; ignore the flyer/teleporter, pressure with Charge only when it commits, farm/side objectives instead | free | Avoids paying souls to chase one hero | Gain gone only if the dasher is their carry and nobody else can reach it | n/a (decision rule) | playstyle |
| Team | Ally slow/stun/pull sets up the first hit (duo partner with a pull, stun, or mark); see Duo Builder | free for this build | First contact | Needs the partner in lane/team; UNSUPPORTED in the sandbox (no ally op) | UNSUPPORTED | pair suggestion only (low) |
| Accept | Do not fix: kit catches grounded targets; fliers are rarer than the cost of a slot | 0 | n/a | n/a | n/a | default outcome (medium) |

Decision for M1: leave the core as it is; keep Phantom Strike last with its flyer/dasher trigger; no Warp Stone, Slowing Hex, Fleetfoot or Weighted Shots added unless R1/P2 disagree. Proposed playstyle note (for playstyle/abrams.md, not applied): "Open with Charge from as far as it reaches, not by walking; one punch lands the Lifestrike slow; save the ult for the second dash or a group; skip a target that flies or teleports until Phantom Strike." Test status: ability reach, slow-modifier presence/duration, tool-versus-tool first-contact latency are RUNNABLE; true fleeing/dashing behaviour, enemy cleanse and slow stacking are UNSUPPORTED (no `emove`, `ecc`), so the verdict is kit maths plus static reach.

## 5. Test specifications (runnable with AUTORUN ops unless marked)
Common header for each scenario file: `setup Atlas Haze`, `aimoff 5.5 3`. `k` from P0. Each arm = one BLOCK.

### R1 first-contact latency (M1)  RUNNABLE
Hypothesis: for a static target at gap D, a gap closer lowers time to first melee hit; Charge-first lowers it more than any item; Phantom Strike hits at 25 m. Varied thing: one item swap (tied price) or one opening move. Price points: 37.6k (BASE11) and 20k (BASE7).
Arms (37.6k): A base (BASE11); B Spirit Resilience -> Warp Stone; C Colossus -> Phantom Strike (6.4k tie); D BRS -> Slowing Hex (not in BASE11 order: use BASE11 minus bullet_resist_shredder plus upgrade_containment); E BRS -> Fleetfoot; F base opening with Charge; G base opening with Seismic. 20k: A20 BASE7; B20 Hunter's Aura -> Warp Stone.
Gaps D in {8, 12, 20, 28} m (x k). Scripts (chunk = `move` 0.5 s then `cast melee` 0.4 s, 8 chunks):
```
# A / baseline walk
move 1 0 0.5 ; cast melee 0.4     # x8
# B Warp Stone first, then walk
cast i1 0.3 ; move 1 0 0.5 ; cast melee 0.4   # then x7
# C Phantom Strike first
cast i1 0.6 ; cast melee 0.4 ; (cast melee 0.4 x6)
# F Charge first
cast 2 1.8 ; cast melee 0.4 ; (cast melee 0.4 x6)
# G Seismic first
cast 4 1.8 ; cast melee 0.4 ; (cast melee 0.4 x6)
```
Metrics: t_first = first damage row (attacker=player, victim=enemy, ability melee/heavy) minus the `mark` time; melee damage in 8 s; hit count. Granularity is one chunk (0.9 s). Confound: static target means walking always eventually closes; the numbers measure reach and delay, not chase; record this on every result. Stop rule: if A/A SD > 0.5 chunk, increase n to 10 or call INCONCLUSIVE.
Pass criterion for a "change" recommendation: item arm beats base by more than 2 x A/A SD in both 20 m and 28 m gaps AND P4 shows its hold effect applies.

### R2 ratchet-flee proxy (M1)  RUNNABLE-AS-PROXY, labelled
Re-place the bot farther every chunk so walking never closes (assumes `fetch` is relative to the player; verify with P0 first): `fetch G0*k ; mark flee_X ; (cast <tool> once at chunk n0) ; then 8 x [ fetch (G0 + n*3.5)*k ; move 1 0 0.5 ; cast melee 0.4 ]` with G0 = 12 m, n0 in {0, 2}. Metric: melee hits landed in 8 s, per arm of R1. It measures "only burst tools catch a runner at least as fast as me" and nothing about dashes, stamina or cleanse. Not used for a change verdict by itself.

### R3 damage while approaching (M2)  RUNNABLE
`incoming gun 150` on (starts when the block starts) with the R1 scripts at D = 20 m; metric HP lost before t_first and total HP lost in 8 s (samples csv my_hp). Arms: A, B (Warp Stone bullet resist 6 s), C, plus Colossus popped first (`cast i1 0.4` then walk). Caveat: stream of ticks, not discrete hits (GAPS #6); Plated/Metal Skin-style per-hit items are not scored here.

### R4 survival curve under focus (M3, M8)  RUNNABLE with flags
Price points 12k, 20k, 31k (BASE items through the point). `lowhp 0` (do not clamp), `incoming gun 250` plus `incoming spirit 120` alternating each 4 s, 5 `enemies 5 8`; player does `cast 2 1.8; cast melee 0.4` loop. Metric: time until my_hp reaches 0 (samples), HP healed (healDiffObserved), total melee damage dealt. Arms: base20 vs Spirit Resilience swapped in for Hunter's Aura at 20k. Berserker 0/mid/max: run at 28k after P1 passes, stack levels reached by pre-running `incoming gun 300` for 0, 6, 20 s (no stack API; only if P1 shows a stack modifier). Flags: Hunter's Aura's enemy fire-rate slow cannot show (bots do not shoot, GAPS #17); stream damage may not feed Infernal/Berserker (P1).

### R5 melee output (M6, M12)  RUNNABLE
`fetch 120; ehp 50000; ekeep 1; mark melee; cast melee 0.4` x20, repeat with `eresist gun 25` and `eresist gun 50`; also `enemies 5 8` ring and ult. Gives the "measured melee DPS" used in the section 4 formula. Light vs heavy cannot be separated (UNSUPPORTED: no `melee light|heavy`).

### P5 ult answer check (M4)  RUNNABLE (names only)
`hardreset; souls 30000; unlock 7; basemods; mark p5; cast 4 1.8; mods; wait 3; mods; wait 4; mods`. Expect an Unstoppable-type modifier for about 5 s (T3). Effect against a real stun is UNSUPPORTED (no `ecc`).

## 6. Regression sweep (WEAKNESS_PROCESS F) of the candidate changes
No change is proposed to data.js. For the conditional candidates, what they would break:
- Warp Stone replacing Spirit Resilience at 31.2k: both are 3.2k vitality (Armor), so no spike change (health 8.0k either way); loses the spirit-damage resist, so the build would then lack a spirit counter unless Spirit Resilience moves into the Counters menu.
- Warp Stone replacing Hunter's Aura at 20k: weapon 10.4k -> 7.2k (below the 8k step, above the 4.8k spike), loses shred and the single-enemy fire-rate slow; moves a weapon item out of the mid damage run.
- Slowing Hex replacing BRS: spirit 2.4k -> 2.4k (tie colour), loses the -10% bullet shred needed for the gun side (Close Quarters/Point Blank); pure melee damage is unaffected.
- Fleetfoot replacing BRS: pushes weapon colour by 1.6k and drops spirit to 800 at 12k, delays the spirit 4.8k (16.8k) to about 18.4k; avoid.
New weaknesses: none for the default outcome. Re-sweep needed only if R1/P2 contradict the hypothesis.

## 7. Runnable summary
RUNNABLE now: P0, P1, P2, P3 (probe), P4, P5, R1, R3, R4 (flagged), R5, R2 (proxy only).
UNSUPPORTED (need op): true flee/dash chase (`emove`), stun/slow/silence/disarm on the player (`ecc`), enemy anti-heal (`eheal`), light vs heavy melee, wall/terrain control, NPC/camps, allies, bot shoot-back, imbue (not needed in this build), slow magnitude/stack reading (no velocity or modifier values).
Data gaps to fill by tests: Charge reach and cooldown, Seismic Impact leap range, Phantom Strike cooldown, Siphon cooldown, Charge slow %, base move speed.
Memory-worthy facts for the main session: Kieran 13:06 ruling that the Abrams kit already catches people (Weighted Shots removed); Abrams hero enum is Atlas; fetch/move/cast cannot run simultaneously, so true chase tests need a new `emove` op.


## I. Practicality (WEAKNESS_PROCESS section I; added 2026-10-24, appended, nothing above changed)
Sources added: `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` and `heroes.vdata` (game files: weapon, cooldowns, level table), data.js walk (prac/out/walk_abrams_melee.txt, 0 flags). Level table: unlocks at 0 / 500 / 1.4k / 3.2k souls, 1 point at every other level to 48.6k (32 points; tier costs 1/2/5 [U, consistent]). Time: ~7k at 8:00, ~1k/min after (late times are upper bounds).
Kit numbers that fill the [GAP]s in sections 1 and 7: Shoulder Charge cooldown 33 s (T1 32% slow 3 s, T2 +0.8 s wall stun, T3 -18 s); Seismic Impact cooldown 215 s (T1 -30 s, T2 +0.8 s stun, T3 5 s Unstoppable +6 m); Siphon cooldown 42 s (T1 -20 s).

### I.1 Ability points vs item timing
Order 2233124344243111: Charge T1 0.2k, T2 (wall stun) 2.6k, T3 (15 s cooldown) 11.0k; Infernal 0.5k, T1 (+200 HP) 0.9k, T2 (18% melee lifesteal) 4.6k, T3 24.6k; Siphon 1.4k (unused until T1 at 26.9k); Seismic 3.2k, T1 5.3k, T2 6.8k, T3 (Unstoppable) 16.1k.
Checks: Melee Charge (4.0k, "Charge pins them") has the T2 wall stun from 2.6k; Lifestrike (8.0k) lands after Infernal T2 melee lifesteal (4.6k); Colossus "pop as you ult in" (37.6k) has ult T3 from 16.1k. Consistent.
Candidate: Charge T3 before Seismic T1/T2 gives the 15 s Charge at 8.4k (2.6k earlier) and moves ult T1/T2 to 9.2k/11.0k. Charge is the only engage (Chain A), so this doubles engages for ~2.6 min at the cost of a 215 s instead of 185 s ult and a 1.6 s instead of 2.4 s stun for ~4k. Decision: leave (small gain, both sides depend on fight timing). UNTESTABLE-HIGH-RISK, 40%.
Sandbox validity: `unlock 7` at 12k/20k grants Infernal T3 and Siphon tiers the real order has at 24.6k+; R4 survival is biased up. Use `unlock 3` at 12k and say Charge T3 is missing (real at 11.0k).

### I.2 Gun economy
Shotgun: 9 pellets x 3.6 (+0.1 per pellet per level), 9 shells at 0.63 s (5.7 s to empty), shell reload 0.705 s + 0.353 s per shell (3.9 s full; cancellable, ReloadSingleBulletsAllowCancel). No fire-rate or magazine items; weapon items add close-range power (Close Quarters +20, Point Blank +50 within 15 m). Crushing Fists (24.8k) restores 15 ammo [U: shells or %] per light melee on a 5 s cooldown, so after 24.8k one light punch per 5 s means no full reloads. Before that a 10 s brawl uses about one magazine; whether punching interrupts the shell reload is [U]. The magazine supports the fire rate; no change. CALCULATED, 65%.

### I.3 Farming
Strong melee sustain on camps (Infernal T2 18% melee lifesteal from 4.6k, Melee Lifesteal 30% on NPCs, Lifestrike 40%, Restorative Shot 20 HP per NPC hit); no AoE clear tool, so waves are slow [U]. Losing-lane box (Extra Regen) covers the lane. Accept. CALCULATED; measurement UNSUPPORTED (no NPC op).

### I.4 Spike timing vs survivability (incl. the countered case)
Gun 4.8k at 5.6k, health 4.8k at 9.6k (Lifestrike, Enduring Speed), then no vitality until Spirit Resilience at 31.2k: ~21 min flat at 4.8k health. HP at 20k is about 2,600 (800 + 49 x 24 levels + Infernal T1 200 + item HP 425).
Defence = contact lifesteal + Infernal regen + ult T3 Unstoppable; no escape. Countered case: a silence or hex on Charge (Chain A) leaves him walking at a kiter with no contact sustain, so health is the only layer left. Orderings: A current; B Spirit Resilience (3.2k) before Hunter's Aura (health 8.0k at ~19k, Hunter's Aura and later items 3.2k later); C Extra Health/Colossus earlier. Same question as M3 (test R4).
Decision unchanged: leave; the Counters trigger ("Dying after Enduring Speed") is the answer. UNTESTABLE-HIGH-RISK, 35%. Wrong if R4 (with `unlock 3`) shows B living clearly longer at 20k.

### I.5 Buttons and rhythm
3 abilities + a melee rhythm: a heavy every 5 s for Melee Charge / Crushing Fists, lights between (Lifestrike, Spirit Strike at 2x cooldown on lights, Snatch -30% on lights). Core actives: Colossus (37.6k), Phantom Strike (44k). Optional actives: Metal Skin, Dispel, Counterspell (parry timing), Unstoppable, Ethereal Shift, Divine Barrier. Medium load; the procs need no tracking ("heavy whenever Charge pins"). Leave; the playstyle rotation line covers it.

### I.6 Slot lock and sell chain
9 slots at 20k, 10 at 31.2k: fine. Conflict: Counters sell Stalker; Ethereal Shift sells Stalker, or Spirit Resilience if gone; Unstoppable also sells Spirit Resilience. After one counter + Unstoppable, Ethereal Shift has no named sell. Reviewer note. CALCULATED, 70%.

### I.7 Forgiveness when behind
Identity items are cheap and early (Melee Charge 4.0k, Lifestrike 8.0k); Crushing Fists is a 4.8k upgrade; the only 6.4k no-component buy is Phantom Strike, last. Forgiving. No change. CALCULATED, 60%.

### I.8 Tests
No new test needed for section I. Reload-interrupt by melee is UNSUPPORTED (no light/heavy op, no ammo readout). The Charge-T3 order question is UNSUPPORTED (no per-ability tier op, GAPS #2).

### I.9 Regression (F)
No change chosen, so no new weaknesses.

| problem | chosen | grade | conf. |
|---|---|---|---|
| Charge T3 at 11.0k | leave | UNTESTABLE-HIGH-RISK | 40% |
| Flat 4.8k health 9.6k-31.2k | leave; Counters menu (see M3/R4) | UNTESTABLE-HIGH-RISK | 35% |
| Ethereal Shift / Unstoppable sell conflict | reviewer note | CALCULATED | 70% |
| Gun, farm, buttons, forgiveness | leave | CALCULATED | 60-65% |


## J. Item roles (WEAKNESS_PROCESS J; added 2026-10-24, appended, nothing above changed)
Sources: audit/items_full.json [i]; game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` [g] (modifier value types, cooldowns) and `gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt` [l]; audit/hero_abrams.txt [k]; walk prac/out/walk_abrams_melee.txt. Grades: C = CALCULATED, U = UNTESTABLE-HIGH-RISK, M = MEASURED (none).

### J.0 Game-file facts that change earlier statements
- Bullet Resist Shredder, Stalker and Crushing Fists provide MODIFIER_VALUE_BULLET_AND_MELEE_RESIST_REDUCTION [g]: their shred reduces melee resist too. BRS triggers on spirit damage [l], i.e. on Spirit Strike/Snatch melee procs.
- Melee Charge and Crushing Fists provide MELEE_TRAVEL_DISTANCE_PERCENTAGE (MeleeDistanceScale 50 / 60) [g]: the heavy melee travels further, a reach effect.
- Cooldowns [g]: Phantom Strike 35 s (fills the [GAP] in M1), Colossus 37 s, Lifestrike 4 s (x1.5 on light), Spirit Snatch 6 s, Spirit Strike 8 s (x2 on light), Stalker 6 s, Unstoppable 60 s, Ethereal Shift 37 s, Metal Skin 24 s.
- Berserker max 10 stacks (+70 weapon power) [g] (M8). Dispel Magic [l]: purges all non-ultimate negative effects; not usable while stunned or slept.

### J.1 Item roles
| item (box, souls) | every effect [source] | what it feeds | matters from | grade |
|---|---|---|---|---|
| Restorative Shot (0.8k, sold for Berserker) | next bullet heals 50 (hero) / 20 (NPC), 6 s; +6% weapon damage [i/g] | lane sustain off shotgun pokes, camps | at once | C |
| Close Quarters (1.6k, becomes Point Blank) | +20 weapon power within 15 m, 20% melee resist [i] | shotgun; survival vs enemy melee | at once | C |
| Melee Lifesteal (2.4k, becomes Lifestrike) | next melee heals 100, 8 s (x1.5 light), +12% melee [i] | lane/camp sustain | at once | C |
| Melee Charge (4.0k, becomes Crushing Fists) | next heavy +25 and +10% melee, heavy travels +50% further, +6% bullet resist, 5 s [i/g] | heavy after a Charge pin; reach: a longer heavy lunge starts contact from further (M1) | at once | C (travel), U (metres) |
| Stalker (5.6k) | close-range weapon damage opens a wound: 17 DPS 5 s, -6% bullet AND melee resist, revealed through walls (25 m); +1.5 m/s for you; -50% footstep sound; +50 HP; 6 s [i/l/g] | chase: speed after the first hit and seeing a runner behind cover (M1); a quiet approach (M2); melee shred; the Counters and Ethereal Shift sell | at once | C, U (reveal value) |
| Lifestrike (8.0k) | melee: 48% slow 2.5 s, heal 120+1.75x spirit plus (35%+0.5x spirit) of melee damage, +16% melee, +125 HP; 4 s (6 s light); 40% vs NPCs [i/g] | the retention slow (M1 Chain C), sustain; spirit from Snatch (+25 stolen) adds ~44 HP per proc | at once | C |
| Sprint Boots > Enduring Speed (9.6k) | +2 m/s, 25% slow resist, OOC 2 [i] | closing (M1), kiting resistance | at once | C |
| Spirit Strike (10.4k, becomes Snatch) | melee vs hero: +40+0.372x spirit damage, -6% spirit resist 6 s; 8 s (16 s light) [i/g] | melee burst; triggers BRS and Healbane; with Snatch, spirit for Lifestrike | at once | C |
| Bullet Resist Shredder (12.0k) | on spirit damage: -10% bullet AND melee resist 8 s; +9% weapon damage, +9% bullet resist self [i/l/g] | melee (heavy, Crushing Fists, Lifestrike's % heal) and the shotgun, applied by the Strike/Snatch proc on the same punch; survival (M2/M3) | at once (Spirit Strike owned) | C |
| Point Blank (14.4k) | within 15 m: +50 weapon power and a 20% 2 s slow on bullets; 30% melee resist; +75 HP [i] | retention slow from the shotgun (M1), survival vs melee brawlers | at once | C |
| Spirit Snatch (16.8k) | melee vs hero: +50+0.84x, steals 12% spirit resist and 25 spirit 10 s; +7% melee; +75 HP; 6 s [i/g] | Lifestrike heal (+44 per proc), its own and Strike's damage; spirit survival; triggers BRS | at once | C |
| Hunter's Aura (20.0k) | 15 m: enemies -10% bullet resist and -15% fire rate (doubled vs a lone hero); +100 HP; +0.75 m/s sprint [i] | survival vs gun while approaching and in the brawl (M2/M3); shred for the shotgun (melee part [U]: the game file does not list a melee type for it) | at once | C, U (melee) |
| Crushing Fists (24.8k) | melee: stacking -5% bullet and melee resist (6 stacks, 8 s; heavy = 2) then a 0.75 s stun; light melee restores 15 ammo; +22% melee, +25 heavy, heavy travels +60%; +12% bullet resist; 5 s [i/g/l] | melee damage, the stun is a hold (M1 retention) and a mini-interrupt, ammo (I.2), reach, survival | at once | C |
| Berserker (28.0k) | +7 weapon power per 120 damage taken in 10 s, max 10 (+70); +8% bullet resist [i/g] | shotgun (melee [U]), survival | when focused | C, U |
| Spirit Resilience (31.2k) | 30% spirit resist (+15 below 50%), OOC 3 [i] | spirit focus (M3) | at once | C |
| Extra Health > Colossus (37.6k) | 7 s: +35% bullet and spirit resist, 24% slow and -22% dash speed in 14 m, +30% melee, +15% weapon damage; +25% base HP; 37 s [i/g] | the commit window: survival, retention, damage | at once | C |
| Phantom Strike (44.0k) | 25 m teleport to an enemy, pull to ground, 40% slow 3 s, disarm, 75+0.93x; +8 spirit, +15% weapon damage; 35 s [i/g] | first contact vs fliers/dashers (M1), disarm = defence vs a gun carry | at once | C |
| Counters: Plated Armor / Metal Skin / Spellbreaker / Counterspell | as in the tank file; Spellbreaker also 25% debuff resist always [i/g] | gun / standing gun / spirit / telegraphed ults; Spellbreaker's passive shortens CC (M4) | at once | C/U |
| Counters: Dispel Magic | purge non-ultimate negatives (Slowing Hex, burn, a pending Knockdown [U]); then 250 heal and +2 m/s 3 s; 45 s [l/g] | Chain A/C RECOVER; chase speed after a cleanse | at once | C, U (timing) |
| Counters: Healbane | his spirit damage (Strike/Snatch procs) applies -35% healing 8 s; 275 heal on kill; +7 spirit [i] | vs healers; needs the procs to land | at once | C |
| Rich: Witchmail / Scourge / Unstoppable / Divine Barrier / Ethereal Shift | Witchmail: 22% spirit resist, cooldown cut on big spirit hits; Scourge: self 40% spirit resist, 20% debuff resist, max-HP aura, ally-castable; Unstoppable: 5.5 s CC immunity, 60 s, 25% debuff resist always; Divine Barrier: non-stun cleanse, barrier, ally-castable; Ethereal Shift: 4 s invulnerable then speed and spirit resist [i/g] | M3/M4/M11; Unstoppable's passive is CC duration even when the active is not used | at once | C/U |
| Slot locked: Juggernaut | +2.5 m/s, 50% slow resist, 25% melee resist, +8 regen, attackers' fire rate -40% 4 s [i/l] | M1 (slow resist), M2 (anti-gun) | when a slot frees | C |
| Losing lane: Extra Regen | +2.5 regen, OOC 1.5 [i] | lane | at once | C |

### J.2 Earlier verdicts re-opened with all roles counted
| earlier verdict (section) | role it was judged on | roles added | restated verdict | changed? | grade, conf. |
|---|---|---|---|---|---|
| Section 6: "Slowing Hex replacing BRS: ... pure melee damage is unaffected"; Fleetfoot for BRS | BRS as a gun shred | game file: the shred is bullet AND melee, applied by the Strike/Snatch proc on the punch itself; +9% weapon damage, +9% bullet resist self | Withdrawn: either swap loses -10% melee resist on the target and 9% bullet resist. M1's "not added" for Slowing Hex and Fleetfoot is firmer | yes (regression statement) | C, 65% |
| M1 catching mobile targets: leave core | Charge, ult, slows, Phantom Strike, Warp Stone etc. | heavy-melee travel +50%/+60% (Melee Charge, Crushing Fists), Stalker's +1.5 m/s and reveal through walls, Crushing Fists' 6-stack stun, Dispel's +2 m/s, Phantom Strike's 35 s cooldown [g] | LEAVE core (unchanged); the kit and build reach further than the first pass counted, which supports Kieran's 13:06 ruling. R1 cannot test the lunge (no light/heavy op) | no (reasoning) | U, 50% (cap) |
| I.6 / Counters and Ethereal Shift sell Stalker | Stalker as a minor damage item | Stalker is the build's chase and vision item (speed, reveal, quiet steps) and a melee shred | Cannot determine a better sell (the other early items are components of core upgrades or named); keep, reviewer note that the first counter costs chase | no (note) | C, 45% |
| M4 CC: leave, cannot determine | actives (ult Unstoppable, menu actives) | Spellbreaker (Counters) and Unstoppable (rich) both carry 25% debuff resist always | LEAVE unchanged; a passive CC answer already sits in the menu | no | U, 30% |
| M3 Spirit Resilience before Hunter's Aura | health vs shred | Hunter's Aura also -15%/-30% enemy fire rate in 15 m and +100 HP (already flagged as invisible in the Sandbox) | unchanged | no | U, 35% |
| M5 anti-heal on melee sustain | heal sources | Lifestrike's heal scales with spirit (1.75x and 0.5x%), so Snatch's +25 stolen spirit is a sustain item here (+44 HP per proc) | unchanged; note that Snatch is part of the sustain | no | U, 30% |

### J.3 Tests that separate the roles (AUTORUN.md ops; `setup Atlas Haze`; `fetch 120`; A/A n=6, ABBA n=6; effect > 2 x A/A SD)
- J-M1 does bullet resist touch melee, and does BRS shred it (separates BRS's melee role from its gun role):
```
hardreset
ehp 50000
ekeep 1
fetch 120
eitem upgrade_improved_bullet_armor
mark jm1_bres
cast melee 0.4
cast melee 0.4
cast melee 0.4
mark none
eclear
mark jm1_none
cast melee 0.4
cast melee 0.4
cast melee 0.4
mark none
```
  Then arms with `give upgrade_acolytes_glove` vs `give upgrade_acolytes_glove` + `give upgrade_bullet_resist_shredder`: first punch procs Strike (and BRS), next five punches' melee damage per hit (+10% expected if the shred applies to melee). Same for the shotgun with `fire 2` after the proc. RUNNABLE.
- J-M2 Snatch feeding Lifestrike: `give upgrade_boxing_glove` vs + `upgrade_spirit_snatch`, `lowhp 50`, `healreset`, punches 4.5 s apart (Lifestrike cooldown), `healsum`; expect about +44 HP per Lifestrike proc after a Snatch proc. RUNNABLE.
- Heavy-melee travel (Melee Charge/Crushing Fists), Stalker speed and reveal, Hunter's Aura fire-rate slow: UNSUPPORTED (no heavy op, no velocity or vision readout, bots never shoot); `mods` can confirm the Stalker buff name only.

### J.4 Regression (F)
No item or order change. One earlier regression line is withdrawn (BRS swaps lose melee shred). No new weakness.

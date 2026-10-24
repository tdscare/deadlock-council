# Weakness sweep: abrams (tank) ("Rizuhble's Spirit Tank Abrams", Siphon Life tank)
Solver: weakness-solver, 2026-10-24. Process: council/WEAKNESS_PROCESS.md. Sources: data.js (id abrams), audit/items_full.json, audit/hero_abrams.txt, sandbox/GAPS.md, sandbox/playstyle/abrams.md, council/RULES_KIERAN.md, AUTORUN.md ops. data.js was not touched; nothing here is applied. Sibling file: weaknesses/abrams_melee.md (shares probes P0-P2 and the protocol; repeated here in short so this file runs alone).
Tags: [kit] read from data, [GAP] number not in the data (measure it), [U] game knowledge to verify. `setup Atlas Haze` (hero enum Atlas).

## 0. Hero identity map and ranked dependency chains (WEAKNESS_PROCESS A2) and evidence grades (H)
Grades used: MEASURED (valid sandbox result above A/A noise; sandbox, not live game), CALCULATED (kit maths, assumptions stated), UNTESTABLE-HIGH-RISK (depends on positioning, travel time, enemy reaction, CC timing, imbue chains, stacking; confidence capped at 50%; verdict can only be keep current / situational note). No test in this file has been run, so nothing below is MEASURED; all verdicts are CALCULATED or UNTESTABLE-HIGH-RISK. The Siphon imbue chain (six items) is itself UNTESTABLE-HIGH-RISK until probe P3 passes.

### Identity map (spirit tank build)
| strength [kit] | compensates for | dependency / condition | verified enemy counters (item/ability data) |
|---|---|---|---|
| Siphon Life (4 s, 8 m, damage + 70% heal on heroes, six imbue items) | no gun, no escape, low burst | cooldown [GAP], enemy inside 8-14 m, cast must not be silenced | Silence Wave (3 s), Cursed Relic (3.25 s silence/disarm/item lock), stuns before cast, kiting out of radius, Slowing Hex does not stop it; anti-heal Healbane -35%, Decay -50%, Spirit Burn -70% cuts the heal |
| Infernal Resilience (13% of damage taken regenerated over 20 s, T3 +9%, +20% debuff resist) | low sustain between Siphons | damage must be taken and survived for the 20 s | burst that kills inside the window; HealAmpRegenPenalty from anti-heal items; enemies that do not shoot (nothing to regen) |
| Charge pin + Seismic stun (1.6 s, 9 m) | cannot hold a group for Siphon | cooldowns [GAP], wall for the pin stun, ult T3 gives 5 s Unstoppable | silence/interrupt/stun before they fire, spreading, dashing out |
| Scourge self (2.3% max HP/s aura 10 m, +40% spirit resist, +20% debuff resist, 10 s) | low damage output | 35.2k, active | Silence/Relic item lock, Dispel (aura on self), kiting out of 10 m |
| Large spirit invest + Healing Booster + Witchmail | squishy mid game, spirit burst | souls | bullet damage (Counters menu only), anti-heal |

### Ranked chains (frequency x lethality; frequency [U], not measured)
1. Chain A: Siphon is the heal, the damage and the imbue sink; silence or lockdown before it fires removes sustain AND six items' worth of value, leaving a spirit-stat tank with Infernal regen only. Common (silence/Relic items), lethal. PREVENT: engage with Charge/ult first so the cheap ability eats the CC, Debuff Reducer (not in build), Infernal T3 20% and Scourge self 20% debuff resist, Counterspell. RECOVER: Dispel Magic/Divine Barrier (menu/rich), Healing Booster, Healbane kill-heal. SURVIVE: Witchmail, Spirit/Bullet Resilience, Infuser, Colossus. Enemy counters to the answers: a second silence, cleanse on cooldown, Unstoppable unusable once stunned, Cursed Relic locks the items too.
2. Chain B: Siphon needs range; kiting, dashes or flight leave 8-14 m and cut heal/damage to zero while ranged damage continues. Common vs mobile or ranged heroes, medium lethality. PREVENT: Charge/ult stun first, Colossus slow aura, Mystic Slow/Slowing Hex (candidates). RECOVER: Phantom Strike/Warp Stone (candidates, not in build). SURVIVE: Infernal regen (still runs), Healing Booster, Counters menu resists. Counter to answers: dash, slow resist, cleanse.
3. Chain C: Infernal regen and Siphon heal are healing; anti-heal plus burst beats them. Common, medium lethality. PREVENT: Healbane in build (their heals), kill first. RECOVER/SURVIVE: Spirit/Bullet Resilience, Witchmail; Leech irrelevant (no lifesteal items). Counter: anti-heal -70% (Spirit Burn).
4. Chain D: mid-game durability gap (no vitality between 9.6k and 28.8k) against gun focus before the counters menu is bought. PREVENT: positioning. RECOVER: none. SURVIVE: Extra Regen/Healing Booster/Enduring Speed, menu items. Counter: focus fire while Siphon is on cooldown.

## 1. Build snapshot
Core order with cumulative souls and colour spend (upgrades count the difference only):
Extra Regen 0.8k > Spirit Strike 1.6k > Arcane Surge 3.2k > Duration Extender 4.8k > Extra Spirit 5.6k (spirit 4.8k) > Healing Booster 6.4k > Healbane 8.0k > Enduring Speed 9.6k (health 4.8k) > Mystic Expansion 10.4k > Compress Cooldown 12.0k > Spirit Snatch 14.4k (spirit 9.6k) > Improved Spirit 15.2k > Superior Duration 16.8k > Superior Cooldown 18.4k > Mystic Vulnerability 20.0k > Greater Expansion 22.4k (spirit 17.6k) > Witchmail 28.8k (health 11.2k) > Scourge 35.2k > Boundless Spirit 40.0k > Escalating Exposure 44.8k (spirit 33.6k).
Final 12: Healing Booster, Arcane Surge, Healbane, Enduring Speed, Spirit Snatch, Boundless Spirit, Superior Duration, Superior Cooldown, Greater Expansion, Escalating Exposure, Witchmail, Scourge. Siphon Life carries the imbues (Duration Extender > Superior Duration, Mystic Expansion > Greater Expansion, Compress > Superior Cooldown). Nothing in the build is gun or punch based; Spirit Strike/Snatch fire on any melee.
Kit tools [kit]: Siphon Life (4 s, 8 m, heals 70% of dealt damage on heroes, 35% NPCs, ticks 0.25 s; T3 +2 m radius; T1 -20 s cooldown per data.js notes; base cooldown [GAP]); Shoulder Charge (T1 slow 3 s, T2 wall stun +0.8 s, T3 -18 s cooldown); Infernal Resilience (13% of damage taken regenerated over 20 s, T3 +9% and +20% debuff resist, T1 +200 HP); Seismic Impact (9 m radius [+6 m], 1.6 s stun, T3 5 s Unstoppable on cast); Scourge self-cast (2.3% max HP/s aura 10 m for 10 s, +40% spirit resist, +20% debuff resist).
Rules touched: health spike right after first damage spike for Abrams (done at 9.6k), "Siphon alone is not sustain" (Healing Booster, Healbane kill-heal 275, Infernal regen, Infuser in rich), counters menu, 12-slot fold, sells named.

## 2. Shared test protocol
Block macro BLOCK(arm, N, D):
```
setup Atlas Haze ; aimoff 5.5 3     # once
hardreset                           # fresh pawns, no items/buffs, factory cooldowns
souls N
give <upgrade classes only, no components>
unlock 7                            # upper bound (GAPS #2); unlock 0 where noted
basemods
ekeep 1 ; ehp 50000
fetch D
mark <label> ... mark none ; wait 1
```
Arms A,B,B,A counterbalanced, n=6 per arm, A/A first for the noise floor, effect counts only if above 2 x A/A SD. Setup-truth checks per PILOT 0.2.
Class names (item_commands.json): Extra Regen upgrade_endurance; Spirit Strike upgrade_acolytes_glove; Arcane Surge upgrade_arcane_surge; Duration Extender upgrade_arcane_extension; Extra Spirit upgrade_improved_spirit; Healing Booster upgrade_healing_booster; Healbane upgrade_healbane; Enduring Speed upgrade_cardio_calibrator; Mystic Expansion upgrade_magic_reach; Compress Cooldown upgrade_magic_tempo; Spirit Snatch upgrade_spirit_snatch; Improved Spirit upgrade_soaring_spirit; Superior Duration upgrade_imbued_duration_extender; Superior Cooldown upgrade_cooldown_reduction; Mystic Vulnerability upgrade_magic_vulnerability; Greater Expansion upgrade_tech_range; Witchmail upgrade_absorbing_armor; Scourge upgrade_discord; Boundless Spirit upgrade_boundless_spirit; Escalating Exposure upgrade_escalating_exposure; Mystic Slow upgrade_magic_slow; Slowing Hex upgrade_containment; Phantom Strike upgrade_phantom_strike; Warp Stone upgrade_warp_stone; Torment Pulse upgrade_tech_damage_pulse; Debuff Reducer upgrade_debuff_reducer; Unstoppable upgrade_unstoppable; Colossus upgrade_colossus; Vortex Web upgrade_aoe_root; Knockdown upgrade_target_stun; Bullet Resilience upgrade_improved_bullet_armor; Spirit Resilience upgrade_tech_purge; Toughness upgrade_health_2; Leech upgrade_damage_recycler.
Price points: TB12 (12.0k) = endurance>healing_booster, acolytes_glove, arcane_surge, arcane_extension, improved_spirit, healbane, cardio_calibrator, magic_reach, magic_tempo (gives Healing Booster in place of Extra Regen); TB20 (20.0k) = healing_booster, arcane_surge, healbane, cardio_calibrator, spirit_snatch, soaring_spirit, imbued_duration_extender, cooldown_reduction, magic_vulnerability; TB30 (30k band) = TB20 + tech_range + absorbing_armor (28.8k); TB45 (44.8k) = full core 12.

### Probes (results gate dependent tests)
- P0 unit calibration: `hardreset; souls 20000; unlock 0; fetch 150; ehp 50000; enemies 3 R` then `mark ring_R; cast 1 2; mark none` for R in {250,290,315,340,380,430}. Siphon radius is 8 m at unlock 0; the cut gives u per m (provisional k = 39.4 [U]; 8 m = 315u). RUNNABLE; ring placement unconfirmed (AUTORUN), so pass = clean monotonic cut.
- P1 hooks: does `incoming`/`hurtme` feed Infernal Resilience (and Pain-style hooks)? `hardreset; souls 30000; basemods; healreset; mark p1a; wait 5; incoming gun 300; wait 6; incoming off; wait 8; healsum; mark none` and compare healDiffObserved with and without the 6 s stream phase; Infernal regen = 13% of incoming over 20 s (about 234 HP on 1800 damage). RUNNABLE. If it fails, every survival test below is biased low (state it).
- P3 imbue auto-apply (gates everything on Siphon; GAPS #1): arm X: `hardreset; unlock 0; souls 5000; give upgrade_magic_reach; fetch 150; enemies 3 346; mark ex_on; cast 1 2; mark none`; arm Y: same without the item. 346u is 1.1 x the base 8 m radius (k=39.4) and 0.92 x the +20% radius. Hits on ring bots in X and none in Y = imbue applies automatically; no hits anywhere = the item is not imbued on Siphon (all Siphon items score 0, UNSUPPORTED until an `imbue` op exists). Similarly Duration Extender: Siphon damage row span (4 rows/s) should lengthen 22%; Compress: recast interval shrinks. RUNNABLE.
- P4 slow/debuff presence and duration (names only; magnitude and stacking unreadable): `hardreset; give <item>; fetch 300; mark p4_X; <apply>; mods; wait 1; mods; wait 2; mods; wait 4; mods` with apply = `cast 1 2` (Mystic Slow on Siphon ticks), `cast i1 0.5` (Slowing Hex, Phantom Strike, Colossus, Warp Stone, Knockdown), `cast 2 1.8` (Charge). Expect a slow modifier name on the bot while Siphon ticks (Mystic Slow, kit 24% for 2 s) and gone shortly after. Also verifies `cast iN` slot mapping (give actives one at a time). RUNNABLE.
- P5 ult answers: `hardreset; souls 30000; unlock 7; basemods; mark p5; cast 4 1.8; mods; wait 3; mods; wait 4; mods` for the 5 s Unstoppable modifier; Scourge self-cast `cast i1` for Scourge modifier. RUNNABLE (names only).

## 3. Weakness sweep (table form per WEAKNESS_PROCESS G)
| id | weakness (category) | sev | evidence | remedies considered | chosen | cost | tests | verdict (confidence) | new weaknesses |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Siphon needs targets inside about 8-14 m; kiting or dashing enemies leave it (reach) | M-H | Siphon radius 8 m (+2 m T3), expansions give +20% and +30%; heal and damage only while targets are inside; build has no gap closer and no slow | Section 4 (all classes) | Leave core; Mystic Slow <-> Arcane Surge as named candidate; ability use + target choice | 0 now | P0, P3, P4, T-R1, T-R2 | LEAVE ALONE core, candidate swap pending tests (low-medium) | If swapped, Arcane Surge's +12% range/+15% duration after a dash-jump is lost |
| T2 | Durability gap: no vitality spend between 9.6k and 28.8k (survival) | M-H | health 4.8k at 9.6k then spirit only to 22.4k; Witchmail 28.8k; counters menu is the answer | Toughness/Debuff Reducer for Mystic Vulnerability at 20k (T2 tie, MV is bought again before Escalating Exposure), Bullet/Spirit Resilience, Extra Health, pulling Witchmail ahead of Greater Expansion | Keep order; counters menu | 0 | T-S (stream, flagged), P1 | LEAVE ALONE (low-medium) | Moving health earlier delays spirit 17.6k and the expansions |
| T3 | CC chains and silence: all Siphon imbues die with Siphon silenced; no Unstoppable or Debuff Reducer (CC) | M | Infernal T3 +20% debuff resist, Scourge self +20%, ult T3 5 s Unstoppable, Dispel Magic/Counterspell in menu; Unstoppable only in the melee build's rich box | Debuff Reducer (1.6k, 25% shorter negatives, +90 HP), Unstoppable (6.4k, once ready, unusable while stunned), Reactive Barrier, Juggernaut, Counterspell/Dispel (already) | Propose adding Debuff Reducer (cheapest) to Counters menu vs "long stuns and silences"; Unstoppable below it | 1.6k only if bought | UNSUPPORTED (no `ecc`); P5 for the ult window | Situational note only: Debuff Reducer as a Counters-menu entry (UNTESTABLE-HIGH-RISK, low; needs reviewer) | Debuff Reducer is a T2 buy late unless sold for something; only valid as a menu item (rule: no fresh T2 late is bent by the menu) |
| T4 | Low kill pressure before Scourge (35.2k) and Boundless (output) | M | Output = Siphon (spirit scaling), Spirit Strike/Snatch on melee, Escalating Exposure at the end; Scourge arrives 35.2k; plan abrams.md already lists Spirit Snatch vs Torment Pulse vs none as uncertain | Torment Pulse (T3 3.2k, pulses the closest two within 9 m, +100 HP; rules say it is the tank-in-their-face item), Spirit Burn (rich), Infuser (rich), Scourge earlier, Boundless | Test Torment Pulse for Spirit Snatch at 14.4k (T3 for T3 tie, Spirit Snatch costs 2.4k net because Spirit Strike is a component, so tie by price point not net) | 0 until a result | T-O1 (valid for substitution; absolute numbers biased by missing imbues) | INCONCLUSIVE until T-O1 (low) | Spirit Snatch also gives shred and +75 HP; Torment Pulse gives +100 HP and 18% melee resist |
| T5 | Siphon downtime: uptime of the one sustain and damage tool (output/ability downtime) | M | Duration 4 s base; Duration Extender +22%, Superior +28%, Arcane Surge +15%; cooldown base [GAP]; Compress -18%, Superior -20%, T1 -20 s | Cooldown stacking already core (Compress, Superior Cooldown), Echo Shard (6.4k, imbue doubles uses), Refresher (rich-ish) | Leave | 0 | T-U (measures duration and recast; depends on P3) | LEAVE ALONE, measure (low) | none |
| T6 | Enemy healing reduction (output/sustain) | M | Sustain is 70% of Siphon damage, Healing Booster +20%, Infernal regen; sandbox has no `eheal`; 25 builds buy anti-heal | Leech (T4, no lifesteal items otherwise, wasted), Healbane in build, cleansing | Accept | 0 | UNSUPPORTED (`eheal`) | LEAVE ALONE, cannot determine (low) | none |
| T7 | Everything on one ability: single point of failure if Siphon is on cooldown, dead or silenced (dependency) | M | Six imbue items (Duration Extender, Superior Duration, Mystic Expansion, Greater Expansion, Compress, Superior Cooldown) | Spread (Mystic Expansion still helps Charge/ult? no, only the imbued ability), keep Greater Expansion global (it is not an imbue), Debuff Reducer for T3 | Accept; note Greater Expansion improves everything | 0 | P3 for imbue; failure case UNSUPPORTED | LEAVE ALONE (medium) | none |
| T8 | Economy: no scaling farm tool, Siphon 35% on NPCs, tank has no gun (economy) | M | playstyle: farms camps/troopers with punches; first 5.6k is all spirit 4.8k with Extra Regen only | Cultist Sacrifice (6.4k), Spirit Strike clears camps, Siphon on camps | Leave | 0 | UNSUPPORTED (no NPC/camp op) | LEAVE ALONE (low) | none |
| T9 | Charge stun/pin needs a wall; wall presence in the test map unknown (positioning) | L-M | playstyle note "Charge speed/turn and wall availability uncertain" | Position near walls | Playstyle | 0 | P3 (wall) in the melee file; UNSUPPORTED effect | LEAVE ALONE (low) | none |
| T10 | Team/objective dependence: a tank without followers dies; Scourge/ally buffs need allies (team) | M | Scourge can target allies (35 m), self-cast in build | Duo partner | Pair suggestion | 0 | UNSUPPORTED (no ally ops) | LEAVE ALONE (low) | none |
| T11 | No escape when losing a fight (survival) | L-M | Rich box has Divine Barrier (barrier 600, 6 s speed, removes non-stun debuffs) and Spirit Burn, Infuser; no dash | Warp Stone, Majestic Leap, Ethereal Shift | Leave | 0 | UNSUPPORTED | LEAVE ALONE (low) | none |
| T12 | Slot fold and sell chain: 20 buys fold into 12 slots; notes name Arcane Surge/Healbane as sacrifices (slot) | L | Final 12 listed in section 1; counters/rich sells reference Arcane Surge, Healbane, Spirit Snatch | n/a | Leave; confirm nothing double-sells (Counters sell Arcane Surge, Spirit Burn also sells Arcane Surge) | 0 | none | LEAVE ALONE, note: two boxes name Arcane Surge, Healbane is the other sell, Superior Duration is the fallback (medium) | If Arcane Surge becomes Mystic Slow the sells keep working (same slot) |

Categories checked and below the bar: ammo/reload (no gun), finishing kills (no gun/execute need), armour scaling (Spirit Snatch/Mystic Vulnerability/Escalating Exposure shred), ramp-up, objective timing.

## 3b. Evidence grade per verdict (H)
| id | verdict | grade | confidence | what would make this wrong |
|---|---|---|---|---|
| T1 | leave core; Mystic Slow for Arcane Surge named candidate only (situational note at most) | UNTESTABLE-HIGH-RISK (kiting, slow trigger on ticks, stacking, additive radius); coverage radius CALCULATED until P3 | <=40% | P3 passes and T-R1 shows coverage/retention gain above noise with P4 showing the slow on all ring bots |
| T2 | leave | UNTESTABLE-HIGH-RISK (focus fire, P1 hook unknown) | 35% | T-S shows much earlier death at 20k that Toughness/Debuff Reducer fixes |
| T3 | Debuff Reducer as a Counters-menu entry is a situational note only, not a core change | UNTESTABLE-HIGH-RISK (no `ecc`) | 30% | a CC test op showing 25% shorter stuns/silences does not change outcomes |
| T4 | inconclusive until T-O1 | CALCULATED, then MEASURED (substitution only) if T-O1 above noise | 30% | T-O1 shows Torment Pulse clearly beating Spirit Snatch at equal price with imbues applied |
| T5 | leave, measure | CALCULATED; MEASURED after T-U | 40% | T-U shows long Siphon downtime that Echo Shard/more cooldown fixes |
| T6-T12 | leave / accept | CALCULATED or UNTESTABLE-HIGH-RISK as stated per row | <=40% | the per-row test named in section 3 |
Rule check: nothing here changes a core build.

## 4. Deep dive: reach and retention versus mobile enemies (T1), all remedy classes
The tank's problem is staying inside Siphon radius, not first contact: Siphon, Scourge (10 m) and the ult (9 m) are area effects around a hero who has Charge (reach [GAP, P2 in the melee file]) and nothing else. The build already buys range: Mystic Expansion +20%, Greater Expansion +30% (global), Arcane Surge +12% after a dash-jump, T3 +2 m. If additive, 8 m + 2 m becomes about 12-15 m; if multiplicative, about 15.6 m [U, test P3].
Utility to damage and heal: extra Siphon output = (seconds the target stays inside radius) x (measured Siphon damage per second, T-R1) x (1 + 0.7 heal factor for sustain). Time inside radius for a runner at speed v_them when I stand still = R/v_them (12 m / 7.5 m/s = 1.6 s [U numbers]); a 24% slow raises it to R/(0.76 v_them) = 2.1 s (+31%) only if Mystic Slow applies on Siphon ticks (needs P4) and the Siphon is up. Chasing changes it to R/(v_them - v_me) if v_me < v_them. Gain disappears when: Siphon on cooldown or silenced, the enemy has a dash or teleport, slow resist items (Enduring Speed 25%, Juggernaut 50%), the slows do not stack [GAP #18], the enemy simply leaves 14+ m (no tool reaches), or the tick damage does not trigger the slow (threshold [GAP]).

| class | candidate | cost / price point | what it removes | utility to damage and when the gain disappears | test | verdict |
|---|---|---|---|---|---|---|
| Item: slow on damage | Mystic Slow (T2 Tech 1.6k, 24% slow 2 s on spirit damage taken, +50 HP) | Replaces Arcane Surge (T2 Tech tie, same slot, early #3 at 3.2k) | Keeps runners inside radius while Siphon ticks (4 ticks/s) | +31% time in radius in the model above; gone when Siphon is down or the damage does not trigger it; lose Arcane Surge's +12% radius, +15% duration, +20 spirit after a dash-jump | P4, T-R1 arms B and C | Named candidate; not added (low-medium) |
| Item: anti-dash slow | Slowing Hex (T2 Tech 1.6k; 16% slow 3.5 s, silences their movement items/abilities, 25 m, cooldown 29 s) | Arcane Surge tie as above | The only cheap anti-dash; single target | Gain only if they have a dash; 16% slow is small; Dispel/Divine Barrier removes it | P4, T-R1 arm D | Not added (low) |
| Item: gap closer + hold | Phantom Strike (T4 Armor 6.4k, 25 m, pull, 40% slow 3 s, disarm; ImpactDamage 75 + 0.93 x TechPower, a spirit scaling hit) | Late; would replace Healbane (rich sell chain) at about 44k or Witchmail order | Reach and hold; unique vs fliers | Contact gained = reach + 3 s hold; gone on parry/cleanse/cooldown/no line of sight; pushes vitality; kills the "no punch items in the tank build" rule (Round 13) | T-R1 arm E | Not added (medium); the tank build has no melee payoff, Siphon only needs proximity |
| Item: teleport | Warp Stone (T3 3.2k, 11 m forward, 30% bullet resist 6 s) | Would sell Arcane Surge or sit in Counters menu | Instant 11 m | Gain = 11 m / closing speed s; no hold; doubles as approach armour | T-R1 arm F | Not added (low); candidate for Counters ("they kite you") |
| Item: group/hold | Vortex Web (T4, comp Slowing Hex; 12 m capture radius, 28% slow, tether; scales with range/radius multipliers) | 6.4k, rich-box tier | Pulls enemies into the same spot, good for Siphon | Not checked in the sandbox (no ally/enemy dash); expensive; skip | UNSUPPORTED | Not added (low) |
| Item: slow aura | Colossus (T4 Armor 6.4k with Extra Health; 24% slow, -22% dash speed, 14 m, 7 s, +35% resists) | Rich list already includes it? The tank rich box has Infuser, Spirit Burn, Colossus, Divine Barrier | Slow aura exactly around the tank, scales with Greater Expansion | 7 s window only; fits Siphon's 4-6 s | P4 | KEEP in rich box (medium) |
| Item: movement stats | Enduring Speed (in build), Sprint Boots, Fleetfoot (off-colour), Majestic Leap (3.2k), Extra Stamina chain (Arcane Surge's component) | Enduring Speed already core | Closing speed only if v_me > v_them | none | n/a | KEEP; others not added |
| Ability use | Charge pin (T2 wall stun), ult stun 1.6 s (radius 9 m [+6 m]), Scourge self as you ult in, Siphon after the stun lands | free | Holds targets before Siphon starts; the stun is the hold | Gain gone when Charge/ult on cooldown; playstyle note already says this | P2 (melee file), T-R1 arms G and H | CHANGE playstyle note (proposal) |
| Positioning | Fight in cover/narrow lanes so targets cannot kite out of radius; stand in the cluster | free | n/a | gain gone if no cover | n/a | playstyle |
| Target selection | Siphon the group, ignore the single runner, use Charge on the one who commits | free | n/a | none | n/a | playstyle |
| Team | Ally CC/pull/peel | free | n/a | UNSUPPORTED | n/a | pair suggestion |
| Accept | Do nothing: Siphon +50% radius already built; mobile heroes are for allies | 0 | n/a | n/a | n/a | default (medium) |

Decision for T1: leave the core; keep Mystic Slow <-> Arcane Surge as the only candidate (same tier, colour and slot); run P3 first because the whole radius model depends on imbue auto-apply. Proposed playstyle note (for playstyle/abrams.md, not applied): "Charge or ult first so Siphon starts on a held group; do not chase one runner out of range." Tested part: radius coverage, slow-modifier presence and duration, Siphon uptime; untested: real kiting, dashes and cleanse (no `emove`, `ecc`).

## 5. Test specifications
### T-R1 Siphon coverage and retention  RUNNABLE after P0 and P3
Arms at TB12 (Arcane Surge present, "A"), B = Arcane Surge -> Mystic Slow, C = none of both (removed), D = Arcane Surge -> Slowing Hex; at TB45: E = Healbane -> Phantom Strike (tie by price: Healbane is 1.6k net so tie by slot, not by price: label it a slot-swap), F = Arcane Surge -> Warp Stone, G/H = openings (Charge first / ult first).
Script per block: `fetch 150; enemies 4 R` with R in {8,10,12,14} m x k (ring placed at fixed radius); `mark cov_<arm>_<R>; cast 1 2; mark none; wait 6`. Metric 1: number of distinct ring victims with Siphon rows (coverage vs radius, shows the expansion and T3 radius). Metric 2 (retention, ratchet proxy): `cast 1 0.3` then 8 x [`fetch (R+1.2*n)*k`; `wait 0.5`] with the bot pushed out 1.2 m per 0.5 s (about 2.4 m/s of "escape", scaled to match runner minus tank speed [U]); count Siphon rows. Heal per block from `healsum` (start `lowhp 60`). Proxy only; true kiting is UNSUPPORTED.
Pass for "add Mystic Slow": coverage/retention gain above noise AND P4 shows the slow modifier on every ring bot for the Siphon duration AND no loss of Arcane Surge effect that outweighs it (measure Arcane Surge: `cast jump; cast 1 2` vs `cast 1 2`, dash-jump may need `cast alt`; if the dash-jump cannot be scripted, Arcane Surge is UNTESTABLE and the swap stays a "cannot determine").

### T-U Siphon uptime and cooldown  RUNNABLE after P3
`fetch 150; enemies 3 250; mark up_<arm>; (cast 1 0.3 ; wait 0.5) x 120 ; mark none` for arms none, +Duration Extender, +Duration+Compress, full TB45 set. Metric: damage-row span per cast (duration), recast interval between starts (cooldown), uptime fraction = span/(span+gap). Reads real timing from the csv (cooldown readers are garbage, AUTORUN).

### T-S survival under focus (T2, T3)  RUNNABLE, flagged
Price points TB12, TB20, TB30. `lowhp 0`; stream `incoming gun 250` for 4 s then `incoming spirit 150` for 4 s repeated; `enemies 5 8`; player loop `cast 2 1.8; cast 1 2; cast 4 1.8; cast 1 2`. Arms at TB20: A base; B Mystic Vulnerability -> Toughness; C -> Debuff Reducer (both T2 1.6k tie; MV returns before Escalating Exposure). Metric: time until HP 0, total healed (`healsum`), Siphon damage. Flags: Debuff Reducer's value (CC) invisible without `ecc`; P1 must pass or all heal-derived numbers are biased low.

### T-O1 Spirit Snatch vs Torment Pulse vs none  RUNNABLE (substitution valid; absolute biased by missing Siphon imbues if P3 fails)
TB20 base vs Spirit Snatch -> Torment Pulse (T3 tie) vs Spirit Snatch removed. `enemies 5 8; fetch 150; mark o1_<arm>; cast 4 1.8; cast 1 2; cast melee 0.4 x6; cast 2 1.8; wait 3; mark none`, plus `eresist gun 25` and `eresist off`. Metric: damage per cycle over 12 s (split by victim), Spirit Snatch shred effect visible only through damage to the target after the melee; Torment Pulse pulses (closest two).

### T-P Ult answer / unstoppable window  RUNNABLE (names only)
P5 above. Real stun/silence interrupts UNSUPPORTED.

## 6. Regression sweep of the candidates
- Mystic Slow for Arcane Surge: same tier/colour/slot, spirit 4.8k spike at 5.6k unchanged; loses +12% radius/+15% duration/+20 spirit after a dash-jump (Arcane Surge also gives stamina), gains +50 HP. No new dependency except enemy taking spirit damage. Sells in boxes (Counters, Spirit Burn) name Arcane Surge, so they would name Mystic Slow instead.
- Debuff Reducer in Counters menu: a T2 bought late conflicts with "no fresh T2s late", but it is a menu item bought by cause and sold for it; first sell is Arcane Surge.
- Torment Pulse for Spirit Snatch: loses melee-based shred and 75 HP, gains 100 HP, 18% melee resist; a pulse needs no punching. Spirit 9.6k at 14.4k unchanged.
New weaknesses introduced by the default outcome (no change): none.

## 7. Runnable summary
RUNNABLE now: P0, P1, P4, P5 (names), P3 (gates Siphon tests), T-R1 (proxy retention, coverage exact), T-U, T-S (flagged), T-O1.
BLOCKED until P3: every Siphon-imbue score (T-U, T-R1 radius, absolute damage).
UNSUPPORTED (needs op): real kiting/dash (`emove`), stun/silence/slow on the player (`ecc`), enemy anti-heal (`eheal`), imbue assignment (`imbue`), NPC/camps, allies, bot shoot-back, wall control, slow magnitude or stacking.
Data gaps: Siphon cooldown, Charge reach/cooldown/slow %, Seismic Impact range, Mystic Slow trigger threshold, whether radius upgrades are additive.


## I. Practicality (WEAKNESS_PROCESS section I; added 2026-10-24, appended, nothing above changed)
Sources added: game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` (weapon, cooldowns, ability upgrades) and `heroes.vdata` (level table), plus data.js walk (prac/out/walk_abrams.txt, regenerated, 0 flags). Level table: abilities unlock at 0 / 500 / 1.4k / 3.2k souls, 1 ability point at every other level up to 48.6k (32 points = 4 abilities x 1+2+5, so tier costs 1/2/5 [U, consistent]). Time: ~7k at 8:00, ~1k/min after (late times are upper bounds).
New kit numbers (fill the [GAP]s in sections 1, 5, 7): Siphon Life cooldown 42 s (T1 -20 s), duration 4 s (T2 +2 s), DPS 22 + 0.6x spirit per target (T3 +18 DPS, +0.12x, +2 m). Shoulder Charge cooldown 33 s (T1 32% slow 3 s, T2 +0.8 s wall stun, T3 -18 s). Seismic Impact cooldown 215 s (T1 -30 s, T2 +0.8 s stun, T3 5 s Unstoppable +6 m). hero_abrams.txt drops the cooldown upgrades.

### I.1 Ability points vs item timing (main finding)
Order 3312224444111332 spent as soon as points arrive: Infernal T1 0.2k; Siphon unlock 0.5k; Charge T1 1.4k, T2 2.6k; Seismic 3.2k, T1 3.9k, T2 5.3k, T3 9.2k; **Siphon T1 10.1k**, T2 11.9k, T3 17.4k; Infernal T2 20.6k, T3 32.1k; Charge T3 48.6k.
Problem: Duration Extender (4.8k) is imbued on a Siphon that stays on a 42 s cooldown until 10.1k, so the build's heal/damage/imbue hub runs at ~12% uptime (1.4 casts/min) from 4.8k to 10.1k (~5:30 to 11:00).
Candidate ALT-A1 = 3,3,1,2,2,2,4,4,**1**,4,4,1,1,3,3,2 (Siphon T1 straight after ult T1): Siphon T1 4.6k (5.5k earlier), ult T2 6.0k (+0.7k), ult T3 10.1k (+0.9k); nothing else moves.

| souls | current: Siphon dur / cd / uptime (cd from cast; cd after end) | ALT-A1 |
|---|---|---|
| 5k-10k | 4.9 s / 42 s / 12% (10%), 1.4 casts/min | 4.9 s / 22 s / 22% (18%), 2.7 casts/min |
| 12.5k | 7.3 s / 18 s / 41% (29%) | same |
| 20k | 7.7 s / 17.6 s / 44% (30%) | same |

Value at 7k (spirit about 23 = Extra Spirit 10 + 12 level boons x 1.1): one Siphon = 36 DPS x 4.9 s = 175 damage and 147 HP per hero in range (70% x Healing Booster 1.2). ALT-A1 adds about +1.3 casts/min = +230 damage and +190 HP per hero per fighting minute in that window, doubles Healbane procs and the 35% camp heal, and halves the time a silence on Siphon (Chain A) costs before 10.1k. Cost: the 2.4 s ult stun and the 5 s Unstoppable arrive about 1 min later on an ult used once per 185 s.
Decision: propose ALT-A1 to the reviewer as an ability-order change (not applied). Grade: CALCULATED for the uptime (game-file cooldowns; assumes points are spent at once and cooldown starts on cast [U, probe PR-A1]); the fight value of an earlier Unstoppable is UNTESTABLE-HIGH-RISK. Confidence 55%. Wrong if: PR-A1 shows a different cooldown, or lane fights at 5-10k are decided by the ult's 2.4 s stun.
Other order facts: Infernal T3 (+20% debuff resist, named as a Chain A PREVENT answer) arrives at 32.1k (~33 min) and Charge T3 at 48.6k, so Charge is a 33 s engage all game. Accept (the build's damage is Siphon), but Chain A's "debuff resist" answer is late in real play.
Sandbox validity: `unlock 7` at TB12/TB20 grants Siphon T3, Infernal T3 and Charge T3 that the real order has at 17.4k/32.1k/48.6k, so T-S and T-U are biased toward survival and uptime. `unlock` is global; use `unlock 3` (T1+T2) for TB12 Siphon tests and state the remaining bias (Infernal T2, Charge T3 granted).

### I.2 Gun economy
No gun items in the build. Shotgun: 9 pellets x 3.6 (+0.1 per pellet per level), 9 shells, 0.63 s per shot (5.7 s to empty), shell-by-shell reload 0.705 s + 0.353 s per shell (3.9 s full, cancellable). Irrelevant to this build's output; no action. CALCULATED, 80%.

### I.3 Farming
No farm tool: Spirit Strike/Snatch proc on heroes only; Siphon heals 35% vs NPCs but is on a 42 s cooldown until 10.1k (ALT-A1: 22 s from 4.6k, which also helps camp sustain). Farm = shotgun at close range (falloff starts 669 u) + punches. The build ignores farm speed (T8). Accept. CALCULATED; measuring it UNSUPPORTED (no NPC/camp op).

### I.4 Spike timing vs survivability (incl. the countered case)
Spirit 4.8k at 5.6k (~6:30), health 4.8k at 9.6k (~10:40): matches the Abrams rule (green right after the first damage spike). Orderings compared:
- A current: as above.
- B health first (Healing Booster, Healbane, Enduring Speed before Arcane Surge/Duration Extender): health 4.8k at ~4.8k, spirit 4.8k slips to 9.6k, Siphon duration imbue later.
- C Witchmail before Greater Expansion (T2 in section 3).
Abrams has no escape; his defence is Siphon heal + Infernal regen. When Siphon is silenced (Chain A) he has only regen and item HP, and under the current order a lost Siphon costs 42 s of sustain until 10.1k. Health is already early, so the countered case argues for ALT-A1 (shorter Siphon cooldown) rather than for moving more health forward.
Decision: keep the item order. Grade: CALCULATED (spike maths) + UNTESTABLE-HIGH-RISK (fight value). Confidence 55%. Wrong if T-S at TB12 (with `unlock 3`) shows B surviving clearly longer than A.

### I.5 Buttons and new-player load
3 abilities + Scourge (35.2k) is the only core active: low. Arcane Surge (3rd buy, 3.2k) only gives +12% radius, +15% duration, +20 spirit if he dash-jumps within 7 s before Siphon; without that input it is +1 stamina. Options: playstyle note "dash-jump, then Siphon" (free); the Mystic Slow swap already named in T1; accept. Decision: note only. UNTESTABLE-HIGH-RISK (input execution), 40%.

### I.6 Slot lock and sell chain
9 slots at 12.0k, 10 at 20.0k (~21 min, around the flex-slot unlock in the rules). Every T1/T2 is upgraded or named in a sell. The Counters menu names one sell (Arcane Surge); a second counter has no named sell (Spirit Burn falls back to Superior Duration, Infuser takes Healbane, Colossus takes Spirit Snatch). Reviewer note: name a second Counters sell. CALCULATED, 70%.

### I.7 Forgiveness when behind
Early buys are 0.8-1.6k steps and the spirit spike lands at 5.6k whatever happens; the first 6.4k buy is Witchmail at 28.8k (Witchmail and Scourge have no components: ~6 min of saving each, late). Weak point: six Siphon items lose their value whenever Siphon is down or silenced (T7). High forgiveness early, medium mid. No change. CALCULATED, 60%.

### I.8 Tests (existing ops only)
PR-A1 Siphon cooldown semantics (gates I.1 numbers), RUNNABLE:
```
setup Atlas Haze
hardreset
unlock 0
fetch 150
ekeep 1
ehp 50000
mark pra1_t0
cast 1 0.3
wait 5
# then 50 x: cast 1 0.3 / wait 0.7
mark none
```
Repeat after `unlock 1` (T1 on all abilities). Read the start times of Siphon damage bursts: about 42 s apart (22 s with T1) = cooldown from cast; about 46 s (26 s) = cooldown after the 4 s duration. n=3 per arm (deterministic timer). ALT-A1 vs current as an A/B: UNSUPPORTED (no per-ability tier op; needs `abilitypoints`, GAPS #2). Farm and countered-Siphon survival: UNSUPPORTED (no NPC op, no `ecc`).

### I.9 Regression (F) for ALT-A1
No item, spike, slot or sell change. Ult T2/T3 about 0.7-0.9k later, so the Chain A PREVENT line "ult first so the cheap ability eats the CC" is weaker for ~1 min. No new serious weakness; no second loop.

| problem | candidates | chosen | cost | grade | conf. |
|---|---|---|---|---|---|
| Siphon T1 at 10.1k under six Siphon items | ALT-A1, keep | propose ALT-A1 (reviewer) | ult T2/T3 ~1 min later | CALCULATED (+UNTESTABLE part) | 55% |
| Health timing | A/B/C | keep A | 0 | CALCULATED + UNTESTABLE | 55% |
| Arcane Surge needs dash-jump | note, Mystic Slow, accept | note | 0 | UNTESTABLE-HIGH-RISK | 40% |
| One named Counters sell | name a second | reviewer note | 0 | CALCULATED | 70% |
| Gun, farm, forgiveness | accept | leave | 0 | CALCULATED | 60-80% |


## J. Item roles (WEAKNESS_PROCESS J; added 2026-10-24, appended, nothing above changed)
Sources: audit/items_full.json [i]; game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` [g] (imbue filters, cooldowns, scaling tags) and `gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt` [l]; audit/hero_abrams.txt [k]; walk prac/out/walk_abrams.txt. Grades: C = CALCULATED, U = UNTESTABLE-HIGH-RISK, M = MEASURED (none).

### J.0 Game-file facts that change earlier statements
- Only Duration Extender, Mystic Expansion and Compress Cooldown are imbues (EApplyFilter_OnlyIfImbued) [g]. Their upgrades Superior Duration (16.8k), Greater Expansion (22.4k) and Superior Cooldown (18.4k) have no filter: global, "abilities and items" for duration and range [g/l]. The component is consumed on upgrade [i], so Siphon goes +22% -> +28% duration, +20% -> +30% radius, -18% -> -20% cooldown: never +50% radius (T1 accept row and section 4 model).
- Cooldowns [g]: Spirit Strike 8 s (x2 on light), Spirit Snatch 6 s, Scourge 35 s, Colossus 37 s, Infuser 30 s, Dispel 45 s, Counterspell 23 s, Metal Skin 24 s, Spellbreaker 9 s.
- Dispel Magic [l]: purges all non-ultimate negative effects; heal and speed only if something was removed; not usable while stunned or slept.
- Healing Tempo [l]: every heal he applies (not innate regen or passive lifesteal) gives +35% fire rate and +1.25 m/s for 7 s; Siphon's heal is an ability heal [U that it counts].
- Spellbreaker carries 25% debuff resist always [i]; Debuff Reducer is its component (and Unstoppable's) [i].

### J.1 Item roles
| item (box, souls) | every effect [source] | what it feeds | matters from | grade |
|---|---|---|---|---|
| Extra Regen (0.8k, becomes Healing Booster) | +2.5 regen, OOC 1.5 [i] | lane sustain | at once | C |
| Spirit Strike (1.6k, becomes Snatch) | melee vs a hero: +40+0.372x spirit damage and -6% spirit resist 6 s; 8 s cd (16 s on light) [i/g] | lane trades; the -6% feeds Siphon on that target; spirit damage applies Healbane/MV/EE | at once | C |
| Arcane Surge (3.2k, from Extra Stamina) | after a dash-jump, the next ability within 7 s gets +12% range/radius, +15% duration, +20 spirit; +1 stamina, -12% stamina cooldown [i] | stamina: one more dash for chasing a kiter or leaving (T1, T11: the build has no other mobility item); the window buffs whichever ability is next: Siphon, Shoulder Charge (+15% duration = longer charge [U], +12% range), Seismic (+12% radius) | stamina at once; window needs the dash-jump input | C (stats), U (charge length) |
| Duration Extender (4.8k, Siphon imbue, becomes Superior Duration) | +22% duration on Siphon only [i/g] | Siphon 4 -> 4.9 s while Siphon is on a 42 s cooldown until 10.1k (I.1) | at once, low value until Siphon T1 | C |
| Extra Spirit (5.6k, becomes Improved) | +10 spirit [i] | Siphon +6 DPS per target (0.6x), Spirit Strike | at once | C |
| Healing Booster (6.4k) | +20% cast and regen healing, +3 regen [i] | Siphon heal, Infernal regen, Healbane kill heal 275 -> 330, Dispel heal; becomes Healing Tempo (slot locked) | at once | C |
| Healbane (8.0k) | his spirit damage: enemies -35% healing 8 s; 275 heal if one dies under it; +7 spirit [i] | team anti-heal (Siphon applies it to everyone in radius), kill sustain; Infuser's sell | at once | C |
| Enduring Speed (9.6k) | +2 m/s, 25% slow resist, OOC 2 [i] | staying inside Siphon radius (T1), chasing, leaving | at once | C |
| Mystic Expansion (10.4k, Siphon imbue, becomes Greater Expansion) | +20% range and radius on Siphon only [i/g] | Siphon 8 -> 9.6 m (12 m with T3) | at once | C |
| Compress Cooldown (12.0k, Siphon imbue, becomes Superior Cooldown) | -18% Siphon cooldown [i/g] | Siphon uptime (T5) | at once (Siphon T1 10.1k) | C |
| Spirit Snatch (14.4k) | melee vs a hero: +50+0.84x spirit damage, steals 12% spirit resist and 25 spirit power for 10 s, +7% melee damage, +75 HP; 6 s cd [i/g] | +25 spirit = Siphon +15 DPS per target and Scourge for 10 s (12.8 s with Superior Duration); +12% spirit resist self (survival, T2); -12% on the target (Siphon/Scourge on it); applies Healbane/MV/EE | at once | C |
| Improved Spirit (15.2k, becomes Boundless) | +18 spirit, +75 HP, +1 m/s sprint, OOC 1.5 [i] | Siphon, Scourge, Strike/Snatch scaling; HP | at once | C |
| Superior Duration (16.8k) | global +28% ability and item duration, +8% bullet resist [i/g/l] | Siphon (+6% over the imbue), Scourge 10 -> 12.8 s, Healbane 8 -> 10.2 s, MV 7 -> 9 s, EE 12 -> 15.4 s, Snatch steal 10 -> 12.8 s, Strike shred, Charge T1 slow 3 -> 3.8 s; Charge length, Seismic stun, T3 Unstoppable [U which ability timers scale]; rich Colossus 7 -> 9 s, Infuser 7 -> 9 s; the first bullet resist in the core (T2) | at once | C, U (which timers) |
| Superior Cooldown (18.4k) | global 20% ability cooldown, OOC 4 [i/g] | Shoulder Charge 33 -> 26.4 s (15 -> 12 s at T3), Seismic 185 -> 148 s, Siphon 18% -> 20% | at once | C |
| Mystic Vulnerability (20.0k, becomes Escalating Exposure) | spirit damage: -8% spirit resist on the target 7 s; +8% spirit resist self [i] | Siphon/Scourge damage; survival vs spirit | at once | C |
| Greater Expansion (22.4k) | global +30% range and radius of abilities and items, +10% spirit resist [i/g/l] | Siphon (13 m at T3), Scourge aura 10 -> 13 m and ally cast 35 -> 45.5 m, Seismic radius [U], rich Colossus 14 -> 18.2 m; spirit resist | at once | C |
| Witchmail (28.8k) | +14 spirit, 22% spirit resist, 7% CDR; each enemy spirit hit >= 75 takes 4 s off a random ability [i/l] | tank role: being focused returns Siphon/Charge/Seismic sooner; spirit survival | at once | C |
| Scourge (35.2k) | self or ally (35 m): +40% spirit resist, +20% debuff resist, existing debuffs reduced, 2.3% of enemy max HP/s in 10 m for 10 s, +100 HP; 35 s [i/g] | damage that scales with enemy HP; Chain A PREVENT/RECOVER; a team role (on the carry); gains from Superior Duration and Greater Expansion | at once | C |
| Boundless Spirit (40.0k) | +30 spirit, +15% spirit power, +75 HP, OOC 4 [i] | every spirit scaler | at once | C |
| Escalating Exposure (44.8k) | spirit hits stack +4.5% spirit amp (12, 0.7 s), 17% spirit resist, -8% spirit armor 12 s [i/g] | Siphon ticks (4/s) stack it to 12 in ~8.4 s on every target in radius; Scourge; survival | at once | C |
| Counters: Plated Armor / Metal Skin / Bullet Resilience | 30% deflect, 50% on-hit prevention, +130 HP / 5 s bullet immunity 24 s, 12% bullet resist / 30% bullet resist (+15 below 50%) [i/g] | gun focus (T2) | at once | C |
| Counters: Spirit Resilience / Spellbreaker | 30% spirit resist / 65% off the next spirit hit >= 175 (9 s), 18% spirit resist, 25% debuff resist always, +90 HP [i/g] | spirit focus; Spellbreaker's passive also shortens every CC (T3) | at once | C |
| Counters: Counterspell | parry 0.8 s blocks ability/item damage and effects; on success 150 heal, +1.75 m/s, +20 spirit 6 s; 23 s [i/g] | telegraphed ults (Chain A PREVENT) | at once | U |
| Counters: Dispel Magic | purge non-ultimate negatives (hex, burn, a pending Knockdown [U]); then 250 x 1.2 heal and +2 m/s 3 s; 10% spirit resist; 45 s [l/g] | Chain A RECOVER (silence), Chain B (hex/slow out of radius), Chain C (anti-heal); chase speed | at once | C, U (timing) |
| Rich: Infuser (sells Healbane) | always: 13% spirit LS, +6 spirit, +100 HP, 10% spirit resist; active 7 s (9 s with Superior Duration), 30 s cd: 70% spirit LS and +30 spirit [i/g] | Siphon heal (additive with Siphon's own 70% [U]), +18 Siphon DPS per target in the window; loses Healbane's team anti-heal and kill heal | at once | C, U (stacking) |
| Rich: Spirit Burn (sells Arcane Surge) | 500 spirit damage in 5 s on one enemy: explosion, 8 s burn, -70% healing; 20 s per enemy [i] | Siphon + Scourge reach it; anti-heal; loses Arcane Surge's stamina | at once | C |
| Rich: Colossus (sells Snatch) | 7 s: +35% bullet and spirit resist, 24% slow and -22% dash speed in 14 m, +30% melee, +15% weapon damage; +25% base HP; 37 s [i/g] | T1 retention: 18.2 m slow aura for 9 s with Greater Expansion and Superior Duration, i.e. larger than Siphon's radius; survival | at once | C |
| Rich: Divine Barrier (sells Dispel) | non-stun cleanse, 600 barrier, +2.75 m/s 6 s, ally-castable 40 m (52 m with Greater Expansion), 45 s (half on allies) [i] | self RECOVER and peeling his team (tank role) | at once | C |
| Slot locked: Healing Tempo | +25% heal amp, +6 regen, +10% spirit resist; +1.25 m/s 7 s after each Siphon heal [i/l, U trigger] | T1 retention (speed while draining), sustain | when a slot frees | C/U |
| Slot locked: Juggernaut / Transcendent Cooldown | +2.5 m/s, 50% slow resist, 25% melee resist, +8 regen, attackers' fire rate -40% / 25% ability and item cooldown (Scourge 35 -> 26 s) [i/l] | T1, T2 / Scourge and ability uptime | when a slot frees | C |

### J.2 Earlier verdicts re-opened with all roles counted
| earlier verdict (section) | role it was judged on | roles added | restated verdict | changed? | grade, conf. |
|---|---|---|---|---|---|
| T1 / section 4: Mystic Slow <-> Arcane Surge as the named candidate | Arcane Surge's Siphon range/duration after a dash-jump | +1 stamina and -12% stamina cooldown (the build's only added mobility, T1 and T11), and the window also buffs Shoulder Charge and Seismic | Candidate demoted: Mystic Slow would trade the only extra dash for a slow that needs Siphon damage. Test it only if T-R1 shows a large retention gain, and the decision must price the stamina role, which the Sandbox cannot measure (UNSUPPORTED) | yes (demoted) | U, 30% |
| T1 accept row "Siphon +50% radius already built"; section 4 radius model | radius items summed | Mystic Expansion is consumed by Greater Expansion | Siphon +20% (10.4k-22.4k), then +30%: (8+2) x 1.3 = 13 m at T3 if the +2 m is added first. Verdict unchanged | number corrected | C, 70% |
| T7 / Chain A "six imbue items die with Siphon" | items as Siphon imbues | three are imbues only until 16.8k/18.4k/22.4k; from then the upgrades are global: Charge and Seismic cooldown -20%, Scourge/Healbane/MV/EE/Snatch durations +28%, Scourge/Colossus radius +30% | The single point of failure is three items' worth from 4.8k to ~22.4k, then small. LEAVE unchanged; severity M -> L-M after 22.4k | severity yes | C, 50% (was 40%) |
| Imbue target choice (section 1: all three on Siphon) | Siphon only | while Siphon sits on 42 s until 10.1k (I.1), Duration Extender on Shoulder Charge would lengthen the charge (+22%) [U that charge distance scales with duration] | Keep Siphon (the hub once ALT-A1 or Siphon T1 lands). Charge-imbue for 4.8k-10.1k is a named candidate only | no (new candidate) | U, 30% |
| T2 durability gap "no vitality spend 9.6k-28.8k" | health-colour items | Superior Duration +8% bullet resist (16.8k), Snatch +12% stolen spirit resist and +75 HP (14.4k), Improved Spirit +75 HP, MV +8% (20.0k) and Greater Expansion +10% (22.4k) spirit resist | The gap is real vs gun (8% only until the menu) and smaller vs spirit. LEAVE unchanged | no (reasoning) | U, 40% (was 35%) |
| T3 Debuff Reducer in Counters; regression "a T2 bought late" | Debuff Reducer alone | it is the component of Spellbreaker (already in the menu) and Unstoppable; Spellbreaker's passive 25% debuff resist was not counted | Regression concern withdrawn: Debuff Reducer is a step into Spellbreaker, not a dead T2. Situational note stands | yes (regression) | U, 35% (was 30%) |
| T4 Spirit Snatch vs Torment Pulse (inconclusive) | melee damage, shred, HP | Snatch's stolen +25 spirit feeds Siphon (+15 DPS per target) and Scourge; +12% spirit resist self. Pulse: no-input pulses on 2 targets every 1.4 s that keep MV/EE/Healbane applied; 18% melee resist | INCONCLUSIVE unchanged; T-O1 cast Siphon before the punches, so it never measured Snatch feeding Siphon: add a punch-first arm (J-A3) | test changed | C, 30% |
| Rich Colossus "KEEP in rich box (medium)" | slow aura | 18.2 m for 9 s with Greater Expansion and Superior Duration | KEEP; it is the strongest T1 retention item in the data for this build | no (stronger) | C, 55% |

### J.3 Tests that separate the roles (AUTORUN.md ops; `setup Atlas Haze`; A/A n=6, ABBA n=6; effect > 2 x A/A SD; upgrade classes only)
- J-A1 imbue vs global (extends P3): arm G = `give upgrade_tech_range` (Greater Expansion, no imbue), `unlock 7`, ring at 12.5 m x k: `cast 4 1.8` (Seismic 9 m base -> 11.7 m only if global reaches it; ImpactRadius scaling [U]) and `cast 1 2` (Siphon 10 m -> 13 m). Victims beyond the base radius in G and not in the no-item arm = global confirmed. RUNNABLE.
- J-A2 Superior Cooldown on Charge: PR-A1 recipe with `cast 2 0.3` repeated (Charge) with vs without `upgrade_cooldown_reduction`; start-to-start spacing of Charge damage rows 33 vs 26.4 s. RUNNABLE.
- J-A3 Snatch feeding Siphon: TB20, `fetch 120`, arm P = `cast melee 0.4` then `cast 1 2`; arm S = `cast 1 2` then `cast melee 0.4`; Siphon damage per tick per target (expect +0.6 x 25 = +15 DPS in P). RUNNABLE.
- J-A4 Superior Duration on Scourge: `give upgrade_discord` with vs without `upgrade_imbued_duration_extender`; self-cast mapping of `cast i1` is unknown (smoke-test; `use` op is in src/Realism.cs, not in AUTORUN.md); span of Scourge damage rows 10 vs 12.8 s. RUNNABLE if self-cast works.
- Arcane Surge's stamina dash and buffed Charge length: UNSUPPORTED (no stamina or velocity readout; dash-jump not scriptable as one input). Healing Tempo's speed on Siphon heal: names only (`give upgrade_healbuff`, `cast 1 2`, `mods`), RUNNABLE, low priority (slot locked).

### J.4 Regression (F)
No item or order change. Corrections: radius +30% not +50%; six imbues -> three until 22.4k. If the Mystic Slow candidate were ever adopted, the new weakness is no added mobility at all (stamina lost). No second loop.

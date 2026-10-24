# Victor spirit ("Aura Farming Victor", data.js id victor) - weakness -> remedy
Written 2026-10-24 by weakness-solver. Sources: data.js build (core order below), audit/items_full.json, audit/hero_victor.txt, GAPS.md, playstyle/victor.md, RULES_KIERAN.md, plans/victor.md, results (gun-only lifesteal; no spirit-build result exists). No game or data.js changes.
Revision 2 (2026-10-24, updated WEAKNESS_PROCESS A2 + H): added section A2 (identity map, verified counters, ranked chains VC1-VC5, aura-loop model, PREVENT/RECOVER/SURVIVE, counter-the-counter), the verified Leech/Spirit Lifesteal correction (A2.6), evidence grades on every verdict, a re-ranked summary. First-pass analysis and tests kept below.

## A2. Hero identity map and dependency chains (revision 2, 2026-10-24, per WEAKNESS_PROCESS A2/H)
Added on top of the first pass; sections 0-5 are kept and graded. Tags: [kit]/[item] = audit/hero_victor.txt / audit/items_full.json; [GAP] = not in the data; [U] = game knowledge to verify. Build walked from data.js (wk2/walk_victor.txt): spirit 4.8k at 5.6k, health 4.8k at 9.6k, core 59.2k / 12 slots (no gun items). Ability points (order 3312341312214424): Aura 1/2/5/8 (T1 20% slow + dash slow at 2, T2 at 5, T3 +1 m and enemies take +15% damage at 8), Pain Battery 3/7/9/12 (T3 heal at 12), Jumpstart 4/10/11/15 (T3 50% debuff resist at 15), Reanimation 6/13/14/16 (T2 100% HP revive at 14, T3 stun at 16). Frequency proxy: share of the Council's 81 builds (44 heroes) buying the counter in core; not a public pick rate. Note: audit/walk_victor.txt is stale (an older "Aura Brawler" version); the regenerated walk is wk2/walk_victor.txt.

### A2.1 Identity map
| strength [source] | compensates | depends on |
|---|---|---|
| Aura of Suffering: 8 s channel, 2 s cd, 13 -> 58 dps (+0.15 -> 0.72x spirit), 8 m (+20% imbued Mystic Expansion 12.0k, +30% Greater Expansion 25.6k, +1 m T3), ticks 0.25 s, self-damage 70% of dealt + SelfDPS 15 [kit] | No gun items: it is the build's main damage, and it hits everyone near him | Enemies inside ~8-12 m for the ramp (ramp time [GAP]); not interrupted; HP to pay the self-damage; low enemy spirit resist |
| Self-sustain loop: Spirit Lifesteal 13 (8.0k) -> Infuser 13 passive / 70 active for 7 s (16.8k; cd [GAP]), Healing Booster +20% (6.4k), Jumpstart regen 100 +70 +1.2x over 4.5 s (Compress imbued 18.4k), Pain Battery T3 15% missing HP, Juggernaut 8 regen (46.4k), Scourge self-cast (36.8k) [item/kit] | The aura's self-damage and standing in melee range | Infuser active up; enemies in the aura (hero lifesteal only, NPC 3%); healing not reduced |
| Shocking Reanimation: as in the gun file; 100% HP revive from point 14, stun from 16; Superior Cooldown (30.4k, global 20% [U for ult]) | No escape, full commitment | Cooldown; [GAP] whether silence/stun at the lethal moment blocks it |
| Pain Battery: charges from any damage taken (40% max HP stored), 7 bolts, 28 m, 100 + 1.6x per target, T1 32% slow 2 s, T3 heal 15% missing HP [kit] | Ranged burst and slow when he cannot reach; turns being focused into damage + heal | Taking damage (from enemies; self-damage [GAP]); bolts hitting (spread 40 degrees) |
| Reach: Sprint/Enduring Speed (+2 m/s, 25% slow resist, 9.6k), Warp Stone (11 m blink, +30% bullet resist 6 s, 28.8k), Jumpstart +3 m/s, Aura T1 slow 20% / dash slow, Juggernaut 50% slow resist (46.4k) [item/kit] | Short-range kit | Slows, movement silence (Warp Stone is a movement item), Jumpstart cooldown |
| Scourge self-cast: +40% spirit resist, +20% debuff resist, "existing debuffs on the target are reduced", 2.3% max HP/s aura 10 m [item] | Spirit burst, CC and anti-heal durations; extra AoE | 36.8k; cast delay 0.25 s; not silenced? (item, [U]) |

### A2.2 Enemy counters (verified in the data)
- Anti-heal (cuts lifesteal, Infuser, Booster, Jumpstart regen, Pain Battery heal; does NOT cut the aura's self-damage): Toxic -35, Inhibitor -40, Crippling -35, Healbane -35, Decay -50, Spirit Burn -70 (once per 20 s per enemy), Haunting Shot -40, Nullification Burst prevents healing; kit Venator -30 [item/hero]. Core 47/81 builds; P(>=1 of 6) > 99%.
- Spirit resist vs the aura: Spirit Resilience (30%, +15 below 50% HP; Counters in 67/81), Spirit Armor, Escalating Exposure holders' own resist, Scourge, Witchmail; Spellbreaker (65% off the next hit >= 175) does not trigger on 0.25 s aura ticks but does on Pain Battery bolts at high spirit [item]. Return Fire reflects 25% of spirit damage back at Victor (adds to self-damage).
- Out-ranging and slowing him: kiting heroes/ranged builds; slows core 27/81 (Slowing Hex 16% + movement silence, Capacitor, Vortex Web, Cold Front 48%, Arctic Blast freeze, Point Blank, Mystic Slow, Phantom Strike); movement silence (Slowing Hex, Capacitor) blocks Warp Stone.
- Channel break: Cursed Relic interrupts (explicit); Haze Sleep Dagger and Infernus Concussive interrupt (explicit); stuns from items/kits [U that they break the aura channel]; Silence Wave explicitly does NOT interrupt channels (blocks the recast).
- Revive: no item targets it; behavioural counter (wait out the 3 s channel outside 18 m, re-kill, bait 240 s).
- Invulnerability/untargetable on them: Ethereal Shift (4 s), Kelvin Frozen Shelter, Prism Blast: aura ticks deal nothing, self-damage then only SelfDPS 15 [U].

### A2.3 Chains ranked by frequency x lethality
| rank | chain | freq | lethality |
|---|---|---|---|
| VC1 | Aura damage covers "no gun"; lifesteal/Infuser covers the aura's self-damage; anti-heal cuts the heal side only, so the loop turns into self-harm | H (>99%) | H: he damages himself 70% of what he deals while healing a fraction of it |
| VC2 | Aura/Torment/Scourge need 8-12 m; speed + Warp Stone + aura slow cover it; kiting, slows and hex (blocks Warp Stone) keep him out | H vs ranged comps | L-M: useless rather than dead (Pain Battery still reaches 28 m) |
| VC3 | Revive covers no escape; wait-out/re-kill makes the second death final | M | H after a death |
| VC4 | Aura ramp needs an unbroken channel; stuns/curse/interrupts reset it, and the CC also lets them leave | M (item stuns core 15/81 + kits) | M |
| VC5 | Pain Battery needs 40% max HP of damage taken; with more HP (health items) and no self-feed it is rarely ready | M | L |

### A2.4 VC1 in three layers (CALCULATED loop model)
Model (per second of aura on heroes, D = aura damage dealt to heroes; assumptions: self-damage = 0.70 D + 15, lifesteal applies to aura ticks at full rate, Healing Booster's +20% applies to lifesteal [U], Infuser's 70% active is the total during the active (if it adds to the 13% passive, read 83%)):
net/s = D x h x 1.2 x (1 - a) - 0.70 D - 15, with h = 0.13 (passive) or 0.70 (Infuser active) and a = anti-heal.
- h = 0.70: a = 0 -> +0.14 D - 15 (positive once D > ~107 dps); a = 0.35 -> -0.15 D - 15; a = 0.70 -> -0.45 D - 15. Break-even anti-heal = 1 - 0.70/(0.70 x 1.2) = 17% (30% if the active is 83%).
- h = 0.13: a = 0 -> -0.54 D - 15 (always negative); worse with anti-heal.
- Leech instead (28%, both sides): -0.36 D - 15 at a = 0: never sustains the aura either; its value is average lifesteal and anti-heal mitigation [GAP], not the loop.
So the loop is only self-sustaining inside the Infuser window and only under at most ~17-30% anti-heal; every 35-70% anti-heal item in the data is above that (Venator's 30% grenade sits at the edge). Under anti-heal the aura is a deliberate HP trade, paid by Jumpstart regen (also cut), Juggernaut regen, Pain Battery heal and the revive.
PREVENT: (a) ability use: run the aura only with Infuser active, in short bursts otherwise, and stop it when the anti-heal debuff is on him (playstyle; no cost); (b) target choice: Pain Battery (28 m) and Torment Pulse on the anti-heal carrier first; (c) Plated Armor (Counters) halves bullet on-hit anti-heal build-up [U for build-ups]; nothing in the data prevents spirit-sourced anti-heal (Healbane, Spirit Burn, Decay) except Counterspell (parries one ability/item hit, so one Decay cast) and not taking that damage.
RECOVER: (a) Divine Barrier (rich box, verified "Remove all non-stun debuffs", 600 barrier): vs Spirit Burn the per-enemy 20 s lockout means a cleanse buys about 12 s of clean healing; vs Decay a 12 s debuff removed; vs bullet build-ups it reapplies in seconds. (b) Scourge self-cast (core 36.8k): "existing debuffs are reduced" + 20% debuff resist: shortens, does not remove [U whether heal reduction counts as a debuff here]. (c) Dispel Magic (Counters): scope not in data [GAP].
SURVIVE: stop the aura (removes the 0.70 D cost at once: the cheapest answer), Jumpstart regen, Juggernaut regen, revive; spirit/bullet resist from Counters; Warp Stone out (+30% bullet resist 6 s).
Counter-the-counter: bullet anti-heal reapplies after Divine Barrier; Nullification Burst prevents healing; Cursed Relic blocks items (no Divine Barrier/Scourge for 3.25 s); two anti-heal sources [U stacking]; enemies with spirit resist reduce D and therefore his lifesteal (and possibly his self-damage, [U]).
Verdict VC1: keep core (Infuser stays: it is the only item that makes the loop positive, and Leech cannot); add a playstyle note: "aura with Infuser up; under anti-heal, aura in short bursts or off, fight with Pain Battery and Torment Pulse"; reviewer note: Divine Barrier (already the rich-box upgrade of Dispel) is the verified cleanse and is strongest vs Spirit Burn/Decay. Grade: CALCULATED (loop maths; Infuser cooldown, ramp, heal-amp scope and Infuser additivity are GAPs). Confidence 55% that the loop is net-negative under any 35%+ anti-heal; 45% on the playstyle note being the right answer (vs simply accepting). Wrong if: lifesteal on aura ticks is amplified or the self-damage is reduced by Victor's own spirit resist/Scourge (then the break-even moves up); Infuser's active is on a very short cooldown.
Test (supported, extends T1/T2 of S1): arms Infuser-active / Infuser-idle / Spirit Lifesteal / Leech (Leech arm: `give upgrade_damage_recycler` alone; at the 16.8k slot it is price-equal to Infuser, A2.6), each `cast 3 8` with `enemies 3` at aura range, lowhp 70; metric net HP = healDiffObserved - self-damage rows; ABBA x5 after an A/A floor. Anti-heal arms need P-CC0 (gun file 3b) to pass; otherwise UNSUPPORTED.

### A2.5 VC2 to VC5
- VC2 reach. PREVENT: engage only with Warp Stone and Jumpstart available and the hex carrier's 29 s cooldown spent; Aura T1 slow (point 2) holds them once inside. RECOVER: Divine Barrier/Dispel vs hex/slows (Dispel scope [GAP]); Jumpstart speed after a hex (whether Jumpstart's speed is "movement-based" [U]). SURVIVE: Pain Battery at 28 m, Torment Pulse. Verdict: leave. Grade UNTESTABLE-HIGH-RISK (positioning). Confidence 50%. Wrong if: ranged comps make him useless in most fights (would argue for a reach item; Warp Stone is already core).
- VC3 revive: same analysis as the gun file GC3; spirit points: 100% HP from point 14, stun from 16. Verdict: leave + note. Grade UNTESTABLE-HIGH-RISK. Confidence 50%.
- VC4 channel break. PREVENT: Jumpstart T3 50% debuff resist arrives only at point 15 (late) and only for 4.5 s; Scourge self-cast before diving (+20% debuff resist, existing debuffs reduced). RECOVER: Debuff Reducer (Counters) upgrades to Unstoppable (data); Unstoppable is not in this build's menu and cannot be used while stunned. SURVIVE: recast the aura (2 s cd; ramp restarts). Verdict: leave; note "Scourge on yourself before the dive". Grade UNTESTABLE-HIGH-RISK. Confidence 45%. Wrong if: stuns do not break the channel [U].
- VC5 Pain Battery gating: unchanged (S5, test T5). Grade: none until T5 runs.

### A2.6 Correction: Leech consumes Spirit Lifesteal (verified)
items_full.json and gamedata.js: Leech = [Bullet Lifesteal, Spirit Lifesteal]; Infuser = [Spirit Lifesteal]. In this build Infuser (16.8k) consumes the only Spirit Lifesteal. Leech as an extra item later would get no credit at all: 6.4k fresh plus a slot. Leech as a swap for Infuser at the same point is credited Spirit Lifesteal: 6.4k - 1.6k = 4.8k, exactly Infuser's price, so that comparison is price-fair. The first pass (S4) said Leech "needs BL + a second Spirit Lifesteal"; that is only true if Infuser is kept. Grade: CALCULATED (deterministic). Confidence 90%.

## 0. Prior results: inconclusive, why
- The only measured Victor data (results/victor_lifesteal_gun_only) is gun-only fire, so it says nothing about this build: Infuser/Spirit Lifesteal read 0 because no ability damage was dealt, which is the exact opposite of how this build plays (aura + Torment Pulse + Pain Battery).
- Same instrument problems as the gun file: n=1, no A/A, no anti-heal, no incoming damage, no self-damage netting, one range.
- plans/victor.md and scenarios/victor_sustain_three.json (Spirit Lifesteal vs Leech) were never run with valid results; Leech is not in this build, and Infuser would consume Spirit Lifesteal, so that swap needs a second Spirit Lifesteal and is not a like-for-like substitute.
Verdict: no usable evidence. All items below are decided from kit maths unless a runnable test is listed.

## 1. Build as read (order of purchase)
Early: Extra Regen, Extra Spirit, Improved Spirit, Torment Pulse (lane: Grit). Mid: Healing Booster, Spirit Lifesteal, Sprint Boots, Enduring Speed, Mystic Vulnerability, Mystic Expansion (imbue 3 = Aura), Infuser, Compress Cooldown (imbue 2 = Jumpstart), Escalating Exposure, Greater Expansion, Warp Stone, Superior Cooldown. Late: Scourge, Boundless Spirit, Juggernaut, Spirit Burn, Witchmail. Ability order 3312341312214424 (Aura first).
Scaling in play: Aura 13..58 dps (+0.15..0.72x spirit), Pain Battery 100 + 1.6x per bolt target, Jumpstart regen 100 (+70) + 1.2x, Torment Pulse 25 + 0.23x to the closest two, Scourge 2.3% max HP/s in 10 m, revive 200 + 2.0x.

## 2. Weakness table
| id | weakness | cat | sev | evidence | solved by kit? |
|---|---|---|---|---|---|
| S1 | Aura self-damage (70% of dealt) is the core loop's cost. At ~240 dps dealt (58 + 0.72 x 250 spirit) self = ~170 hps, more than any regen here. Infuser active (70% hero lifesteal, 7 s) is the only item that cancels it, and it is one 7 s window per cooldown (cooldown not in item stats; read in game). | survival | H | kit maths | partly (Infuser active, Healing Booster, Juggernaut regen 8) |
| S2 | Aura ramp-up: dps climbs from min to max over the channel; ramp time is not in the stats. Recast restarts the ramp (cd 2 s). Average dps over a short fight is far below the listed max. | output | H | hero_victor.txt | no |
| S3 | Reach: aura 8 m (+Expansion 20/30%), kiters and gun carries stay out; Warp Stone is the only engage. Enemy slow on aura is 20% (T1), dash slow. | reach | M-H | kit | partly (Expansion x2, Warp Stone, Sprint, Enduring Speed, Jumpstart +3 m/s) |
| S4 | Anti-heal on Victor: Infuser, Healing Booster, Jumpstart regen, Pain Battery T3 all shrink. Build has no Leech-type counter and Infuser/Leech cannot share one Spirit Lifesteal. Spirit Burn (own) applies -70% to enemies but not to him. | survival | M | items | partly: Divine Barrier (rich box) cleanse, Healbane in Counters |
| S5 | Pain Battery availability: needs stored damage = 40% max HP. High HP (health spike) means more damage needed per charge; it is not available at will. Unknown whether Aura/Jumpstart self-damage count. | output | M | kit | unknown |
| S6 | Burst / CC / low HP: Scourge self-cast +40% spirit resist and debuff resist, Juggernaut 50% slow resist, Warp Stone 30% bullet resist 6 s, revive 240 s; no stun answer in core; bullet armor only in Counters (Plated, Metal Skin). | survival/CC | M | kit | partly |
| S7 | Farming/lane: name says farming; Aura at T1 is 13 dps min (+0.15x) with a self-damage cost, so early waves are slow; Grit in losing-lane box. NPC damage multiplier for aura unknown. | economy | M | kit | no |
| S8 | Ult cooldown allocation: Compress Cooldown imbue is on Jumpstart (changed from ult in Round 25). Revive 240 s: Superior/Transcendent CDR still shortens it. | output | L | data.js changes | yes (Superior) |

## 3. Remedies, price, test, verdict
### S1 aura self-damage
Remedy classes: item - Infuser (owned), Healing Booster (owned, +20% cast and regen heal), Juggernaut (regen), Spirit Lifesteal (13%), Mystic Reverb (T4 lifesteal 8/22, delayed), Healing Tempo (slot locked), Leech (not compatible); ability use - cast Aura only with Infuser active (7 s fits the 8 s aura), stop aura at low HP, use Jumpstart first (regen 170 + 1.2x over 4.5 s), pick targets in clumps (aura hits many but self-damage is 70% of dealt, so more enemies = more self damage and more lifesteal: with Infuser 70% lifesteal on each hero hit, net self-damage ~0 per enemy); positioning - stay in aura with teammates healing; accept.
Utility->damage: Infuser's heal only equals aura self-damage if lifesteal counts the aura ticks at 70% for heroes and ticks of a channelled DoT are not halved; and only for 7 s of the 8 s aura. If it works, the 8 s aura at full ramp is a free ~1500 damage nuke; if DoT ticks heal at a reduced rate, the net is ~-100 hps. This is the highest decision value test in the build.
Tests (existing ops; fresh pawn per block; lowhp so heals are not capped; compare self-damage rows in damage csv with healDiffObserved):
- T1 A/A noise floor: aura-only block x6 (below, Infuser absent).
```
setup Frank Haze
hardreset
give upgrade_improved_spirit
give upgrade_soaring_spirit
give upgrade_health_stealing_magic
fetch 120
lowhp 70
healreset
cast 3 8
healsum
```
- T2 arm B: replace Spirit Lifesteal with `give upgrade_infuser` and `cast i1 0.3` (activate; item index depends on give order - verify with `abilist`) immediately before `cast 3 8`. Arm C: Infuser owned but not activated. Metric: net HP change over 8 s = healDiffObserved - sum(self rows). Pass: B net > C net + 2x floor. ABBA x5.
- Ramp (S2) comes out of the same block: per-tick damage vs timestamp, no extra run.
Decision rule: if B net >= 0 keep the loop and make "Aura with Infuser" the playstyle note; if B net still < -100 hps, propose swapping nothing but moving Infuser earlier is useless - treat Aura as short-burst (3-4 s) and keep Juggernaut. Provisional verdict: keep, confidence 50%.
**Grade (H)**: CALCULATED (see A2.4 loop model; T1/T2 would make the Infuser part MEASURED, sandbox not live game). Confidence 55% (loop maths) / 45% (note).

### S2 ramp-up
Remedy classes: item - Compress Cooldown is on Jumpstart not Aura (cooldown 2 s, no help); Greater/Mystic Expansion (range only); ability use - one long channel (8 s) vs short re-casts (ramp resets); hold it only while in range; engage with Warp Stone and cast aura immediately.
Test T3 (no extra setup beyond T1): `cast 3 8` once vs `cast 3 4` x2 (wait 2 s between) measuring total damage dealt in 10 s; also with 3 enemies (`enemies 3 4`). Metric: damage dealt per self-damage. Decision: playstyle note only. Verdict undecided, expect "hold the aura through" as note. Confidence 45%.
**Grade (H)**: none yet (T3); ramp time is a GAP.

### S3 reach
Remedies: Warp Stone (owned, replaced by Ethereal Shift in rich), Majestic Leap (3.2k, barrier 200 + 12x boons, 45 s), Phantom Strike (T4), Greater Expansion (owned, +30% radius -> 8 m becomes ~12 m with both), Enduring Speed/Sprint (owned), Jumpstart speed, Aura slow T1 (20%), Pain Battery slow T1 (32% 2 s), target choice.
Tests:
- T4 aura radius: `fetch d` d = 150, 250, 350, 450, 600, 800 (units, ~39 u/m is a guess; calibrate with `pos`), `cast 3 2` each; first d with zero aura damage = radius. Arms: base, +Mystic Expansion imbued on 3 (`imbue upgrade_magic_reach Signature3` is in src/Scenario.cs only, undocumented: smoke-test; if it fails mark UNSUPPORTED), +Greater Expansion (passive: `give upgrade_tech_range`).
- Chasing a fleeing target: UNSUPPORTED (bots static; no flee). Kit maths: +3 m/s Jumpstart for 4.5 s decaying (~+6 m) plus Warp Stone 11 m teleport covers one 8-12 m gap per fight.
Decision: leave alone (no cheap fix beats owned items). Confidence 60%.
**Grade (H)**: UNTESTABLE-HIGH-RISK for the chase (positioning, enemy movement); the radius part of T4 would be MEASURED. Confidence 50% (capped, was 60%).

### S4 anti-heal
Remedy classes: Leech (needs BL + a second Spirit Lifesteal; Infuser consumes the first), Divine Barrier (rich box, cleanse non-stun debuffs, 600 barrier), Dispel Magic (250 heal on use; Counters), Healbane (Counters), Debuff Reducer (shorter debuffs), kill/avoid the carrier, Spirit Burn (deny their healing first).
Test: UNSUPPORTED (no `eheal`; bot cannot shoot). Decision from maths: leave; this build already lists Dispel and Divine Barrier as the cleanse path. Confidence 50%. Would change with: a measured anti-heal share of Victor's total healing > 30%.
**Grade (H)**: CALCULATED (anti-heal UNSUPPORTED in the Sandbox, GAPS 8). Confidence 50%. Correction (A2.6): Leech as a swap for Infuser costs the same 4.8k at 16.8k; it only needs a second Spirit Lifesteal if Infuser is kept. A2.4 shows Leech cannot sustain the aura loop, so it is not the answer to S4 either.

### S5 Pain Battery gating
Remedy classes: self-fed charge (Aura self-damage, Jumpstart), absorb with Scourge/Torment, Witchmail/Spellbreaker (not charge), accept; item: none directly (Tankbuster removed in Round 14 because only the battery clears 165).
Tests: same as gun T5: `cast 3 8`, `cast 2 0.4`, `cast 1 0.5` on a fresh pawn; bolts in damage csv = full. Control: `cast 1 0.5` first. With `hurtme` vs `incoming` to test which damage source charges it (GAPS #6). Metric: bolt damage per hero = 100 + 1.6x spirit (known-answer). Decision: playstyle (do Aura -> Jumpstart -> battery) if self-fed works; else treat Pain Battery as a defensive-reactive nuke, note unchanged. Verdict cannot determine. Confidence 55% no change.
**Grade (H)**: none yet (cannot determine until T5).

### S6 burst / CC / revive
Same as gun G6: CC UNSUPPORTED, revive UNSUPPORTED except the `incoming gun 600` (no lowhp) probe. Kit maths: Scourge self-cast = 40% spirit resist + 20% debuff resist + aura; Warp Stone 30% bullet resist 6 s; Juggernaut slow resist; Witchmail 22% spirit resist, cooldown reduction on hits >= 75; Plated/Metal Skin only in Counters. Gun-heavy teams are the gap. Decision: leave, Counters menu covers. Confidence 55%.
**Grade (H)**: UNTESTABLE-HIGH-RISK. Confidence 50% (capped, was 55%).

### S7 farming
Remedies: Cultist (not listed, rule: strong on weak farmers, ~8 min), Torment Pulse early (owned), Aura early point (order starts with 3), Trophy Collector (no), lane Grit, Extra Regen.
Test: UNSUPPORTED (no creeps; bot-only). Possible partial: aura damage per second vs a bot at 100% accuracy times a guessed NPC multiplier is not a measurement; skip. Decision: keep; revisit if Council adds an NPC wave op.
**Grade (H)**: CALCULATED (no NPC measurement, GAPS 21). Confidence 40%.

### S8 ult cooldown
Remedy: move Compress imbue to ult. Price: ult CD 240 s -> 197 s (18%); Jumpstart 22 s -> 18 s (and Mercurial charge irrelevant here). Revive is a once-per-fight tool, so the cooldown matters only if second deaths happen in the same 4 min window. Jumpstart regen gives 170 + 1.2x spirit; 4 s less CD = +~1 heal per 25 s fight = ~+500 HP/min. Slight edge to Jumpstart for sustained fights; ult edge only if 2 lethal events <240 s apart. Test: UNSUPPORTED (lethal). Leave (Round 25 reasoning stands). Confidence 45%.
**Grade (H)**: CALCULATED (cooldown arithmetic; value of a second revive depends on fight timing). Confidence 45%.

## 4. Regression
No change proposed, so none. If S1/T2 shows Infuser fails to offset the aura, the likely response is a playstyle note (short aura bursts), not an item swap; if swap were chosen, re-check spirit 4.8k spike (Infuser 16.8k is the gate in the current order), slot count and Healing Tempo (slot locked).

## 5. Summary table (re-ranked by chain frequency x lethality; graded per section H)
| rank | weakness / chain | chosen | cost | tests | verdict | grade | conf. | what would make it wrong | new weaknesses |
|---|---|---|---|---|---|---|---|---|---|
| 1 | VC1 + S1 + S4 aura loop vs anti-heal | keep Infuser core; playstyle note (aura with Infuser up, short bursts under anti-heal); Divine Barrier the verified cleanse; Leech rejected (cannot sustain the loop) | 0 | T1/T2 + Leech arm runnable; anti-heal arms need P-CC0 | KEEP + note | CALCULATED | 55% (maths), 45% (note) | heal amp on lifesteal / self-damage reduced by own resist; short Infuser cd | none |
| 2 | VC2 + S3 reach | leave | 0 | T4 radius runnable; chase UNSUPPORTED | LEAVE | UNTESTABLE-HIGH-RISK | 50% | ranged comps dominate | none |
| 3 | VC3 revive | leave + note | 0 | `incoming gun 600` probe | LEAVE | UNTESTABLE-HIGH-RISK | 50% | silence/stun blocks revive | none |
| 4 | VC4 channel break | note: Scourge self-cast before the dive | 0 | UNSUPPORTED | LEAVE + note | UNTESTABLE-HIGH-RISK | 45% | stuns do not break the channel | none |
| 5 | S2 ramp | playstyle (hold the aura) after T3 | 0 | T3 runnable | UNDECIDED | none yet | n/a | n/a | none |
| 6 | S5 / VC5 battery gating | playstyle after T5 | 0 | T5 runnable | CANNOT DETERMINE | none yet | n/a | n/a | none |
| 7 | S6 burst/CC | leave, Counters | 0 | UNSUPPORTED, one probe | LEAVE | UNTESTABLE-HIGH-RISK | 50% | n/a | none |
| 8 | S7 farming | keep | 0 | UNSUPPORTED | KEEP | CALCULATED (no farm data) | 40% | measured farm deficit | none |
| 9 | S8 ult CDR | leave (Compress on Jumpstart) | 0 | UNSUPPORTED | LEAVE | CALCULATED | 45% | repeated lethal events within 240 s | none |
| 10 | Leech/Spirit Lifesteal cost | record corrected (A2.6) | 0 | none | KEEP | CALCULATED | 90% | shop credits differently | none |
No verdict here is MEASURED; nothing may be presented as real-game performance.

## 6. Re-sweep (revision 2)
No core change. The playstyle notes add no item, slot or dependency. If a later measured result ever supported Leech for Infuser (same 4.8k at 16.8k): new weaknesses = loses the only window where the aura loop is net-positive, -18 spirit (Infuser 6 + 30 vs Leech 12 [U whether Infuser's +30 is active-only]) which lowers aura, Pain Battery and Jumpstart scaling, and -10% spirit resist; gains +80 HP and anti-heal mitigation; spikes unchanged (both health colour, same price). Not proposed. No second B-F loop needed.


## I. Practicality (WEAKNESS_PROCESS section I; added 2026-10-24, appended, nothing above changed)
Sources added: game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` and `heroes.vdata` (cooldowns, upgrades, level table); data.js walk (prac/out/walk_victor.txt, regenerated, 0 flags). Level table: unlocks at 0 / 500 / 1.4k / 3.2k souls, 1 point at every other level to 48.6k (32 points; tier costs 1/2/5 [U, consistent]). Time: ~7k at 8:00, ~1k/min after (late times are upper bounds).
Kit numbers not in hero_victor.txt: Aura T2 = +6 min / +34 max DPS; Pain Battery T2 +50 damage; Jumpstart T2 also -8 s; Reanimation T3 -95 s (240 -> 145 s).

### I.1 Gun economy
No gun items. The gun (24 rounds, 12 per bullet, 2.4 s reload) is filler. Reanimation T1 (+15% fire rate and spirit damage per bullet while the revive is on cooldown, 17.4k) is a gun stat on a spirit build: a wasted point, but required for T2 (revive at 100% HP, 20.6k). Accept. CALCULATED, 80%.

### I.2 Ability points vs item timing
Order 3312341312214424: Aura T1 0.2k, T2 2.0k, T3 6.8k; Pain Battery 0.5k, T1 3.2k, T2 8.4k, T3 (heal) 16.1k; Jumpstart 1.4k, T1 9.2k, T2 11.0k, T3 32.1k; Reanimation 3.2k, T1 17.4k, T2 20.6k, T3 48.6k.
Checks: Mystic Expansion on Aura (12.0k) after Aura T3 (6.8k); Compress on Jumpstart (18.4k) after Jumpstart T2 (11.0k); Torment Pulse (5.6k) needs nothing. Consistent. Revive stays 240 s (192 s if Superior Cooldown at 30.4k applies to the ult [U]) until 48.6k; matches S8. Leave. CALCULATED, 60%.

### I.3 Farming ("Aura Farming")
Aura self-damage = 70% of damage dealt + 15/s (A2.1), while Spirit Lifesteal/Infuser heal only 3% from NPCs. Using the VC1 loop model with h = 0.03: net HP/s = 0.036 D - 0.70 D - 15 = -0.66 D - 15. If the 70% counts damage dealt to every target, an aura on a 4-trooper wave costs about 4x the HP of the same aura on one hero, and lifesteal returns almost nothing. Farming tempo is then HP-limited (Extra Regen/Healing Booster, Jumpstart regen), not damage-limited. Torment Pulse (5.6k, closest two) and the gun farm without that cost.
Decision: playstyle note candidate "farm with Torment Pulse and the gun; aura only on big camps or heroes", pending PR-V2. Grade: CALCULATED with [U] on the self-damage formula; NPC farming itself UNSUPPORTED (no NPC op). Confidence 45%. Wrong if self-damage is per-cast (SelfDPS only) rather than per damage dealt, or excludes non-hero damage.

### I.4 Spike timing vs survivability (incl. the countered case)
Spirit 4.8k at 5.6k, health 4.8k at 9.6k, 9.6k at 16.8k (Infuser), 12.8k at 28.8k (Warp Stone): the Victor rule (health right after the first damage spike) is met. Alternative B (Healing Booster, Spirit Lifesteal, Enduring Speed before Torment Pulse) moves health to ~4.8k and the spirit spike to 9.6k: a slower aura and no Torment Pulse in lane for a hero whose health already comes 4k after. Countered case: anti-heal, silence on Jumpstart or Cursed Relic (no Infuser active) do not stop the aura's self-damage, so this build can lose HP to itself; the answer is behaviour (stop the aura, VC1), not earlier health. Decision: keep. Grade: CALCULATED (spike maths) + UNTESTABLE-HIGH-RISK (fight value). 50%.

### I.5 Buttons and new-player load
3 abilities (Aura channel, Jumpstart, Pain Battery when charged) + 3 core item actives: Infuser (16.8k, must be timed with the aura, VC1), Warp Stone (28.8k), Scourge (36.8k, self-cast). Full engage by 36.8k: Warp Stone -> Scourge on self -> Infuser -> Aura -> Jumpstart -> Pain Battery = 6 inputs: the heaviest of the five pilot builds, and the sustain depends on getting the Infuser/Aura pairing right. Options: playstyle line with that order (free); accept. Decision: note. UNTESTABLE-HIGH-RISK, 40%.

### I.6 Slot lock, core length, sell chain
9 slots at 28.8k; core ends at 59.2k: Juggernaut (46.4k), Spirit Burn (52.8k) and Witchmail (59.2k) arrive at ~47-60 min at 1k/min, so in most games they behave like rich-box items and the build's late defence (Juggernaut slow resist, Witchmail spirit resist) is often never bought. Not a rule breach (core cost has no target); reviewer note. Sell conflict: Counters and Ethereal Shift both sell Warp Stone. CALCULATED, 65%.

### I.7 Forgiveness when behind
The damage is an ability, so a delayed item costs less than on an item carry; the weak point is Infuser (16.8k), the only item that makes the aura loop positive (VC1): behind = longer stretch of uncovered self-damage. Medium. No change. 50%.

### I.8 Tests (existing ops only)
PR-V2 aura self-damage vs target count (gates I.3), RUNNABLE:
```
setup Frank Haze
hardreset
fetch 120
ekeep 1
ehp 50000
enemies 1
mark pv2_1
cast 3 8
mark none
wait 3
hardreset
fetch 120
ekeep 1
ehp 50000
enemies 3 200
mark pv2_3
cast 3 8
mark none
```
A/A (1 vs 1) n=5 first, then ABBA n=5. Metric: sum of damage rows with victim = player and ability = aura, vs damage dealt to enemies. Self-damage about 3x with 3 targets = per-damage-dealt (I.3 holds); about equal = per cast. Ring placement is unconfirmed (AUTORUN), so check all 3 bots took aura damage. Heroes stand in for NPCs; NPC farming UNSUPPORTED.

### I.9 Regression (F)
Only notes proposed; no item, spike or slot change; no new weaknesses.

| problem | chosen | grade | conf. |
|---|---|---|---|
| Aura farming costs HP (if per damage dealt) | note pending PR-V2 | CALCULATED [U] | 45% |
| 6-input engage, Infuser timing | playstyle note | UNTESTABLE-HIGH-RISK | 40% |
| Core ends 59.2k; late defence rarely bought | reviewer note | CALCULATED | 65% |
| Warp Stone named by two sells | reviewer note | CALCULATED | 65% |
| Ability order, gun, health timing | leave | CALCULATED | 50-80% |


## J. Item roles (WEAKNESS_PROCESS J; added 2026-10-24, appended, nothing above changed)
Sources: audit/items_full.json [i]; game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` [g] and `gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt` [l]; audit/hero_victor.txt [k]; walk prac/out/walk_victor.txt. Grades: C = CALCULATED, U = UNTESTABLE-HIGH-RISK, M = MEASURED (none).

### J.0 Game-file facts that fill earlier [GAP]s
- Infuser cooldown 30 s [g]: the 7 s active is up 23% of the time (S1 "cooldown not in item stats" closed).
- Greater Expansion has no imbue filter and its text says "abilities and items" [g/l]: a global +30% range and radius. Mystic Expansion (the imbued +20% on Aura) is consumed by it at 25.6k [i], so Aura gets +20% from 12.0k and +30% from 25.6k, never +50%.
- Superior Cooldown is global [g]: the revive becomes 240 -> 192 s from 30.4k (A2.1/I.2's [U] becomes C).
- Torment Pulse fires every 1.4 s [g]. Warp Stone cooldown 16 s; range tagged ETechRange [g].
- Dispel Magic [l]: purges all non-ultimate negative effects, then heals and gives speed if it removed anything; not usable while stunned or slept; 45 s [g] (A2.4 RECOVER (c) [GAP] closed).
- Juggernaut [l]: enemies that shoot you get their fire rate slowed (40% for 4 s).
- Healing Tempo [l]: every heal he applies (not innate regen or passive lifesteal) gives +35% fire rate and +1.25 m/s for 7 s.

### J.1 Item roles
| item (box, souls) | every effect [source] | what it feeds | matters from | grade |
|---|---|---|---|---|
| Extra Regen (0.8k, becomes Healing Booster) | +2.5 regen, OOC 1.5 [i] | lane sustain under aura self-damage | at once | C |
| Extra Spirit > Improved Spirit (2.4k, becomes Boundless) | +18 spirit, +75 HP, +1 m/s sprint, OOC 1.5 [i] | Aura max DPS +13 per target (0.72x), Pain Battery +29 per bolt-target, Jumpstart regen +22, Torment Pulse +4 per pulse; HP; sprint (reach) | at once | C |
| Torment Pulse (5.6k) | every 1.4 s: 25+0.23x to the closest two within 9 m (11.7 m with Greater Expansion); +100 HP, 18% melee resist [i/g] | lane and camp farm without the aura's self-damage (I.3 note); keeps Mystic Vulnerability, Escalating Exposure stacks, Spirit Burn's 500-in-5 s and spirit lifesteal running when the aura is off (VC1 "short bursts"); vs melee divers; Refresher's sell | at once | C |
| Healing Booster (6.4k) | +20% cast and regen healing, +3 regen [i] | Jumpstart regen, Pain Battery T3 heal (16.1k), Dispel heal; lifesteal and Infuser [U: lifesteal is tagged EHealingOutput, Booster supplies heal amp cast/regen; the VC1 x1.2 stays U]; becomes Healing Tempo (slot locked) | at once | C/U |
| Spirit Lifesteal (8.0k, becomes Infuser) | 13% spirit LS (3% vs NPCs), +6 spirit, +90 HP [i] | aura, Torment Pulse, Pain Battery sustain | at once | C |
| Sprint Boots > Enduring Speed (9.6k, becomes Juggernaut) | +2 m/s, 25% slow resist, OOC 2 [i] | reach into aura range (VC2), leaving | at once | C |
| Mystic Vulnerability (11.2k, becomes Escalating Exposure) | spirit damage: -8% spirit resist on the target 7 s; +8% spirit resist self [i] | aura, Pulse, Battery, Scourge damage; survival vs spirit | at once | C |
| Mystic Expansion (12.0k, Aura imbue, becomes Greater Expansion) | +20% range and radius on Aura only [i/g] | Aura 8 -> 9.6 m (10.8 m at T3) | at once (Aura T3 6.8k) | C |
| Infuser (16.8k) | always: 13% spirit LS (3% NPC), +6 spirit, +100 HP, 10% spirit resist; active 7 s, 30 s cd: 70% spirit LS on heroes and +30 spirit [i/g] | the aura loop's only positive window (VC1), now known to be 23% of the time; a damage window too: +30 spirit = aura max DPS +22 per target, Pain Battery +48 per bolt-target, Pulse +7, Jumpstart regen +36; spirit resist vs spirit heroes | at once | C |
| Compress Cooldown (18.4k, Jumpstart imbue) | -18% Jumpstart cooldown [i] | more regen, speed, T3 debuff resist (32.1k) windows | at once | C |
| Escalating Exposure (23.2k) | spirit hits stack +4.5% spirit amp (12 stacks, 0.7 s proc cd, 12 s), 17% spirit resist, -8% spirit armor [i/g] | aura ticks (4/s) stack it to 12 in ~8.4 s on every target in range; Pulse/Battery; spirit survival | at once | C |
| Greater Expansion (25.6k) | global +30% range and radius of abilities and items, +10% spirit resist [i/g/l] | Aura 8 -> 10.4 m (11.7 m at T3); Pain Battery 28 -> 36.4 m; Torment Pulse 9 -> 11.7 m; Scourge aura 10 -> 13 m and cast range 35 -> 45.5 m; Warp Stone 11 -> 14.3 m [U that a blink's range scales]; spirit resist | at once | C, U (Warp Stone) |
| Warp Stone (28.8k) | 11 m blink, +30% bullet resist 6 s, 16 s [i/g] | engage into aura range, escape, anti-gun window; sold by Counters and Ethereal Shift | at once | C |
| Superior Cooldown (30.4k) | global 20% ability cooldown, OOC 4 [i/g] | Jumpstart 18% -> 20% only; revive 240 -> 192 s; Pain Battery, Aura recast | at once | C |
| Scourge (36.8k) | self or ally (35 m): +40% spirit resist, +20% debuff resist, existing debuffs reduced, aura 2.3% of enemy max HP/s in 10 m for 10 s, +100 HP; 35 s [i/g] | damage that scales with enemy HP (tanks); VC1/VC4 answer (debuffs reduced, CC shorter); a team role: cast on a diving ally | at once | C |
| Boundless Spirit (41.6k) | +30 spirit, +15% spirit power, +75 HP, OOC 4 [i] | every spirit scaler | at once | C |
| Juggernaut (46.4k) | +2.5 m/s, 50% slow resist, 25% melee resist, +8 regen; attackers' fire rate -40% 4 s [i/l] | reach (VC2), sustain, and the build's main anti-gun item besides Warp Stone's 6 s (S6) | at once | C |
| Spirit Burn (52.8k) | 500 spirit damage to one enemy in 5 s: explosion + burn 24+0.06x DPS 8 s and -70% healing; once per 20 s per enemy [i] | aura at full ramp reaches it; offence vs enemy healers | at once | C |
| Witchmail (59.2k) | +14 spirit, 22% spirit resist, 7% CDR; each enemy spirit hit >= 75 takes 4 s off a random ability [i/l] | spirit survival, ability uptime under focus | at once | C |
| Counters: Spirit Resilience / Metal Skin / Plated Armor | as in the Wraith file (30% spirit resist; 5 s bullet immunity 24 s; 30% deflect) [i/g] | vs spirit / one gun carry / gun teams; Metal Skin's -1.5 m/s slows walking in | at once | C |
| Counters: Dispel Magic | purge non-ultimate negatives (hexes, slows, anti-heal); heal 250 x 1.2 and +2 m/s 3 s if anything was removed; 10% spirit resist; 45 s [l/g] | VC2 RECOVER (the menu line), VC1 RECOVER (anti-heal) | at once | C, U (timing) |
| Counters: Healbane | his spirit damage applies -35% healing 8 s on enemies; 275 heal on kill; +7 spirit [i] | vs enemy healers; the aura applies it to everyone in range | at once | C |
| Counters: Debuff Reducer | 25% debuff resist, +90 HP; component of Unstoppable/Spellbreaker [i] | VC4 channel-break CC duration, slows | at once | C |
| Counters: Counterspell | parry 0.8 s; on success 150 heal, +1.75 m/s, +20 spirit 6 s; 23 s [i/g] | telegraphed ults | at once | U |
| Rich: Ethereal Shift (sells Warp Stone) | 4 s invulnerable then +20 spirit, +3 m/s, 30% spirit resist 5 s; 37 s [i/g] | survival, escape | at once | C |
| Rich: Refresher (sells Torment Pulse) | resets abilities and charges incl. the revive; 300 s; +14% spirit, +15% bullet resist [i/g] | second revive (VC3) | at once | C |
| Rich: Divine Barrier (sells Dispel) | non-stun cleanse, 600 barrier, +2.75 m/s, ally-castable, 45 s [i] | VC1/VC2 RECOVER, team peel | at once | C |
| Slot locked: Transcendent Cooldown / Healing Tempo | 25% ability and item cooldown (Infuser 30 -> 22.5 s: active uptime 23% -> 31%) / +25% heal amp, +6 regen, +10% spirit resist, +1.25 m/s 7 s on each heal (Jumpstart, Pain Battery T3, Dispel) [i/l] | Infuser window, revive; reach | when a slot frees | C |
| Losing lane: Grit | 200 barrier 4 s, 60 s [i] | lane trades | at once | C |

### J.2 Earlier verdicts re-opened with all roles counted
| earlier verdict (section) | role it was judged on | roles added | restated verdict | changed? | grade, conf. |
|---|---|---|---|---|---|
| S1 / VC1 keep Infuser; aura with Infuser up | the loop heal (cooldown unknown) | 30 s cooldown [g] = 23% uptime; +30 spirit during the active (damage window for aura, Battery, Pulse); 10% spirit resist and 100 HP always | Keep Infuser (unchanged). The loop is net-positive at most ~23% of the time, which supports the note "aura with Infuser up, short bursts otherwise"; the active is also the build's burst window, so pair it with Pain Battery when charged | no (stronger) | C, 55% |
| S3 / VC2 reach: leave; "8 m becomes ~12 m with both" expansions | Greater Expansion as Aura radius | Mystic Expansion is consumed: Aura +30% from 25.6k (10.4 m, 11.7 m at T3), not +50%; Greater Expansion also lengthens Pain Battery (36.4 m), Torment Pulse (11.7 m), Scourge (13 m aura, 45.5 m cast), Warp Stone (14.3 m [U]) | Leave (unchanged); the aura number is corrected down, the reach answer is wider than stated (one item covers four tools) | number corrected | C, 50% |
| S8 Compress on Jumpstart, not the ult | imbue choice for the whole game | Superior Cooldown (30.4k) is global, so the choice only matters 18.4k-30.4k (~12 min); afterwards Jumpstart and revive both have 20% | Leave (unchanged); stakes smaller than stated | no | C, 50% |
| S6 burst/CC/gun teams: leave, Counters | Juggernaut as slow resist and regen | Juggernaut also slows attackers' fire rate 40% for 4 s [l] | Juggernaut (46.4k) is the core's main anti-gun item, which is why the "gun-heavy teams" gap is open until then; the Counters Metal Skin/Plated lines stay the earlier answer. Unchanged | no | C, 50% |
| VC1 RECOVER / summary row 1: "Divine Barrier the verified cleanse"; Dispel scope [GAP] | cleanse | Dispel verified by game text (non-ultimate negatives, incl. anti-heal; heal 250 x 1.2 when it removes something; usable while silenced) | Dispel (3.2k, already in Counters) is the first anti-heal and hex answer; Divine Barrier is the rich upgrade path (ally cover, 600 barrier). Reviewer note changes accordingly | yes | C, 60% |
| Rich: Refresher sells Torment Pulse | Torment Pulse as a minor late item | Pulse is the no-self-damage farm tool, keeps MV/EE/Spirit Burn running with the aura off, 100 HP, 18% melee resist | Cannot determine a better sell: the other final slots are upgraded or named (Healing Booster is the only alternative, and it amplifies Infuser/Jumpstart heals [U]). Keep the line; reviewer note that it costs the aura-off playstyle | no (note) | C, 40% |
| I.3 farming note "farm with Torment Pulse and the gun" | Pulse as farm | confirmed 1.4 s interval and two targets | Note stands | no | C, 45% |

### J.3 Tests that separate the roles (AUTORUN.md ops; `setup Frank Haze`; A/A n=5-6, ABBA; effect > 2 x A/A SD)
- J-VS1 Infuser's damage window vs heal: S1 T2 arms B (active) and C (idle); score enemy damage rows (aura) per second over the 7 s separately from net HP. Expected +0.72 x 30 = +22 DPS per target at max ramp. RUNNABLE.
- J-VS2 Infuser cooldown: `give upgrade_infuser`, `cast i1 0.3`, `mods`, `wait 7.5`, `mods`, `wait 22`, `cast i1 0.3`, `mods` (reappears = 30 s). RUNNABLE (names).
- J-VS3 Greater Expansion global reach: (a) Torment Pulse: `give upgrade_tech_damage_pulse` with vs without `upgrade_tech_range`, `enemies 3 R` with R = 10.5 m x k (P0 calibration), `wait 6`; ring victims with pulse rows only in the Greater Expansion arm. (b) Pain Battery 28 vs 36 m: `fetch 32 m x k`, charged battery via `incoming gun 300` until full, `cast 1 0.5`. (c) Warp Stone: `pos`, `cast i1 0.3`, `pos` (`pos` is in src/Scenario.cs, not in AUTORUN.md: smoke-test). RUNNABLE ((c) if `pos` works).
- J-VS4 Torment Pulse as the aura-off spirit source: `give upgrade_tech_damage_pulse`, `give upgrade_escalating_exposure`, no casts, `enemies 2 200`, 10 s: pulse rows every 1.4 s and an Exposure stack modifier on both bots (`mods`). RUNNABLE.
- Juggernaut's fire-rate slow, Dispel purge, Superior Cooldown on the revive: UNSUPPORTED (bots never shoot; no `ecc`; no lethal op).

### J.4 Regression (F)
No item or order change; one reviewer note changes (Dispel first). No new weakness.

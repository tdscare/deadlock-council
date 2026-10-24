# Victor gun ("It's Alive And Armed", data.js id victor_gun) - weakness -> remedy
Written 2026-10-24 by weakness-solver. Sources: data.js build, audit/items_full.json, audit/hero_victor.txt, GAPS.md, playstyle/victor.md, RULES_KIERAN.md, results/victor_lifesteal_gun_only. No game or data.js changes.
Revision 2 (2026-10-24, updated WEAKNESS_PROCESS A2 + H): added section A2 (identity map, verified counters, ranked chains GC1-GC5, PREVENT/RECOVER/SURVIVE, counter-the-counter), the verified Leech/Spirit Lifesteal correction (A2.6, which withdraws the G2 spike claim), probe P-CC0, evidence grades on every verdict and a re-ranked summary. First-pass analysis and tests kept below.

## A2. Hero identity map and dependency chains (revision 2, 2026-10-24, per WEAKNESS_PROCESS A2/H)
Added on top of the first pass; sections 0-5 are kept and graded. Tags: [kit]/[item] = audit/hero_victor.txt / audit/items_full.json; [GAP] = not in the data; [U] = game knowledge to verify. Build walked from data.js (wk2/walk_victor_gun.txt): gun 4.8k at 5.6k, health 4.8k at 9.6k, spirit 4.8k at 20.8k, core 51.2k / 12 slots. Ability points (order 2213241231443143): Jumpstart 1/2/5/8 (T3 = 2 charges + 50% debuff resist at point 8), Pain Battery 3/7/10/14 (T3 heal at 14), Aura 4/9/13/16, Reanimation 6/11/12/15 (T1 gun buff 11, T2 revive at 100% HP at 12, T3 stun at 15). Frequency proxy: share of the Council's 81 builds (44 heroes) that buy the counter in core; not a public pick rate.

### A2.1 Identity map
| strength [source] | compensates | depends on |
|---|---|---|
| Lifesteal + heal stack: Bullet LS 13 (9.6k) -> Leech 28/28 (38.4k), Overflow 13 (+10 charged) spirit LS (27.2k), Frenzy 10 + Fervor below 50% HP (51.2k), Healing Booster +20% (6.4k) -> Healing Tempo +25% (44.8k) [item] | A close-range brawler with no blink, no barrier and a self-damaging kit | Hitting heroes; healing not reduced; enemy bullets not deflected away from him (he heals by trading) |
| Jumpstart hub: 15% current HP self-damage, then 100 +70 (T2) +1.2x spirit regen over 4.5 s, +3 m/s (+3 T1), 30 -8 s cd, Compress -18% (imbued), 2 charges 8 s apart (T3), 50% debuff resist (T3) [kit]; imbues Quicksilver -> Mercurial (reload on use, +22% fire rate 12 s, bonus magic bullets until reload, +20% clip), Spellslinger stack per ability or item cast [item] | Reload/ammo, fire rate, sustain, chase speed and CC duration all hang on one button | Not silenced/stunned; HP to pay 15%; heal not reduced (regen is cut by HealAmpRegen penalties) |
| Shocking Reanimation: lethal hit -> wave (120% slow, diminishing, 18 m) -> 3 s channel -> back at 50% HP (100% from T2, point 12), 200 + 2.0x damage (+175 and 1.5 s stun at T3); 240 s; T1 +15% fire rate and spirit damage per bullet while on cooldown [kit] | No escape and full commitment: he can fight to the death once per 240 s | Cooldown up; whether silence/stun/curse at the lethal moment blocks it is [GAP] |
| Damage-taken conversion: Berserker +7 weapon power per 120 damage taken in 10 s (+8% bullet resist), Pain Battery charge (40% max HP stored), Frenzy below 50% HP [item/kit] | Low base damage; makes being focused pay | Living through the damage; whether self-damage counts [GAP, T4/T5] |
| Reach: Sprint Boots/Enduring Speed +2 m/s, 25% slow resist; Jumpstart +6 m/s decaying; Pain Battery 28 m with 32% slow 2 s (T1, point 7) [item/kit] | No gap closer | Slows, kiting ranges, Jumpstart off cooldown |

### A2.2 Enemy counters (verified in the data)
- Anti-heal (cuts every heal source above; self-damage is not reduced, so the kit's costs stay): Toxic Bullets -35, Inhibitor -40 (also -30% of HIS outgoing damage), Crippling Headshot -35, Healbane -35, Decay -50, Spirit Burn -70 (500 spirit damage in 5 s, 8 s, once per 20 s per enemy), Haunting Shot -40, Nullification Burst "prevents healing effects"; kit: Venator grenade -30 [item/hero]. Core 47/81 builds (36/44 heroes): P(>=1 of 6 enemies) > 99%. Leech "reduces the effect of enemy applied healing reduction" by an unstated amount [GAP].
- Bullet denial (stops damage AND lifesteal at once): Metal Skin 5 s bullet immunity (Counters in 75/81 builds), Plated Armor 30% deflect + 50% of on-hit effects prevented (Counters 64/81), Ethereal Shift 4 s invulnerable, Return Fire reflects 65% bullet damage, fire-rate slows Hunter's Aura -15% (x2 vs a lone hero; core 10/81), Rusted Barrel -32%, Suppressor -28% [item]. Disarm: Phantom Strike, Cursed Relic (Disarming Hex 0/81).
- Silence on the hub: Silencer 2.5 s build-up (core 9/81, 14 heroes any), Focus Lens 4.5 s, Cursed Relic 3.25 s (also interrupts, prevents item use, removes non-ultimate buffs: would strip Mercurial/Spellslinger/Jumpstart buffs [U]), Silence Wave 3 s; kits Grey Talon, Violet [item/hero]. Item or kit stun/sleep: Knockdown, Crushing Fists, Lightning Scroll, Arctic Blast freeze; Haze, Infernus, Seven, Venator, Paige, Solomon, Abrams etc.
- Revive counters: none in item data target it directly. The kit counter is behavioural: leave his 18 m wave radius before the lethal hit or during the 3 s channel, then re-engage on a 50% HP Victor (before point 12) or bait the 240 s cooldown (192 s with Superior Cooldown's global 20% at 40.0k [U whether Superior applies to the ult]). Cursed Relic "removes all non-ultimate buffs": the revive is an ultimate, so not stripped.
- Slows on the chaser: Slowing Hex (also silences movement items/abilities; whether Jumpstart's speed buff counts as "movement-based" is [U]), Capacitor, Vortex Web, Point Blank, Cold Front, Arctic Blast, Mystic Slow, Phantom Strike: core 27/81.

### A2.3 Chains ranked by frequency x lethality
| rank | chain | freq | lethality |
|---|---|---|---|
| GC1 | Lifesteal/regen covers "brawler with no escape who hurts himself"; anti-heal (and bullet denial: Metal Skin) cuts it; he is left trading 15%-HP Jumpstarts and taking focus with heals cut | H (>99% lobbies own anti-heal; Metal Skin is the most common counter buy) | H: Jumpstart becomes a net HP loss; Berserker/Frenzy push him into lower HP on purpose |
| GC2 | Jumpstart is the hub (reload, +22% fire rate, Spellslinger, regen, speed, 50% debuff resist); silence/stun/Cursed Relic switch it off, and a silenced Jumpstart cannot provide its own debuff resist | M-H | M: gun still fires; loses reload refresh, regen and chase |
| GC3 | Revive covers no-escape; enemies wait out the 3 s channel or re-kill at 50% HP; second death within 240 s is final | M (long fights) | H, but only after a death the build accepted |
| GC4 | Damage-taken conversion covers low base damage; burst, Inhibitor (-30% of his output) and anti-heal make the HP he spends unrecoverable | M | M (depends on GAP: does self-damage feed it) |
| GC5 | Speed-only reach; slows/kiting keep him out of his close-range trade | M | L-M (he still shoots) |

### A2.4 GC1 in three layers
PREVENT: (a) target the anti-heal carrier first (Toxic/Inhibitor/Crippling need their bullets on him; Healbane/Spirit Burn/Decay need their spirit damage); Inhibitor holders also cut his output by 30% while it builds. (b) Plated Armor (Counters): 50% of bullet on-hit effects prevented, which should slow Toxic/Inhibitor/Crippling build-up [U whether build-ups count as on-hit]; does nothing vs spirit anti-heal. (c) Timing: Jumpstart's 15%-of-current cost is largest in HP when healthy but least risky then; cast it before the anti-heal lands, not into it.
RECOVER: (a) Divine Barrier (rich box; verified text "Remove all non-stun debuffs", 600 barrier, 45 s): removes the anti-heal debuff; vs Spirit Burn the per-enemy 20 s lockout means one cleanse gives clean healing until that enemy can burn again; vs bullet build-ups it reapplies within seconds. (b) Dispel Magic (Counters, 3.2k): no description in data; cleanse scope [GAP]. (c) Leech (core): mitigation amount [GAP].
SURVIVE: (a) Metal Skin (Counters): bullet immunity 5 s, -1.5 m/s self-slow (verified), no spirit cover. (b) Revive. (c) Frenzy's 40% debuff resist below 50% HP may shorten anti-heal debuffs [U whether heal reduction is a status effect]. (d) Stop Jumpstarting under heavy anti-heal: the regen is cut but the 15% HP cost is not.
Counter-the-counter: bullet build-ups reapply after Divine Barrier; two anti-heal sources [U stacking]; Nullification Burst prevents healing outright; Cursed Relic prevents item use (no Divine Barrier/Metal Skin for 3.25 s); Metal Skin is answered by spirit damage.
Utility -> survival conversion (CALCULATED): Jumpstart under anti-heal a: net HP = -0.15 x HP_now + (170 + 1.2 x spirit) x 1.2 (Healing Booster) x (1 - a). At 3,000 HP and 60 spirit: -450 + 290 x (1 - a): a=0 -> -160; a=0.35 -> -261; a=0.70 -> -363. So Jumpstart is already a net HP loss without anti-heal at that HP (it is a speed/reload/debuff-resist button, not a heal), and anti-heal makes it worse by ~100-200 HP per cast. Assumptions: HP and spirit values [U]; Healing Booster applies to Jumpstart regen (its text says regen +20%); Healing Tempo not counted.
Verdict GC1: keep Leech core (the only anti-heal mitigation in the build). Add nothing to core. Reviewer notes (no data.js edit here): (1) the verified cleanse is Divine Barrier; Dispel Magic's Counters line names Knockdown, a stun after a 2 s delay: neither Divine Barrier (non-stun only) nor an unverified Dispel is shown to stop it, unless the pending-stun marker is removable during the delay [U]; (2) playstyle: under anti-heal, Jumpstart for speed/reload/resist only. Grade: CALCULATED for the Jumpstart maths and price facts; the "keep" verdict also depends on enemy behaviour, so overall UNTESTABLE-HIGH-RISK. Confidence 50%. Wrong if: Leech's mitigation is large enough to make Infuser/VB irrelevant (strengthens keep) or negligible (then VB's +10% bullet resist and burst could matter more: test P2-style once anti-heal is testable).

### A2.5 GC2 to GC5
- GC2 Jumpstart hub vs silence/stun. PREVENT: cast Jumpstart before engaging so the T3 50% debuff resist (from point 8) is up when the CC lands, and keep the second charge for after; Spellslinger also stacks on item casts, so actives keep it up during a silence. RECOVER: Divine Barrier/Unstoppable for silence (Unstoppable is reachable via the Counters' Debuff Reducer; data says it cannot be used while stunned). SURVIVE: Titanic Magazine (+100% clip) keeps the gun firing without Mercurial reloads; Mercurial bullets persist until reload. Counter-the-counter: Cursed Relic strips buffs and blocks items; silence before the first Jumpstart. Verdict: playstyle note "Jumpstart first, then fight; keep a charge". Grade UNTESTABLE-HIGH-RISK (CC timing). Confidence 45%. Wrong if debuff resist from Jumpstart does not apply to silence/stun durations [U].
- GC3 revive. PREVENT the wait-out: the revive wave slows 120% (diminishing) in 18 m, and T3 adds a 1.5 s stun (point 15), so enemies inside 18 m cannot simply walk away; the counter is to step out before the lethal hit. RECOVER: Refresher (rich box) resets it. SURVIVE: 100% HP revive from point 12. Verdict: leave; playstyle note "after reviving, use the slow/stun window to finish or leave; assume no second revive for 240 s". Grade UNTESTABLE-HIGH-RISK. Confidence 50%. Wrong if silence/stun at the lethal moment blocks the revive [GAP]; test: the `incoming gun 600` no-lowhp probe in G6 (does the revive fire at all in the Sandbox).
- GC4 conversion. Decided by T4/T5 (does self-damage feed Berserker/Pain Battery). Grade: none until run (then MEASURED, sandbox not live game). If self-damage does not feed them, the chain's cost is real enemy damage only; no item change either way.
- GC5 reach. Leave (Sprint/Enduring/Jumpstart speed; Juggernaut slot-locked). Grade CALCULATED. Confidence 60%.

### A2.6 Correction: Leech consumes Spirit Lifesteal (verified; replaces the G2 reasoning below where they differ)
items_full.json and gamedata.js: Leech = [Bullet Lifesteal, Spirit Lifesteal]; Spiritual Overflow = [Spirit Lifesteal]; Infuser = [Spirit Lifesteal]; Vampiric Burst = [Bullet Lifesteal]. In this order Spirit Lifesteal (22.4k) is consumed by Overflow (27.2k), so Leech at 38.4k is credited Bullet Lifesteal only: 6.4k - 1.6k = 4.8k (it pays for a second Spirit Lifesteal inside its price; with Spirit Lifesteal still owned it would be 3.2k). Totals: Overflow + Leech = 9.6k on top of BL + SL in either order; Leech-first only moves 1.6k earlier and delays Overflow's damage. Fair price comparison at the 38.4k slot: Leech 4.8k, Vampiric Burst 4.8k (BL credited), Infuser 6.4k (no Spirit Lifesteal left to credit): an Infuser arm is 1.6k dearer, not equal. The walk tool (audit/walk2.js) already credits only owned components, so the spike table (gun 5.6k, health 9.6k, spirit 20.8k) is correct; the first-pass claim "spike table mis-stated ~1.6k" (G2) is withdrawn. Grade: CALCULATED (deterministic shop maths). Confidence 90%.

## 0. Why the prior Victor result is inconclusive (results/victor_lifesteal_gun_only, Oct 23; swap run Oct 24)
1. n=1 block per item, forward order only, no A/A: noise floor unknown. dmg/s ranged 113-155 on a fixed 8 s with hit counts 27-36, so a 15% spread is already inside plausible noise; first-block warm-up bias was noted but not counterbalanced.
2. Target had no anti-heal (GAPS #8). Leech's only unique text is "reduces enemy healing reduction"; it was scored with nothing to reduce.
3. Gun-only fire: Infuser/Spirit Lifesteal read 0 by construction. Victor's heals are mostly kit (Pain Battery T3, Jumpstart regen, Healing Booster/Tempo, regen): the "empty slot" block still healed ~107 hps, so item effect is a small difference on a big baseline.
4. Vampiric Burst was scored with its 5 s active on for the whole 8 s window (best case). Real uptime = 5 s / its cooldown (cooldown is not in items_full stats: read it in game).
5. Heal column includes regen; no incoming damage, one enemy, one range (350u), no accuracy model, no self-damage netting (Jumpstart, Aura).
Verdict kept: INCONCLUSIVE on Leech vs VB vs Infuser. Needs: A/A floor, ABBA counterbalance, lowhp + incoming, accuracy model, uptime-weighted VB, source isolation by subtraction.

## 1. Kit facts that drive everything (read from data)
- Pain Battery: 7 bolts, 100 + 1.6x spirit per target hit once, needs stored damage = 40% max HP (charge from ANY damage taken), T1 32% slow 2 s, T3 heals 15% missing HP on hero hit.
- Jumpstart: costs 15% CURRENT HP, then 100 (+1.2x spirit) (+70 at T2) regen over 4.5 s and +3 m/s; cd 30 (-8 at T2), T3 +1 charge (8 s between charges) and 50% debuff resist.
- Aura: 13..58 dps (+0.15..0.72x spirit) ramping, 8 m, self-damage 70% of dealt, 8 s.
- Revive: lethal -> 3 s channel -> 50% HP, 240 s cd. T1 fire rate +15% and spirit damage/bullet while it is on cooldown.
- Build order here maxes Jumpstart first (2,2,1,3,2,4,...): Aura is a late 1-2 point ability. Gun build is Jumpstart/Pain Battery/ult, not aura.
- Spirit available is small: Overflow 30, Leech 12, Mercurial 7, Spirit Lifesteal 6 (consumed) = about 50-60 + 1.1/level boons.
- Item facts: Leech 28% bullet + 28% ability lifesteal, +12% weapon dmg, +180 HP; Berserker +7 weapon power/stack per 120 damage taken within 10 s, +8% bullet resist; Spellslinger +11% fire rate/stack, 6 stacks, 18 s, each ability/item cast refreshes; Mercurial: imbued ability charges 14 s, on use reloads, +22% fire rate 12 s, bullets add 20 (+0.38 x spirit) magic damage until next reload, +20% clip; Frenzy: 10% bullet lifesteal, +15% fire rate, Fervor 40% fire rate / 40% debuff resist <50% HP, 160 HP.
- Component graph: Leech = Bullet Lifesteal + Spirit Lifesteal; Spiritual Overflow = Spirit Lifesteal; Vampiric Burst = Bullet Lifesteal; Infuser = Spirit Lifesteal.

## 2. Weakness table
Severity = frequency x cost (H/M/L). "Solved by kit?" = already answered by an owned item/ability.

| id | weakness | cat | sev | evidence | solved by kit? |
|---|---|---|---|---|---|
| G1 | Sustain is the build's identity but is unmeasured and exposed to anti-heal (Healbane -35, Toxic -35, Crippling -35, Inhibitor -40, Spirit Burn -70). Every heal source here (lifesteal, Booster, Tempo, Jumpstart, Pain Battery) is reduced. | survival | H | kit/items; GAPS #8 | partly: Leech text; Divine Barrier (rich box) cleanses non-stun debuffs |
| G2 | Leech and Spiritual Overflow both consume Spirit Lifesteal. Bought in build order (Overflow mid, Leech late) Leech pays the Spirit Lifesteal component again (T2 price, ~1.6k) on top of the Bullet Lifesteal credit. Real late cost and 4.8k/6.4k spike math are off by that amount; notes say nothing. | economy | M | components in gamedata.js | no |
| G3 | Self-damage economy unknown: Jumpstart (15% current HP) is the imbue target for Quicksilver/Mercurial/Compress (3 items on ability 2) so the damage plan costs HP every ~20 s. Whether that self-damage feeds Berserker (120 dmg/stack) and Pain Battery (40% max HP) decides if these are free upside or a tax. | output/survival | H | GAPS #6, #20 | unknown |
| G4 | Spirit scaling shortage. Mercurial bullet bonus 20 + 0.38x spirit, Pain Battery 100 + 1.6x, Jumpstart regen 1.2x: with ~55-90 spirit those are weak. Each +10 spirit adds about +3.8 per bullet while Mercurial is active (body bullet ~34.8, so +11%); Improved Spirit (+18, +75 HP, +1 m sprint) is about +6.8/bullet = +19.6% vs Titanic Magazine +14% base. Hypothesis, not measured. | output | M | item data | no |
| G5 | Spellslinger stack uptime. Needs casts in-combat inside 18 s; gun build has Jumpstart (30/22 s cd, 2 charges at T3), Pain Battery (needs battery), Aura (low priority), item actives (none core). Expect ~2-3 casts per 18 s = 2-3 stacks (22-33% fire rate), not 6 (66%). | output | M | item+kit | no |
| G6 | CC / burst / low-HP phase: no stun answer in core (Counters box has Debuff Reducer, Dispel; Juggernaut slot-locked; Jumpstart T3 50% debuff resist only for 4.5 s). Revive 240 s. Frenzy <50% HP gives fire rate + 40% debuff resist. | survival/CC | M | kit | partly (Frenzy, Revive) |
| G7 | Reach: no gap closer, Aura 8 m, Pain Battery 28 m. Kiting gun heroes outrange; Sprint + Enduring Speed + Jumpstart speed are the answers. | reach | L-M | kit | partly |
| G8 | Opening Rounds bonus (>50% enemy HP) is a dead stat in the 2nd half of a fight and in the sandbox (bot HP floor 90% over-rewards it). Already sold via Counters note. | output | L | GAPS #4 | yes (sell) |

## 3. Remedies, price, test, verdict
### G1 sustain / anti-heal
Remedy classes: (a) item: Leech (owned late), Vampiric Burst, Infuser, Spirit Lifesteal/Overflow, Healbane (counters), Divine Barrier (cleanse), Dispel Magic (250 heal on use), Cheat Death; (b) ability use: Jumpstart at the start of a trade rather than at low HP (regen is flat per second, not a heal-on-use, so it is cut by anti-heal the same either way); (c) positioning/target: kill the healer-debuffer first; (d) accept.
Price: Leech ~6.4k total (4.8k if BL owned, ~+1.6k Spirit Lifesteal again, see G2), no active, 24/7. VB 6.4k, 70% bullet lifesteal + 34% fire rate + 75% reload for 5 s, uptime = 5/cd. Infuser: needs ability damage that this build barely has (Aura low prio): 13% passive of tiny numbers -> poor here, note 70% active only helps if you cast Aura.
Conversion (utility -> damage): VB's +34% fire rate is extra damage only while a target is in aim; at 70% active lifesteal and ~150 dps gun that is ~105 hps for 5 s = ~525 HP per cooldown. Leech passive: 28% x ~150 dps = 42 hps continuous, so over a 20 s fight 840 HP (VB: 525 + 13% passive x 15 s ~ 290 = 815 if cd <= 20 s). Almost equal, VB wins only if cd short AND you can fully trade for 5 s; Leech wins when trades are intermittent or anti-heal present (Leech reduces the penalty, size unknown). Gains vanish if accuracy < ~50%, target out of line of sight, or anti-heal cuts both equally.
Tests (existing ops; counterbalanced ABBA, 5 pairs, hardreset between blocks, `expect hero=Frank items=<n>` where available):
- T1 (A/A floor): identical Leech block x6. Metric dmg/s, healDiffObserved/s. Gate for everything below.
```
setup Frank Haze
hardreset
give upgrade_vampire
give upgrade_health_stealing_magic      # then the arm's item (Leech: upgrade_damage_recycler)
fetch 350
aimoff 5.5 3
accuracy 0.6 0
enemies 1
lowhp 45
incoming gun 150
healreset
cast reload 2.5
mark leech
fire 15
mark none
healsum
```
  Arms: Leech | Vampiric Burst (`cast i<k> 5` at t=0 and again when cd reads ready) | Bullet+Spirit Lifesteal only | none. Marginal = arm - none (subtract). Uptime-weighted VB by running 20 s fires with the active used once.
- T2 (anti-heal): UNSUPPORTED (no eheal op; GAPS #8). Substitute: none valid; do not infer from eitem Healbane (bot never shoots). Decide from kit maths.
- T3 (VB cooldown probe): hardreset, give upgrade_surging_power, `cast i1 5`, `wait 6`, `cast i1 1`, check if second use fires (read damage/fire-rate change); repeat with `wait` ladder. Needed to price VB.
Decision (now, from maths): keep Leech as core, no change. Confidence 55%. What would change it: T1/T3 showing VB net heal > Leech by more than 2x noise at 15-20 s fights, or a real anti-heal measurement showing Leech does not offset it.
Row-level note: if kept, the build itself should not add Infuser (confirms prior results).
**Grade (H)**: CALCULATED (lifesteal maths; VB cooldown, accuracy and anti-heal unknown). Confidence 55%. Not real-game performance. Price correction (A2.6): at the 38.4k slot Leech and VB both cost 4.8k and Infuser 6.4k, so the line "Leech ~6.4k total ... VB 6.4k" above should read: marginal 4.8k each (Leech's includes the re-bought Spirit Lifesteal); Infuser 6.4k.

### G2 Spirit Lifesteal conflict
Remedies: reorder (Leech before Overflow so Leech takes the Spirit Lifesteal and Overflow pays full 6.4k - worse), drop Spirit Lifesteal from mid cont. and let Overflow's component be a fresh purchase (same total), drop Overflow (replace with weapon/spirit item), accept. Overflow itself: +25% fire rate (stacks by shooting heroes, 5 s buildup), +30 spirit, +13% ability / +10 spirit lifesteal, 90 HP - it is a damage item here, not sustain. Price of keeping both: Overflow ~4.8k (SL credited), Leech ~4.8k (BL credited) + SL re-buy 1.6k folded into price; total late cost is simply the shop price, not a wasted slot. So the weakness is notes/spike math, not build function.
Test: UNSUPPORTED (shop math). Decision: ask Data/Spike checker to recompute spikes with Leech priced at 6.4k - BL. Add to reviewer checklist. No build change. Confidence 80% that no change is needed, 60% that spike table is currently mis-stated.
**Revision 2**: verified in items_full/gamedata (A2.6). The walk already prices Leech at 4.8k and the spikes are correct; the "spike table mis-stated" part is withdrawn. **Grade (H)**: CALCULATED (deterministic). Confidence 90% that no build or spike change is needed.

### G3 self-damage economy
Remedies: (a) playstyle: cast Jumpstart when HP is high (cost is 15% current) vs low; (b) item: drop Quicksilver/Mercurial imbue to a non-HP ability (not possible, Mercurial needs an ability to imbue; Pain Battery charge needs 40% HP, Aura costs more) ; (c) accept.
Key unknown: does self-damage count for Berserker and Pain Battery? If yes, a Jumpstart at 3.5k HP (525 dmg) = ~4 Berserker stacks (7 weapon power each) and 13% of battery. Cost of the answer: nothing (read-only test).
Tests (existing ops; run on a fresh pawn per block):
- T4 (Berserker feeds from Jumpstart?): blocks control / `cast 2 0.4` / `hurtme 500` (Hurt may bypass events: GAPS #6) / `incoming gun 200` for 3 s, each followed by `fire 3` at 100% accuracy; metric = per-hit damage by shot index (damage csv). Berserker stack = +7 weapon power per stack, so per-hit damage should step up. Items: give upgrade_berserker only.
- T5 (Pain Battery fed by self-damage?): give nothing; `cast 3 8` (Aura self-damage) then `cast 2 0.4` then `cast 1 0.5`; bolts in damage csv = battery full. Control: `cast 1 0.5` on fresh pawn (should not fire). Expect no bolts if battery needs enemy damage or amount < 40% max HP.
Verdict: cannot determine until T4/T5 run. Decision-impact: if self-damage feeds Berserker, Berserker becomes cheaper than it looks and Jumpstart-then-fire is the engage pattern (playstyle note, not item); if not, Berserker needs real enemy damage and its place after Enduring Speed stays, no change either way. Therefore low decision value for items, high for the note/playstyle. Confidence in "keep as is": 70%.
**Grade (H)**: none yet (cannot determine until T4/T5; results would be MEASURED, sandbox not live game, and `hurtme`/`incoming` may bypass the game's damage events, GAPS 6).

### G4 spirit scaling vs gun
Remedies: Improved Spirit (1.6k) or Extra Spirit (0.8k) instead of Swift Striker/Rapid Rounds; Boundless Spirit (late, 6.4k); more Mercurial uptime via Compress/Superior; Spellslinger earlier. Price: slot (gun build uses 12 core slots), delay of fire-rate spike, rule "weapon-tree items that deal spirit damage scale off spirit invest, buy right after the spirit spike" (RULES_KIERAN): Mercurial deals spirit damage, so by the rule it should come just after a spirit spike. The build has Mercurial at the 8th mid slot with 0 spirit invest beyond Quicksilver/Compress/Spirit Lifesteal (tech cost ~ 4.8k at most): spike not reached.
Tests:
- T6 (known answer for Mercurial): give upgrade_quick_silver -> upgrade_ethereal_bullets, `imbue` op exists only in src/Scenario.cs (not in AUTORUN.md): smoke-test `imbue upgrade_ethereal_bullets Signature2`; if no effect in damage csv (no 20+0.38x rows), mark UNSUPPORTED. Then `cast 2 0.4` `cast reload`? (reload reloads per item) and `fire 5`; per-hit extra magic damage vs expected 20+0.38 x spirit. Add arms: +Improved Spirit / +Titanic Magazine / +Swift Striker at same soul cost, measure damage per magazine and dps over 15 s with accuracy 0.6.
- Metric: damage per 15 s fight and time to empty clip. Noise floor from T1.
Decision from maths: treat as hypothesis; do not change core. Candidate to propose to Council: swap Swift Striker (20% fire rate, 2.4k tier-2 weapon) for Improved Spirit only if T6 confirms per-bullet spirit scaling AND the extra rows are not spirit-resisted by real targets (bots have 0 resist). Confidence 40%.
**Grade (H)**: CALCULATED (per-bullet spirit maths; imbue may be inert in the Sandbox, GAPS 1). Confidence 40%. A core swap needs a MEASURED T6 result.

### G5 Spellslinger uptime
Remedy: playstyle (cast Jumpstart/Pain Battery/Aura inside the 18 s window to refresh), or replace Spellslinger with Glass Cannon (bad: kill-scaled, small clip not an issue here but -13% HP) / Lucky Shot (rich box). Price: Spellslinger is the 8th mid-cont. item; late fix not needed if stacks reach 3+.
Test T7 (stack uptime): hardreset, give upgrade_enchanted_holsters; rotation `cast 2 0.4`, `cast 3 2`, `cast 1 0.5` (if battery), `fire 3`, repeating every 6 s for 18 s; metric hits/s per 3 s window vs control without Spellslinger. If hits/s rises by ~11% per cast, linear stacks confirmed. Then decide whether the build fires it often enough: need >= 3 casts per 18 s in the spirit-less rotation. Verdict: undecided, expected keep. Confidence 50%.
**Grade (H)**: CALCULATED (cast count per 18 s). Confidence 50%.

### G6 CC / burst / low HP / revive
Remedies: Unstoppable (T4, Debuff Reducer component), Debuff Reducer (T2), Juggernaut (+50% slow resist, 25% melee resist), Divine Barrier, Cheat Death, Ethereal Shift (rich), Warp Stone (6 s bullet resist), Majestic Leap, play: use Jumpstart T3 resist before engage, pick fights with Frenzy window.
All CC testing is UNSUPPORTED (no `ecc` op). Revive under lethal damage: UNSUPPORTED (`lowhp` clamps >=3%; no `lethal` op). Probe worth trying: `incoming gun 600` with no `lowhp` and Safety off: if the player actually dies and Reanimation fires, we get a real revive timing test for free. Cheap, one block.
Decision: leave alone; Counters box already carries the menu. Confidence 60%. New dependency check: none.
**Grade (H)**: UNTESTABLE-HIGH-RISK (CC timing, lethal events). Confidence capped at 50% (was 60%). See GC2/GC3.

### G7 Reach
Remedies: Warp Stone, Majestic Leap, Phantom Strike (6.4k), Sprint Boots/Enduring Speed (owned), Jumpstart speed, target selection, accept. Test: UNSUPPORTED (bots do not flee; `move` is player only). Maths: Jumpstart gives +3 m/s for 4.5 s decaying = about +6 m of catch-up; Enduring Speed/Sprint in build: +4 m/s total. Leave alone, 65%.
**Grade (H)**: UNTESTABLE-HIGH-RISK (positioning, enemy movement). Confidence capped at 50% (was 65%).

### G8 Opening Rounds
Already a swap in Counters ("Sell Opening Rounds"). Leave. Sandbox over-credits it (ekeep 0.9): use `ekeep 0.5` blocks for any damage comparison, or exclude.
**Grade (H)**: CALCULATED (item text: the bonus only applies above 50% enemy HP). Confidence 70%.

## 3b. New probe (revision 2; shared with the Wraith and spirit Victor files)
- P-CC0: do enemy-held on-hit items apply their debuffs through `incoming`? `setup Frank Haze`, `hardreset`, `eitem upgrade_inhibitor` (then `upgrade_toxic_bullets`, `upgrade_proc_silence`), `basemods`, `incoming gun 300`, `mark PCC0_<item>`, `wait 1`, `mods`, `wait 2`, `mods`, `incoming off`, `mark none`. Pass = the debuff modifier on the player. If Inhibitor/Toxic pass, rerun T1 with the debuff on: Leech vs Vampiric Burst vs Bullet LS under anti-heal (closes GC1's untested part; Infuser arm must be priced +1.6k, see A2.6). If Silencer passes, `cast 2 0.4` under it shows whether Jumpstart is blocked (GC2). Expected outcome: fail (`incoming` is a direct damage call, not a bullet), then GC1/GC2 stay UNSUPPORTED. Item actives can be fired by name with the undocumented `use <AbilityName>` op (src/Realism.cs), which avoids the `cast iN` slot-order guess.

## 4. Regression (after any change above)
No build change is proposed now, so no regression pass yet. If the Improved-Spirit-for-Swift-Striker swap is ever adopted: re-run spikes (weapon 4.8k at 5.6k: Swift Striker is part of that, so the swap lands the weapon spike late: new weakness = fire-rate and weapon spike delayed), slot count unchanged, sell chain unchanged.

## 5. Summary table (WEAKNESS_PROCESS G; re-ranked by chain frequency x lethality; graded per section H)
| rank | weakness / chain | chosen | cost | tests | verdict | grade | conf. | what would make it wrong | new weaknesses |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GC1 + G1 sustain vs anti-heal / bullet denial | keep Leech; Divine Barrier is the verified cleanse (reviewer: Dispel scope unverified, Knockdown line doubtful); under anti-heal use Jumpstart for speed/reload only | 0 | T1/T3 runnable; anti-heal UNSUPPORTED unless P-CC0 passes | KEEP + notes | UNTESTABLE-HIGH-RISK (maths parts CALCULATED) | 50% | Leech mitigation negligible and VB ahead under anti-heal | none |
| 2 | GC2 Jumpstart hub vs silence/stun | playstyle: Jumpstart first, keep a charge | 0 | UNSUPPORTED (P-CC0 may unlock) | NOTE | UNTESTABLE-HIGH-RISK | 45% | Jumpstart debuff resist does not shorten silence/stun | none |
| 3 | GC3 revive wait-out | playstyle: use the slow/stun window; assume one revive | 0 | `incoming gun 600` probe | LEAVE + note | UNTESTABLE-HIGH-RISK | 50% | silence/stun blocks the revive | none |
| 4 | GC4 / G3 self-damage conversion | decide after T4/T5 | 0 | T4, T5 runnable | CANNOT DETERMINE | none yet | n/a | n/a | none |
| 5 | G2 Spirit Lifesteal consumed (Leech 4.8k) | correct the record: spikes are right, claim withdrawn; Infuser arms cost +1.6k at that slot | 0 | none (shop maths) | KEEP | CALCULATED | 90% | shop credits differently | none |
| 6 | G4 spirit scaling | hypothesis only | 0 | T6 if `imbue` works | INCONCLUSIVE | CALCULATED | 40% | T6 per-bullet scaling | delayed weapon spike if swapped |
| 7 | G5 Spellslinger | keep | 0 | T7 | KEEP | CALCULATED | 50% | T7 shows < 3 stacks in rotation | none |
| 8 | G6 CC/revive | leave, Counters box | 0 | UNSUPPORTED, one probe | LEAVE | UNTESTABLE-HIGH-RISK | 50% | see GC2/GC3 | none |
| 9 | GC5 / G7 reach | leave | 0 | UNSUPPORTED | LEAVE | UNTESTABLE-HIGH-RISK (positioning) | 50% | kiting comps dominate | none |
| 10 | G8 Opening Rounds | leave (Counters sell) | 0 | use ekeep 0.5 | LEAVE | CALCULATED | 70% | n/a | none |
No verdict here is MEASURED; nothing may be presented as real-game performance.

## 6. Re-sweep (revision 2)
No core change; only notes. If the reviewer swaps the Dispel Magic line for Divine Barrier in Counters: Divine Barrier is already in the rich box as Dispel's upgrade, T4 (6.4k fresh vs 3.2k), so the cheapest answer to slows/hexes arrives later; the Counters slot sells Opening Rounds either way; no spike or slot change. Playstyle notes add no item, no slot, no new dependency. No serious new weakness, so no second B-F loop.


## I. Practicality (WEAKNESS_PROCESS section I; added 2026-10-24, appended, nothing above changed)
Sources added: game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` (citadel_weapon_frank_set2, ability cooldowns/upgrades) and `heroes.vdata` (level table, per-level growth); data.js walk (prac/out/walk_victor_gun.txt, 0 flags). Level table: unlocks at 0 / 500 / 1.4k / 3.2k souls, 1 point at every other level to 48.6k (32 points; tier costs 1/2/5 [U, consistent]). Time: ~7k at 8:00, ~1k/min after (late times are upper bounds).
Weapon: 24 rounds, 12 damage per bullet (+0.26 per level), 0.198 s per shot spinning up to 0.171 s (spin-up weapon), reload 2.4 s, projectile 8000 u/s. Kit numbers not in hero_victor.txt: Pain Battery T2 +50 damage; Jumpstart T2 also -8 s, T3 +0.9x scaling; Aura T2 +6 min / +34 max DPS; Reanimation T3 -95 s (240 -> 145 s).

### I.1 Gun economy (magazine vs fire rate)
Model: 20 s of continuous fire on a target, fight buffs on (Quicksilver/Mercurial buff, Overflow charged, Spellslinger 3 stacks with reload -30% [U how reload stacks]), Mercurial/Quicksilver refill used when the magazine empties (Jumpstart every ~18 s), fire rate and clip % additive [U]. b = one base bullet incl. level.

| souls | magazine | shots/s | s to empty | reload | % of 20 s reloading | damage (b) |
|---|---|---|---|---|---|---|
| 2.4k (Opening Rounds) | 24 | 5.8 | 4.1 | 2.4 | 36% | 81 |
| 4.0k Titanic | 48 | 5.8 | 8.2 | 2.4 | 18% | 117 |
| 5.6k + Swift Striker | 48 | 7.0 | 6.8 | 2.4 | 24% | 131 |
| 5.6k alt: Extended only + Swift | 31 | 7.0 | 4.4 | 2.4 | 31% | 111 (-15%) |
| 11.2k + Quicksilver | 48 | 7.6 | 6.3 | 2.4 | 12% | 172 |
| 20.8k Mercurial | 53 | 8.3 | 6.4 | 2.4 | 12% | 187 |
| 33.6k + Overflow, Spellslinger x3 | 53 | 11.7 | 4.5 | 1.7 | 17% | 248 |
| 51.2k full core | 53 | 12.6 | 4.2 | 1.7 | 17% | 279 |

Verdict: the magazine supports the fire rate at every checkpoint (12-24% reloading once Titanic is in); the early Titanic is right (about +15% over the Extended-only path at 5.6k). Keep. CALCULATED, 70%. Wrong if fire-rate bonuses are not additive or Spellslinger's reload bonus does not stack.
Rich box: "Lucky Shot: sell Titanic Magazine" is about neutral: magazine 53 -> 36, 28% reloading, about -3% damage over 20 s (Lucky Shot = +25% average per bullet, but -100% clip and -14% weapon damage). Selling Swift Striker instead gives about +14%. Reviewer note: Lucky Shot should name Swift Striker (Refresher also names Swift Striker, so one of the two needs another sell). CALCULATED, 55%; rich box only.

### I.2 Build-up items vs this fire rate
Spiritual Overflow charges by shooting heroes: 1.08 per shot over 5 s [GAP semantics], about 93 hits to full. Victor lands at most ~58-63 hits in 5 s at 100% accuracy (11.7-12.6 shots/s). If the build-up is a sliding 5 s window, Overflow never charges on Victor (its +25% fire rate, +30 spirit, +10% spirit lifesteal would be dead); if it accumulates while hits continue, it charges in about 8 s at 100% and about 16 s at 50% accuracy. This decides whether Overflow (27.2k) belongs here. Grade: cannot determine until PR-V1. Decision: keep pending PR-V1; if it never charges, return the slot to the Council (Leech earlier is the obvious candidate, see I.4).

### I.3 Ability points vs item timing
Order 2213241231443143: Jumpstart T1 0.2k, T2 2.0k (22 s), T3 6.8k (2 charges, 50% debuff resist); Pain Battery 0.5k, T1 3.2k, T2 9.2k, T3 20.6k; Aura 1.4k, T1 7.6k, T2 13.8k, T3 48.6k; Reanimation 3.2k, T1 10.1k, T2 11.9k (100% HP), T3 32.1k (145 s).
Checks: all three Jumpstart imbues (Quicksilver 11.2k, Compress 16.0k, Mercurial 20.8k) arrive after Jumpstart T3: consistent. Jumpstart cycle 22 s x 0.82 = 18 s with 2 charges, so Mercurial refills are limited by Jumpstart (~every 18 s), not by Mercurial's 14 s charge; each refill costs 15% current HP (A2.4 maths).
Spellslinger (33.6k: 18 s, up to 6 stacks of +11% fire rate): sources per 18 s are Jumpstart 1-2, Pain Battery 0-1, items 0 (no core actives), and Aura (2 s cooldown, T1 at 7.6k). If each Aura cast counts, 6 stacks (+66%) are reachable at the cost of Aura self-damage; if not, ~2-3 stacks. Test: G5/T7 with an Aura-recast arm (below). No order change. CALCULATED, 60%.

### I.4 Spike timing vs survivability (incl. the countered case)
Gun 4.8k at 5.6k, health 4.8k at 9.6k: the Victor rule (health right after the first damage spike) is met. After that the health spend stays at 4.8-6.4k until Leech at 38.4k (Overflow consumes Spirit Lifesteal at 27.2k): ~28 min flat. HP at 30k is about 2,000 (800 + 34 x 29 levels + Bullet Lifesteal 90 + Overflow 90).
Defence = lifesteal/regen + revive (240 s; 145 s only from 32.1k). Countered case (A2 GC1/GC2): anti-heal cuts the lifesteal layer and a silence switches off the Jumpstart hub (regen, speed, refill, debuff resist), which leaves only HP and the revive. Orderings: A current; B Leech before Spellslinger (health 9.6k at 32.0k instead of 38.4k, Spellslinger 6.4k later); C Healing Tempo before Spellslinger. Fight value UNTESTABLE-HIGH-RISK; the Counters trigger "Dying after Berserker" covers it. Decision: leave; reviewer note that health is flat 9.6k-38.4k. 40%.

### I.5 Buttons and new-player load
3 active abilities, no core item actives (Quicksilver/Mercurial, Spellslinger, Frenzy, Berserker are passive or proc). The lowest load of the five pilot builds. Keep. CALCULATED, 70%.

### I.6 Slot lock and sell chain
9 slots at 16.0k, 10 at 22.4k, 11 at 33.6k: fits a 9-slot early game. Conflicts: Counters and Ethereal Shift both sell Opening Rounds; Lucky Shot sells Titanic (I.1); Refresher sells Swift Striker. Reviewer note. CALCULATED, 70%.

### I.7 Forgiveness and farming
The gun spike is built from 0.8-1.6k steps; Berserker is 3.2k; Spellslinger and Frenzy are 6.4k with no components (late, ~6 min saves each). Forgiving. Farming: Titanic at 4.0k halves the reload share (36% -> 18%), which helps camps; no AoE farm tool; Aura farming costs HP (victor_spirit I.3). CALCULATED; farm measurement UNSUPPORTED.

### I.8 Tests (existing ops only; `setup Frank Haze`, `aimoff 5.5 3`, `fetch 350`, `ekeep 1`, `ehp 50000`, A/A n=6 first, then ABBA n=6, effect must exceed 2 x A/A SD)
- PR-0 fire/reload probe (shared with the Wraith file): `hardreset; accuracy 1 0; mark pr0; fire 12; mark none; acclog`. If shots stop at 24 and the block ends early, `fire` ends at an empty magazine; then every gun test uses cycles of [`fire 30` (ends at empty), `cast reload 2.4`] and scores damage per elapsed second (mark to end), which counts real reload time for any magazine size. RUNNABLE.
- PR-V1 Overflow charge: `hardreset; give upgrade_tech_overflow; basemods; accuracy 1 0` then 10 x [`fire 1`, `mods`], reload cycle as in PR-0; arms: base, + upgrade_titan_round + upgrade_blitz_bullets; repeat at `accuracy 0.5 0`. Metric: first second the charged-Overflow modifier appears (or never). RUNNABLE (names only).
- PR-V3 Lucky Shot sell choice: 51.2k core given as final items, arms core / core - titan_round + upgrade_critshot / core - blitz_bullets + upgrade_critshot (check "FAILED" in plugin.log for the class name); no Jumpstart casts (imbue confound identical in all arms); 4 PR-0 cycles at `accuracy 0.6 0`. Metric: damage per elapsed second. RUNNABLE.
- T7 Aura arm: as G5/T7 plus an arm that recasts `cast 3 0.3` six times inside 12 s before `fire 3`; hits/s vs the Jumpstart-only arm shows whether Aura casts stack Spellslinger. RUNNABLE.
- Ordering B vs A and the countered case: UNSUPPORTED (no `ecc`, no `eheal`, no per-ability tier op).

### I.9 Regression (F)
Only notes proposed. If Lucky Shot's note changes to "sell Swift Striker": Refresher needs another sell; no spike or core change. If PR-V1 shows Overflow never charges and the Council moves Leech earlier: Leech then credits the still-owned Spirit Lifesteal (3.2k instead of 4.8k) and Overflow pays 6.4k fresh; re-walk the spikes.

| problem | chosen | cost | grade | conf. |
|---|---|---|---|---|
| Magazine vs fire rate | keep (supports it) | 0 | CALCULATED | 70% |
| Lucky Shot sells Titanic | note: sell Swift Striker | 0 | CALCULATED | 55% |
| Overflow may never charge at this fire rate | keep pending PR-V1 | 0 | cannot determine | n/a |
| Spellslinger stack source | test Aura recasts (T7) | 0 | CALCULATED | 60% |
| Health flat 9.6k-38.4k | leave; Counters menu | 0 | UNTESTABLE-HIGH-RISK | 40% |
| Sell conflicts | reviewer note | 0 | CALCULATED | 70% |


## J. Item roles (WEAKNESS_PROCESS J; added 2026-10-24, appended, nothing above changed)
Sources: audit/items_full.json [i]; game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` [g] and `gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt` [l]; audit/hero_victor.txt [k]; walk prac/out/walk_victor_gun.txt. Grades: C = CALCULATED, U = UNTESTABLE-HIGH-RISK, M = MEASURED (none). Bonuses assumed additive [U].

### J.0 Game-file facts that fill earlier [GAP]s
- Vampiric Burst cooldown 30 s [g] (T3 probe no longer needed for the price); its active adds 75% of a magazine as rounds beyond the magazine cap [l] (40 at 53).
- Healing Tempo [l]: "Applying [Heal] to yourself or an ally grants the target +35% Fire Rate and +1.25 m/s (7 s). Does not apply on innate Regen or passive Bullet/Spirit Lifesteals." Cooldown 1 s [g]. Jumpstart's regen is an ability heal, not innate regen, so it should trigger it [U, PR-V4].
- Superior Cooldown, Superior Duration and Greater Expansion carry no imbue filter in the game file (their T1/T2 parts do: EApplyFilter_OnlyIfImbued) [g]: Superior Cooldown is a global 20%, so it reaches the revive (A2.2's [U] becomes C).
- Spiritual Overflow: +13% ability duration, +13% spirit lifesteal, +6 spirit, +90 HP are always on; only +25% fire rate, +30 spirit, +10% spirit lifesteal need the charge [g].
- Dispel Magic [l]: purges all non-ultimate negative effects; heal and speed only if something was removed; not usable while stunned or slept; 45 s [g]. Its scope (A2.4 RECOVER (b) [GAP]) is verified.
- Berserker max 10 stacks = +70 weapon power [g]. Frenzy [l]: below 50% HP its buffs also reduce existing debuffs. Juggernaut [l]: enemies that shoot you get their fire rate slowed (40% for 4 s).
- Cooldowns [g]: Metal Skin 24 s, Counterspell 23 s, Ethereal Shift 37 s, Infuser 30 s, Refresher 300 s, Frenzy 16 s.
- Correction to section 6: Divine Barrier is the upgrade of Guardian Ward [i], not of Dispel Magic; the rich line sells Dispel for it.

### J.1 Item roles
| item (box, souls) | every effect [source] | what it feeds | matters from | grade |
|---|---|---|---|---|
| High-Velocity Rounds (0.8k, becomes Opening Rounds) | +60% bullet speed, +8% weapon damage [i] | lane poke, hitting moving targets at range (8000 u/s projectile) | at once | C |
| Extra Regen (1.6k, becomes Healing Booster) | +2.5 regen, OOC 1.5 [i] | lane sustain against his own Jumpstart cost | at once | C |
| Opening Rounds (2.4k) | +25% weapon damage vs targets above 50% HP; keeps +60% bullet speed and +8%; +7 spirit [i] | lane trades (most are above 50%), fight openers; bullet speed vs kiters (GC5); spirit: Pain Battery +11 per bolt-target, Jumpstart regen +8 | at once | C |
| Extended Magazine > Titanic Magazine (4.0k) | +100% clip, +14% weapon damage [i] | reload share 36% -> 18% (I.1); Mercurial: each refill gives a full magazine of empowered bullets, so 53 instead of 36 empowered bullets per Jumpstart; Overflow build-up continuity across a fight; farm | at once | C |
| Rapid Rounds > Swift Striker (5.6k) | +20% fire rate, +0.75 m/s sprint [i] | gun damage; hits per second for Overflow's 5 s build-up (I.2), lifesteal per second; sprint (GC5) | at once | C, U (build-up) |
| Healing Booster (6.4k) | +20% cast and regen healing, +3 regen, OOC 1 [i] | Jumpstart regen, Pain Battery T3 heal (20.6k), Dispel/Counterspell heals; lifesteal [U: lifesteal is tagged EHealingOutput, Booster supplies heal amp cast/regen; not shown to be the same stat]; becomes Healing Tempo | at once | C/U |
| Sprint Boots > Enduring Speed (8.0k) | +2 m/s, 25% slow resist, OOC 2 [i] | reach (GC5), closing to his short-range trade, leaving | at once | C |
| Bullet Lifesteal (9.6k, becomes Leech) | 13% bullet lifesteal, +90 HP, +6% weapon damage [i] | sustain, damage | at once | C |
| Quicksilver Reload (11.2k, Jumpstart imbue, becomes Mercurial) | Jumpstart charges over 18 s: +44+0.16x damage, +10% fire rate 12 s, reload on use [i/l] | reload, fire rate; whether its bonus damage lands on Jumpstart's self-zap is [U] (would add self-damage, i.e. Berserker/Pain Battery feed) | at once | C, U |
| Berserker (14.4k) | +7 weapon power per 120 damage taken within 10 s, max 10 stacks (+70), +8% bullet resist [i/g] | gun damage when focused; Jumpstart/Aura self-damage may feed it [U, T4]; bullet resist | when taking damage | C, U |
| Compress Cooldown (16.0k, Jumpstart imbue) | -18% Jumpstart cooldown [i] | more Jumpstarts = more Mercurial refills, regen, speed, T3 debuff-resist windows, Spellslinger stacks, Healing Tempo procs | at once (Jumpstart T3 6.8k) | C |
| Mercurial Magnum (20.8k) | charge 14 s: +60+0.16x damage, +22% fire rate 12 s, reload, +20% clip, +7 spirit; bullets +20+0.38x magic until reload [i/l] | reload, fire rate, magic per bullet (scales with magazine and spirit) | at once if the imbue is live | C |
| Spirit Lifesteal (22.4k, becomes Overflow) | 13% spirit lifesteal, +6 spirit, +90 HP [i] | Pain Battery/Aura sustain | at once | C |
| Spiritual Overflow (27.2k) | always: +13% ability duration, +13% spirit LS, +6 spirit, +90 HP; charged: +25% fire rate, +30 spirit, +10% spirit LS 15 s [g] | always-on: Jumpstart 4.5 -> 5.1 s window (speed, regen, T3 debuff resist); charged: gun, Pain Battery (+48 per bolt-target), Mercurial magic (+11 per bullet) | always-on at once; charge [U, PR-V1] | C, U |
| Spellslinger (33.6k) | per ability/item cast: +11% fire rate and -10% reload time, 6 stacks, 18 s; 5% cooldown reduction always [i/l] | gun; reload; CDR on Jumpstart and revive; stack sources: Jumpstart, Pain Battery, Aura, and any item active (none in core; Counters/rich actives, VB if swapped) | at once | C |
| Leech (38.4k) | 28/28% lifesteal, +12% weapon damage, +12 spirit, +180 HP, anti-heal mitigation (amount GAP) [i/l] | sustain; over Bullet LS +6% weapon damage, +12 spirit (Pain Battery +19/bolt-target, Jumpstart regen +14) | at once | C |
| Superior Cooldown (40.0k) | global 20% ability cooldown, OOC regen 4 [i/g] | Jumpstart only 18% -> 20%; the real gain is the revive (240 -> 192 s; 145 -> 116 s after T3 at 32.1k) and Aura | at once | C |
| Healing Tempo (44.8k) | +25% heal amp, +6 regen, +10% spirit resist, OOC 4; every heal he applies (not innate regen or passive lifesteal): +35% fire rate and +1.25 m/s for 7 s, 1 s cooldown [i/l/g] | sustain AND a fire-rate item: Jumpstart (every ~18 s), Pain Battery T3 heal, Dispel/Counterspell heals; ~7 of every 18 s = about +14% average fire rate, concentrated in the engage window; speed for reach | at once if PR-V4 passes | C, U (trigger) |
| Frenzy (51.2k) | +15% fire rate, 10% bullet LS, +160 HP; below 50% HP for 10 s (16 s cd): +40% fire rate, +4 m/s, 40% debuff resist, existing debuffs reduced [i/l/g] | low-HP phase that Jumpstart self-damage reaches on purpose; escape speed and CC resist in that phase; revive at 50% HP before point 12 lands straight in it | at once | C |
| Counters: Spirit Resilience | 30% spirit resist (+15 below 50%), OOC 3 [i] | vs spirit | at once | C |
| Counters: Metal Skin | 5 s bullet immunity, 24 s, 12% bullet resist always; -1.5 m/s while on [i/g] | vs one gun carry; item cast = Spellslinger stack | at once | C |
| Counters: Plated Armor | 30% deflect, 50% bullet on-hit prevention, +130 HP [i] | vs gun; Toxic/Inhibitor/Crippling build-ups [U] | at once | C/U |
| Counters: Dispel Magic | purge non-ultimate negatives (hexes, slows, silence, anti-heal, a pending Knockdown [U]); then 250 heal x heal amp and +2 m/s 3 s; 10% spirit resist; 45 s [l/g] | GC1 RECOVER (anti-heal), GC2 RECOVER (silence on Jumpstart), its heal triggers Healing Tempo, item cast = Spellslinger stack | at once | C, U (timing) |
| Counters: Healbane | his spirit damage (Pain Battery, Aura) applies -35% healing 8 s; 275 heal on kill; +7 spirit [i] | vs enemy healers; kill heal triggers Healing Tempo [U] | at once | C |
| Counters: Debuff Reducer | 25% debuff resist, +90 HP; component of Unstoppable and Spellbreaker [i] | CC duration (GC2), slows (GC5) | at once | C |
| Counters: Counterspell | parry 0.8 s blocks ability/item damage+effects; on success 150 heal, +1.75 m/s, +20 spirit 6 s; 23 s [i/g] | telegraphed ults; heal triggers Healing Tempo | at once | U |
| Rich: Lucky Shot (sells Titanic) | 25% of bullets +100% weapon damage, +30% clip [i] | gun damage | at once | C |
| Rich: Ethereal Shift (sells Opening Rounds) | 4 s invulnerable, then +20 spirit, +3 m/s, 30% spirit resist 5 s; 37 s [i/g] | survival, escape; item cast = Spellslinger stack | at once | C |
| Rich: Refresher (sells Swift Striker) | resets all abilities and charges incl. the revive, 300 s; +14% spirit and +15% bullet resist always [i/g] | second revive (GC3), double Jumpstart; item cast = stack | at once | C |
| Rich: Divine Barrier (sells Dispel) | non-stun cleanse, 600 barrier, +2.75 m/s 6 s, ally-castable, 45 s [i] | GC1/GC2 RECOVER, team peel | at once | C |
| Slot locked: Juggernaut / Transcendent Cooldown | Juggernaut: +2.5 m/s, 50% slow resist, 25% melee resist, +8 regen, attackers' fire rate -40% 4 s [i/l]; Transcendent: 25% ability and item cooldown [i] | anti-gun survival, reach; revive and item cooldowns | when a slot frees | C |
| Losing lane: Grit | 200 barrier 4 s, 60 s [i] | lane trades | at once | C |

### J.2 Earlier verdicts re-opened with all roles counted
| earlier verdict (section) | role it was judged on | roles added | restated verdict | changed? | grade, conf. |
|---|---|---|---|---|---|
| G1 / GC1 keep Leech over VB and Infuser | lifesteal | VB: 30 s cooldown [g], +40 rounds beyond the magazine, +34% fire rate 5 s, +10% bullet resist, its cast is a Spellslinger stack (and may trigger Healing Tempo [U: active lifesteal is not "passive"]). Infuser: active +30 spirit 7 s, 10% spirit resist, cast = stack. Leech: +6% weapon damage and +12 spirit over Bullet LS | Victor reloads only 12-17% of a fight, so VB's ammo role is about +10% damage in one fight per 30 s, smaller than on Wraith. Keep Leech (unchanged); confidence 55% -> 50% because VB gains three roles the first pass did not price. T1 must score damage per fight and Spellslinger stacks, not only heal | confidence only | C, 50% |
| G4 Improved Spirit for Swift Striker (hypothesis) | per-bullet spirit on Mercurial vs fire rate | Swift's hits per second may be what lets Overflow charge (I.2); Improved Spirit adds +75 HP, Pain Battery +29/bolt-target, Jumpstart regen +22 | Hypothesis unchanged; T6 must also read the Overflow charge (PR-V1) because the swap could switch it off | test scope | C, 40% |
| G5 keep Spellslinger | cast count from abilities | item actives are stack sources too (Metal Skin, Dispel, Counterspell, Ethereal Shift, Refresher, VB if swapped); its 5% CDR and reload role are always on | unchanged | no | C, 50% |
| I.1 rich note: Lucky Shot should sell Swift Striker, not Titanic | damage over 20 s | Titanic also sets how many Mercurial-empowered bullets each refill gives (53 vs 36); Swift also feeds Overflow's charge and lifesteal per second | Cannot determine until PR-V1: if Overflow only charges with Swift, keep "sell Titanic"; if it charges either way or never, "sell Swift" (+14%) stands | yes (now conditional) | C, 45% (was 55%) |
| I.2 if Overflow never charges, return the slot | charged buff only | always-on +13% ability duration, +13% spirit LS, +6 spirit, +90 HP | If PR-V1 fails, compare these always-on roles (4.8k) with the replacement; Overflow is weak, not dead | decision rule | C, 55% |
| I.4 health flat 9.6k-38.4k: leave; option C (Healing Tempo before Spellslinger) | Healing Tempo as sustain | Healing Tempo's +35% fire rate and +1.25 m/s for 7 s after each Jumpstart heal (~40% uptime, engage-weighted) vs Spellslinger's 2-3 stacks (+22-33% fire rate, faster reload); Healing Tempo is 4.8k marginal and health colour (health 9.6k at ~32.0k instead of 38.4k) | Propose C to the reviewer pending PR-V4 (does Jumpstart trigger it). Not a core change on this grade | yes (leave -> proposal) | C for stats, U for fight value; 45% |
| GC3 / A2.2 revive 192 s "[U whether Superior applies to the ult]" | n/a | Superior Cooldown is global in the game file | Superior Cooldown's main role here is the revive (192 s, 116 s after T3), not Jumpstart (+2%). Verdict leave unchanged; grade of the number U -> C | grade | C, 70% |
| G3 / A2.4 Jumpstart as the imbue hub (HP tax) | HP cost vs refill | Jumpstart couples refill, fire rate, speed, regen, T3 debuff resist, Spellslinger stack, Healing Tempo proc. Alternative target for Quicksilver/Mercurial: Aura (2 s cooldown): refills on Mercurial's own 14 s charge (+29% refills vs the 18 s Jumpstart cycle) without the 15%-HP cost [U: whether a short Aura tap can be cancelled; Aura self-damage is 70% of what it deals] | Keep Jumpstart (engage button, couples the most roles). Aura-imbue is a named candidate only | no (new candidate) | U, 35% |
| A2.4 RECOVER (b) Dispel scope [GAP]; reviewer note "Knockdown line doubtful" | cleanse | Dispel verified: purges all non-ultimate negatives; heals 250 x 1.2 and +2 m/s when it does; usable while silenced | Dispel is the verified 3.2k answer to anti-heal, hexes and silence; the Knockdown line holds only if the 2 s pre-stun marker counts as a negative effect [U] | yes | C, 60% |
| G8 Opening Rounds dead in the second half | the +25% bonus only | +8% weapon damage, +60% bullet speed and +7 spirit stay on | The Counters/Ethereal sell of Opening Rounds still loses the least; unchanged | no | C, 70% |

### J.3 Tests that separate the roles (AUTORUN.md ops; `setup Frank Haze`, `aimoff 5.5 3`, `fetch 350`, `ekeep 1`, `ehp 50000`; A/A n=6, ABBA n=6, effect > 2 x A/A SD; upgrade classes only)
- PR-V4 Healing Tempo trigger (gates I.4 option C):
```
hardreset
give upgrade_healbuff
basemods
lowhp 60
accuracy 1 0
cast reload 2.4
mark pv4_js
cast 2 0.4
mods
fire 6
mods
mark none
lowhp 0
```
  Control: the same block without `cast 2`. Pass: a Healing Tempo buff modifier after Jumpstart and shorter hit spacing (`t_ms`) in the 7 s after. RUNNABLE (spin-up weapon: compare the same seconds of firing in both arms).
- PR-V1 extension: arms core-with-Swift vs core-minus-`upgrade_blitz_bullets`; first second the charged-Overflow modifier appears (gates the Lucky Shot sell). RUNNABLE.
- J-VG1 VB roles: (a) ammo: `give upgrade_surging_power`, `cast i1 0.2`, `fire 30` to empty, GunFired via acclog (expect 53 + 40 with Titanic); (b) Spellslinger stack: with `upgrade_enchanted_holsters`, `cast i1 0.2` then `mods` (stack +1); (c) heal: existing T1. RUNNABLE.
- J-VG2 Overflow always-on duration: Jumpstart speed modifier lifetime via `mods` at 4.0/4.8/5.4 s after `cast 2 0.4`, with vs without `upgrade_tech_overflow`. RUNNABLE (names, 0.6 s resolution).
- PR-V5 Quicksilver/Mercurial damage on the self-zap: self-damage row of `cast 2 0.4` with vs without `upgrade_quick_silver`; needs the imbue live (P0-type probe). RUNNABLE if imbue works.
- PR-V6 Mercurial imbued on Aura: `imbue` exists in src/Scenario.cs but not in AUTORUN.md: smoke-test first; then `cast 3 0.3` and look for the reload and magic-bullet rows. RUNNABLE only if `imbue` works.
- Superior Cooldown on the revive, Juggernaut's fire-rate slow, Dispel purge: UNSUPPORTED (no lethal op, cooldown readers broken for Victor's abilities per AUTORUN, bots never shoot, no `ecc`).

### J.4 Regression (F) for option C (Healing Tempo before Spellslinger), if adopted
Health 9.6k at ~32.0k (was 38.4k); Spellslinger 4.8k later; gun and spirit spikes unchanged; 11 slots at the same point; no new sell. New dependency: Jumpstart (silenced in GC2) also switches Healing Tempo's fire rate off, so GC2 gets slightly worse. Not serious; no second loop.

# Weakness -> remedy process (applies to every hero, every build, every problem type)

The Council does not only find weaknesses; it works out the best way to deal with each one, tests the promising answers, prices what each costs, and decides. Nobody should have to teach this per hero.

## A. Discover weaknesses (hero-analyst + sandbox-planner + data)
Derive from the kit, not from a fixed hero list. Sweep every category for the hero/playstyle:
- Reach: catching mobile/flying/escaping targets, closing distance, kiting resistance.
- Survival: burst, sustained damage, CC chains, silence/disarm, being focused, low-HP phases, no escape.
- CC and counterplay: being stunned/slowed/silenced, parried, dodged, line-of-sight, interrupted channels, ability misses (skillshots, lunges, bombs).
- Output: ammo/reload, fire rate, ramp-up time, ability downtime/cooldowns, resource/charge gaps, range limits, target-count limits, finishing kills (execute range, no burst), armour/resist scaling, healing reduction.
- Economy: farming speed, lane weakness, soul dependence, snowball dependence, slot lock.
- Team/situational: needs allies, enemy-comp counters, objective fights.
Sources: ability text and numbers, public build patterns, win-rate by situation, Reddit/community complaints, and the Sandbox (measured shortfalls). Each weakness gets: id, category, severity (how often x how costly), evidence, and "is it already solved by the kit?".

## A2. Dependency chains (strength -> compensates weakness -> enemy counters strength)
Weaknesses are not isolated stats. For every hero/build, first write the hero's identity map from the kit:
- Strengths and what each one COMPENSATES for (e.g. a teleport/dash/heal/shield/CC/range/stealth that covers low survivability, no escape, no sustain, low damage uptime).
- Dependencies: which ability/item the hero's survival, damage or role relies on, and its conditions (cooldown, cast time, line of sight, target, resource).
- Counters to each dependency: how the enemy turns it off or punishes it (silence, slow, stun, interrupt, root, disarm, dispel, knockback, sleep, parry/dodge, line-of-sight, baiting the cooldown, focus before it comes up, anti-heal, resist). List only counters that exist in the game's item/ability data; verify each.
- Chain: "X compensates for Y; counter Z disables X; therefore Y becomes exposed; how bad is that and how often does it happen?" Rank chains by frequency x lethality (how often enemies have Z, how easy it is to apply, what happens next).
For each serious chain investigate three layers, each with the remedy classes of section B:
1. PREVENT: stop the counter landing (avoid it, bait it, use a different ability first, positioning, a counter-item that blocks/cleanses ahead of time, saving the ability).
2. RECOVER: undo it once applied (dispel/cleanse, break effects, alternate escape, ally help, a second movement/escape tool).
3. SURVIVE WITHOUT RECOVERY: live through the exposed window (defences vs the damage type that follows, healing, barriers, trading position, accepting the death and minimising its cost).
Then attack the chosen answers: how can the enemy counter the counter (e.g. cleanse on cooldown, a second disable, damage type that the defence does not cover, baiting the defensive item first, silence that the item does not stop)? Keep the answer only if it still holds, and say what it does not cover.
Frequency check: decide whether the chain is common or dangerous enough to justify souls/slots (core), a situational/enemy-comp trigger, a playstyle rule, or nothing. Items named here are examples only; the Council derives and verifies the real candidates from the data.
 (theorycrafter, with item-analyst and researcher)
For each weakness above a severity bar, enumerate EVERY plausible remedy class, then pick candidates by data:
1. Item, core or situational (full item list scanned tier by tier, incl. utility, movement, defensive, anti-CC, sustain items).
2. Ability use: point order, rotation, which ability to use when, imbue target.
3. Positioning / engage-disengage pattern.
4. Target selection (switch to a target the kit can actually reach/kill).
5. Team coordination / pairing (Duo Builder ties in here).
6. Accept it: the weakness is not worth the souls/slot.
Do not stop at the first idea; ask "what would a top player do about this?" and check public builds for hints, but derive from the kit.

## C. Price each remedy
- Cost: souls, slot, spike impact (4.8k/colour rules), delay to damage/health spike, opportunity cost vs the item it replaces, playstyle burden (extra button/skill), new dependency.
- Benefit: how much of the weakness it removes, in which situations, measured in the Sandbox where measurable, else from kit maths.
- Utility -> damage conversion: a utility effect (stun/slow/range/duration/CC reduction/mobility) only counts as damage or kill gain if timing and enemy counterplay allow the follow-up. Model it explicitly: duration extended X s -> how many extra shots/ability casts fit given cooldowns, cast times, travel time, whether the enemy can break/dodge/cleanse, and whether the CC stacks diminish. State the assumptions and the conditions under which the gain disappears.

## D. Test where possible, otherwise reason
Design the A/B with the standard in PILOT.md (fair comparison, same state, counterbalanced, noise floor, kit confounds). Test the 1-3 most promising remedies against "do nothing" on the realistic scenario that exhibits the weakness (e.g. target that flees, stun/parry events, low ammo, low HP). If the sandbox cannot represent the situation (CC, allies, real counterplay), say UNSUPPORTED and decide from kit maths, flagged as untested.

## E. Decide
Allowed outcomes, each with evidence and confidence: change the core build; add a situational option (with the trigger stated concretely, per build rules); change ability order/playstyle note; pair with a partner (duo); leave it alone (weakness not worth fixing). "Leave it alone" and "cannot determine" are valid.

## F. Regression: did the fix create a new weakness?
After any proposed change, re-run the weakness sweep on the NEW build: spikes (4.8k per colour), slot count, survival/damage at checkpoints vs the old build, new dependencies, sell chain, interactions with other items, items now redundant. Compare old vs new on the same price-point scenarios. A fix that trades a bigger weakness for a smaller one is fine only if the trade is explicit. Record new weaknesses; loop B-F once more if one is serious.

## G. Record
Per build: council/sandbox/weaknesses/<hero>_<build>.md, starting with the hero identity map and ranked dependency chains (A2), then a table: weakness | evidence | remedies considered | chosen | cost | tests run (or UNSUPPORTED) | verdict | new weaknesses found. This feeds the reviewer (must challenge each chosen remedy and each "leave alone") and the self-review in REVIEW_LOG.md.

Example shape (not a hero-specific rule): "Abrams cannot catch mobile enemies" -> candidates: Phantom Strike, Warp Stone, Sprint/movement items, using Shoulder Charge differently, waiting for CC from team, picking different targets, ignoring because Siphon/regen make chasing unnecessary -> price each -> test the chase scenario with a fleeing bot -> decide.

## H. Evidence grades (Kieran, 04:39): theory is not proof
Every verdict carries one grade and says so in plain words:
- MEASURED: valid Sandbox result, above the A/A noise floor, kit confounds ruled out. Still labelled "sandbox, not live game" for anything involving real aim, movement, enemy reactions.
- CALCULATED: kit/item maths only. Never presented as real-game performance. Must state the assumptions and what real play could change.
- UNTESTABLE-HIGH-RISK: kit maths on things that depend on animations, positioning, hitboxes, travel time, enemy reactions/counterplay, CC timing, or complex item interactions (procs, stacking, imbue chains, ordering). These can only be "plausible"; confidence is capped (<=50%) and the verdict must be "keep current / situational note" unless a measured test supports a change. Do not change a core build on this grade alone.
Report format: grade + confidence + "what would make this wrong". Reviewer must reject any verdict whose language is stronger than its grade.

## I. Whole-build practicality (Kieran, 04:49) - the build as a system, not item damage
For every build, derive from the kit, economy and (where measurable) sandbox combat data; no fixed rules applied blindly:
- Gun economy: does magazine size support the fire rate (seconds to empty, reload time, ammo-limited uptime, damage per magazine, reload items vs mag items vs fire-rate items)? How much time is lost reloading in a fight and does it matter for this hero's burst windows?
- Farming: how efficiently does the hero farm (camps/troopers per minute with and without ability use, safe vs contested), does the build speed it or ignore it, and how does soul income feed the spikes (gap between "souls available" and "build online")?
- Spike timing vs survivability: is delaying health/greens to hit damage or investment spikes earlier worth it FOR THIS HERO? Decide from the kit (built-in sustain/escapes/range), playstyle, economy (soul income vs spike thresholds) and combat performance, and include the case where the escape/defence is countered (see A2): a hero who only survives while an escape is up should not delay health. Some heroes farm aggressively and delay greens, others need health early; compare candidate orderings (spike times, survival at checkpoints, damage uptime) rather than assuming.
- Practicality: buttons/actives to manage per fight (items with actives, ability rotation load, imbue targets), ability-point order vs item timing (charges, thresholds, tiers actually unlocked at the buy point), slot lock and sell chain, how forgiving the build is when behind or when a core item is delayed, items that only work in situations the player cannot create, and cognitive burden for a new player.
- Output: a "Practicality" section in each weaknesses file: problems found, candidate solutions (re-order, swap, ability points, playstyle, accept), cost, evidence grade (H), and decision. Fold any chosen change through F (new weaknesses).

## J. Items serve several purposes (Kieran, 05:19)
Never reduce an item to the one role it is usually bought for (e.g. Ricochet = "farming item"). For every item in a build, on every hero, the Council derives the item's FULL contribution from its data and the hero's kit, then values the whole:
- Enumerate every effect: base stats (damage, fire rate, health, resist, regen, speed, ammo, range), procs, actives, ramps, multi-target/bounce behaviour, side effects on abilities (fire rate boosting a channelled ult, charges, cooldowns, imbue targets, thresholds it helps other items reach), and component/upgrade value (what it builds into, what it replaces).
- For each effect ask which of the hero's abilities, playstyle phases (lane, farming, skirmish, teamfight, escape, objective) and other items it feeds, and when in the purchase order it starts to matter (does it do something at the moment it is bought?).
- Value = sum over all roles, in the situations that actually occur, not the primary role alone. Record primary role AND secondary benefits per item in the weaknesses file ("item roles" table) with evidence and grade (H).
- Applies in both directions: do not keep an item only because of an unused secondary effect, and do not cut or swap one on single-role grounds (e.g. a swap evaluated only on farming speed). Comparisons between an item and its substitute must cover every role of both. Any earlier verdict that judged an item on one role is re-opened.
- Test design: when an item has several roles, the experiment measures each role separately (e.g. farming rate, sustained dps with and without the multi-target bounces, ult fire-rate uptime) and the decision weighs them by how often each occurs.

## K. Kit-first build thesis (Kieran, 05:19): one strong mechanic can reshape the whole build
Before and while optimising items, the Council asks what the hero's KIT already provides and what that makes unnecessary or more valuable, then optimises the entire progression around the best idea. Not item-by-item comparison, not copying popular builds, not random combinations.
1. Find engine mechanics: kit effects that are unusually strong or that scale with something buyable (e.g. built-in lifesteal that scales with bullet damage, charge-based abilities that scale with recharge/charge items, cleanses/heals on short cooldowns, ramps, resource refunds, on-hit procs, ability uptime, farming tools).
2. Derive consequences for every build dimension: which stats make the engine worth more (and how much, from numbers); damage focus (gun/spirit/ability/melee); farming strategy and timing; survivability timing (what the kit already covers, so green items can wait or are unnecessary - and what happens when the engine is countered, section A2); purchase order and spikes; which investments become redundant (e.g. extra healing items if the engine already heals) or more attractive; implied playstyle.
3. State it as a falsifiable BUILD THESIS: "engine X + stat Y => focus Z, order W, skip V", with the numbers that would make it wrong.
4. Generate rival theses from other mechanics (including unpopular or unusual playstyles) and the conventional/popular approach; the thesis must beat them on the whole progression, not on one item.
5. Build the coherent item set and order for each surviving thesis, then CHALLENGE every item in it (section J roles, section I practicality, A2 counters): is it still the best use of those souls given the thesis? Test substitutes and combinations (e.g. which lifesteal/healing items overlap or conflict; whether a fire-rate item's secondary benefits beat a sustain item; whether a whole item group is now redundant).
6. Verify the whole progression works end to end: soul-timed walk, checkpoint states (levels/ability points/boons), survival and damage at each price point, early-game viability, what is delayed and what that costs, and behaviour when the engine is countered. Mark each link MEASURED/CALCULATED/UNTESTABLE per section H.
7. Decide: adopt a thesis as the main build, a second playstyle build, a situational pivot, or reject; record the reasoning chain so a reviewer can attack any link. A user-supplied build is a hypothesis, never a proven optimum: it gets the same challenge.
This is how every hero is approached, including odd playstyles; examples in these notes (Haze lifesteal + gun + Ricochet farming) are illustrations, not templates.

## L. Item synergies and the marginal value of each purchase (Kieran, 05:25)
Strong combinations are not automatically worth buying early or at all. The Council finds combinations itself and then prices every step of completing them.
1. Discover combinations (2, 3 or more items) from item data and the kit, including unconventional ones whose parts are rarely bought: effects that trigger or amplify each other (procs, on-hit, imbues, shared/consumed components, thresholds, stat-scaling, cooldown/charge interactions, timing windows, ult interactions), plus what the combination ENABLES (new damage source, uptime, survivability, reach, farming speed, a playstyle). Enumerate by scanning the full item list against owned items and the hero's abilities, not only popular pairings. Record each as: parts, mechanism, what it enables, conditions, current-patch numbers (recomputed from game data; example numbers in prompts are not trusted).
2. Price completion step by step. For each step in the path to the combination ask: (a) standalone value of each part before the combination is complete (some are weak alone), (b) the marginal gain of THIS purchase given what is already owned (e.g. an upgrade over its component may add little), (c) what else the same souls buy now (cheaper item giving most of the benefit, a different spike, another colour investment, farming/survival), (d) when the souls are realistically available (soul-timed walk), and the risk of being behind while waiting, (e) how the value changes later (is completing it now better than later?), (f) opportunity cost against spikes (4.8k per colour, 6.4k etc.) and slot lock.
3. Combination effects on the rest of the build: does it make another item redundant (overlapping sustain, fire rate, CC, reach), raise the value of other items, or allow a different purchase order or playstyle? Re-evaluate those items (section J) and the order (section I) with the combination present, and without it.
4. Compare candidate paths as whole builds: path A (rush combination), path B (partial: cheaper part first or alternative item), path C (complete later), path D (skip), by damage/survival/farming at each checkpoint (10k..full) and by when the combination first pays for itself. Choose the best complete build and order, not the strongest synergy.
5. Verdict per synergy: core now / core later / situational / skip, with H grade; sandbox tests compare paths at the same soul total and kit state (A/B/A, equal stacks, noise floor) where measurable, else CALCULATED/UNTESTABLE with confidence caps.
Examples are illustrations only and must be recomputed from current data: whether a recovery-over-time item upgrade is worth its extra souls over its component when sustain is already adequate, or whether a fire-rate item gives comparable power sooner; whether to rush an ult-enabling pair at the cost of farming, survivability or an earlier spike.

## M. Ability timeline x item timing (Kieran, 05:26): ability points and items are optimised together
What an ability can do changes with souls -> level -> ability points. Item value depends on that moment, so item order and ability-point order are one decision.
1. Build the timeline per build from game data (not memory): soul total -> hero level -> unlocks and ability points available (verify the unlock thresholds and point costs per tier against game files / in-game; do not assume) -> each ability's tier, charges, cooldown, damage/scaling, range, duration, imbue slots at each purchase moment. Reuse prac/ap.py (generalise it to read a build's ability order and item walk from data.js); no new system.
2. For every ability-related item (charges: Extra Charge/Rapid Recharge; cooldown: Recharging Rush, Compress/Superior Cooldown; duration, range, imbues, ability-triggered procs, thresholds), compute its value at the moment it is bought under the current point order: does it do anything now, how much, and how much more after the next relevant upgrade. Compare buying earlier vs later vs a cheaper stand-in. Sometimes an item is much stronger after an upgrade and should wait; sometimes buying early is still worth it (it helps another ability, adds base stats, enables a threshold, covers lane); calculate, do not apply a fixed rule. Kieran's earlier statement (charge items need 2+ charges) is a starting fact to check against data, not a substitute for calculation.
3. Joint optimisation: generate alternative ability-point orders (including unusual ones: charge/unlock first, ult early, skipping a tier) and evaluate each as a whole build: what it enables earlier (charge item usable, a threshold item procs, combo online, escape available), what it delays (damage tier, survival, farming ability), and how item order should change with it. Choose the best (point order, item order) pair; both can change.
4. Verification: the sandbox must test at the real ability tiers for each checkpoint (`abil`/level ops, not `unlock 7`); verify the tier/charge state by logging it before each block; test the contested cases (item bought before vs after the upgrade) with A/B at equal souls, grading per section H.
5. Output in each weaknesses file: an ability-timeline table and an item-vs-ability-timing table with verdicts (buy now / after point N / swap / reorder points), including cases where an earlier decision (e.g. removing a charge item) was based on a rule rather than the timeline, which must be re-checked. Any earlier build change made on a rule alone is re-opened if the timeline disagrees.
4. **Activation thresholds and conditional mechanics (Kieran, 05:31)** - part of the same timeline calculation, not a separate system. For EVERY item with a condition (damage/health/stack/hit-count/range/duration/charge/cooldown/target-state/ability-tier requirement; e.g. Mystic Burst on Violet):
   a. Verify the trigger rule from current game data (items_full / abilities.vdata, descriptions plus raw fields), never memory. Record exactly what is compared: a SINGLE hit or the total, BASE damage or scaled (Spirit Power, boons, amp), per target or per cast, which damage types and sources count, what is excluded (DoT ticks, bonus damage added by other items), and cooldown/internal limits. If the rule cannot be read from data, mark it UNVERIFIED and test it in the Sandbox known-answer check.
   b. Compute the actual number at the exact purchase moment under the current (point order, item order): ability tier, boons at that soul total, Spirit Power and investment spikes, other owned items, relevant buffs/debuffs. Compare with the threshold; report margin and which levers move it.
   c. Reliability: does it hold on every cast / only some targets / only at max range / only with a buff up? Grade with section H (theory is not proof; cap confidence for animation/positioning dependence).
   d. Enablers: which purchase or ability upgrade would make it activate (or more reliably), and its cost, including other uses of that enabler (section J).
   e. Decision: buy now / delay until enabler / change ability-point order / buy something else first / skip. Record the reason with numbers. Re-run after every reorder (it can flip).
   f. Validation: the Sandbox known-answer test must reproduce the computed damage and the trigger/no-trigger outcome on both sides of the threshold before the calculation is trusted for that item class. Until then the result is CALCULATED, not MEASURED.
   The ability-timeline tool must emit a row per conditional item (rule, compared value, threshold, margin, verdict); an item with no row is unchecked, not fine.

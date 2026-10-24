# Requirements inventory (what Kieran asked the build system / Council to do)

Sources: M-DB = memory /topics/deadlock-building.md (dated lines not available; undated "stated"), M-CC = memory /areas/deadlock-build-council.md, RK = council/RULES_KIERAN.md, R1 = rules.md / council/rules.md (identical working notes), CL = CHECKLIST.md (a14 audit checklist A-P), TM = sandbox/TEST_MATRIX.md, then the human messages in the transcript (jsonl, origin=human) with timestamps UTC (local = +1h). Transcript before 00:44 Oct 24 is only visible through the compaction summaries (jsonl L-numbers unavailable), so older items cite memory/RK.
Contradictions are marked **[CONFLICT]**. No implementation assessed.

## A. Kit / playstyle
- A1. Build per hero/playstyle only for real, popular, played styles, not invented hybrids (e.g. Victor = full Spirit "Aura Brawler" + Gun Victor; Venator melee not "close range"). M-DB.
- A2. Separate named build per viable playstyle (usually 2/hero; Lash, Mina, Pocket, Silver one) instead of role-pivot/"Behind?"/"Worth a try" boxes; a reorder-only answer = one empty box whose note explains the reorder. M-DB, RK. (supersedes older pivot boxes in R1: "Can't land the dive?" box)
- A3. Styles he explicitly requested stay even without public support (Grenade Rat King, Support Bebop, Ult McGinnis); don't remove. M-DB.
- A4. Per-hero playstyle list (main build) in M-DB/RK, e.g. Abrams tanky, Bebop gun 1v1, Dynamo support, Haze tanky healer lifesteal, Rat King grenade-only + Return Fire, Seven ult w/ early farm, Shiv = Spirit Shiv (updated; older "Shiv dash/gun"), Celeste = copy top builds (updated; older "heavy gun"), Venator grenade/melee, Sinclair melee "Rabbit Backshots" vs later "bolt Sinclair". Later wins.  **[CONFLICT: several hero styles changed over time; RK keeps both lists, "later wins"]**
- A5. A build named "gun" must be gun-heavy; melee-heavy mix is called hybrid. M-DB.
- A6. Items must match the playstyle (no Torment Pulse on squishy backline, no Escalating Resilience on burst/poke, no melee items on flyers, kiting+Sprint Boots also Enduring Speed, Glass Cannon not on tank/small-mag, Infuser only many-hit spirit heroes, Mystic Shot not on high fire rate). M-DB, RK, CL-A/L.
- A7. Playstyle of a build does not ban other items (pure gun Vindicta still Counterspell; gun Bebop buys spirit to scale bomb). M-DB.
- A8. Kit-first reasoning: read ability text thoroughly (e.g. Danny jetpack cooldown, ult pulls flyers), find non-obvious synergies (Haze smokes -> lifesteal), don't copy public builds unless genuinely high win rate; Valve default builds are "slop". M-DB.
- A9. Never base on his hunches/suggestions as gospel (Toxic Bullets on Vyper etc.), check numbers, push back, say when an item is bad; never agree blindly. M-DB, RK.
- A10. Reuse builds already agreed/made in game as the base (his in-game Haze etc.), don't rebuild from scratch. M-DB.
- A11. Research method: in-game Public browser top ~10 same-style builds/hero (hover captions of odd items), Reddit for bugs/interactions, scan FULL item list tier by tier vs kit; check Build Browser + seemeta. M-DB, R1, CL-B.
- A12. Use only data from after the latest patch affecting hero/item; same-style pick rates only (hero-wide rates mix styles). M-DB, CL-B.
- A13. Value items on ALL their roles (Ricochet: farm + fire rate for Haze ult + multi-target bounce); don't reduce to headline role; Council discovers the roles itself. msg 04:19 Oct24 (L2757), M-CC.
- A14. Kit-first build thesis: find hero's strong mechanic (Haze 2: 50% bullet lifesteal + cleanse), derive implications for damage focus/farming/survivability timing/order/redundant items, challenge every item (his builds are examples not optima, e.g. Leech vs Vampiric Burst, Healing Booster/Tempo open), incl. unusual playstyles. M-CC, 04:19.
- A15. Whole-build practicality: mag size vs fire rate, reload time lost, farming efficiency, whether delaying greens for spikes fits the hero (some farm and delay greens, some need health early), incl. when escape/defence is countered; is the build practical to play. 03:49 (L2619).
- A16. Wording of specific kit facts (Nurse Harrow: Burst Fire works on teammates, no Long Range/Rescue Beam, Ricochet bounces her healing; Haze Surge on dagger not Bullet Dance; Lifestrike procs light melee/troopers; etc.) must be applied. M-DB, RK.

## B. Item selection
- B1. Every item must fit THIS hero's kit numbers; never copy from another hero/suggestion unchecked (threshold items need clearing ability; charge items need a charge ability). M-DB, RK, CL-A.
- B2. Item relevance: each item must raise a stat the build's damage sources actually scale with (ability-damage builds: no range/headshot/fire-rate items; e.g. Trash Lobber Rat King). RK Oct22, CL-M.
- B3. Items fixing hero weakness early are fine even off-spike (Enduring Speed, Grit, High-Velocity); early lane items may be sold later. M-DB.
- B4. No untouched random 800s: every cheap item is upgraded later, is an optional that solves a lane problem, or has a named sell/replacement; assume slot-lock (3 flex slots until Walker, up to ~20 min). M-DB, RK, CL-F.
- B5. Don't buy fresh T2s late; late buys T3/T4 or upgrades. M-DB, R1.
- B6. No item twice in one build; no token investments (one lone melee item etc.); either commit or drop. M-DB, CL-A/G.
- B7. Sustain must exist (Leech core on gun Graves; Siphon alone isn't sustain); skip regen items on heroes with built-in heal; Extra Regen preferred over Healing Rite. M-DB.
- B8. Dislikes Restorative Shot/Weakening Headshot; later: Restorative Shot fine on shotgun/reliable-hit heroes but bought first or not at all (dead-end sell). **[CONFLICT/evolution: dislike -> allowed]** M-DB, RK.
- B9. Fortitude not a default (roamers, kit reason e.g. Rat King barrier, support Paige). Never Slowing Bullets. Mystic Regen only on many-hit heroes and upgraded to Radiant. Mercurial Magnum counts as gun item. Imbues go on most-cast/most-benefiting ability. M-DB, RK.
- B10. Multiple imbues on same ability all apply (not redundant). Imbue-upgrade notes never say "keep it on X". M-DB.
- B11. Counters/armours on every build (vs gun carry, flyer, spirit burst, on-hit); Counters box = menu "buy one only when dying, by killer, cheapest first; not dying skip". **[CONFLICT: early "buy 2 or 3 to not die every game, picked by enemy comp" / "After X. Pick 1 or 2" (R1) vs Oct 22 menu premise; desc text also changed between "Get after X..." (CL) and "Dying after X? Buy what is killing you..." (RK) ]**
- B12. Hero-specific sustain/lane rules: Losing-lane box = survival only (Extra Regen/Grit/Healing Rite; no damage items, no Mystic Regen); Echo Shard on Rem's 2 early; Viscous Echo Shard mid/late; Trophy Collector on pure support; Cultist Sacrifice for poor farmers (Pocket, Billy, Venator); Drifter souls from picks (Trophy, not Monster Rounds). M-DB, RK.
- B13. Rich box ("I'm rich as fuck"): T4 only, no T3, only pricier versions of something the build already does, deep late list for ~70k souls; luxuries last. Slot locked: tiny-gain/expensive upgrades only (Transcendent CD, Healing Tempo, Juggernaut), no box description, never early items; Echo Shard usually rich. If Dispel Magic present, Divine Barrier listed as rich upgrade. M-DB, RK, CL-G/O.
- B14. Swap boxes name what they replace, solve the same job, and swapped build still hits spikes (no colour dropping below 4.8k; no swap pushing health spike to ~32k). M-DB, CL-H/N.
- B15. Best complete build: challenge every item incl. same-tier substitutes and "none"; also cost-efficiency (value per soul, buy timing vs other builds). M-CC, TM#1.

## C. Synergies / combinations
- C1. Threshold chaining: order the enabler before the threshold item (Tankbuster -> Spirit Burn 500). M-DB.
- C2. Council independently discovers 2/3+ item combos incl. unconventional, understands what they enable, and PRICES each completion step by marginal gain over owned components (Healing Booster->Tempo vs Burst Fire; Seven Unstoppable+Infuser vs farm/survive/earlier spikes), when affordable, now vs later, what becomes redundant; uses current-patch numbers, not his examples. 04:25 (L2790).
- C3. Special interactions to use: Split Shot+Ricochet (each split procs Ricochet) on gun Graves; Haze Siphon+Healing Tempo; Weapon-tree spirit-damage items (Mystic Shot) after the spirit spike. M-DB.
- C4. Find non-obvious interactions via Reddit/TikTok and test (Ricochet on healing bullets). M-CC.

## D. Ability points
- D1. Ability orders copy what same-style popular builds do (real orders; cheap T1s early across abilities; e.g. Paige) -- **[CONFLICT with D2]** M-DB, CL-J.
- D2. Ability orders must suit THIS build's own playstyle, not what most do (tanky Haze: max Smoke first); be willing to experiment from ability scaling. M-DB (later line).
- D3. Orders specifics: Abrams ult maxed much earlier, his 1 low; Seven first point in Lightning Ball for 2nd charge; Grey Talon Charged Shot T1; order = 16 clicks, sensible. M-DB, R1.
- D4. Check exactly what each ability can do at each point (ability-point upgrades such as Grey Talon extra charge) to decide when Extra Charge/Rapid Recharge/Recharging Rush/CDR are worth buying; optimise point order together with item order; calculate/test, not a fixed rule; tell him whether currently implemented or only written. 04:26 (L2813).
- D5. Charge items do nothing on 1-charge abilities: put the point giving charge 2 before/at the buy and don't buy while points go elsewhere; later upgrade supplying charge is OK. M-DB, summary.
- D6. Verify ability-point costs, unlock rules and progression from the CURRENT game before trusting timelines for all 81 builds; unsettled first-point model (T1 vs unlock) -- verdicts must hold under both. Prior ability checker used simplified rules; "no dead items" NOT proven -- new timeline must be able to challenge it. 04:28 (L2857), summaries.
- D7. Re-audit ability orders against top same-style builds (gun Bebop not bomb Bebop). M-DB.

## E. Thresholds / activation requirements
- E1. Threshold items must proc when bought: check ability's single-hit damage at that point (Mystic Burst >80 vs Violet's 1 ~64; Tankbuster >165; Spirit Burn 500 in 5 s; Mystic Reverb 100; Recharging Rush 200 in 3.5 s; Witchmail late; Tankbuster not rushed). Check every hero. M-DB, CL-D.
- E2. Threshold maths counts boons (+1.1 spirit/boon), spirit invest bonus, items, imbues, ability tier at buy point; never statue/sinner buffs. M-DB.
- E3. Generalised (05:31 L2871): for EVERY conditional item mechanic, compute actual damage/mechanics at exact purchase moment (ability upgrades, boons, Spirit Power, spikes, other items, buffs); decide whether it activates, how reliably, what enables it; decide buy now/delay/reorder points/other item/skip; verify trigger rules from current data (single hit vs base vs total); and say whether this is actually calculated or only a written rule.
- E4. Item notes never state proc conditions; builder guarantees them via order/timing. M-DB.

## F. Spikes / purchase order / thresholds in souls
- F1. Race to 4.8k in main colour; spikes 800/1.6k/2.4k/3.2k/4.8k then 6.4k/8k/16k; don't overshoot a spike by a lot before the next (8k/10.4k spirit before health wrong); small overshoot OK when exact-landing cheap items don't suit. M-DB, R1.
- F2. 4.8k in EVERY colour (weapon, spirit, vitality) on most characters; applied to swaps too. **[CONFLICT/evolution vs F1 "main colour only"]** M-DB later line.
- F3. Order: damage spike first, then 4.8k health, then damage, then health; cheap greens early only if fixing lane. Exceptions: abysmal-lane heroes take lane-fixers first; Supports: gun/spirit spike first, healing later (R1). M-DB, R1.
- F4. Health-spike timing by kit: sustain/escape heroes ~14-16k; fighty without sustain ~11-12k; in-face heroes (Bebop, Abrams, Billy, Victor, Yamato) health before more big damage; mobile (Vindicta, Holliday) may delay. Council must work this out from kit/economy/combat performance, not fixed rules. M-DB, 03:49.
- F5. Spike totals count souls actually spent per colour (upgrade over owned component adds only the difference); recount after upgrades (incl. Leech consuming Spirit Lifesteal). M-DB.
- F6. Soul income ~1k/min: no 6.4k before ~20 min; no long early/mid run of 6.4ks (3+ before ~30k); snowball items after fire rate/health to use them; core cost has no target. M-DB, CL-F.
- F7. Delayed spikes must be filled with items that fix the missing spike's problem (heal/survive + damage count). M-DB.
- F8. Farming builds may take damage spikes and rush a farm item (Ricochet) before health spike, but greens start right after; very late health is bad. M-DB.
- F9. Cultist Sacrifice timing ~8:00 exactly (not earlier, not later; ~7k souls at 8:00, work out real souls) -- **[CONFLICT/evolution: later "6.4k-7.2k souls" in 4 builds; "before the 8-minute mark"]** M-DB, summary.
- F10. Core (Early/Mid/Late) must fill all 12 slots alone (no counters/rich); past 12 slots, note says what to sell. M-DB, CL-F.

## G. Farming / economy
- G1. For each hero decide whether the build needs souls and how it gets them (Trophy, Cultist, farming ability); weak farmers (Deadman Danny) need explicit answer; Lash range questions (ult reach, Greater/Mystic Expansion earlier, Trophy). 00:49 msg (L1637), TM.
- G2. Farm heroes that lose lane farm harder; Wraith/Seven early farm styles. M-DB.
- G3. Hero economy modelled for checkpoint souls (~1k/min, ~7k at 8:00, range 5.5-8.5k). summary, TM.

## H. Layout / text / export (site)
- H1. Identical layout on every build: Lane · L-R, Mid · L-R, Late · L-R; optional boxes with timing in titles; lane "pick 1" box beside Early; Counters box right of Late; every box a single row (split into two boxes); boxes sized so all items visible; one "lane going badly" box; Slot locked on every build. M-DB, RK, R1.
- H2. Don't remove+re-add items in game; park in spare box and drag. R1.
- H3. Names: "Rizuhble's <name> (Fully Annotated)", must explain playstyle, British-friendly, unique, <=32 chars, not a Valve/public name; funny but style evident. **[CONFLICT/evolution: earlier "Rizuhble YT <joke>", "funny lore names", then final format]** M-DB, CL-K.
- H4. Build description: **[CONFLICT]** "come watch me live on" + Twitch & YouTube links (M-DB final format) vs short style label only, blank if hero's usual (M-DB later, RK, CL-K).
- H5. Item notes: **[CONFLICT]** "all item explanations on the item notes, category is only a title" (earlier) vs "item notes only when needed, otherwise empty" (later; later wins). Notes: player-facing, simple, no commanding, no jargon/proc/tick/AI phrasing, "your gun", no bugs mention, no "keep it on X", no stat restatement, concrete triggers for new players, upgrades written "upgrade", sells named. M-DB, RK, CL-I.
- H6. Counters/box captions short; Tips box only for non-obvious things. M-DB.
- H7. Every note/claim TRUE vs game files (Dispel vs Geist bomb, Unstoppable scope, Spirit Resilience heroes). CL-I.
- H8. Keep the existing website, import system (codes), rules, preferences, progress. M-CC. Pipeline data.js -> rebuild.sh -> mkcodes.js -> in-game import (Importer only when he says; never overwrite non-"Fully Annotated" builds). README, IMPORT.
- H9. He copies codes into game himself; builds made in website not in game; he drags items. M-DB.
- H10. Written order in text when clicking slow. M-DB.
- H11. Build names/descriptions for every build. M-DB.
- H12. Don't change his builds just because the audit finds a possible improvement; preserve current pilot/progress. 05:37.

## I. Review / process
- I1. Audit: when he points out a mistake treat as problem TYPE, hunt it across all builds. M-DB.
- I2. "Final audit zero mistakes" standard; checklist A-P per build; tools walk1 (FLAGS none), check12, sp.js. CL (Oct 20).
- I3. Council of specialist agents: research, theorycraft, create, test, improve, cross-check before finalising; Duo Builder retained. M-CC, PROTOCOL.
- I4. Cost-efficiency sub-agent: value per soul, buy timing, cross-build comparison. M-CC.
- I5. Make the calls yourself when data supports; ask only on pure taste inside set playstyle; no per-hero teaching; no "go test X". M-DB, 02:30, 04:11.
- I6. Council takes responsibility for missing mechanics, regular self-review (missing mechanics, misleading measurements, complexity, efficiency); progress = consistent evidence-backed decisions, not number of tests/features; don't force conclusions ("cannot measure" valid); milestone updates only; say when unverified. 04:11, 04:12 (L2470, L2486).
- I7. Weakness -> remedy process: find weaknesses, independently work out best fix across all categories (item, ability use, positioning, target choice, team, accept/leave alone), test promising, cost/tradeoff, utility-to-damage only when timing/counterplay allow, decide core/situational/playstyle/leave, re-check no new weakness. 04:33 (L2502).
- I8. Dependency chains: strengths compensate weaknesses; enemy counters strength (Wraith teleport vs Slowing Hex); investigate prevent / recover / survive; enemy counters to our fix; commonness vs souls cost; items he names are examples. 04:41 (L2585).
- I9. Evidence grades; uncertainty explicit (kit maths != proven); confidence caps for animation/positioning/enemy reaction/complex interactions. summary, M-CC.
- I10. Independent reviewer (blind) tries to break each build; audit itself needs independent reviewer; one challenge per core item. PROTOCOL, 05:37.
- I11. Audit request (05:37 L2930): inventory all requirements; distinguish written / coded / integrated / tested; inspect real code, builds, results; find claims not handled; check decisions use all considerations together (not each agent separately with final build ignoring findings); critical of own work; no new rule/agent explosion; then prioritise fixing top gaps.
- I12. Don't disrupt the running pilot; don't touch builds from audit. 05:37.
- I13. Builds for new players (concrete triggers e.g. "lots of gun carries on your team").

## J. Sandbox testing
- J1. Sandbox Tester that works in-game (spawn, give items, test); if it doesn't function don't use it again; Deadworks private local server on E:, no -insecure on his client; auto-launch/keep running and auditing continuously; relaunch if closed (Oct 23 "don't open" superseded Oct 24 "launch the tester"). M-CC. **[CONFLICT time-ordered]**
- J2. Realistic multi-enemy play (Victor vs 3; Wraith Ricochet+Leech vs Vampiric Burst); 1, 2, 5 enemies; surround 4-5 bots but shoot one; incoming gun AND spirit damage; low-HP starts. M-CC, TM.
- J3. Not best case: different price points (5k lane, 10k, 18k, 24k, 30k, full 12) buying build strictly left-to-right incl. components; heroes alphabetical (Abrams..., Deadman Danny); every hero/build; re-run each patch. M-CC, TM (01:43, 02:24).
- J4. Realistic accuracy (40-50%; Eternus-level), mix headshots/body (aim slightly above/side to miss, no flicks; later "look at ground" to miss); report whether winner changes. TM, 02:50.
- J5. Enemy resists (bullet/spirit) so resist-shred judged; enemy god mode / never dies; enemies buy items; range-limited items test at both ends and fleeing targets. TM.
- J6. Clean state between blocks (remove ALL items both sides, clear buffs, reset CDs, heal, respawn), counterbalanced order, >=3 repeats, warm-up bias handled. TM. (Do not corrupt cooldowns; use hardreset.)
- J7. Optimal rotations per hero derived from kit (actives first: Focus Lens, Alchemical Fire; imbue/proc conditions satisfied); hero-specific play (Calico, Baba, Apollo, Abrams melee range, Celeste stacks, Drifter isolated, Grey Talon owls, Infernus dash trail, Kelvin ice path, Lash height, Danny slam+ult). 00:49.
- J8. Stack/ramp mechanics modelled at 0/partial/max (Berserker, Celeste 3, Pocket Barrage, Ballistic Enhancement, Radiant Daggers, Glass Cannon, Fiery, charging/ramping guns); equal stacks/equal time-in-effect; Occam's razor: check hero's kit first before crediting item/headshot (Victor aura time, per-bullet ramps). 01:24, 03:59, 04:05.
- J9. Healing attribution: list all heal sources, baseline, marginal at low HP; read end-of-match stat graphs or subtract. TM, 01:24.
- J10. Support/utility judged on outcomes (ally survives, ult range, downtime), not raw healing (Viscous, Dynamo, Rem: Healing Nova vs Rescue Beam). M-CC, TM.
- J11. CC and the build's answers tested (Unstoppable, Dispel, Reactive Barrier, Warp Stone); escapes/catch (Mina, Vindicta flying, Danny). TM.
- J12. Boons/ability points at that level (not max); close-range abilities test with enemies moved close; tests positioned in the arena he picked (noclip open ground), verified after every reset; guard must not interfere with legit movement (charge/teleport/fly); exact start distances verified per experiment. 04:06, 03:38, 03:49, 03:52 (L2063, L2403, L2619, L2688).
- J13. Item questions: Infuser vs Leech by price point; damage testing; proc thresholds; cooldown reality (Surge of Power); Extra Charge vs Recharging Rush on Grey Talon. M-CC, TM.
- J14. Tester results must feed back and challenge bad item choices; Sandbox can overturn calculation; calibration/reliability checks re-run after any tester change (not just pilot). M-CC, 04:12.
- J15. Pilot: small number of representative builds (Victor gun, Abrams tank/melee, Wraith) end to end: uncertain decision -> fair comparison -> run -> detect failure -> analyse -> say whether build changes; then expand. 04:11.
- J16. Fix broken cooldown display (Pain Battery -2B, 1200 s) and keep it fixed. 00:44 summary.
- J17. Morning summary of optimal vs not + proposed data.js changes, no auto-apply removals without verification. TM.
- J18. Don't test in-game while he plays something else; drive his PC only to browse builds, not make them; never launch a second Deadlock instance. M-CC, M-DB.

## K. Duo builds
- K1. Duo builds: separate build per hero in the pair, never replacing main; Council derives pairs from stats/kits (his examples are guesses); real combos = partner solves exactly what a hero struggles with, builds change because of partner, reliable not gimmick; reject cross-shred "nice to have". M-CC.

## L. Models
- L1. Cheap models for simple work, Sonnet 5.5 everyday coding/sandbox/analysis, Opus 5.5 only for deep reasoning (architecture, unconventional strategies, synergies, contradictions, review); actually configured (not just stated); avoid repeated work; hit usage limits but don't sacrifice theorycraft quality. 04:27 (L2833), M-CC.
- L2. Pick model/effort per task by judgement. 04:27.

## Conflict list (consolidated)
Counters box semantics (B11); 4.8k main-colour vs every-colour (F1/F2); ability order copy-popular vs own-style (D1/D2); description = Twitch/YouTube text vs style label (H4); notes everywhere vs notes only when needed (H5); Cultist 8:00 vs 6.4-7.2k (F9); Restorative Shot (B8); pivot boxes vs separate builds (A2); per-hero styles that changed (A4); Deadlock open/not open (J1); R1 "Can't land the dive?" pivot, "Counters desc After X. Pick 1 or 2." superseded.

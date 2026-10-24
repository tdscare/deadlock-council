# Wraith / "Rizuhble's Pinball Wraith" (id `wraith`) - weakness -> remedy record
Weakness-solver pass, 2026-10-24. Process: council/WEAKNESS_PROCESS.md. Sources: data.js build `wraith` (read-only), audit/items_full.json, audit/hero_wraith.txt, sandbox/GAPS.md, sandbox/playstyle/wraith.md, council/RULES_KIERAN.md, AUTORUN.md ops only. Nothing in data.js or the game was touched. Only one Wraith build exists, so the file is `wraith_wraith.md`.
Revision 2 (2026-10-24, updated WEAKNESS_PROCESS A2 + H): added section A2 (identity map, verified counters, ranked chains, PREVENT/RECOVER/SURVIVE, counter-the-counter, frequency), an evidence grade on every verdict, the verified Leech/Spirit Lifesteal cost correction (A2.6), probes P-CC0/P-PM, a re-ranked summary. Earlier analysis and tests kept unchanged below.

## A2. Hero identity map and dependency chains (revision 2, 2026-10-24, per WEAKNESS_PROCESS A2/H)
Added on top of the first pass; sections 0-6 are kept and graded. Tags: [kit]/[item] = read from audit/hero_wraith.txt / audit/items_full.json; [GAP] = number or rule not in the data; [U] = game knowledge to verify in game. Frequency proxy used throughout: share of the Council's own 81 builds (44 heroes, data.js) that buy the counter in core ("core x/81"); it is a proxy for "how often an enemy owns it", not a public pick rate, and assumes enemies build like the Council does.

### A2.1 Identity map (strength -> what it compensates -> what it depends on)
| strength [source] | compensates | depends on (conditions) |
|---|---|---|
| Project Mind teleport, 25 m (+15 m T1 at point 9), 0.75 s cast delay with ChannelMoveSpeed 5.1 m; T2 (point 10) 300 barrier for 5 s, spirit-scaled [kit]. Cooldown not in data [GAP]; T3 effect not in data [GAP] | No dash, no armor items in core, stands still in Full Auto: PM is her only fast escape and (from point 10) her only on-demand barrier | Not silenced/stunned/slept/movement-silenced for the 0.75 s plus the decision moment; PM off cooldown; a safe landing spot within 25-40 m; the trail may show where she went (TrailInterval stat) [U] |
| Gun + fire-rate stack (Swift Striker 20, Ricochet 18, Overflow 25, Mercurial 22, Surge 20 on use, Full Auto 20-30) with Ricochet 2 bounces at 65% in 13 m [item] | Low burst, no execute; also feeds sustain (lifesteal) and card resource | Bullets hitting heroes (aim, line of sight, no bullet immunity/evasion on the target), ammo (W6) |
| Lifesteal stack: Leech 28/28 (39.2k), Overflow 13 (+10 charged), Spirit Rend 10, Bullet LS 13 before Leech; Hearts 60 + 0.5x (T2 +75 +0.5x) [item/kit] | Low HP pool and no armor: she heals by fighting back instead of leaving | Dealing damage to heroes; healing not reduced; Ricochet bounce heals not confirmed (P1) |
| Card Trick: 2 charges, 0.6 s cd, 45 + 0.55x, 500 m range, suits: Clubs 24% slow 3 s, Diamonds -7 resist, Hearts heal, Spades +60 [kit]; Mercurial/Quicksilver/Surge imbued on it | Ranged spirit damage, a ranged slow, healing and reloads (Mercurial reloads on use) | Card resource from bullet hits (4/hit, 6/crit) and melee; not silenced (it is an ability) |
| Telekinesis: 10 m, 0.45 s delay + 1.25 s channel, lifts 2 s, slam 100 (+100 T1) + 1.0x, 32% slow, prevents stamina and movement items/abilities; 150 s (-45 at T2, point 14) [kit] | Peel: removes one diver, and denies THEIR escape | Within 10 m (so she is in danger range), not silenced/stunned during cast and channel [U whether stun breaks the channel], 105-150 s cooldown |
| Reactive Barrier (core, 23.2k): 325 + 1.8x spirit barrier when Stunned, Chained, Immobilized, Slept or Silenced; 55 s [item] | Survives the CC window that disables PM | The CC type must be in that list (slows and Disarm are not; whether Slowing Hex's movement silence counts as "Silenced" is [U]); 55 s cooldown |
| Enduring Speed (21.6k): +2 m/s, 25% slow resist [item] | Kiting and walking out when PM is down | Slows only; does nothing vs silence/stun |
| Inhibitor (45.6k): bullets build up -30% outgoing damage and -40% healing on the target [item] | Reduces the damage of the one hero she is shooting | Hitting that hero for long enough (0.77/shot build-up); useless vs a second attacker she is not shooting |
| Silencer (53.6k): bullets build up a 2.5 s silence, 10 s immunity after [item] | PREVENT layer vs ability-based CC (kit stuns/sleeps) from the hero she is shooting | Build-up 1.04/shot over 5 s; does not stop item CC (Slowing Hex, Knockdown, Cursed Relic are items; [U] that silence blocks only abilities, implied by Cursed Relic listing "preventing item usage" separately) |

### A2.2 Enemy counters to each dependency (verified against the data; nothing listed that is not in it)
Teleport denial (the main example, checked, not assumed):
- Movement-silence: Slowing Hex (T2, 25 m, 0.1 s cast, 3.5 s, 29 s cd, "Silences their movement-based items and abilities") [item]; Capacitor (T4, projectile, slow 60%, "Silences their movement-based items and abilities") [item]; Wraith's own Telekinesis slam has the same rider. Vortex Web (upgrade of Slowing Hex) has no description in items_full: whether it keeps the movement silence is [GAP]. Whether Project Mind counts as "movement-based" is not in the data; the user note ("slowing hex stops teleport") is the only evidence [U, user-observed]. Core 9/81 builds own one of these (8 heroes).
- Full silence: Silencer (bullet build-up, 2.5 s), Focus Lens (targeted, 25 m, 4.5 s, 45 s cd), Cursed Relic (20 m, 3.25 s: "interrupting, Silencing, Disarming, and preventing item usage. Removes all non-ultimate buffs"), Silence Wave (40 m, 3 s; "does not interrupt channeling abilities"), Haunting Scream (T5 curse 3 s); kits: Grey Talon Spirit Snare (silence/immobilize/disarm, interrupt), Violet ult silence 2 s [hero data]. Core 14/81 builds (13 heroes). Note: PM's 0.75 s is channel-like (ChannelMoveSpeed), so a plain silence may block a new PM but not cancel one in progress [U]; Cursed Relic interrupts explicitly.
- Stun / sleep / immobilize / freeze (all interrupt casts [U for items that do not say so]): Knockdown (0.5 s after a 2 s delay, 45 m), Crushing Fists (6 melee stacks, 0.75 s), Lightning Scroll (ult hit then 0.75 s after 3 s), Arctic Blast (1 s freeze), Mystical Piano, Unstable Concoction, Frostbite Charm [item]; kits with an explicit interrupt: Haze Sleep Dagger 2.75 s, Infernus Concussive Combustion 1.25 s; other kit stuns/immobilizes: Seven 0.9 s, Venator 0.6 s + snap trap 1.25 s, Paige 1 s, Solomon 1-1.25 s, Violet 1 s, Grey Talon owl 0.75 s, Abrams 1.6 s, Viscous, Danny, Rem sleep [hero data, 14 of the 20 heroes in heroes_full have a hard disable]. Item stuns in core 15/81.
- Any of the item counters above in core: 34/81 builds (26/44 heroes). With 6 enemies drawn at that rate, P(at least one) = 1 - 0.58^6 = 96%, before counting kit CC. Treat "PM can be denied in a given fight" as near-certain; the question is how often it is denied at the moment she needs it.
- Not a teleport counter, though it looks like one: plain slows (Slowing Bullets, Cold Front, Mystic Slow, Point Blank) do not stop PM in any item text; they only hurt walking (Enduring Speed covers 25%). Disarm (Disarming Hex, Phantom Strike, Cursed Relic) does not stop PM; it stops her gun.
- Baiting/punishing: PM cooldown [GAP] and the visible trail let a team follow or wait; burst before the 0.75 s completes.
Sustain denial: anti-heal items: Toxic Bullets -35%, Inhibitor -40%, Crippling Headshot -35%, Healbane -35% (on spirit damage, 8 s), Decay -50% (12 s), Spirit Burn -70% (after 500 spirit damage in 5 s, 8 s, once per 20 s per enemy), Haunting Shot -40%, Nullification Burst "prevents healing effects"; kit: Venator Consecrating Grenade -30% [item/hero data]. Core 47/81 builds (36/44 heroes): P(at least one of 6 enemies) > 99%. Leech "reduces the effect of enemy applied healing reduction" by an amount not in the data [GAP].
Gun denial: Metal Skin (5 s bullet immunity; Counters in 75/81 builds), Plated Armor (30% deflect, 50% of bullet on-hit effects prevented: also blunts her Silencer/Inhibitor/Tesla procs [U whether build-ups count as on-hit]), Ethereal Shift (4 s invulnerable), Disarming Hex (4.25 s, 0/81 builds), Phantom Strike / Cursed Relic disarm, fire-rate slows: Hunter's Aura -15% (x2 single target; core 10/81), Rusted Barrel -32%, Suppressor -28%, Return Fire (reflects 65% bullet damage) [item].
Card/imbue denial: silence blocks Card Trick (ability), so no thrown cards, no Mercurial reload-on-use, no Surge move-speed proc for the silence; existing Mercurial bonus bullets last until her next reload [item text].

### A2.3 Chains, ranked by frequency x lethality
| rank | chain | frequency | lethality | F x L |
|---|---|---|---|---|
| WC1 | PM covers no-escape/low-HP; movement-silence, silence, stun/sleep or cooldown-bait deny it; she is exposed standing still (often in Full Auto) to the team that just used CC on her | H (96% of lobbies own an item counter; most kits have one) | H if the denial comes from a diver with burst follow-up; M if she can fight back (silence leaves her gun, Leech, Inhibitor, Silencer working) | 1 |
| WC2 | Lifesteal covers low HP and no armor; anti-heal cuts Leech/Overflow/Rend/Hearts; the fight-back answer to WC1 also weakens | H (>99%) | M: slow erosion, not a one-shot; Leech offsets an unknown part | 2 |
| WC3 | Gun drives damage, heal and cards; Metal Skin / Ethereal Shift / Plated Armor / disarm turn off all three at once | M (reactive buys, mostly Counters menus) | M (lost trade, rarely lethal by itself; combines with WC1) | 3 |
| WC4 | Card Trick is the imbue hub (Mercurial, Surge, Quicksilver path); silence removes cards, reload-on-use and the move-speed proc | M (silence core 14/81) | L-M (output loss, ammo pressure W6) | 4 |
| WC5 | Telekinesis peel needs 10 m and a 1.7 s cast+channel; silence/stun deny it, and it is up once per 105-150 s | M | L-M | 5 |

### A2.4 WC1 in three layers (all remedy classes; items derived from the data; prices from the walk)
PREVENT (stop the denial landing)
- Positioning/ability use: fight from beyond the common CC ranges (Slowing Hex/Focus Lens 25 m, Cursed Relic 20 m; Knockdown 45 m and Silence Wave 40 m outrange this) since cards reach 500 m and the gun has no close-range items; teleport early (when the diver commits), not at low HP; keep PM for escape rather than engage when the enemy CC carriers are alive and not on cooldown. Cost 0; burden: decision-making. Counter: long-range CC (Knockdown, Silence Wave), invisible/flanking divers.
- Silencer (core, already): silences the hero she shoots; stops kit CC (stuns, sleeps, Spirit Snare) from that hero for 2.5 s, not item CC. Counter: 10 s immunity after, Plated Armor proc deflection, a second CC source.
- Unstoppable pre-emptively (Counters menu; T4, built from Debuff Reducer; 6.4k fresh): 5.5 s immunity to stun/silence/sleep/root/disarm, "suppress negative status effects". Verified limit: "Cannot be used while Stunned or Slept", so it is PREVENT for stuns (pop before) and RECOVER only for silence/root/disarm. Counter: Cursed Relic removes non-ultimate buffs and prevents item use [U whether it strips Unstoppable], baiting it then CC after 5.5 s, damage (it is not a defence).
- Counterspell (Counters menu, T3 3.2k): next parry within 0.8 s blocks damage and effects of enemy abilities and items. Covers seen projectiles (Silence Wave, Capacitor, kit skillshots); weak vs instant targeted casts (Slowing Hex, Focus Lens, Cursed Relic have 0.1 s cast delay) [U whether parry stops targeted casts]. Burden: a timed button.
- Hexafoil Ward (T3 3.2k, not in any build): "Block the next [word missing in data] or Debuff"; only regenerates out of combat. A passive one-per-fight block of the opener (Slowing Hex / silence). Counter: any minor debuff pops it first (Clubs-like slows, Silencer build-up? [U]), one block per fight. Candidate only: description incomplete [GAP].
RECOVER (undo it once applied)
- Divine Barrier (rich box; T4 from Guardian Ward): verified "Remove all non-stun debuffs" + 600 barrier + move speed, 0.2 s cast, 45 s. Covers silence, movement silence, slows, anti-heal debuffs, disarm; not stuns. Usable while silenced [U: items under silence], not while stunned [U].
- Dispel Magic (Counters menu, T3 3.2k): data has no description, only 10% spirit resist, +2 m/s for 3 s, 250 heal on use [item]. That it removes Slowing Hex/silence rests on its name and the user note [U, unverified scope]. If it does not cleanse, the menu line "Silences and hexes keep stopping your teleport" points to the wrong item and Divine Barrier is the verified one.
- Unstoppable after a silence/hex (see above); not after a stun.
- Indomitable (rich box; upgrade of Reactive Barrier, class name upgrade_auto_cleanse): no description in data; cleanse scope [GAP].
- Second escape when PM is denied by a plain silence or on cooldown: Warp Stone (T3 3.2k, 11 m instant, +30% bullet resist 6 s). It is an item, so an ability silence should not block it [U], but it IS a movement item, so Slowing Hex/Capacitor block it exactly like PM. It replaces a core slot (Enduring Speed or Rend). Covers the silence and cooldown cases only.
- Ally peel/cleanse: not modelled (no ally ops).
SURVIVE WITHOUT RECOVERY (live through the window)
- Reactive Barrier (core): ~325 + 1.8 x spirit (about 415 at 50 spirit) on stun/silence/sleep/immobilize. Does not fire on slows or disarm; [U] on movement silence. 55 s cd.
- Fight back: under a plain silence or movement silence her gun, Leech, Inhibitor (-30% damage of her target) and Silencer all still work; vs a single diver this is the realistic answer. Fails under stun/sleep/disarm, vs two attackers, and vs anti-heal (WC2).
- Metal Skin (Counters): 5 s bullet immunity, usable under ability silence [U]; verified cost: -1.5 m/s move speed during it, so it fights walking away; nothing vs spirit.
- Ethereal Shift (in other builds' rich boxes; T4): 4 s invulnerable, "instantly"; buys the CC duration out (2.5-4.5 s silences, 3.5 s hex). Counter: they wait 4 s; Cursed Relic prevents item use first.
- Spirit Resilience / Plated Armor (Counters): flat resist vs the damage type that follows.
- Accept the death and minimise its cost: PM early so the death happens less deep; no item helps the respawn here.
Counter-the-counter summary: Cursed Relic (core 5/81, 11 heroes) beats every active answer at once (prevents items, removes buffs, interrupts, silences); only passives survive it (Reactive Barrier [U trigger on curse], Hexafoil if unspent [U]). Stuns beat Unstoppable/Divine Barrier/Dispel unless used first. A second disable after a 5.5 s Unstoppable or a 45 s Divine Barrier. Anti-heal weakens the fight-back layer. Long-range CC beats positioning.

Frequency check and decision for WC1: the chain is near-universal, but the answers above are all either already in the menu (Unstoppable, Dispel, Counterspell, Divine Barrier, Metal Skin) or cost a core slot for partial coverage (Warp Stone covers silence/cooldown, not hex; Hexafoil one block per fight). No single item covers stun + silence + hex + item lockout. Core change is not justified on this grade.
- Verdict WC1: keep core; keep the Counters menu; reviewer notes (not data.js edits by this file): (1) Dispel Magic's cleanse is unverified in the data, Divine Barrier's is verified: if a game check shows Dispel does not remove Slowing Hex/silence, swap the menu line to Divine Barrier; (2) Unstoppable's line "Stuns keep cancelling your teleport" is only true if it is used before the stun (data: cannot be used while stunned); (3) Hexafoil Ward is a candidate menu line vs "one hex/silence opener" pending a game check of its text. Grade: UNTESTABLE-HIGH-RISK (CC timing, item-under-silence rules, enemy reactions). Confidence 45%. What would make it wrong: PM not counting as movement-based (then Slowing Hex is not a counter at all); normal silence blocking items (then all active RECOVER answers fail under silence and the passive answers, Reactive Barrier/Hexafoil, rise); a measured lobby-level rate of CC-denied deaths much higher than other deaths.

### A2.5 WC2 to WC5 (shorter; same three layers)
- WC2 anti-heal on lifesteal. PREVENT: kill or out-range the anti-heal carrier (Healbane/Decay/Spirit Burn need their spirit damage on her; Toxic/Inhibitor/Crippling need their bullets: Plated Armor's 50% proc prevention [U for build-ups]); Inhibitor on the carrier cuts their damage, not their debuff. RECOVER: Divine Barrier removes the debuffs (non-stun) and Spirit Burn cannot reapply from that enemy for 20 s (per-enemy cooldown, verified text), so one cleanse buys real time vs Spirit Burn/Decay; bullet build-ups reapply within seconds. Leech's reduction amount [GAP]. SURVIVE: barriers (Reactive Barrier, PM T2) are not healing so anti-heal does not cut them [U]; resist items. Counter-the-counter: two anti-heal sources stack [U]; Nullification Burst prevents healing outright. Verdict: keep Leech (also the only item in the build that touches anti-heal); no change. Grade: CALCULATED (kit maths; Leech's mitigation size unknown; anti-heal UNSUPPORTED in Sandbox, GAPS 8). Confidence 50%. Wrong if: Leech's mitigation is negligible and VB measures ahead in P2 (then the anti-heal argument for Leech disappears).
- WC3 gun denial. PREVENT: switch target to the hero without Metal Skin up (5 s), throw cards (spirit, not blocked by Metal Skin) during it; Plated Armor on the enemy deflects 30%: stays. RECOVER: none needed (time). SURVIVE: Full Auto magic bullet damage is spirit [U whether it passes Metal Skin]. Verdict: playstyle note "cards and target swap during Metal Skin", no items. Grade: CALCULATED (item text). Confidence 60%. Wrong if: cards cannot be generated during Metal Skin (no bullet hits = no resource; she may have 0 cards banked).
- WC4 silence on the imbue hub. PREVENT: same as WC1 (Silencer, range). RECOVER: Unstoppable/Divine Barrier (menu). SURVIVE: reload normally; Mercurial bullets persist until reload, so do not reload under silence while bonus bullets remain (playstyle). Verdict: leave; note only. Grade: CALCULATED. Confidence 55%. Wrong if: Mercurial's buff ends on silence [U].
- WC5 Telekinesis peel. Verdict: leave (ultimate, 105-150 s; no item fixes the 10 m range need). Grade: UNTESTABLE-HIGH-RISK. Confidence 50%.

### A2.6 Correction carried from the first pass: Leech consumes Spirit Lifesteal (verified)
items_full.json and gamedata.js both list Leech = [Bullet Lifesteal, Spirit Lifesteal]; Spiritual Overflow = [Spirit Lifesteal]; Vampiric Burst = [Bullet Lifesteal]. In this order Overflow (34.4k) consumes the only Spirit Lifesteal, so Leech (39.2k) is credited Bullet Lifesteal only: 6.4k - 1.6k = 4.8k, i.e. it pays for a second Spirit Lifesteal inside its price. The walk (wk2/walk_wraith.txt, regenerated from data.js) already prices it at 4.8k, so spikes are correct (gun 5.6k, spirit 10.4k, health 21.6k); only the old changes-log sentence "Bullet Lifesteal makes Leech a 3.2k upgrade instead of 4.8k" is wrong (true value: 4.8k instead of 6.4k). Reordering Leech before Overflow makes Leech 3.2k and Overflow 6.4k: total identical (9.6k), it only moves 1.6k of spend and swaps which arrives first. Price comparison at the 39.2k slot stays fair: Leech 4.8k = Vampiric Burst 4.8k. Grade: CALCULATED (deterministic shop maths from component data). Confidence 90%. Wrong if: the shop credits consumed components differently from walk2.js.

## 0. Build as it stands (walked from data.js; audit/walk_wraith.txt regenerated from it)
Core 53.6k, 12 slots after sells: Swift Striker, Surge of Power (Card Trick imbue), Tesla Bullets, Mercurial Magnum (Card Trick imbue), Ricochet, Enduring Speed, Reactive Barrier, Spirit Rend, Spiritual Overflow, Leech, Inhibitor, Silencer. Monster Rounds sold for Spirit Lifesteal.
Order: Ricochet 16.8k, Spirit LS 18.4k, Bullet LS 20.0k, Enduring Speed 21.6k (health 4.8k), Mercurial 29.6k, **Spiritual Overflow 34.4k (consumes Spirit Lifesteal)**, **Leech 39.2k (consumes Bullet Lifesteal; costs 4.8k)**, Inhibitor 45.6k, Rend 47.2k, Silencer 53.6k. Spikes: gun 5.6k, spirit 10.4k, health 21.6k.
Ability points (order 1132341322314424): Card Trick unlock/T1/T2/T3 at points 1/2/7/12; Full Auto 3/5/8/11 (T3 = unlimited ammo at point 11); Project Mind 4/9/10/15 (T2 barrier at 10); Telekinesis 6/13/14/16.
Kit sustain already present: Card Trick Hearts (HeartHeal 60 + 0.5 spirit, T2 +75/+0.5; half vs non-heroes), Overflow spirit LS 13 (+10 when charged), Rend 10% spirit LS, Bullet LS 13 / Spirit LS 13 until upgraded, Reactive Barrier (325 + 1.8 spirit on CC), Project Mind T2 barrier 300 (5 s), Frenzy only in rich box.

## 1. Test environment limits that shape every test below (AUTORUN.md + GAPS.md)
- Ops used: hardreset, give, souls, unlock 7, enemies n r, fetch, aimoff, accuracy p headFrac, ekeep/ehp, eresist, eitem, incoming, lowhp, hurtme, healreset/healsum, mark, fire, cast <1-4|i1-i4|melee|reload>, move, wait, acclog, mods, cds. Heals are measured as `healDiffObserved` (HP jumps), never per-source: isolate by item removal and subtract (GAPS: Victor run).
- No imbue op (GAPS 1): Mercurial/Surge/Quicksilver may be inert. Probe P0 below. Until proven, they are given identically in both arms and the verdict is tagged "spirit damage possibly undercounted (biases toward VB)".
- Headshots uncalibrated: use `accuracy p 0` (body only). aimoff 5.5 3 valid only at fetch 350.
- No anti-heal on player (GAPS 8), no CC op (GAPS 7), no moving target (GAPS 16), no NPC/camp spawn (GAPS 21), bots never shoot (GAPS 17), `incoming` is 100 ms ticks (GAPS 6). Anything needing these is UNSUPPORTED.
- `fire N` ends at an empty mag: use repeated `fire 3` + `cast reload 2.5` chunks (over-penalises reload slightly; same in both arms).
- Item classes: Leech upgrade_damage_recycler, Vampiric Burst upgrade_surging_power, Bullet LS upgrade_vampire, Spirit LS upgrade_health_stealing_magic, Overflow upgrade_tech_overflow, Ricochet upgrade_ricochet, Mercurial upgrade_ethereal_bullets, Surge upgrade_magic_storm, Tesla upgrade_chain_lightning, Swift Striker upgrade_blitz_bullets, Enduring Speed upgrade_cardio_calibrator, Reactive Barrier upgrade_vex_barrier, Rend upgrade_spellslinger_headshots, Inhibitor upgrade_inhibitor, Silencer upgrade_proc_silence. Give only FINAL items (components double count, GAPS 22).
- Reps: >=5 per arm, order A B B A / B A A B, hardreset between blocks, noise floor from an A/A pair first (PILOT 0.3); effect below that = "no detectable difference". Decision threshold pre-registered: 15% on net HP over the window (matches scenarios/wraith_leech_vs_vampiric.json).

## 2. Weakness table
Severity = how often x how costly (H/M/L). "Kit solves it?" = already covered by the kit/build.

| ID | Category | Weakness | Evidence (data) | Severity | Kit solves? |
|---|---|---|---|---|---|
| W1 | Survival/sustain | Bullet lifesteal slot (Leech vs Vampiric Burst) is the build's only large sustain choice and its value depends on unmeasured things: do Ricochet bounces heal, bullet:spirit damage split, anti-heal | Leech 28% bullet + 28% spirit (hero), +180 HP, +12 spirit, +12% weapon dmg; VB 13% passive, +70% for 5 s, +34% fire rate, 75% reload, +100 HP, +10% bullet resist, cooldown absent from items_full; Ricochet "applying any bullet procs and 65% damage" (does not say lifesteal) | H | partly (Hearts, Overflow, Rend) |
| W2 | Survival | Mid-game sustain/health gap 20k-39k: only 13% bullet + 13% spirit LS until Overflow (34.4k) and Leech (39.2k); fights at 25-35k are the first real focus fights | walk: health 4.8k at 21.6k, Leech 39.2k, Inhibitor 45.6k | M-H | partly (Enduring Speed, Reactive Barrier, Counters menu) |
| W3 | CC/escape | Project Mind 0.75 s cast delay, 25 m (+15 T1), cancelled by silence/slow hex/stun (user note), Telekinesis 10 m range, 0.45 s cast, 1.25 s channel | hero_wraith.txt | H | partly (Reactive Barrier on stun, Dispel/Unstoppable in Counters, Enduring Speed 25% slow resist, PM T2 barrier at point 10) |
| W4 | Survival | Squishy gunner standing still in Full Auto/Overflow build-up; focus burst | no armor in core except Reactive Barrier/Enduring; health 16.0k only with Inhibitor | M | partly (Counters menu, Inhibitor -30% enemy damage, Metal Skin/Plated menu) |
| W5 | Output | Card Trick economy depends on hits: 4 per bullet hit, 6 crit, 10 light / 25 heavy melee, 100 per card (ResourceGenPctScale 85); misses starve cards | hero_wraith.txt | M | partly (Mercurial/Quicksilver charge on a timer, Ricochet may add hits) |
| W6 | Output | Ammo/reload: fire rate stacked very high (Swift 20, Ricochet 18, Overflow 25, Mercurial 22, Surge 20, FA 20-30, VB 34) with no clip item; Full Auto T3 unlimited ammo arrives only at ability point 11 and only for 5-8 s every 45 s (25 s with T1) | items_full, hero_wraith.txt | M | partly (Mercurial refills + 20% clip on Card Trick, FA T3) |
| W7 | Output | Single-target / late bullet resist: Ricochet is a cluster item; no bullet shred in core (Bullet Resist Shredder cut in Round 14), spirit shred present (Rend, Exposure in rich box) | build rows | M | partly (Ricochet +18% fire rate alone, spirit damage from cards/Tesla/Mercurial/FA) |
| W8 | Economy | Early lane/farm and snowball dependence: Ricochet at 16.8k, Monster Rounds sold, Wraith has no reach/CC in lane | build, GAPS 21 | M | partly (Tesla/Card waveclear, Losing-lane Extra Regen) |
| W9 | Output | Ability downtime: Full Auto 45 s (-20 T1), Telekinesis 150 s (-45 T2), Cards 2 charges / 0.6 s | hero_wraith.txt | L-M | yes (gun fills gaps) |
| W10 | Reach | Chasing fleeing/flying targets | Card Trick range 500 m, TP 25 m | L | yes |
| W11 | Finishing | No execute; Telekinesis slam 100 + 1.0x spirit | hero_wraith.txt | L | n/a |
| W12 | Build structure | Spirit lifesteal stacking may overshoot (Rend 10 + Overflow 13/23 + Leech 28 + hearts) while bullet lifesteal is thin; Overflow and Leech both consume lifesteal components (Overflow takes Spirit LS, Leech then costs 4.8k, not 3.2k as Round 13 note assumed) | walk costs | L-M | n/a |
| W13 | Dependency | Mercurial/Surge/Quicksilver require the Card Trick imbue; the whole spirit plan assumes it | data.js imb=1 | M | n/a |

## 3. Per weakness: remedies, price, test, decision

### W1 Sustain slot: Ricochet+Leech vs Vampiric Burst (the question asked)
**Remedies**: (a) Leech (current core). (b) Vampiric Burst in the same slot. (c) Both (needs a slot: sell Silencer or Inhibitor, +4.8k to +6.4k, VB needs its own Bullet LS so total about +6.4k). (d) Neither, keep Bullet LS 13% and put the 4.8k into damage/Frenzy (rich box). (e) Playstyle: Heart cards + Overflow charge before engaging (free). (f) Infuser (needs Spirit LS, consumed by Overflow; skip). (g) Fury Trance (3.2k: 14% passive, 32% fire rate, 40 spirit resist, 6.5 s) as a mid-game stepping stone: rule says no stepping stones that are sold later, so only as a replacement, see W2. (h) Frenzy (below 50% HP: +40% fire rate, 10% LS): already rich option.
**Price** (both 4.8k, both Armor/health colour, both upgrade Bullet LS, so spikes/slot/sell chain are identical; the difference is pure effect):
- Leech: +15 pts bullet LS over BL (13 -> 28), +28 spirit LS (new on top of Overflow 13/23 and Rend 10), +180 HP, +12 spirit, +12% weapon damage, anti-heal mitigation. Passive, no button.
- VB: bullet LS 13 passive, 83% for 5 s (13+70) with +34% fire rate and 75% reload, +100 HP, +10% bullet resist, +6% weapon dmg. Active (extra button), cooldown unknown (not in items_full; test `cds` is unreliable, measure by casting i1 twice and watching `mods`).
**Kit maths** (B = bullet damage/s to heroes before bounces, S = spirit-type damage/s: cards, Tesla, Mercurial bullet magic, Full Auto magic; R = bounce multiplier 1 / 1.65 / 2.3 for 1 / 2 / 3 targets IF bounce damage heals, unknown; assume VB cooldown 30 s and a 30 s continuous window):
- Leech marginal over holding Bullet LS: bullets +0.15 x B x R x 30 = 4.5BR; spirit +0.28 x S x 30 = 8.4S.
- VB marginal over Bullet LS: bullets (0.83 x 1.34 x 5 - 0.13 x 5) x B x R = 4.9BR in the 5 s window, plus the 34% fire rate raising S a little; spirit 0.
- So bullets alone are a tie over 30 s (4.5 vs 4.9 BR); Leech wins whenever S is more than about 5% of B (any realistic Wraith: cards 85+ every 0.6 s, Tesla chains, Mercurial and FA magic bullets), and the more so the longer the fight. VB wins the first 5 s: 5.6BR vs Leech 1.4BR + 1.4S, i.e. it is the better emergency button only if you can spend the 5 s shooting at heroes, and if the VB cooldown is much longer than 30 s its 30 s total drops below Leech's. Reload +75% and +34% fire rate also help W6.
- Ricochet matters twice: if bounce damage heals, both scale by R and Leech's absolute lead grows; if only the primary hit heals (R = 1 for lifesteal), Leech's 28% is wasted on the 65% bounces and VB's burst is relatively better only in 2-3 target clusters (damage grows, healing does not). That is the unknown to measure first.
- Anti-heal (Toxic -35, Inhibitor -40, Healbane -35, Spirit Burn -70, Decay -50): VB lifesteal is scaled down by it, Leech "reduces the effect" (amount not in data). UNSUPPORTED to measure (no `eheal`); kit maths favours Leech by an unknown margin. Wraith's own Inhibitor does not help her heal.
- Overflow already supplies 23% spirit LS when charged and Rend 10%, so the extra spirit LS from Leech has diminishing worth only if lifesteal caps (no cap known). Test P3 shows whether Leech's spirit part adds real HP.
**Tests (all supported with existing ops; scripts in section 4)**:
- P0 imbue probe (is Mercurial live?), P1 bounce-heal attribution, P2 sustain A/B at 1/2/3 targets x accuracy 100/50, P3 spirit-part isolation, P4 survival under `incoming`.
**Prediction (to be falsified)**: Leech >= VB on net HP over 30 s at every target count; VB ahead only in the first 5 s window and for Wraith's reload/fire rate; if P1 shows bounces do not heal and S/B is small, VB's lead in 2-3 target bursts could flip the 5 s window but not the 30 s one.
**Decision**: keep Leech as core. Confidence: medium on kit maths, untested. Allowed update: if P2 shows VB >= Leech +15% net HP in the 30 s window at 2 of 3 target counts with CV under noise, propose swapping to VB with the concrete trigger "bounce heals don't land / fights are short bursts" as a Counters-style situational swap box "Vampiric Burst: Swap for Leech when ..."; otherwise do not add VB (an extra button for a tie is a playstyle burden). "Both" rejected on price (slot, 6.4k, delays Inhibitor/Silencer) unless P4 shows deaths with 2 sustain items still being 4+ s short.
**Grade (H)**: CALCULATED (kit maths: bounce-heal attribution, VB cooldown and the bullet:spirit split are unknown). Confidence 50%. Wrong if P1 shows bounces do not heal AND fights are short bursts, or VB's cooldown is under ~25 s. Not real-game performance.

### W2 Mid-game sustain gap (20k-39k)
**Remedies**: (a) accept (current). (b) Buy Leech before Mercurial (29.6k): Leech is still an upgrade of Bullet LS only at 4.8k, but Overflow then needs a fresh Spirit LS (+1.6k) or is delayed; costs the spirit spike (Mercurial is the 9.6k spirit step). (c) Fury Trance (3.2k) as a lane/mid item: sold later, which RULES say to avoid. (d) Healing Booster/Extra Regen: Wraith has Hearts; rule skips regen items on heroes with built-in healing. (e) Playstyle: farm until 29.6k, fight with Reactive Barrier + TP. (f) Counters menu already covers dying.
**Price**: (b) delays Mercurial/Overflow by 4.8k each (damage spike later), (c) 3.2k that is sold, wasting about 3.2k in a 12-slot-locked early game.
**Test (supported)**: checkpoint loadouts 24k (Ricochet, SL, BL, Enduring, RB, Shredder + early stack) and 30k (+Mercurial) vs variant order (Leech inserted before Mercurial, Overflow after). Metric: net HP and time-to-zero under `incoming gun 120` + `incoming spirit 60` while firing at a 50% accuracy bot; deltas must exceed A/A noise. Script T6.
**Decision**: leave alone unless T6 shows death-time at 30k within noise of the 39k Leech loadout (then the build is not gap-limited) or clearly worse (then propose option b as a situational "lost lane / behind" reorder, not core). Confidence low; likely "leave alone" (rules: damage spike first, then 4.8k health, mobile heroes may delay it).
**Grade (H)**: CALCULATED (soul curve maths). Confidence 40%. Wrong if T6 shows the 30k loadout dying well before the 39k one under the same incoming profile.

### W3 Teleport/ult interrupt (silence, slowing hex, stun) and reach of Telekinesis
**Remedies**: (a) Dispel Magic (Counters, already menu), (b) Unstoppable (Counters), (c) Reactive Barrier (core, only triggers after the stun), (d) Warp Stone (swap, replaces Enduring Speed: 11 m straight-line blink + 30% bullet resist 6 s, instant vs PM's 0.75 s), (e) Enduring Speed (core; 25% slow resist, +2 m), (f) ability order: PM T2 barrier at point 10 (already), (g) positioning: teleport before being focused, never inside enemy CC range, use PM to dodge not to chase, (h) target selection: Telekinesis the carry only when their CC is on cooldown, (i) Debuff Reducer / Veil Walker not relevant.
**Utility->damage model**: no remedy converts to damage directly; they convert to "alive for the next 5 s". Warp Stone: instant blink avoids a 0.75 s window where a Slowing Hex (3 s duration [U]) or a stun can cancel PM; gain exists only if the enemy CC is projectile/cast-time and lands in that window; disappears vs hitscan or point-blank CC, and costs the Enduring Speed slot (kiting speed) which the rules call core.
**Test**: UNSUPPORTED (no CC op, no enemy casts). Needed ops: `ecc silence|slow|stun <s>` on the player and a metric "PM completion rate / time to leave 25 m". Decide from kit maths.
**Decision**: leave core alone; keep Dispel/Unstoppable as menu items with the existing triggers (kit-derived and consistent with the user note). Add nothing. Confidence: medium (CC-heavy lobbies would change this; flagged untested).
**Grade (H)**: UNTESTABLE-HIGH-RISK (CC timing, enemy reactions; see A2.4, which supersedes the reasoning here: Warp Stone is also a movement item, so Slowing Hex blocks it too). Confidence 45% (capped). Verdict limited to keep core + situational notes.

### W4 Focus burst / standing still
**Remedies**: Counters menu items (Metal Skin, Plated Armor, Spirit Resilience, Counterspell), Inhibitor (already), Enduring Speed/RB, positioning behind cover with Ricochet bounces, TP escape, Full Auto only when covered.
**Test (supported, resist path)**: `incoming gun 150` / `incoming spirit 150` with 5 s/10 s windows, compare time-to-zero with Metal Skin / Plated Armor / Spirit Resilience given in place of Silencer (the sell chain's counters slot), to price each counter's survival seconds; not a decision on the build, a price list for the menu. Because `incoming` is per-tick, Plated Armor deflect and Metal Skin per-bullet effects are unreliable (GAPS 6): scoring limited to flat resist items.
**Decision**: leave alone (menu already names the trigger per threat). Confidence medium.
**Grade (H)**: CALCULATED (flat-resist price list only; `incoming` is per-tick so burst and Plated/Metal Skin effects are not represented). Confidence 55%.

### W5 Card Trick economy vs accuracy
**Remedies**: (a) accept, (b) more bullets per second (fire rate stack already), (c) crits (6 vs 4) via headshots/Lucky Shot-type items, (d) melee weave (light 10, heavy 25 = ~6 bullet hits each) as a playstyle, (e) Ricochet bounces (if they count as hits, that is up to 2.3x cards at 3 targets), (f) rely on the Mercurial/Quicksilver timer (14-18 s charge) for cards regardless of accuracy.
**Test (supported)**: T5: accuracy 1.0 / 0.5 / 0.4 body-only, 30 s fire, spam `cast 1`; metric = Card Trick damage events per 30 s (cards produced) and resource per hit; plus 3 enemies vs 1 to see if bounce hits add card resource. `cast melee` mixed block for the melee weave (light/heavy not distinguishable: UNSUPPORTED for the 25-resource heavy).
**Decision**: not decided; likely "playstyle note" outcome only if T5 shows bounces count (then positioning to cluster), else leave alone. Playstyle notes are kept out of data.js per rules, so this feeds the Council note only. Confidence low until T5.
**Grade (H)**: none yet (cannot determine until T5). Any later T5 result is MEASURED only for the Sandbox's hit model, not real aim.

### W6 Ammo/reload with stacked fire rate
**Remedies**: (a) accept (Mercurial refills on Card Trick every 14 s, +20% clip), (b) Extended Magazine 800 / Titanic (needs a slot; weapon colour), (c) Vampiric Burst 75% reload on use (W1), (d) Active Reload (4 builds, timing press) swap, (e) Full Auto T3 earlier (point 11 now; moving costs Card Trick T2/T3), (f) playstyle: throw a card to refill (Mercurial CD 14 s) before the reload.
**Price**: (b) one of the 12 slots (Extended 0.8k, Titanic 1.6k) for a clip bonus; (d) fresh T2 late is against rules; (e) delays Card Trick T3/Jokers.
**Test (supported)**: T4: full loadout, 40 s continuous in chunks (`fire 3` / `cast reload 2.5`), count GunFired and damage; vs loadout minus fire-rate items to show reload-limited dps; report shots per mag via acclog and effective dps incl. reload. Requires P0 (Mercurial refill only works if imbue live).
**Decision**: leave alone unless T4 shows reload downtime above 25% of fight time with the full stack, then propose cast-card refill as playstyle first, VB second. Confidence low-medium.
**Grade (H)**: CALCULATED until T4 runs (then MEASURED, sandbox not live game). Confidence 45%.

### W7 Single target / bullet resist
**Remedies**: Bullet Resist Shredder (1.6k, cut Round 14), Armor Piercer (replace Inhibitor/Silencer slot, 6.4k), Escalating Exposure (rich box), Hollow Point, more spirit share (Wraith's cards/Tesla/Mercurial/FA are spirit).
**Test (supported)**: `enemies 1` vs `enemies 3 250`, `eresist gun 25` and `eresist spirit 20` (late-game realistic), arms: current vs +Bullet Resist Shredder (swap Silencer) vs +Armor Piercer; metric = damage dealt per 20 s (damage csv by type), 5 reps.
**Decision**: leave alone unless Shredder/Piercer beats the replaced item by >=15% in resist runs; then situational "enemy stacked bullet armor" box (trigger named). Confidence low.
**Grade (H)**: CALCULATED. Confidence 40%. Wrong if T7 shows a shred item beating the replaced slot by >= 15% at realistic resists.

### W8 Early lane/farm/snowball
**Test**: UNSUPPORTED for farming (no NPC/camp op, GAPS 21). Lane damage vs hero partially supported (p8k/p12k loadouts vs bot at fetch 350, damage only). **Decision**: leave alone; Monster Rounds is sold on a defined trigger, Tesla/Cards/Ricochet cover waves, Extra Regen box covers lost lane. Confidence medium (build source: Strenngth/tracklock per changes log).
**Grade (H)**: CALCULATED (no farm measurement possible, GAPS 21). Confidence 50%.

### W9-W11 Downtime, chasing, finishing: leave alone
Cards and gun fill ability downtime; range 500 m for cards and the TP cover chasing; no execute exists in the kit and none is needed at this soul curve. Confidence medium. Not tested (nothing to test).
**Grade (H)**: CALCULATED (kit text). Confidence 60%.

### W12 Lifesteal redundancy (spirit side)
Spirit LS pieces if additive: Rend 10 + Overflow 13 (+10 charged) + Leech 28 = 51-61% of spirit damage versus 28% on bullets. P3 below isolates Leech's spirit half; if its marginal HP is small because spirit damage is mostly Tesla (15% proc) and cards at 0.6 s, W1 flips toward VB. Decision tied to W1.
**Grade (H)**: cost part CALCULATED (deterministic, see A2.6; Leech is 4.8k at 39.2k because Overflow consumed Spirit Lifesteal), confidence 90%; value part follows W1 (CALCULATED, 50%).

### W13 Imbue dependency
Flagged BLOCKED until P0. If Mercurial/Surge are inert in the Sandbox, every measurement of spirit damage is undercounted; arms stay valid for the lifesteal difference only if S is reported separately.
**Grade (H)**: BLOCKED (instrument gate P0); no grade until P0 runs.

## 4. Runnable tests (existing ops only; one op per line, `#` comments; hero name `Wraith`, enemy `Haze`; all blocks start `hardreset`, end with `mark none`)
Common loadout L (final items, no sustain slot): upgrade_blitz_bullets, upgrade_magic_storm, upgrade_chain_lightning, upgrade_ethereal_bullets, upgrade_ricochet, upgrade_cardio_calibrator, upgrade_vex_barrier, upgrade_spellslinger_headshots, upgrade_tech_overflow, upgrade_inhibitor, upgrade_proc_silence (11 items). Arms add one slot: A_leech = upgrade_damage_recycler; B_vb = upgrade_surging_power; C_bl = upgrade_vampire (baseline, price-equal filler not available: 13% Bullet LS component, report as "no 4.8k item"); D_none = nothing.

**P0 imbue probe** (decides W13/all spirit measurements)
```
setup Wraith Haze
hardreset
give upgrade_quick_silver
mods
cast reload 2.5
cast 1 0.5
mods
cds
```
Pass = a Quicksilver/Mercurial-type modifier name appears after the Card Trick cast, and `acclog` shows the next bullets with extra magic damage. Fail = tag all Mercurial/Surge results UNVALIDATED.

**P1 bounce-heal attribution** (key unknown for Ricochet+Leech)
Arms: [Bullet LS only] vs [Bullet LS + Ricochet]; targets 1 vs 3. Heal measured by lowhp (heals not capped) so Overflow/Hearts excluded (do not cast 1).
```
hardreset
give upgrade_vampire
give upgrade_ricochet            # omit in the no-bounce arm
enemies 3 250 1                  # use "enemies 1" for the 1-target condition
fetch 350
aimoff 5.5 3
accuracy 1 0
lowhp 40
healreset
mark P1_<arm>_<n>
cast reload 2.5
fire 3
cast reload 2.5
fire 3
healsum
mark none
lowhp 0
```
Metric: heal per damage dealt, split by victim. If heal/damage falls by about 1 - (1 + 0.65*2)^-1 x (bounce share) when bounces are present, bounces do NOT heal; if it stays constant, they do. 5 reps.

**P2 sustain A/B (W1 main test)**: arms A_leech, B_vb, D_none; conditions targets 1/2/3 x accuracy 1.0 and 0.5 (body only). Window 30 s, rotation from playstyle: `cast 3` (Full Auto) at t0, VB arm `cast i1` at t0 (active item order = give order, assumed), fire in 3 s chunks with reloads.
```
hardreset
give <L items>
give <arm item>                  # omit for D_none
enemies <n> 250 1
fetch 350
aimoff 5.5 3
accuracy 0.5 0
lowhp 40
healreset
mark P2_<arm>_<n>_<acc>_<rep>
cast 3 0.2
cast i1 0.2                      # VB arm only
cast reload 2.5
fire 3
cast 1 0.3
cast reload 2.5
fire 3
# repeat the fire/reload pair until 30 s elapsed (about 5 pairs)
healsum
mark none
lowhp 0
```
Order per rep set: A B D D B A, then reversed; first block per session discarded (warm-up bias). Primary metric: healDiffObserved minus D_none block (marginal HP), plus damage by type (B:S split) from the damage csv. Pre-registered: win needs >=15% marginal-HP difference with non-overlapping min/max across 5 reps.

**P3 spirit-half isolation**: arms [Leech] vs [Leech minus spirit] cannot be built from items; instead compare marginal HP of Leech vs a Bullet-LS-only block, and split by damage type: heal / bullet damage vs heal / spirit damage (needs the damage csv type per hit). If heal per spirit damage in the Leech arm is not above the D_none arm, Leech's spirit 28% is not active (flag, possibly bug) and W1 shifts toward VB.

**P4 survival under incoming** (the real purpose of sustain)
```
hardreset
give <L items>
give <arm item>
fetch 350
aimoff 5.5 3
accuracy 0.5 0
hurtme 500                       # start about 70% HP, no lowhp clamp
healreset
incoming gun 120
mark P4_<arm>_<rep>
cast 3 0.2
cast i1 0.2                      # VB arm only
cast reload 2.5
fire 3
cast reload 2.5
fire 3
# continue to 25 s or death
incoming spirit 60               # second stage after 10 s
healsum
incoming off
mark none
```
Metrics: time to zero HP (or HP at 25 s), net HP. `incoming` disables the heal-to-full safety so death is reachable; if the player never dies in 25 s raise dps. Tick-based incoming (GAPS 6) makes this valid for lifesteal and flat resist, not for burst or on-hit items.

**T4 ammo/effective dps (W6)**: full loadout including each arm item, 40 s in `fire 3`/`cast reload 2.5` chunks at accuracy 1.0; compare against loadout without Swift Striker/Overflow/Ricochet to show reload-limited dps; add arm B_vb with `cast i1` at t0. Metric: GunFired count (acclog), damage per second incl. reload, mags per 40 s.

**T5 card economy (W5)**: accuracy 1.0, 0.5, 0.4 (`accuracy p 0`), `enemies 1` vs `enemies 3 250`, 30 s `fire 3`/`cast 1 0.3` loops without lowhp; metric = Card Trick damage events and thrown cards per window from damage csv; confirm whether bounce hits add card resource by 1 vs 3 targets at equal primary hits.

**T6 mid-game gap (W2)**: loadouts at 24k, 30k from the walk (give final items only, GAPS 22) vs Leech-first order variant (L30 + Leech - Mercurial - Overflow); run P4 on each; compare time-to-zero and net HP.

**T7 resist/shred (W7)**: P2-style damage windows with `eresist gun 25`, `eresist spirit 20`, arms current vs swap Silencer -> upgrade_bullet_resist_shredder vs upgrade_aprounds; 1 and 3 targets.

**P-CC0 (new, gate for WC1/WC2; existing ops only, expected to fail)**: do enemy-held on-hit items apply their debuffs through `incoming`? If yes, the Sandbox gains a silence and an anti-heal source on the player without new ops.
```
setup Wraith Haze
hardreset
eitem upgrade_proc_silence       # then repeat with upgrade_inhibitor, upgrade_toxic_bullets
basemods
incoming gun 300
mark PCC0_<item>
wait 1
mods
wait 2
mods
wait 3
mods
incoming off
mark none
```
Pass = a silence / Inhibitor / Toxic modifier on the player. If Silencer passes: run `cast 2 1` under it and compare `pos` before/after vs control (PM blocked or not = first CC data point; also tells whether Reactive Barrier fires on it via `mods`). If Inhibitor/Toxic pass: rerun P2/P4 with the debuff on, which closes WC2 (Leech vs VB under anti-heal). Fail = WC1/WC2 stay UNSUPPORTED.

**P-PM (new, cheap)**: `hardreset`, `pos`, `cast 2 1`, `pos`, `mods` with unlock 7: confirms the teleport moves the player in the Sandbox and that the T2 barrier modifier appears; baseline for any future CC test. Low decision value; run only with P-CC0.

**UNSUPPORTED**: anti-heal on the player (need `eheal`), CC/interrupts on TP/Telekinesis (need `ecc`), mobile/fleeing targets (need `emove`), farming/NPC (need camp spawn), allies, shoot-back, kill stacks, light vs heavy melee for the 25-resource heavy hit.

## 5. Decisions summary (re-ranked by chain frequency x lethality; every verdict graded per section H)
| rank | item | chosen | cost | tests | verdict | grade | conf. | what would make it wrong |
|---|---|---|---|---|---|---|---|---|
| 1 | WC1 / W3 PM denial (silence, hex, stun) | keep core; menu stays; reviewer notes: Dispel scope unverified (Divine Barrier verified), Unstoppable must be used before a stun, Hexafoil Ward candidate | 0 | UNSUPPORTED; P-CC0 / P-PM probes | KEEP + situational notes | UNTESTABLE-HIGH-RISK | 45% | PM not movement-based; silence blocks items; CC deaths dominate |
| 2 | WC2 anti-heal on lifesteal | keep Leech (only anti-heal answer in build) | 0 | UNSUPPORTED unless P-CC0 passes | KEEP | CALCULATED | 50% | Leech's mitigation tiny and VB wins P2 |
| 3 | W1 Leech vs Vampiric Burst | keep Leech; VB only if P2 hits +15% at 2 of 3 target counts | 0 now | P0-P4 designed, not run | KEEP (provisional) | CALCULATED | 50% | bounces do not heal (P1) and fights are 5 s bursts; VB cooldown short |
| 4 | WC3 gun denial (Metal Skin etc.) | playstyle: cards and target swap | 0 | none needed | NOTE | CALCULATED | 60% | no banked cards when Metal Skin lands |
| 5 | W4 focus burst | leave; menu | 0 | incoming price list (flat resist only) | LEAVE | CALCULATED (incoming is per-tick, GAPS 6) | 55% | burst, not sustained, kills her (untestable) |
| 6 | WC4 silence on imbue hub | leave; do not reload under silence while Mercurial bullets remain | 0 | none | NOTE | CALCULATED | 55% | Mercurial buff ends on silence |
| 7 | W2 mid gap 20-39k | leave | 0 | T6 | LEAVE | CALCULATED | 40% | T6 shows 30k loadout dies far sooner than 39k |
| 8 | W6 ammo | leave; card throw to refill | 0 | T4 | LEAVE/PENDING | CALCULATED | 45% | reload downtime > 25% in T4 |
| 9 | W5 card economy | note only if T5 shows bounce hits count | 0 | T5 | PENDING (cannot determine) | none yet | n/a | n/a |
| 10 | W7 bullet resist | situational box only if T7 >= 15% | 0 | T7 | LEAVE | CALCULATED | 40% | T7 win |
| 11 | WC5 Telekinesis peel | leave | 0 | UNSUPPORTED | LEAVE | UNTESTABLE-HIGH-RISK | 50% | n/a |
| 12 | W8 farm | leave | 0 | UNSUPPORTED | LEAVE | CALCULATED (no farm data) | 50% | measured farm deficit |
| 13 | W9-W11 | leave | 0 | n/a | LEAVE | CALCULATED | 60% | n/a |
| 14 | W12 Leech/Spirit LS cost | correct the changes-log claim (4.8k, not 3.2k); no build change | 0 | none (shop maths) | KEEP, note | CALCULATED | 90% | shop credits differently |
| 15 | W13 imbue dependency | BLOCKED until P0 | 0 | P0 | BLOCKED | none | n/a | n/a |
No verdict here is MEASURED: none of the designed tests has been run, so nothing may be presented as real-game performance.

## 6. Re-sweep of the (unchanged) build
No change proposed, so no new weaknesses introduced. If the W1 swap to VB were adopted: slot, spikes (health 4.8k at 21.6k, Leech/VB both 4.8k at 39.2k) and sell chain identical; new weaknesses = +1 active button, no spirit LS (-28% spirit sustain and -12 spirit, -6% weapon damage vs Leech), no anti-heal mitigation, but +10% bullet resist, +34% fire rate and faster reload. Note for reviewer: the Round 13 change note claims Leech is a 3.2k upgrade; with Overflow consuming Spirit Lifesteal it is 4.8k (walk 34.4k -> 39.2k), still the same price as Vampiric Burst.

Revision 2 re-sweep (situational notes proposed in A2, nothing in core changed): (a) If the reviewer moves the hex/silence line from Dispel Magic to Divine Barrier: Divine Barrier is a T4 (6.4k fresh, or 3.2k + Guardian Ward path) in a Counters slot that sells Swift Striker: it is pricier and later than Dispel (3.2k), so the earliest answer to a hex shifts later; no spike or slot change. (b) Hexafoil Ward as a menu line: 3.2k in the same Counters slot; new weakness = one block per fight and it may be spent on a minor debuff. (c) Warp Stone (not proposed): would take Enduring Speed's slot and lose 25% slow resist and +2 m/s, i.e. trade walking escape for a second blink that hex also blocks; rejected. No new serious weakness, so no second B-F loop.


## I. Practicality (WEAKNESS_PROCESS section I; added 2026-10-24, appended, nothing above changed)
Sources added: game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` (citadel_weapon_wraith_set, ability cooldowns/upgrades) and `heroes.vdata` (level table, per-level growth); data.js walk (prac/out/walk_wraith.txt, 0 flags). Level table: unlocks at 0 / 500 / 1.4k / 3.2k souls, 1 point at every other level to 48.6k (32 points; tier costs 1/2/5 [U, consistent]). Time: ~7k at 8:00, ~1k/min after (late times are upper bounds).
Weapon: 52 rounds, 5.64 per bullet (+0.14 per level), 0.0945 s per shot (10.6/s), reload 2.82 s. Kit numbers missing from hero_wraith.txt (they fill the A2.1 [GAP]s): **Project Mind cooldown 46 s, T3 = -32 s (14 s)**; Full Auto cooldown 45 s (T1 -20 s); Telekinesis 150 s (T2 -45 s).

### I.1 Gun economy (magazine vs fire rate) - main finding
Model: 20 s of continuous fire on a target, fight buffs on (Surge on Card Trick use, Quicksilver/Mercurial buff, Overflow charged), Quicksilver/Mercurial refill thrown when the magazine empties, fire rate and clip % additive [U]. b = one base bullet incl. level; FA = Full Auto cast at t0.

| souls | current: mag / shots/s / % of 20 s reloading / damage | alt: Extended -> Titanic instead of Rapid Rounds -> Swift Striker | gain |
|---|---|---|---|
| 5.6k, no FA | 52 / 12.7 / 38% / 156 b | 104 / 10.6 / 14% / 206 b | +32% |
| 5.6k, FA T2 (no unlimited ammo yet) | 163 b, 42% reloading | 234 b, 14% | +44% |
| 16.8k Ricochet, no FA | 52 / 17.8 / 41% / 208 b | 104 / 15.7 / 14% / 307 b | +48% |
| 16.8k, FA T3 (unlimited 8 s) | 323 b | 383 b | +19% |
| 29.6k Mercurial, no FA | 62 / 19.0 / 28% / 287 b | 114 / 16.9 / 14% / 344 b | +20% |
| 53.6k full core, no FA | 62 / 21.7 / 28% / 373 b | 114 / 19.6 / 14% / 450 b | +21% |
| 53.6k, FA T3 | 470 b | 560 b | +19% |
| 3 s trade at 16.8k | 52 b (mag empty at 2.9 s) | 54 b | +4% (tie at about 2 s) |

Outside Full Auto, Wraith spends 28-42% of a fight reloading at every checkpoint, above the W6 trigger (25%). Every fire-rate item (Swift, Ricochet, Overflow, Mercurial buff, Surge, FA) only shortens the magazine; reload stays 2.82 s. Swift Striker and Titanic Magazine are the same tier, colour and price (0.8k component + 1.6k), so the swap keeps every spike (gun 4.8k at 5.6k), slot and sell. Side effects: more sustained hits per second (+20-30%) means more card resource (4 per hit), more Tesla procs, and the build-up items become reachable: Silencer needs ~97 hits (1.04/shot) and Inhibitor ~130 (0.77/shot) [U: 100 threshold, decay rules]; neither fills inside one 62-round magazine, Silencer can inside 114. Costs: -0.75 m/s sprint, about 5% less in the first ~2 s of a trade.
This supersedes W6 remedy (b) ("Titanic needs a slot"): it is a same-slot swap.
Decision: top candidate core swap (Rapid Rounds -> Swift Striker becomes Extended Magazine -> Titanic Magazine); do not change data.js until PR-W1 measures it, then put it to the Council with the result. Grade: CALCULATED (game-file magazine, cycle and reload; assumptions as stated; real fights have pauses where reloads are free, which pulls the gain toward the 2-3 s trade case). Not real-game performance. Confidence 55% that it is better in real play. Wrong if: fights are mostly 2-3 s peeks; fire-rate or clip bonuses do not add as assumed; PR-W1 shows no gain above noise.

### I.2 Ability points vs item timing (escape)
Order 1132341322314424: Card Trick T1 0.2k, T2 3.2k, T3 16.1k; Full Auto 0.5k, T1 1.4k, T2 4.6k, T3 (unlimited ammo) 11.0k; Project Mind 1.4k, T1 5.3k (+15 m), T2 6.8k (barrier), **T3 (14 s) 32.1k**; Telekinesis 3.2k, T1 17.4k, T2 20.6k, T3 48.6k.
Items fit (Quicksilver 8.0k, Surge 10.4k, Mercurial 29.6k after Card Trick T2). Problem: the only escape is on a 46 s cooldown until 32.1k (~33 min), so the A2.2 counter "bait the cooldown" works for most of the game; it also feeds WC1.
- ALT-W1 = 1,1,3,2,3,4,1,3,2,2,3,1,**2**,4,4,4: Project Mind T3 at 24.6k (7.5k earlier); Telekinesis T1/T2 move to 26.9k/32.1k (ult 150 s instead of 105 s and -100 slam damage for ~11k).
- ALT-W2: Project Mind T3 at 16.1k, Card Trick T3 to 24.6k (loses improved suits, Jokers and +75 +0.5x Hearts heal for 8.5k): dearer.
Effect: Project Mind casts available per 2 min rise from ~2.6 to ~8.6 once T3 is in. Decision: propose ALT-W1 to the reviewer (ability-order note, not applied). Grade: cooldowns CALCULATED (game files); survival value UNTESTABLE-HIGH-RISK (escape timing, enemy reactions). Confidence 45%. Wrong if Telekinesis peel is Kieran's main survival tool, or the game files are out of date.

### I.3 Spike timing vs survivability (delaying health; escape countered)
Current: gun 4.8k at 5.6k, spirit 4.8k at 10.4k, Ricochet 16.8k, health 4.8k at 21.6k (~22:40). Kieran's rule (farming builds may rush Ricochet before health; greens straight after) is met. HP = 730 + 35 per level.

| ordering | at 16.8k | Ricochet at | at 21.6k |
|---|---|---|---|
| A current | 1,500 HP, no lifesteal, no barrier | 16.8k | 1,785 HP, 13%/13% lifesteal, Enduring Speed |
| D Sprint -> Enduring Speed + Reactive Barrier first | 1,500 HP + ~370 barrier on stun/silence (+25% vs a CC opener), +2 m/s, 25% slow resist | 20.0k (3.2k later) | as A, Ricochet ~3 min later |
| B all greens + Reactive Barrier first | 1,680 HP + lifesteal + ~370 barrier (~+37%) | 23.2k (6.4k later) | |

Countered case: Project Mind (0.75 s, 46 s) is denied by hex/silence/stun in nearly every lobby (A2.2). Then current Wraith at 16.8k has 1,500 HP and nothing else; Enduring Speed does not help against silence/stun; lifesteal needs her to keep shooting. Reactive Barrier (1.6k) triggers on exactly the CC that removes her escape (stun, silence, sleep, immobilize; hex [U]). Ricochet has no components, so 10.4k -> 16.8k is ~6.4 min of saving with no power gain; D spends 3.2k of that gap.
Decision: keep A as core (rule-consistent; Ricochet's farm speed is real but unmeasurable here). Situational note candidate: "Enemy has 2+ stuns, silences or hexes: Sprint Boots -> Enduring Speed and Reactive Barrier before Ricochet". Grade UNTESTABLE-HIGH-RISK, 40%. Wrong if: Ricochet's farm gain is small (then D is nearly free), or Reactive Barrier does not trigger on hex/movement-silence (then D covers stun/silence only).

### I.4 Buttons and new-player load
4 abilities (Card Trick is spam with resource and 2 charges); no core item actives (Reactive Barrier, Inhibitor, Silencer, Mercurial are passive/proc). Counters actives (Metal Skin, Unstoppable, Dispel) and rich (Capacitor, Divine Barrier) optional. Low load. Keep. CALCULATED, 65%.

### I.5 Slot lock, core length, sell chain
9 slots at 23.2k, 10 at 24.8k, 12 at 53.6k. Core ends at 53.6k (~55 min at 1k/min): Inhibitor (45.6k), Rend (47.2k) and Silencer (53.6k) are late, so A2's PREVENT (Silencer) and SURVIVE (Inhibitor) layers are absent from most real games before ~45 min. Note for A2/WC1. Sells: Counters sell Swift Striker (if the Titanic swap is adopted, the Counters line needs a new sell; Tesla Bullets, upgradable to Capacitor in rich, is the natural one), Spellslinger sells Enduring Speed, Escalating Exposure sells Rend: no conflicts. CALCULATED, 65%.

### I.6 Forgiveness when behind
If behind, Ricochet slips and every green slips with it (all greens come after Ricochet); the Counters trigger is "Dying after Ricochet", so before 16.8k only the Losing-lane Extra Regen is named. Candidate (situational, same as I.3 D): "Dying before Ricochet: Enduring Speed and Reactive Barrier first". UNTESTABLE-HIGH-RISK, 40%.

### I.7 Farming
Strong and front-loaded: Tesla (5.6k; 15% proc, 33 + 0.19x per chain, 4 chains, 8 m), Monster Rounds (6.4k; +25% weapon damage vs NPCs), cards from NPC hits at 35% resource, Ricochet bounces (16.8k). The ammo finding (I.1) applies to camps too: same-slot Titanic would cut camp reload time similarly [U: small camps may die inside one magazine]. Measurement UNSUPPORTED (no NPC op).

### I.8 Tests (existing ops only; `setup Wraith Haze`, `aimoff 5.5 3`, `fetch 350`, `ekeep 1`, `ehp 50000`; A/A n=6 first, then ABBA n=6 per condition; effect must exceed 2 x A/A SD)
- PR-0 fire/reload probe: `hardreset; accuracy 1 0; mark pr0; fire 12; mark none; acclog`. Shots stop at 52 and the block ends early = `fire` ends at an empty magazine. Then all gun tests use cycles of [`fire 30` (ends at empty), `cast reload 2.82`] and score damage per elapsed second from mark to the end of the last reload; that counts real reload time for any magazine size without per-arm timing. If instead `fire 12` holds for 12 s with a gap and resumes, use `fire 20` directly. RUNNABLE.
- PR-W1 magazine vs fire rate (gates I.1). Give final items only. L5: A = upgrade_blitz_bullets + upgrade_chain_lightning; B = upgrade_titan_round + upgrade_chain_lightning; `unlock 3` (Full Auto T2, no unlimited ammo, as at 5.6k). L17: A = blitz_bullets, chain_lightning, non_player_bonus, quick_silver, magic_storm, ricochet; B = same with titan_round for blitz_bullets; `unlock 7` (Full Auto T3 from 11.0k). Conditions: no FA / `cast 3 0.2` at t0; `enemies 1` and `enemies 3 250`; `accuracy 1 0` and `accuracy 0.6 0`. Do not cast Card Trick (imbue confound, P0). 4 PR-0 cycles per block. Expected (CALCULATED, 1 target, 100%): L5 noFA A 156 b vs B 206 b; L17 noFA 168 vs 237; L17 FA 245 vs 272. Metrics: damage per elapsed second, damage in the first 3 s (burst), GunFired (acclog). Pass for a Council proposal: B ahead by more than noise in no-FA at both accuracies and not behind by more than 5% in FA or burst. RUNNABLE.
- PR-W2 build-up vs magazine: 53.6k core (final items) A vs B (titan_round for blitz_bullets), `enemies 1`, `accuracy 0.8 0`, cycles of [`fire 1`, `mods`] with `cast reload 2.82` when the magazine is empty; metric: time until a Silencer silence modifier appears on the bot. RUNNABLE (names, 1 s resolution).
- ALT-W1 and ordering D vs A: UNSUPPORTED (no per-ability tier op, no `ecc`, no NPC op).

### I.9 Regression (F) for the candidates
- Titanic for Swift: spikes, slots, colour and price unchanged; loses 0.75 m/s sprint and ~5% of the first 2 s; Counters line must name another sell; W1's VB comparison changes slightly (VB's +75% reload matters less with a 104-114 round magazine, so the Leech case gets stronger). No serious new weakness.
- ALT-W1: Telekinesis 150 s instead of 105 s for ~11k souls; WC5 peel slightly weaker. Acceptable if adopted; not applied.
- D (situational): Ricochet 3.2k later; farm slower for ~3 min. Only by trigger.

| problem | chosen | cost | grade | conf. |
|---|---|---|---|---|
| Reload-bound gun (28-42% reloading outside FA) | candidate swap Swift -> Titanic, pending PR-W1 | 0 souls, 0 slots | CALCULATED | 55% |
| Project Mind 46 s until 32.1k | propose ALT-W1 (reviewer) | Telekinesis T2 (-45 s) 11.5k later | CALCULATED + UNTESTABLE | 45% |
| Health at 21.6k when escape is countered | keep; situational RB + Enduring first vs 2+ CC | 3.2k Ricochet delay when used | UNTESTABLE-HIGH-RISK | 40% |
| Silencer/Inhibitor late and hard to fill | note to A2; helped by the Titanic swap | 0 | CALCULATED | 60% |
| Buttons, sells, farm | leave | 0 | CALCULATED | 65% |


## J. Item roles (WEAKNESS_PROCESS J; added 2026-10-24, appended, nothing above changed)
Sources: audit/items_full.json [i]; game files `gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata` [g] (cooldowns, scaling tags, imbue filters, modifier types) and `gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt` [l] (item text missing from items_full); audit/hero_wraith.txt [k]; walk prac/out/walk_wraith.txt (souls). Kieran 2026-10-24: Ricochet is not only a farm item; its fire rate helps long-fire abilities and its bounces hit extra enemies. Grades: C = CALCULATED, U = UNTESTABLE-HIGH-RISK, M = MEASURED (nothing here is measured). Fire-rate, clip and damage bonuses assumed additive [U], as in I.1.

### J.0 Game-file facts that fill earlier [GAP]s
- Vampiric Burst: cooldown 30 s [g] (W1 assumed 30 s: confirmed). Active text [l]: "Grants Lifesteal, Fire Rate, and Ammo. This added Ammo is not limited by your max magazine size." ActiveReloadPercent 75 = +75% of a magazine as extra rounds (39 at 52), not a reload.
- Dispel Magic active [l]: "Purge all non-ultimate negative effects currently applied to you. If any effects were removed, heal yourself and gain a move speed bonus. Cannot be used while Stunned or Slept." Cooldown 45 s [g]. The cleanse is verified, and it works while silenced or hexed.
- Silencer debuff [l]: "Your bullets reduce the target's outgoing spirit damage" (TechDamageReduction -25, 6 s per hit): works from the first bullet, no build-up needed.
- Spiritual Overflow: +13% ability duration, +13% spirit lifesteal, +6 spirit and +90 HP are always on (intrinsic modifier); only +25% fire rate, +30 spirit and +10% spirit lifesteal need the charge [g].
- Inhibitor's -30% is an all-damage multiplier on the target [g]. Ricochet's radius scales with range items (ETechRange) [g]; none in this build.
- Cooldowns [g]: Surge of Power proc 14 s, Metal Skin 24 s, Counterspell 23 s, Unstoppable 60 s, Divine Barrier 45 s, Capacitor 40 s.

### J.1 Item roles
| item (box, souls) | every effect [source] | what it feeds (abilities, phases, items) | matters from | grade |
|---|---|---|---|---|
| Rapid Rounds (early 0.8k, becomes Swift) | +9% fire rate [i] | lane gun damage, Full Auto bullets, card resource per second | at once | C |
| Extra Spirit (1.6k, becomes Surge) | +10 spirit [i] | cards +5.5 each (0.55x), Hearts heal +5, Full Auto magic per bullet | at once (Card Trick from 0.2k) | C |
| Swift Striker (2.4k) | +20% fire rate, +0.75 m/s sprint [i] | gun damage in every phase; Full Auto (T3 unlimited ammo from 11.0k turns fire rate into damage 1:1); the per-second rate of every per-hit effect: cards (4/hit), Tesla (15%/bullet), Overflow/Silencer/Inhibitor build-up, lifesteal; sprint for rotations, farm routes, walking out; the Counters sell | at once | C (fire rate), U (build-up semantics) |
| Tesla Bullets (5.6k) | 15% per bullet: 33+0.19x per chain, 4 chains, 8 m, 0.2 s proc cooldown [i/g]; upgrades to Capacitor | waves and camps, teamfight spread, spirit damage that Shredder/Rend and spirit lifesteal ride on; Ricochet bounces carry it ("applying any bullet procs" [l]) | at once | C; carry by bounces U |
| Monster Rounds (6.4k, sold 18.4k) | +25 weapon power and 25% bullet resist vs NPCs, OOC regen 1 [i] | camp and wave speed, tanking troopers | 6.4k-18.4k | C |
| Quicksilver Reload (8.0k, Card Trick imbue) | card charges over 18 s: +44+0.16x card damage, +10% fire rate 12 s, reloads on use [i/l] | reload source (I.1), fire rate, card burst | at once if the imbue is live (P0) | C |
| Surge of Power (10.4k, imbue, from Extra Spirit) | +28 spirit on Card Trick only; on cast +20% fire rate and +1.75 m/s for 8 s, full speed while shooting, 14 s [i/g] | card damage (+15 each), gun fire rate, strafing while in Full Auto (W4 "stands still"), escape speed when PM is down | at once | C |
| Ricochet (16.8k) | +18% fire rate always; each bullet bounces to 2 more enemies within 13 m for 65%, applying bullet procs [i/l] | (a) one target: fire rate only, about +12% damage over 20 s outside Full Auto (reload eats the rest; I.1 model about 206 vs 184 b) and +10% inside Full Auto T3 (8 s, unlimited ammo, so no reload loss; FA magic per bullet and Mercurial bonus ride on the extra bullets); (b) 2 or 3 enemies within 13 m: bullet damage x1.65 / x2.3 (teamfights, objectives, waves, camps); (c) bounced targets get the procs: Tesla, Spirit Shredder/Rend (-8/-7 spirit resist spread to the group for cards, Tesla, FA magic), possibly Silencer/Inhibitor build-up [U if build-ups count as procs]; (d) lifesteal on bounce damage [U, P1] and card resource from bounce hits [U, T5]; (e) farm speed | fire rate at once on any target; bounces from the first fight or camp with 2+ targets in 13 m | C (fire rate, bounce %), U (procs, lifesteal, cards on bounces) |
| Spirit Lifesteal (18.4k, becomes Overflow) | 13% spirit lifesteal, +6 spirit, +90 HP [i] | sustain on cards/Tesla/FA magic | at once | C |
| Bullet Lifesteal (20.0k, becomes Leech) | 13% bullet lifesteal, +90 HP, +6% weapon damage [i] | sustain, damage | at once | C |
| Sprint Boots > Enduring Speed (21.6k) | +2 m/s, 25% slow resist, OOC regen 2 [i] | walking escape when PM is down (WC1 SURVIVE), kiting, chasing, rotations; nothing vs silence/stun | at once | C |
| Reactive Barrier (23.2k, from Grit) | 325+1.8x barrier on stun, chain, immobilize, sleep, silence; 55 s [i] | survives the CC that stops PM (WC1); spirit scaling ties it to Overflow/Leech spirit; upgrades to Indomitable | at once, when CC'd | C (trigger list), U (hex trigger) |
| Spirit Shredder (24.8k, becomes Rend) | bullets: -8% spirit resist 8 s and +10% spirit lifesteal against that target for her AND her allies [l] | every spirit source of hers; allies' spirit damage and sustain (team role); spread by Ricochet | at once | C; ally part U (no ally op) |
| Mercurial Magnum (29.6k) | card charges over 14 s: +60+0.16x card damage, +22% fire rate 12 s, reload on use, +20% clip, +7 spirit; bullets +20+0.38x magic until the next reload [i/l] | reload (W6/I.1), fire rate, magic per bullet: a bigger magazine means more empowered bullets per refill (so it gains from Titanic) | at once if the imbue is live | C |
| Spiritual Overflow (34.4k) | always: +13% ability duration, +13% spirit lifesteal, +6 spirit, +90 HP; charged (1.08 per shot, 5 s build-up): +25% fire rate, +30 spirit, +10% spirit lifesteal for 15 s [g] | always-on duration: Full Auto 8 -> 9.0 s (+13% FA bullets), PM T2 barrier 5 -> 5.7 s, Telekinesis lift/debuff; Surge speed and Reactive Barrier windows if item durations take it [U]; charged half: gun, cards, sustain | always-on half at once; charge needs ~93 hits inside the window (PR-W2) | C (always-on), U (charge) |
| Leech (39.2k) | 28% bullet and 28% spirit lifesteal, +12% weapon damage, +12 spirit, +180 HP; reduces enemy healing reduction by an unstated amount [i/l] | sustain (WC2); over Bullet Lifesteal: +15/+28 lifesteal, +6% weapon damage, +12 spirit (cards, barriers), +90 HP | at once | C; anti-heal size GAP |
| Inhibitor (45.6k) | always: +10% weapon damage, +150 HP; build-up 0.77/shot: target -30% all outgoing damage and -40% healing for 5 s [i/g] | +10% damage and HP even unfilled; survival vs the hero she shoots; anti-heal on enemy healers (offence vs sustain heroes) | always-on half at once; debuff needs ~130 hits in 5 s | C (stats), U (fill) |
| Silencer (53.6k) | build-up 1.04/shot: 2.5 s silence, 10 s immunity; every bullet: target -25% outgoing spirit damage 6 s; +12% spirit resist [i/l/g] | WC1 PREVENT vs ability CC (late); anti-spirit defence from the first bullet; spirit resist | defence at once; silence needs ~96 hits in 5 s | C, U (fill) |
| Counters: Dispel Magic | purge all non-ultimate negative effects (silence, hex/movement silence, slows, anti-heal); if anything was removed 250 heal and +2 m/s 3 s; 10% spirit resist; 45 s; not usable while stunned or slept [l/g] | WC1 RECOVER (PM free again), WC2 RECOVER (anti-heal), escape speed | at once | C (text), U (timing) |
| Counters: Spirit Resilience | 30% spirit resist, +15% below 50% HP, OOC regen 3 [i] | survival vs spirit | at once | C |
| Counters: Metal Skin | 5 s bullet immunity, -1.5 m/s and -20% dash while on; 12% bullet resist always; 24 s [i/g] | gun focus; usable under ability silence [U] | at once | C |
| Counters: Plated Armor | 30% bullet deflect, 50% of bullet on-hit effects prevented, +130 HP [i] | vs gun; may blunt enemy Toxic/Inhibitor/Silencer build-ups [U] | at once | C/U |
| Counters: Counterspell | 0.8 s parry blocks ability/item damage and effects; on success 150 heal, +1.75 m/s and +20 spirit 6 s; +5 spirit, +50 HP always; 23 s [i/g] | telegraphed ults and projectile CC (WC1 PREVENT) | at once | U |
| Counters: Unstoppable | 5.5 s immune to stun, silence, sleep, root, disarm; 60 s; always +25% debuff resist, +125 HP [i/g] | pre-pop vs stuns; the passive shortens every hex, slow and silence by 25% | passive at once | C (passive), U (timing) |
| Rich: Capacitor | Tesla upgrade: 20% proc, 6 chains 10 m, +5% fire rate; active 100 damage, 60% slow, no stamina, movement silence 3 s, 40 s [i/g] | waves, teamfights, catching (denies their escape); bounces carry the proc | at once | C |
| Rich: Escalating Exposure (sells Rend) | spirit hits stack +4.5% spirit amp (12 stacks, 0.7 s), 17% spirit resist, -8% spirit armor 12 s [i] | cards, Tesla, FA magic; spirit survival | at once | C |
| Rich: Spellslinger (sells Enduring Speed) | each ability/item cast in combat: +11% fire rate and -10% reload time per stack, 6 stacks, 18 s; 5% cooldown reduction always [i/l] | Card Trick (0.6 s, 2 charges) reaches 6 stacks in seconds: +66% fire rate and faster reloads, the strongest answer in the data to the reload-bound gun (I.1); CDR on PM (46 s) and Full Auto | at once | C (stack count), U (reload stacking) |
| Rich: Indomitable (from Reactive Barrier) | 325+2.0x barrier on CC, 10% bullet and spirit resist, CooldownReductionOnProc 20 [i/g]; cleanse not in data | WC1 SURVIVE | at once | U |
| Rich: Divine Barrier (sells Dispel) | removes non-stun debuffs from self or an ally, 600 barrier, +2.75 m/s 6 s, 40 m, 45 s (half on allies) [i] | self RECOVER and ally peel (team role) | at once | C |
| Losing lane: Extra Regen | +2.5 regen, OOC 1.5 [i] | lane sustain | at once | C |

### J.2 Earlier verdicts re-opened with all roles counted
| earlier verdict (section) | role it was judged on | roles added | restated verdict | changed? | grade, conf. |
|---|---|---|---|---|---|
| I.3 keep order A; option D (Enduring Speed + Reactive Barrier before Ricochet) as a trigger note; "Ricochet's farm speed is real" | Ricochet = farm | +18% fire rate in every fight (+12% one-target damage outside FA, +10% inside), x1.65-2.3 bullet damage in clustered fights, proc spread | Keep A. D's cost was understated: a 3.2k delay costs ~3 min of +12-18% fight damage plus the bounces, not only farm. D stays a trigger-only note ("2+ stuns, silences or hexes on their team") with that cost stated | cost line yes, verdict no | U, 35% (was 40%) |
| W1 keep Leech; VB only if +15% net HP | lifesteal (VB fire rate/reload as side notes) | VB: +39 extra rounds beyond the magazine on a gun that reloads 28-42% of a fight, +34% fire rate 5 s, +10% bullet resist, 30 s cooldown [g]. Leech over Bullet Lifesteal: +6% weapon damage, +12 spirit, +90 HP, anti-heal mitigation | One VB use in a 20 s fight at 16.8-29.6k: about +25-35% gun damage that fight (39 extra rounds + up to ~30 from the fire rate) vs Leech's +6% + spirit. Sustain over 30 s stays a bullet tie with Leech ahead on spirit and anti-heal. The slot is a damage-vs-sustain trade, not a sustain tie. Keep Leech, provisional; P2's pass rule becomes a joint score (net HP and damage per 30 s, both above noise) | rule yes, verdict no | C, 40% (was 50%) |
| W1 / I.9 coupling | n/a | Titanic (104-114 rounds) halves VB's ammo role | decide I.1 before W1 | new dependency | C, 70% |
| I.1 Swift -> Titanic top candidate | reload share, damage %, FA and 3 s rows | Mercurial: empowered bullets per refill grow with the magazine (Titanic gain). Build-ups: if Overflow/Silencer/Inhibitor need hits inside a sliding 5 s window, hits per second decide (Swift); if build-up survives a 2.82 s reload, hits per fight decide (Titanic). At 34.4k, 100% accuracy: Swift path ~19-21 shots/s x 5 s x 1.08 = 103-113 (charges), Titanic path ~17-19 -> 92-103 (borderline). Swift's sprint; Counters sell | Still the top candidate, now gated by PR-W1 AND PR-W2: if PR-W2 shows a sliding window, the swap may switch off Overflow's charged half, and that loss enters the decision | gate yes, verdict no | C, 50% (was 55%) |
| I.5 "Silencer/Inhibitor late and hard to fill" | build-up only | Silencer: -25% target spirit damage per bullet, 12% spirit resist; Inhibitor: +10% weapon damage, +150 HP: all work unfilled | Not dead before they fill; WC1's silence layer is still late, the anti-spirit and damage halves are not | note restated | C, 60% |
| A2.4 WC1 reviewer note (1): Dispel's cleanse unverified, swap the line to Divine Barrier if it fails | cleanse scope | game text verifies Dispel: purge all non-ultimate negatives, usable while silenced, not while stunned or slept | Withdraw the swap note. The Counters line "Silences and hexes keep stopping your teleport" is right and Dispel is the cheaper answer (3.2k vs 6.4k); Divine Barrier stays the rich upgrade path and adds ally cover | yes | C, 70% (timing U) |
| WC2 RECOVER (Divine Barrier only) | cleanse | Dispel also purges anti-heal debuffs (non-ultimate) and then heals 250 | Dispel is the 3.2k anti-heal RECOVER; same reapply limits (bullet build-ups return in seconds) | yes (adds an answer) | C, 55% |
| W6 ammo remedies (a)-(f) | slot items, VB, playstyle | Spellslinger (rich) with Card Trick spam: +66% fire rate, -60% reload time if additive, 5% CDR | Reviewer note: the strongest reload/fire-rate item for Wraith in the data; not core (6.4k, takes Enduring Speed's slot and walking escape); consider it first in the rich box | note | C, 50% |
| W7 single target | Ricochet as cluster item | already counted its +18% fire rate | unchanged | no | C, 40% |

### J.3 Tests that separate the roles (AUTORUN.md ops; A/A n=6 first, ABBA n=6, effect > 2 x A/A SD; `setup Wraith Haze`, `aimoff 5.5 3`, `fetch 350`, `ekeep 1`, `ehp 50000`; final items only)
- J-W1 Ricochet, 16.8k loadout L17 (PR-W1) with vs without `upgrade_ricochet`, `unlock 7`, `accuracy 1 0`, PR-0 fire/reload cycles, no Card Trick casts (imbue confound):
  (a) fire-rate role: `enemies 1`, no Full Auto; damage per elapsed second and hit spacing from damage csv `t_ms`. Expected +12%. RUNNABLE.
  (b) Full Auto role: as (a) with `cast 3 0.2` at t0, 8 s window. Expected +10% bullets. RUNNABLE.
  (c) bounce role: `enemies 3 250` (~6 m ring, inside 13 m); damage to victims other than the main target (csv `victim`) per primary hit; expected 2 x 0.65. RUNNABLE (ring placement unconfirmed: check all three victims appear).
  (d) proc carriage: add `upgrade_tech_defense_shredders` and `upgrade_proc_silence`; after `fire 3`, `mods` lists the Shredder debuff and Silencer build-up on the ring bots or not; Tesla rows with a ring victim as first target. RUNNABLE (names only).
  (e) lifesteal and card resource on bounces: P1 and T5 (designed above). (f) farming: UNSUPPORTED (no NPC/camp op); (c) is a hero-cluster proxy only.
- J-W2 Overflow's always-on duration: `give upgrade_tech_overflow` vs none, `unlock 7`, `cast 3 0.2`, `fire 12` (reload when empty); Full Auto end = last bullet with an FA magic row / hit spacing widening. Expected 8.0 vs 9.0 s. RUNNABLE.
- J-W3 VB's damage roles: P2 arms also score damage per 30 s and GunFired (acclog) per 30 s; separate block: `give upgrade_surging_power`, `cast i1 0.2`, `fire 30` to empty: rounds fired before empty = 52 + 39 expected. RUNNABLE.
- J-W4 Spellslinger from Card Trick: `give upgrade_enchanted_holsters` (no imbue items), `cast 1 0.3` x6, `mods`, then PR-0 cycles; stack modifier, hit spacing and reload gap vs control. RUNNABLE.
- Silencer's spirit-damage debuff: modifier name after `fire 1` via `mods` RUNNABLE; its effect UNSUPPORTED (bots never shoot). Dispel purge, VB/Leech under anti-heal: UNSUPPORTED (no `ecc`/`eheal`; P-CC0 may unlock).

### J.4 Regression (F)
No core change. New dependency recorded: the Titanic swap now depends on PR-W2 (build-up window), and W1 depends on I.1. Notes add no item or slot. No new serious weakness.

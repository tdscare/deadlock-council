# Novel interaction hypotheses (independent research, 2026-10-24)
Author: strategy/theorycraft agent. Nothing applied; no data.js change; no live Sandbox command; no queue edit. Source data: effects/items.json (195 items), effects/heroes.json (43 heroes), abilities.vdata / heroes.vdata (parsed with lib/effects/kv3.py), builds in data.js (81).

## Five tiers (kept separate)
1. FACT: value present in the game files (field, text, flag). Semantics of a flag are as named, not engine-verified.
2. USER-REPORTED: Kieran's examples. Recorded below, used only to check the model understands the mechanic. Never listed as a discovery.
3. MEASURED: sandbox results (none of the items below has one yet).
4. MODELLED: arithmetic on top of facts with assumptions (marked MODELLED).
5. UNRESOLVED hypothesis: everything in the ranked list.

## Tier 2: user-reported known (not discoveries)
Crushing Fists x Rend; Close Quarters x Rend; healing bullets with Burst Fire / Ricochet; Nurse Wretched Vapors and Lurking Terrors; Viscous The Cube x Echo Shard; Haze / Deadman Danny; Berserker; Tankbuster. Use: sanity check that the model reads these mechanics (heavy-melee flag requirement, cast-phase item lockout, imbue reset, damage-threshold charge) correctly.
Discovery-tool output (hypotheses/ranked.json, 110 items) is mostly these examples multiplied by template: 98 are Echo Shard x ability (T2, the Viscous/Echo Shard example repeated per hero), 8 are heavy-melee x Crushing Fists / Melee Charge (T5), 2 are item-lockout during a channel (T4), 2 others. They are complete coverage of the examples, not independent discovery. The list below was generated separately from the data fields named in each entry.

## Method
1. Read every item and every hero ability (text, behaviours, props, modifiers) and the proc-semantic fields in abilities.vdata: m_vecProcDamageTypes, m_bCanProcByOtherObjects, m_flMaxBulletsToProcInShot, m_bCanProcMultipleTimesFromSameShot / OnOneTarget, m_bProcAppliesBuildup, m_bDurationExtendible, imbue behaviours, DO_NOT_ALLOW_SPAM_PROC, PROJECTILE_FIRED_AS_BULLET, weapon blocks (m_iBullets, m_iBurstShotCount).
2. Cross-reference each flag family against the 81 builds in data.js to count how many builds are exposed.
3. Split: resolved from data (section below) vs genuinely open (ranked list).
4. Rank by ordinal judgments 1-5 (ASSUMED, not measured): Reach R (builds x souls at stake), Uncertainty U, sandbox Feasibility F with the current ops, Decision D (chance the answer changes a real build). Score = 0.3 R + 0.25 U + 0.2 F + 0.25 D. The weights are a choice, the 1-5 values are judgments; ties are not meaningful below 0.3.
No experiment counts are fixed: each entry says what the answer would change; the Sandbox runs the top entries only.

## Resolved or narrowed by reading the data (no sandbox time)
- FACT / build issue: graves_ult places Echo Shard on ability 4 (Borrowed Decree, an ultimate); Echo Shard's imbue type is ACTIVE_NON_ULT (items.json imbue=active_non_ult, from CITADEL_TARGET_ABILITY_BEHAVIOR_IMBUE_ACTIVE_NON_ULT). The placement contradicts the item data. Recommend the builds owner review it (nothing applied).
- FACT: Headshot Booster, Mystic Shot, Headhunter, Haunting Shot and Restorative Shot can proc on at most one bullet per shot and once per target (m_flMaxBulletsToProcInShot=1, CanProcMultipleTimes* = false). MODELLED consequence: on a 9-pellet weapon a flat next-bullet bonus lands on one pellet.
- FACT: Lucky Shot may proc several times from the same shot (CanProcMultipleTimesFromSameShot = true), so it scales with pellets.
- FACT: Mystic Slow, Suppressor, Healbane, Escalating Exposure, Mystic Vulnerability react to ABILITY damage only; Lifestrike, Spirit Strike/Snatch, Melee Charge, Crushing Fists, Runed Gauntlets react to MELEE only; Siphon Bullets, Arcane Eater to BULLET only; Mystic Reverb, Lightning Scroll to ABILITY and BULLET; Quicksilver, Mercurial Magnum to ABILITY, BULLET and MELEE.
- FACT: Echo Shard adds the imbued ability's cooldown to its own (ImbuedCooldownMultiplier 100); Frostbite Charm gives the imbued ability 50% cooldown reduction (ImbuedCooldownReduction 50).
- FACT: health-gate thresholds: Hollow Point, Battle Vest, Enchanter's Emblem need above 65% health; Fortitude 75%; Frenzy below 50%; Bullet Resilience and Spirit Resilience below 50%. Ghost Essence Bomb self-damage is 30 (SelfDamagePct), Malice 9, Frank Jumpstart 15% of current health; the self-damage basis is not stated, so no verdict.
- FACT: Spellslinger max 6 stacks, 18 s buff; Mercurial charge-up 14 s, Quicksilver 18 s.

## Ranked novel hypotheses (all UNRESOLVED unless stated)
Operations in test specs are the existing runner ops (hardreset, give, imbueown, enemies, fetch, accuracy, fire, cast, mods, cds, lowhp, incoming, eresist, wait, mark). Specs are sketches: the planner must still emit lint-valid scenario files (clean state, A-B-A, order control, readbacks) before anything is queued. Casting a given hero's ability slot is verified only for Haze, Drifter, Nurse; every other hero needs a statecheck first. No ally control exists.

### 1. N01  Several imbue items on ONE ability: does the game allow / stack them?
Score 4.8 (R5 U5 F4 D5). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: all hero-mapped builds (47 of 71 assign >=2 imbue items to one ability slot; 10 builds with unmapped heroes not counted)
- Items: Compress Cooldown, Duration Extender, Mystic Expansion, Frostbite Charm (modifier_value type); Surge of Power, Mercurial Magnum, Quicksilver Reload, Mystic Reverb, Ballistic Enchantment (active type); Echo Shard, Omnicharge Signet (active_non_ult)
- Mechanism and provenance: abilities.vdata gives each imbue item a CITADEL_TARGET_ABILITY_BEHAVIOR_IMBUE_* behaviour (ACTIVE / ACTIVE_NON_ULT / MODIFIER_VALUE); I found no per-ability imbue-capacity field in abilities.vdata or heroes.vdata (grep of every *mbue* key). Whether a second imbue replaces, is refused, or stacks is therefore not in the data. Tier of the premise: game-data FACT (types, absence of capacity field); outcome UNRESOLVED.
- Why it matters: Largest single exposure in the build set: data.js assigns 2-5 imbue items to the same ability in 47 builds (e.g. dynamo_damage 5 on ability 1, mina 5, ratking_grenade 5). Earlier note (sandbox/GAPS.md [U]) counted 20; recount from data.js is 47+.
- Decision it changes: If one imbue per ability: every such build has 1-4 dead item slots (2-5 items of 1.6k-6.4k+ each) and its imbue allocation must be re-split across abilities or dropped. If they stack: the model must add them (and Echo Shard + Compress Cooldown cooldown arithmetic).
- Cost / uncertainty: ~2-3 min runtime, 1 hero; 4 arms. Uncertainty: high (no data either way).
- Proposed test:
  - setup Haze Haze
  - souls 30000
  - arms: P0 no imbue | A Compress Cooldown only | B Compress Cooldown then Surge of Power | C Surge of Power then Compress Cooldown | D Compress+Frostbite Charm
  - per arm: hardreset; souls 30000; give <items>; imbueown <item> Signature2 (each); basemods; cds; cast 2 0.6; mods; cds
  - readbacks: ability-2 cooldown (cds), imbue op result/refusal text, mods names, spirit-power effect via damage csv on a cast ability if Surge is used
- Outcome mapping: WORKS (stack): ability-2 cooldown in B/C/D equals the product/sum of both effects in both orders -> keep builds, add stacking to the model. REPLACES: only the last (or first) imbue shows -> order matters, 47 builds re-planned. REFUSED: second imbueown errors -> same.

### 2. N03  Ability-only proc items vs bullet-delivered spirit damage (which damage type does it carry?)
Score 4.25 (R4 U4 F4 D5). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: Gigawatt/Seven (Power Surge shock), Hornet/Vindicta (Flight bonus spirit damage), Mina/Vampirebat (Love Bites), Wraith (Full Auto spirit per bullet), Victor/Frank (Reanimation bullets)
- Items: Mystic Slow, Suppressor, Healbane, Escalating Exposure, Mystic Vulnerability (all m_vecProcDamageTypes = ABILITY only)
- Mechanism and provenance: abilities.vdata m_AutoIntrinsicModifiers/m_vecProcDamageTypes lists only CITADEL_DAMAGETYPE_ABILITY for these five (FACT); the hero text says the bullet-attached damage is spirit damage but the damage-type tag of that damage is not in the vdata (the damage csv does record dmg_type per hit).
- Why it matters: 45 of 81 builds hold >=1 of these five items; 7 of them sit on heroes whose repeated damage is bullet-borne (seven, seven_gun, victor, victor_gun, wraith, mina, vindicta_sniper). If the bullet-borne spirit damage is typed BULLET these items never trigger there.
- Decision it changes: Typed ABILITY: bullet-spirit heroes get a per-bullet proc rate (huge for Escalating Exposure stacking and Healbane). Typed BULLET: the items are dead weight in those 7 builds -> swap (cheapest first).
- Cost / uncertainty: 1 hero, 3 arms, damage csv only. Uncertainty: high.
- Proposed test:
  - setup Gigawatt (verify cast 3 with statecheck first; fall back to Wraith Full Auto)
  - arms: bullets only | cast 3 then fire 12 | cast 3 + Escalating Exposure then fire 12
  - ops: hardreset; give upgrade_escalating_exposure; enemies 1 300 4; eresist gun 50 then eresist spirit 50 as separate arms; cast 3 0.6; fetch 350; fire 12; mark
  - readback: dmg_type of each damage row, which resist moved the damage, whether damage per bullet rises across the burst (stack growth)
- Outcome mapping: dmg_type=Ability on the shock/bonus rows AND damage growing across the burst -> eligible. dmg_type=Bullet or no growth -> the five items do not trigger from bullet-borne spirit damage.

### 3. N02  Do bullet-resist reducers stack (add / multiply / strongest-only)?
Score 4.2 (R4 U4 F5 D4). Tier: UNRESOLVED hypothesis.
- Heroes / builds: 20 builds hold >=2 reducers, 6 hold >=3 (sinclair holds 4)
- Items: Bullet Resist Shredder, Weakening Headshot, Crippling Headshot, Hollow Point, Hunter's Aura, Rusted Barrel, Disarming Hex, Alchemical Fire, Crushing Fists
- Mechanism and provenance: Each item applies its own resist-reduction modifier (items.json effects subtype=resist/op=reduce; abilities.vdata per-item values). The combining rule (additive vs multiplicative vs max-wins per modifier family) is engine-side and not in the vdata.
- Why it matters: Redundant reducers are paid for in 20 builds; the model currently combines them by an assumed rule.
- Decision it changes: If max-wins or heavy diminishing: cut the weaker reducer in those builds (800-6400 souls each) and reinvest. If multiplicative: keep and credit the full combined value in the trade model.
- Cost / uncertainty: 1 hero, 5 arms, ~20 bullets per arm, uses existing eresist + damage csv. Uncertainty: high.
- Proposed test:
  - setup Haze Haze
  - arms: none | BRS | Weakening Headshot | BRS + Weakening Headshot | BRS + Weakening Headshot + Hollow Point
  - per arm: hardreset; give items; enemies 1 300 4; eresist gun 50 (fixed base resist); fetch 350; accuracy 1.0; fire 20 (headshots forced where required, mark each arm)
  - readback: mean damage per bullet from damage csv; base bullet damage from the A0 arm
- Outcome mapping: Ratio of damage per bullet vs the product/sum predicted from each item's own value separates ADD / MULTIPLY / MAX. MAX or sub-additive -> prune redundant reducers (gate flag); MULTIPLY -> keep.

### 4. N04  "Next bullet" items on burst, pellet and beam weapons
Score 4.0 (R4 U4 F4 D4). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: Lash and Gigawatt (3-round bursts), Chrono (5), Yamato (5 pellets), Drifter (3), Atlas/Calico (9 pellets), Shiv (6), Synth (7), Werewolf (7), Bebop (continuous beam)
- Items: Headshot Booster, Mystic Shot, Headhunter, Haunting Shot, Restorative Shot (cap 1 bullet per shot), Express Shot (fires twice, uses extra ammo)
- Mechanism and provenance: abilities.vdata: m_flMaxBulletsToProcInShot=1, m_bCanProcMultipleTimesFromSameShot=false, m_bCanProcMultipleTimesOnOneTarget=false on the five items (FACT). Weapon blocks: m_iBullets (pellets) and m_iBurstShotCount (burst) per hero weapon (FACT). Bebop weapon text: "continuous beam with no bullet travel" (FACT, text).
- Why it matters: 13 builds combine such items with a multi-pellet/burst/beam weapon (paradox 3 items on a 5-round burst, lash 3 on a 3-burst, bebop 2 on the beam, shiv_gun, silver, yamato_brawler, danny_gun).
- Decision it changes: Cap=1 means a flat next-bullet bonus is worth ~1 pellet of 5-9 on shotgun heroes (resolved by reading, the arithmetic is MODELLED). Open: does a burst count as one shot or several, do two items share the same first bullet or consume successive bullets, and does the beam ever raise "headshot"? Decides whether these items are bought on those heroes at all.
- Cost / uncertainty: 2 heroes (1-bullet control + burst/pellet hero), 3 arms. Uncertainty: medium-high.
- Proposed test:
  - setup Haze Haze (control) and Drifter or Lash (multi-pellet/burst)
  - give upgrade_headshot_booster upgrade_crackshot upgrade_express_shot; enemies 1 300 4; fetch 350; accuracy 1.0; fire 6; mark
  - arms: each item alone | all three together
  - readback: per-bullet damage rows in order (which bullet carries which bonus), count of bullets per shot, ammo drop per shot (Express Shot)
- Outcome mapping: Bonus lands on exactly one bullet per shot and items consume successive shots -> order/rotation matters, shotgun value divided by pellets. All items on the same first bullet -> bursty, cooldowns synchronise. No proc on beam -> drop on Bebop.

### 5. N07  Healing Tempo: do granted lifesteals and ability heals count as "applying healing"?
Score 4.0 (R4 U4 F4 D4). Tier: UNRESOLVED hypothesis.
- Heroes / builds: 21 builds hold Healing Tempo (dynamo, kelvin x2, haze, rem, solomon_support, victor x2, viscous, yamato x2, geist x2, apollo x2, celeste x2, baba_tank, abrams, ivy, nurse)
- Items: Healing Tempo (6400, T4); sources: Vampiric Burst, Infuser (grant lifesteal for a duration), Healing Rite/Extra Health (regen), Rescue Beam, Healing Nova, ability lifesteals (Lash Flog, Yamato Crimson Slash, Krill Scorn, Bebop Hyper Beam)
- Mechanism and provenance: Item text (FACT): "Applying healing to yourself or an ally grants the target ...; does not apply on innate regen or passive Bullet/Spirit Lifesteals". Item cd 1.0 s. Whether a lifesteal that is granted by an active (Vampiric Burst, Infuser) is "passive" is not in data.
- Why it matters: A 6.4k T4 slot in 21 builds; its value depends entirely on which heal events count.
- Decision it changes: If active-granted lifesteal and ability lifesteal count: Healing Tempo is strong in lifesteal builds. If only discrete heals count: keep it only on heal-ability heroes, swap elsewhere.
- Cost / uncertainty: Haze + Nurse, ~2 min. Uncertainty: high.
- Proposed test:
  - setup Haze Haze: give upgrade_healbuff upgrade_surging_power; lowhp 60; enemies 1 300 4; fetch 350; cast i1 (Vampiric Burst); fire 6; mods
  - control: Healing Rite instead of Vampiric Burst
  - readback: mods list for the Tempo buff, healDiffObserved with/without the item
- Outcome mapping: Tempo buff appears on Vampiric Burst heals -> counts. Appears only for Healing Rite -> discrete heals only.

### 6. N05  Chance / build-up bullet items on multi-pellet weapons: per pellet or per shot?
Score 3.7 (R3 U4 F4 D4). Tier: UNRESOLVED hypothesis.
- Heroes / builds: Calico/Nano (9 pellets, 0.21 s cycle), Shiv (6), Atlas (9), Synth (7), Silver/Werewolf (7), Drifter (3)
- Items: Tesla Bullets, Armor Piercer, Slowing Bullets, Weighted Shots, Toxic Bullets, Silencer, Inhibitor, Lucky Shot
- Mechanism and provenance: Lucky Shot (upgrade_critshot) has m_bCanProcMultipleTimesFromSameShot=true (FACT); Slowing Bullets/Weighted Shots have m_bProcAppliesBuildup=true (FACT); Armor Piercer, Tesla and Silencer carry no per-shot cap field (absence is not proof). Pellet counts from weapon blocks (FACT).
- Why it matters: calico_gun and shiv_gun hold 3-5 of these items on 6-9 pellet weapons; drifter holds three on 3 pellets.
- Decision it changes: Per pellet: proc and build-up rates scale with pellet count, so these items are far stronger on shotguns and the model must multiply. Per shot: they are worth the same as on a 1-bullet hero.
- Cost / uncertainty: 1 hero with pellets (+Haze control), counts only. Uncertainty: medium.
- Proposed test:
  - give upgrade_chain_lightning (and separately upgrade_critshot); enemies 1 300 4; fetch 350; accuracy 1.0; fire 30
  - run on Haze (1 bullet) and Drifter (3 pellets)
- Outcome mapping: Proc rows per shot divided by the control: ~3x on Drifter -> per pellet; ~1x -> per shot.

### 7. N06  Which items are triggered by summons / turrets / clones (m_bCanProcByOtherObjects)?
Score 3.55 (R4 U3 F3 D4). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: Forge/McGinnis (Mini Turret), Magician/Sinclair (Spectral Assistant), Necro/Graves (Deadheads), Chessmaster/Solomon (pieces), Ratking, Bookworm/Paige
- Items: can be charged by other objects (flag true): Mystic Burst, Tankbuster, Mystic Reverb, Suppressor, Quicksilver, Mercurial Magnum, Lightning Scroll, Ballistic Enchantment, Siphon Bullets, Arcane Eater. No such flag on Mystic Slow, Mystic Vulnerability, Healbane, Escalating Exposure.
- Mechanism and provenance: abilities.vdata m_bCanProcByOtherObjects = true on exactly those ten item classes (FACT); absent elsewhere (default presumably false, engine default not verified).
- Why it matters: 14 summoner builds. mcginnis_turret (turret build) holds Mystic Slow + Mystic Vulnerability + Healbane + Escalating Exposure: none flagged; graves, graves_ult, graves_tank hold Mystic Vulnerability + Escalating Exposure.
- Decision it changes: If the flag decides: summon heroes should buy the flagged burst/charge items and skip the unflagged spirit-debuff items (or credit them only for the hero's own casts). Largest swap candidate: mcginnis_turret.
- Cost / uncertainty: 1 summoner hero, 3 arms. Uncertainty: medium (flag present; engine default unverified).
- Proposed test:
  - setup Forge (verify cast 1 works; otherwise Magician)
  - arms: turret only | turret + Mystic Vulnerability | turret + Suppressor
  - ops: give item; enemies 1 300 4; cast 1; fetch 350; wait 6; cast own damaging ability; mark
  - readback: damage csv attributed to turret rows; amplified damage on the follow-up cast (Vulnerability); enemy fire-rate / mods (Suppressor)
- Outcome mapping: Turret damage triggers flagged items only -> flag is authoritative, apply it to all 14 builds. Triggers both -> flag means something else, drop it from the model.

### 8. N10  Abilities flagged PROJECTILE_FIRED_AS_BULLET: do they act as bullets for items and resist?
Score 3.45 (R3 U4 F4 D3). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: Nurse Leech Therapy, Viper Screwjab Dagger and Petrifying Bola, Werewolf Slam Fire and Entangling Bola, Bookworm Bookwyrm, Chrono Pulse Grenade, Hornet Stake, Kelvin Frost Grenade, Necro Jar of Dead, Ratking Scrap Grenade, Tengu Entangling Thorns
- Items: Burst Fire-type on-hit self buffs (Escalating Resilience, Spiritual Overflow), Armor Piercer, Ricochet, bullet-resist items on the target
- Mechanism and provenance: behaviours list contains PROJECTILE_FIRED_AS_BULLET for these 12 abilities and for the items Mystical Piano and Alchemical Fire (FACT). What that implies for item procs and for the resist applied is engine-side.
- Why it matters: If these abilities count as bullet hits they can trigger bullet-hit items and may be reduced by bullet resist rather than spirit resist, changing how those heroes should itemise.
- Decision it changes: Counts as bullet: bullet-hit procs/resist apply to the ability (re-class in the model, e.g. spirit vs gun item choice). Does not: no change.
- Cost / uncertainty: Nurse, 2 arms. Uncertainty: high.
- Proposed test:
  - setup Nurse Haze: give upgrade_reinforcing_casings; enemies 1 300 4; cast 1 aimed at the bot
  - arms: eresist gun 50 vs eresist spirit 50
  - readback: damage csv dmg_type and which resist scaled the damage; self mods for Escalating Resilience stack
- Outcome mapping: Damage scales with the gun resist or Bullet type / self stack appears -> bullet; otherwise ability.

### 9. N15  Spirit-resist reducers: do Spirit Strike / Snatch / Sap / Shredder / Mystic Vulnerability stack?
Score 3.45 (R3 U4 F4 D3). Tier: UNRESOLVED hypothesis.
- Heroes / builds: 12 builds hold >=3 (abrams, baba, baba_tank, bebop, bebop_bomb, calico, drifter_spirit, graves_tank, holliday_spirit, infernus, mirage, viscous_damage)
- Items: Spirit Strike, Spirit Snatch, Spirit Sap, Spirit Shredder, Mystic Vulnerability, Escalating Exposure (amp), Crippling Headshot
- Mechanism and provenance: Same family as N02 but on spirit resist; combining rule engine-side.
- Why it matters: Several of these are bought together on melee/spirit builds.
- Decision it changes: Prune redundant reducers or credit the product.
- Cost / uncertainty: Drifter/Haze, eresist spirit, 4 arms. Uncertainty: high.
- Proposed test:
  - eresist spirit 50; give item sets; cast a damaging ability x3 per arm; compare damage
- Outcome mapping: As N02.

### 10. N08  Duration Extender / Superior Duration: only flagged modifiers?
Score 3.4 (R3 U3 F5 D3). Tier: UNRESOLVED hypothesis (premise: game-data FACT with extractor caveat).
- Heroes / builds: Drifter (Stalker's Mark), Infernus (Afterburn), Dynamo (Singularity), Seven (Storm Cloud), Sinclair (Rabbit Hex), Paige (Captivating Read), McGinnis (Heavy Barrage), Graves (Borrowed Decree), Silver, Pocket, Holliday, Mokrill, Ivy
- Items: Duration Extender (imbue), Superior Duration (global)
- Mechanism and provenance: m_bDurationExtendible exists on 61 item modifiers and on a subset of hero modifiers (FACT: field values). In the effects data 18 Duration Extender imbues target abilities with no flagged modifier, and mcginnis_turret, mcginnis_ult, graves_ult, ivy hold Superior Duration with zero flagged ability. The extractor may under-detect flags that sit on debuff modifiers (caveat).
- Why it matters: If the flag is the gate, those placements add nothing.
- Decision it changes: Remove or re-target Duration Extender / Superior Duration in the listed builds; otherwise keep.
- Cost / uncertainty: Drifter + Haze, mods timeline. Uncertainty: medium.
- Proposed test:
  - setup Drifter (cast slot 2 works) and Haze (Smoke Bomb flagged control)
  - arms: no imbue | Duration Extender imbued; cast 2; mods at 1 s steps until expiry
  - readback: modifier lifetime in seconds (mods + wait steps)
- Outcome mapping: Unflagged ability lifetime unchanged while the flagged control lengthens -> flag is the gate (build edits needed). Both lengthen -> flag is not the gate.

### 11. N14  Hunter's Aura "doubled with one enemy hero nearby": the 1v1 case and stacking with other reducers
Score 3.4 (R3 U3 F5 D3). Tier: UNRESOLVED hypothesis.
- Heroes / builds: 11 builds (bebop, bebop_support, venator, yamato_brawler, apollo_melee, silver, sinclair, abrams_melee, drifter, calico_gun, shiv_gun)
- Items: Hunter's Aura (T3 WeaponMod)
- Mechanism and provenance: Item text (FACT): reduces nearby enemies' bullet resist and fire rate; doubled when only one enemy hero is nearby. Radius and the combining rule with other reducers are not tested.
- Why it matters: Lane (1v1) value differs from fight value by 2x; the trade model assumes one.
- Decision it changes: If doubling is real in lane and stacks with Weakening Headshot etc.: buy earlier on lane-heavy builds; else treat as fight-only.
- Cost / uncertainty: Haze, 2 arms. Uncertainty: medium.
- Proposed test:
  - give upgrade_bullet_armor_reduction_aura; eresist gun 50; enemies 1 300 4 vs enemies 3 300 4; fetch 350; fire 20
- Outcome mapping: Damage per bullet with 1 vs 3 enemies differs by the doubled value.

### 12. N13  Damage-over-time ticks and "spirit damage dealt" stacking (Escalating Exposure)
Score 3.25 (R3 U4 F3 D3). Tier: UNRESOLVED hypothesis.
- Heroes / builds: Inferno (Afterburn), Viper (Lethal Venom), Hornet (Crow bleed), Shiv, Astro (burn), Priest (burning), Ghost (toxic mess)
- Items: Escalating Exposure (38 builds), Mystic Vulnerability, Healbane, Mystic Slow
- Mechanism and provenance: Escalating Exposure proc types = ABILITY only (FACT). Affliction and Decay text explicitly "do not apply item procs" (documented); other DoTs carry no such text.
- Why it matters: 38 builds hold Escalating Exposure; DoT heroes either saturate it per tick or never trigger it.
- Decision it changes: Per tick: DoT heroes should prefer it; otherwise skip on them.
- Cost / uncertainty: Astro or Inferno, 2 arms. Uncertainty: medium-high.
- Proposed test:
  - give upgrade_escalating_exposure; enemies 1 300 4; cast DoT ability; wait 4; cast a direct spirit ability; mark
  - control: no DoT first
- Outcome mapping: Direct cast damage higher after a DoT than control -> ticks count.

### 13. N09  Cast-triggered stacking (Spellslinger, Radiant Regeneration): which casts count?
Score 3.2 (R3 U3 F4 D3). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: 11 builds hold Spellslinger (bebop, haze_assassin, victor_gun, violet, wraith, geist, celeste_carry, warden, holliday, calico_gun, ivy_carry)
- Items: Spellslinger (6 stacks max, 18 s buff duration), Radiant Regeneration, Arcane Surge
- Mechanism and provenance: behaviour flag DO_NOT_ALLOW_SPAM_PROC (FACT) marks six abilities: Deadpack Jettison Fuel, Familiar Tag Along and Lil Helpers, Frank Aura of Suffering, Mirage Djinn's Mark, Nurse Healing Needles. Item text: "whenever you cast an ability or item". Which items read that flag is not in data.
- Why it matters: Fast-cast kits (Wraith Card Trick 0.6 s, Frank, Mirage, Nurse) either fill Spellslinger instantly or are excluded.
- Decision it changes: Excluded: Spellslinger is weak for those heroes (swap). Counted: strong enough to justify cheap actives bought only to stack it.
- Cost / uncertainty: Nurse, 3 arms. Uncertainty: medium.
- Proposed test:
  - setup Nurse Haze: give upgrade_enchanted_holsters; enemies 1 300 4
  - arms: cast 3 x6 (flagged) | cast 1 x6 (unflagged) | item active x3 (Healing Rite)
  - mods after each cast
- Outcome mapping: Stack count increments per arm identify which cast types count.

### 14. N11  Mercurial Magnum / Quicksilver Reload: charge-up by time only, or also by damage?
Score 3.2 (R3 U3 F4 D3). Tier: UNRESOLVED hypothesis (premise: game-data FACT).
- Heroes / builds: 17 builds (dynamo_damage, greytalon_gun, haze, victor_gun, violet, wraith, mina, vindicta, mcginnis, celeste_carry, warden, vyper x2, holliday, graves, mokrill, nurse)
- Items: Mercurial Magnum (AbilityChargeUpTime 14), Quicksilver Reload (18)
- Mechanism and provenance: Both items list m_vecProcDamageTypes = ABILITY, BULLET, MELEE and m_bCanProcByOtherObjects=true (FACT), which suggests damage dealt feeds the item as well as the timer; text says "charges up over time". Interaction between the two is not in data.
- Why it matters: The reload-on-use value (and the ammo model) assumes a fixed time charge.
- Decision it changes: Damage-accelerated: effective availability is shorter in fights; raise the value. Time only: unchanged.
- Cost / uncertainty: Haze, 2 arms, ammo/clip readback. Uncertainty: medium.
- Proposed test:
  - setup Haze Haze: give upgrade_ethereal_bullets; imbueown upgrade_ethereal_bullets Signature2; enemies 1 300 4
  - arms: wait 8 then cast 2 | fire 40 for 8 s then cast 2
  - readback: clip/ammo after the cast (SC logs), mods for the charge
- Outcome mapping: Different ammo refill / charge state at equal elapsed time -> damage matters.

### 15. N12  Damage-reshaping kits vs threshold-triggered barriers (Bloodletting, Royal Pestments)
Score 2.9 (R2 U3 F4 D3). Tier: UNRESOLVED hypothesis.
- Heroes / builds: Shiv (Bloodletting defers damage), Ratking (Royal Pestments caps single hits), Viscous cube, Warden
- Items: Weapon Shielding, Spirit Shielding, Spellbreaker, Plated Armor, Reactive Barrier
- Mechanism and provenance: Shielding items trigger on "significant damage in a small time frame" (text, FACT); Bloodletting converts immediate damage to a deferred tick (kit text, FACT); Royal Pestments caps per-hit damage. Whether deferred ticks or capped hits satisfy the threshold is not in data.
- Why it matters: shiv holds Spirit Shielding + Spellbreaker + Plated Armor; 22 builds hold a threshold barrier.
- Decision it changes: If Bloodletting prevents the trigger: the barrier items are redundant on Shiv (cut ~3.2k). If ticks count: fine.
- Cost / uncertainty: Shiv, uses existing `incoming gun|spirit dps` op. Uncertainty: medium.
- Proposed test:
  - setup Shiv: give upgrade_weapon_shielding; enemies 1 300 4
  - arms: incoming gun 250 for 4 s | cast 3 then incoming gun 250 for 4 s
  - readback: barrier modifier appears? barrier amount (mods), HP loss
- Outcome mapping: Barrier absent after Bloodletting -> redundant pair.

### 16. N16  Heal-reduction and slow stacking (Leech, Toxic, Inhibitor, Healbane, Crippling Headshot; Slowing/Weighted/Mystic Slow)
Score 2.85 (R3 U4 F1 D3). Tier: UNRESOLVED hypothesis (blocked).
- Heroes / builds: 8 builds hold >=3 heal reducers (infernus, haze, geist, apollo, baba, mirage, graves, shiv); mirage holds six
- Items: listed + Leech (reduces effect of enemy healing reduction)
- Mechanism and provenance: Each applies its own modifier; combination rule not in data.
- Why it matters: If reducers do not stack, 2-4 of them are dead in those builds.
- Decision it changes: Prune; reconsider Leech.
- Cost / uncertainty: needs enemy healing / movement readback: BLOCKED in the current runner (no enemy heal or movement op). Uncertainty: high.
- Proposed test:
  - BLOCKED: needs an op to heal or move the enemy bot and read the result
- Outcome mapping: n/a until the op exists.

### 17. N17  Shadow Weave ambush: triggered by hero-granted invisibility?
Score 2.55 (R1 U3 F5 D2). Tier: UNRESOLVED hypothesis.
- Heroes / builds: Haze (Smoke Bomb), Sinclair build (only holder)
- Items: Shadow Weave, Shadow Strike, Veil Walker
- Mechanism and provenance: Shadow Weave text: attacking or using an ability ends stealth and starts an ambush; Smoke Bomb text: attacking removes invisibility. Both use an invisibility modifier; whether the ambush trigger reads any invisibility is not in data.
- Why it matters: Would give a free ambush window from a cooldown the hero already has.
- Decision it changes: Low: one build holds the item.
- Cost / uncertainty: Haze, 2 arms. Uncertainty: medium.
- Proposed test:
  - give upgrade_cloaking_device_active; cast 2; fire 3; mods
- Outcome mapping: ambush modifier appears or not.

## Pending queue tasks: example recycling or informative
- T2_5d1b5cd1f7 (Haze: Echo Shard imbued on Smoke Bomb, cast / reset / cast again): example recycling (Echo Shard x ability, the Viscous/Echo Shard example moved to a hero whose cast works). Keep it only as the single executable representative of that whole class (discovery's own verdict: MODELLED, Compress Cooldown beats it on average uptime; only double-cast burst is unique). Informative value low-medium; run after N01, N02, N03.
- T4_da3e1d605b (Nurse: Lurking Terrors disables item actives): example recycling (Nurse Lurking Terrors) and its own verdict is "constraint, not a gain, no build change". Informative value low; defer or drop.
- act:ar2 and cap:test1: duplicates. p2:act_ar2 and p2:cap_test1 are already `done` with VALID: yes (19:00-19:02); the plain entries are still `pending`. Not informative; remove or ignore (I did not touch the queue).
- The other 97 Echo Shard x ability and 8 heavy-melee hypotheses in ranked.json are the same class; do not queue them as separate experiments.

## Not done / limits
- Specs are sketches, not lint-valid scenario files; nothing was queued or run.
- Reach counts come from item names in data.js and a hero-name mapping; 10 builds (rem, violet x2, vindicta x2, mcginnis x3, baba x2) could not be mapped to hero data in some counts and are excluded from the N01 and N08 figures.
- N08 relies on the extractor's duration_extendible flag; a flag on a debuff modifier may be missed.
- Scores are ordinal judgments. Pending items N16 (blocked) needs a new runner op.

## Tool changes made with this research (offline, 2026-10-24)
- discover_interactions.py reads validated/measured.json (`links`), sets stage 2 MEASURED on the matching hypothesis and re-ranks T5 siblings by an explicit rule (+0.6 same item on another ability whose damage types match the item\'s proc types, +0.3 other items on the measured ability, -1.5 / -1.0 on rejection). `python3 -I council/tools/discover_interactions.py rerank-diff` writes evidence/interactions/hypotheses/rerank_diff.txt (ranking with vs without the measured results, user-example flags and caps applied to both).
- De-example: validated/user_example_patterns.json flags `user_example_derived` (penalty 1.0); cap 10 hypotheses per item and 12 per event class (88 Echo Shard hypotheses moved to meta.overflow); T5 event classes are derived from shared ability/item property stems that also occur in both texts (21 stems), not from a written list; relabel-invariance and provenance self-check pass (285 citations, 0 failed).
- lib/effects/extract.py: `damage_split` per ability (MELEE / ABILITY / BULLET from the property CSS class and scale stat; Rend = Damage MELEE + BonusDamage ABILITY, matching the measured split), `proc_semantics` per item/ability (proc damage types, other-object procs, per-shot caps, build-up), `text_source` (20 items have empty text in localisation, none of them actives; their values come from properties). 17 unit tests pass (known-answer from raw files plus negatives, and the learning loop).
- queue.js `retire-unplanned`: the 243 paused-needs-design tasks are now `not-a-queue` in the local sandbox/queue.json.

# graves_ult: triage of changes since CLEANBASE (data.CLEANBASE_pre_spikefix.js -> data.js)

Confidence for every verdict: calculated, unvalidated (no sandbox results exist for these scenarios; no council/evidence/graves.json).

## What changed (silent, no changes line)
| # | Change | Verdict |
|---|---|---|
| 1 | Arcane Surge moved from Early (3rd buy, 2.4k) to Mid cont. (25.6k) | MISTAKE |
| 2 | (pre-existing in both bases) Echo Shard imbued on Borrowed Decree (ult) | MISTAKE (hard error) |
| 3 | (pre-existing) Refresher note "Use it right after Echo Shard for a third gravestone" | MISTAKE (false) |

No other differences: items, boxes, ability order, name/desc identical (diff of the extracted builds).

## 1. Arcane Surge position: section N comparison
Source: council/triage/calc/graves_paths.txt (paths.py, which runs abtimeline analyse/state on each candidate).

| Path | Order (Early) | Spirit 4.8k | Health 4.8k | SP @3.2k (ult unlock, model A) | Hands / ult hit @3.2k | @8k Hands / ult |
|---|---|---|---|---|---|---|
| P0 clean | ES, EStam, **Arcane Surge**, IS, Grit, DE, EE | 5.6k | 9.6k | 65 (45 without the dash bonus) | 194 / 197 | 348 / 249 |
| P1 current | ES, EStam, IS, Grit, DE, EE ... Surge @25.6k | **13.6k** | 8.0k | 37 | 149 / 162 | 296 / 207 |
| P2 | ES, EStam, IS, Grit, DE, Surge, EE | 5.6k | 9.6k | 37 (+200 barrier, +12% vitality bonus) | 149 / 162 | 348 / 249 |
| P3 | ES, EStam, IS, Grit, Surge, DE, EE | 5.6k | 9.6k | 37 (Surge at 4.0k) | 149 / 162 | 348 / 249 |
| P4 | ES, EStam, IS, DE, Surge, Grit, EE | 5.6k | 9.6k | 37 | same as P2 from 5.6k | 348 / 249 |

- P1 loses 20-40 spirit power for 8,000 souls (5.6k-13.6k): -15% Hands, -17% ult at 8k. Its only gain is health 4.8k at 8.0k instead of 9.6k. It also broke the Counters line "Sell Arcane Surge" (not owned yet at Heroic Aura, 12k). MISTAKE.
- P0 against P2/P3/P4: same spikes. P0 has +28 spirit power and Arcane Surge on the first ults (3.2k model A, 3.9k model B). P2 has Grit and the vitality bonus 800 souls earlier (about +30% effective HP at 3.2k-4k). It's a close call, and the rule "damage spike first" settles it: **P0**.

Item roles (section J), Arcane Surge: +1 stamina and 12% stamina cooldown (the same as Extra Stamina, which it consumes, so mobility is kept), unconditional spirit investment (1600, which reaches the 3.2k step at 3.2k), and after a dash-jump the next ability gets +15% duration, +12% range/radius and +20 spirit. On Decree that also stacks with Duration Extender, because Decree's duration scales from ETechPower+ETechDuration (scale_function_multi_stats, so Round 23 is confirmed). It is also the Counters/Cursed Relic sell slot. Cost: vitality investment drops from 800 to 0 until Grit.

## 2. Echo Shard on the ult
Data: abilities.vdata `upgrade_ability_power_shard` m_TargetAbilityEffectsToApply = CITADEL_TARGET_ABILITY_BEHAVIOR_IMBUE_ACTIVE_NON_ULT (line 223096). Text: "Reset the cooldown of the imbued non-ultimate ability" (items_full_6819 text_extra). 6819 changes nothing (GAMEDATA_6819.md). Verified.
Retarget candidates:
- Grasping Hands (chosen): cd 20s at T3 (from 13.8k), 2 ghouls per cast at T3, 585 damage + 1.75s immobilize at 36.8k. A second wall right away fits the ghoul/ult plan. Echo cooldown = 30 + Hands cooldown, about 46-50s.
- Jar of Dead: its charges are gated by collected death (ResourceCost 120, AbilityChargesConditionally), so a reset gives no extra jar. Rejected.
- Essence Theft: no cooldown. Rejected.
- Refresher in core instead: about one extra gravestone per 300s, against about 6 extra Hands per 300s from Echo. UNTESTABLE-HIGH-RISK. Kieran's rule keeps Refresher in rich when the ult matters. Not adopted.
The Round 23 claim "Echo Shard + Refresher give 3 gravestones" is withdrawn.

## 3. Refresher note
Late ult cooldown: 125s base, with Superior Cooldown 20%, Enchanter's 5% and Kevlar ult 10% = ~81s (additive) / ~85s (multiplicative). Duration: (16 + 0.04x~300 SP + 10) x (1 + 0.28 + 0.15 + 0.15) = ~60s. The cooldown stays above the duration, so Refresher alone gives 2 live stones. New note: "Use it right after your ult to cast it again. Sell Enchanter's Emblem for this." The stacking of cooldown reduction is model-only.

## Corrected progression (council/work/graves_ult.js)
Early: Extra Spirit, Extra Stamina, Arcane Surge, Improved Spirit, Grit, Duration Extender (Decree), Enchanter's Emblem. Mid: Spirit Lifesteal, Spirit Shielding, Heroic Aura, Compress Cooldown (Decree), Superior Duration, Superior Cooldown, Mystic Vulnerability, Diviner's Kevlar, Boundless Spirit. Late: **Echo Shard (Grasping Hands)**, Escalating Exposure, Magic Carpet, Spirit Burn. Counters/rich/slot locked unchanged except the Refresher note. Ability order unchanged: 1123444224231133.
Spikes: spirit 4.8k @5.6k, health 4.8k @9.6k. walk1 FLAGS none, CHECK12 none, abtimeline gate PASS (no errors or warnings).

## Open mechanics questions
- Unlock vs ability-point queue (F5c): model A (separate queues) and model A strict (one queue) give identical tiers at every checkpoint for P0-P4. Model B (old: 1 AP per tier) moves the ult unlock to 3.9k and Hands T3 to 6.8k. No verdict changes under any of the three (all are shown in graves_paths.txt).
- 1-charge counting (F7): there are no charge items in this build, so it doesn't apply.

## Model-only (not validated)
Spirit power and invest bonuses (heroes.vdata), vitality bonus = % health (INFERRED), the cooldown-stacking formula, Echo-on-Hands value and the Refresher stone count. Scenarios: council/sandbox/scenarios/graves_ult_echo_target.json, graves_ult_arcane_surge_timing.json, graves_ult_refresher_second_stone.json (not run). The pending duo_b3_graves_decree_duration test also bears on Duration Extender/Arcane Surge on Decree.

## Depends on item data that could change
Echo Shard's non-ult flag and cooldown formula; Arcane Surge stats (Stamina, duration 15%, spirit 20); the Tech invest bonus table; Grasping Hands T3 (-14s cooldown, +1 ghoul); Decree duration scaling (0.04x spirit, ETechDuration); Refresher 300s.

## Gate (node council/tools/gate.js check council/proposals/graves_ult.json): PASSES, 0 blocking
Fixed: MAIN_4.8K_LATE (spirit 13.6k), ECHO-ON-ULT. RT_ITEMS differences are the export round-trip, which the gate ignores.
UNRESOLVED (all present before this proposal):
- CORE_NOTE_NONEMPTY Arcane Surge "Dash-jump right before you cast your ult." and Heroic Aura "Works on your ghouls too.": both are allowed note kinds (a usage tip, and a niche interaction: Heroic Aura NonHeroMult 2). The checker's prefix list doesn't cover them. Left as is; changing them is a wording decision for Kieran (the Arcane Surge note is imperative).
- THRESH_ITEM_NO_THRESHOLD_LINE Spirit Burn, Arcane Surge: the proposal reason has a "Threshold:" line naming both (Spirit Burn ~863 without ult vs 500; Arcane Surge = dash condition). It enters `changes` only on apply, so check can't see it: resolvable on apply only.

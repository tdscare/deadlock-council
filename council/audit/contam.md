# contam: shared-calculation contamination audit (read-only; nothing in data.js/tools edited)
Scratch (reproducible): council/audit/tmp_contam/ (ext.py = per-hero vdata extract -> heroes_gd.json; sp_tp.js = sp.js with TP env var; hm/ = haze_model copies).
Ground truth used: gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata + abilities.vdata (all 68 hero blocks parsed), audit/items_full.json. Item PRICES are not in the vdata (see E8).

## 1. Per-hero per-level stats from game data vs code
`m_mapStandardLevelUpUpgrades` (per standard level 2..36, 35 levels). Only heroes in data.js shown where value differs from hero_base:
| hero (hk) | spirit/lvl | bullet dmg/lvl | HP/lvl | other per-level |
|---|---|---|---|---|
| default hero_base | 1.1 | - | 62 | melee 1.58 |
| haze | **0.5** | 0.143 | 33 | |
| kelvin | **1.3** | 0.418 | 60 | tech resist 0.625/lvl |
| orion (greytalon) | **1.6** | 0.85 | 38 | |
| tengu (ivy) | **1.2** | 0.08 | 45 | |
| viscous | **1.3** | 0.36 | 45 | |
| magician (sinclair) | **1.3** | 0.55 | 38 | |
| dynamo | 1.1 | 0.5 | 61 | bullet resist 0.625/lvl |
| bebop | 1.1 | 0.115 | 52 | bullet resist 0.3/lvl |
| forge (mcginnis) | 1.1 | 0.171 | 52 | tech resist 0.35/lvl |
| atlas (abrams) | 1.1 | 0.1 | 49 | melee 1.738 |
All other data.js heroes = 1.1. Boon = BOON_COUNT 1 per standard level (2..36): matches code.

## 2. Error register
| # | error | evidence | consumers | decisions affected | corrected result | status |
|---|---|---|---|---|---|---|
| E1 | spirit/level hard-coded 1.1 for every hero | a7/sp.js:11 `std*1.1`; gen/ac1_sp.js:21; gen/spirit3.js:17 `(l-1)*1.1`; heroes.vdata MODIFIER_VALUE_TECH_POWER above. Error at L36 (35 boons): Haze -21.0 SP, Greytalon +17.5, Kelvin/Viscous/Sinclair +7.0, Ivy +3.5 | sp.js -> a7 Threshold lines (a7/w/mk_thr.js T texts) -> data.js `changes` of viscous, sinclair; a14/log/*.md for haze, haze_assassin, kelvin(_support), greytalon(_gun), ivy(_carry), viscous(_damage), sinclair(_bolt); worked examples (see below) | 12 builds' threshold checks (Mystic Burst >80, Tankbuster >165, Spirit Burn >=500/5s, Mercurial Magnum value). Five of six heroes were UNDER-stated, so every PASS stays PASS. Haze builds have no SP-threshold item (a14 log: "no threshold items"). Only possible flip: viscous Tankbuster moved 17.6k->28k because Splatter was 168 vs 165 at SP 110.3; corrected SP 114.9 gives ~+4 damage (~172), still thin, the delay stays defensible | See section 3 | numbers INVALIDATED for 6 hero lines (12 builds); decisions CONFIRMED-UNAFFECTED (severity LOW; no flip) |
| E1b | same constant in wx7/model.py:34-40 (`std*1.1`) | hero = Seven (gigawatt 1.1) | wx7 Seven ult model, seven_worked_example | none, value is correct for Seven | correct but hard-coded: would be wrong for any other hero | CONFIRMED-UNAFFECTED |
| E1c | abtimeline.py (council/tools) reads tp and bdl from heroes.vdata per hero | abtimeline.py:80; I diffed all 44 data.js heroes: 0 mismatches vs vdata | 82 council/sandbox/abtimeline outputs | none | already correct (uses 0.5 for Haze etc.) | CONFIRMED-UNAFFECTED |
| E2 | Haze weapon-investment table above 4.8k "not in extracted data", assumed | haze_model.py:11-12 and haze_worked_example.md line 9 say GAP; heroes.vdata hero_base m_MapModCostBonuses has it: WeaponMod 6.4k 54, 8k **62** (model 63), 11.2k 74, 16k **86** (80), 22.4k **100** (91), 28.8k **115** (100) | haze_model.py -> haze_runs.py/.out -> haze_worked_example.md | only checkpoints with gun invest >=16k (CUR/K paths at 41.6k+, B0 18k+) | rerun with correct table (hm/fix.out): late dmg +2..5% (e.g. CUR 41.6k 1v1 3452->3513, 52.8k 3624->3717). Ranking of paths unchanged except one: 18k heal ordering B0 vs CUR (B0 drops below CUR) | INVALIDATED numbers, conclusions CONFIRMED (low) |
| E3 | haze_model ignores Vitality Investment (health +%), doc calls it GAP | vdata Armor table: 800 9, 1.6k 12, 2.4k 15, 3.2k 20, **4.8k 38**, 6.4k 42, 8k 46, 11.2k 50, 16k 54, 22.4k 60, 28.8k 66 ("Health Increases", loc key Citadel_ModBonus_ArmorInvestmentDesc). haze_model.py:79 `HPMAX = 730+33(lvl-1)+items`, no multiplier. Also wx7/model.py:`hp=` same omission (info column only) | haze_model/haze_runs/haze_worked_example (all "dies N s", "endHP", F1/F2/F5 rows, K1/K2/R1/R2/B0 rows, Q1-Q6 marginals) | The weakness-process "Haze" verdicts: delay-greens vs Ricochet-first, B0 conventional vs CUR, Healing Tempo/Booster value (survival-based). Health-heavy paths are undervalued | Rerun (hm/runs_fix.out, assumes multiplier on base+item HP): CUR 10k dies 9.5s -> 11.3s; CUR 14.4k dies 6.9s -> 9.1s; CUR 18k dies 8.1s -> 11.0s, 24k dies 10.2s -> survives 24%HP, 30k 17%HP -> 45%HP; K1 stays worse (6.7s vs 11.3s at 10k) so "do not Ricochet-first" holds. B0 vs CUR flips at 14.4k (B0 barely survives 0%HP vs CUR dies 9.1s -> CUR better; base said B0 better). R1 spirit hybrid improves a lot (24k+: 7.9s -> 9.6s, 41.6k dies 5.1 -> 8.9s) so "R1 rejected: behind 14-41k in survival" is weaker. Multiplier base (base vs base+items) is itself unverified | survival numbers INVALIDATED; direction of the headline (K1 worse) CONFIRMED; order of other paths NOT reliable |
| E4 | Point model = one strict queue (an entry waiting for AP blocks later unlock entries) | sp.js:9-10, prac/ap.py, haze_model.lvl_state, wx7/model.py:state. abtimeline.py default model_A is two queues (unlocks independent). Which is real game behaviour is not in the data | all consumers above + a7 tiers[] in every a14 log | 24/81 builds' timelines differ (paige ratking_grenade venator victor victor_gun violet_spirit viscous viscous_damage wraith yamato yamato_brawler geist mcginnis mcginnis_turret mcginnis_ult warden lash mirage vyper sinclair sinclair_bolt graves ivy_carry nurse); shifts 300-1800 souls except nurse 5500. Item-relevant (an enabling item bought inside the window): **nurse** Compress Cooldown @6400 on Wretched Vapors (unlocked @1400 two-queue vs @6800 strict); **lash** Mystic Burst @2400 (Grapple T1 1400 vs 3200; abtimeline already shows only +9% margin: Flog 88 vs 80 at SP 26). All other 22 have no dependent item in the window | no single corrected value; both models must be reported. nurse: imbue on a locked ability under strict; fine under two-queue. lash: thin under either | UNRESOLVED (needs the live-game check); severity MEDIUM for 2 builds, none for 22 |
| E5 | First-point model B (abilities 1-3 pre-unlocked, 1st point = T1) | council/tools/abtimeline.py model_B, gen/ac_tl.js timesB, gen "four-way check". Data against B: (a) m_bStartTrained=false for all Signature 1,2,3,4 of every hero (66/66/65/66; dash is true so the flag works); (b) EAbilityUnlocks grants exactly 4, at L1/3/5/8, separate from AP; (c) AP total = 32 (L2..L36 minus 3 unlock levels) = 4 abilities x (1+2+5) exactly; B would need 33; (d) build `order` is always 16 = 4 unlocks + 12 tiers (builds_check ORDER_LEN), B needs 13 | gen/ac*_out*.md, a14/a17/a19 "no dead items" statements; Kieran's stated fact | Model A (data) is correct with high confidence. Items judged "OK" only under B: abtimeline rows where B differs: 19 (greytalon Extra Charge 800, paige_support Extra Charge, rem Extra Charge, yamato_brawler Recharging Rush, vindicta_sniper Extra Charge/Tankbuster/Mystic Reverb, mcginnis_turret Extra Charge/Spirit Burn, mcginnis_ult + lash Mystic Expansion, paradox Tankbuster/Mystic Reverb, baba Extra Charge, baba_tank Extra Charge, sinclair_bolt Extra Charge/Rapid Recharge, graves_ult Echo Shard, drifter_spirit Spirit Burn) | all 24 abtimeline flags are in council/sandbox/abtimeline/_all.json (flag != null); not repeated here. Tier cost 1/2/5 only inferred (F4) but 4x8=32 supports it | B INVALIDATED; A CONFIRMED from static data (live check still outstanding) |
| E6 | souls->level, unlock/AP per level | heroes.vdata m_mapLevelInfo identical for all 46 non-disabled heroes (plus hero_base) and equals a7/levels.json (diffed cell by cell) | all | none | - | CONFIRMED-UNAFFECTED |
| E7 | spirit investment table | a7/levels.json `tech` == hero_base Tech table; no hero overrides any slot table | sp.js, abtimeline, wx7, haze_model, cost_*.js, gen/spikes | none | WeaponMod/Armor tables had to be added to haze_model only | CONFIRMED-UNAFFECTED |
| E8 | item prices 800/1600/3200/6400 (T5 16000) | prices are not in abilities.vdata (only tier). Consistent with invest thresholds being multiples of 800. sp.js C={1..4} has no tier 5 (NaN); no build contains a T5 item (checked) | everything | none found | cannot verify from gt data | UNVERIFIED (no contradiction) |
| E9 | threshold constants | Mystic Burst MinimumDamage 80, Tankbuster 165, Spirit Burn DamageThreshold 500/5s, Mystic Reverb 100, Recharging Rush 200/3.5s, Witchmail 75 match items_full | THRESH checks | none | - | CONFIRMED-UNAFFECTED |
| E10 | spirit-power composition in sp.js itemSP | omits Boundless Spirit TechPowerPercent +15%, Extra Charge/Rapid Recharge +7/+14 on charged abilities, Surge of Power imbue 28 (a14 logs add these by hand); counts SpiritPower of Counterspell 20, Mystic Shot 7, Healing Nova 8, Alchemical Fire 10, Veil Walker 6 as permanent (abtimeline marks only Arcane Surge, Magic Shield conditional) | sp.js, ac1_sp.js, spirit3.js | mostly conservative (omissions) ; over-count only for Mystic Shot (violet*, lash* core, bought at 7.2-8k, after their thresholds), Alchemical Fire (sinclair 40k, doorman_support opt), Healing Nova (rem, solomon_support), Veil Walker (permanent per tooltip history, "6 spirit now" in bebop log) | none flips | UNVERIFIED which SpiritPower props are always-on; severity LOW |
| E11 | resist model | wx7/model.py:93 `(1-(resist-shred))` additive; haze_model `BR` summed additively, cap 60, enemy resist constant 0.20; per-level resist (dynamo 0.625 bullet/lvl, kelvin 0.625 tech/lvl, bebop 0.3 bullet/lvl, forge 0.35 tech/lvl) not modelled anywhere | wx7 Seven model, haze_model | stacking rule not in the data. No tool for dynamo/kelvin/bebop/mcginnis uses resist | - | UNVERIFIED, no consumer for per-level resist |
| E12 | soul income / timing | no income model exists in code (grep). Times like "8:00 ~7k" live only in docs. All timelines treat souls = cumulative item cost (sells not refunded, bank = 0) | every "souls" axis | rank statements like "Ricochet 3 min earlier" cannot be supported | - | UNVERIFIED (R only) |

## 3. Re-run of affected sp.js quotes (TP corrected; same order/builds as data.js now)
| build | check (as logged) | old | corrected |
|---|---|---|---|
| greytalon | Mystic Burst @1.6k SP | 15.4 -> arrow 80+15.4+7=102 | 17.4 -> 104 (pass) |
| greytalon | Tankbuster @12.8k SP | 98.9 (346) | 108.4 (365) |
| greytalon | Spirit Burn @41.6k / Reverb @48k | 156.3 / 182.4 | 172.8 / 199.4 |
| greytalon_gun | Mercurial Magnum @28.8k, 20+0.38xSP | 95.8 (56.4/bullet) | 109.8 (61.7/bullet) |
| kelvin | Spirit Burn @48k | 194.4 | 201.2 (still >500/5s) |
| viscous | Mystic Burst 7.2k / Tankbuster 28k / Splatter T3 Tankbuster 17.6k | 69.2 / 143.8 / SP110.3 | 71.6 / 149.4 / 114.9 |
| viscous_damage | Tankbuster @16.8k / Spirit Burn @49.6k | 94.2 / 168.5 | 98.6 / 175.5 |
| sinclair_bolt | Mystic Burst @2.4k / Tankbuster @16.8k / Spirit Burn @48k | 30.5 / 107.2 / 228.4 | 31.5 / 111.6 / 235.2 |
| ivy, ivy_carry, kelvin_support, sinclair | no threshold item | - | - |
| haze, haze_assassin | no threshold item; Smoke T3 (cleanse/50% lifesteal) timing is point-model not tp | 38.5 SP at L36 | 17.5 |
Haze note: haze_worked_example.md line 16 says sp.js is "about +18 too high at level 36"; arithmetic is 35 x 0.6 = +21.

## 4. Worked examples and council outputs
| artefact | uses | status |
|---|---|---|
| haze_worked_example.md / haze_model.py / haze_runs.* | 0.5/lvl correct, 730+33, 5.26+0.143 correct; **E2, E3 wrong**; haze_runs.out is stale vs current haze_model.py (41.6k+ columns differ, I re-ran in place) | numbers INVALIDATED (E3 large), headline CONFIRMED |
| seven_worked_example.md, wx7 | 1.1 correct, HP 730+41/lvl correct; vitality invest omitted (HP info only) | CONFIRMED-UNAFFECTED |
| victor_gun/victor_spirit, wraith, abrams, abrams_melee (prac/*.py, weaknesses/*.md) | bullet/level 0.26 / 0.14 / 0.1, HP/lvl 35 for wraith, spirit 1.1 all match vdata; weapon cycle/clip match (0.198/24, 0.0945/52, 0.63/9) | CONFIRMED-UNAFFECTED |
| council/sandbox/abtimeline/* (82 files) | per-hero tp/bdl from vdata (E1c) | CONFIRMED-UNAFFECTED by E1 (see E4/E5 for model choice) |
| cost_gen/cost_swap/cost_manual, gen/spikes.js | hero-independent invest tables; cost_swap TH = [4800,6400,8000,16000] ignores the 11.2k, 22.4k and 28.8k steps (28.8k is +25 spirit, +15 gun, bigger than 4.8k's +19 spirit) | CONFIRMED-UNAFFECTED, gap only |
| ledger.js, validate.js, loadout.js | no hero stats | n/a |

## 5. Build impact (81 builds)
- No data.js build decision is shown to flip from E1. Builds whose logged numbers are wrong: greytalon, greytalon_gun, kelvin, kelvin_support, ivy, ivy_carry, viscous, viscous_damage, sinclair, sinclair_bolt (SP too low), haze, haze_assassin (SP too high, no SP threshold). data.js `changes` text quoting sp.js numbers: viscous [7] (also stale: says Mystic Burst at 1.6k, the build now buys it at 7.2k) and sinclair_bolt [1]; nothing in the user-visible notes quotes a wrong SP.
- E4 decisions at risk: nurse (Compress Cooldown imbue 6400), lash (Mystic Burst 2400, +9% margin).
- E5: the 24 abtimeline flags are the real point-model fallout (list in _all.json).
- E3/E2: no data.js build was changed by haze_model (council/work/haze.js proposal is UNAPPROVED), so no shipped build is contaminated; the proposed K1 "Lost lane" reorder and the Healing Tempo/Booster claims in haze_worked_example are.

## 6. haze_model.py assessment (council/sandbox/weaknesses/haze_model.py, 204 lines)
Can it support build-order claims? Only coarse, same-colour comparisons ("Ricochet-first dies sooner than Fortitude-first at 10k"), and even that with E3 corrected. Not item-vs-item rankings across colours, not absolute survival times.
| assumption | where | validated? |
|---|---|---|
| enemy = one target, 2500 HP, resist 0.20 fixed | fight(enemy_hp, resist) | no, no source |
| accuracy 0.5, headshot 0.2, crit x1.65 | fight(acc, head) | no (1.65 not found in vdata) |
| enemy DPS = k x the player's own CUR 1v1 dps at same souls (k 1 or 2), focus for 12 s, smoke ready | haze_runs.survive | no; self-referential, not a real enemy |
| no farming, no income, no later purchases, inventory static at checkpoint, bought in path order with all souls spent | owned_after | no; cannot rank "earlier Ricochet pays back" (doc itself marks UNSUPPORTED) |
| healing = lifesteal% x damage dealt x amp; no incoming heal, no enemy heal reduction | fight | partly (lifesteal values from items_full); amp on lifesteal = [U] |
| vitality invest ignored | E3 | wrong (data exists) |
| gun invest table >4.8k | E2 | wrong |
| Spiritual Overflow: `FR += 0`, bonus spirit 30 / fire rate not modelled; Surge of Power imbue +28 not modelled; Extra Charge/RR spirit stored in SPI_SMOKE, never used | stats() lines 69, 77-78 | R1 "spirit hybrid" and B0 are handicapped; "R1 rejected" is not supported |
| Lucky Shot = flat x1.25 | fight | approximates 25% x +100%; "cannot crit" ignored |
| Active Reload 1.0 s timed reload, Bullet Dance uses no ammo, Siphon 2.5% of enemy_hp every 1.2 s on every hit, Burst Fire 9 s cd | marked [U]/ASSUMED in code | no (item numbers from vdata, mechanics not) |
| Healing Tempo trigger switch (none/siphon/vb) | arg | unknown mechanic (doc item 8) |
| Fixation T3 0.00035 x WD (units of WD%) | fight | unchecked units |
| Reproducibility | committed haze_runs.out differs from current haze_model | stale output |
Grade: CALCULATED at best (doc says UNAPPROVED/UNVERIFIED), no sandbox/measured run behind any number.

## 7. Proposed root-cause fix (not applied)
1. One shared hero-stat loader, used by sp.js, ac1_sp.js, spirit3.js, wx7/model.py, haze_model.py (abtimeline already has it). Minimal sp.js diff:
```
-const G=...;const L=...;
+const G=...;const L=...;
+const V=require('fs').readFileSync('gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata','utf8');
+const hb=(k)=>{const i=V.indexOf('\t'+k+' =\n');const s=V.slice(i,i+60000);const m=s.match(/MODIFIER_VALUE_TECH_POWER = ([0-9.]+)/);return m?+m[1]:1.1};
+const TP=hb(b.hk);
-return {lvl,lvlSP:+(std*1.1).toFixed(1),tier:tier.slice(1)}}
+return {lvl,lvlSP:+(std*TP).toFixed(1),tier:tier.slice(1)}}
```
(b.hk is already in every data.js build; same two-line change in gen/ac1_sp.js:21, gen/spirit3.js:17 and wx7/model.py:`sp=std*1.1`.)
2. haze_model.py: add `VIT_INV` from the Armor table and `HPMAX *= 1+inv_bonus(VIT_INV,inv['v'])/100` (confirm base vs base+items multiplier in game first); replace GUN_INV by the vdata WeaponMod table; model Spiritual Overflow, Surge of Power, SPI_SMOKE or state they are excluded.
3. Add to abtimeline COND_SP the SpiritPower props that are not permanent (decide Counterspell, Mystic Shot, Healing Nova, Alchemical Fire after one live check).
4. Settle E4 (strict vs two queue) with one live observation: unlock ability B while ability A's next tier is unaffordable and see whether the game lets you. Until then keep both in abtimeline.
5. Add a startup assert in every tool: `levels.json` and hero tables equal the vdata (cheap diff, as done in this audit).

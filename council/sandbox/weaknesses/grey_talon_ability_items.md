# Grey Talon (greytalon, "One Shot"): ability timeline x item timing (section M worked example)

Data: game build 6801 (see `council/sandbox/abtimeline/FOUNDATIONS.md`; installed 6819 not checked, F0). Tools: `python3 -I council/tools/abtimeline.py greytalon`, `python3 -I council/tools/abt_orders.py greytalon <label>=<order> ...`. Full timeline: `council/sandbox/abtimeline/greytalon.txt`; gate verdict: `council/sandbox/abtimeline/gate/greytalon.json` (WARN: 1 warning, 0 errors). data.js unchanged (FREEZE); the record is in `council/work/greytalon.js`.

## 1. Kit facts used (abilities.vdata)
- Charged Shot (1): 80 + 1.0x spirit, AbilityCharges 1, cooldown 17 s, between-charge 4 s. T1 +1 charge; T2 +54 damage; T3 between-charge -3 s (4 -> 1) and +1.0x spirit scaling.
- Rain of Arrows (2): cd 25. T1 +3 weapon damage and a 24% slow while airborne; T2 cd -12 (13 s); T3 **while airborne +30% bullet lifesteal, +30% spirit lifesteal, +30% bullet evasion** (citadel_heroes_english `ability_power_jump_t3_desc`).
- Spirit Snare (3): cd 34, T1 -20 (14 s).
- Guided Owl (4, ult): 230 + 0.94x spirit, cd 125. T1 +85, T2 cd -40, T3 execute threshold +22%.
- Gun: 23.51 per bullet, 0.6 s cycle, 17 per magazine, +0.85 per boon.

## 2. Ability timeline, current order 1123141434422233 (model A = game data)
| souls | level | event |
|---|---|---|
| 0 | 1 | Charged Shot unlocked |
| 200 | 2 | Charged Shot T1 (2 charges) |
| 500 | 3 | Rain of Arrows unlocked |
| 1400 | 5 | Spirit Snare unlocked |
| 2000 | 6 | Charged Shot T2 |
| 3200 | 8 | Owl unlocked |
| 6000 | 12 | Charged Shot T3 (the earliest possible: T1+T2+T3 = 8 AP = the 8th AP) |
| 6800 / 9200 / 13800 | 13 / 16 / 21 | Owl T1 / T2 / T3 |
| 7600 | 14 | Snare T1 |
| 14900 / 17400 / 26900 | 22 / 24 / 29 | Rain T1 / T2 / T3 |
| 32100 / 48600 | 31 / 36 | Snare T2 / T3 |

Old model B (1 AP per tier) had Charged Shot T3 at 3900 and Owl T3 at 8400: 2.1k and 5.4k too early.

## 3. Item vs ability timing
| item @ buy | at the buy (tool) | after the next relevant upgrade | cheaper stand-in / alternative | verdict, grade |
|---|---|---|---|---|
| Extra Charge @800 | 2 -> 3 charges, +7 spirit on the arrow (charged-only filter): arrow 90 -> 97. Shots inside 5 s: 2 -> 2 (4 s gap); 3rd arrow at 8 s | Charged Shot T3 @6000 (+5.2k): shots in 5 s 2 -> 3, arrow ~295 at 6.4k | Extra Spirit first: +10 spirit on every ability (arrow +3 more than EC's +7 for the 2.4k souls until Extra Spirit is bought anyway at 3200); no stored 3rd arrow. Delaying EC to 5600: same 4.8k spirit spike (5600), loses the stored arrow for 4.8k souls. Skipping EC: Rapid Recharge costs 3200 straight and the spirit 4.8k spike moves one 800 item later | **Keep (buy now)**. Burst value really starts at 6000 (flag WEAK-UNTIL-UPGRADE, gap 5.2k), but the buy also feeds the 4.8k spike, +7 arrow spirit, a stored 3rd arrow in long trades, and is Rapid Recharge's component. CALCULATED, 55%. Wrong if F8 is wrong (between-charge is not the gap between casts) or if lane trades never last 8 s. |
| Mystic Burst @1600 | needs one ability hit > 80 (proc type ABILITY): arrow 104 (+31%); Snare 25 does not count | Charged Shot T2 @2000: 160 | - | Buy now. CALCULATED. |
| Compress Cooldown @4800 on the arrow | 17 -> 13.9 s per charge (3.53 -> 4.30 casts/min) | no Charged Shot tier changes its cooldown, so the value is the same before and after every upgrade | - | Buy now; timing is neutral to the point order. CALCULATED (F8: cooldown = per-charge recharge, INFERRED). |
| Tankbuster @12800 | arrow 365 > 165 (+121%), Owl 417 | - | - | Buy now. CALCULATED. |
| Recharging Rush @16800 | needs 200 gun damage in 3.5 s: 70/bullet, 6 shots possible = 420 at 100% hits, so 3 body hits; Charged Shot already has 2 charges | none pending (Charged Shot maxed since 6000) | - | Buy now (no ability gate). Hit rate is the risk: UNTESTABLE-HIGH-RISK for real aim. |
| Rapid Recharge @19200 (eats EC) | 2 -> 4 charges, gap 1 -> 0.7 s, cd 17 -> 14.6 s, +14 arrow spirit: shots in 5 s 2 -> 4 | none pending | - | Buy now, full value at once. CALCULATED. |
| Surge of Power @22400 on the arrow | arrow 482 with +28 imbued spirit | - | - | Buy now. |
| Superior Cooldown @28800 | 20% on all four: 25.8 s per rotation | - | - | Buy now. Whether it stacks with Compress by adding or multiplying is UNVERIFIED. |
| Spirit Burn @41600 | 500 spirit in 5 s: 4 arrows x 615 alone (upper bound) | - | - | Buy now. UNTESTABLE-HIGH-RISK (hit rate). |
| Mystic Reverb @48000 on the arrow | arrow 677 > 100 (proc types ABILITY and BULLET) | - | - | Buy now. |

None of the four charge/cooldown items is dead at its buy. The only timing gap is Extra Charge's burst (5.2k souls), and no point order can close it: Charged Shot T3 is already as early as the AP rules allow.

## 4. Alternative point orders as whole builds (items unchanged; `abt_orders.py`)
| order | Charged Shot T1/T2/T3 | Rain T1/T2/T3 | Snare T1 | Owl unl/T1/T2/T3 | arrow at 4.8k / 8k / 12.8k | gains | costs | grade, verdict |
|---|---|---|---|---|---|---|---|---|
| O0 current 1123141434422233 | 200/2000/6000 | 14900/17400/26900 | 7600 | 3200/6800/9200/13800 | 184 / 332 / 365 | arrow T3 as early as possible, Owl maxed by 13.8k | Rain stays at base (cd 25) until 14.9k | **keep**, CALCULATED 60% |
| O1 Rain T1 before arrow T2, 1123214143442233 | 200/2600/6800 | 900/17400/26900 | 8400 | 3200/7600/10100/14900 | 184 / 332 / 365 | Rain T1 (slow, +3 gun damage airborne) 14k souls sooner | arrow T2/T3 +600/+800, Owl tiers +800..1100, Snare T1 +800 | reject for a one-arrow build; CALCULATED |
| O2 Owl before arrow T3, 1123144441322233 | 200/2000/12800 | 14900/17400/26900 | 13800 | 3200/3200/4600/8400 | 184 / 233 / 365 | Owl T2 (cd 85) at 4.6k, T3 at 8.4k | arrow at 8k -30%; Extra Charge burst gap 12k | reject; CALCULATED |
| O3 public consensus, 2134214441133322 | 900/9200/13800 | 200/32100/48600 | 14900 | 3200/3200/3900/7600 | 130 / 179 / 249 | Owl maxed by 7.6k, Rain T1 at 200 | arrow T3 +7.8k (at 8k -46%); Extra Charge bought 100 souls before the 2nd charge | belongs to an Owl/gun style, not this one; CALCULATED |
| O5 Rain before Owl, 1123114322244433 | 200/2000/6000 | 7600/9200/13800 | 6800 | 3200/14900/17400/26900 | 184 / 332 / 365 | Rain cd 13 at 9.2k; **Rain T3 at 13.8k (O0: 26.9k): arrows fired while gliding get 30% spirit lifesteal**, ~110 HP per arrow at 13.8k, ~220-330 per Rain cast | Owl T1/T2/T3 +8.1k/+8.2k/+13.1k: at 12.8k the ult hits 332 every 125 s instead of 417 every 85 s | rival thesis (kit-first: a sustain engine from Rain T3 + charged arrows). UNTESTABLE-HIGH-RISK (aim while gliding), confidence <= 50%: **keep O0**, test first |
| O4 arrow then Rain maxed, Snare last, 1123114222444333 | 200/2000/6000 | 6800/8400/12800 | 26900 | 3200/13800/16100/24600 | 184 / 332 / 365 | Rain T3 at 12.8k | Snare T1 (cd 34 -> 14, the self-peel) +19.3k | dominated by O5 |

Decision: (point order, item order) = (O0, current). The O5 thesis would change other items if it holds (sustain items such as Indomitable's role, Spirit Lifesteal-type items become redundant), so it is a second-playstyle candidate, not an edit.

## 5. Sandbox tests (runnable with existing ops; per-ability tiers via `abil`, logged with `abilist`)
1. `council/sandbox/scenarios/greytalon_charge_tiers_f7_f9.json` + `council/sandbox/autorun/scenarios/gt_f7_f9_charge_bits.txt`: six blocks (bits 1 / 1+EC / 3 / 7+EC / 15+EC / 15). Settles F9 (is `unlock 7` only T2?), F7 (does Extra Charge work on a 1-charge ability? decides 14 gate rows) and Extra Charge's burst before/after Charged Shot T3. Predictions are written in the file.
2. `council/sandbox/scenarios/greytalon_rain_t3_arrow_lifesteal.json` + `autorun/scenarios/gt_rain_t3_arrow_lifesteal.txt`: arrow while gliding at Rain T2 vs T3 vs grounded, heal as % of arrow damage. Decides whether O5 gets a build.
Caveats: `hold` and `cast`+`hold` sequencing are implemented but never exercised; check the `abilist` lines first (a block with the wrong bits is void). Until run, both are INCONCLUSIVE and nothing changes (no evidence/greytalon.json exists yet).

## 6. Was this already being done?
Partly. The ability-check audits (gen/ac_out0..3.md) and the charge audit (gen/proposals_charge.md) checked "charge point before the charge item" and thresholds at the buy point, but on model B (1 AP per tier, 1-3 pre-unlocked) or a strict single queue, a fixed 2+ charge rule, without burst/upgrade-gap valuation, without the trigger fields in the vdata (Echo Shard non-ult, Reverb bullet type, Tankbuster no item procs), and without testing alternative orders as whole builds. For Grey Talon the old verdict (all OK) stands; the timeline adds the Extra Charge burst gap and the O5 rival.

# REVIEW_LOG (instrument validation and self-review)

## 2026-10-24 03:44-04:45 Stage 0 so far (plugin build "arena+async", validated by the suite below)
Changes since the last validated state: arena teleport/enemy placement (Kieran), aim in world units (`aimpt right up`), miss = look straight down (`accuracy p headFrac headUp missUnits`, missUnits now unused), `accseed` (same random hit/miss/head windows in every block), `expect` setup-truth op, `imbueown`, `pos`/BOT logging, EnemyPawn = nearest living active bot, async buffered logging, cached player/bot lookups, usercmd hook rate-limited (no per-usercmd logging), camera updates 60-100 ms, PERF counters per scenario.

### 0.1 Stability
- Disconnects: 02:19 and 03:52 (NETWORK_DISCONNECT_OVERFLOW, 582 ms for 2 Move messages). Cause (unconfirmed but consistent): synchronous File.AppendAllText/Console.WriteLine per log line and per damage row, plus LINQ over Players.GetAll() on every usercmd.
- Fix 03:54: background writer thread, no console writes, cached lookups. PERF after fix: tick hook avg 0.01-0.03 ms, max 28-84 ms (hero swaps in hardreset), usercmd hook max 0.9-9.5 ms.
- Since reconnect at 03:54: continuous scenarios until at least 04:42 without a drop (48+ min). Status: PASS (will keep monitoring).

### 0.2 Setup truth
`expect` logs `VERIFY <label> PASS|FAIL` with hero, level, maxhp, items, ability bits, cooldown busy count, gold, distance, enemies, min enemy distance, enemy hp, resists, extra modifiers. All 40+ validation blocks PASS. Rule: analysis must drop any block whose VERIFY is not PASS (valan.py prints it; an.py not yet wired, TODO before Abrams verdicts).
Findings from the checks: (1) a block that gives a component AND its upgrade holds both items (stats double count); builds must give final items only. (2) `imbue X Signature1` Success for base items; `ItemNotImbuable` for upgrade items; `give <item>` of an imbue-capable item auto-applies to Signature1 (Abrams Siphon). Signature3 for a passive: AbilityRejected. Imbue verified live by effect: Duration Extender +22% Siphon ticks (24 -> 30 in 8.5 s), two duration items stack additively (35 ticks = +50%), Mystic Expansion widens Siphon radius (hit at 400u that base misses).

### 0.4 Known-answer tests (Haze level 18 vs Haze bot, arena, 25-50 bullets per cell, per-bullet damage has ZERO variance)
| test | expected | measured | verdict |
|---|---|---|---|
| body bullet | - | 7.70 | baseline |
| head bullet | - | 12.70 (x1.65; 16.4/9.9 = x1.657) | head multiplier x1.65 |
| enemy gun resist 20% | x0.80 | 6.2 / 10.2 (x0.805) | PASS |
| Close Quarters (+20% weapon dmg <15 m) | +20% | 9.9 at 300-500u (x1.286), 8.4 at 600-750u (x1.09) | PASS: x1.286 = 1.20 + 0.09 shop weapon bonus (800 souls tier), range edge between 500 and 600u => 15 m ~ 590u => 1 m = 39.4u |
| High-Velocity Rounds (+8% base dmg) | +8% (+9% shop) | 9.0 (x1.17) | PASS |
| Extended Magazine (+8%) | same | 9.0 | PASS |
| Rapid Rounds (+9% fire rate) | +9% shots | 21 vs 19 hits (+10%), dmg x1.09 (shop bonus only) | PASS |
| Headshot Booster | +45 head bonus (?) | head/body ratio unchanged 1.65, only shop +9% | UNEXPLAINED (item may need a condition); not usable as known answer |
Conclusions: `give` DOES apply the shop category bonus (weapon spike 800: +9%), so category invest effects ARE present at checkpoints. Distance scale: 1 m = 39.4u (bracket 33-40 by Close Quarters edge; Siphon 8 m radius reached 340u not 380u, consistent with 315u + hitbox). Bullet damage also falls off with distance (300u 7.7, 900u 7.3, CC item at 1100u 6.5).
Realised hit rate: `accuracy 0.45` gave only 25-35% of shots hitting (aim transitions between windows); p=0.55 gave 41% (61/150). Use p=0.55 for "45%" and always report realised hits/(hits+misses).

### 0.3 Noise floor (Haze, 75 shots/block)
- Random windows (no seed): block damage 156/181/217/215 => CV 15% (n=4), hits 19-26. Too noisy for effects under ~25%.
- Seeded windows (`accseed`): hits per 150-shot cell 61/55/60 (CV 5.5%), same seed A vs B hit counts within 0-7%. Per-hit damage ratio B/A = 1.27-1.28 vs 1.286 expected. Paired design adopted (same seed across arms and conditions).
### 0.5 Order effect
ORD sequence A,B,B,A,B,A,A,B (random windows): first block A=212 vs other A 207/227/189: no first-block deficit observed. (Previous "first block low" claim from Victor run NOT reproduced here; kit confound candidates: Victor aura age.)

## Abrams specifics found (affects rotation validity)
- Light melee lands every ~0.75 s (84-94 dmg, repeating 8-step sawtooth at L20: 94,92,90,89,87,85,84), heavy every ~1.65 s (193-213). Melee reaches at least 170u. Aim does not matter for melee.
- Seismic Impact takes ~6 s from cast to landing in the arena (player hovers ~3 s, then slams ~1700u toward aim); no melee possible meanwhile. Shoulder Charge needs the camera on the target before casting (use `aim 0.3` after `fetch`) or it runs the wrong way.
- Melee damage numbers at the first 5k checkpoint come from Abrams at L8 with 4 items.
- UNSUPPORTED: wall stun for Shoulder Charge (no walls in arena), knockback behaviour, ult landing placement.

## 2026-10-24 04:53 Abrams A/A (pre location patch; every block passed VERIFY dist=120, start pos logged exactly 12197.9/2625.8, enemy +120)
Abrams 10k duel45, L15, 7 items, 4 reps x (warm, A, A2), seeded accuracy, melee-range rotation (MEASURED instrument noise):
- dps: A 51.5 vs A2 50.6, CV 5.3%, paired diff mean -0.9, sd 2.8 (5.5%). Usable for effects above ~10% (2 sd).
- hps: A 88.8 vs A2 110.0, CV 42% (r4 A = 25.8 vs ~96-119 elsewhere); loss/s CV 15.5%, paired sd 20.8. NOT measurable at this design: heal/loss verdicts for Abrams are "cannot measure reliably" until outlier cause found (suspect timing of Seismic Impact/charge vs incoming windows).
- No order effect (A, A2 swapped on even reps; diff ~ -1 dps).
## 2026-10-24 04:55-05:04 Location patch (Kieran/coordinator): SETUP VERIFY, ArenaGuard (new pawn only), FetchVerify
- Found bug: setup verify used arena+350 while a prior `fetch 40` left _dist=40 and the maintain loop; hardreset+fetch 40 then stuck 'moving enemy' for minutes. Fix: setup waits on _dist, hardreset resets _dist.
- Regression pv_test (hardreset + fetch 40/150/350/1000, Atlas/Haze/Wraith swaps): PASS, every `POS VERIFY ok` exact (dist=40.0/150.0/350.0/1000.0, dz 0), SETUP VERIFY ok at arena each swap.
- The ~940u mid-block displacement is rotation motion (Shoulder Charge/Seismic Impact travel), not setup: block starts are verified by `pos`/`expect`.
### 2026-10-24 05:12 Regression suite after location patch (build 05:02): PASS
val_aa2 (unique labels): 36 blocks all VERIFY PASS, bullet value sets unchanged (7.7/12.7 body/head, 9.9/16.4 with Close Quarters), pv_test exact positions, 25 min stable. Results from here on VALIDATED for location.

## 2026-10-24 05:25 Generator bug found: ability_bits gave a learned-but-untiered ability bits=1 (free T1)
`UpgradeBits` are tier bits (T1=1, T2=3, T3=7); learning is free (souls-gated) and hardreset leaves every ability IsUnlocked=True. ovlib.ability_bits set 1 on learn => unlock-only abilities carried a free T1. Fixed (learn = 0). Consequences: Abrams A/A (04:42-04:52) ran with bits 1,3,1,7 (true plan ~0,3,0,7 -> actually 1,3,1,7 includes free T1 on Siphon and Infernal Resilience); both arms identical so the noise floor stands, but Abrams absolute kit state is UNVALIDATED (tier overstated). Rerun Abrams with the fixed generator before any Abrams verdict.
- Wraith 5.6k plan check: 5600 souls -> L9, bits Card T2, FA T2 (3,0,3,0) = weakness-file timeline; 16.8k -> L22, (7,3,7,0) = Card T3, PM T2, FA T3.
- PR-0 (Wraith, accuracy 1): `fire 12` continues through the reload: 52 shots in ~4.9 s, ~2.5-2.8 s gap, then resumes (96 bullets in 12 s). So `fire N` is elapsed-time based and counts reload; use it directly. Note a block with no lvlhold sits at level 87 / 151.8k gold: always lvlhold.

## 2026-10-24 05:58 CORRECTIONS (audit by coordinator, confirmed)
1. `accseed` was NOT in the running plugin build (62 "unknown op accseed" lines 04:36-05:45). Earlier claims "seeded windows, CV 5.5%, paired design" are WITHDRAWN: every result so far (Abrams A/A, val_aa2, pw1 first run) used unseeded random accuracy windows. Abrams A/A dps CV 5.3% stands as the REAL unseeded noise for that rotation (n=4 reps). accseed now implemented in src (reseeds the RNG at each `accuracy` op; reset on scenario start); needs build + identical-sequence check (seedtest) before use.
2. UpgradeBits schema: bit0 = unlocked, T1 = 3, T2 = 7, T3 = 15 (FOUNDATIONS.md). Previous generator emitted tiers one step too low (learn=1, T1=1, T2=3, T3=7) then "fixed" to learn=0 (locks the ability). Now [1,3,7,15]. Consequences: Abrams A/A ran bits 1,3,1,7 meaning Siphon learned only (no T1), Charge T1, passive learned only, ult T2: plan was (L15) 1,7,3,15 -> Abrams A/A kit state UNVALIDATED (noise result still valid for that kit). pw1 run in progress (started 05:21) used bits Card 3 (T1), PM 0 (locked), FA 3 (T1), Tele 0: gun A/B no-FA cells are valid as gun comparisons (abilities not cast), FA cells are FA T1 not T2/T3 (no unlimited ammo) and must be rerun. "unlock 7" runs (Abrams ult) were T2, not max.
3. Not claiming any result as build evidence: FREEZE 05:46, tester not validated.
### 06:03 accseed implemented and verified (build 06:00)
seedtest (Haze, accuracy 0.55 head 0.25, 4 blocks): seed 7 blocks a/b/d -> windows=67 missWindows=33 headWindows=13 in all three; seed 9 -> 67/34/7. Window sequences are identical per seed and differ across seeds. Landed hits per block still vary (38/34/36 for seed 7) because shot timing vs window edges differs by ~100 ms: paired design reduces but does not remove noise. Real noise to quote: Abrams unseeded dps CV 5.3% (n=4); Wraith 100%-accuracy blocks have ~0.3% sd (deterministic), 60%-accuracy unseeded sd 17-19% (pw1).
### 06:00 pw1 (Wraith PR-W1 first run, UNSEEDED, FA cells at FA T1, UNVALIDATED kit tiers) instrument finding
Item clip-size bonuses (Titanic +100%) only apply after the next reload: the first magazine of a block after `give` is still base size (B's first gap at 4.9 s = 52 rounds). Every gun test must `cast reload` before firing. pw1 B therefore understated; pw2 adds the reload.
### 06:16 Foundation check gt_f7_f9 (results/foundation_gt_f7_f9.md): bit schema 1/3/7/15 = unlocked/T1/T2/T3 CONFIRMED; Extra Charge on a 1-charge ability adds a charge CONFIRMED. ovlib.ability_bits now emits [1,3,7,15] (06:00). Client interference 06:06-06:11 (selecthero hero_punkgoat, buyitem lines not from scenarios) aborted bitstest block 4.
### 06:58 pw2 (Wraith PR-W1, seeded, clip live): 52 blocks VERIFY PASS; results in results/wraith_gun_PR-W1.md. Instrument note: first magazine after `give` is base size (clip bonus applies after reload): fixed with `cast reload` in every gun block.

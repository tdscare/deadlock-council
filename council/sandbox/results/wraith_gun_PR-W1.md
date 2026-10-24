> **SCOPE WARNING (Kieran 12:26): ISOLATED ITEM DATUM, NOT A BUILD VERDICT.** Wraith's own build already owns Quicksilver Reload (imbued but NOT cast in this test), Mercurial Magnum and Vampiric/ammo effects, which can make magazine size largely redundant. This test did not cast Quicksilver Reload or model reload avoidance, so it cannot say whether Titanic Magazine improves the complete build vs other uses of the same souls. Do not use as a purchase recommendation.

SCOPE: isolated
VALID: yes (scope: sustained 20 s stationary-target damage only; Stage 0 gates: stable >2 h, POS/SETUP VERIFY ok at every block start, all 52 pw2 blocks VERIFY PASS, accseed verified 06:03, `cast reload` before fire so clip bonuses are live, ability tiers read back by `abilist` per block; 100%-accuracy cells deterministic sd 0-1%)
# Wraith PR-W1: Swift Striker (A) vs Titanic Magazine (B), 2026-10-24 06:19-06:58. FROZEN data.js: proposal evidence only, NOT build evidence.
Build state: 5.6k = L9, Tesla + gun item, bits Card T2 / FA T2 (7,1,7,1); 16.8k = L22, Tesla, Monster Rounds, Quicksilver(imbued, not cast), Surge of Power, Ricochet + gun item, bits Card T3 / FA T3 (15,7... read back). Enemy Haze 350u, resist 5%/12%gun. Gun item only differs. 4 reps per cell, order A,B / B,A alternated, accseed = rep. Metric: weapon damage in the 20 s after the first shot (reload included); burst = first 3.5 s.

| cell (acc, FA) | A dps | B dps | B vs A | shots 20 s A/B | per hit A/B | burst 3.5 s B vs A | tag |
|---|---|---|---|---|---|---|---|
| 5.6k, 100%, no FA | 73.1 | 93.0 | +27.2% | 156 / 181 | 9.38 / 10.28 | -8.1% | MEASURED |
| 5.6k, 100%, FA T2 | 75.0 | 105.8 | +41.1% | 160 / 206 | same | +3.3% | MEASURED |
| 5.6k, 60%, no FA | 37.9 | 46.5 | +22.8% (sd 6) | 80.8 / 90.5 | same | -12.8% | MEASURED, noisier |
| 16.8k, 100%, no FA | 109.7 | 147.1 | +34.1% | 167 / 207 | 13.14 / 14.20 | -12.7% | MEASURED |
| 16.8k, 100%, FA T3 | 159.0 | 170.3 | +7.2% | 242 / 240 | same | -3.2% | MEASURED |
| 16.8k, 60%, no FA | 54.4 | 76.1 | +40.6% (sd 8) | 82.8 / 107.3 | same | -7.9% | MEASURED |
Calculation in the weakness file predicted +32% / +44% / +48% / +19%: measured +27 / +41 / +34 / +7 (calculation overstated the gain by 5-12 points).

## Kit explanation (confounds checked)
- A = +20% fire rate and +0.75 m/s sprint; B = +100% clip and +14% weapon damage (measured +9.6% / +8.0% per hit after resist). Reload is unchanged 2.82 s. B's damage per hit is an extra role of the item (damage), which the weakness file's reload-share model left out; the measured gain includes it (per-hit +8-10% is about a third of the 5.6k gain).
- Sustained gain comes from fewer reload pauses (A gaps 3.0 s x2-3 per 20 s; B gap x1) and +8-10% per hit; burst loss comes from the 20% fire rate: first 3.5 s -8 to -13% without FA, near zero with FA.
- Full Auto T3 (16.8k) provides unlimited ammo for its duration, so clip adds little there (+7%).
- NOT covered by this test (item roles, Section J): sprint speed (-0.75 m/s for B), Quicksilver refill on Card cast (shortens A's reload share; not cast here), Mercurial/Surge buffs, multi-target (`enemies 3` not run), card resource (+hits per second favours A in burst), build-up items (Silencer/Inhibitor reach), what each item builds into (Swift Striker -> nothing here; Titanic -> upgrade options). Fight duration distribution is an assumption: B wins when fights are longer than ~4-5 s of continuous fire; A wins on 2-3 s peeks.
## Verdict (proposal only)
Titan wins sustained 20 s damage in every cell, by +23% to +41% except under FA T3 (+7%). First-3.5 s burst is lower by 3-13%. Real-play benefit depends on how long fights run continuously (enemy reactions, positioning): UNTESTABLE-HIGH-RISK for the decision, so capped at 50% confidence: 50% that the swap is better in real play. It cannot justify a core change alone; suggest as a situational pivot candidate for the Council ("long trades / sustained fire -> Extended -> Titanic instead of Rapid -> Swift") together with a multi-target + Quicksilver-cast follow-up.
What would make this wrong: fights shorter than ~5 s; Quicksilver/Surge casts refilling the magazine often (not measured); sprint speed mattering for kiting; fire-rate/clip stacking with Overflow/Mercurial differing from additive at the 29.6k+ checkpoints (not tested); stationary 100%/60% accuracy targets.

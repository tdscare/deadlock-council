VALID: yes (scope T4 only; T5 inconclusive. 18/18 blocks VERIFY PASS: hero Frank L20, bits 7/15/7/7 per plan, enemy Haze 350u; order counterbalanced over 3 reps; per-hit damage deterministic)
# Victor gun T4/T5, 2026-10-24 07:01-07:09. MEASURED, sandbox only, NOT build evidence (data.js frozen).
## T4: does self-damage feed Berserker (+7 weapon power per 120 damage taken in 10 s)? Berserker only, 3 reps x 4 conditions, fire 3 s at 100% accuracy after `cast reload`.
| condition | damage actually taken (damage csv) | per-hit gun damage (all 17 hits identical) |
|---|---|---|
| control | 0 | 32.98 |
| `cast 2 0.4` (Jumpstart: 15% current HP self-damage) | 217 | 34.94 (+5.9%) in 3/3 reps |
| `hurtme 500` | 0 (no damage row, no event) | 32.98 |
| `incoming gun 200` for 3 s (600 damage taken) | 597-600 | 32.98 |
Reading: Jumpstart's real self-damage (217 = 1 stack of 120) raised bullet damage by one stack's worth and it is present from the first bullet; the tester's `incoming` (600 taken = 5 stacks worth) and `hurtme` did NOT feed Berserker at all. So (a) GC4 answer: self-damage from Jumpstart DOES feed Berserker (MEASURED, 75%: the +5.9% could also come from Jumpstart itself, but nothing in its kit raises bullet damage; not separated); (b) tester limitation: every test that relies on `incoming`/`hurtme` to trigger damage-taken effects (Berserker, Infernal Resilience, Pain Battery charge, Frenzy thresholds) is biased: those hooks are not exercised. Earlier Abrams P1 (heal 147 vs loss 1776) must be read with this in mind.
Decision impact (proposal): Jumpstart then fire is a Berserker engage pattern worth one stack per ~120 damage (about +6% per stack); no item change. Confidence 55%. Wrong if: Jumpstart itself adds damage; stacks decay (10 s) before use; per-stack value differs at other levels.
## T5: Pain Battery fed by self-damage? INCONCLUSIVE.
`cast 1 0.5` dealt `ability_frank_shocktarget2` 183.44 in every arm, including control with no stored damage and no Aura/Jumpstart/incoming. So either slot 1 is not charge-gated the way the kit text says, the battery starts charged after hardreset, or the 183.44 row is another effect. Cannot decide whether self-damage charges it. Would need: read the Pain Battery modifier/ammo with `mods` before and after, and a second consecutive cast to see recharge. UNTESTABLE as scripted.

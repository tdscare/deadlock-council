# Abrams (Atlas) probes, 2026-10-24 05:17 (build validated 05:12; abilities unlock 7 = upper bound, NOT checkpoint-true)
Tags per WEAKNESS_PROCESS H. Single runs unless stated.

| probe | result | tag / confidence | what would make it wrong |
|---|---|---|---|
| P0 u per metre (Siphon ring) | 8 m Siphon radius cut between 315 and 340u (earlier imbue tests: hit at 340u not 380u) => 1 m ~ 39.4u (bracket 33-40 from Close Quarters edge 500-600u / 15 m) | MEASURED (coarse) 80% | ring bot hitbox radius adds ~25u, so true 8 m could be 315 |
| P1 do incoming hits feed Infernal Resilience? | L35-equivalent Abrams, 6 s stream of `incoming gun 300`: loss 1776, heal 147 (8.3% of loss) over 19 s; control (no stream) heal 0 | MEASURED 60% that the hook is fed (heal>0 only with damage); magnitude 147 vs expected 13% x 1776 = 231 unresolved (single run, regen cap, ult point-state unknown) | a single run; heal may be Pain of base regen reacting to damage rather than Resilience |
| P3 imbue auto-apply | `give` of imbue-capable items lands on Signature1 (Siphon): Duration Extender +22% ticks, Mystic Expansion widens radius | MEASURED 85% (see REVIEW_LOG 0.1) | none known |
| P4 Mystic Slow on Siphon | enemy at 300u carries `upgrade_magic_slow/modifier_tech_resist_debuff_proc/mystic_slow_debuff` at +1.0 s, +2.0 s, +4.0 s after `cast 1 2`, absent at +8 s | MEASURED presence 80%; magnitude/stacking UNTESTABLE (names only) | modifier name may come from another source |
| P5 ult answer (Unstoppable) | samples at +2/+5/+9 s of `cast 4`: leap_active, bull_leap_boosting (hover), boosting_crash (slam); no Unstoppable-named modifier seen | MEASURED absence at 3 sample times only, 40%; unlock 7 included T3 so the 5 s Unstoppable should exist if modeled as a modifier | sampling gaps; effect may be a flag not a modifier |
Kit confound note: Siphon is the Signature1 imbue target for Duration/Expansion/Compress items; Infernal Resilience is passive and only reacts to damage taken; Charge/ult motion moves the player up to ~900u mid-block (positions re-asserted at every block start).

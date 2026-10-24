# MORNING (overnight sandbox run, updated 2026-10-24 ~07:10)
data.js and all builds untouched (frozen by Kieran 05:46). Nothing here is build evidence; everything is a proposal with tags.

## Status
Stage 0 gates: stability PASS (>3 h since 03:54 fix), setup truth PASS (VERIFY per block), position truth PASS (SETUP/POS VERIFY exact), seeded accuracy PASS after fix (it was missing from the build until 06:00), known-answers PASS (head x1.65, resist, Close Quarters threshold both sides, shop bonus), A/A noise: Abrams unseeded dps CV 5.3%, Wraith 100%-accuracy deterministic. Pilots: Wraith gun PR-W1 done; Abrams probes done; Abrams checkpoint/tank scoring and Victor T4 done, T5 inconclusive; Victor spirit T2, Leech vs Vampiric Burst, Abrams scoring not started.

## Optimal vs not (proposals, sandbox only)
- Wraith gun (results/wraith_gun_PR-W1.md): Titanic Magazine beats Swift Striker in sustained 20 s damage by +23..+41% (+7% under Full Auto T3), burst first 3.5 s -3..-13%. Real-play value depends on fight length: capped 50%; situational-pivot candidate only, not a core change.
- Victor gun T4 (results/victor_gun_T4_T5.md): Jumpstart self-damage feeds Berserker (+5.9% per stack, MEASURED 75%); T5 Pain Battery inconclusive. `incoming`/`hurtme` do NOT trigger damage-taken effects: any survival/low-HP result built on them is biased.
- Abrams: only instrument/probes (results/abrams_probes.md); DPS noise 5% usable, heal/loss noise 42%/15% NOT usable.

## Proposed changes
None to data.js. Candidate for Council: Wraith situational note "long trades: Extended -> Titanic instead of Rapid -> Swift" (50%).

## Netchan fix (logged)
Two disconnects (02:19, 03:52, NETWORK_DISCONNECT_OVERFLOW). Cause: synchronous log/console I/O and LINQ per usercmd. Fix 03:54: background writer, cached lookups, no per-usercmd logs. No drop since.

## Corrections made tonight (honest list)
1. `accseed` was missing from the running plugin from 04:36 to 06:00 (62 "unknown op"); every earlier "seeded/paired/CV 5.5%" claim is withdrawn. Implemented and verified at 06:03 (identical window sequences per seed).
2. Ability tier bits were wrong: correct schema 1/3/7/15 = unlocked/T1/T2/T3 (confirmed on Grey Talon Charged Shot damage +54 T2, T3 faster recharge; Wraith Full Auto cooldown 45 -> ~25 s at bits 3). Earlier `unlock 7` and Abrams A/A kit states were lower than labelled: Abrams A/A kit UNVALIDATED (noise valid).
3. Arena setup bug (setup stuck when fetch distance != 350 after hardreset) fixed; the ~940 u mid-block displacement was Charge/ult travel, not setup. Block starts were verified by `pos`/`expect`.
4. Item clip bonuses only apply after the next reload; gun blocks now `cast reload` first.
5. Something else drove the game client 06:06-06:11 (selecthero hero_punkgoat, buyitem lines): bitstest block 4 invalid; keep the client free.

## Tester limitations / uncertainties
- No walls/height (Shoulder Charge stun, Lash untestable), no anti-heal/CC ops on the enemy, no NPCs (farming UNSUPPORTED), `abil` bypasses the point-spend rules (ability-point queue check not testable).
- Realised hit rate for `accuracy p` is below p; headshot booster known-answer unexplained; melee/ult timing depends on animations (capped 50%).
- Quicksilver/Mercurial/Surge interactions, multi-target and Ricochet bounce roles not yet measured in the Wraith swap (Section J).
- Abrams heal/loss metrics unusable until the A/A outlier (block with 25 hps vs ~100) is explained.

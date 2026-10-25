# Council Mode batch 1 — pre-registration (written BEFORE any of these tasks run)
Session: council-mode-2026-10-25-0004Z. Executor: existing Sandbox QueueRunner via `sbx_q add` command files. Heroes: Haze and Drifter only (forced casts verified for Haze/Drifter/Nurse; Viscous casts still blocked). Scenario files: `/mnt/user-data/outputs/arena/sc_novel/` -> `E:\deadworks-server\scenarios\` (copied to `plugin/arena/sc_novel/` in this repo with this commit).

## Validity rules, fixed in advance (apply to every task)
- Runner verdict `VALID: yes` in the raw result json, client version == server version in that json, `humanClientInput 0`, `forcedExternal 0`, `verifyFail 0`.
- Frame validity by `frame_validity.py` must be CLEAN (any frame >250 ms inside a timing-sensitive step => not accepted). These batches read cooldowns, damage rows and hit counts, not timings, so a `flag(non-timing)` run is reported but its numbers must still be identical to the clean run to count.
- n_min (decided now): every arm is measured in >= 2 blocks (forward + reversed order, already in each scenario's rotation) AND the task is run twice as separate valid tasks (replication) before a finding is called CONTROLLED SANDBOX RESULT. One valid run = PRELIMINARY. Disagreement between blocks = INCONCLUSIVE, not averaged.
- Build hash is whatever the runner/plugin.log records at task start; if not recorded in the raw file it stays labelled INFERRED and cannot satisfy the provenance gate.
- A task that is BLOCKED/INVALID is reported as such. Nothing in this batch is a purchase verdict or changes data.js / the 81 frozen builds.

## Tests (priority order), hypothesis / baseline / comparison / what it would change
1. **N01 `nv_N01_multi_imbue`** (Haze, Sleep Dagger). H: several imbue items on one ability stack. Baseline P0 (no imbue) and single-imbue arms A/B. Comparison C/D (both items, both orders) and G (Surge on another ability). Readbacks: ability cooldown (cds), imbueown log, damage row. Outcomes: STACK / REPLACE-LAST / FIRST-WINS-OR-REFUSE / Surge-global (prediction table is in the file). Why: 56 of 81 frozen builds put 2-5 imbue items on one ability (`council/evidence/interactions/imbue_audit/IMBUE_AUDIT.txt`); if only one works those builds carry dead slots.
2. **N04b `nv_N04b_next_bullet_drifter_pellets`** with control **N04a** (Haze, single-bullet weapon). H: "next bullet" items (Crackshot, Express Shot) apply to one pellet only on a multi-pellet weapon. Baseline: no item; comparison: item vs per-pellet damage rows; N04a shows the single-bullet behaviour as control. Changes: value of next-bullet items on pellet heroes.
3. **N02 `nv_N02_resist_reducer_stacking`** (Haze). H: bullet-resist reducers combine as ADD / MAX / FRACTION. Baseline no reducer; arms: each alone, pairs. Match to nearest outcome column within 0.02 (rule in file). Changes: 22 builds buying two reducers.
4. **N07 `nv_N07_healing_tempo_scope`** (Haze). H: Healing Tempo's buff triggers from Vampiric Burst lifesteal. Arms per file. Changes: 21 builds paying for Healing Tempo.
Not queued: N03 (needs an uncast-verified hero), N10 (Nurse; later), Graves/Echo (needs a hero with a verified ult cast).

# N01 — several imbue items on one ability (Haze, Sleep Dagger) — attempt 1
Pre-registered in `council/review/prereg/COUNCIL_MODE_BATCH1.md` (commit 36d8a1c). Run 2026-10-25 01:29:33-01:34:57 local (00:29-00:34 UTC), task `novel:N01#1`.
Raw files here (hashes in `SHA256SUMS.txt`): `novel_N01.json/.md` (runner result), damage rows for the task window, `samples` csv, plugin.log excerpt TASK-START..TASK-END.

## Runner-recorded in the raw result
`VALID: yes`; client 6819 / server 6819 (match); readback checks `items_ok` and `dmg_hits` PASS; 13 blocks in range.
NOT recorded by the runner: plugin build hash (last hot reload was 2026-10-24 22:45:05 local and nothing reloaded since, so the build is INFERRED as the deployed 33D1B53F, not logged); frame validity (`frame_validity.py` not run: this session has no shell on the PC).

## Observations (one Sleep Dagger cast per block, target 350u, hardreset between blocks, each arm measured twice: forward and reverse order)
| arm | items imbued on Sleep Dagger | dagger damage | dagger cooldown (end-start, s) |
|---|---|---|---|
| P0 / P0_rev / P0_end | none | 103.5 / 103.5 / 103.5 | 13.0 |
| A (`upgrade_magic_tempo` only) / rev | 1 | 127.7 / 127.7 | 10.7 |
| B (`upgrade_magic_storm` only) / rev | 1 | 206.9 / 206.9 | 13.0 |
| C (tempo then storm) / rev | 2 | 248.7 / 248.7 | 10.6 / 10.6 |
| D (storm then tempo) / rev | 2 | 248.7 / 248.7 | 10.6 / 10.6 |
| G (storm imbued on another ability) / rev | storm on ability 2 | 145.3 / 145.3 | 13.0 / 13.0 |
Log: both `imbueown` calls returned `Success` and the readback showed `isImbued=True imbuedInto=[ability_sleep_dagger]` for BOTH items in C and D (`plugin_log_excerpt_...txt`, lines 'SC IMBUE readback').

## What this shows (CONTROLLED SANDBOX RESULT would need the replicate; today PRELIMINARY)
- The game accepted two imbue items on the same ability and both effects showed in both orders: cooldown equals the tempo-only arm (10.6-10.7 vs 13.0), damage is above either item alone. No refusal, no order dependence. This contradicts the "only one imbue per ability => dead slots" inference for this pair.
- Damage is NOT a plain sum: B-P0=103.4, A-P0=24.2, C-P0=145.2 (sum would be 127.6). Reason not established; do not model it as additive.
- Storm's effect has a part that does not need the imbue: G (storm on another ability) +41.8; imbue adds a further +61.6 on the dagger (B-G), which matches the file's modelled +61.6 (ImbuedTechPower 28 x 2.2).
## What it does NOT show
Only two items, one ability, one hero, one session. Not whether three to five imbues stack, not other item pairs, not same-type pairs (both items here are different types, so "same-type refused" is untested), not duration/uptime effects, no purchase verdict, no change to any build.
## Status
PRELIMINARY (one valid run; frame validity and build hash not independently recorded). Replicate queued as `novel:N01r`.

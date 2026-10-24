# nurse (Friendly Fire Harrow) — review 2

Sources: abilities.vdata (gt/repo, written Oct 20, includes Harrow), `python3 -I ab.py ability_nurse_leech_therapy ability_nurse_adrenaline_rush ability_nurse_healing_needles ability_nurse_fear`, names from citadel_heroes_english.txt (ability_nurse_adrenaline_rush = Wretched Vapors), items via `python3 -I audit_D_q.py`, Echo Shard text from citadel_mods_english.txt. No evidence/nurse.json exists, so no tested verdicts yet: every decision below is from game-file numbers, each has a pre-registered scenario.

## Kit numbers
- Leech Therapy (1): 30s cd, T2 -10 → 20s (16s with Superior Cooldown). AbilityDuration 5s. DPS 23 + 0.19x (T3 +0.3 → 0.49x). 4 leeches; pickups give regen, +5% fire rate, T2 +4 spirit each, max 10 (18 at T3).
- Wretched Vapors (2): 40s cd, T1 -15 → 25s (20s with Superior Cooldown). Rush 4s, T2 +1 → 5s. Rush speed 25% + 0.06x (T3 +15, dispel). Crash 4s: unhealed specters deal the delayed damage +30%.
- Healing Needles (3): no cooldown. 1 charge (T1 +1), recharged by damage (1.26% per bullet hit, 2.52% headshot, 0.15%/s per leech stack). Heal 25 + 0.2x per needle (T2 +20, T3 +0.4 → 45 + 0.6x). T3: each needle extends a teammate's non-ult buffs by 6%, up to 200%. Clip 11 (Code Blue, 0.38s cycle).
- Lurking Terrors (4): 200s cd, 7s channel (channel time, not a duration), fear debuff 2.2s.

## Q1 Echo Shard: Wretched Vapors (kept)
Echo Shard: resets the imbued non-ult ability; its own cooldown is 30s + that ability's cooldown. Needles have no cooldown (Echo does nothing there), the ult can't be imbued.
- On Vapors: resets 20s; Echo every 50s. Casts per minute 3.0 → 4.2 (+40%). Recast = a second rush (numb + up to 49% faster actions at 150 spirit, dispel at T3) on a second teammate.
- On Leech: resets 16s; Echo every 46s. 3.75 → 5.05 (+35%). Recast = 4 more leeches; Echo is a rich-box buy (after 60.8k) when stacks are already capped at 18, so the gain is only leech damage (23 + 0.49x per target, ~96 DPS at 150 spirit).
- Decision: Vapors. Larger reset and the recast is a teammate save, which is this build's job. Scenario: sandbox/scenarios/harrow_echo_vapors_vs_leech.json (pending).

## Q2 Duration extenders: not needed (CHANGED)
Abilities with durations: Leech 5s, Vapors 4s/5s rush (crash fixed 4s), fear 2.2s. Ult is a channel; needles have no duration.
- Duration Extender (+22%, imbue): Vapors 5 → 6.1s (+1.1s). Needles T3 already extends Vapors to 200% (10s) by needling the teammate (6% per needle, about 17 needles), so it only raises the cap 10 → 12.2s. A longer rush also banks more specter damage for the crash (+30% if not healed off).
- Superior Duration (+28% all, last core buy at 64.0k, +1.6k): Vapors +1.4s, Leech +1.4s, item actives (Unstoppable 5.5 → 7.0s, Vampiric Burst 5 → 6.4s). Small gains at the end of a 64k build.
- Displaced: Duration Extender holds the 6.4k spirit slot. Compress Cooldown (same 1.6k, same imbue slot) cuts Vapors 40 → 32.8s (25 → 20.5s after T1) = 22% more rushes and dispels, each a full fresh window; Superior Cooldown (already core, bought fresh for 3.2k) becomes its upgrade for 1.6k and stops using its own slot. Shorter Vapors cooldown also shortens Echo Shard's cooldown.
- Result: Duration Extender → Compress Cooldown (On Wretched Vapors.); Superior Duration out. Spirit 4.8k still at 8.8k on Surge; spirit 6.4k at 16.0k, 8.0k exactly at 17.6k (was 9.6k at 19.2k, overshooting 8k). Core 60.8k, 12 slots (was 64.0k). Freed slot: Escalating Exposure no longer sells Burst Fire; Echo Shard now sells Burst Fire (old sell, Superior Duration, is gone). Scenario: harrow_vapors_duration_vs_cooldown.json (pending).

## Q3 Surge of Power: Healing Needles (kept)
Surge: +28 spirit on the imbued ability; on cast, +1.75m move speed for 8s and full speed while shooting; 14s cooldown.
- Leech: cast every 20s (16s with Superior Cooldown) → procs at most every 20s/16s, 40–50% uptime. +28 spirit = +13.7 leech DPS at T3.
- Healing Needles: no cooldown; in fights a charge comes back every ~11–16s (late: fire rate +90% from 18 leeches → ~5 shots/s x 1.26% + 18 x 0.15%/s ≈ 9%/s), plus each swap-in is a cast, so the 14s item cooldown is the limit: ~57% uptime. +28 spirit = +16.8 heal per needle at T3, x11 needles = ~185 per clip (more with Vampiric Burst ammo); the free move while shooting keeps her moving while healing.
- Decision: Needles. Short ability cooldown beats the item's 14s; bigger per-cast gain. Scenario: harrow_surge_needles_vs_leech.json (pending).

## Other
- Mercurial Magnum note "On the needles, over Surge of Power." → "On Healing Needles. Sell Titanic Magazine for this." (rule: no "X over Y").
- walk1: FLAGS none, spikes spirit @8.8k, gun @11.2k, health @14.4k (unchanged). check.js: CHECK12 none.

# mirage (Mark My Words Mirage) — review 2

Sources: `python3 -I ab.py mirage_fire_beetles mirage_tornado mirage_sand_phantom mirage_teleport`, weapon citadel_weapon_mirage_set, heroes.vdata (bullet +0.3/boon), items via audit_D_q.py, `node a7/sp.js`. Public same-style builds from a19/w_mine/src.json (lockbuilds GUN/SPIRIT official 632506 Oct 19, apacycle 649576, Arctic 272974, seemeta Oct 5–19). No evidence/mirage.json, so no tested verdict; decision from numbers + public builds, scenario pending.

## Does she rely on gun?
- Gun: 14.8 (+0.3/boon) x 2.72 shots/s, 16 clip. ~58 DPS at level 24, ~85 with the 4.8k gun spike.
- Djinn's Mark: every shot marks, per-target cd 2.75s (2.0s T3, ~1.64s with Compress). Pop = 31 (T2) + 0.35x, doubling per mark, 5 marks at T3 = 16x. At 88 spirit a full pop is ~990 (~120 DPS), and each spirit point adds 5.6 to it. Fire rate doesn't add marks (cooldown-limited); Ricochet does (2 more targets).
- Dust Devil 125 + 0.9x (T3), 24s; Scarabs 15 + 0.23x/s, 7s, 3 charges, -35% target damage; Traveler is mobility/barrier only.
- So the gun applies the marks, the marks do most of the damage. Gun items that feed marks: Toxic (bleed is spirit damage, css tech_damage, ticks every 0.5s), Ricochet (marks on 3 targets), Spirit Shredder/Rend (-15% spirit resist). Pure gun: Headshot Booster/Headhunter (75 + 4/boon per headshot, 8s), Extended/Titanic (+100% clip, +14%).

## Verdict: the gun run was not justified (CHANGED)
Old Mid: Toxic → Headshot Booster → Headhunter → Extended → Ricochet → Titanic → Spirit Rend, spirit invest frozen at 4.8k from 4.8k to 38.4k souls.
Per 1k souls at ~20–28k: Escalating Exposure (+4.8k) +54% spirit damage at 12 stacks (Toxic bleed fills it in ~8s) ≈ +65 DPS on marks alone plus +14 spirit from invest → ~17 DPS/1k; Headhunter (+2.4k) ~20 DPS → ~8/1k; Titanic (+0.8k) ~+15 sustained → strong per soul but small.
Public builds: EE directly after Ricochet in official, apacycle and seemeta, and after Ricochet + Improved Spirit/MV in Arctic; Superior Cooldown right after EE (apacycle, Arctic); Headhunter late (Arctic) or absent (official, apacycle).
New: Mid = Toxic, Headshot Booster, Extended Magazine, Ricochet, Escalating Exposure, Superior Cooldown. Late = Inhibitor, Spirit Rend, Titanic, Boundless, Headhunter, Leech. Same 18 items, same 51.2k core, 12 slots.
- At 28.8k: spirit 114.8 (was 93.8 at 27.2k) → full pop 1139 before EE (was ~1021), ~1750 with 12 EE stacks.
- Spikes: spirit 4.8k @4.8k, 9.6k @27.2k, 11.2k exactly @28.8k, 16k exactly @42.4k (Boundless). Gun 4.8k @14.4k (Toxic, unchanged), 6.4k exactly @16.0k. Health 4.8k @11.2k, 11.2k @35.2k (was 33.6k; she has Traveler, Scarabs and Shredder lifesteal).
- Lost lane? box removed: Ricochet now follows Toxic after only two 800s, so the reorder no longer helps.
- walk1 FLAGS none; check.js CHECK12 none. Scenario: sandbox/scenarios/mirage_ee_before_gun_run.json (pending).

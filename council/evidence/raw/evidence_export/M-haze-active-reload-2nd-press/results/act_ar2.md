# act:ar2 attempt 1
VALID: yes
SCOPE: ability levels: isolated
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: act_ar2  wallSec: 68.1  end: end step
question: Can the tester trigger Active Reload with a timed second reload press, and does the reload get shorter?
purpose: discover and verify the timed-input path; not a build verdict
mechanics: gun plus timed reload input; no abilities
excluded: all abilities and all other items; this is a mechanic check
required_activation: Active Reload buff|modifier|active_reload/buff|1
required_readback: Timed press reloaded faster|ar_best|<|base_reload
## measured (exact plugin log lines)
ACT required: Active Reload buff [modifier ~active_reload/buff >= 1]
SC RESET method=hard (hero swap, fresh pawn)
LEVELS ACT|none|body: actual [ability_sleep_dagger=3, ability_smoke_bomb=3, ability_stacking_damage=3, ability_bullet_flurry=3, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST ACT|none|body: target 150 units away
RBPROBE weapon ability = citadel_weapon_haze_set
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_iClip (int) = 34
RBPROBE clip field chosen: CCitadel_Ability_PrimaryWeapon.m_iClip
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_bInReload (int) = 256
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_flNextPrimaryAttack (float) = 13221.1875
RBPROBE ok CBasePlayerWeapon.m_iClip1 (int) = 0
RBPROBE ok CBasePlayerWeapon.m_iClip2 (int) = 0
SC RELOAD press: clip=20 secondPress=none (timed input via the plugin)
SC RELOAD done: first press -> refill 2.38s (clip 20->30, second press none)
ACT reload/refill event: clip 20 -> 30 (max seen 33)
SC RB base_reload = 2.375  (reload_s)
ACT modifier seen: upgrade_active_reload/modifier_intrinsic_base
SC RELOAD press: clip=15 secondPress=0.90s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.41s (clip 15->36, second press 0.90s)
ACT reload/refill event: clip 15 -> 36 (max seen 36)
SC RB ar_0 = 2.406  (reload_s)
SC RELOAD press: clip=21 secondPress=1.00s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.47s (clip 21->36, second press 1.00s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
SC RB ar_1 = 2.469  (reload_s)
SC RELOAD press: clip=21 secondPress=1.10s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.11s (clip 21->36, second press 1.10s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT modifier seen: upgrade_active_reload/buff
ACT Active Reload buff: activation #1 (modifier ~active_reload/buff)
SC RB ar_2 = 1.109  (reload_s)
ACT modifier seen: modifier_life_steal
SC RELOAD press: clip=18 secondPress=1.30s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.38s (clip 18->36, second press 1.30s)
ACT reload/refill event: clip 18 -> 36 (max seen 36)
SC RB ar_3 = 2.375  (reload_s)
SC RELOAD press: clip=21 secondPress=1.40s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.44s (clip 21->36, second press 1.40s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
SC RB ar_4 = 2.438  (reload_s)
SC RELOAD press: clip=21 secondPress=1.50s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.49s (clip 21->36, second press 1.50s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
SC RB ar_5 = 2.485  (reload_s)
SC RB ar_best = 1.109  (minof:ar_0,ar_1,ar_2,ar_3,ar_4,ar_5)
ACT SUMMARY Active Reload buff: count=1 (needed 1) uptime=7.0s of 67s (10%) avgDuration=7.0s shortestGap=n/a (a continuous-bonus assumption would be 100% uptime) activeWhileFiring=15% of 10.4s
DIST SUMMARY blocks=1 inRange=1 outOfRange=0 expected=mixed
RB SUMMARY clipField=CCitadel_Ability_PrimaryWeapon.m_iClip clipMax=36 refillEvents=7
RB CHECK Timed press reloaded faster: ar_best=1.109 < base_reload=2.375 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_214809.csv  window ms: [3163422,3231500]
samples csv: E:\deadworks-server\sbx_logs\samples_act_ar2_224052.csv

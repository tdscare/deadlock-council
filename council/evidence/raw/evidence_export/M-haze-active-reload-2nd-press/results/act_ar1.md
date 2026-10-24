# act:ar1 attempt 1
VALID: yes
SCOPE: ability levels: isolated
ENV: unlabelled
scenario: act_ar1  wallSec: 51  end: end step
question: Can the tester trigger Active Reload with a timed second reload press, and does the reload get shorter?
purpose: discover and verify the timed-input path; not a build verdict
mechanics: gun plus timed reload input; no abilities
excluded: all abilities and all other items; this is a mechanic check
required_activation: Active Reload buff|modifier|active_reload|1
required_readback: Timed press reloaded faster|ar_best|<|base_reload
## measured (exact plugin log lines)
ACT required: Active Reload buff [modifier ~active_reload >= 1]
ACT modifier seen: upgrade_clip_size/modifier_intrinsic_base
LEVELS ACT|none|body: actual [ability_sleep_dagger=3, ability_smoke_bomb=3, ability_stacking_damage=3, ability_bullet_flurry=3, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST ACT|none|body: target 150 units away
RBPROBE weapon ability = citadel_weapon_haze_set
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_iClip (int) = 34
RBPROBE clip field chosen: CCitadel_Ability_PrimaryWeapon.m_iClip
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_bInReload (int) = 256
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_flNextPrimaryAttack (float) = 13082.375
RBPROBE ok CBasePlayerWeapon.m_iClip1 (int) = 0
RBPROBE ok CBasePlayerWeapon.m_iClip2 (int) = 0
SC RELOAD press: clip=19 secondPress=none (timed input via the plugin)
SC RELOAD done: first press -> refill 2.44s (clip 19->30, second press none)
ACT reload/refill event: clip 19 -> 30 (max seen 34)
SC RB base_reload = 2.438  (reload_s)
ACT modifier seen: upgrade_active_reload/modifier_intrinsic_base
ACT Active Reload buff: activation #1 (modifier ~active_reload)
SC RELOAD press: clip=15 secondPress=0.80s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.47s (clip 15->36, second press 0.80s)
ACT reload/refill event: clip 15 -> 36 (max seen 36)
SC RB ar_a = 2.469  (reload_s)
SC RELOAD press: clip=21 secondPress=1.20s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.27s (clip 21->36, second press 1.20s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT modifier seen: upgrade_active_reload/buff
SC RB ar_b = 1.266  (reload_s)
ACT modifier seen: modifier_life_steal
SC RELOAD press: clip=18 secondPress=1.60s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.44s (clip 18->36, second press 1.60s)
ACT reload/refill event: clip 18 -> 36 (max seen 36)
SC RB ar_c = 2.438  (reload_s)
SC RB ar_best = 1.266  (minof:ar_a,ar_b,ar_c)
ACT SUMMARY Active Reload buff: count=1 (needed 1) uptime=17.5s of 51s (34%) avgDuration=17.5s shortestGap=n/a (a continuous-bonus assumption would be 100% uptime) activeWhileFiring=76% of 5.9s
DIST SUMMARY blocks=1 inRange=1 outOfRange=0 expected=mixed
RB SUMMARY clipField=CCitadel_Ability_PrimaryWeapon.m_iClip clipMax=36 refillEvents=4
RB CHECK Timed press reloaded faster: ar_best=1.266 < base_reload=2.438 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_154715.csv  window ms: [2260969,2312016]
samples csv: E:\deadworks-server\sbx_logs\samples_act_ar1_162456.csv

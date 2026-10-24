# p3:act_ar3 attempt 1
VALID: yes
SCOPE: ability levels: isolated
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: act_ar3  wallSec: 224.2  end: end step
question: Where exactly does the Active Reload window open and close between 1.00 and 1.30 s?
purpose: discover and verify the timed-input path; not a build verdict
mechanics: gun plus timed reload input; no abilities
excluded: all abilities and all other items; this is a mechanic check
required_activation: Active Reload buff|modifier|active_reload/buff|1
required_readback: Timed press reloaded faster|ar_best|<|base_reload
## measured (exact plugin log lines)
ACT required: Active Reload buff [modifier ~active_reload/buff >= 1]
ACT modifier seen: upgrade_ability_power_shard/modifier_intrinsic_base
ACT modifier seen: ability_smoke_bomb/smokebomb_modifier_invis
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: ability_smoke_bomb/buff_modifier
LEVELS ACT|none|body: actual [ability_sleep_dagger=3, ability_smoke_bomb=3, ability_stacking_damage=3, ability_bullet_flurry=3, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST ACT|none|body: target 150 units away
RBPROBE weapon ability = citadel_weapon_haze_set
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_iClip (int) = 34
RBPROBE clip field chosen: CCitadel_Ability_PrimaryWeapon.m_iClip
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_bInReload (int) = 256
RBPROBE ok CCitadel_Ability_PrimaryWeapon.m_flNextPrimaryAttack (float) = 14079.09375
RBPROBE ok CBasePlayerWeapon.m_iClip1 (int) = 0
RBPROBE ok CBasePlayerWeapon.m_iClip2 (int) = 0
SC RELOAD press: clip=20 secondPress=none (timed input via the plugin)
SC RELOAD done: first press -> refill 2.39s (clip 20->30, second press none)
ACT reload/refill event: clip 20 -> 30 (max seen 33)
SC RB base_reload = 2.39  (reload_s)
ACT modifier seen: upgrade_active_reload/modifier_intrinsic_base
SC RELOAD press: clip=15 secondPress=1.00s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.41s (clip 15->36, second press 1.00s)
ACT reload/refill event: clip 15 -> 36 (max seen 36)
SC RB ar_0 = 2.406  (reload_s)
SC RELOAD press: clip=22 secondPress=1.05s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.06s (clip 22->36, second press 1.05s)
ACT reload/refill event: clip 22 -> 36 (max seen 36)
ACT modifier seen: upgrade_active_reload/buff
ACT Active Reload buff: activation #1 (modifier ~active_reload/buff)
SC RB ar_1 = 1.062  (reload_s)
SC RELOAD press: clip=21 secondPress=1.10s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.16s (clip 21->36, second press 1.10s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #2 (modifier ~active_reload/buff)
SC RB ar_2 = 1.157  (reload_s)
SC RELOAD press: clip=21 secondPress=1.15s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.20s (clip 21->36, second press 1.15s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #3 (modifier ~active_reload/buff)
SC RB ar_3 = 1.203  (reload_s)
SC RELOAD press: clip=22 secondPress=1.20s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.27s (clip 22->36, second press 1.20s)
ACT reload/refill event: clip 22 -> 36 (max seen 36)
ACT Active Reload buff: activation #4 (modifier ~active_reload/buff)
SC RB ar_4 = 1.266  (reload_s)
SC RELOAD press: clip=21 secondPress=1.25s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.31s (clip 21->36, second press 1.25s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #5 (modifier ~active_reload/buff)
SC RB ar_5 = 1.313  (reload_s)
SC RELOAD press: clip=21 secondPress=1.30s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.36s (clip 21->36, second press 1.30s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #6 (modifier ~active_reload/buff)
SC RB ar_6 = 1.359  (reload_s)
SC RELOAD press: clip=22 secondPress=1.30s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.36s (clip 22->36, second press 1.30s)
ACT reload/refill event: clip 22 -> 36 (max seen 36)
ACT Active Reload buff: activation #7 (modifier ~active_reload/buff)
SC RB ar_7 = 1.359  (reload_s)
SC RELOAD press: clip=21 secondPress=1.25s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.30s (clip 21->36, second press 1.25s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #8 (modifier ~active_reload/buff)
SC RB ar_8 = 1.297  (reload_s)
SC RELOAD press: clip=21 secondPress=1.20s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.24s (clip 21->36, second press 1.20s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #9 (modifier ~active_reload/buff)
SC RB ar_9 = 1.235  (reload_s)
SC RELOAD press: clip=21 secondPress=1.15s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.17s (clip 21->36, second press 1.15s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #10 (modifier ~active_reload/buff)
SC RB ar_10 = 1.172  (reload_s)
SC RELOAD press: clip=21 secondPress=1.10s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.11s (clip 21->36, second press 1.10s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #11 (modifier ~active_reload/buff)
SC RB ar_11 = 1.109  (reload_s)
SC RELOAD press: clip=21 secondPress=1.05s (timed input via the plugin)
SC RELOAD done: first press -> refill 1.16s (clip 21->36, second press 1.05s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
ACT Active Reload buff: activation #12 (modifier ~active_reload/buff)
SC RB ar_12 = 1.156  (reload_s)
SC RELOAD press: clip=21 secondPress=1.00s (timed input via the plugin)
SC RELOAD done: first press -> refill 2.41s (clip 21->36, second press 1.00s)
ACT reload/refill event: clip 21 -> 36 (max seen 36)
SC RB ar_13 = 2.406  (reload_s)
SC RB ar_best = 1.062  (minof:ar_0,ar_1,ar_2,ar_3,ar_4,ar_5,ar_6,ar_7,ar_8,ar_9,ar_10,ar_11,ar_12,ar_13)
ACT SUMMARY Active Reload buff: count=12 (needed 1) uptime=84.5s of 223s (38%) avgDuration=7.0s shortestGap=13.5s (a continuous-bonus assumption would be 100% uptime) activeWhileFiring=0% of 22.5s
DIST SUMMARY blocks=1 inRange=1 outOfRange=0 expected=mixed
RB SUMMARY clipField=CCitadel_Ability_PrimaryWeapon.m_iClip clipMax=36 refillEvents=15
RB CHECK Timed press reloaded faster: ar_best=1.062 < base_reload=2.39 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_224505.csv  window ms: [610547,834781]
samples csv: E:\deadworks-server\sbx_logs\samples_act_ar3_225516.csv

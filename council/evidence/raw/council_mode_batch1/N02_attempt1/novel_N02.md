# novel:N02 attempt 1
VALID: yes
SCOPE: ability levels: fixed
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: nv_N02_resist_reducer_stacking  wallSec: 486.1  end: end step
question: Checking whether two bullet-resist reducers add up, take only the stronger one, or each remove a share of what is left (and whether they do anything on an enemy with no bullet resist).
purpose: decides whether the second reducer is worth its souls: 10 builds hold Bullet Resist Shredder together with Hunter's Aura or Crippling Headshot, and 22 builds hold 2+ reducers of any kind
mechanics: each reducer applies its own debuff (items.json: BulletArmorReduction on Bullet Resist Shredder -10 and Hunter's Aura -10, doubled with one enemy hero near = -20 (SingleTargetPlayerMultiplier 2); BulletResistReduction on Crippling Headshot -16 with DiminishingMultiplier 0.5). The combining rule and whether the number is percentage points or a share of the target's resist are engine-side (UNRESOLVED). The target gets 30 percent bullet resist from Bullet Resilience (verified 34.8 -> 24.4 per bullet); two arms use 0 percent
required_activation: cast1|ability|ability_sleep_dagger|1
required_readback: items_ok|1|==|1 ; dmg_hits|hits|>|0
required_levels: 1=4;2=1;3=1;4=1
stack_track: none
## measured (exact plugin log lines)
ACT required: cast1 [ability ~ability_sleep_dagger >= 1]
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: citadel_ability_card_toss/modifier_ability_resource_pool
LEVELS N_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_
DIST N_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citade
DIST BRS_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS HA_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel
DIST HA_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_HA_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST BRS_HA_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS Nh_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel
DIST Nh_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS CH_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel
DIST CH_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_CH_30: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST BRS_CH_30: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS N_0: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_a
DIST N_0: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_HA_0: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cita
DIST BRS_HA_0: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_HA_0_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, 
DIST BRS_HA_0_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS N_0_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citad
DIST N_0_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_CH_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST BRS_CH_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS CH_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST CH_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS Nh_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST Nh_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_HA_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST BRS_HA_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS HA_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST HA_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS BRS_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, ci
DIST BRS_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS N_30_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cita
DIST N_30_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS N_30_end: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cita
DIST N_30_end: target 350 units away
ACT SUMMARY cast1: count=1 (needed 1) uptime=0.0s of 486s (0%) avgDuration=0.0s shortestGap=n/a (a continuous-bonus assumption would be 100% uptime) activeWhileFiring=n/a of 0.0s
DIST SUMMARY blocks=19 inRange=19 outOfRange=0 expected=mixed
RB CHECK items_ok: 1=1 == 1=1 => PASS
RB CHECK dmg_hits: hits=39 > 0=0 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_224505.csv  window ms: [10633906,11119984]
samples csv: E:\deadworks-server\sbx_logs\samples_nv_N02_resist_reducer_stacking_014219.csv

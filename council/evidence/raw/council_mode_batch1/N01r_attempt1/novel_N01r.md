# novel:N01r attempt 1
VALID: yes
SCOPE: ability levels: fixed
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: nv_N01_multi_imbue  wallSec: 323.1  end: end step
question: Checking what happens when two imbue items are put on the same ability: do both work, does the last one replace the first, or is the second refused?
purpose: decides how 56 of 81 builds should use their imbue items: 56 builds put 2-5 imbue items on one ability (104 item placements would be unused if the game allows only one per ability)
mechanics: game data (abilities.vdata) gives each imbue item a behaviour type (ACTIVE / ACTIVE_NON_ULT / MODIFIER_VALUE) but no per-ability capacity field; replace vs refuse vs stack is not in the data (UNRESOLVED). Sleep Dagger is used because both effects are readable: Compress Cooldown shows in the ability cooldown (cds), Surge of Power adds imbued Spirit Power (ImbuedTechPower 28 x damage scale 2.2 = +61.6 dagger damage before resists, MODELLED)
required_activation: cast1|ability|ability_sleep_dagger|1
required_readback: items_ok|1|==|1 ; dmg_hits|hits|>|0
required_levels: 1=4;2=1;3=1;4=1
stack_track: none
## measured (exact plugin log lines)
ACT required: cast1 [ability ~ability_sleep_dagger >= 1]
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: citadel_ability_card_toss/modifier_ability_resource_pool
LEVELS P0_none: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citad
DIST P0_none: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS A_CC_only: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cit
DIST A_CC_only: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: upgrade_magic_storm/modifier_magic_storm_watcher
LEVELS B_Surge_only: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, 
DIST B_Surge_only: target 350 units away
ACT modifier seen: upgrade_magic_storm/modifier_magic_storm_watcher/modifier_upgrade_magic_storm
SC RESET method=hard (hero swap, fresh pawn)
LEVELS C_CC_then_Surge: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=
DIST C_CC_then_Surge: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS D_Surge_then_CC: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=
DIST D_Surge_then_CC: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS G_Surge_on_other_slot: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_
DIST G_Surge_on_other_slot: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS G_Surge_on_other_slot_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_abil
DIST G_Surge_on_other_slot_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS D_Surge_then_CC_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_sl
DIST D_Surge_then_CC_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS C_CC_then_Surge_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_sl
DIST C_CC_then_Surge_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS B_Surge_only_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide
DIST B_Surge_only_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS A_CC_only_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3,
DIST A_CC_only_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS P0_none_rev: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, c
DIST P0_none_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS P0_end: actual [ability_sleep_dagger=4, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citade
DIST P0_end: target 350 units away
ACT SUMMARY cast1: count=13 (needed 1) uptime=0.0s of 322s (0%) avgDuration=0.0s shortestGap=n/a (a continuous-bonus assumption would be 100% uptime) activeWhileFiring=n/a of 0.0s
DIST SUMMARY blocks=13 inRange=13 outOfRange=0 expected=mixed
RB CHECK items_ok: 1=1 == 1=1 => PASS
RB CHECK dmg_hits: hits=13 > 0=0 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_224505.csv  window ms: [11344984,11668047]
samples csv: E:\deadworks-server\sbx_logs\samples_nv_N01_multi_imbue_015410.csv

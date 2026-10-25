# novel:N04a attempt 1
VALID: yes
SCOPE: ability levels: fixed
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: nv_N04a_next_bullet_haze_control  wallSec: 217.1  end: end step
question: Checking whether a 'next bullet' item gives its bonus to one pellet or to every pellet of a multi-pellet shot, and what Express Shot does to a shotgun-style shot.
purpose: decides if next-bullet items (Mystic Shot, Headshot Booster, Headhunter, Restorative Shot, Express Shot) are worth buying on multi-pellet or burst weapons: 7 builds hold one on such a hero
mechanics: the data caps these items at one bullet per shot (m_flMaxBulletsToProcInShot=1, no multiple procs per shot or per target; VERIFIED MECHANIC). Drifter's weapon fires m_iBullets=3 per shot (cycle 0.441 s), Haze 1 per shot (cycle 0.105 s). Whether the cap means 1 pellet of 3, and what Express Shot does (fires twice, uses extra ammo) is UNRESOLVED
required_readback: items_ok|1|==|1 ; dmg_hits|hits|>|0
required_levels: 1=1;2=1;3=1;4=1
stack_track: none
## measured (exact plugin log lines)
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: citadel_ability_card_toss/modifier_ability_resource_pool
LEVELS H_X0: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_
DIST H_X0: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_M: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_a
DIST H_M: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_E: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_a
DIST H_E: target 350 units away
ACT modifier seen: upgrade_express_shot/notification
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_ME: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citadel_
DIST H_ME: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_ME_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cita
DIST H_ME_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_E_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citad
DIST H_E_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_M_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, citad
DIST H_M_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS H_X0_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3, cita
DIST H_X0_rev: target 350 units away
DIST SUMMARY blocks=8 inRange=8 outOfRange=0 expected=mixed
RB CHECK items_ok: 1=1 == 1=1 => PASS
RB CHECK dmg_hits: hits=25 > 0=0 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_224505.csv  window ms: [10413812,10630906]
samples csv: E:\deadworks-server\sbx_logs\samples_nv_N04a_next_bullet_haze_control_013839.csv

# novel:N07 attempt 1
VALID: yes
SCOPE: ability levels: fixed
ENV: unlabelled
BUILD: client 6819 / server 6819 (match)
scenario: nv_N07_healing_tempo_scope  wallSec: 219  end: end step
question: Checking whether Healing Tempo's speed buff turns on when healing comes from Vampiric Burst's lifesteal, from a direct heal item, from passive bullet lifesteal, or from nothing.
purpose: decides where Healing Tempo (a late, expensive item) belongs: 21 builds hold it, most of them pair it with lifesteal items whose heals may not count
mechanics: item text (VERIFIED MECHANIC, citadel_mods_english.txt upgrade_healbuff_desc): applying healing grants fire rate and move speed; does not apply on innate regen or passive Bullet/Spirit Lifesteals. Whether lifesteal granted by an active (Vampiric Burst, Infuser) counts as passive is not in the data (UNRESOLVED). Healing Nova is the positive control (a direct heal), passive Bullet Lifesteal the negative control (excluded by the text)
required_readback: items_ok|1|==|1
required_levels: 1=1;2=1;3=1;4=1
stack_track: none
## measured (exact plugin log lines)
SC RESET method=hard (hero swap, fresh pawn)
ACT modifier seen: citadel_ability_card_toss/modifier_ability_resource_pool
LEVELS T0_tempo_alone: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3
DIST T0_tempo_alone: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS P_passive_lifesteal: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_sl
DIST P_passive_lifesteal: target 350 units away
ACT modifier seen: modifier_life_steal
SC RESET method=hard (hero swap, fresh pawn)
LEVELS D_healing_nova: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide=3
DIST D_healing_nova: target 350 units away
ACT modifier seen: upgrade_health_nova/modifier_healing_Nova_active
ACT modifier seen: upgrade_healbuff/modifier_healbuff/modifier_healbuff_buff
SC RESET method=hard (hero swap, fresh pawn)
LEVELS V_vampiric_burst: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_slide
DIST V_vampiric_burst: target 350 units away
ACT modifier seen: upgrade_surging_power/surge
ACT modifier seen: upgrade_surging_power/surge/active
SC RESET method=hard (hero swap, fresh pawn)
LEVELS V_vampiric_burst_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_s
DIST V_vampiric_burst_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS D_healing_nova_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_sli
DIST D_healing_nova_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS P_passive_lifesteal_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_abilit
DIST P_passive_lifesteal_rev: target 350 units away
SC RESET method=hard (hero swap, fresh pawn)
LEVELS T0_tempo_alone_rev: actual [ability_sleep_dagger=1, ability_smoke_bomb=1, ability_stacking_damage=1, ability_bullet_flurry=1, citadel_ability_zip_line=3, citadel_ability_mantle=3, citadel_ability_climb_rope=3, citadel_ability_jump=3, citadel_ability_sli
DIST T0_tempo_alone_rev: target 350 units away
DIST SUMMARY blocks=8 inRange=8 outOfRange=0 expected=mixed
RB CHECK items_ok: 1=1 == 1=1 => PASS
## files
damage csv: E:\deadworks-server\sbx_logs\damage_20261024_224505.csv  window ms: [11122984,11341984]
samples csv: E:\deadworks-server\sbx_logs\samples_nv_N07_healing_tempo_scope_015028.csv

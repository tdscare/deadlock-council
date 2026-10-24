"""Writes the INTERACTION scenario specs for the duo unknowns (council/sandbox/autorun/scenarios/duo/*.txt) + their evidence stubs.
Specs only: nothing is queued or run from here. Ops that do not exist in the plugin yet are listed in `meta blocked_by` and in REQUESTS."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = SP + '/council/sandbox/autorun/scenarios/duo'
EVD = SP + '/council/work/duo/evidence'

# ops that exist in the plugin source (/mnt/user-data/outputs/arena, read 16:3x): see report. PC build state UNVERIFIED.
OPS_OK = 'setup raw abil souls hardreset give basemods enemies fetch cast hold fire aim wait mark eitem eresist ehp end ally allycheck aexec castself eshoot moddump modadd rb'.split()

REQUESTS = [
 ('aitem <item...> / asouls <n> / aabil <b1 b2 b3 b4>', 'give the ally bot items, souls and ability upgrade bits (give/souls/abil only act on the human pawn today)', 'D4,D5,D7'),
 ('aaim enemy|me|<x y z> and aexec ... target enemy|me', 'point the ally bot at a target before aexec (bots have no input: unit-target and projectile abilities need an aim/target)', 'D4,D5,D7'),
 ('ahold <slot> <sec>', 'hold a channelled/charged ally ability for N seconds (aexec executes once; Telekinesis, Hyper Beam style channels end immediately)', 'D5,D7'),
 ('emove <strafe|flee|circle|walk> <speed> <sec>', 'scripted enemy movement (bots stand still: a held-vs-free comparison and every landing-frequency h needs a moving target)', 'D6,D7'),
 ('rb enemy:<spec> and rb ally:<spec>', 'readbacks on the enemy/ally pawn (modifier present/duration/stacks, hp) - today rb reads only the human pawn', 'D3,D4,D5'),
 ('dmglog by attacker (player|ally)', 'per-hit damage CSV with the attacker so shared-debuff tests can attribute ally hits', 'D4'),
 ('ashoot gun|spirit|melee <dmg> [n] [gap]', 'ally->enemy real damage via ApplyDamage (eshoot is enemy->player only); lets the ally act as the second damage dealer without aim', 'D4'),
]

COMMON_SETUP = ['raw citadel_unlock_flex_slots']

def meta(d):
    return ''.join('meta %s %s\n' % (k, v) for k, v in d.items())

def arm(items, extra, label, fire='fire 4'):
    L = ['hardreset', 'souls 30000'] + ['give %s' % i for i in items] + ['basemods', 'enemies 1 300 4'] + extra + ['fetch 350', 'cast reload 2.5', 'mark %s' % label, fire, 'mark none', 'wait 2']
    return L

SPECS = {}

# D1 resist formula + stacking: single player, runnable on the current runner
SPECS['duo_D1_shred_formula'] = dict(
    note='D1 NOW (single player). Settles the two unknowns every shred estimate carries: formula (absolute vs relative) and stacking (max/add).',
    meta=dict(kind='INTERACTION', question="Checking how Hollow Point and Hunter's Aura change an armoured enemy's gun damage.",
        purpose='measure the resist formula (points vs fraction of resist) and stacking of two bullet shreds; every duo shred estimate holds both as UNKNOWN bounds',
        mechanics='BulletArmorReduction -10 on the enemy: does it remove 10 points of resist or 10 percent of it, and do two sources add, take the max or multiply (GAPS 18 unverified)',
        expectedstate='souls=30000 items=upgrade_hollow_point_rounds,upgrade_bullet_armor_reduction_aura', build='haze', checkpoint='30000',
        items='upgrade_hollow_point_rounds upgrade_bullet_armor_reduction_aura', strategy_source='council/work/duo/evidence/duo_D1_shred_formula.txt',
        feeds='duo engine shred formula and stacking bounds', selection_kind='discovery',
        selection_reason='discovery: duo shred value moves from +1% to +18% kills depending on formula and stacking, one single-player test fixes both',
        cond_scope='gun only', cond_abilities_used='none', cond_abilities_excluded='all active abilities', cond_accuracy='all shots on target (aimoff calibrated at 350u)',
        cond_misses='none', cond_start_stacks='n/a', cond_activations="Hollow Point,Hunter's Aura",
        cond_distance='350u: read back the measured metres (aura range is 15 m)', cond_targets='enemies=1 allies=0',
        readbacks="equipped_items,distance_m,activation:Hollow Point,activation:Hunter's Aura",
        player_title='Shred stacking test', player_what='Armoured bot, 4 gun setups', player_why='Do two shreds add up?', player_short='Shred stacking', player_expect='Damage per hit A to D',
        result_says='WORKS (formula and stacking read from per-hit damage ratios) if B,C,D differ from A; DOES NOT WORK if all equal (shred not applied by this setup)'),
    body=lambda: ['setup Haze Haze'] + COMMON_SETUP + arm([], ['eitem upgrade_bullet_armor'], 'A_none') + arm(['upgrade_hollow_point_rounds'], ['eitem upgrade_bullet_armor'], 'B_hollow')
        + arm(['upgrade_bullet_armor_reduction_aura'], ['eitem upgrade_bullet_armor'], 'C_aura') + arm(['upgrade_hollow_point_rounds', 'upgrade_bullet_armor_reduction_aura'], ['eitem upgrade_bullet_armor'], 'D_both')
        + arm([], ['eitem upgrade_bullet_armor'], 'A2_none') + ['end'],
    blocked=None)

# D2 isolation counting for Hunter's Aura (nearby-enemy count radius)
def d2_body():
    L = ['setup Haze Haze'] + COMMON_SETUP
    for r in (300, 500, 700, 900, 1300, 2500):
        L += ['hardreset', 'souls 30000', 'give upgrade_bullet_armor_reduction_aura', 'basemods', 'enemies 2 %d 4' % r, 'eitem upgrade_bullet_armor', 'fetch 350', 'cast reload 2.5', 'mark R%d' % r, 'fire 4', 'mark none', 'wait 2']
    L += ['hardreset', 'souls 30000', 'give upgrade_bullet_armor_reduction_aura', 'basemods', 'enemies 1 300 4', 'eitem upgrade_bullet_armor', 'fetch 350', 'cast reload 2.5', 'mark R_alone', 'fire 4', 'mark none', 'wait 2', 'end']
    return L
SPECS['duo_D2_isolation_radius'] = dict(
    note="D2 NOW (single player). How 'only one enemy hero nearby' is counted (radius, who is the centre). Ring distance of the 2nd enemy is the scanned variable.",
    meta=dict(kind='INTERACTION', question="Checking how far away a second enemy must stand before Hunter's Aura stops halving its shred.",
        purpose="verify how nearby enemies are counted for 'only one enemy nearby' effects (centre, radius, line of sight) instead of assuming the 15 m aura radius",
        mechanics="Hunter's Aura text doubles its effect with a single enemy hero nearby; GAPS 19 measured halving with a second enemy in a 5-bot ring but not the counting radius",
        expectedstate='souls=30000 items=upgrade_bullet_armor_reduction_aura', build='haze', checkpoint='30000', items='upgrade_bullet_armor_reduction_aura',
        strategy_source='council/work/duo/evidence/duo_D2_isolation_radius.txt', feeds='duo engine isolation rule (STATE isolated)', selection_kind='discovery',
        selection_reason='discovery: every isolation-based duo idea (pull/knock/tether then isolated bonus) depends on how nearby enemies are counted; no data states it',
        cond_scope='gun only', cond_abilities_used='none', cond_abilities_excluded='all active abilities', cond_accuracy='all shots on target (aimoff calibrated at 350u)',
        cond_misses='none', cond_start_stacks='n/a', cond_activations="Hunter's Aura", cond_distance='350u to the target; second enemy ring 300..2500u: read back measured metres of both',
        cond_targets='enemies=2 allies=0', readbacks="equipped_items,distance_m,activation:Hunter's Aura",
        player_title='Who counts as nearby?', player_what='2nd bot at 6 distances', player_why='Is it the 15 m aura range?', player_short='Nearby count', player_expect='Damage per hit vs distance',
        result_says='WORKS (counting radius read from the distance where per-hit damage drops) if damage steps down at some ring distance; DOES NOT WORK if flat'),
    body=d2_body, blocked=None)

# D3 sleep wake timing (single player, Haze)
def d3_body():
    L = ['setup Haze Haze'] + COMMON_SETUP + ['abil 7 3 7 1']
    for d, tag in ((0.0, 'S0'), (0.3, 'S1'), (1.2, 'S2')):
        L += ['hardreset', 'souls 30000', 'basemods', 'enemies 1 300 4', 'fetch 350', 'cast reload 2.5', 'mark %s_cast' % tag, 'cast 1 1', 'wait 0.6', 'moddump enemy', 'wait %g' % d, 'mark %s_shoot' % tag, 'fire 0.3', 'moddump enemy', 'wait 0.15', 'moddump enemy', 'wait 0.4', 'moddump enemy', 'mark none', 'wait 2']
    L += ['end']
    return L
SPECS['duo_D3_sleep_break'] = dict(
    note='D3 NOW (single player; enemy modifier dump via moddump). Measures the real wake-up delay after damage and whether the sleep outlasts a delayed payload.',
    meta=dict(kind='INTERACTION', question='Checking how fast Sleep Dagger ends once the sleeping enemy is shot.',
        purpose='measure the real sleep break after damage (data says SleepWakeUpDelay 0.1 s, MinimumSleepTime 0.2 s) so no duo plan shoots a sleeper or builds a damage zone on one by mistake',
        mechanics='sleep ends shortly after damage; the data gives the constants but not whether a single bullet, a tick of area damage or a delayed hit ends it, nor the real hold left for a delayed payload',
        expectedstate='souls=30000 items=none', build='haze', checkpoint='30000', items='none', strategy_source='council/work/duo/evidence/duo_D3_sleep_break.txt',
        feeds='duo engine HOLD sleep rule', selection_kind='discovery',
        selection_reason='discovery: a sleep-based combo was proposed before and the data constants imply it breaks almost at once; one run confirms what the target actually does',
        cond_scope='ability 1 cast + gun', cond_abilities_used='cast 1', cond_abilities_excluded='all other active abilities', cond_accuracy='all shots on target (aimoff calibrated at 350u)',
        cond_misses='none', cond_start_stacks='n/a', cond_activations='Sleep Dagger', cond_distance='350u: read back the measured metres', cond_targets='enemies=1 allies=0',
        readbacks='ability_tiers,distance_m,ability_cast:1', player_title='Does Sleep Dagger stay on?', player_what='Shoot the sleeper', player_why='Sleep breaks on damage?', player_short='Sleep break', player_expect='Sleep time after a hit',
        result_says='WORKS (wake delay read from the enemy modifier dump) if the asleep modifier disappears within 0.5 s of damage; DOES NOT WORK if it persists'),
    body=d3_body, blocked='enemy_modifier_readback')

# D4 shared debuff (needs ally)
SPECS['duo_D4_shred_shared_ally'] = dict(
    note='D4 UNTESTABLE-NOW (needs ally items/levels + ally aim). Does a resist debuff applied by the ally raise the PLAYER\'s damage? Decides whether concentrating shred on an enabler can ever pay.',
    meta=dict(kind='INTERACTION', question="Checking whether Danny's Jettison Fuel shred raises Haze's own gun damage.",
        purpose="settle SHARED (UNKNOWN): the ally's shred applied to the enemy lowers damage taken from the player too, or only from the ally",
        mechanics='resist debuff modifiers may be keyed to the applier; the data does not say whether other attackers benefit',
        expectedstate='souls=30000 items=none', build='haze', checkpoint='30000', items='none', strategy_source='council/work/duo/evidence/duo_D4_shred_shared_ally.txt',
        feeds='duo engine shred SHARED flag', selection_kind='discovery', selection_reason='discovery: the whole Danny/enabler concentration question is worth +0% or +18% depending on this one flag, and no data states it',
        cond_scope='ally-target test', cond_abilities_used='ally cast 3', cond_abilities_excluded='all player abilities', cond_accuracy='all shots on target (aimoff calibrated at 350u)',
        cond_misses='none', cond_start_stacks='n/a', cond_activations='Jettison Fuel', cond_distance='350u', cond_targets='enemies=1 allies=1',
        readbacks='distance_m,ally_effect_applied,ability_cast:3', player_title='Does ally shred help me?', player_what='Danny sprays, I shoot', player_why='Is shred shared?', player_short='Shared shred', player_expect='My damage with and without',
        result_says='WORKS (shared) if my per-hit damage rises while the ally shred modifier is on the enemy; DOES NOT WORK if unchanged'),
    body=lambda: ['setup Haze Haze'] + COMMON_SETUP + ['hardreset', 'souls 30000', 'basemods', 'enemies 1 300 4', 'eitem upgrade_bullet_armor', 'ally Deadpack 6', 'allycheck', 'aabil 3 3 3 1', 'fetch 350', 'cast reload 2.5',
        'mark A_alone', 'fire 3', 'mark none', 'wait 3', 'aaim enemy', 'ahold 3 2', 'mark B_with_ally', 'fire 3', 'mark none', 'wait 3', 'mark A2_alone', 'fire 3', 'mark none', 'end'],
    blocked='ally_item_and_level_grant,ally_aim_target,ally_hold_channel,enemy_modifier_readback,damage_log_by_attacker')

# D5 channel carry (needs ally)
SPECS['duo_D5_channel_carried'] = dict(
    note='D5 UNTESTABLE-NOW (needs ally aim/target on the player + ally levels). Can a rooted channel continue while the ally relocates the channeller?',
    meta=dict(kind='INTERACTION', question="Checking whether Bebop's Hyper Beam keeps firing while Doorman's Luggage Cart drags him.",
        purpose='settle UNKNOWN: an ability can be cast/continued while carried or dragged by an ally ability (the CARRY rule of the duo engine depends only on this)',
        mechanics='data lists the states the carry applies but not whether channel abilities may start or continue under them',
        expectedstate='souls=30000 items=none', build='bebop', checkpoint='30000', items='none', strategy_source='council/work/duo/evidence/duo_D5_channel_carried.txt',
        feeds='duo engine CARRY rule', selection_kind='discovery', selection_reason='discovery: the top unproven duo ideas (move a channeller with Luggage Cart / Air Drop) are +9% to +34% kills if this works and zero if not',
        cond_scope='ability 4 cast + ally-target test', cond_abilities_used='cast 4, ally cast 3 alt', cond_abilities_excluded='all other active abilities', cond_accuracy='all shots on target (aimoff calibrated at 350u)',
        cond_misses='none', cond_start_stacks='n/a', cond_activations='Hyper Beam,Luggage Cart', cond_distance='350u', cond_targets='enemies=1 allies=1',
        readbacks='distance_m,ability_cast:4,ally_effect_applied', player_title='Beam while dragged?', player_what='Doorman drags me', player_why='Can I keep channelling?', player_short='Channel while moved', player_expect='Beam damage during drag',
        result_says='WORKS if Hyper Beam damage continues while the player has the drag modifier; DOES NOT WORK if the channel ends or damage stops'),
    body=lambda: ['setup Bebop Haze'] + COMMON_SETUP + ['hardreset', 'souls 30000', 'basemods', 'enemies 1 300 4', 'ally Doorman 6', 'allycheck', 'aabil 3 3 3 1', 'fetch 350',
        'mark A_beam_alone', 'hold 4 3', 'mark none', 'wait 4', 'aaim me', 'mark B_beam_then_drag', 'hold 4 5', 'aexec ally 3 alt', 'mark none', 'wait 4', 'moddump me', 'end'],
    blocked='ally_item_and_level_grant,ally_aim_target,ally_hold_channel,enemy_modifier_readback')

# D6 landing frequency h of ground-delayed payloads against a moving enemy
SPECS['duo_D6_flask_landing_moving'] = dict(
    note='D6 UNTESTABLE-NOW (needs scripted enemy movement). Measures h = how often a thrown ground payload lands on a moving enemy; the duo model sweeps h in 0.3..0.7 as ASSUMED.',
    meta=dict(kind='INTERACTION', question='Checking how often Alchemical Fire lands on an enemy that is walking away.',
        purpose='measure the independent landing frequency h (the one free parameter of every HOLD/ZONE value estimate) for a ground-thrown flask against standing, strafing and fleeing targets',
        mechanics='Alchemical Fire is a thrown projectile that explodes on contact and leaves an area; whether a moving enemy stays inside is not in data',
        expectedstate='souls=30000 items=upgrade_thermal_detonator', build='bebop', checkpoint='30000', items='upgrade_thermal_detonator', strategy_source='council/work/duo/evidence/duo_D6_flask_landing_moving.txt',
        feeds='duo engine h parameter', selection_kind='discovery', selection_reason='discovery: all HOLD and ZONE values scale with h which is ASSUMED 0.3-0.7; measuring it replaces a guess with data',
        cond_scope='active item use + gun', cond_abilities_used='item 1', cond_abilities_excluded='all signature abilities', cond_accuracy='all throws aimed at the enemy position (aimoff calibrated at 350u)',
        cond_misses='allowed (that is the measurement)', cond_start_stacks='n/a', cond_activations='Alchemical Fire', cond_distance='350u', cond_targets='enemies=1 allies=0',
        readbacks='distance_m,activation:Alchemical Fire', player_title='Does the flask land?', player_what='Throw at a moving bot', player_why='How often does it hit?', player_short='Flask hit rate', player_expect='Hits out of 10 throws',
        result_says='WORKS (h read as hits/throws per movement pattern) if standing > strafing > fleeing; DOES NOT WORK if the pattern has no effect'),
    body=lambda: ['setup Bebop Haze'] + COMMON_SETUP + ['hardreset', 'souls 30000', 'give upgrade_thermal_detonator', 'basemods', 'enemies 1 300 4', 'fetch 350'] + sum([['emove %s 7 12' % pat, 'mark H_%s' % pat] + ['cast i1 1.5'] * 10 + ['mark none', 'wait 3'] for pat in ('stand', 'strafe', 'flee')], []) + ['end'],
    blocked='enemy_move_script')

def write_all(lint=True):
    os.makedirs(OUT, exist_ok=True); os.makedirs(EVD, exist_ok=True)
    out = []
    for name, s in SPECS.items():
        m = dict(s['meta'])
        if s.get('blocked'): m['blocked_by'] = s['blocked']
        txt = '# duo test request generated by council/tools/duo.py sandbox (duo-v1)\n# %s\n' % s['note'] + meta(m) + '\n'.join(s['body']()) + '\n'
        p = '%s/%s.txt' % (OUT, name)
        open(p, 'w').write(txt)
        ev = ['KIND: duo-evidence', 'SCENARIO: ' + name, 'STATUS: ' + ('UNTESTABLE-NOW (blocked_by %s)' % s['blocked'] if s.get('blocked') else 'RUNNABLE on the current runner source (PC build state UNVERIFIED)'),
              'NOTE: ' + s['note'], 'QUESTION: ' + m['question'], 'MECHANICS: ' + m['mechanics'], 'MODEL USE: ' + m['feeds'], 'RESULT RULE: ' + m['result_says']]
        open('%s/%s.txt' % (EVD, name), 'w').write('\n'.join(ev) + '\n')
        out.append(p)
    return out

if __name__ == '__main__':
    for p in write_all(): print(p)

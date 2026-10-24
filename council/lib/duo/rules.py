"""Mechanics rules: (carry NEED) x (partner OFFER) -> Match with numeric feasibility checks.
A rule never assumes a mechanic the data does not state: every unresolved link goes into m['unknown'] and caps the match.
Constants in ASSUME are the only free parameters; each is reported and swept in the sensitivity analysis (duo.py sens)."""
import re
UNK = 'UNKNOWN'

ASSUME = dict(
    t_react=0.35,        # s between "partner effect lands" and "carry can act on it" (human reaction + animation); swept 0.2..0.8
    gap_typical=20.0,    # m: typical distance between a short-range carry and the enemy it wants (ASSUMED, swept 12..30)
    close_m=12.0, medium_m=25.0, long_m=40.0,     # effective weapon range classes (ASSUMED; weapon attr names come from heroes.vdata)
    run_speed=None,      # filled per target from heroes.vdata EMaxMoveSpeed of the reference enemy (6.4..7.5 m/s DATA); default 7.0
    shred_base_resist=(0.10, 0.35),   # enemy bullet/spirit resist range ASSUMED (STRAT_P enemy_at uses 0.05..0.35)
)

HARD_HOLD = ('cc_stun', 'cc_immobilize')
SOFT_HOLD = ('cc_sleep',)       # breaks on damage
NO_DAMAGE = ('cc_petrify',)     # target blocks ALL damage -> cannot be used as a damage window

def _num(x):
    return x if isinstance(x, (int, float)) else None

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def target_anchored(n, carry):
    """True if the delayed effect is anchored on the unit it was cast on (target moves -> effect moves), False if on the ground,
    None if unknown. Unit-targeted = ability has a cast range and enemy-hero target type and no projectile behaviour."""
    a = carry_ability(carry, n['ability'])
    if a is None: return None
    B = a.behaviors
    if 'CITADEL_ABILITY_BEHAVIOR_PROJECTILE' in B or 'CITADEL_ABILITY_BEHAVIOR_NO_TARGET' in B: return False
    if (a.p('AbilityCastRange', 3) or 0) > 0 and any('HERO_ENEMY' in t for t in a.targets): return True
    return None

def carry_ability(kit, cls):
    for a in kit.abilities:
        if a.cls == cls: return a
    return None

def reliability(partner, o):
    """how reliably the partner's ability lands, from behaviour flags and the ability text (DATA/TEXT); factors are ASSUMED and swept:
    unit-targeted lock 1.0 | no-target self-centred area 0.8 | ground-targeted area / delayed detonation 0.75 | projectile (aimed) 0.7"""
    a = carry_ability(partner, o['ability'])
    if a is None: return 1.0, 'ability not found'
    B = a.behaviors; t = a.fulltext().lower()
    if 'CITADEL_ABILITY_BEHAVIOR_PROJECTILE' in B and 'PASS_THROUGH' not in ' '.join(B): return 0.7, 'projectile (must be aimed; can miss)'
    if re.search(r'target an area|detonates after|after a delay|ground', t): return 0.75, 'ground area with delayed effect (target can leave before it lands)'
    if 'CITADEL_ABILITY_BEHAVIOR_NO_TARGET' in B: return 0.8, 'no-target area around the caster'
    if (a.p('Radius', 3) or 0) > 0 and (a.p('AbilityCastRange', 3) or 0) > 0 and not re.search(r'target an enemy|curse an enemy|target enemy|enemy hero', t): return 0.75, 'ground-targeted area'
    return 1.0, 'unit-targeted'

def cd_of(o):
    c = o.get('cd')
    if isinstance(c, (list, tuple)):
        v = [x for x in c if isinstance(x, (int, float)) and x > 0]
        return v[-1] if v else None
    return _num(c)

def avail(n, o):
    """fraction of the carry's casts the partner's effect can be up for: min(1, cd_carry/cd_partner) (charges ignored; ASSUMED simple ratio)"""
    cp = cd_of(o); cc = _num(n.get('cd'))
    if not cp or not cc: return 1.0, 'cooldown unknown'
    cps = [x for x in (o.get('cd') or []) if isinstance(x, (int, float)) and x > 0]
    cp0 = cps[0] if cps else cp          # conservative: unupgraded partner cooldown
    return min(1.0, cc / max(cp, cp0)), 'carry ability %gs vs partner effect %gs (unupgraded %gs)' % (cc, cp, cp0)

def M(rule, need, offer, mech, checks, unknown, q, **kw):
    d = dict(rule=rule, need=need, offer=offer, mech=mech, checks=checks, unknown=unknown, q=q)
    d.update(kw)
    if 'functional' not in d: d['functional'] = (q is not None and q >= 0.5 and not kw.get('invalid'))
    return d

def ok(name, passed, detail):
    return dict(name=name, ok=passed, detail=detail)

# ---------------------------------------------------------------- R1 hold for a delayed / charged payload
def r_hold(carry, partner, n, o):
    if n['kind'] not in ('delayed_payload', 'charge_or_lockon'): return None
    if o['kind'] not in HARD_HOLD + SOFT_HOLD + NO_DAMAGE + ('remove_target',): return None
    if o.get('condition'): return None     # a CONDITIONAL hold (only on failure / wall / trap-escape / stays-still) is not a reliable hold: the enemy chooses whether it applies
    D = _num(n.get('delay'))
    d = _num(o['params'].get('duration'))
    chk = []; unk = []
    anch = target_anchored(n, carry) if n['kind'] == 'delayed_payload' else None
    if n['kind'] == 'delayed_payload' and anch is True:
        return M('HOLD', n, o, 'payload is anchored on the unit it targets (moves with it); holding the unit in place does not change where it lands', [ok('payload anchored on ground', False, 'ability is unit-targeted')], [], 0.0, invalid=True)
    if n.get('self_applied_hold'):
        return None
    if o['kind'] in NO_DAMAGE or o['kind'] == 'remove_target':
        return M('HOLD', n, o, '%s makes the target immune to / out of play for damage; it cannot host a damage payload' % o['kind'], [ok('target can be damaged during hold', False, o['kind'])], [], 0.0, invalid=True)
    if d is None:
        unk.append('hold duration of %s not in data' % o['aname']); q = None; margin = None
    else:
        margin = d - (ASSUME['t_react'] + (D or 0))
        chk.append(ok('hold covers reaction + delay', margin >= 0, '%.2f s hold - (%.2f react + %.2f delay) = %+.2f s' % (d, ASSUME['t_react'], D or 0, margin)))
        q = clamp(margin / max(D or 0.5, 0.5)) if margin >= 0 else 0.0
    sleep = o['kind'] == 'cc_sleep'
    forgone = None
    if sleep:
        chk.append(ok('carry can avoid damaging the sleeper until the payload lands', None, 'sleep breaks %.2fs after damage (SleepWakeUpDelay) - every other hit of the carry during the window wakes the target' % (_num(o['params'].get('wake_delay_after_damage')) or 0)))
        forgone = D
        if q: q *= 0.6   # window only guarantees the first payload and costs the carry's fire during D (conservative haircut, swept)
    if n['kind'] == 'charge_or_lockon':
        unk.append('whether the charge/lock-on keeps its target through the hold (unit lock-on rules not in data)')
    if o.get('breaks_on_damage') and not sleep: pass
    rel, relwhy = reliability(partner, o)
    if q: q = q * rel
    chk.append(ok('partner ability lands reliably', None, '%s -> x%.2f (ASSUMED factor)' % (relwhy, rel)))
    av, avwhy = avail(n, o)
    if q: q = q * av
    chk.append(ok('partner effect available', av >= 0.5, avwhy + ' -> x%.2f' % av))
    cd = cd_of(o)
    mech = '%s holds the target %ss; carry payload "%s" needs %ss on the ground area' % (o['aname'], ('%g' % d) if d is not None else '?', n['aname'], ('%g' % D) if D is not None else '?')
    return M('HOLD', n, o, mech, chk, unk, q, functional=(margin is not None and margin >= 0 and rel >= 0.7 and av >= 0.5), margin=margin, sleep=sleep, forgone_fire_s=forgone, window=d, tier=o['tier'], rel=rel, partner_cd=cd)

# ---------------------------------------------------------------- R2 bring the target to the carry (or the carry to the target)
def r_range(carry, partner, n, o):
    if n['kind'] not in ('close_range_weapon', 'short_range', 'conditional_close_range'): return None
    k = o['kind']
    if k not in ('displace_pull', 'displace_tether', 'displace_swap', 'displace_portal', 'ally_move', 'displace_teleport_target'): return None
    chk = []; unk = []
    rng = _num(o['params'].get('cast_range')) if k == 'ally_move' else None
    if k == 'ally_move':
        # moves the CARRY next to the target instead
        mech = '%s moves the carry itself (%s); closes distance by ability range/speed' % (o['aname'], ', '.join('%s=%s' % kv for kv in list(o['params'].items())[:3]))
        unk.append('whether the carried ally may shoot/cast at the destination (see carry rule) and where the carry lands relative to the enemy')
        reach = _num(o['params'].get('AllyDistance')) or _num(o['params'].get('cast_range')) or 10.0
        q = clamp(reach / ASSUME['gap_typical']) * 0.7
        return M('RANGE', n, o, mech, chk, unk, q, reach=reach, constraint='carry must be where the partner can reach him; destination chosen by partner' if k == 'ally_move' else '')
    reach = None
    for key in ('PullDistance', 'EnemyDragSpeed', 'TetherRadius', 'ChainLength', 'MultiSwap', 'TeleportBackOffsetFromTarget', 'DoorwayDistance', 'AbilityCastRange'):
        v = _num(o['params'].get(key))
        if v: reach = v if key not in ('EnemyDragSpeed',) else reach
    # cast range of the partner's ability = distance over which an enemy can be brought to the puller
    pa = None
    for a in partner.abilities:
        if a.cls == o['ability']: pa = a
    cr = pa.p('AbilityCastRange', 3) if pa else None
    if cr: reach = max(reach or 0, cr)
    if reach is None:
        unk.append('displacement distance not in data'); q = None
    else:
        if reach > 200: reach = reach / 10.0   # unit-scale properties (e.g. PullDistance 800) are in inches/units, not metres
        q = clamp(reach / ASSUME['gap_typical'])
        chk.append(ok('reach vs typical gap', reach >= 8, '%.1f m reach vs ASSUMED %.0f m typical gap' % (reach, ASSUME['gap_typical'])))
    where = 'next to the partner' if k in ('displace_pull',) else ('inside the partner-defined area' if k in ('displace_tether', 'displace_portal') else 'at the partner swap point')
    mech = '%s relocates the enemy %s; carry then needs to stand within its own range (%s) of that point' % (o['aname'], where, n['kind'])
    unk.append('exact landing point relative to the partner and enemy facing (physics not in data)')
    return M('RANGE', n, o, mech, chk, unk, q, reach=reach, constraint='carry within weapon range of %s' % where)

# ---------------------------------------------------------------- R3 keep the target inside the carry's zone
def _r_zone(carry, partner, n, o):
    if n['kind'] != 'zone_occupancy': return None
    k = o['kind']
    if k not in ('slow', 'cc_stun', 'cc_immobilize', 'displace_tether', 'displace_pull'): return None
    R = _num(n.get('radius')); T = _num(n.get('duration'))
    chk = []; unk = []
    v = 7.0
    if n.get('anchored'):
        unk.append('zone is centred on the caster (moves with him): holding the enemy still does not keep him in it unless the caster stays')
    if k == 'slow':
        s = clamp((_num(o['params'].get('pct')) or 0) / 100.0, 0, 0.9)
        if not R or not T: return None
        base = 2 * R / v
        gain = base / max(0.1, (1 - s)) - base
        d = _num(o['params'].get('duration'))
        if d is None: unk.append('slow duration not in data')
        q = clamp(gain / max(T, 1.0))
        chk.append(ok('slow increases dwell time in zone', gain > 0.3, 'crossing a %.1f m zone at %.1f m/s: %.2f s -> %.2f s with %d%% slow' % (2 * R, v, base, base / (1 - s), s * 100)))
        return M('ZONE', n, o, '%s slows the enemy so it spends longer inside "%s"' % (o['aname'], n['aname']), chk, unk, q, gain=gain)
    if o['kind'] == 'cc_sleep' or o.get('breaks_on_damage'):
        return M('ZONE', n, o, 'sleep wakes %ss after the first damage, and the carry zone deals damage every tick: the sleeper is awake almost immediately' % (_num(o['params'].get('wake_delay_after_damage')) or '~0.1'), [ok('hold survives the zone damage', False, 'IS_ASLEEP breaks on damage')], [], 0.0, invalid=True)
    d = _num(o['params'].get('duration'))
    if d is None:
        unk.append('hold duration not in data'); return M('ZONE', n, o, '%s holds enemy inside "%s"' % (o['aname'], n['aname']), chk, unk, None)
    cover = min(d, T or d)
    rel, relwhy = reliability(partner, o)
    av, avwhy = avail(n, o)
    q = clamp(cover / max(T or 1.0, 1.0)) * rel * av
    chk.append(ok('hold overlaps zone', cover > 0.5, '%.2f s of %.2f s zone covered if the hold lands inside it' % (cover, T or 0)))
    unk.append('the hold must land while the target is inside the zone area (placement order: zone first or hold first?)')
    return M('ZONE', n, o, '%s holds the enemy in place inside "%s" for %.2fs' % (o['aname'], n['aname'], cover), chk, unk, q, hold=cover)

def r_zone(carry, partner, n, o):
    m = _r_zone(carry, partner, n, o)
    if m and n.get('anchored'):
        m['functional'] = bool(m['q'] is not None and m['q'] >= 0.5)
        m['speculative'] = True      # caster-centred / moving zone: whether holding the ENEMY keeps it inside depends on caster movement - cannot be decided from data
        if m['q'] is not None: m['q'] = min(m['q'], 0.3)
    return m

# ---------------------------------------------------------------- R4 create the state a conditional bonus needs
def r_state(carry, partner, n, o):
    if not n['kind'].startswith('conditional_'): return None
    st = n['state']; k = o['kind']
    chk = []; unk = []
    if st == 'wall':
        if k in ('displace_pull', 'displace_tether', 'displace_portal', 'displace_swap', 'displace_teleport_target'):
            ctrl = 1.0 if k in ('displace_pull', 'displace_portal', 'displace_teleport_target') else 0.5
            unk += ['whether a displaced enemy counts as "near a wall" is evaluated at cast time of the carry (not in data)', 'a wall must exist within the stated distance of the landing point (map-dependent)']
            return M('STATE', n, o, '%s chooses where the enemy stands, so it can be placed beside terrain for the carry\'s wall condition' % o['aname'], chk, unk, 0.5 * ctrl, terrain_required=True)
        return None
    if st == 'isolated':
        if k in ('displace_pull', 'displace_tether', 'displace_portal', 'displace_swap', 'cc_stun', 'cc_immobilize', 'remove_target'):
            unk += ['HOW "isolated"/nearby enemies are counted (radius, line of sight, whether the displaced target counts) is not in the data - must be measured']
            return M('STATE', n, o, '%s could separate the target from its team, which is the condition of "%s"' % (o['aname'], n['aname']), chk, unk, None, speculative=True)
        return None
    if st in ('marked_or_revealed', 'revealed'):
        if k == 'reveal':
            unk.append('whether a reveal applied by another hero satisfies the carry\'s "revealed target" condition (applier-specific modifiers are not in data)')
            return M('STATE', n, o, '%s reveals the enemy; carry ability "%s" rewards revealed/marked targets' % (o['aname'], n['aname']), chk, unk, None, speculative=True)
        return None
    if st == 'stacks_on_target':
        # sustained single-target focus: a hold that does not break on damage keeps the stacks building
        if k in HARD_HOLD or k == 'displace_tether':
            d = _num(o['params'].get('duration')) or _num(o['params'].get('TetherDuration'))
            if d is None: unk.append('hold duration not in data'); q = None
            else: q = clamp(d / 5.0)
            unk.append('stack gain rate while the target is held (hit rate) - measurable only in the sandbox')
            return M('STATE', n, o, '%s keeps one target still so on-target stacks of "%s" can build' % (o['aname'], n['aname']), chk, unk, q, hold=d)
        if k == 'cc_sleep':
            return M('STATE', n, o, 'sleep wakes on the first damage: stacks cannot build during the sleep', [ok('hold survives damage', False, 'IS_ASLEEP breaks')], [], 0.0, invalid=True)
        return None
    if st == 'low_health':
        return None   # damage-conditioned: any damage dealer qualifies -> handled as ordinary compatibility elsewhere
    if st == 'close_range':
        if k in ('displace_pull', 'displace_tether', 'displace_portal', 'displace_swap'):
            unk.append('reach/landing point (see RANGE rule)')
            return M('STATE', n, o, '%s brings the target inside the close-range window of "%s"' % (o['aname'], n['aname']), chk, unk, 0.4)
        return None
    return None

# ---------------------------------------------------------------- R5 move a channelling carry
def _relocates_ally(partner, o):
    """does the partner's ability relocate the ALLY (grab/lift/drag/teleport with)? decided from ability text (TEXT grade); trails/speed buffs and 'caster jumps to ally' are not relocations"""
    a = carry_ability(partner, o['ability'])
    if a is None: return False
    t = a.fulltext().lower()
    if re.search(r'jump to an ally|nap alongside', t): return False
    return bool(re.search(r'grab an ally|take flight with them|bring nearby allies|target friendly heroes instead|drag|pulls? (?:an )?ally|carries? (?:an )?ally|teleport(?:s|ing)? (?:your |an )?ally', t))

def r_carry(carry, partner, n, o):
    if n['kind'] != 'exposed_channel' or o['kind'] != 'ally_move': return None
    if not n.get('rooted') or not _relocates_ally(partner, o): return None
    if not (n.get('radius') or n.get('dps') or n.get('damage')): return None
    chk = []; unk = []
    intr = set('MODIFIER_STATE_' + s for s in n.get('interrupted_by', []))
    applied = set(o.get('states_applied', []))
    clash = sorted(s.replace('MODIFIER_STATE_', '') for s in intr & applied)
    chk.append(ok('carry states do not interrupt the channel', not clash, 'channel interrupted by %s; carry applies %s' % (sorted(s.replace('MODIFIER_STATE_', '') for s in intr), sorted(s.replace('MODIFIER_STATE_', '') for s in applied)[:8]) + (' CLASH %s' % clash if clash else '')))
    block = sorted(s.replace('MODIFIER_STATE_', '') for s in applied if s in ('MODIFIER_STATE_SILENCED', 'MODIFIER_STATE_COMMAND_RESTRICTED', 'MODIFIER_STATE_STUNNED', 'MODIFIER_STATE_COMBAT_ABILITIES_DISABLED', 'MODIFIER_STATE_IS_ASLEEP'))
    chk.append(ok('carry does not lock abilities', not block, 'ability-locking states applied: %s' % (block or 'none in data')))
    unk.append('whether an ability can be CAST/CHANNELLED while the ally is carried (cast rules beyond state masks are not in data)')
    d = _num(o['params'].get('duration')); ch = _num(n.get('channel'))
    if d is None: unk.append('carry duration not in data'); q = None
    else:
        q = clamp(min(d, ch or d) / max(ch or d, 1.0))
        chk.append(ok('carry outlasts the channel', d >= (ch or 0), '%.1f s carry vs %.1f s channel' % (d, ch or 0)))
    pen = o.get('own_outgoing_dmg')
    if pen: chk.append(ok('damage penalty while carried', None, 'carried ally outgoing damage %+g%%' % pen))
    av, avwhy = avail(n, o)
    if q: q *= av
    chk.append(ok('partner effect available', av >= 0.5, avwhy + ' -> x%.2f' % av))
    if clash or block: q = 0.0
    return M('CARRY', n, o, '%s relocates the carry while "%s" channels, repositioning its area/beam over enemies' % (o['aname'], n['aname']), chk, unk, q, invalid=bool(clash or block), penalty=pen, speculative=True)

# ---------------------------------------------------------------- R6 protect the channel
def r_protect(carry, partner, n, o):
    if n['kind'] != 'exposed_channel': return None
    k = o['kind']
    if k not in ('barrier', 'immunity', 'cleanse', 'cc_stun', 'cc_immobilize', 'displace_knock_away'): return None
    chk = []; unk = []
    if k in ('barrier', 'immunity', 'cleanse') and o['side'] == 'self': return None
    if k == 'barrier':
        intr = n.get('interrupted_by', [])
        dmg_int = [s for s in intr if s in ('DAMAGE', 'TAKES_DAMAGE')]
        chk.append(ok('barrier addresses the interrupt', bool(dmg_int), 'channel is interrupted by %s only; a barrier absorbs damage and does not stop %s' % (intr, ', '.join(intr))))
        if not dmg_int:
            return M('PROTECT', n, o, '%s absorbs damage on the channeller but the channel is interrupted by %s, not by damage' % (o['aname'], intr), chk, [], 0.0, invalid=True)
        return None
    if k == 'immunity':
        st = o['params'].get('states', [])
        stopper = any(s in ('UNSTOPPABLE', 'STATUS_IMMUNE') for s in st)
        if not stopper or o['side'] != 'ally': return None
        return M('PROTECT', n, o, '%s grants immunity to the channeller' % o['aname'], chk, ['can it be cast on an ally?'], 0.6, generic=True)
    if k in ('cc_stun', 'cc_immobilize'):
        return None
    return None

# ---------------------------------------------------------------- R7 shared debuffs for a damage dealer (generic amplification)
def r_amp(carry, partner, n, o, carry_type):
    if n['kind'] not in ('amp_target',): return None
    return None

RULES = [r_hold, r_range, r_zone, r_state, r_carry, r_protect]

def match_pair(carry, partner):
    """all matches carry(need) x partner(offer); carry != partner"""
    out = []
    for n in carry.needs:
        for o in partner.offers:
            if o.get('unusable'): continue
            for r in RULES:
                m = r(carry, partner, n, o)
                if m: out.append(m)
    return out

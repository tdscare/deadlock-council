#!/usr/bin/env python3
"""INTERACTION DISCOVERY ENGINE (council/tools/discover_interactions.py)  -- generic, no hero/ability/item names in any rule.

Pipeline:  game data --(lib/effects/extract.py)--> typed EFFECTS --(relation templates T1..T6)--> HYPOTHESES
           --> score (impact/plausibility/availability/testability) --> VIABILITY LADDER --> scenario specs + reports.
Commands (run with python3 -I from the scratchpad root):
  extract                      write council/evidence/interactions/effects/{heroes,items}.json
  run [--hero hero_x] [--top N] [--out DIR]   generate + rank hypotheses for all heroes (or one), write
                               council/evidence/interactions/hypotheses/{ranked.json,ranked.txt} and validated/mechanics_verified.json
  show <hypothesis id>         print one hypothesis with ladder
  scenarios [--top N]          write sandbox scenario specs for the top TESTABLE hypotheses into
                               council/sandbox/autorun/scenarios/interaction/ and print `queue.js add` commands (never pushes to a queue)
  selfcheck                    verifies that no rule/output depends on seeded names (opaque-relabel invariance)
Evidence tiers: VERIFIED MECHANIC (game data) | MEASURED (sandbox result) | MODELLED (arithmetic on data with labelled assumptions) | HYPOTHESIS.
Measured results in validated/measured.json (entries with `links`) are READ by `run`: the matching hypothesis becomes MEASURED (ladder stage 2) and T5 siblings are re-ranked by an explicit rule (see apply_measured / BOOST). `rerank-diff` prints the ranking with and without the measured results.
Event classes for T5 are derived from the data (shared property-key stems between ability and item properties that also occur in ability and item text), not from a written list. Hypotheses whose relation class matches validated/user_example_patterns.json are flagged user_example_derived and penalised; at most ITEM_CAP hypotheses per item stay in the list (the rest are in meta.overflow). Hypotheses live in hypotheses/, only data facts in validated/.
"""
import os, sys, json, re, hashlib, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
COUNCIL = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(COUNCIL, 'lib', 'effects')); sys.path.insert(0, HERE)
import extract as X

EVD = os.path.join(COUNCIL, 'evidence', 'interactions')
SCEN_DIR = os.path.join(COUNCIL, 'sandbox', 'autorun', 'scenarios', 'interaction')
PRICE = {1: 800, 2: 1600, 3: 3200, 4: 6400}   # SECONDARY evidence (wiki); not in game files

# ---------------------------------------------------------------- sandbox capability model (from council/sandbox/AUTORUN.md + src/*.cs read 2026-10-24)
CAPS = {
 'cast_slot':               ('HAVE', 'cast <1-4> in Scenario.cs'),
 'cast_item_active':        ('HAVE', 'cast i1..i5'),
 'give_item':               ('HAVE', 'give <class>'),
 'imbue_item':              ('UNVERIFIED', '`imbueown <item> <slot>` / `imbue` exist in src; effect on the imbued ability never verified'),
 'ability_tier_set':        ('HAVE', 'abil <bits> / unlock; verify with expect/cds'),
 'timed_rotation':          ('HAVE', 'rot / wait / cast sequences'),
 'modifier_names_readback': ('HAVE', '`mods` logs modifier names of player and enemy (no remaining duration, no stack count)'),
 'modifier_duration_readback': ('MISSING', 'mods gives names only'),
 'cooldown_readback':       ('PARTIAL', '`cds` start/end unreliable for some abilities; trustworthy only on a fresh pawn'),
 'self_cast_ally_ability':  ('UNVERIFIED', 'cast forces ONE button; alt-cast + ability together is not supported; auto self-cast when no ally is aimed is untested'),
 'ally_bot':                ('MISSING', 'no allied bot (GAPS #10)'),
 'real_enemy_damage_source':('MISSING', 'bots never shoot; `incoming` uses Hurt() (bypasses OnTakeDamage; damage-taken modifiers not shown to react)'),
 'apply_cc_to_player':      ('MISSING', 'no ecc op (GAPS #7)'),
 'melee_attack':            ('HAVE', 'cast melee'),
 'damage_csv':              ('HAVE', 'damage_*.csv per hit'),
 'heal_diff':               ('HAVE', 'healDiffObserved'),
}
def cap_ok(n):
    return CAPS[n][0] in ('HAVE', 'PARTIAL')

# ---------------------------------------------------------------- helpers over extractor output
def load_effects():
    D = X.load()
    return D, X.hero_effects(D), X.item_effects(D)

def ab_by_slot(h, slot):
    for a in h['abilities']:
        if a['slot'] == slot:
            return a
def kit(h):
    return [a for a in h['abilities'] if isinstance(a['slot'], int)]
def E_(a, op=None, state=None, sub=None, grade=None):
    out = []
    for e in a['effects']:
        if op and e['op'] != op: continue
        if state and e['state'] != state: continue
        if sub and (e['subtype'] not in (sub if isinstance(sub, (list, tuple, set)) else [sub])): continue
        if grade and e['evidence'][0]['grade'] != grade: continue
        out.append(e)
    return out
def hid(*parts):
    return hashlib.sha1('|'.join(map(str, parts)).encode()).hexdigest()[:10]
def fnum(x, d=None):
    return x if isinstance(x, (int, float)) else d
def tier_of(e):
    t = e['tier_needed']
    return 0 if t == 'item' else t
def ref(a, e):
    ev = e['evidence'][0]
    return dict(ability=a['cls'], name=a['name'], slot=a['slot'], effect=e['id'], op=e['op'], subtype=e['subtype'], tier=e['tier_needed'], grade=ev['grade'],
                src='%s:%s' % (ev['file'], ev['key']), value=ev.get('value', ev.get('matched')))
def bytier(v, t):
    return v[min(t, 3)] if v else None
def ult_cost_note(a):
    return 'ultimate (long cooldown, typically once per major fight)' if a['is_ult'] else None

# ---------------------------------------------------------------- scoring
def info_value(plaus):
    """value of information 0..5: highest when the data leaves the outcome open (plausibility near the middle), lowest when data already predicts yes or no."""
    p = max(0.0, min(1.0, plaus / 5.0))
    return round(5.0 * (1.0 - abs(2 * p - 1) * 0.8), 2)

def score(impact, plaus, avail, test):
    """priority for running an experiment: 0.35 impact + 0.2 information value + 0.1 plausibility + 0.15 availability + 0.2 testability (all 0..5). Generic weights, no per-case terms."""
    return round(0.35 * impact + 0.2 * info_value(plaus) + 0.1 * plaus + 0.15 * avail + 0.2 * test, 2)

def availability_of(parts, items=()):
    """0..5 : earlier tiers, shorter cooldowns, cheaper items => higher. parts = list of (ability, tier_needed)."""
    s = 5.0; notes = []
    for a, t in parts:
        if t:
            s -= 0.4 * t; notes.append('%s needs T%d' % (a['name'], t))
        cd = bytier(a['cooldown_by_tier'], t or 0)
        if a['is_ult']:
            s -= 1.0; notes.append('%s is an ultimate (cd %ss): about once per major fight' % (a['name'], cd))
        elif cd and cd > 60:
            s -= 0.5; notes.append('%s cd %ss' % (a['name'], cd))
    for it in items:
        p = PRICE.get(it['tier'])
        if p and p >= 3200:
            s -= 0.5 if p == 3200 else 1.0; notes.append('%s costs tier %d (~%s souls, secondary)' % (it['name'], it['tier'], p))
    return max(0.0, round(s, 1)), notes

def testability_of(needs):
    s = 5.0
    for n in needs:
        st = CAPS[n][0]
        s -= {'HAVE': 0, 'PARTIAL': 0.5, 'UNVERIFIED': 1.0, 'MISSING': 2.5}[st]
    return max(0.0, round(s, 1))

# ---------------------------------------------------------------- ladder
STAGES = ['1 mechanically possible (data)', '2 works reliably in controlled tests', '3 executable in combat', '4 substantial practical value', '5 worth changing a complete build']
def mk_ladder(s1, s2, s3, s4, s5):
    L = [dict(stage=STAGES[i], **x) for i, x in enumerate((s1, s2, s3, s4, s5))]
    cap = 0
    for i, x in enumerate(L):
        if x['status'] == 'EVIDENCED':
            cap = i + 1
        else:
            break
    return dict(stages=L, cap=cap, cap_text='highest stage evidenced: %s' % (STAGES[cap - 1] if cap else 'none (components only)'))
def st(status, tier, why, unknown=()):
    return dict(status=status, evidence_tier=tier, why=why, stage_unknowns=list(unknown))

# ---------------------------------------------------------------- T1: protective state x delayed / deferred damage cost
PROTECT_SUBS = {'invulnerable', 'damage_immune', 'protected_from_damage', 'ignore_bullets', 'ignore_melee', 'barrier'}
def timing_model(B, A, tB, tA):
    """window arithmetic from data numbers only (MODELLED). B = cost producer ability, A = protector ability."""
    m = {}
    buff = bytier(B['duration_by_tier'], tB)
    app_dur = None
    GEN = {'modifier', 'buff', 'debuff', 'ability', 'duration', 'base', 'the', 'hero', 'item'}
    for m_ in B['modifiers']:
        if m_['debuff_type'] != 'MODIFIER_DEBUFF_YES': continue
        mtok = {t for t in re.split(r'_', m_['cls'].lower()) if t not in GEN and len(t) > 2}
        for n, p in B['props'].items():
            ptok = {t.lower() for t in re.findall(r'[A-Z][a-z]+', n)} - GEN
            if n.endswith('Duration') and ptok & mtok:
                app_dur = bytier(p['by_tier'], tB)   # duration property sharing a name token with the penalty (debuff) modifier class
                break
        if app_dur: break
    ch = bytier(A['channel_time_by_tier'], tA)
    dur = bytier(A['duration_by_tier'], tA)
    window = ch if ch else dur
    cast_delay = A.get('cast_delay')
    m['cost_buff_duration_s'] = buff
    m['cost_application_duration_s'] = app_dur if app_dur else 'UNKNOWN'
    m['protect_window_s'] = window if window else 'UNKNOWN'
    m['protect_cast_delay_s'] = cast_delay
    m['protect_cooldown_s'] = bytier(A['cooldown_by_tier'], tA)
    m['interrupted_by'] = A['interrupted_by']
    m['window_scales_with'] = [p['scale'] for n, p in A['props'].items() if n == 'AbilityChannelTime' and p['scale']]
    if isinstance(window, (int, float)) and isinstance(app_dur, (int, float)):
        m['full_coverage_start_tolerance_s'] = round(max(0.0, window - app_dur), 2)
        m['instant_application_start_tolerance_s'] = round(window, 2)
        m['assumptions'] = ['protection starts when channel/duration starts (data does not say whether the cast delay is covered)',
                            'cost applies after the buff ends, over its application duration (as named); single-hit variant uses the instant tolerance']
    return m

def t1_protect_vs_cost(h, items):
    out = []
    ks = kit(h)
    Bs = [(a, e) for a in ks for e in E_(a) if e['op'] in ('defer', 'delayed_cost') and e['state'] == 'incoming_damage' and a['targeting']['side'] in ('self', 'self_or_ally', 'ally') and e['target'] in ('self', 'self_or_ally', 'ally')]   # cost must be BORNE by the recipient/caster (delayed damage dealt to enemies is not a drawback)
    protos = []
    for a in ks:
        for e in a['effects']:
            if e['state'] == 'incoming_damage' and e['subtype'] in PROTECT_SUBS and e['target'] in ('self', 'self_or_ally', 'ally') and tier_of(e) is not None:
                if e['subtype'] == 'barrier' and not bytier(a['duration_by_tier'], 3) and not e['magnitude']:
                    continue
                protos.append((a, e))
    import re as _re
    def self_borne(a):
        txt = ' '.join(d['text'] for d in a['desc'].values())
        friendly_debuff = a['targeting']['side'] in ('ally', 'self_or_ally') and any(m['debuff_type'] == 'MODIFIER_DEBUFF_YES' for m in a['modifiers'])
        return friendly_debuff or bool(_re.search(r'(incoming|taken|taking|receive[sd]?) damage|damage (you|they|it) (take|receive)', txt, _re.I))
    Bs = [(a, e) for a, e in Bs if self_borne(a)]
    seenB = {}
    for a, e in Bs:
        seenB.setdefault(a['cls'], (a, [])) [1].append(e)
    seenA = {}
    for a, e in protos:
        seenA.setdefault((a['cls'], e['subtype'], tier_of(e)), (a, e))
    for bcls, (B, Be) in seenB.items():
        flags = [e for e in B['effects'] if e['op'] == 'modifier_flag']
        ign = [e for e in flags if e['subtype'] == 'ignore_invulnerable']
        nop = [e for e in flags if e['subtype'] == 'cannot_be_purged']
        heals = [e for e in B['effects'] if e['subtype'] == 'interacts_with_incoming_heal']
        tB = max([tier_of(e) for e in Be] + [0])
        for (acls, sub, tA), (A, Ae) in seenA.items():
            if acls == bcls:
                continue
            typed_state = 'MODIFIER_STATE' in str(Ae['evidence'][0].get('value'))
            recipient_ok = B['targeting']['side'] in ('self', 'self_or_ally') and (A['targeting']['side'] in ('self', 'enemy', 'self_or_ally') or e_is_self(Ae))
            same_unit = 'caster only (protector targets self)' if (Ae['target'] in ('self',) or A['targeting']['side'] in ('self',)) else 'protector may target allies'
            tm = timing_model(B, A, tB, tA)
            tm_max = timing_model(B, A, 3, tA)
            bonus_p = next((p['by_tier'][0] for n, p in B['props'].items() if n.startswith('Deferred') and 'Bonus' in n), None)
            defer_p = next((p['by_tier'][0] for n, p in B['props'].items() if n.startswith('Deferred') and 'Bonus' not in n and 'Percent' in n), None)
            tm['at_max_cost_tier'] = {k: v for k, v in tm_max.items() if k.endswith('_s')}
            tm['cost_model'] = dict(deferred_pct=defer_p, extra_pct=bonus_p,
                formulas=['avoided by protector = (1 + extra_pct/100) x D, D = damage taken while the cost-ability is active (UNKNOWN, depends on enemies)',
                          'avoided by ordinary healing = same factor x min(D, H), H = healing received before the cost lands (UNKNOWN); data text says incoming healing is spent on the stored amount first',
                          'so the protector only beats healing on the part of D that healing cannot cover in time: gain <= factor x (D - H)'],
                label='MODELLED (formula on data numbers; assumes the extra scales with the remaining stored amount)')
            a_ok = tm.get('protect_window_s') not in (None, 'UNKNOWN')
            ch_locks = [e for e in A['effects'] if e['op'] == 'lockout_self']
            cond = []
            if ign: cond.append('DATA AGAINST: cost modifier carries MODIFIER_ATTRIBUTE_IGNORE_INVULNERABLE (%s); whether the protector counts as "invulnerable" for that flag is not in the data' % ign[0]['evidence'][0]['key'])
            if sub in ('damage_immune',) and not typed_state: cond.append('protector is a property flag (%s), NOT a MODIFIER_STATE_INVULNERABLE state; the data cannot say which damage types/sources it blocks' % Ae['evidence'][0]['key'])
            impact = 2.0 + (1.5 if Be[0]['subtype'] == 'deferred_damage' else 1.0) + (0.8 if A['is_ult'] else 0.5)
            plaus = 2.5 + (0.5 if typed_state else 0) - (1.5 if ign else 0) + (0.5 if Ae['evidence'][0]['grade'] == 'TEXT' else 0)
            av, anotes = availability_of([(B, tB), (A, tA)])
            needs = ['real_enemy_damage_source', 'cast_slot', 'modifier_names_readback', 'self_cast_ally_ability', 'damage_csv']
            if ch_locks: needs.append('apply_cc_to_player')
            hy = dict(
                id='T1-' + hid(h['hero'], bcls, acls, sub, tA), template='T1 protective state vs deferred/delayed cost', hero=h['hero'], hero_name=h['name'], scope='kit',
                title='%s: can %s (%s) stop what %s defers or charges later?' % (h['name'], A['name'], sub, B['name']),
                components=[ref(B, Be[0]), ref(A, Ae)] + [ref(B, e) for e in (ign + nop + heals)],
                orders=['cost-ability first, protector active when the delayed cost lands', 'protector first (pre-emptive), then cost-ability', 'protector expires before the cost lands (control arm)'],
                why='The kit contains an effect that stores/defers incoming damage or charges a penalty afterwards (%s) and a separate effect granting a damage-protection state (%s, T%s). If the protection state covers the moment the stored damage is applied, the drawback may disappear.' % (Be[0]['evidence'][0]['key'], Ae['evidence'][0]['key'], tA),
                competing_outcomes=['blocks the whole delayed application', 'blocks nothing (delayed damage ignores the protection / is not typed as blockable damage)', 'blocks part (only some ticks / only the extra penalty / only non-bonus portion)', 'protector ends or is interrupted before the cost lands: worse than not using it'],
                distinguishing_test='Log damage taken at the instant the cost modifier ends with the protector (a) covering it, (b) ended 0.5 s before, (c) cast at the buff mid-point; compare total HP lost and per-tick damage.',
                availability=dict(tier_needed=max(tB, tA), ult=bool(A['is_ult']), notes=anotes, once_per_fight=bool(A['is_ult'])),
                premises=[ref(B, e) for e in Be[:3]] + [ref(A, Ae)],
                unknown_fields=['damage types/sources blocked by the protector', 'whether protection starts at cast or at channel start', 'how the delayed cost is applied (one hit vs over time)', 'whether healing/other sustain cancels the stored amount first'] + (['whether the flagged ignore-invulnerable rule covers this protector'] if ign else []),
                conditions=cond, timing=tm, recipient_note=same_unit,
                scoring=dict(impact=round(impact, 1), plausibility=round(plaus, 1), availability=av, testability=testability_of(needs)),
                sandbox=dict(needs={n: CAPS[n][0] for n in needs}, status='TESTABLE-NOW' if all(cap_ok(n) for n in needs) else 'UNTESTABLE-NOW',
                             missing=[dict(cap=n, state=CAPS[n][0], detail=CAPS[n][1]) for n in needs if not cap_ok(n)]),
                alternatives=[dict(name='ordinary sustain / heal through', note='data text: incoming healing is spent on the stored amount first', model='needs the amount stored (UNKNOWN: depends on enemy damage) vs healing available'),
                              dict(name='cast the protector on its own for a different purpose', note='keeps the long-cooldown ability for a fight-deciding use'),
                              dict(name='do not use the deferral', note='no cost, no benefit')],
            )
            hy['scoring']['total'] = score(impact, plaus, av, hy['scoring']['testability']); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0)
            hy['ladder'] = mk_ladder(
                st('PARTIAL', 'VERIFIED MECHANIC (components) / HYPOTHESIS (combined outcome)', 'both components exist in game data at the stated tiers; whether the protector applies to the delayed cost is NOT determinable from data' + ('; data contains a flag pointing against it' if ign else ''), hy['unknown_fields'][:3]),
                st('NOT-EVIDENCED', 'HYPOTHESIS', 'no sandbox result exists; ' + ('blocked by: ' + ', '.join(m['cap'] for m in hy['sandbox']['missing']) if hy['sandbox']['missing'] else 'testable'), [m['cap'] for m in hy['sandbox']['missing']]),
                st('PARTIAL', 'MODELLED', 'timing tolerance from data numbers: %s; interrupt exposure: %s' % (json.dumps({k: v for k, v in tm.items() if k.endswith('_s')}), ','.join(A['interrupted_by']) or 'UNKNOWN'), ['cast delay coverage', 'enemy interrupt frequency (must be measured)', 'positioning while channeling/standing']),
                st('MODELLED', 'MODELLED', 'value = stored amount avoided; depends on damage taken while buffed (UNKNOWN) vs alternatives above; protector cooldown %ss is spent' % tm.get('protect_cooldown_s'), ['stored amount distribution', 'value of the alternative use of the protector']),
                st('NOT-EVIDENCED', 'HYPOTHESIS', 'requires stages 2-4 first', ['opportunity cost over the complete build']))
            out.append(hy)
    return out

def e_is_self(e):
    return e['target'] == 'self'

# ---------------------------------------------------------------- T2: cooldown reset on an imbued ability x ability worth repeating
def cdr_alternatives(items):
    """cooldown-reduction items (tier<=4, price known secondary). imbue_only=True: applies to the one imbued ability (fair for a single-ability comparison)."""
    alts = []
    for cls, it in items.items():
        if it['disabled'] or it['tier'] > 4: continue
        for n, p in it['props'].items():
            prov = p.get('provides') or ''
            if 'COOLDOWN_REDUCTION_PERCENTAGE' in prov and 'ULTIMATE' not in prov and 'ITEM_' not in prov and 'BETWEEN' not in prov and p['by_tier'][0] and p['by_tier'][0] > 0:
                alts.append(dict(item=it['name'], cls=cls, tier=it['tier'], cdr_pct=p['by_tier'][0], source='items.json %s.%s' % (cls, n), imbue_only=it['imbue'] == 'modifier_value'))
    return alts

def cast_model(ab, tier, item_cd, mult, window=180.0, alts=()):
    cd = bytier(ab['cooldown_by_tier'], tier); dur = bytier(ab['duration_by_tier'], tier) or 0.0
    if not cd: return None
    base_casts = window / cd
    cyc = item_cd + mult * cd            # item cooldown "increased by the cooldown of the imbued ability" (text); additive form is an ASSUMPTION
    extra = window / cyc
    m = dict(window_s=window, ability_cd_s=cd, ability_duration_s=dur, item_cd_s=item_cd, item_cd_formula='base + %.2f x imbued cd (ASSUMED additive; text + ImbuedCooldownMultiplier)' % mult,
             item_cycle_s=round(cyc, 1), casts_base=round(base_casts, 2), casts_with_item=round(base_casts + extra, 2), extra_casts=round(extra, 2),
             uptime_base=round(base_casts * dur / window, 3), uptime_with_item=round((base_casts + extra) * dur / window, 3))
    m['uptime_gain'] = round(m['uptime_with_item'] - m['uptime_base'], 3)
    alt_rows = []
    for a in alts:
        r = a['cdr_pct'] / 100.0
        casts = base_casts / (1 - r)
        alt_rows.append(dict(item=a['item'], tier=a['tier'], cdr_pct=a['cdr_pct'], uptime=round(casts * dur / window, 3), uptime_gain=round((casts - base_casts) * dur / window, 3), souls_secondary=PRICE.get(a['tier']), source=a['source'], applies_to='imbued ability only' if a.get('imbue_only') else 'all abilities'))
    m['alternatives_same_ability'] = sorted(alt_rows, key=lambda r: -r['uptime_gain'])[:4]
    return m

def t2_reset_items(h, items, alts):
    out = []
    resets = [it for it in items.values() if not it['disabled'] and it['imbue'] in ('active', 'active_non_ult') and any(e['op'] == 'reset_cd' for e in it['effects'])]
    for it in resets:
        reset_e = next(e for e in it['effects'] if e['op'] == 'reset_cd')
        mult_p = it['props'].get('ImbuedCooldownMultiplier'); mult = (mult_p['by_tier'][0] / 100.0) if mult_p else 0.0
        for a in kit(h):
            if a['is_ult'] and it['imbue'] == 'active_non_ult': continue
            if a['slot'] not in (1, 2, 3, 4): continue
            prot = [e for e in a['effects'] if (e['op'] in ('heal', 'absorb', 'grant', 'apply_cc', 'remove_cc', 'displace', 'amplify')) and e['target'] != 'unknown']
            t_best = 3 if any(v for v in (a['duration_by_tier'] or [0])) or prot else 0
            cd = bytier(a['cooldown_by_tier'], 3)
            if not cd or cd < 8: continue
            dur = bytier(a['duration_by_tier'], 3) or 0
            if not prot and not dur: continue
            ally = a['targeting']['side'] in ('ally', 'self_or_ally', 'any')
            lock = [e for e in a['effects'] if e['op'] == 'lockout_target' and e['evidence'][0]['grade'] == 'TEXT' and e['target'] in ('self_or_ally', 'ally', 'self')]
            ext = [e for e in a['effects'] if e['subtype'] == 'duration_extendible']
            protect_txt = [e for e in a['effects'] if e['subtype'] in ('protected_from_damage', 'damage_immune', 'invulnerable', 'heal_or_sustain') and e['target'] in ('self', 'self_or_ally', 'ally')]
            model = cast_model(a, 3, fnum((it['props'].get('AbilityCooldown') or {}).get('by_tier', [None])[0], 30.0), mult, alts=alts)
            if not model: continue
            pr = PRICE.get(it['tier'])
            if pr:
                model['item_uptime_gain_per_1000_souls'] = round(model['uptime_gain'] / (pr / 1000.0), 4)
                for r in model['alternatives_same_ability']:
                    r['uptime_gain_per_1000_souls'] = round(r['uptime_gain'] / (r['souls_secondary'] / 1000.0), 4) if r.get('souls_secondary') else 'UNKNOWN'
                model['price_basis'] = 'tier prices 800/1600/3200/6400 are SECONDARY (wiki), not game files; modelled uptime ignores that stacking items multiply and that the item also has its own longer cooldown'
            subs = {e['subtype'] for e in prot}
            pv = (1.0 if subs & {'invulnerable', 'protected_from_damage', 'damage_immune'} else 0) + (0.8 if 'heal_or_sustain' in subs else 0) + (0.6 if 'barrier' in subs else 0) + (0.5 if 'cleanse' in subs else 0) + (0.3 if subs & {'hard_cc', 'slow'} else 0) + (0.2 if 'displacement' in subs else 0)
            impact = 0.8 + min(1.5, cd / 50.0) + pv + (0.8 if ally else 0.0) + (0.5 if lock else 0)
            plaus = 3.0 + (0.8 if reset_e['evidence'][0]['grade'] == 'TEXT' else 0) - (0.8 if lock and not ally else 0)
            av, anotes = availability_of([(a, 3)], [it])
            needs = ['give_item', 'imbue_item', 'cast_slot', 'cast_item_active', 'modifier_names_readback']
            if ally: needs.append('self_cast_ally_ability')
            qs = ['does the 2nd cast on the SAME recipient refresh, extend, stack or do nothing?']
            if ally: qs.append('can the 2nd cast go to a DIFFERENT ally (needs two allies in range)?')
            if lock: qs.append('while the recipient is locked out (text: cannot act), can the recipient/caster activate the item or cast again?')
            hy = dict(
                id='T2-' + hid(h['hero'], it['cls'], a['cls']), template='T2 cooldown reset on imbued ability vs repeatable effect', hero=h['hero'], hero_name=h['name'], scope='kit x item',
                title='%s: %s imbued on %s (cast, reset, cast again)' % (h['name'], it['name'], a['name']),
                components=[ref(a, e) for e in (protect_txt[:1] + lock[:1] + ext[:1])] + [dict(item=it['cls'], name=it['name'], effect=reset_e['id'], op='reset_cd', grade=reset_e['evidence'][0]['grade'], src='%s:%s' % (reset_e['evidence'][0]['file'], reset_e['evidence'][0]['key']), tier='item', item_tier=it['tier'], imbue=it['imbue'])],
                orders=['ability -> item active -> ability (second cast same recipient)', 'ability -> item active -> ability (second recipient)', 'item active before the first cast (control: should waste the reset)'],
                why='The item resets the cooldown of the imbued ability (text) so the ability can be cast twice in a row; the ability has a long cooldown (%ss at T3) and a %ss effect on %s.' % (cd, dur, a['targeting']['side']),
                competing_outcomes=['second cast refreshes/extends the same effect (extra protection or sustain on one recipient)', 'second cast on another recipient (two recipients covered)', 'second cast rejected or wasted while the first effect is active', 'item cannot be activated at the needed moment (lockout / cooldown / cast constraint)'],
                distinguishing_test='; '.join(qs) + ' Read modifier names after each step and the time each modifier disappears.',
                availability=dict(tier_needed=3, ult=False, notes=anotes, once_per_fight=False, item_cycle_s=model['item_cycle_s']),
                premises=[ref(a, e) for e in protect_txt[:2]] + [dict(item=it['cls'], text=reset_e['evidence'][0].get('text'))],
                unknown_fields=['whether a second instance refreshes, stacks or is rejected', 'item cooldown formula after cooldown reduction', 'activation allowed while recipient locked out', 'ally targeting range/geometry for the second cast'],
                conditions=['item imbue rule: %s' % it['imbue']], timing=model,
                scoring=dict(impact=round(impact, 1), plausibility=round(plaus, 1), availability=av, testability=testability_of(needs)),
                sandbox=dict(needs={n: CAPS[n][0] for n in needs}, status='TESTABLE-NOW' if all(cap_ok(n) for n in needs) else 'PARTIAL-TESTABLE-NOW (self recipient only)' if cap_ok('cast_slot') and cap_ok('give_item') else 'UNTESTABLE-NOW',
                             missing=[dict(cap=n, state=CAPS[n][0], detail=CAPS[n][1]) for n in needs if not cap_ok(n)] + ([dict(cap='ally_bot', state='MISSING', detail='second-recipient branch needs two allies')] if ally else [])),
                alternatives=[dict(name='ordinary use of the ability', note='no item slot, no souls'), ] + [dict(name=r['item'], note='cooldown reduction %s%%: uptime gain %s vs item gain %s' % (r['cdr_pct'], r['uptime_gain'], model['uptime_gain']), model=r) for r in model['alternatives_same_ability'][:3]],
            )
            hy['scoring']['total'] = score(impact, plaus, av, hy['scoring']['testability']); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0)
            hy['ladder'] = mk_ladder(
                st('EVIDENCED' if reset_e['evidence'][0]['grade'] == 'TEXT' and not lock else 'PARTIAL', 'VERIFIED MECHANIC (text)' if not lock else 'VERIFIED MECHANIC (components) / HYPOTHESIS', 'item text says it resets the cooldown of the imbued ability%s' % ('; ability text says the recipient cannot act: can the item still be activated?' if lock else ''), ['activation while locked' if lock else 'duration refresh vs stack']),
                st('NOT-EVIDENCED', 'HYPOTHESIS', 'no sandbox result; ' + ('partially testable on self' if hy['sandbox']['status'].startswith('PARTIAL') else hy['sandbox']['status']), [m['cap'] for m in hy['sandbox']['missing']]),
                st('PARTIAL', 'MODELLED', 'cadence: item cycle %ss vs ability cooldown %ss (about %s extra casts per 180 s)' % (model['item_cycle_s'], model['ability_cd_s'], model['extra_casts']), ['reaction time to the item + second cast', 'recipient position for the second cast', 'recipient lockout']),
                st('MODELLED', 'MODELLED', 'uptime %s -> %s of a 180 s window (gain %s) vs same-souls alternatives in alternatives[]' % (model['uptime_base'], model['uptime_with_item'], model['uptime_gain']), ['whether extra uptime lands when someone is actually threatened']),
                st('NOT-EVIDENCED', 'HYPOTHESIS', 'requires stages 2-4; item tier %d (~%s souls secondary) + a slot' % (it['tier'], PRICE.get(it['tier'])), ['opportunity cost over the build']))
            out.append(hy)
    return out

# ---------------------------------------------------------------- T3: cleanse/dispel vs modifiers that cannot be purged (negative-prediction template)
def t3_cleanse_vs_unpurgeable(h, items):
    out = []
    ks = kit(h)
    flagged = [(a, e) for a in ks for e in a['effects'] if e['subtype'] == 'cannot_be_purged']
    cleans = [(a, e) for a in ks for e in a['effects'] if e['op'] == 'remove_cc' and e['evidence'][0]['grade'] != 'TEXT' and e['target'] in ('self', 'self_or_ally', 'ally')]
    for (B, Be) in flagged:
        for (A, Ae) in cleans:
            if A['cls'] != B['cls'] and not any(e['op'] in ('defer', 'delayed_cost') for e in B['effects']): continue
            tA = tier_of(Ae)
            impact = 2.0; plaus = 0.8; av, notes = availability_of([(A, tA)])
            needs = ['apply_cc_to_player', 'cast_slot']
            hy = dict(id='T3-' + hid(h['hero'], A['cls'], B['cls']), template='T3 cleanse vs unpurgeable own debuff', hero=h['hero'], hero_name=h['name'], scope='kit',
                title='%s: can %s cleanse the penalty modifier of %s?' % (h['name'], A['name'], B['name']),
                components=[ref(B, Be), ref(A, Ae)], orders=['cleanse while penalty active'],
                why='A cleanse effect exists in the kit and the penalty modifier is flagged CANNOT_BE_PURGED in data: the data predicts the cleanse does nothing. Kept as a negative-prediction check so the engine records rejected ideas.',
                competing_outcomes=['cleanse removes it (data flag wrong/irrelevant)', 'cleanse does nothing (data prediction)'],
                distinguishing_test='Apply the penalty modifier, cast the cleanse, read modifier names.', availability=dict(tier_needed=tA, ult=A['is_ult'], notes=notes, once_per_fight=False),
                premises=[ref(B, Be)], unknown_fields=['meaning of purge vs dispel in engine'], conditions=['DATA AGAINST'], timing={},
                scoring=dict(impact=impact, plausibility=plaus, availability=av, testability=testability_of(needs)),
                sandbox=dict(needs={n: CAPS[n][0] for n in needs}, status='UNTESTABLE-NOW', missing=[dict(cap=n, state=CAPS[n][0], detail=CAPS[n][1]) for n in needs if not cap_ok(n)]),
                alternatives=[dict(name='avoid the penalty by not using the deferring ability', note='')])
            hy['scoring']['total'] = score(impact, plaus, av, hy['scoring']['testability']); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0)
            hy['ladder'] = mk_ladder(st('NOT-EVIDENCED', 'VERIFIED MECHANIC (flag) predicts NO', 'game data flags the modifier as not purgeable (as named)', []),
                st('NOT-EVIDENCED', 'HYPOTHESIS', 'no test', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'n/a', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'n/a', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'n/a', []))
            out.append(hy)
    return out

# ---------------------------------------------------------------- T4: self-lockout of cast phases vs item actives (order constraint / conflict)
def t4_lockout_vs_items(h, items):
    out = []
    for a in kit(h):
        locks = [e for e in a['effects'] if e['subtype'] == 'items_disabled' and e['op'] == 'lockout_self']
        if not locks: continue
        # any item whose active could matter: tier>=3 actives
        act = [it for it in items.values() if it['active'] and not it['disabled'] and it['tier'] >= 3 and it['cooldown_s']]
        if not act: continue
        phases = sorted({c for e in locks for c in e['conditions']})
        chan = bytier(a['channel_time_by_tier'], 3)
        needs = ['cast_slot', 'cast_item_active', 'give_item', 'cooldown_readback']
        impact = 1.5 + (1.0 if a['is_ult'] else 0.3); plaus = 4.0; av, notes = availability_of([(a, 0)])
        hy = dict(id='T4-' + hid(h['hero'], a['cls']), template='T4 cast-phase lockout vs item actives (order constraint)', hero=h['hero'], hero_name=h['name'], scope='kit x item',
            title='%s: %s disables item actives (%s): item must be used before the cast' % (h['name'], a['name'], ', '.join(phases)),
            components=[ref(a, locks[0])], orders=['item active -> ability', 'ability -> item active (should be blocked)'],
            why='Cast-phase state mask contains ITEMS_DISABLED; every item active with a cooldown shorter than the lockout is unusable during it and must be fired before; items whose effect should overlap the channel must be pre-activated.',
            competing_outcomes=['item activation blocked during phase', 'item activation allowed (name misleading)', 'item effect already running continues through the phase'],
            distinguishing_test='Cast the ability, press the item active inside the phase, read item cooldown state and modifiers.',
            availability=dict(tier_needed=0, ult=a['is_ult'], notes=notes + ['phase length: channel %ss at T3' % chan], once_per_fight=a['is_ult']),
            premises=[ref(a, e) for e in locks[:2]], unknown_fields=['exact engine meaning of ITEMS_DISABLED', 'whether already-running item buffs persist'], conditions=[], timing=dict(channel_time_by_tier=a['channel_time_by_tier']),
            scoring=dict(impact=round(impact, 1), plausibility=plaus, availability=av, testability=testability_of(needs)),
            sandbox=dict(needs={n: CAPS[n][0] for n in needs}, status='TESTABLE-NOW' if all(cap_ok(n) for n in needs) else 'UNTESTABLE-NOW', missing=[dict(cap=n, state=CAPS[n][0], detail=CAPS[n][1]) for n in needs if not cap_ok(n)]),
            alternatives=[dict(name='fire actives before the ability', note='costs nothing')])
        hy['scoring']['total'] = score(impact, plaus, av, hy['scoring']['testability']); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0)
        hy['ladder'] = mk_ladder(st('EVIDENCED', 'VERIFIED MECHANIC (state name in data; semantics name-inferred)', 'phase mask lists ITEMS_DISABLED', ['engine semantics']), st('NOT-EVIDENCED', 'HYPOTHESIS', 'no test', []), st('NOT-EVIDENCED', 'MODELLED', 'ordering is trivial to execute if known', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'constraint, not a gain', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'n/a', []))
        out.append(hy)
    return out

# ---------------------------------------------------------------- T5: ability produces an event class that items consume (kit x item catalogue)
STACK_PROPS = ('MaxStacks', 'LightMeleeStacks', 'HeavyMeleeMultiplier', 'LightMeleeAmmo')
# structural words that carry no event meaning (they appear on almost every property); NOT hero/ability/item names
STEM_STOP = set('Damage Duration Bonus Percent Cooldown Range Radius Time Max Min Count Health Stack Stacks Speed Amount Value Base Resist Resistance Charges Charge Ability Cast Delay Scale Multiplier Power Spirit Weapon Rate Fire Move Movement Heal Healing Regen Lifesteal Bullet Bullets Incoming Outgoing Tech Per Second Seconds Threshold Required Fade Off On Enemy Ally Target Amp Reduction Increase Increased Reduced Extra Total Current Life Limit Initial Final Interval Tick Slow Stun Stamina Cost Resource Chance Level Number Buff Debuff Self Hero Heroes Npc Trooper Troopers Of Out In To The And'.split())
GENERIC_STEMS = set('Channel Between Post Unit Attack Combat Penalty Height Ground Armor Dash Barrier Parry Angle Length Taken Percentage Spread Mult Player While Window Aura Size Factor Impact Control Start Explosion Magic Sprint Status Receive Reveal Fading Restore Steal Velocity Activate Active Before Minimum Particle Randomness Reduce Shoot Shooting Stacking Success Targets Close Full Distance Accel Alert Beam Cancel Capture Caster Damping Degrees Enable Frequency Gravity Growth Meter Model Modifier Pct Pulse Reflected Respawn Shots Skip Frames Sound Think Visual Width Zoomed Float Lost Hit Non Others Invis Mod Lockout Tether Slide Split Spotted Evasion Model Others Target Immunity Heavy Light Build'.split())  # structural / non-event vocabulary; no hero, ability or item names
def _words(k):
    return re.findall(r'[A-Z][a-z]+|[A-Z]+(?![a-z])|\d+', k)
def prop_stems(k):
    """event-stem candidates of a property key: runs of 1-2 consecutive non-structural CamelCase words, as word tuples"""
    w = [x for x in _words(k) if x not in STEM_STOP and len(x) > 2]
    out = set()
    for n in (2, 1):
        for i in range(len(w) - n + 1):
            out.add(tuple(w[i:i + n]))
    return out
def derive_event_classes(H, I, max_abil=30, max_item=12):  # defaults tuned on the 6819 data: <=30 abilities / <=12 items per stem
    """EVENT CLASSES FROM DATA: a stem is an event class when some ability property and some item property share it (e.g. UseHeavyMelee / BonusHeavyMeleeDamage -> ('Heavy','Melee')).
    Specificity limits (<= max_abil abilities, <= max_item items, stem not structural) keep generic words out. No hero/ability/item name is used."""
    ab = collections.defaultdict(set); it = collections.defaultdict(set)
    for h in H.values():
        for a in kit(h):
            for k, p in a['props'].items():
                if any(p['by_tier']):
                    for st_ in prop_stems(k): ab[st_].add(a['cls'])
    for i in I.values():
        if i['disabled']: continue
        for k, p in i['props'].items():
            if p['by_tier'][0]:
                for st_ in prop_stems(k): it[st_].add(i['cls'])
    txtA = ' '.join(d['text'].lower() for h in H.values() for a in kit(h) for d in a['desc'].values())
    txtI = ' '.join(d['text'].lower() for i in I.values() for d in i['desc'].values())
    ev = []
    for st_ in ab:
        txt = ''.join(st_)
        if not all(w.lower()[:5] in txtA and w.lower()[:5] in txtI for w in st_): continue
        if st_ in it and len(txt) >= 5 and not (len(st_) == 1 and txt in GENERIC_STEMS) and 1 <= len(ab[st_]) <= max_abil and 1 <= len(it[st_]) <= max_item:
            ev.append(st_)
    # drop a one-word stem when a longer stem covers the same abilities and items (keeps the most specific name)
    keep = []
    for st_ in sorted(ev, key=lambda x: (-len(x), x)):
        if len(st_) == 1 and any(len(o) == 2 and st_[0] in o and ab[o] == ab[st_] and it[o] == it[st_] for o in ev): continue
        keep.append(st_)
    return sorted(keep)
def _event_name(st_):
    return '_'.join(w.lower() for w in st_)
NEG_WORDS = {'Block', 'Blocked', 'Disable', 'Disabled', 'Immune', 'Cannot', 'Prevent', 'Resist', 'Lost', 'Lose', 'Penalty', 'Reduce', 'Reduction', 'Ignore', 'Skip'}   # a property that blocks/loses/reduces an event is not a producer or consumer of it
def _has_stem(k, st_):
    return st_ in prop_stems(k) and not (set(_words(k)) & NEG_WORDS)
def _damage_types(a):
    return {d['damage_type'] for d in a.get('damage_split', []) if d['damage_type'] != 'UNCLASSIFIED'}
def t5_event_chain(h, items, events=None):
    out = []
    events = events if events is not None else derive_event_classes({h['hero']: h}, items)
    for a in kit(h):
        for st_ in events:
            ev = _event_name(st_)
            arx_t = re.compile(r'\s*'.join(re.escape(w) for w in st_), re.I)
            sprops = [(n, p) for n, p in a['props'].items() if _has_stem(n, st_) and any(p['by_tier']) and re.match(r'(Use|Damage|Enable|Can|Deal)', n)]   # producer = a damage/use/enable property; force/resource/cost properties are not producers
            tdesc = [(k, d) for k, d in a['desc'].items() if arx_t.search(d['text'])]
            if not sprops and not tdesc: continue
            tier = min([next(i for i, v in enumerate(p['by_tier']) if v) for n, p in sprops] + [d['tier'] for k, d in tdesc])
            structured = bool(sprops)
            cons = {}
            for it in items.values():
                if it['disabled']: continue
                hits = [(n, p) for n, p in it['props'].items() if _has_stem(n, st_) and p['by_tier'][0]]
                if hits: cons[it['cls']] = (it, hits)
            ranked = sorted(cons.values(), key=lambda x: (0 if any(n in STACK_PROPS or n.endswith('Multiplier') for n, _ in x[1]) else 1, x[0]['tier']))
            for it, hits in ranked[:4]:
                trigger = any(n in STACK_PROPS or n.endswith('Multiplier') or 'Stack' in n for n, _ in hits)
                n0, p0 = hits[0]
                ev_src = ('abilities.vdata:m_mapAbilityProperties.%s' % sprops[0][0], sprops[0][1]['by_tier'], 'STRUCTURED') if structured else ('localization:%s' % tdesc[0][0], arx_t.search(tdesc[0][1]['text']).group(0), 'TEXT')
                impact = 2.0 + (1.2 if trigger else 0.0) + (0.5 if bytier(a['cooldown_by_tier'], 3) and bytier(a['cooldown_by_tier'], 3) < 30 else 0.0)
                plaus = 2.5 + (1.0 if structured else 0.0)
                ptypes = set((it.get('proc_semantics') or {}).get('proc_damage_types') or [])
                atypes = _damage_types(a); tmatch = None
                if ptypes and atypes:
                    tmatch = bool(ptypes & atypes)
                    plaus += 0.8 if tmatch else -1.2
                elif ptypes and not atypes:
                    plaus -= 0.8   # the item reacts to typed damage but the ability has no typed damage instance in its properties   # item reacts to damage types (proc_damage_types, FACT); ability deals these types (damage_split, STRUCTURED)
                av, notes = availability_of([(a, tier)], [it]); needs = ['cast_slot', 'give_item', 'damage_csv'] + (['melee_attack'] if 'melee' in ev else [])
                model = {}
                if trigger and 'MaxStacks' in it['props']:
                    mx = it['props']['MaxStacks']['by_tier'][0]; per_heavy = (it['props'].get('HeavyMeleeMultiplier', {'by_tier': [1]})['by_tier'][0]) * (it['props'].get('LightMeleeStacks', {'by_tier': [1]})['by_tier'][0])
                    ch = bytier(a['charges_by_tier'], tier) or 1; cd = bytier(a['cooldown_by_tier'], tier)
                    model = dict(max_stacks=mx, stacks_per_event=per_heavy, events_to_cap=-(-mx // per_heavy), ability_charges=ch, ability_cooldown_s=cd,
                                 stacks_from_one_ability_cycle=ch * per_heavy, label='MODELLED: assumes each ability-delivered event counts like a manual one and hits one target (the question under test)')
                hy = dict(id='T5-' + hid(h['hero'], a['cls'], it['cls'], ev), template='T5 ability produces an event an item consumes', event=ev, ability_cls=a['cls'], item_cls=it['cls'], damage_type_match=tmatch, ability_damage_types=sorted(atypes), item_proc_types=sorted(ptypes), hero=h['hero'], hero_name=h['name'], scope='kit x item',
                    title='%s: does %s (%s) count for %s (%s)?' % (h['name'], a['name'], ev, it['name'], n0),
                    components=[dict(ability=a['cls'], name=a['name'], effect='event', src=ev_src[0], value=ev_src[1], grade=ev_src[2], tier=tier, op='emit_event', subtype=ev),
                                dict(item=it['cls'], name=it['name'], effect=n0, op='consume_event', subtype='trigger' if trigger else 'stat_bonus', src='abilities.vdata:m_mapAbilityProperties.%s' % n0, value=p0['by_tier'][0], grade='NAME-INFERRED', tier='item', item_tier=it['tier'])],
                    orders=['ability hit then item effect check', 'manual event then ability hit (stack ordering)'],
                    why='%s data marks the ability as delivering %s from T%d (%s); the item has a property keyed to that event class (%s%s). Whether an ability-delivered event counts as the event for the item is not in the data.' % ('Structured' if structured else 'Text-only', ev, tier, ev_src[0].split(':')[-1], n0, ', stack/trigger type' if trigger else ', stat bonus'),
                    competing_outcomes=['item effect fires/stacks on the ability hit', 'only on the player\'s own melee input', 'fires but excludes the ability\'s damage', 'applies to every target hit (multi-target stacks) or the first only'],
                    distinguishing_test='Compare the item effect (extra damage / stacks / ammo / stun) after the ability hit vs after a manual event, at 3 distances, arms interleaved; control = manual event with the item proves the item works.',
                    availability=dict(tier_needed=tier, ult=a['is_ult'], notes=notes, once_per_fight=False), premises=[], unknown_fields=['whether ability-delivered %s triggers the item' % ev, 'multi-target stacking'], conditions=[], timing=model,
                    scoring=dict(impact=round(impact, 1), plausibility=round(plaus, 1), availability=av, testability=testability_of(needs)),
                    sandbox=dict(needs={q: CAPS[q][0] for q in needs}, status='TESTABLE-NOW' if all(cap_ok(q) for q in needs) else 'UNTESTABLE-NOW', missing=[dict(cap=q, state=CAPS[q][0], detail=CAPS[q][1]) for q in needs if not cap_ok(q)]),
                    alternatives=[dict(name='manual event with the same item', note='no ability cooldown spent; the ability still does its own damage')])
                hy['scoring']['total'] = score(impact, plaus, av, hy['scoring']['testability']); hy['scoring']['priority_if_testable'] = score(impact, plaus, av, 5.0)
                hy['ladder'] = mk_ladder(st('PARTIAL', 'VERIFIED MECHANIC (components) / HYPOTHESIS (link)', 'ability emits the event class (%s) and item consumes it; link unknown' % ev_src[2], ['trigger rule']), st('NOT-EVIDENCED', 'HYPOTHESIS', 'no sandbox result', []),
                    st('PARTIAL' if model else 'NOT-EVIDENCED', 'MODELLED' if model else 'HYPOTHESIS', ('cadence: %d event(s) per ability cycle of %ss vs %d needed to cap' % (model['ability_charges'], model['ability_cooldown_s'], model['events_to_cap'])) if model else 'n/a', ['melee range/positioning', 'parry/dodge by enemy']),
                    st('NOT-EVIDENCED', 'HYPOTHESIS', 'depends on stage 2', []), st('NOT-EVIDENCED', 'HYPOTHESIS', 'requires stages 2-4', ['opportunity cost']))
                out.append(hy)
    return out

def verdict(h):
    t = h['template'][:2]
    if t == 'T3': return 'REJECTED BY DATA: the penalty modifier is flagged not purgeable, so the cleanse is predicted to do nothing (VERIFIED MECHANIC flag; engine rule not in data). Not worth a test slot.'
    if t == 'T4': return 'CONSTRAINT, not a gain: item actives must be fired before the cast; cheap to test, no build change implied.'
    if t == 'T1': return 'INSUFFICIENT EVIDENCE. Cannot be tested with the current sandbox (%s). Data points both ways; stages 2-5 of the ladder are not evidenced; no build change is supportable.' % ', '.join(m['cap'] for m in h['sandbox']['missing'])
    if t == 'T2':
        m = h['timing']; mine = m.get('item_uptime_gain_per_1000_souls'); alts = [r for r in m.get('alternatives_same_ability', []) if isinstance(r.get('uptime_gain_per_1000_souls'), (int, float))]
        best = max(alts, key=lambda r: r['uptime_gain_per_1000_souls']) if alts else None
        if mine is not None and best and best['uptime_gain_per_1000_souls'] > mine:
            return 'MODELLED (upper bound): on average uptime per 1000 souls the item (%.4f) is beaten by %s (%.4f, %s). The only thing a cooldown-reduction item cannot give is TWO casts within seconds (burst/rescue coverage); that is stage 3-4 and is not evidenced. Test the mechanic first; do not change a build on this.' % (mine, best['item'], best['uptime_gain_per_1000_souls'], best['applies_to'])
        return 'MODELLED (upper bound): item uptime per 1000 souls is competitive with the cooldown-reduction alternatives; still unevidenced beyond stage 1.'
    if t == 'T5': return 'TEST FIRST: cheap and testable now; if it works the ability becomes a delivery mechanism for the item effect (value then needs stage 3-4 modelling).'
    return 'HYPOTHESIS'

def reliability(h):
    t = h['template'][:2]; tm = h['timing'] or {}
    need = {'T1': ['activation success count vs late/early offsets (-3..+8 s around the buff end), N per offset', 'stun/interrupt exposure during the protection window (counts per fight from real enemy comps)', 'damage taken per tick with and without the protector under real incoming damage', 'cast-delay coverage (is damage immune during the cast delay?)'],
            'T2': ['rate at which the item press is accepted vs press delay (0/0.6/1.2 s)', 'second-cast acceptance (refresh/stack/reject) over N trials', 'recipient positioning success for the second cast on a different ally (needs allied bot)', 'how often a rescue needs two casts inside the same few seconds (from play data)'],
            'T4': ['accept/reject count of item press during the phase, N trials'],
            'T5': ['trigger count per ability cast at 100/150/250 u, N trials; multi-target behaviour'], 'T3': []}.get(t, [])
    best = None
    if t == 'T1' and 'full_coverage_start_tolerance_s' in tm:
        best = 'MODELLED best case: protector start may be up to %ss (full coverage) / %ss (single-hit) wide; assumes no interrupt and protection from channel start' % (tm['full_coverage_start_tolerance_s'], tm['instant_application_start_tolerance_s'])
    return dict(best_case=best or 'not computed', practical='UNKNOWN: no trial counts exist; no success probability is stated or implied', measurements_needed=need, rule='report counts per condition; a strategy that keeps partial value after a late/missed step beats one that needs every input perfect')

TEMPLATES = ['t1', 't2', 't3', 't4', 't5']
def finalize(allh, H):
    for x in allh:
        x['verdict'] = verdict(x); x['reliability'] = reliability(x)
        if x['template'].startswith('T2'):
            a = None
            for h in H.values():
                a = a or next((k for k in h['abilities'] if k['cls'] == x['components'][0].get('ability')), None)
            ops = {e['op'] for e in (a or {}).get('effects', []) if e['target'] != 'unknown'}
            sust = ops & {'heal', 'absorb', 'grant', 'remove_cc', 'apply_cc', 'displace', 'amplify'}
            x['generic'] = not sust
            if x['generic']:
                x['scoring']['total'] = round(x['scoring']['total'] - 0.8, 2); x['scoring']['generic_penalty'] = 0.8
                x['verdict'] += ' [GENERIC: ability has no protective, sustain, control or amplify effect; a repeat cast is only more of the same output, so it is ranked below]'
    allh.sort(key=lambda x: (-x['scoring']['total'], x['id']))
    return allh

def user_reported():
    fn = os.path.join(EVD, 'validated', 'user_example_patterns.json')
    return json.load(open(fn))['entries'] if os.path.exists(fn) else []

def measured_entries():
    fn = os.path.join(EVD, 'validated', 'measured.json')
    return json.load(open(fn)).get('measured', []) if os.path.exists(fn) else []

USER_PENALTY = 1.0      # a question the user already raised adds less to what he knows (flag + fixed penalty, same for every entry)
ITEM_CAP = 10           # at most this many hypotheses per item class stay in the ranked list; the rest go to `overflow`
EVENT_CAP = 12          # and at most this many per event class (T5), so one relation class cannot fill the list
# measured-result re-rank rule (explicit, applied only to T5 siblings of a measured link)
BOOST = dict(same_item_other_ability_type_match=0.6, same_ability_other_item=0.3, reject_same_item=-1.5, reject_same_ability=-1.0)

def flag_user_examples(allh, entries):
    for x in allh:
        x['user_example_derived'] = False
        for e in entries:
            if e.get('template') and not x['template'].startswith(e['template']): continue
            if e.get('item') and (x.get('item_cls') or (x['components'][1].get('item') if len(x['components']) > 1 else None)) != e['item'] and not (e.get('item') and any(c.get('item') == e['item'] for c in x['components'])): continue
            if e.get('event') and x.get('event') != e['event']: continue
            if e.get('hero') and x['hero'] != e['hero']: continue
            x['user_example_derived'] = True; x['user_example_note'] = e.get('note', '')
            x['scoring']['user_example_penalty'] = USER_PENALTY; x['scoring']['total'] = round(x['scoring']['total'] - USER_PENALTY, 2)
            break

def apply_measured(allh, measured):
    """LEARNING LOOP. A measured entry carries `links` [{template, hero, ability, item, event, outcome: confirmed|rejected, stage}].
    1. the matching hypothesis: ladder stage 2 becomes EVIDENCED (tier CONTROLLED SANDBOX RESULT), status MEASURED, run priority 0 (answered; its score is kept as score_before).
    2. confirmed: same item + same event on another ability whose damage types match the item's proc types -> +0.6; other items with the same event on the SAME ability -> +0.3.
       rejected: same item + event elsewhere -> -1.5; same ability other item -> -1.0.  Never touches other templates."""
    log = []
    for m in measured:
        for ln in m.get('links', []):
            if ln.get('template') != 'T5': continue
            hit = [x for x in allh if x['template'].startswith('T5') and x.get('ability_cls') == ln['ability'] and x.get('item_cls') == ln['item'] and x['hero'] == ln['hero']]
            conf = ln['outcome'] == 'confirmed'
            for x in hit:
                x['measured'] = dict(id=m['id'], outcome=ln['outcome'], tier=m['tier'], fact=m['fact'][:200])
                x['scoring']['score_before_measured'] = x['scoring']['total']; x['scoring']['total'] = 0.0
                x['sandbox']['status'] = 'MEASURED (%s)' % ln['outcome']
                L = x['ladder']['stages'][1]; L.update(status='EVIDENCED' if conf else 'REFUTED', evidence_tier='CONTROLLED SANDBOX RESULT', why=m['fact'][:160], stage_unknowns=[])
                x['ladder'] = dict(stages=x['ladder']['stages'], cap=x['ladder']['cap'], measured_stage=2 if conf else None, cap_text=('stage 2 works reliably in controlled tests: MEASURED (%s); stage 1 link stays PARTIAL (components)' % m['id']) if conf else 'stage 2 REFUTED by measurement (%s)' % m['id'])
                x['verdict'] = 'MEASURED (%s): %s' % (ln['outcome'].upper(), m['fact'][:180])
                log.append((m['id'], x['id'], 'measured'))
            for x in allh:
                if not x['template'].startswith('T5') or x in hit or x.get('measured'): continue
                same_item = x.get('item_cls') == ln['item'] and x.get('event') == ln['event'] and x.get('ability_cls') != ln['ability']
                same_abil = x.get('ability_cls') == ln['ability'] and x.get('item_cls') != ln['item'] and x.get('event') == ln['event']
                d = 0.0; why = None
                if same_item and conf and x.get('damage_type_match') is not False: d, why = BOOST['same_item_other_ability_type_match'], 'sibling: %s confirmed on %s' % (ln['item'], ln['ability'])
                elif same_item and not conf: d, why = BOOST['reject_same_item'], 'sibling: %s rejected on %s' % (ln['item'], ln['ability'])
                elif same_abil and conf: d, why = BOOST['same_ability_other_item'], 'ability %s confirmed to deliver %s' % (ln['ability'], ln['event'])
                elif same_abil and not conf: d, why = BOOST['reject_same_ability'], 'ability %s rejected as a %s source' % (ln['ability'], ln['event'])
                if d:
                    x['scoring']['measured_adjust'] = round(x['scoring'].get('measured_adjust', 0) + d, 2); x['scoring']['measured_adjust_why'] = why
                    x['scoring']['total'] = round(x['scoring']['total'] + d, 2); log.append((m['id'], x['id'], '%+.1f %s' % (d, why)))
    return log

def cap_per_item(allh, cap=ITEM_CAP):
    keep, over, cnt, ecnt = [], [], collections.Counter(), collections.Counter()
    for x in allh:   # allh already sorted by score
        k = x.get('item_cls') or next((c.get('item') for c in x['components'] if c.get('item')), None)
        e = x.get('event')
        if not x.get('measured'):
            if k and cnt[k] >= cap:
                x['overflow_reason'] = 'item %s already has %d hypotheses in the list' % (k, cap); over.append(x); continue
            if e and ecnt[e] >= EVENT_CAP:
                x['overflow_reason'] = 'event class %s already has %d hypotheses in the list' % (e, EVENT_CAP); over.append(x); continue
        cnt[k] += 1
        if e: ecnt[e] += 1
        keep.append(x)
    return keep, over

def generate(hero_filter=None, use_measured=True, apply_flags=True):
    D, H, I = load_effects()
    allh = run_on(H, I, hero_filter)
    generate.events = derive_event_classes(H, I)
    LOG = []
    if apply_flags:
        flag_user_examples(allh, user_reported())
    if use_measured:
        LOG = apply_measured(allh, measured_entries())
    allh.sort(key=lambda x: (-x['scoring']['total'], x['id']))
    allh, over = cap_per_item(allh) if apply_flags else (allh, [])
    generate.overflow = over; generate.log = LOG
    return D, H, I, allh

# ---------------------------------------------------------------- outputs
def write_outputs(hy, D, outdir=None):
    outdir = outdir or EVD
    hd = os.path.join(outdir, 'hypotheses'); vd = os.path.join(outdir, 'validated')
    os.makedirs(hd, exist_ok=True); os.makedirs(vd, exist_ok=True)
    ov = getattr(generate, 'overflow', [])
    meta = dict(format_version=2, source_sha=D['sha'], count=len(hy), tier_note='HYPOTHESIS unless a premise says VERIFIED MECHANIC or the entry carries `measured` (CONTROLLED SANDBOX RESULT from validated/measured.json)',
                user_example_derived=sum(1 for x in hy if x.get('user_example_derived')), measured=sum(1 for x in hy if x.get('measured')), item_cap=ITEM_CAP,
                overflow_count=len(ov), overflow_by_template=dict(collections.Counter(x['template'][:2] for x in ov)), overflow_ids=[x['id'] for x in ov],
                measured_log=[list(t) for t in getattr(generate, 'log', [])], event_classes_derived=[' '.join(e) for e in getattr(generate, 'events', [])])
    json.dump(dict(meta=meta, hypotheses=hy), open(os.path.join(hd, 'ranked.json'), 'w'), indent=1)
    with open(os.path.join(hd, 'ranked.txt'), 'w') as f:
        f.write('# RANKED HYPOTHESES (generated; HYPOTHESIS tier unless stated)  source_sha=%s  n=%d\n# priority = 0.35 impact + 0.2 information value + 0.1 plausibility + 0.15 availability + 0.2 testability (0..5 each)\n' % (D['sha'], len(hy)))
        for i, x in enumerate(hy, 1):
            s = x['scoring']
            f.write('%3d. [%s] %s\n     score=%s (impact %s, plaus %s, avail %s, test %s; priority-if-testable %s)  sandbox=%s\n     ladder: %s | %s\n     verdict: %s\n' % (i, x['id'] + (' [USER-EXAMPLE]' if x.get('user_example_derived') else '') + (' [MEASURED]' if x.get('measured') else ''), x['title'], s['total'], s['impact'], s['plausibility'], s['availability'], s['testability'], s['priority_if_testable'], x['sandbox']['status'], x['ladder']['cap_text'], ' / '.join('%s:%s' % (q['stage'][0], q['status']) for q in x['ladder']['stages']), x['verdict']))
    facts = {}
    for x in hy:
        for p in x['premises'] + x['components']:
            if p.get('grade') in ('STRUCTURED', 'NAME-INFERRED') and p.get('src'):
                facts[p['src'] + '|' + str(p.get('value'))] = dict(fact=p.get('name') or p.get('item'), src=p['src'], value=p.get('value'), grade=p['grade'], tier=p.get('tier'), claim='VERIFIED MECHANIC: the data field has this value (engine semantics of the field are as named, not verified)')
    json.dump(dict(meta=dict(note='data facts only (VERIFIED MECHANIC = present in game files). No MEASURED entries: sandbox has produced none for these hypotheses.'), facts=sorted(facts.values(), key=lambda f: f['src'])), open(os.path.join(vd, 'mechanics_verified.json'), 'w'), indent=1)

def cmd_run(args):
    hero = None; top = 40
    if '--hero' in args: hero = args[args.index('--hero') + 1]
    if '--top' in args: top = int(args[args.index('--top') + 1])
    D, H, I, hy = generate(hero)
    write_outputs(hy, D)
    c = collections.Counter(x['template'] for x in hy)
    print('heroes', len(H), 'items', len(I), 'hypotheses', len(hy), dict(c))
    for i, x in enumerate(hy[:top], 1):
        s = x['scoring']
        print('%3d. [%s] %-8s %s | score %s i%s p%s a%s t%s | %s | cap %s' % (i, x['id'], x['hero_name'], x['title'][:110], s['total'], s['impact'], s['plausibility'], s['availability'], s['testability'], x['sandbox']['status'], x['ladder']['cap']))

def cmd_rerank_diff(args):
    """ranking with vs without validated/measured.json (user-example flags and item cap applied to both, so the difference is driven ONLY by the measured results)."""
    top = int(args[args.index('--top') + 1]) if '--top' in args else 15
    _, _, _, b = generate(use_measured=False); _, _, _, a = generate(use_measured=True); log = generate.log
    rb = {x['id']: i for i, x in enumerate(b, 1)}; ra = {x['id']: i for i, x in enumerate(a, 1)}
    out = ['RE-RANK DIFF driven only by validated/measured.json (%d measured entries, %d with links)' % (len(measured_entries()), sum(1 for m in measured_entries() if m.get('links'))), 'rule: see apply_measured(); BOOST=%s' % BOOST, '']
    out.append('measured log:'); out += ['  %s -> %s : %s' % t for t in log] or ['  (none)']
    out.append(''); out.append('moved hypotheses (id | rank before -> after | score before -> after | title):')
    moved = [x for x in a if rb.get(x['id']) != ra[x['id']]]
    sb = {x['id']: x['scoring']['total'] for x in b}
    for x in sorted(moved, key=lambda x: ra[x['id']])[:40]:
        out.append('  %s | %s -> %d | %s -> %s | %s' % (x['id'], rb.get(x['id']), ra[x['id']], sb.get(x['id']), x['scoring']['total'], x['title'][:90]))
    out.append(''); out.append('top %d BEFORE:' % top); out += ['  %2d %s %s' % (i, x['id'], x['title'][:100]) for i, x in enumerate(b[:top], 1)]
    out.append('top %d AFTER:' % top); out += ['  %2d %s %s%s' % (i, x['id'], x['title'][:100], '  [MEASURED]' if x.get('measured') else '') for i, x in enumerate(a[:top], 1)]
    txt = '\n'.join(out); print(txt)
    open(os.path.join(EVD, 'hypotheses', 'rerank_diff.txt'), 'w').write(txt + '\n')

def cmd_show(args):
    D, H, I, hy = generate()
    for x in hy:
        if x['id'] == args[0]:
            print(json.dumps(x, indent=1)); return
    print('not found')

def cmd_extract(args):
    H, I = X.write_all(os.path.join(EVD, 'effects')); print('wrote effects', len(H), len(I))

def pick_scenarios(hy, S, top=4, per_template=2):
    """diverse selection of runnable (not UNTESTABLE-NOW) hypotheses: at most per_template per template, one per hero, hero must have a build id."""
    chosen, cnt, heroes = [], collections.Counter(), set()
    for x in hy:
        t = x['template'][:2]
        if t not in S.PLANS or x['sandbox']['status'] == 'UNTESTABLE-NOW': continue
        if cnt[t] >= per_template or (x['hero'], t) in heroes or not S.build_for(x['hero']): continue
        chosen.append(x); cnt[t] += 1; heroes.add((x['hero'], t))
        if len(chosen) >= top: break
    return chosen

def cmd_scenarios(args):
    import interaction_scenarios as S, subprocess
    top = int(args[args.index('--top') + 1]) if '--top' in args else 4
    ids = [args[i + 1] for i, a in enumerate(args) if a == '--id']
    D, H, I, hy = generate()
    write_outputs(hy, D)
    hyp_file = 'council/evidence/interactions/hypotheses/ranked.json'
    os.makedirs(SCEN_DIR, exist_ok=True)
    chosen = [x for x in hy if x['id'] in ids] if ids else pick_scenarios(hy, S, top)
    written = []
    for x in chosen:
        sid, lines = S.PLANS[x['template'][:2]](x, I, H, hyp_file)
        fn = os.path.join(SCEN_DIR, 'int_disc_%s.txt' % x['id'].replace('-', '_'))
        open(fn, 'w').write('\n'.join(lines) + '\n'); written.append((x, fn))
    specs = []
    sd = os.path.join(EVD, 'hypotheses', 'specs'); os.makedirs(sd, exist_ok=True)
    for x in hy:
        if x['template'].startswith('T1'):
            sid, lines = S.plan_t1_spec(x, I, H, hyp_file)
            fn = os.path.join(sd, 'spec_%s.txt' % x['id'].replace('-', '_')); open(fn, 'w').write('\n'.join(lines) + '\n'); specs.append(fn)
    lint = subprocess.run([sys.executable, '-I', os.path.join(COUNCIL, 'tools', 'lint_meta.py')] + [f for _, f in written] + specs, capture_output=True, text=True)
    print(lint.stdout.strip())
    print('RUNNABLE (queue-ready, not pushed):')
    for x, fn in written:
        print('  node council/tools/queue.js add %s interaction:disc_%s %s' % (S.build_for(x['hero']), x['id'], os.path.relpath(fn, os.path.dirname(COUNCIL))))
    print('SPEC ONLY (UNTESTABLE-NOW, not queueable):', *specs, sep='\n  ')
    return lint.returncode

def relabel(H, I):
    """replace every hero/ability/item key and display name by opaque tokens (names inside localisation text are left: the generator reads text patterns, never names)."""
    import copy
    H2, I2 = copy.deepcopy(H), copy.deepcopy(I)
    mp = {}
    n = 0
    for hk, h in H2.items():
        for a in h['abilities']:
            n += 1; mp[a['cls']] = 'ZA%03d' % n
    for ik in I2: n += 1; mp[ik] = 'ZI%03d' % n
    hm = {hk: 'zh%02d' % i for i, hk in enumerate(H2)}
    def sub(o):
        if isinstance(o, dict): return {sub(k) if isinstance(k, str) else k: sub(v) for k, v in o.items()}
        if isinstance(o, list): return [sub(x) for x in o]
        if isinstance(o, str):
            return mp.get(o) or hm.get(o) or o
        return o
    H3 = {}
    for hk, h in H2.items():
        h = sub(h); h['name'] = hm[hk]
        for a in h['abilities']: a['name'] = a['cls']
        H3[hm[hk]] = h
    I3 = {}
    for ik, it in I2.items():
        it = sub(it); it['name'] = it['cls']; I3[mp[ik]] = it
    return H3, I3

def run_on(H, I, hero_filter=None):
    alts = cdr_alternatives(I); out = []; events = derive_event_classes(H, I)
    for hk, h in H.items():
        if hero_filter and hk != hero_filter: continue
        out += t1_protect_vs_cost(h, I) + t2_reset_items(h, I, alts) + t3_cleanse_vs_unpurgeable(h, I) + t4_lockout_vs_items(h, I) + t5_event_chain(h, I, events)
    return finalize(out, H)

def cmd_selfcheck(args):
    import provenance as P
    D, H, I, hy = generate(use_measured=False, apply_flags=False)
    ok = bad = 0; fails = []
    for x in hy:
        for c in x['components'] + x['premises']:
            src = c.get('src'); cls = c.get('ability') or c.get('item')
            if not src or not cls: continue
            r, why = P.check(cls, src, c.get('value'))
            if r: ok += 1
            else: bad += 1; fails.append((x['id'], cls, src, why))
    print('provenance: %d citations verified against raw files, %d failed' % (ok, bad)); [print('  FAIL', f) for f in fails[:10]]
    H2, I2 = relabel(H, I)
    base = sorted((x['template'][:2], x['scoring']['total'], x['scoring']['impact'], x['sandbox']['status']) for x in hy)
    rel = sorted((x['template'][:2], x['scoring']['total'], x['scoring']['impact'], x['sandbox']['status']) for x in run_on(H2, I2))
    print('relabel invariance (all hero/ability/item names and keys replaced by opaque tokens): %s (%d vs %d hypotheses)' % ('IDENTICAL ranking inputs' if base == rel else 'DIFFERENT', len(base), len(rel)))
    if base != rel:
        a, b = collections.Counter(base), collections.Counter(rel); print('  only in original:', list((a - b).items())[:5]); print('  only in relabelled:', list((b - a).items())[:5])
    return 0 if (bad == 0 and base == rel) else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    {'extract': cmd_extract, 'run': cmd_run, 'show': cmd_show, 'scenarios': cmd_scenarios, 'selfcheck': cmd_selfcheck, 'rerank-diff': cmd_rerank_diff}.get(a[0], lambda x: print(__doc__))(a[1:])


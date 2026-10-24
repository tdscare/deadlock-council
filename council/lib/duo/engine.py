"""Candidate generation -> value model -> pre-registered conclusion -> classification -> ranking.
Pre-registered bars (ASSUMED, set before looking at results, reported): a coordination must raise the kill probability of a won engagement
(p_kill = min(1, T_ESC/ttk), Council model) by >= BAR_OPP (opportunistic use) or >= BAR_DED (dedicated strategy) on >= SHARE of the parameter grid."""
import os, sys, itertools, statistics, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit as K, rules as R, synergy as S, econ, shred

BAR_OPP, BAR_DED, SHARE_OPP, SHARE_DED = 0.08, 0.20, 0.50, 0.75   # bars are RELATIVE increases in kill probability per won engagement ('+8% more kills'); ASSUMED
GRID = dict(T_ESC=(3.0, 5.0, 8.0), enemy=(0.6, 1.0, 1.6))
H_LIST = (0.3, 0.5, 0.7)

_cm = {}
def CM(bid):
    if bid not in _cm: _cm[bid] = econ.CarryModel(bid)
    return _cm[bid]

def builds_of(hk):
    return [b for b in econ.builds().values() if b['hk'] == hk]

def grid_cells(carry_hk, fn):
    """run fn(cm, P) over every baseline build of the carry hero x parameter grid; returns list of dp cells (dicts) and the builds used"""
    cells = []; used = []
    for b in builds_of(carry_hk):
        try: cm = CM(b['id'])
        except Exception as ex: continue
        used.append(b['id'])
        for te, en in itertools.product(GRID['T_ESC'], GRID['enemy']):
            P = econ.P_default(dict(T_ESC=te, enemy=en))
            for r in fn(cm, P):
                if 'dp' in r: r = dict(r, build=b['id'], T_ESC=te, enemy=en); cells.append(r)
    return cells, used

def stats(cells):
    if not cells: return None
    dps = sorted(c['dp'] / max(c.get('p_ind', 0.3), 0.05) for c in cells)
    n = len(dps)
    return dict(n=n, median=dps[n // 2], p10=dps[int(n * 0.1)], p90=dps[min(n - 1, int(n * 0.9))], share_opp=sum(1 for d in dps if d >= BAR_OPP) / n, share_ded=sum(1 for d in dps if d >= BAR_DED) / n, max=dps[-1])

def conclude(st, speculative, unknown_critical):
    """pre-registered rule (written before results)"""
    if st is None: return 'INSUFFICIENT'
    if st['share_ded'] >= SHARE_DED and not unknown_critical: return 'MEETS DEDICATED BAR (modelled)'
    if st['share_ded'] >= SHARE_DED: return 'MEETS DEDICATED BAR ONLY IF UNKNOWNS RESOLVE'
    if st['share_opp'] >= SHARE_OPP: return 'MEETS OPPORTUNISTIC BAR'
    if st['share_opp'] > 0: return 'DEPENDS ON ASSUMPTION'
    return 'BELOW BAR ON EVERY CELL'

def pair_id(r): return '%s>%s|%s|%s' % (r['carry'], r['partner'], r['rule'], r['need']['aname'])

def ability_candidates(rows, kits):
    """one candidate per (carry, partner, rule, need): evaluated rows only for HOLD/ZONE; all others get an UPPER-BOUND prune"""
    C = []
    for r in rows:
        if r['q'] <= 0: continue
        if not builds_of(r['carry']): continue
        m = r['match']; n = r['need']; o = m['offer']
        cand = dict(id=pair_id(r), kind='ABILITY', rule=r['rule'], carry=r['carry'], partner=r['partner'], cname=kits[r['carry']].name, pname=kits[r['partner']].name,
                    need=n, offer=o, match=m, q=r['q'], rank=r['rank'], n_equiv=r['n_equiv'], n_valid=r['n_valid'], cls0=r['cls0'], unknown=m['unknown'], mech=m['mech'], checks=m['checks'])
        C.append(cand)
    return C

def evaluate_candidate(c, row_lookup):
    r = row_lookup[c['id']]
    spec = r['speculative']
    if c['rule'] == 'HOLD' and not spec:
        cells, used = grid_cells(c['carry'], lambda cm, P: econ.evaluate(cm, r, P) or [])
        c['value_kind'] = 'MODELLED (Council trade model; h, T_ESC, enemy swept)'
    elif c['rule'] == 'ZONE' and not spec:
        cells, used = grid_cells(c['carry'], lambda cm, P: econ.evaluate(cm, r, P) or [])
        c['value_kind'] = 'MODELLED (Council trade model; h, T_ESC, enemy swept)'
    else:
        need = dict(c['need'])
        cells, used = grid_cells(c['carry'], lambda cm, P: econ.eval_ub(cm, need, P))
        c['value_kind'] = 'UPPER BOUND if the unproven mechanic works perfectly (used to prune)'
    c['cells'] = len(cells); c['builds'] = used
    c['stats'] = stats(cells)
    return c

def classify(c):
    st = c['stats']
    spec = c['cls0'] == 'UNPROVEN IDEA' or c['value_kind'].startswith('UPPER')
    crit = any(('unknown' in u.lower() or 'not in data' in u.lower()) for u in c['unknown'])
    c['conclusion'] = conclude(st, spec, crit and c['value_kind'].startswith('UPPER'))
    reasons = []
    if c['cls0'] == 'ORDINARY COMPATIBILITY':
        c['classification'] = 'ORDINARY COMPATIBILITY'
        reasons.append('substitutable: %d of %d partners score within 70%% of the best on the same contribution' % (c['n_equiv'], c['n_valid']))
    elif st is None:
        c['classification'] = 'UNPROVEN IDEA'; reasons.append('value not computable from data')
    elif c['value_kind'].startswith('UPPER'):
        if st['share_opp'] == 0 or st['median'] < BAR_OPP:
            c['classification'] = 'REJECTED'; reasons.append('even the perfect-execution upper bound is below the opportunistic bar (median relative dp_ub %.3f < %.2f)' % (st['median'], BAR_OPP))
        else:
            c['classification'] = 'UNPROVEN IDEA'; reasons.append('upper bound clears the bar (median dp_ub %.3f) but the key mechanic is not in data: %s' % (st['median'], '; '.join(c['unknown'][:2])))
    else:
        if st['share_ded'] >= SHARE_DED: c['classification'] = 'DEDICATED DUO STRATEGY (candidate)'
        elif st['share_opp'] >= SHARE_OPP: c['classification'] = 'GENUINE MECHANICAL SYNERGY'
        else:
            c['classification'] = 'REJECTED'; reasons.append('modelled gain too small: median dp %.3f (<%.2f bar, relative) on %d%% of grid cells below it' % (st['median'], BAR_OPP, round(100 * (1 - st['share_opp']))))
    c['reasons'] = reasons
    return c

def run_ability(kits=None, verbose=False):
    rows, kits = S.all_rows()
    lookup = {pair_id(r): r for r in rows}
    C = ability_candidates(rows, kits)
    out = []
    for c in C:
        if c['cls0'] == 'ORDINARY COMPATIBILITY':
            c['stats'] = None; c['value_kind'] = 'not evaluated (ordinary: substitutable)'; c['cells'] = 0; c['builds'] = []
            out.append(classify(c)); continue
        out.append(classify(evaluate_candidate(c, lookup)))
    return out, kits

# ---------------------------------------------------------------- item-zone candidates (e.g. Alchemical Fire kept inside its area by a partner)
ZONE_ITEMS = [('upgrade_thermal_detonator', 'Alchemical Fire', 3200)]

def item_zone_candidates(kits):
    out = []
    for cls, iname, cost in ZONE_ITEMS:
        T = (econ.abt().pv(econ.abt().at_tier(econ.abt().ability(cls), 0), 'AbilityDuration')) or 5.0
        cdI = econ.abt().pv(econ.abt().at_tier(econ.abt().ability(cls), 0), 'AbilityCooldown') or 30.0
        for pk_, part in kits.items():
            for o in part.offers:
                if o['kind'] not in ('cc_stun', 'cc_immobilize', 'displace_tether', 'slow') or o.get('condition') or o.get('unusable') or o.get('breaks_on_damage'): continue      # sleep excluded: the zone's own damage wakes the target
                d = o['params'].get('duration') if o['kind'] != 'slow' else None
                if not isinstance(d, (int, float)) or d <= 0.5: continue
                rel, _ = R.reliability(part, o)
                cds = [x for x in (o.get('cd') or []) if isinstance(x, (int, float)) and x > 0]
                cdp = cds[0] if cds else cdI
                av = min(1.0, cdI / cdp)
                cover = min(T, d)
                for ck, carry in kits.items():
                    if ck == pk_ or not builds_of(ck): continue
                    out.append(dict(id='ITEMZONE|%s|%s>%s' % (iname, ck, pk_), kind='ITEMZONE', rule='ITEMZONE', item=iname, cls=cls, cost=cost, carry=ck, partner=pk_, cname=carry.name, pname=part.name,
                                    offer=o, cover=cover, rel=rel * av, need=dict(aname=iname, kind='zone_occupancy', ability=cls), unknown=['whether the thrown flask lands where the held enemy stands (projectile aim)', 'DPSIncrease unit assumed per-second (UNVERIFIED)', 'whether an enemy held by the partner counts as inside the zone for the whole hold']))
    return out

def evaluate_item_zone(c):
    cells, used = grid_cells(c['carry'], lambda cm, P: econ.eval_item_zone(cm, c['cls'], c['cost'], c['cover'], c['rel'], P))
    c['stats'] = stats(cells); c['cells'] = len(cells); c['builds'] = used
    c['value_kind'] = 'MODELLED (Council trade model; opportunity cost = the build\'s own next purchases)'
    return c

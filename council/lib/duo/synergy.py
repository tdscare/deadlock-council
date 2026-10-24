"""Contribution scoring + substitution test + classification over ALL ordered pairs.
Contribution = (carry hero, carry need, rule class). Every partner (43) is scored on the SAME contribution; classification uses rank/spread."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit as K, rules as R

UNK_Q = 0.25      # a match whose strength is not in data is scored at most this (and flagged) - ASSUMED
EQUIV = 0.70      # partners within 70% of the best are "equivalent" substitutes - ASSUMED, swept 0.5..0.9

def need_key(n):
    return (n['kind'], n.get('ability'), n.get('aname'))

def qeff(m):
    if m.get('invalid'): return 0.0
    if m['q'] is None: return UNK_Q
    return m['q']

_cache = {}
def all_matches(kits=None):
    """{(carry, need_key, rule): {partner: best match}}"""
    kits = kits or K.all_kits()
    if 'x' in _cache: return _cache['x'], kits
    T = {}
    for ka, A in kits.items():
        for kb, B in kits.items():
            if ka == kb: continue
            for m in R.match_pair(A, B):
                key = (ka, need_key(m['need']), m['rule'])
                cur = T.setdefault(key, {}).get(kb)
                if cur is None or qeff(m) > qeff(cur): T[key][kb] = m
    _cache['x'] = T
    return T, kits

def classify_contribution(key, per_partner, npart):
    """returns list of (partner, match, rank, n_equiv, spread, cls) sorted by q."""
    qs = sorted(((qeff(m), kb, m) for kb, m in per_partner.items()), key=lambda x: -x[0])
    if not qs: return []
    best = qs[0][0]
    n_func = sum(1 for q, _, m in qs if m.get('functional') and q > 0)
    n_rel = sum(1 for q, _, _ in qs if q >= EQUIV * best and q > 0)
    n_equiv = max(n_func, n_rel)      # the larger of: partners functionally sufficient, partners within 70% of the best
    n_valid = sum(1 for q, _, _ in qs if q > 0)
    med = qs[len(qs) // 2][0] if qs else 0
    out = []
    for i, (q, kb, m) in enumerate(qs):
        if q <= 0: continue
        spread = (q - med) / best if best else 0
        out.append(dict(carry=key[0], need=m['need'], rule=key[2], partner=kb, match=m, q=q, rank=i + 1, n_equiv=n_equiv, n_valid=n_valid,
                        n_partners=npart, spread=spread, best=best, unknown=bool(m['unknown']), speculative=bool(m.get('speculative')) or m['q'] is None))
    return out

def provisional_class(r):
    """class from mechanics + substitution only (the DEDICATED level needs the value model in engine.py)."""
    share = r['n_equiv'] / float(r['n_partners'])
    if r['n_equiv'] > 3 or share > 0.08: return 'ORDINARY COMPATIBILITY'          # 5+ partners do the same job within 70% of the best
    if not r['match'].get('functional') and r['q'] < EQUIV * r['best']: return 'ORDINARY COMPATIBILITY'      # a different partner does it better and this one is not functionally sufficient
    if r['speculative']: return 'UNPROVEN IDEA'
    return 'GENUINE MECHANICAL SYNERGY'

def all_rows():
    T, kits = all_matches()
    rows = []
    for key, pp in T.items():
        for r in classify_contribution(key, pp, len(kits) - 1):
            r['cls0'] = provisional_class(r)
            rows.append(r)
    return rows, kits

if __name__ == '__main__':
    rows, kits = all_rows()
    import collections
    c = collections.Counter(r['cls0'] for r in rows)
    print(len(rows), c)
    top = sorted([r for r in rows if r['cls0'] == 'GENUINE MECHANICAL SYNERGY'], key=lambda r: -r['q'])
    for r in top[:60]:
        m = r['match']
        print('%-9s <- %-9s %-6s q=%.2f rk=%d/%d eq=%d  need=%s(%s) offer=%s(%s) unk=%d' % (kits[r['carry']].name, kits[r['partner']].name, r['rule'], r['q'], r['rank'], r['n_valid'], r['n_equiv'], r['need']['kind'], r['need']['aname'], m['offer']['kind'], m['offer']['aname'], len(m['unknown'])))

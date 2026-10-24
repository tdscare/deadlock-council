"""RESEARCHED CLAIMS (council/lib/captions/research.py).
A researcher (agent or human) writes hero-/build-specific claims into council/captions/research/<build id>.json.  The phrase is free text, but every claim
carries machine-checkable `checks` that are re-run against the raw game files at the claim's progression point; a claim whose checks fail (or whose
`requires` are not true at that purchase) is NOT publishable.  Check kinds:
  item_stat   {item, key, op, value}            item vdata property (abilities.vdata) compared with value
  item_text   {item, contains}                  the item's game text (citadel_mods localisation) contains the substring
  item_cmp    {a, a_key, op, b, b_key}          two items' properties compared (e.g. Capacitor chain count > Tesla Bullets chain count)
  ability_prop{slot, tier, prop, op, value}     hero ability property at that upgrade tier (vdata + upgrade deltas)
  ability_flag{slot, behavior|target_loc|shape} effects json (heroes.json) behaviour / targeting flag of the ability
  ability_scale{slot, tier, prop, scale}        the property's scale type is `scale` (e.g. ETechRadius)
  calc        {expr, equals}                    arithmetic over numbers only
requires: {"owned": [items owned before or at this purchase], "tier": {"<slot>": min tier under BOTH point models}, "not_owned": [...]}
"""
import os, re, json, ast, operator
import core as C
A = C.A
OPS = {'>=': operator.ge, '>': operator.gt, '<=': operator.le, '<': operator.lt, '==': lambda a, b: abs(a - b) < 1e-6}

def load(bid):
    p = os.path.join(C.SP, 'council', 'captions', 'research', bid + '.json')
    return json.load(open(p)) if os.path.exists(p) else {}

def _calc(expr):
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b}[type(n.op)]
        raise ValueError('only arithmetic over numbers')
    return ev(ast.parse(expr, mode='eval').body)

def run_check(P, ch):
    k = ch['kind']; R = P['R']; H = R['H']
    if k == 'item_stat':
        it = A.item(ch['item']); v = A.num(str(it['vstats'].get(ch['key'], ''))) if it else None
        return v is not None and OPS[ch['op']](v, ch['value']), f"{ch['item']}.{ch['key']}={v}"
    if k == 'item_text':
        it = A.item(ch['item']); t = A.desc(it['class']) if it else ''
        return ch['contains'].lower() in t.lower(), f"text of {ch['item']}"
    if k == 'item_cmp':
        a = A.num(str(A.item(ch['a'])['vstats'].get(ch['a_key'], ''))); b = A.num(str(A.item(ch['b'])['vstats'].get(ch['b_key'], '')))
        return a is not None and b is not None and OPS[ch['op']](a, b), f"{a} vs {b}"
    if k in ('ability_prop', 'ability_scale'):
        a = R['abil'][ch['slot']]; Q = A.at_tier(a, ch['tier']); p = Q.get(ch['prop'])
        if not p: return False, 'no such property'
        if k == 'ability_scale': return (p.get('stype') == ch['scale'] or ch['scale'] in (p.get('sfun') or '')), f"{ch['prop']} scale={p.get('stype')}"
        v = p.get('v'); return v is not None and OPS[ch['op']](v, ch['value']), f"{ch['prop']}@T{ch['tier']}={v}"
    if k == 'ability_flag':
        ad = next((x for x in C.hero_eff(P['b']['hk']) if x['slot'] == ch['slot']), None)
        if not ad: return False, 'ability not in effects json'
        if 'behavior' in ch: return ch['behavior'] in ad['behaviors'], str(ad['behaviors'])
        if 'target_loc' in ch: return ad['targeting'].get('location') == ch['target_loc'], str(ad['targeting'])
        if 'shape' in ch: return ad['targeting'].get('shape') == ch['shape'], str(ad['targeting'])
    if k == 'calc':
        try: return abs(_calc(ch['expr']) - ch['equals']) < 1e-6, ch['expr']
        except Exception as e: return False, str(e)
    return False, 'unknown check ' + k

def check_requires(P, w, req):
    why = []
    for it in req.get('owned', []):
        if it not in w['owned'] and it not in w['prev_own']: why.append(f'{it} not owned yet')
    for it in req.get('not_owned', []):
        if it in w['owned']: why.append(f'{it} already owned')
    for sl, t in (req.get('tier') or {}).items():
        if C.tmin(w, int(sl)) < t: why.append(f'ability {sl} below tier {t} under at least one point model')
    return (not why), why

def claims_for(P, w, bid_research):
    out = []
    for r in bid_research.get('items', {}).get(w['n'], []):
        c = C.claim(P, w, 'researched', r['phrase'], C.V, r.get('sources', []), r.get('score', 60), timing=(r.get('timing', 'now'), r.get('delta_souls', 0), r.get('event', '')),
                    check=dict(kind='researched', checks=r['checks'], requires=r.get('requires', {})), numbers=r.get('numbers', []), specific=True, researcher_note=r.get('note', ''))
        out.append(c)
    return out

def verify(P, w, c):
    ok, why = check_requires(P, w, c['check']['requires'])
    if not ok: return False, 'requires: ' + '; '.join(why)
    for ch in c['check']['checks']:
        r, d = run_check(P, ch)
        if not r: return False, f'check failed {ch}: {d}'
    return True, 'all checks pass'

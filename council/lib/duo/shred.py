"""Resist-shred / debuff-concentration analysis (the 'enabler concentrates debuffs vs carry buys them' question).
Everything from raw vdata; the two game rules the data does not state are carried as explicit bounds:
  SHARED   : does a resist debuff applied by player X raise damage dealt by player Y?   UNKNOWN -> scenarios shared / owner-only
  STACKING : how several shreds on one target combine                                   UNKNOWN -> bounds max / additive (Council formula) / relative
Resist formula (Council abtimeline.py line ~1892, ASSUMED): damage x (1-(r-s))/(1-r), r = enemy resist, s = shred. Relative bound: r' = r*(1-s)."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamedata as G, econ

BULLET_KEYS = ('BulletResistReduction', 'BulletArmorReduction')
SPIRIT_KEYS = ('MagicResistReduction', 'TechArmorDamageReduction', 'TechResistDebuff')
SOULS = {1: 800, 2: 1600, 3: 3200, 4: 6400}

def _trigger(txt):
    t = txt.lower()
    if 'headshot' in t: return 'on owner headshot'
    if 'when you deal' in t or 'you deal [spiritdamage]' in t or 'takes [spiritdamage]' in t or 'enemy takes' in t: return 'on owner spirit damage'
    if 'your bullets' in t or 'bullets reduce' in t: return 'on owner bullet hit'
    if 'nearby enem' in t: return 'aura (range)'
    if 'target an enemy' in t or 'disarms enemy target' in t: return 'active, targeted'
    if 'throw a flask' in t: return 'active, thrown area'
    if 'wound' in t: return 'on owner close-range damage'
    return 'unclear (text)'

_inv = None
def item_inventory():
    global _inv
    if _inv: return _inv
    d = G.D(); a = econ.abt(); out = []
    for k in d.abil:
        if not k.startswith('upgrade_'): continue
        A = G.Ability(k); nm = d.loc.get(k)
        if not nm: continue
        it = a.item(nm)
        if not it: continue
        for typ, keys in (('bullet', BULLET_KEYS), ('spirit', SPIRIT_KEYS)):
            for p in keys:
                if A.has(p) and (A.p(p, 0) or 0) < 0:
                    dur = next((A.p(q, 0) for q in ('DebuffDuration', 'AbilityDuration', 'ResistReductionDuration', 'BuffDuration') if A.has(q) and (A.p(q, 0) or 0) > 0), None)
                    sc = A.props0[p].get('scale') if isinstance(A.props0[p], dict) else None
                    sc = (sc.get('m_flStatScale') if isinstance(sc, dict) and sc.get('m_eSpecificStatScaleType') == 'ETechPower' else 0.0) or 0.0
                    out.append(dict(item=nm, cls=k, type=typ, pct=-A.p(p, 0), spirit_scale=-sc, prop=p, duration=dur, tier=it['tier'], slot=it['slot'], cost=SOULS.get(it['tier'], 0),
                                    cd=A.p('AbilityCooldown', 0) or 0, trigger=_trigger(A.fulltext()), range=A.p('AbilityCastRange', 0) or A.p('Radius', 0) or None,
                                    ev='%s.%s=%g (base tier; spirit scale %g)' % (k, p, A.p(p, 0), sc), comps=it['components']))
    _inv = out
    return out

def base_build(hk):
    for b in econ.builds().values():
        if b['hk'] == hk and not b['id'].endswith('_support'): return b['id']
    for b in econ.builds().values():
        if b['hk'] == hk: return b['id']

U_OWN = (0.5, 0.85)          # ASSUMED uptime of an owner-triggered debuff: buyer = enabler (not always on the target) vs carry (always shooting)

def mult_gain(r, s, mode):
    if mode == 'abs': return ((1 - (r - s)) / (1 - r)) - 1.0 if s else 0.0
    return ((1 - r * (1 - s)) / (1 - r)) - 1.0 if s else 0.0

def combine(shreds, mode):
    """combine several simultaneous shreds s_i (fractions): max / additive / multiplicative-of-remaining"""
    if not shreds: return 0.0
    if mode == 'max': return max(shreds)
    if mode == 'add': return sum(shreds)
    p = 1.0
    for s in shreds: p *= (1 - s)
    return 1 - p

def offer_vals(cm, kit, o, S):
    """the offer's pct / duration / cooldown at the ability tier the baseline build has reached at S (None if the ability is still untrained)"""
    A = next((a for a in kit.abilities if a.cls == o['ability']), None)
    if A is None or not o.get('pprop'): return None
    sl = cm.slot_of(o['ability']); T = 3 if sl is None else cm.seg(S)[1]['T'][sl]
    if T < 0: return None
    pct = abs(A.p(o['pprop'], T) or 0)
    dur = A.p(o['dprop'], T) if o.get('dprop') else None
    if not dur: dur = A.p('AbilityDuration', T) or None
    cd = A.p('AbilityCooldown', T) or 0
    return dict(pct=pct, dur=dur, cd=cd, tier=T)

def builtin_shreds(kit, typ='bullet'):
    out = []
    for o in kit.offers:
        if o['kind'] == 'shred_' + typ and not o.get('unusable') and isinstance(o['params'].get('duration'), (int, float)):
            out.append(o)
    return out

def analyse(carry_hk, enabler_hk, kits, S_list=(6000, 10000, 15000, 20000), P=None):
    """Return a table of options per checkpoint under {shared, owner-only} x {max, add} bounds. Carry = the gun hero being enabled."""
    P = P or econ.P_default()
    ca, en = base_build(carry_hk), base_build(enabler_hk)
    if not ca or not en: return dict(err='no baseline build in data.js for %s' % (ca and enabler_hk or carry_hk))
    cmA, cmB = econ.CarryModel(ca), econ.CarryModel(en)
    inv = [i for i in item_inventory() if i['type'] == 'bullet']
    kB = kits[enabler_hk]; bi = builtin_shreds(kB)
    rows = []
    for S in S_list:
        mA, e, trA = cmA.trade(S, P); mB, _, trB = cmB.trade(S, P)
        r = e['res']
        gA, gB = trA['gun'], trB['gun']          # bullet damage/s before resist
        W = P['W']; I = P['I']
        # built-in shred of the enabler (free): s, uptime within the trade window
        bs = 0.0; bdesc = None
        for o in bi:
            v = offer_vals(cmB, kB, o, S)
            if not v or not v['pct'] or not v['dur']: continue
            s = v['pct'] / 100.0; d = v['dur']; cd = v['cd']
            av = min(1.0, (W + I) / cd) if cd else 1.0
            u = av * min(d, W) / W
            if s * u > bs: bs, bdesc = s * u, '%s %s -%g%% for %gs (cd %gs, tier %d)' % (kB.name, o['aname'], s * 100, d, cd, v['tier'])
        for mode in ('abs', 'rel'):
            pass
        opts = []
        # lost dps from skipping the next `cost` souls of purchases (the build's own model)
        import math
        def lost(cm, cost):
            """buyer's own loss if the next `cost` souls of purchases are skipped, as ln(trade ratio) (the Council's survive-vs-kill metric)"""
            _, _, t0 = cm.trade(S, P); _, _, t1 = cm.trade(S + cost, P, enemy_souls=S)
            return max(0.0, math.log(max(0.05, t1['tr'])) - math.log(max(0.05, t0['tr'])))
        def mix(tr):
            tot = max(1e-9, tr['gun'] + tr['spirit'] + tr['melee'])
            return tr['gun'] / tot, tr['spirit'] / tot
        teamdps0 = trA['dps'] + trB['dps']
        for it in inv:
            for buyer, cm, tr, mm in (('carry', cmA, trA, mA), ('enabler', cmB, trB, mB)):
                s = (it['pct'] + it['spirit_scale'] * mm['sp']) / 100.0
                gs, ss = mix(tr)
                u = U_OWN[1] if buyer == 'carry' else U_OWN[0]
                tg = it['trigger']
                if tg in ('on owner bullet hit', 'on owner close-range damage'): u *= min(1.0, gs / 0.5)
                elif tg == 'on owner headshot': u *= min(1.0, gs / 0.5) * 0.6
                elif tg == 'on owner spirit damage': u *= min(1.0, ss / 0.5)
                elif tg == 'aura (range)': u = 0.8
                elif tg.startswith('active'):
                    cdv = it['cd'] or 1; u = min(1.0, (W + I) / cdv) * min(it['duration'] or W, W) / W
                lo = lost(cm, it['cost'])
                for scen in ('shared', 'owner-only'):
                    gun_benef = (gA + gB) if scen == 'shared' else (gA if buyer == 'carry' else gB)
                    for mode in ('abs', 'rel'):
                        dd = gun_benef * mult_gain(r, s * u, mode) * (1 - r)
                        # gain in the same currency: ln(team ttk before / after) for the team on one enemy
                        g_ln = math.log(teamdps0 + dd) - math.log(teamdps0)
                        opts.append(dict(S=S, item=it['item'], buyer=buyer, scen=scen, mode=mode, gain_dps=dd, gain=g_ln, lost=lo, net=g_ln - lo, cost=it['cost'], trigger=tg, s=s, u=u))
        # builtin value (free): shared / owner-only
        bg = {}
        for scen in ('shared', 'owner-only'):
            gb = (gA + gB) if scen == 'shared' else gB
            for mode in ('abs', 'rel'):
                bg[(scen, mode)] = gb * mult_gain(r, bs, mode) * (1 - r)
        rows.append(dict(S=S, r=r, gA=gA, gB=gB, dpsA=trA['dps'], dpsB=trB['dps'], ttk_team=e['ehp'] / max(1.0, trA['dps'] + trB['dps']), builtin=bs, builtin_desc=bdesc, builtin_gain=bg, opts=opts, ehp=e['ehp']))
    return dict(carry=carry_hk, enabler=enabler_hk, rows=rows, builds=(ca, en))

def best_by(rows_S, buyer, scen, mode):
    c = [o for o in rows_S['opts'] if o['buyer'] == buyer and o['scen'] == scen and o['mode'] == mode]
    return max(c, key=lambda o: o['net']) if c else None

def substitution(carry_hk, kits, S=10000, P=None):
    """score EVERY other hero as the shred enabler for this carry on the same quantity: built-in bullet-shred contribution at the tier that hero's baseline build has reached at S,
    expressed as ln(team dps after / before) with the carry alone as the beneficiary (shared scenario, Council abs formula) so heroes are directly comparable"""
    import math
    P = P or econ.P_default(); ca = base_build(carry_hk); cmA = econ.CarryModel(ca)
    mA, e, trA = cmA.trade(S, P); r = e['res']; out = []
    for hk, k in kits.items():
        if hk == carry_hk: continue
        bi = builtin_shreds(k)
        best = (0.0, None)
        if bi:
            cmB = econ.CarryModel(base_build(hk)) if base_build(hk) else None
            for o in bi:
                if o['params'].get('per_stack'): continue
                v = offer_vals(cmB, k, o, S) if cmB else None
                if not v or not v['pct'] or not v['dur']: continue
                s = v['pct'] / 100.0; d = v['dur']; cd = v['cd']
                u = (min(1.0, (P['W'] + P['I']) / cd) if cd else 1.0) * min(d, P['W']) / P['W']
                val = trA['gun'] * mult_gain(r, s * u, 'abs') * (1 - r)
                if val > best[0]: best = (val, '%s -%g%% %gs cd%g tier%d' % (o['aname'], s * 100, d, cd, v['tier']))
        out.append((best[0], k.name, best[1]))
    return sorted(out, reverse=True)

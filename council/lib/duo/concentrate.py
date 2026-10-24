"""'Concentrate the resist shred on the enabler' vs 'the carry buys it personally' vs 'ordinary builds', for one (carry, enabler) pair.
Measured against the carry's own time-to-kill (same currency as every other rule: p_kill = min(1, T_ESC/ttk)).
Scenarios (all expectations over target overlap):
  ordinary      : nobody coordinates; the enabler's debuff is on the carry's target with probability F_OV (ASSUMED 0.5, swept 0.3..0.7)
  coordinated   : both call the same target: probability F_CO (ASSUMED 0.9)
  x item        : carry buys the best personal bullet-shred item (independent of coordination)
  x variantE    : enabler re-orders abilities so the shred ability is maxed first (own cost charged)
Unknown rules are bounds: shared in {True, False}; resist formula in {abs (Council), rel}; stacking in {max, add}."""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import econ, shred, kit as K

F_OV, F_CO = (0.3, 0.5, 0.7), 0.9

def _gain(r, tr, shreds, mode, stack):
    """carry bullet dps gain from simultaneous shreds (list of effective fractions s*u)"""
    s = shred.combine([x for x in shreds if x > 0], 'max' if stack == 'max' else 'add')
    return tr['gun'] * shred.mult_gain(r, s, mode) * (1 - r)

def scenario_table(carry_hk, enabler_hk, kits, S_list=(6000, 10000, 15000, 20000), Pover=None):
    ca, en = shred.base_build(carry_hk), shred.base_build(enabler_hk)
    cmA, cmB = econ.CarryModel(ca), econ.CarryModel(en)
    kB = kits[enabler_hk]; bi = shred.builtin_shreds(kB)
    if not bi: return None
    # shred ability slot(s) of enabler for the variant order
    slots = sorted({cmB.slot_of(o['ability']) for o in bi if cmB.slot_of(o['ability'])})
    cmV = econ.CarryModel(en, order=econ.order_max_first(econ.builds()[en]['order'], slots[0])) if slots else None
    inv = [i for i in shred.item_inventory() if i['type'] == 'bullet']
    out = []
    for te, enm in itertools.product((3.0, 5.0, 8.0), (0.6, 1.0, 1.6)):
        P = econ.P_default(dict(T_ESC=te, enemy=enm, **(Pover or {})))
        W, I = P['W'], P['I']
        for S in S_list:
            mA, e, trA = cmA.trade(S, P); r = e['res']
            def E_s(cm):
                best = 0.0; desc = None
                for o in bi:
                    v = shred.offer_vals(cm, kB, o, S)
                    if not v or not v['pct'] or not v['dur']: continue
                    sv = v['pct'] / 100.0; cdv = v['cd']
                    u = (min(1.0, (W + I) / cdv) if cdv else 1.0) * min(v['dur'], W) / W
                    if sv * u > best: best, desc = sv * u, (o['aname'], v)
                return best, desc
            sB, dB = E_s(cmB)
            sV, dV = E_s(cmV) if cmV else (sB, dB)
            # enabler's own cost of the variant order: dps and ln trade ratio change at S
            _, _, trB0 = cmB.trade(S, P); _, _, trBV = (cmV.trade(S, P) if cmV else (None, None, trB0))
            ownB = trBV['dps'] - trB0['dps']; ownB_ln = math.log(max(.05, trBV['tr'])) - math.log(max(.05, trB0['tr']))
            # best personal item for the carry (ASSUMED uptime by trigger/damage mix, as in shred.analyse)
            gs = trA['gun'] / max(1e-9, trA['gun'] + trA['spirit'] + trA['melee']); ss = trA['spirit'] / max(1e-9, trA['gun'] + trA['spirit'] + trA['melee'])
            bestI = (0.0, None)
            for it in inv:
                s_it = (it['pct'] + it['spirit_scale'] * mA['sp']) / 100.0
                u = 0.85; tg = it['trigger']
                if tg in ('on owner bullet hit', 'on owner close-range damage'): u *= min(1.0, gs / 0.5)
                elif tg == 'on owner headshot': u *= min(1.0, gs / 0.5) * 0.6
                elif tg == 'on owner spirit damage': u *= min(1.0, ss / 0.5)
                elif tg == 'aura (range)': u = 0.8
                elif tg.startswith('active'):
                    cdv = it['cd'] or 1; u = min(1.0, (W + I) / cdv) * min(it['duration'] or W, W) / W
                elif tg.startswith('unclear'): continue
                if s_it * u > bestI[0]: bestI = (s_it * u, it)
            sI, itm = bestI
            for mode, stack, shared in itertools.product(('abs', 'rel'), ('max', 'add'), (True, False)):
                gE = lambda s_e: (_gain(r, trA, [s_e], mode, stack) if shared else 0.0)
                def dpsA_exp(ov, sE, with_item):
                    base = trA['dps']
                    wE = base + (_gain(r, trA, [sE] + ([sI] if with_item else []), mode, stack) if shared else (_gain(r, trA, [sI], mode, stack) if with_item else 0.0))
                    woE = base + (_gain(r, trA, [sI], mode, stack) if with_item else 0.0)
                    return ov * wE + (1 - ov) * woE
                for f in F_OV:
                    p = lambda d: econ.pk(e['ehp'] / max(1.0, d), P)
                    ordn = p(dpsA_exp(f, sB, False)); coord = p(dpsA_exp(F_CO, sB, False))
                    varE = p(dpsA_exp(F_CO, sV, False))
                    ordI = p(dpsA_exp(f, sB, True)); coI = p(dpsA_exp(F_CO, sB, True)); coIV = p(dpsA_exp(F_CO, sV, True))
                    out.append(dict(S=S, T_ESC=te, enemy=enm, f=f, mode=mode, stack=stack, shared=shared,
                                    d_opp=coord - ordn, d_varE=varE - coord, d_item_coord=(coI - ordI) - (coord - ordn), d_full=coIV - max(ordn, ordI),
                                    d_full_vs_opp=coIV - max(coord, ordI), sB=sB, sV=sV, sI=sI, item=(itm or {}).get('item'), ownB=ownB, ownB_ln=ownB_ln, p_ord=ordn, p_coord=coord, p_varE=varE,
                                    p_item_ord=ordI, p_item_coord=coI, p_full=coIV, dpsA=trA['dps'], gA=trA['gun'], ttk=e['ehp'] / max(1, trA['dps'])))
    return dict(carry=carry_hk, enabler=enabler_hk, builds=(ca, en), cells=out, tiers=dict(base=dB, var=dV), slot=slots[0] if slots else None)

def summarize(T, key, filt=lambda c: True):
    v = sorted(c[key] for c in T['cells'] if filt(c))
    if not v: return None
    n = len(v)
    return dict(n=n, median=v[n // 2], p10=v[int(n * .1)], p90=v[min(n - 1, int(n * .9))], min=v[0], max=v[-1])

# Drivers for haze_model.py (CALCULATED). python3 -I haze_runs.py
import sys, os
sys.path.insert(0, '.')
from haze_model_fix import *

CPS2 = [5000, 10000, 12000, 14400, 18000, 24000, 30000, 41600, 52800, 56000]
def ref_dps(s):
    o, _ = owned_after(CUR, s); S = stats(o, s); return fight(S)['dmg'] / 10

def survive(path, s, k=2.0, T=12, **kw):
    o, spent = owned_after(path, s); S = stats(o, s)
    f = fight(S, T=T, incoming=k * ref_dps(s), **kw)
    return S, f, spent

def table(paths, k=2.0, **kw):
    print(f"\n# focus test: incoming = {k} x CUR 1v1 dps at same souls, 12 s, smoke ready; kw={kw}")
    print('path | ' + ' | '.join(str(c//1000)+'k' for c in CPS2))
    for nm in paths:
        cells = []
        for c in CPS2:
            S, f, sp = survive(PATHS[nm], c, k, **kw)
            d = f['dead']; cells.append((f"dies {d:.1f}s" if d is not None else f"{100*f['hpend']/S['HPMAX']:.0f}%HP") + f" dmg{f['dmg']:.0f} eff{f['eff']:.0f}")
        print(nm + ' | ' + ' | '.join(cells))

def marginal(base_path, upto, cands, s, k=2.0, **kw):
    """value of buying candidate X at soul total s after base_path[:upto]"""
    pre = base_path[:upto]; o0, sp0 = owned_after(pre, 10**6); S0 = stats(o0, s)
    f0 = fight(S0, T=12, incoming=k * ref_dps(s), **kw); g0 = fight(S0, targets=3, **kw)
    print(f"\n# marginal at {s} souls after {pre[-1]} (spent {sp0}); base 1v1 dmg {f0['dmg']:.0f} eff-heal {f0['eff']:.0f} end {f0['hpend']:.0f}/{S0['HPMAX']:.0f} dead {f0['dead']}; 3-tgt {g0['dmg']:.0f}; kw={kw}")
    for x in cands:
        o, sp = owned_after(pre + x, 10**6); S = stats(o, s)
        f = fight(S, T=12, incoming=k * ref_dps(s), **kw); g = fight(S, targets=3, **kw); u = fight(S, T=6, ult=True, targets=3, **kw)
        c = sp - sp0
        print(f"  +{'+'.join(x):38s} cost {c:5d} | 1v1 dmg {f['dmg']-f0['dmg']:+6.0f} | eff heal {f['eff']-f0['eff']:+6.0f} | end HP {f['hpend']-f0['hpend']:+6.0f} dead {f['dead']} | 3-tgt {g['dmg']-g0['dmg']:+6.0f} | ult6s {u['dmg']:6.0f} | per 1k: dmg {1000*(f['dmg']-f0['dmg'])/max(c,1):+5.0f} hp {1000*(f['hpend']-f0['hpend'])/max(c,1):+5.0f}")

if __name__ == '__main__':
    table(list(PATHS))
    table(list(PATHS), k=1.0)
    table(['CUR (data.js)', 'K2 lifesteal-early, no HB/HT'], amp_on_ls=False)
    table(['CUR (data.js)', 'K2 lifesteal-early, no HB/HT'], tempo='siphon')
    # Q1 16k slot: Healing Booster vs Bullet Lifesteal vs Duration Extender vs Burst Fire early vs Extra Charge
    for kw in ({}, {'amp_on_ls': False}):
        marginal(CUR, 8, [['Healing Booster'], ['Bullet Lifesteal'], ['Duration Extender'], ['Burst Fire'], ['Extra Charge'], ['Extra Regen']], 16000, **kw)
    # Q2 last slot: Healing Tempo vs alternatives at 52.8k (after Silencer)
    for kw in ({}, {'tempo': 'siphon'}, {'tempo': 'vb'}):
        marginal(CUR, 17, [['Healing Tempo'], ['Frenzy'], ['Duration Extender', 'Superior Duration'], ['Spiritual Overflow'], ['Leech']], 52800, **kw)
    # Q3 Leech vs Vampiric Burst at 41.6k (after Rapid Recharge; Bullet Lifesteal owned)
    marginal(CUR, 15, [['Vampiric Burst'], ['Spirit Lifesteal', 'Leech'], ['Frenzy']], 41600)
    marginal(CUR, 15, [['Vampiric Burst'], ['Spirit Lifesteal', 'Leech']], 41600, k=1.0)
    # Q4 charges: Extra Charge / Rapid Recharge value at 28k and 36.8k
    marginal(CUR, 12, [['Extra Charge'], ['Extra Charge', 'Rapid Recharge'], ['Duration Extender'], ['Extra Charge', 'Duration Extender']], 28000)
    # Q5 Ricochet vs Fortitude first at 12k / 14.4k
    marginal(CUR, 5, [['Extra Health', 'Fortitude'], ['Ricochet'], ['Burst Fire', 'Bullet Lifesteal', 'Extra Health']], 12000)
    # Q6 Burst Fire vs Healing Booster->Tempo rush at 22.4k
    marginal(CUR, 9, [['Burst Fire'], ['Healing Tempo'], ['Siphon Bullets']], 22400)
    marginal(CUR, 9, [['Burst Fire'], ['Healing Tempo'], ['Siphon Bullets']], 22400, tempo='siphon')

def m2(base_items, s, cands, k=2.0, label='', **kw):
    """explicit owned sets (slot-honest): base_items owned; each cand = (remove list, add list)"""
    def ev(items):
        S = stats(items, s)
        r = {}
        r['b6'] = fight(S, T=6, **kw)['dmg']; r['s20'] = fight(S, T=20, **kw)['dmg']
        f = fight(S, T=12, incoming=k * ref_dps(s), **kw); r['hp'] = f['hpend']; r['dead'] = f['dead']; r['eff'] = f['eff']
        r['t3'] = fight(S, T=12, targets=3, **kw)['dmg']; r['u'] = fight(S, T=6, ult=True, targets=3, **kw)['dmg']
        return r
    b = ev(base_items)
    print(f"\n# {label} @ {s} souls; base 6s {b['b6']:.0f} 20s {b['s20']:.0f} 3tgt12s {b['t3']:.0f} ult6s {b['u']:.0f} focus12s endHP {b['hp']:.0f} dead {b['dead']}; kw={kw}")
    for rem, add in cands:
        items = [i for i in base_items if i not in rem] + add
        r = ev(items)
        cost = sum(COST[G[i]['tier']] for i in items) - sum(COST[G[i]['tier']] for i in base_items)
        dd = r['dead'] if r['dead'] is None else round(r['dead'], 1)
        print(f"  -{'/'.join(rem) or '-':28s} +{'/'.join(add):34s} souls {cost:+6d} | 6s {r['b6']-b['b6']:+5.0f} | 20s {r['s20']-b['s20']:+6.0f} | 3tgt {r['t3']-b['t3']:+6.0f} | ult {r['u']-b['u']:+5.0f} | focus endHP {r['hp']-b['hp']:+6.0f} dead {dd}")

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'm2':
    full = owned_after(CUR, 52800)[0]
    print('full CUR owned:', full)
    alts = [(['Healing Tempo'], ['Healing Booster']),
            (['Healing Tempo'], []),
            (['Healing Tempo'], ['Frenzy']),
            (['Healing Tempo'], ['Superior Duration']),
            (['Healing Tempo'], ['Leech']),
            (['Healing Tempo'], ['Spiritual Overflow']),
            (['Healing Tempo'], ['Burst Fire']) ,
            (['Vampiric Burst'], ['Leech']),
            (['Burst Fire'], ['Surge of Power']),
            (['Siphon Bullets'], ['Leech']),
            (['Active Reload'], ['Superior Duration']),
            (['Fortitude'], ['Superior Duration']),
            (['Silencer'], ['Frenzy'])]
    for kw in ({}, {'tempo': 'siphon'}, {'amp_on_ls': False}, {'acc': 0.35}, {'resist': 0.35}):
        m2(full, 52800, alts, label='CUR full build, slot-honest swaps', **kw)
    mid = owned_after(CUR, 28000)[0]
    print('CUR at 28k owned:', mid)
    m2(mid, 28000, [(['Healing Booster'], ['Bullet Lifesteal']), (['Healing Booster'], []), (['Healing Booster'], ['Duration Extender']), (['Healing Booster'], ['Healing Tempo']),
                    (['Siphon Bullets'], ['Healing Tempo']), (['Burst Fire'], ['Healing Tempo']), (['Extra Charge'], ['Duration Extender'])], label='CUR at 28k')
    m2(mid, 28000, [(['Healing Booster'], ['Healing Tempo']), (['Siphon Bullets'], ['Healing Tempo']), (['Burst Fire'], ['Healing Tempo'])], label='CUR at 28k, Tempo procs off Siphon', tempo='siphon')

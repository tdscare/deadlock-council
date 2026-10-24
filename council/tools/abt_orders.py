# compare point orders for one build as whole builds (tiers per checkpoint + conditional flags). usage: python3 -I council/tools/abt_orders.py <id> <label>=<order> ...
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import abtimeline as T
bid = sys.argv[1]; B = T.load_builds(); b = [x for x in B if x['id'] == bid][0]
CK = [1600, 4800, 8000, 12800, 19200, 28800]
for arg in sys.argv[2:]:
    lab, o = arg.split('='); o = [int(c) for c in o]
    assert all(o.count(i) == 4 for i in (1, 2, 3, 4)) and len(o) == 16, lab
    R = T.analyse(b, o); ev = {(x[2], x[3]): x[0] for x in R['evA']}
    print(f"## {lab} {''.join(map(str,o))}")
    print('  ' + ' | '.join(f"{T.nm(R,s)[:14]} " + '/'.join(str(ev.get((s, t), '-')) for t in range(4)) for s in (1, 2, 3, 4)) + '   (unlock/T1/T2/T3 souls)')
    for s in CK:
        w = [x for x in R['rows'] if not x.get('unknown') and x['souls'] <= s]
        if not w: continue
        w = T.state(R, dict(w[-1], souls=s)); parts = []
        for sl in (1, 2, 3, 4):
            t = w['tA'][sl]
            if t < 0: parts.append(f"{T.nm(R,sl)[:10]} L"); continue
            P = T.at_tier(R['abil'][sl], t); h = T.spirit_hits(P, T.slot_sp(R, w, sl, t)); cd = T.pv(P, 'AbilityCooldown'); bc = T.pv(P, 'AbilityCooldownBetweenCharge')
            parts.append(f"{T.nm(R,sl)[:10]} {T.tlabel(t)} cd{cd:g}{'/'+format(bc,'g') if bc and bc>0 else ''}" + (f" {max(v for v,i in h.values()):.0f}" if h else ''))
        print(f"  @{s:>5}: " + ' | '.join(parts))
    print('  flags: ' + (', '.join(f"{r['item']}@{r['souls']} {r['flag']}" + (f" gap {r['gap']}" if r.get('gap') else '') for r in T.fmt(R)[1] if r['flag']) or 'none'))

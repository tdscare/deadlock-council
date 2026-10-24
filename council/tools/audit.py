"""audit.py: run build_one over every build in data.js (read-only) -> council/captions/builds/*.json + AUDIT.json + AUDIT.md"""
import os, json, collections, time, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lib', 'captions'))
import core as C
SP = C.SP
CLS = {'a': 'a useful now', 'b': 'b justified imminent / path to first spike', 'c': 'c preparatory, weak now -> timing review', 'g': 'g accurate but generic (held)', 'd': 'd no rationale established', 'x': 'x contradiction (purchase may need investigation)'}
def run_all(out, build_one, write_build):
    ids = list(C.builds().keys()); per = []; tot = collections.Counter(); itemd = collections.Counter(); itemx = collections.Counter(); errs = []
    t0 = time.time(); legacy_total = 0; legacy_unv = 0; lint_fail = 0; items_total = 0; lint_rules = collections.Counter()
    for bid in ids:
        try: bun = build_one(bid)
        except Exception as e:
            errs.append((bid, repr(e))); continue
        write_build(bun, out)
        st = collections.Counter(i['cls'] for s in bun['sections'] for i in s['items'])
        n = sum(st.values()); items_total += n
        pub = sum(1 for s in bun['sections'] for i in s['items'] if i['caption'])
        lf = sum(1 for s in bun['sections'] for i in s['items'] if i['lint'])
        lint_fail += lf
        for s in bun['sections']:
            for i in s['items']:
                for r in i['lint']: lint_rules[r[0]] += 1
                if i['legacy_note']: legacy_total += 1
                if i['cls'] == 'd': itemd[i['name']] += 1
                if i['cls'] == 'x': itemx[(i['name'], i['why'][:90])] += 1
        legacy_unv += sum(1 for r in bun['review'] if r['cls'] == 'legacy-unverified')
        tot.update(st)
        per.append(dict(id=bid, hero=bun['hero'], items=n, published=pub, **{k: st.get(k, 0) for k in 'abcgdx'}, lint_blocked=lf, section_order=bun['section_order']))
    json.dump(dict(per_build=per, totals=dict(tot), items=items_total, errors=errs, legacy_notes=legacy_total, legacy_unverified=legacy_unv, lint_rule_hits=dict(lint_rules),
                   top_d=itemd.most_common(40), x=[(k, v) for k, v in itemx.items()], runtime_s=round(time.time() - t0, 1), data_sha16=C.data_sha()), open(SP + '/council/captions/AUDIT.json', 'w'), indent=1)
    print('builds', len(per), 'errors', errs[:5]); print('items', items_total, dict(tot)); print('published', sum(p['published'] for p in per), 'lint-blocked', lint_fail, dict(lint_rules)); print('legacy notes', legacy_total, 'unverified', legacy_unv)
    print('top d', itemd.most_common(25)); print('x', list(itemx.items())[:20])

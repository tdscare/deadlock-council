#!/usr/bin/env python3
"""CAPTIONS (council/tools/captions.py): research -> claim records -> caption draft -> validation -> review list, per build.  READ-ONLY w.r.t. data.js.
usage (from SP):  python3 -I council/tools/captions.py build <id>... [--out council/captions/builds]
                  python3 -I council/tools/captions.py all [--out council/captions/builds]      # every build in data.js; writes AUDIT.json/AUDIT.md
                  python3 -I council/tools/captions.py show <id>                                  # human-readable
                  python3 -I council/tools/captions.py preview <id>... [--out council/captions/preview.html]   # real site renderer + overlay (see preview.py)
Output per build: council/captions/builds/<id>.json (schema council/captions/SCHEMA.md). Never writes data.js or any other agent's file."""
import os, sys, json, re, time, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lib', 'captions'))
import core as C
import research as RS
A = C.A
SP = C.SP
OUT = os.path.join(SP, 'council', 'captions')

SECTION_ORDER = ['lane', 'early', 'mid', 'late', 'counters', 'swap', 'luxury', 'slot_locked']
SECTION_LABEL = {'lane': 'Losing lane (temporary)', 'early': 'Early game', 'mid': 'Midgame', 'late': 'Late game', 'counters': 'Situational counters',
                 'swap': 'Optional swap / pivot', 'luxury': 'Luxury purchases', 'slot_locked': 'Slot locked upgrades', 'other': 'Other'}
def section_of(title):
    t = title.lower()
    if t.startswith('early'): return 'early'
    if t.startswith('mid'): return 'mid'
    if t.startswith('late'): return 'late'
    if t.startswith('counters'): return 'counters'
    if "rich" in t: return 'luxury'
    if t.startswith('slot locked'): return 'slot_locked'
    if t.startswith('losing lane') or t.startswith('lost lane'): return 'lane'
    if t.startswith('swap') or t.endswith('?') or t.startswith('swaps'): return 'swap'
    return 'other'

BOILER = re.compile(r'^(Sell [^.]*?(for this|once you\'re out of slots|it for [^.]*)\.?|Upgrade of [^.]*\.?|If you bought [^.]*\.?|Instead of [^.]*\.?)$')

def build_one(bid):
    P = C.progression(bid); b = P['b']; R = P['R']; RES = RS.load(bid)
    legacy = C.legacy_notes(bid)
    pts = P['pts']; pi = 0
    sections = []; claims = {}; review = []
    stats = collections.Counter()
    boxes = []
    for r in b['rows']:
        for bx in r: boxes.append(bx)
    for bx in boxes:
        title, bdesc, opt, items = bx[0], bx[1], bx[2], bx[3]
        sec = section_of(title); core = bool(C.CORE_BOX.match(title))
        out_items = []; phase_pts = []
        for it in items:
            name = it[0]; imb = it[2] if len(it) > 2 else None
            note = it[1] if len(it) > 1 else ''
            rec = dict(name=name, imbue=imb or None, caption=None, cls=None, why='', claim_ids=[], lint=[], legacy_note=note or None, temporary=sec == 'lane' or bool(re.search(r'Sell [^.]*it\b', note or '')))
            if not A.item(name):
                rec.update(cls='x', why='item not found in item table (name check)'); out_items.append(rec); review.append(dict(build=bid, item=name, section=sec, cls='x', why=rec['why'])); continue
            if core:
                w = pts[pi]; pi += 1
                assert w['n'] == name, (bid, w['n'], name)
                phase_pts.append(w)
            else:
                w = C.noncore_point(P, name, imb, title, note); w['_note'] = note
            cs = C.claims_for(P, w, note) + RS.claims_for(P, w, RES)
            cls, why = C.classify(P, w, cs)
            text, used = C.compose(P, w, cs, cls)
            cmap = {c['id']: c for c in cs}
            for c in cs: claims[c['id']] = c
            used_c = [cmap[i] for i in used]
            ok_all = True; vres = []
            for c in used_c:
                ok, detail = RS.verify(P, w, c) if c['kind'] == 'researched' else C.verify_claim(P, c)
                vres.append((c['id'], ok, detail))
                if not ok: ok_all = False
            errs = C.lint_caption(P, w, text, used_c, name) if text else []
            if text and (errs or not ok_all):
                rec['lint'] = errs + ([('claim-verify-failed', [v for v in vres if not v[1]])] if not ok_all else [])
                text = None; cls_old = cls; cls = 'd' if cls in ('a', 'b') else cls
                why = f"caption failed validation ({[e[0] for e in rec['lint']]}); not published"
            if cls in ('c', 'd', 'x') or text is None:
                text = None
            if cls in ('a', 'b') and text is None:
                cls = 'd'; why = why or 'no publishable claim'
            rec.update(caption=text, cls=cls, why=why, claim_ids=used, verify=vres)
            stats[cls] += 1
            if cls != 'a' or legacy_flag(note):
                pass
            if cls in ('b', 'c', 'd', 'x'):
                review.append(dict(build=bid, item=name, section=sec, cls=cls, why=why, souls=w['souls'],
                                   unpublished=[dict(id=c['id'], tier=c['tier'], phrase=c['phrase'], timing=c['timing']) for c in cs if c['tier'] not in C.PUBLISHABLE or c['timing']['when'] not in ('now',)][:4]))
            if legacy_flag(note):
                review.append(dict(build=bid, item=name, section=sec, cls='legacy-unverified', why='legacy note in data.js is not backed by any claim record (kept untouched, not published by this system)', legacy_note=note))
            out_items.append(rec)
        desc = None; dclaims = []
        if core and phase_pts:
            desc, dclaims = C.phase_desc(P, title, phase_pts)
            for dc in dclaims: claims[dc['id']] = dc
        sections.append(dict(section=sec, label=SECTION_LABEL[sec], box_title=title, optional=bool(opt), legacy_desc=bdesc or None, desc=desc if core else (bdesc or None),
                             desc_origin='generated:progression' if core else ('legacy' if bdesc else None), desc_claims=[dc['id'] for dc in dclaims], items=out_items))
    order_ok = [s['section'] for s in sections]
    return dict(schema=1, id=bid, hero=b['hero'], name=b['name'], game_build='6819 (gt6819 / effects format 1)', data_js_sha16=C.data_sha(), generator='council/tools/captions.py',
                point_model='claims about ability tiers require model A and model B to agree', section_order=order_ok, sections=sections,
                claims=claims, review=review, stats=dict(stats))

def legacy_flag(note):
    return bool(note) and not BOILER.match(note.strip())

def write_build(bundle, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, bundle['id'] + '.json')
    json.dump(bundle, open(p, 'w'), indent=1)
    return p

def show(bundle):
    print(f"# {bundle['id']} | {bundle['name']} | stats {bundle['stats']}")
    for s in bundle['sections']:
        print(f"\n[{s['label']}] ({s['box_title']}){' OPTIONAL' if s['optional'] else ''}\n   desc: {s['desc']}")
        for i in s['items']:
            print(f"  - {i['name']}{' (imb ' + str(i['imbue']) + ')' if i['imbue'] else ''} [{i['cls']}] {i['caption'] or '-- NO CAPTION: ' + i['why']}")

def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    cmd = a[0]; out = OUT + '/builds'
    if '--out' in a: out = a[a.index('--out') + 1]
    if cmd == 'build':
        for bid in [x for x in a[1:] if not x.startswith('--') and x != out]:
            bun = build_one(bid); p = write_build(bun, out); show(bun); print('->', p)
    elif cmd == 'show':
        show(build_one(a[1]))
    elif cmd == 'all':
        t0 = time.time(); import audit
        audit.run_all(out, build_one, write_build); print('runtime s', round(time.time() - t0, 1))
    elif cmd == 'preview':
        import preview
        preview.make([x for x in a[1:] if not x.startswith('--')], a[a.index('--out') + 1] if '--out' in a else OUT + '/preview.html')
    else: print(__doc__)
if __name__ == '__main__': main()

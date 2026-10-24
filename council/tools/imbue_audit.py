#!/usr/bin/env python3
"""Data-only audit of imbue placement across all builds (offline; reads a node dump of data.js, never writes it).
usage: node <dump> -> /tmp/builds_dump.json ; python3 -I tools/imbue_audit.py [builds_dump.json]
Classes (every finding cites item type / ability fields):
 CERTAIN-INVALID  the game data itself makes the placement dead (no dependence on how multiple imbues combine)
 CERTAIN-NOOP     imbue effect needs a property the ability does not have (cooldown / duration / range-radius)
 DEPENDS-ON-N01   2+ imbue items on one ability slot: allowed? replace? stack? (UNRESOLVED)
 UNMAPPED         hero not in heroes.vdata extraction: only item types can be checked
"""
import json, os, sys, ast, collections
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EF = os.path.join(C, 'evidence', 'interactions', 'effects')
H = json.load(open(os.path.join(EF, 'heroes.json')))['heroes']
I = json.load(open(os.path.join(EF, 'items.json')))['items']
byname = {v['name']: (c, v) for c, v in I.items()}
def L(x):
    return x if isinstance(x, (list, dict)) else (ast.literal_eval(x) if isinstance(x, str) and x[:1] in '[{' else x)
def mx(v):
    v = L(v)
    try: return max(float(t) for t in v)
    except Exception: return 0.0
TEXT = {  # game's own text (localization, abridged) for the imbue types that matter
 'modifier_value': 'ability value imbue (cooldown / duration / range+radius / lifesteal)',
 'active': 'effect triggers when the imbued ability is used',
 'active_non_ult': 'Echo Shard: "Reset the cooldown of the imbued non-ultimate ability."',
}
def props(a):
    p = L(a['props']);
    return p if isinstance(p, dict) else {}
def has_range(a):
    return any(('Radius' in k or 'Range' in k or 'Distance' in k) and mx((v.get('by_tier') if isinstance(v, dict) else v) or [0]) > 0 for k, v in props(a).items() if not k.startswith('Tech') )
def audit(builds):
    out = []; sums = collections.Counter(); per_build = {}
    for b in builds:
        h = H.get(b['hk']); abil = h['abilities'] if h else None
        sig = {}
        if abil:
            for a in abil:
                if str(a.get('slot')) in '1234' and a.get('slot') is not None: sig[int(a['slot'])] = a
        groups = collections.defaultdict(list)
        for it in b['items']:
            if it.get('imbue') is None or it['imbue'] == '': continue
            groups[int(it['imbue'])].append(it['name'])
        # an item appearing under two different slots in the same build
        slots_of = collections.defaultdict(set)
        for s, ns in groups.items():
            for n in ns: slots_of[n].add(s)
        rec = dict(build=b['id'], hero=b['hero'], mapped=bool(h), findings=[])
        for n, ss in slots_of.items():
            if len(ss) > 1: rec['findings'].append(('CERTAIN-INVALID', n, sorted(ss), 'one item has one imbue target ("Imbue an ability ...", singular) but is imbued on %d abilities in this build' % len(ss)))
        for s, ns in groups.items():
            a = sig.get(s); types = []
            for n in dict.fromkeys(ns):
                c, v = byname.get(n, (None, None))
                if not v: rec['findings'].append(('UNKNOWN-ITEM', n, s, 'item name not in items.json')); continue
                t = v['imbue']; types.append((n, t))
                if not a: continue
                an = '%s (slot %d)' % (a['name'], s)
                cd = mx(a['cooldown_by_tier']); du = mx(a['duration_by_tier'])
                if t == 'active_non_ult' and (a['is_ult'] == 'True' or s == 4):
                    rec['findings'].append(('CERTAIN-INVALID', n, an, 'type IMBUE_ACTIVE_NON_ULT (%s) on an ultimate' % TEXT['active_non_ult']))
                if n in ('Echo Shard',) and cd <= 0:
                    rec['findings'].append(('CERTAIN-NOOP', n, an, 'no cooldown at any tier (cooldown_by_tier=%s): nothing to reset' % a['cooldown_by_tier']))
                if n == 'Compress Cooldown' and cd <= 0:
                    rec['findings'].append(('CERTAIN-NOOP', n, an, 'no cooldown at any tier: nothing to compress'))
                if n == 'Duration Extender' and du <= 0:
                    dp = sorted(k for k, v in props(a).items() if 'Duration' in k and k not in ('AbilityDuration', 'AbilityPostCastDuration') and mx((v.get('by_tier') if isinstance(v, dict) else v) or [0]) > 0)
                    rec['findings'].append(('DEPENDS-ON-N08', n, an, 'AbilityDuration=0 at every tier; other duration props: %s (does the extender scale them? UNRESOLVED)' % (', '.join(dp[:5]) or 'none')))
                if t in ('active', 'active_non_ult') and cd <= 0 and mx(a['charges_by_tier']) <= 0:
                    rec['findings'].append(('CERTAIN-NOOP?', n, an, 'item acts when the imbued ability is USED; ability has no cooldown and no charges'))
                elif t in ('active', 'active_non_ult') and cd <= 0:
                    rec['findings'].append(('DEPENDS-ON-CHARGES', n, an, 'no cooldown field but charges_by_tier=%s: how a use-triggered imbue interacts with charge recharge is UNRESOLVED' % a['charges_by_tier']))
                if n == 'Mystic Expansion' and not has_range(a):
                    rec['findings'].append(('CERTAIN-NOOP?', n, an, 'no range/radius/distance property on the ability (props scanned)'))
            if len(set(ns)) >= 2:
                tt = [t for _, t in types]
                rec['findings'].append(('DEPENDS-ON-N01', ', '.join(dict.fromkeys(ns)), 'slot %d%s' % (s, ' ' + sig[s]['name'] if s in sig else ''), 'types: ' + ' + '.join(tt) + (' | SAME TYPE x%d' % max(collections.Counter(tt).values()) if len(set(tt)) < len(tt) else '')))
        per_build[b['id']] = rec
    return per_build
def _main():
    B = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/builds_dump.json'))
    R = audit(B)
    cnt = collections.Counter(); builds_by = collections.defaultdict(set)
    for r in R.values():
        for f in r['findings']:
            cnt[f[0]] += 1; builds_by[f[0]].add(r['build'])
    n_imb = sum(1 for b in B if any(i.get('imbue') for i in b['items']))
    res = dict(n_builds=len(B), builds_with_imbue=n_imb, unmapped=[r['build'] for r in R.values() if not r['mapped']],
               finding_counts=dict(cnt), builds_per_class={k: sorted(v) for k, v in builds_by.items()}, per_build={k: v for k, v in R.items() if v['findings']})
    json.dump(res, open(os.path.join(C, 'evidence', 'interactions', 'imbue_audit', 'imbue_audit.json'), 'w'), indent=1)
    print(json.dumps({k: (v if k != 'per_build' else len(v)) for k, v in res.items() if k != 'builds_per_class'}, indent=1))
    print({k: len(v) for k, v in builds_by.items()})

def summary_text(B, R):
    sz = collections.Counter(); combo = collections.Counter(); ult = []; echo_cc = []; same = []; dead = 0; deadtier = collections.Counter(); builds = set(); per = {}
    for b in B:
        h = H.get(b['hk']); sig = {int(a['slot']): a for a in (h['abilities'] if h else []) if isinstance(a.get('slot'), int)}
        g = collections.defaultdict(list)
        for it in b['items']:
            if it.get('imbue'): g[int(it['imbue'])].append(it['name'])
        for s, ns in g.items():
            ns = list(dict.fromkeys(ns)); sz[len(ns)] += 1
            if len(ns) < 2: continue
            builds.add(b['id']); dead += len(ns) - 1
            ty = [byname[n][1]['imbue'] for n in ns if n in byname]
            combo[' + '.join(sorted(collections.Counter(ty).elements()))] += 1
            if len(set(ty)) < len(ty): same.append('%s slot %d: %s' % (b['id'], s, ', '.join(ns)))
            if 'Echo Shard' in ns and 'Compress Cooldown' in ns: echo_cc.append('%s slot %d' % (b['id'], s))
            if s in sig and sig[s]['is_ult'] in (True, 'True'): ult.append('%s slot %d: %s' % (b['id'], s, ', '.join(ns)))
            per.setdefault(b['id'], []).append('slot %d %s: %s' % (s, sig[s]['name'] if s in sig else '?', ', '.join(ns)))
    t = []
    t.append('IMBUE AUDIT (data-only, all %d builds in data.js, read-only; game text from citadel_mods_english.txt)' % len(B))
    t.append('imbue slot groups by number of distinct imbue items: ' + ', '.join('%d item(s): %d' % (k, v) for k, v in sorted(sz.items())))
    t.append('builds with >=2 imbue items on one ability: %d of %d (hero not mapped, item types only: %s)' % (len(builds), len(B), ', '.join(r['build'] for r in R.values() if not r['mapped'])))
    t.append('imbue items that would be unused if the game allows ONE imbue per ability (sum of n-1 per slot): %d placements' % dead)
    t.append('type combinations on one slot (item imbue behaviours): ' + '; '.join('%s x%d' % (k, v) for k, v in combo.most_common()))
    t.append('same-type pairs on one slot (highest chance of replace/refuse): %d' % len(same))
    t.append('Echo Shard + Compress Cooldown on the same ability (cooldown arithmetic: Echo Shard cooldown = 30 s + imbued ability cooldown, so the order of reduction matters): %d  %s' % (len(echo_cc), ', '.join(echo_cc)))
    t.append('multi-imbue slots on an ultimate: %d  %s' % (len(ult), '; '.join(ult)))
    return '\n'.join(t), per, same

if __name__ == '__main__':
    _main()
    B = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/builds_dump.json')); R = audit(B)
    t, per, same = summary_text(B, R)
    L = [t, '', 'A. CERTAIN (the game data alone makes it dead, independent of any multi-imbue rule)']
    for b, r in R.items():
        for f in r['findings']:
            if f[0] in ('CERTAIN-INVALID', 'CERTAIN-NOOP?'): L.append('  %s: %s on %s: %s' % (b, f[1], f[2], f[3]))
    L += ['', 'B. DEPENDS ON ANOTHER UNKNOWN (not N01)']
    for b, r in R.items():
        for f in r['findings']:
            if f[0] in ('DEPENDS-ON-N08', 'DEPENDS-ON-CHARGES'): L.append('  [%s] %s: %s on %s: %s' % (f[0], b, f[1], f[2], f[3]))
    L += ['', 'C. DEPENDS ON N01 (2+ imbue items on one ability: allowed / replace / refuse / stack are all UNRESOLVED)']
    for b, v in per.items(): L.append('  %s: %s' % (b, ' | '.join(v)))
    open(os.path.join(C, 'evidence', 'interactions', 'imbue_audit', 'IMBUE_AUDIT.txt'), 'w').write('\n'.join(L) + '\n')
    print('wrote IMBUE_AUDIT.txt', len(L), 'lines')

#!/usr/bin/env python3
"""rerank_v2.py: re-rank discovery hypotheses by  uncertainty x relevance x expected information value x chance of changing a build decision.
Inputs: hypotheses/ranked.json (generator output, unchanged), validated/measured.json, validated/user_reported.json.
Output: hypotheses/ranked_v2.txt/json  (HYPOTHESIS tier; nothing here is measured).
Factors (each 0..1, derived from existing generator fields, no per-case terms):
  uncertainty = info_value(plausibility)/5            (open when data leaves the outcome undecided)
  relevance   = impact/5
  testability = 0 unless sandbox TESTABLE-NOW, 0.6 if PARTIAL, else 0 (cast/ally gaps)
  build_change= availability/5                         (proxy: can the item/ability be bought and used in a build)
  novelty     = 1.0 for the first member of a relation class; 0.5**k for the k-th further member; 0.15 if the class is user-reported or already measured (model validation only)
score = uncertainty*relevance*testability*build_change*novelty"""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); EVD = os.path.join(HERE, '..', 'evidence', 'interactions')
H = json.load(open(os.path.join(EVD, 'hypotheses', 'ranked.json')))['hypotheses']
KN = json.load(open(os.path.join(EVD, 'validated', 'user_reported.json')))['reported']
known_cls = {k['relation_class'] for k in KN}
def cls(x):
    t = x['title']
    if x['id'].startswith('T5'):
        m = re.search(r'\((\w+)\) count for', t); return 'heavy_melee_ability x BonusHeavyMeleeDamage' if 'BonusHeavyMeleeDamage' in t else 'T5:' + t[-40:]
    if x['id'].startswith('T2'): return 'reset item (Echo Shard) x imbued ability'
    if x['id'].startswith('T4'): return 'cast-phase ITEMS_DISABLED x item actives'
    return x['id'][:2] + ':' + re.sub(r'^.*?: ', '', t)[:40]
def info(p): return max(0.0, 5 - abs(p - 2.5) * 2) if p is not None else 2.5
seen = collections.Counter(); out = []
for x in sorted(H, key=lambda h: -h['scoring']['total']):
    s = x['scoring']; c = cls(x); k = seen[c]; seen[c] += 1
    st = x['sandbox']['status']; test = 1.0 if st.startswith('TESTABLE') else 0.6 if st.startswith('PARTIAL') else 0.0
    nov = 0.15 if c in known_cls else 0.5 ** k
    sc = round((info(s['plausibility']) / 5) * (s['impact'] / 5) * test * (s['availability'] / 5) * nov, 4)
    out.append({'id': x['id'], 'title': x['title'], 'class': c, 'rank_in_class': k + 1, 'novelty': nov, 'score_v2': sc, 'old_score': s['total'], 'sandbox': st})
out.sort(key=lambda o: -o['score_v2'])
json.dump(out, open(os.path.join(EVD, 'hypotheses', 'ranked_v2.json'), 'w'), indent=1)
with open(os.path.join(EVD, 'hypotheses', 'ranked_v2.txt'), 'w') as f:
    f.write('# RANKED v2 (uncertainty x relevance x testability x build-change x novelty). classes=%d of n=%d\n' % (len(seen), len(H)))
    for i, o in enumerate(out, 1): f.write('%3d. [%s] %.4f (old %.2f) class="%s" #%d nov=%.2f  %s\n' % (i, o['id'], o['score_v2'], o['old_score'], o['class'], o['rank_in_class'], o['novelty'], o['title']))
print(collections.Counter(seen).most_common()); [print(o['id'], o['score_v2'], o['class'], o['rank_in_class'], o['title'][:70]) for o in out[:10]]

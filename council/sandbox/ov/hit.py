#!/usr/bin/env python3
"""hit.py damage.csv [prefix] : per-mark shots summary (player-attacker rows)"""
import csv,sys,collections
rows=list(csv.DictReader(open(sys.argv[1])))
pre=sys.argv[2] if len(sys.argv)>2 else ''
g=collections.OrderedDict()
for r in rows:
    if r['label'] in('MARK','DONE') : continue
    l=r['label']
    if not l.startswith(pre): continue
    d=g.setdefault(l,dict(hit=collections.Counter(),world=0,other=0))
    if r['attacker_team']=='2' and r['victim']=='"player"' or (r['attacker_team']=='2' and r['victim_team']=='3'):
        if r['ability']=='incoming': continue
        d['hit'][round(float(r['damage']),1)]+=1
    elif r['victim']=='worldent' or r['victim_team']=='0': d['world']+=1
for l,d in g.items():
    print(l,'hits',sum(d['hit'].values()),'world',d['world'],dict(sorted(d['hit'].items())))

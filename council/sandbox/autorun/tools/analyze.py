#!/usr/bin/env python3
"""analyze.py damage.csv samples.csv  -> per-label table: shots, dmg to enemy hero, dps, my healing (sum of hp rises), hps."""
import csv,sys,collections
dmg,smp=sys.argv[1],sys.argv[2]
lab=collections.OrderedDict()
def L(k):
    return lab.setdefault(k,dict(hits=0,dmg=0.0,world=0,t0=None,t1=None,heal=0.0,taken=0.0))
T0=int(next(csv.DictReader(open(smp)))['t_ms'])
for r in csv.DictReader(open(dmg)):
    if int(r['t_ms'])<T0: continue
    if r['label'] in ('MARK','DONE'): continue
    d=L(r['label'])
    if r['victim']=='player' and r['victim_team']=='3' and r['attacker_team']=='2':
        d['hits']+=1; d['dmg']+=float(r['damage'])
    elif r['victim']=='worldent': d['world']+=1
rows=list(csv.DictReader(open(smp)))
prev=None
for r in rows:
    if r['label'] in ('none','end') or not r['my_hp']: prev=None; continue
    t=int(r['t_ms']); hp=float(r['my_hp']); d=L(r['label'])
    d['t0']=t if d['t0'] is None else d['t0']; d['t1']=t
    if prev is not None and prev[0]==r['label']:
        dh=hp-prev[1]
        if dh>0: d['heal']+=dh
    prev=(r['label'],hp)
print(f"{'label':22}{'hits':>5}{'dmg':>8}{'secs':>6}{'dps':>7}{'heal':>8}{'hps':>7}{'heal/dmg':>9}")
for k,d in lab.items():
    if d['t0'] is None: continue
    s=(d['t1']-d['t0'])/1000 or 1
    print(f"{k:22}{d['hits']:>5}{d['dmg']:>8.0f}{s:>6.1f}{d['dmg']/s:>7.1f}{d['heal']:>8.0f}{d['heal']/s:>7.1f}{(d['heal']/d['dmg'] if d['dmg'] else 0):>9.2f}")

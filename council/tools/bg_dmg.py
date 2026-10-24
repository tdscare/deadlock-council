#!/usr/bin/env python3
"""bg_dmg.py damage.csv [labelSubstr ...] -> per label: bullets, bullet dmg/hit, proc rows, total dmg, dps (20 s from first bullet)"""
import csv,sys,collections
f=sys.argv[1]; subs=sys.argv[2:]
rows=list(csv.reader(open(f)))[1:]
by=collections.OrderedDict(); seg=0; prev=None
for r in rows:
    if r[1]!=prev:
        prev=r[1]; seg+=1
    if r[1]=='none' or r[2]=='none' or r[2]=='' or r[5]!='player' or r[6]!='2': continue
    by.setdefault((seg,r[1]),[]).append(r)
for (sg,l),R in by.items():
    if subs and not any(s in l for s in subs): continue
    b=[x for x in R if x[8]=='Bullet']; ab=[x for x in R if x[8]!='Bullet']
    if not b: continue
    t0=int(b[0][0]); inwin=[x for x in R if int(x[0])-t0<=20000]
    tot=sum(float(x[9]) for x in inwin)
    d=[float(x[9]) for x in b]
    print('%-34s bullets=%3d perHit=%.3f(min %.3f max %.3f) procRows=%3d total20s=%.0f dps=%.1f'%(l,len(b),sum(d)/len(d),min(d),max(d),len(ab),tot,tot/20))

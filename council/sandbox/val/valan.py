#!/usr/bin/env python3
"""valan.py <damage.csv> <plugin.log> [prefix]: per-label bullets (weapon rows on enemy team), worldent hits, VERIFY status."""
import csv,sys,re,collections,statistics as S
def load(dmg,log,prefix=''):
    rows=list(csv.DictReader(open(dmg)))
    B=collections.OrderedDict()
    for r in rows:
        l=r['label']
        if l in('MARK','DONE','none') or not l.startswith(prefix): continue
        b=B.setdefault(l,dict(w=[],world=0,other=collections.Counter(),t=[]))
        if r['attacker_team']=='2' and r['victim_team']=='3':
            if 'weapon' in r['ability']: b['w'].append(float(r['damage'])); b['t'].append(int(r['t_ms']))
            else: b['other'][r['ability']]+=float(r['damage'])
        elif r['victim_team']=='0' and 'weapon' in r['ability']: b['world']+=1
    V={}
    for ln in open(log,errors='ignore'):
        m=re.search(r'VERIFY (\S+) (PASS|FAIL[^|]*)\|?(.*)',ln)
        if m: V[m[1]]=(m[2].strip(),m[3].strip())
    return B,V
if __name__=='__main__':
    B,V=load(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else '')
    for l,b in B.items():
        w=b['w']; 
        cl=collections.Counter(round(x,1) for x in w)
        print(f"{l:28s} hits={len(w):3d} world={b['world']:3d} sum={sum(w):7.1f} vals={dict(cl.most_common(4))} {V.get(l,('NOVERIFY',''))[0]}")

import csv,sys,re,collections,statistics as S
def run(dmg,log,pfx='pw1'):
    rows=list(csv.DictReader(open(dmg)))
    marks={r['victim']:int(r['t_ms']) for r in rows if r['label']=='MARK' and r['victim'].startswith(pfx+'|')}
    V={}
    for ln in open(log,errors='ignore'):
        m=re.search(r'VERIFY ('+pfx+r'\|\S+) (PASS|FAIL)',ln)
        if m: V[m[1]]=m[2]
    out={}
    for nm,t0 in marks.items():
        w=[r for r in rows if r['label']==nm and r['attacker_team']=='2' and r['victim_team']=='3' and 'weapon' in r['ability']]
        ts0=min([int(r['t_ms']) for r in w] or [t0]); ts=[int(r['t_ms'])-ts0 for r in w]; d=[float(r['damage']) for r in w]
        tot=sum(x for t,x in zip(ts,d) if t<=20500); b3=sum(x for t,x in zip(ts,d) if t<=3500)
        n=sum(1 for t in ts if t<=20500)
        out[nm]=dict(dps=tot/20.0,b3=b3,n=n,per=(tot/n if n else 0),v=V.get(nm,'?'))
    return out
if __name__=='__main__':
    o=run(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else 'pw1')
    cells=collections.defaultdict(lambda:collections.defaultdict(list))
    for nm,v in sorted(o.items()):
        _,cp,cd,fa,rep,arm=nm.split('|')
        if arm=='warm': continue
        if v['v']!='PASS': print('INVALID',nm,v['v']); continue
        cells[(cp,cd,fa)][arm].append((rep,v))
    for k,c in sorted(cells.items()):
        A=[v for r,v in sorted(c['A'])];B=[v for r,v in sorted(c['B'])]
        n=min(len(A),len(B))
        if not n: continue
        for met in('dps','b3','n','per'):
            a=[x[met] for x in A[:n]];b=[x[met] for x in B[:n]]
            d=[(y-x)/x*100 for x,y in zip(a,b) if x]
            print(k,met,'A',round(S.mean(a),2),'B',round(S.mean(b),2),'B/A %+.1f%%'%(S.mean(d)),'sd %.1f'%(S.pstdev(d) if len(d)>1 else 0),'n',n)

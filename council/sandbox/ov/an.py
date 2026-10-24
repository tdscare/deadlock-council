#!/usr/bin/env python3
"""an.py <damage.csv> <plugin.log> [labelprefix] -> json blocks; library fn parse(dmg,log,prefix)"""
import csv,re,sys,json,collections,statistics as S
def parse(dmgs,log,prefix='',tmin=None):
    blocks={}
    # damage windows
    for dmg in dmgs:
        rows=list(csv.DictReader(open(dmg)))
        marks=[(int(r['t_ms']),r['label'] if r['label']!='MARK' else r['victim']) for r in rows if r['label'] in('MARK','DONE')]
        # MARK rows: label col 'MARK', victim holds name
        win={}
        for i,(t,nm) in enumerate(marks):
            if nm in('none',) or nm.startswith('ov_') : continue
            t1=marks[i+1][0] if i+1<len(marks) else t+60000
            win[nm]=(t,t1)
        for r in rows:
            if r['label'] in('MARK','DONE'): continue
            nm=r['label']
            if not nm.startswith(prefix) or nm=='none': continue
            b=blocks.setdefault(nm,dict(dealt=0.0,hits=0,taken=0.0,abil=collections.Counter(),typ=collections.Counter(),win=win.get(nm)))
            try: d=float(r['damage'])
            except: continue
            if r['attacker_team']=='2' and r['victim_team']=='3':
                b['dealt']+=d;b['hits']+=1;b['abil'][r['ability'].replace('citadel_ability_','')]+=d;b['typ'][r['dmg_type']]+=d
            elif r['victim_team']=='2' and r['attacker_team']=='3':
                b['taken']+=d
    cur=None
    for ln in open(log,errors='ignore'):
        m=re.search(r'SC ITEMS@(\S+):',ln)
        if m: cur=m.group(1); continue
        m=re.search(r'SC TRK heal=(\d+) loss=(\d+) minHp=(\d+) floorHits=(\d+) firstFloorMs=(-?\d+) secs=([\d.]+) maxhp=(\d+)',ln)
        if m and cur and cur in blocks:
            b=blocks[cur]
            if 'secs' in b: continue   # first TRK after mark only
            b.update(heal=int(m[1]),loss=int(m[2]),minhp=int(m[3]),floor=int(m[4]),firstfloor=int(m[5])/1000,secs=float(m[6]),maxhp=int(m[7]))
    out={}
    for k,b in blocks.items():
        if 'secs' not in b: continue
        s=max(b['secs'],0.1)
        out[k]=dict(dps=b['dealt']/s,hps=b['heal']/s,lps=b['loss']/s,secs=s,maxhp=b['maxhp'],minhp=b['minhp'],floor=b['floor'],firstfloor=b['firstfloor'],hits=b['hits'],
                    abil={a:round(v/s,1) for a,v in b['abil'].most_common(6)},typ={a:round(v/s,1) for a,v in b['typ'].items()})
    return out
def agg(out):
    """label build|cp|cond|rN|variant -> grouped stats"""
    g=collections.defaultdict(list)
    for k,v in out.items():
        p=k.split('|')
        if len(p)<5 or p[4]=='warm': continue
        g[(p[0],p[1],p[2],p[4])].append((int(p[3][1:]),v))
    res={}
    for key,l in g.items():
        l.sort()
        def ms(f):
            xs=[x[1][f] for x in l]
            return (S.mean(xs),S.pstdev(xs) if len(xs)>1 else 0.0,xs)
        res[key]=dict(n=len(l),dps=ms('dps'),hps=ms('hps'),lps=ms('lps'),maxhp=ms('maxhp'),minhp=ms('minhp'),floor=ms('floor'),abil=l[0][1]['abil'])
    return res
if __name__=='__main__':
    out=parse(sys.argv[1].split(','),sys.argv[2],sys.argv[3] if len(sys.argv)>3 else '')
    json.dump(out,open('/dev/stdout','w'),indent=1)

#!/usr/bin/env python3
"""valgen.py: fixed validation suite scenarios (Haze player vs Haze bot, arena). Writes to OUT."""
import sys
OUT='/mnt/user-data/outputs/arena/sc/'
HEAD=['hardreset','raw citadel_unlock_flex_slots','aimoff 0 0','setgold 0','wait 0.4']
def setup(items=(),lvl=18,res=(0,0),dist=150,aim=(-33,-30),acc=None,label='x'):
    o=list(HEAD)
    for it in items: o.append(f'give {it}')
    o+=['wait 0.8',f'lvlhold {lvl}','wait 1.2','nw','egod',f'eresist gun {res[0]}',f'eresist spirit {res[1]}',f'aimpt {aim[0]} {aim[1]}']
    o+=['accoff'] if acc is None else ([f'accseed {acc[2]}'] if len(acc)>2 else ['accseed 0'])+[f'accuracy {acc[0]} {acc[1]} 25 60']
    o+=['wait 0.8','heal',f'fetch {dist}','wait 0.8','healreset',f'mark {label}','pos',
        f"expect hero=Haze level={lvl} items={len(items)} gold=0 dist={dist} enemies=1 resgun={res[0]} resspirit={res[1]} cdready=1"]
    return o
def fire(n=2,s=2.6):
    o=[]
    for _ in range(n): o+=['cast reload 2.3',f'fire {s}','wait 0.3']
    return o
def blk(label,**kw):
    fkw={k:kw.pop(k) for k in ('n','s') if k in kw}
    return setup(label=label,**kw)+fire(**fkw)+['mark none','acclog','wait 0.5']
def ka():
    L=['setup Haze Haze','basemods','mark none']
    L+=blk('KA|body|r0',aim=(-33,-30))
    L+=blk('KA|head|r0',aim=(-33,-5))
    L+=blk('KA|body|res20',aim=(-33,-30),res=(20,0))
    L+=blk('KA|head|res20',aim=(-33,-5),res=(20,0))
    for d in (300,500,600,650,700,750,850,1100):
        L+=blk(f'KA|CQ|body|{d}',items=['upgrade_close_range'],aim=(-33,-30),dist=d,n=1,s=2.6)
    L+=blk('KA|none|body|300',aim=(-33,-30),dist=300,n=1,s=2.6)
    L+=blk('KA|none|body|900',aim=(-33,-30),dist=900,n=1,s=2.6)
    L+=['end']; return L
def aa(nrep=4,pairs=True):
    """A/A noise (identical, accuracy mix) + order test A,B,B,A where B = Close Quarters (+20% known)"""
    L=['setup Haze Haze','basemods','mark none']
    for i in range(nrep):
        L+=blk(f'AA|none|{i+1}',acc=(0.45,0.25),n=3,s=2.6)
    for i,v in enumerate(['A','B','B','A','B','A','A','B']):
        L+=blk(f'ORD|{v}|{i+1}',acc=(0.45,0.25),n=3,s=2.6,items=['upgrade_close_range'] if v=='B' else [])
    L+=['end']; return L
def aa2():
    L=['setup Haze Haze','basemods','mark none']
    for seed in (11,12,13):
        for k,v in enumerate(('A','A','B','B')):
            L+=blk(f'S{seed}|{v}|{k}',acc=(0.55,0.25,seed),n=3,s=2.6,items=['upgrade_close_range'] if v=='B' else [])
    L+=['end']; return L
if __name__=='__main__':
    open(OUT+'val_aa2.txt','w').write('\n'.join(aa2())+'\n'); open(OUT+'q_val_aa2.txt','w').write('sbx_scenario val_aa2\n')
    for n,f in (('val_ka',ka),('val_aa',aa)):
        open(OUT+n+'.txt','w').write('\n'.join(f())+'\n')
        open(OUT+'q_'+n+'.txt','w').write(f'sbx_scenario {n}\n')
    print('ok')

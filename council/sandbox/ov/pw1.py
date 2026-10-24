import ovlib as O,random
OUT='/mnt/user-data/outputs/arena/sc'
O.HEADFRAC=0.0
O.RES[16800]=(12,4); O.RES[5600]=(5,0)
O.COND['g100']=dict(n=1,acc=1.0,gun=0,sp=0,hp=100,floor=0)
O.COND['g60']=dict(n=1,acc=0.6,gun=0,sp=0,hp=100,floor=0)
b=dict(O.BLD['wraith']); b['id']='wraith'
I5A=['Swift Striker','Tesla Bullets']; I5B=['Titanic Magazine','Tesla Bullets']
I17A=['Swift Striker','Tesla Bullets','Monster Rounds','Quicksilver Reload','Surge of Power','Ricochet']
I17B=[('Titanic Magazine' if x=='Swift Striker' else x) for x in I17A]
def its(names): return [(n,'1' if n in('Quicksilver Reload',) else '') for n in names]
ARMS={5600:{'A':its(I5A),'B':its(I5B)},16800:{'A':its(I17A),'B':its(I17B)}}
CELLS=[(5600,'g100',0),(5600,'g60',0),(5600,'g100',1),(16800,'g100',0),(16800,'g60',0),(16800,'g100',1)]
def rot(fa): return dict(dist=350,opener=(['cast 3 0.2'] if fa else []),loop=['fire 20'],loops=1,late=[])
def gen(reps=4,tag='pw1'):
    names=[]
    for rep in range(1,reps+1):
        cells=CELLS[:] if rep%2 else CELLS[::-1]
        L=['lvlhold 0',f'setup Wraith Haze','raw citadel_unlock_flex_slots','basemods','mark none','egod']
        cp,cd,fa=cells[0]
        L+=O.block(b,cp,cd,f'pw1|{cp}|{cd}|fa{fa}|r{rep}|warm',rot(fa),ARMS[cp]['A'],seed=rep)
        for cp,cd,fa in cells:
            vs=['A','B'] if rep%2 else ['B','A']
            for v in vs:
                L+=O.block(b,cp,cd,f'pw1|{cp}|{cd}|fa{fa}|r{rep}|{v}',rot(fa),ARMS[cp][v],seed=rep)
        nm=f'{tag}_r{rep}'
        if rep<reps: L.append(f'include {tag}_r{rep+1}')
        L.append('end'); open(f'{OUT}/{nm}.txt','w').write('\n'.join(L)+'\n'); names.append(nm)
    open(f'{OUT}/q_{tag}.txt','w').write(f'sbx_scenario {names[0]}\n'); return names
if __name__=='__main__': print(gen())

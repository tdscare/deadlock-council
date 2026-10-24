import sys,ovlib as O,rots,os
OUT='/mnt/user-data/outputs/arena/sc'
def gen(bid,tag,cps=None,conds=None,reps=3,variants=None,rotkey=None):
    b=dict(O.BLD[bid]); b['id']=bid+'.'+tag; rot=rots.ROT[rotkey or bid]
    cps=cps or O.CP; conds=conds or ['duel100','duel45','group45']
    f=O.file_for(b,cps,conds,rot,reps=reps,variants=variants)
    names=[]
    for r in range(1,reps+1):
        L=['lvlhold 0']+f[r]
        nm=f'sbxA_{tag}_r{r}'
        if r<reps: L.append(f'include sbxA_{tag}_r{r+1}')
        L.append('end')
        open(f'{OUT}/{nm}.txt','w').write('\n'.join(L)+'\n'); names.append(nm)
    open(f'{OUT}/q_{tag}.txt','w').write(f'sbx_scenario {names[0]}\n')
    return names
if __name__=='__main__':
    print(gen(sys.argv[1],sys.argv[2]))

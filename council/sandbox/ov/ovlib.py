#!/usr/bin/env python3
"""ovlib: overnight sandbox generator + analyzer helpers."""
import json,re,random,os,csv,collections
SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad'
IT=json.load(open(f'{SP}/audit/items_full.json'))
BLD={b['id']:b for b in json.load(open(f'{SP}/council/sandbox/builds_ov.json'))}
COST={1:800,2:1600,3:3200,4:6400}
ENUM={}
for l in open(f'{SP}/council/sandbox/hero_enum.txt'):
    if '=' in l:
        a,b=l.split('='); ENUM[a.strip().lower()]=a.strip()
LV=[0,800,1100,1500,2000,2600,3200,3800,4500,5200,5900,6600,7400,8200,9000,9800,10700,11600,12500,13400,14400,15500,16700,18000,19500,21200,23100,25200,27500,30000,32700,35600,38700,42000,45500,49200]
AP=[0,1,1,2,2,3,4,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
UNL=[0,1,2,2,3,3,3,4]+[4]*28
def level_for(souls):
    L=0
    for i,t in enumerate(LV):
        if souls>=t: L=i
    return L
def hero_enum(b):
    k=b['hk'].replace('hero_','').lower()
    return ENUM.get(k)
def core_items(b):
    out=[]
    for c in b['core']:
        for i in c['items']: out.append((i['n'],i['imb']))
    return out
def cost_walk(b,budget):
    """items bought strictly left-to-right under budget; returns owned final items [(name,imb)] and spent"""
    owned=[];own_set={};spent=0
    for n,imb in core_items(b):
        g=IT[n];c=COST[g['tier']]
        comp=[k for k in g['components'] if k in own_set]
        add=c-sum(COST[IT[k]['tier']] for k in comp)
        if spent+add>budget: break
        spent+=add
        for k in comp: 
            if not imb: imb=own_set[k] or ''
            owned=[x for x in owned if x[0]!=k]; own_set.pop(k)
        owned.append((n,imb)); own_set[n]=imb
    return owned,spent
def ability_bits(b,level):
    """sequential spend of order list under AP/unlock budgets -> bits for abilities 1..4"""
    ap=AP[level]; unl=UNL[min(level,len(UNL)-1)]
    cnt=[0,0,0,0]; used_unl=0; bits=[0,0,0,0]
    for a in b['order']:
        a-=1; k=cnt[a]
        if k==0:
            if used_unl>=unl: break
            used_unl+=1; cnt[a]=1; bits[a]=1   # UpgradeBits: bit0=unlocked, +T1=3, +T2=7, +T3=15 (FOUNDATIONS.md; verify with bitstest)
        else:
            cost={1:1,2:2,3:5}.get(k)
            if cost is None or ap<cost: break
            ap-=cost; cnt[a]+=1; bits[a]=[1,3,7,15][min(cnt[a]-1,3)]
    return bits

# ---------------------------------------------------------------- generator
USE_FIRST=['Surge of Power','Arcane Surge','Focus Lens','Alchemical Fire','Mercurial Magnum','Vampiric Burst','Infuser','Colossus','Cursed Relic','Silence Wave','Escalating Exposure','Mystic Vulnerability']
USE_LATE=['Echo Shard','Refresher']
CP=[5000,10000,18000,24000,30000,'full']
def cp_name(cp): return 'full' if cp=='full' else f'{cp//1000}k'
def cp_level(cp): return 35 if cp=='full' else level_for(cp)
# assumed enemy resists per checkpoint (bullet%, spirit%)
RES={5000:(5,0),10000:(8,0),18000:(15,8),24000:(20,12),30000:(25,18),'full':(30,22)}
COND={
 'duel100':dict(n=1,acc=1.0,gun=0,sp=0,hp=100,floor=0),
 'duel45': dict(n=1,acc=0.45,gun=4.0,sp=2.0,hp=50,floor=8),
 'group45':dict(n=4,acc=0.45,gun=8.0,sp=4.0,hp=50,floor=8),
 'lowhp':  dict(n=1,acc=0.45,gun=3.0,sp=1.5,hp=25,floor=5),
}
HEADFRAC=0.25   # share of landed gun hits that are headshots (high-rank assumption)
AIMR,AIMBODY,HEADUP=-33,-30,25   # calibrated aim point (units): lateral, chest height, extra up for head
def cls(n): return IT[n]['class']
def final_items(b,cp):
    ow,_=cost_walk(b,10**9 if cp=='full' else cp)
    # cap 12: drop earliest lowest tier
    while len(ow)>12:
        i=min(range(len(ow)),key=lambda k:(IT[ow[k][0]]['tier'],k)); ow.pop(i)
    return ow
def expand_rot(rot,items,dist):
    names=[n for n,_ in items]
    out=[]
    for l in rot:
        if l=='@ACTS':
            for n in USE_FIRST:
                if n in names: out.append(f'use {cls(n)} 0.45')
        elif l=='@LATE':
            for n in USE_LATE:
                if n in names: out.append(f'use {cls(n)} 0.45')
        elif l.startswith('@F'):
            out.append(f'fetch {l.split()[1] if len(l.split())>1 else dist}')
        else: out.append(l)
    return out
def block(b,cp,cond,label,rot_def,items=None,aim=None,warm=False,seed=1):
    c=COND[cond]; L=cp_level(cp)
    items=items if items is not None else final_items(b,cp)
    bits=ability_bits(b,L)
    rg,rs=RES[cp]
    o=['hardreset','raw citadel_unlock_flex_slots','aimoff 0 0','setgold 0','wait 0.4']
    for n,imb in items:
        if imb and IT[n]['tier']<=2: o.append(f'imbue {cls(n)} Signature{imb}')   # base items: explicit slot (verified Success)
        else: o.append(f'give {cls(n)}')   # upgrades: ItemNotImbuable via imbue; give applies to Signature1 (verified, only valid when imb==1)
    o+=['wait 0.8',f'lvlhold {L}','wait 1.2',f'abil {bits[0]} {bits[1]} {bits[2]} {bits[3]}','abilist','nw','egod']
    o+=[f'eresist gun {rg}',f'eresist spirit {rs}',f'aimpt {AIMR} {AIMBODY}']
    if c['n']>1: o.append(f"enemies {c['n']} 220 3")
    o+=[f"accseed {seed}",f"accuracy {c['acc']} {HEADFRAC} {HEADUP} 60",'wait 1','heal',f"hp {c['hp']}",'fetch '+str(rot_def['dist']),'wait 0.5']
    if c['floor']: o.append(f"floor {c['floor']}")
    o+=['healreset',f'mark {label}','pos',f"expect hero={hero_enum(b)} level={L} items={len(items)} bits={bits[0]},{bits[1]},{bits[2]},{bits[3]} gold=0 dist={rot_def['dist']} enemies={c['n']} mindist={100 if c['n']>1 else 40} resgun={rg} resspirit={rs} cdready=1"]
    if c['gun'] or c['sp']:
        o+= ['inhit 35 150',f"incoming gunpct {c['gun']}", f"incoming spiritpct {c['sp']}"]
    o+=expand_rot(rot_def['opener'],items,rot_def['dist'])
    for _ in range(rot_def['loops']): o+=expand_rot(rot_def['loop'],items,rot_def['dist'])
    o+=expand_rot(rot_def.get('late',[]),items,rot_def['dist'])
    o+=['incoming off','inhit 0 0','floor 0','healsum','acclog','wait 2.5','mark none','lvlhold 0']
    if c['n']>1: o.append('enemies 1')
    return o
HPBASE={}
def est_maxhp(b,L):
    base=HPBASE.get(b['id'],(800,45))
    return base[0]+base[1]*L
def file_for(b,cp_list,conds,rot_def,reps=3,seed=1,tag='base',variants=None):
    """variants: optional list of (vname, items_override_fn(cp)->items) ; returns dict rep-> lines, and block list"""
    import random as R
    r=R.Random(seed)
    files={}
    for rep in range(1,reps+1):
        if rep==1: order=[(cp,cd) for cp in cp_list for cd in conds]
        elif rep==2: order=[(cp,cd) for cp in cp_list[::-1] for cd in conds[::-1]]
        else:
            order=[(cp,cd) for cp in cp_list for cd in conds]; r.shuffle(order)
        lines=[f"setup {hero_enum(b)} Haze",'raw citadel_unlock_flex_slots','basemods','mark none','egod']
        # warm-up block = copy of the first block, label warm (discard)
        cp0,cd0=order[0]
        lines+=block(b,cp0,cd0,f'{b["id"]}|{cp_name(cp0)}|{cd0}|r{rep}|warm',rot_def,seed=rep)
        for cp,cd in order:
            vs=variants or [('built',None)]
            if rep%2==0: vs=vs[::-1]
            for vn,fn in vs:
                items=fn(cp) if fn else None
                lines+=block(b,cp,cd,f'{b["id"]}|{cp_name(cp)}|{cd}|r{rep}|{vn}',rot_def,items,seed=rep)
        lines.append('mark none')
        files[rep]=lines
    return files

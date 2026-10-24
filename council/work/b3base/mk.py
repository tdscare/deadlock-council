import json,copy,sys
B='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/council/work/'
def load(i): return json.load(open(B+'b3base/base_'+i+'.json'))
def find(b,name):
    for r in b['rows']:
        for bx in r:
            for it in bx[3]:
                if it[0]==name: return bx,it
    return None,None
def remove(b,name):
    bx,it=find(b,name); bx[3].remove(it)
def box(b,title):
    for r in b['rows']:
        for bx in r:
            if bx[0]==title: return bx
def save(b,out):
    b['rows']=[[bx for bx in r if bx[3] or bx[0].startswith('Lost')] for r in b['rows']]
    b['rows']=[r for r in b['rows'] if r]
    open(B+out+'.js','w').write(json.dumps(b,indent=1,ensure_ascii=False)+'\n')

# 1 Mo & Krill for Bebop
b=load('mokrill'); b['id']='mokrill_duo_bebophook'; b['name']="Rizuhble's Grab And Go Mo"; b['desc']='Duo Mo for Bebop'
b['order']=[1,1,3,2,1,2,4,4,2,4,4,2,1,3,3,3]
bx,it=find(b,'Colossus'); i=bx[3].index(it); bx[3][i]=['Spirit Burn','Sell Healbane for this.']
remove(b,'Spirit Burn') if False else None
rb=box(b,"I'm rich as fuck"); rb[3]=[x for x in rb[3] if x[0]!='Spirit Burn']
b['changes']=b.get('changes',[])+['DUO3 (Bebop): see council/evidence/duo/designs_batch3.json pair B3-1.']
save(b,'mokrill_duo_bebophook')

# 2 Bebop (bomb) for Mo
b=load('bebop_bomb'); b['id']='bebop_duo_mohook'; b['name']="Rizuhble's Tow Truck Bebop"; b['desc']='Duo Bebop for Mo & Krill'
b['order']=[2,2,3,1,2,4,4,3,3,4,3,2,4,1,1,1]
b['changes']=b.get('changes',[])+['DUO3 (Mo & Krill): see designs_batch3.json pair B3-1.']
save(b,'bebop_duo_mohook')

# 3 Doorman for Venator / Graves
b=load('doorman'); b['id']='doorman_duo_push'; b['name']="Rizuhble's Room Service Doorman"; b['desc']='Duo Doorman for Venator or Graves'
bx,it=find(b,'Compress Cooldown'); it[1]='On Luggage Cart.'; it[2]='3'
b['order']=[1,1,3,2,1,3,4,2,3,3,2,1,4,4,4,2]
b['changes']=b.get('changes',[])+['DUO3 (Venator, Graves): see designs_batch3.json pairs B3-2, B3-3.']
save(b,'doorman_duo_push')

# 4 Venator for Doorman
b=load('venator'); b['id']='venator_duo_doorman'; b['name']="Rizuhble's Doorstop Venator"; b['desc']='Duo Venator for Doorman'
bx,it=find(b,'Warp Stone'); i=bx[3].index(it); bx[3][i]=['Duration Extender','On Hex-Lined Snap Trap.','3']
lb=box(b,'Late · L-R'); lb[3].append(['Superior Duration',''])
rb=box(b,"I'm rich as fuck"); rb[3]=[x for x in rb[3] if x[0]!='Phantom Strike']
b['order']=[2,2,3,1,2,4,3,2,3,4,4,1,3,4,1,1]
b['changes']=b.get('changes',[])+['DUO3 (Doorman): see designs_batch3.json pair B3-2.']
save(b,'venator_duo_doorman')

# 5 Graves for Doorman
b=load('graves_ult'); b['id']='graves_duo_doorman'; b['name']="Rizuhble's Dead End Graves"; b['desc']='Duo Graves for Doorman'
bx,it=find(b,'Duration Extender'); it[1]='On Grasping Hands.'; it[2]='2'
b['order']=[1,1,2,3,4,4,4,2,2,2,4,3,1,1,3,3]
b['changes']=b.get('changes',[])+['DUO3 (Doorman): see designs_batch3.json pair B3-3.']
save(b,'graves_duo_doorman')

# 6 Pocket for Shiv
b=load('pocket'); b['id']='pocket_duo_shiv'; b['name']="Rizuhble's Softening Up Pocket"; b['desc']='Duo Pocket for Shiv'
bx,it=find(b,'Mystic Expansion'); it[1]='On Affliction.'; it[2]='4'
b['order']=[2,2,3,3,1,3,4,4,4,1,4,1,1,2,2,3]
b['changes']=b.get('changes',[])+['DUO3 (Shiv): see designs_batch3.json pair B3-4.']
save(b,'pocket_duo_shiv')

# 7 Shiv for Pocket
b=load('shiv'); b['id']='shiv_duo_pocket'; b['name']="Rizuhble's Clean Up Crew Shiv"; b['desc']='Duo Shiv for Pocket'
b['order']=[1,1,2,2,3,1,4,3,4,4,4,2,2,1,3,3]
b['changes']=b.get('changes',[])+['DUO3 (Pocket): see designs_batch3.json pair B3-4.']
save(b,'shiv_duo_pocket')

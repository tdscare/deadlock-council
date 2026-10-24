# whole-path comparison at checkpoints (section N). usage: python3 -I cmp.py <out> <label>=<build.json>[@order] ...
import sys,os,json,re; sys.path.insert(0,'/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/council/tools'); import abtimeline as T
SPD='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad'
t=open(T.SC+'heroes.vdata').read()
def armor_tab(hk):
    b=T.block('heroes.vdata',hk) or ''; k=b.find('m_MapModCostBonuses')
    if k<0: b=T.block('heroes.vdata','hero_base'); k=b.find('m_MapModCostBonuses')
    a=b.find('EItemSlotType_Armor',k); return [(int(x),float(y)) for x,y in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)',b[a:b.find(']',a)])]
CK=[int(x) for x in os.environ.get('CK','2400,4000,5600,7200,8800,10400,12000,13600,16000,19200,24000,28800,33600,40000').split(',')]
out=[]
for arg in sys.argv[2:]:
    lab,rest=arg.split('=',1); f,_,o=rest.partition('@'); b=json.load(open(f)); order=[int(c) for c in o] if o else None
    R=T.analyse(b,order); AT=armor_tab(b['hk'])
    out.append(f"## {lab} ({f.split('/')[-1]}{' order '+o if o else ''})")
    out.append("souls | last buy | inv g/s/v | wpn% spiritPow(no-dash) vit% | itemHP | PS chain dmg (tier) | storm DPS (tier) | ball DPS")
    for s in CK:
        w=[x for x in R['rows'] if not x.get('unknown') and x['souls']<=s]
        if not w: continue
        w=T.state(R,dict(w[-1],souls=s)); own=w['own']
        inv=lambda sl: sum(T.SOULS[i['tier']] for i in own if i['slot']==sl)
        vb=max([bo for th,bo in AT if inv('Armor')>=th] or [0]); hp=sum(T.sv(i,'BonusHealth') for i in own)
        def hit(sl,key):
            tt=w['tA'][sl]
            if tt<0: return 'locked'
            P=T.at_tier(R['abil'][sl],tt); h=T.spirit_hits(P,T.slot_sp(R,w,sl,tt)); h2=T.spirit_hits(P,T.slot_sp(R,w,sl,tt,cond=False))
            v=[val for k,(val,inst) in h.items() if key in k]; v2=[val for k,(val,inst) in h2.items() if key in k]
            return f"{max(v):.0f}/{max(v2):.0f} ({T.tlabel(tt)})" if v else T.tlabel(tt)
        out.append(f"{s:>6} | {w['n'][:20]:20} | {inv('WeaponMod')}/{inv('Tech')}/{inv('Armor')} | {w['wb']:.0f} {w['sp']:.0f}({w['sp_unc']:.0f}) {vb:.0f} | {hp:.0f} | {hit(3,'DamagePerChain')} | {hit(4,'DPS')} | {hit(1,'DPS')}")
open(sys.argv[1],'w').write('\n'.join(out)+'\n'); print('\n'.join(out))

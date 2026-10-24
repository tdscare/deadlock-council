# Seven path metrics per checkpoint (section N). CALCULATED, kit/item data only (6801 files = 6819 stats).
# HP = (730 + 41*boons) * (1 + vitality-invest %/100) + item BonusHealth (Cultist's +4/boon ignored)  [heroes.vdata; LOC Citadel_Hero_Stats_Tooltip_HealthMult]
# gun: 3-round burst, 10.8 (+0.24/boon) per bullet, cycle 0.2625 s, mag 29, reload 2.35 s; weapon % = weapon invest bonus + BaseAttackDamagePercent; fire rate = always-on BonusFireRate
#      (+ Surge of Power 20% for 8 s after casting the imbued ability, applied inside the Power Surge window only). Spiritual Overflow's fire rate needs build-up: excluded (conditional).
# Power Surge: one proc per burst on the target (LOC "Occurs once per burst shot"), primary hit = DamagePerChain at the slot's spirit (incl. imbues); bounces not counted.
#      ChainTickRate 0.2 s may cap procs at 5/s: UNVERIFIED; capped value shown when it binds. Window = AbilityDuration x (1 + Duration Extender 22% if imbued on it).
# HERO=1: add Burst Fire's ActivatedFireRate (on hero hit, 4.5 s) as if always up in a fight against heroes.
# Window also x(1 + Superior Duration 28%) when owned (global duration; additive vs multiplicative with the imbue UNVERIFIED, multiplicative used).
# usage: python3 -I m7.py <out> <label>=<build.json>[@order] ...
import sys,os,json,re; sys.path.insert(0,'/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/council/tools'); import abtimeline as T
def tab(hk,slot):
    b=T.block('heroes.vdata',hk); k=b.find('m_MapModCostBonuses'); a=b.find(slot,k)
    return [(int(x),float(y)) for x,y in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)',b[a:b.find(']',a)])]
CK=[int(x) for x in os.environ.get('CK','3200,4800,5600,7200,8800,10400,12000,13600,16000,19200,24000,28800,33600,40000,44800').split(',')]
EXCL_FR={'upgrade_tech_overflow','upgrade_magic_storm'}
out=[]
for arg in sys.argv[2:]:
    lab,rest=arg.split('=',1); f,_,o=rest.partition('@'); b=json.load(open(f)); order=[int(c) for c in o] if o else None
    R=T.analyse(b,order); AT=tab(b['hk'],'EItemSlotType_Armor')
    out.append(f"## {lab} ({os.path.basename(f)}{' order '+o if o else ''})")
    out.append("souls | last buy | inv g/s/v | HP | wpn% fr% | gun DPS sust | PS tier dmg/proc(no-dash) | PS window s | gun+PS dmg in window (cap) | storm DPS")
    for s in CK:
        w=[x for x in R['rows'] if not x.get('unknown') and x['souls']<=s]
        if not w: continue
        w=T.state(R,dict(w[-1],souls=s)); own=w['own']
        inv=lambda sl: sum(T.SOULS[i['tier']] for i in own if i['slot']==sl)
        vb=max([bo for th,bo in AT if inv('Armor')>=th] or [0]); hp=(730+41*w['boons'])*(1+vb/100)+sum(T.sv(i,'BonusHealth') for i in own)
        wp=w['wb']+sum(T.sv(i,'BaseAttackDamagePercent') for i in own)
        fr=sum(T.sv(i,'BonusFireRate')+(T.sv(i,'ActivatedFireRate') if os.environ.get('HERO')=='1' else 0) for i in own if i['class'] not in EXCL_FR)
        per_b=3*(10.8+0.24*w['boons'])*(1+wp/100)
        def dps(frx):
            cyc=0.2625/(1+frx/100); mag_t=9.67*cyc; return per_b/cyc*mag_t/(mag_t+2.35), 1/cyc*mag_t/(mag_t+2.35)
        g,_=dps(fr)
        t3=w['tA'][3]; pss='locked'; win=''; tot=''
        if t3>=0:
            P=T.at_tier(R['abil'][3],t3); h=T.spirit_hits(P,T.slot_sp(R,w,3,t3)); h2=T.spirit_hits(P,T.slot_sp(R,w,3,t3,cond=False))
            d=h['DamagePerChain'][0]; d2=h2['DamagePerChain'][0]
            dur=T.pv(P,'AbilityDuration')*(1+sum(T.sv(T.item(n),'BonusAbilityDurationPercent') for n,sl in w['imbues'].items() if sl==3 and n=='Duration Extender')/100)*(1+sum(T.sv(i,'BonusAbilityDurationPercent') for i in own if i['class']=='upgrade_imbued_duration_extender')/100)
            sop=any(n=='Surge of Power' and sl==3 for n,sl in w['imbues'].items())
            t8=min(8,dur) if sop else 0
            gA,pA=dps(fr+20); gB,pB=dps(fr)
            dmg=t8*(gA+pA*d2)+(dur-t8)*(gB+pB*d2)
            capA=min(pA,5); capB=min(pB,5); dmgc=t8*(gA+capA*d2)+(dur-t8)*(gB+capB*d2)
            pss=f"{T.tlabel(t3)} {d:.0f}({d2:.0f})"; win=f"{dur:.1f}"; tot=f"{dmg:.0f}"+(f" ({dmgc:.0f})" if abs(dmgc-dmg)>1 else '')
        t4=w['tA'][4]; st='locked'
        if t4>=0:
            P=T.at_tier(R['abil'][4],t4); h=T.spirit_hits(P,T.slot_sp(R,w,4,t4,cond=False)); st=f"{h['DPS'][0]:.0f}" if 'DPS' in h else '?'
        out.append(f"{s:>6} | {w['n'][:19]:19} | {inv('WeaponMod')}/{inv('Tech')}/{inv('Armor')} | {hp:.0f} | {wp:.0f} {fr:.0f} | {g:.0f} | {pss} | {win} | {tot} | {st}")
open(sys.argv[1],'w').write('\n'.join(out)+'\n'); print('\n'.join(out))

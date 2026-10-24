import json,re
I=json.load(open('audit/items_full.json'))
T={}
for n,it in I.items():
    if it['disabled']: continue
    s=it['stats']; d=(it['desc'] or '').lower(); t=[]
    ks=' '.join(s.keys())
    if 'HeadShot' in ks or 'headshot' in d: t.append('HEADSHOT')
    if 'AttackRange' in ks or 'LongRange' in ks: t.append('RANGE')
    if 'CloseRange' in ks: t.append('CLOSE')
    if 'BulletSpeed' in ks: t.append('BULLETSPEED')
    if 'FireRate' in ks: t.append('FIRERATE')
    if 'ClipSize' in ks: t.append('CLIP')
    if 'BaseAttackDamagePercent' in s and s['BaseAttackDamagePercent'] not in ('','0'): t.append('WDMG%'+s['BaseAttackDamagePercent'])
    if re.search(r'bullet|shoot|shot',d) or 'Proc' in ks and it['slot']=='WeaponMod': t.append('BULLETPROC')
    if 'Melee' in ks or 'melee' in d: t.append('MELEE')
    if 'Charge' in ks and 'AbilityCharge' in ks or 'charge' in d: t.append('CHARGE?')
    if 'TechPower' in ks or 'BonusSpirit' in ks: t.append('SPIRIT')
    T[n]=(it['tier'],it['slot'],t)
json.dump(T,open('council/apply/rel/itemtags.json','w'))
for n,(ti,sl,t) in sorted(T.items(),key=lambda x:(x[1][1],x[1][0])): print(ti,sl,n,':',' '.join(t))

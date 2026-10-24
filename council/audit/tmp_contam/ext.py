import re,json
V=open('gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata',encoding='utf-8',errors='ignore').read()
hs=[(m.group(1),m.start()) for m in re.finditer(r'^\t(hero_[a-z0-9_]+) =\s*\n',V,re.M)]
out={}
for i,(k,s) in enumerate(hs):
    e=hs[i+1][1] if i+1<len(hs) else len(V); b=V[s:e]
    d={}
    m=re.search(r'm_mapStartingStats =\s*\{(.*?)\n\t\t\}',b,re.S)
    if m: d['start']={a:float(v) for a,v in re.findall(r'(\w+) = ([-0-9.]+)',m.group(1))}
    m=re.search(r'm_mapStandardLevelUpUpgrades =\s*\{(.*?)\n\t\t\}',b,re.S)
    if m: d['lvl']={a:float(v) for a,v in re.findall(r'(\w+) = ([-0-9.]+)',m.group(1))}
    d['dis']=bool(re.search(r'm_bDisabled = true',b)); d['dev']=bool(re.search(r'm_bInDevelopment = true',b))
    lv=re.findall(r'"(\d+)" =\s*\{\s*m_unRequiredGold = (\d+)(.*?)\n\t\t\t\}',b,re.S)
    d['levels']=[(int(a),int(g),('std' if 'm_bUseStandardUpgrade = true' in r else ''),re.findall(r'(EAbility\w+) = (\d+)',r)) for a,g,r in lv]
    out[k]=d
json.dump(out,open('council/audit/tmp_contam/heroes_gd.json','w'))
import collections
print(len(out))
for k,d in out.items():
    if 'lvl' not in d: print('nolvl',k,d['dis'],d['dev']); continue
    l=d['lvl'];print(k.ljust(22),d['dis'],d['dev'],'sp',l.get('MODIFIER_VALUE_TECH_POWER'),'bd',l.get('MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL'),'hp',l.get('MODIFIER_VALUE_BASE_HEALTH_FROM_LEVEL'),'melee',l.get('MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL'),'boon',l.get('MODIFIER_VALUE_BOON_COUNT'),'bres',l.get('MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST'),'tres',l.get('MODIFIER_VALUE_TECH_RESIST'))

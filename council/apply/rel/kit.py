import re,sys
H=open('gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata',encoding='utf-8',errors='ignore').read()
V=open('gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata',encoding='utf-8',errors='ignore').read()
blocks={m.group(1):m.start() for m in re.finditer(r'^\t([a-z0-9_]+) =\s*\n\t\{',V,re.M)}
ks=sorted(blocks.values())
def body(k):
    s=blocks[k]; i=ks.index(s); return V[s:ks[i+1] if i+1<len(ks) else len(V)]
hb={m.group(1):m.start() for m in re.finditer(r'^\t(hero_[a-z0-9_]+) =\s*\n',H,re.M)}
hs=sorted(hb.values())
for hk in sys.argv[1:]:
    s=hb[hk]; i=hs.index(s); hbody=H[s:hs[i+1] if i+1<len(hs) else len(H)]
    print('#',hk)
    for n in range(1,5):
        m=re.search(r'ESlot_Signature_%d = "(\w+)"'%n,hbody); a=m.group(1); b=body(a)
        out=[]
        for mm in re.finditer(r'\n\t\t\t([A-Za-z0-9_]+) =\s*\n\t\t\t\{(.*?)\n\t\t\t\}',b,re.S):
            v=re.search(r'm_strValue = "?([^"\n]*)"?',mm.group(2)); sc=re.search(r'm_flStatScale = ([0-9.]+)',mm.group(2)); st=re.search(r'm_eSpecificStatScaleType = "(\w+)"',mm.group(2))
            cls=re.search(r'_class = "(scale_function_\w+)"',mm.group(2))
            val=v.group(1) if v else None
            if val in (None,'0','-1.0','0.0','-1','0m'): continue
            if sc or (cls and 'weapon' in cls.group(1)) or re.search('Charges|Cooldown$|Damage|DPS',mm.group(1)):
                tag=''
                if sc: tag=f"(+{sc.group(1)}x {st.group(1) if st else 'spirit'})"
                elif cls and 'weapon' in cls.group(1): tag=f"(WEAPONSCALE {st.group(1) if st else ''})"
                out.append(mm.group(1)+'='+val+tag)
        ups=re.findall(r'm_strPropertyName = "(\w+)"\s*\n\s*m_strBonus = "?([^"\n]*)"?',b)
        print(f" [{n}] {a}: "+', '.join(out)+' | ups '+' '.join(f'{p}{v}' for p,v in ups))

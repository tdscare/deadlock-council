import sys,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/council/tools'); import abtimeline as T
H=T.hero_info('hero_gigawatt'); L=H['L']; nm={1:'Ball',2:'Static',3:'PSurge',4:'Storm'}
for lab,o in [a.split('=') for a in sys.argv[1:]]:
    o=[int(c) for c in o]
    for mn,ev in [('A',T.model_A(o,L)),('Astrict',T.model_A(o,L,strict=True)),('B',T.model_B(o,L))]:
        print(f"{lab:8} {mn:7}", ' '.join(f"{nm[a]}{T.tlabel(t)}@{g}" for g,lv,a,t in sorted(ev) if g<=6000))

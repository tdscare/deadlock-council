# per-build rotations. ops: normal scenario ops; @ACTS = use offensive actives owned; @LATE = echo/refresher; @F n = fetch n
# Measured Abrams (Atlas) cadence in the arena: light melee lands every ~0.75 s (84-94 dmg sawtooth at L20), heavy every ~1.65 s (~205);
# Seismic Impact (ult) takes ~6 s from cast to landing (player is not meleeing during it); Shoulder Charge needs the camera on the target BEFORE casting (aim op).
HEAVY=['btn Weapon1 0.7','wait 1.0']
LIGHT=['btn Weapon1 0.12','wait 0.65']
ROT={}
AIM=['aim 0.3']
OPEN=['@ACTS','@F 350']+AIM+['cast 4 0.3','wait 6.0','@F 120']+AIM
CYC=['@F 350']+AIM+['cast 2 1.2','@F 120']+AIM+['cast 1 0.4']
ROT['abrams']=dict(dist=120,opener=OPEN+['cast 1 0.4']+HEAVY+LIGHT+LIGHT+HEAVY,
 loop=CYC+HEAVY+LIGHT+LIGHT+HEAVY,loops=3,late=['@LATE'])
ROT['abrams_melee']=dict(dist=120,opener=OPEN+HEAVY+LIGHT+LIGHT+HEAVY,
 loop=CYC+HEAVY+LIGHT+LIGHT+HEAVY+LIGHT,loops=3,late=['@LATE'])

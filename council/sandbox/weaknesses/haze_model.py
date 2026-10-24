# Haze 'haze' build: kit-first thesis model (CALCULATED grade only). Run: python3 -I haze_model.py
# Sources: audit/items_full.json, abilities.vdata (citadel_weapon_haze_set, ability_*), heroes.vdata hero_haze, a7/levels.json.
import json, sys, os
SP = os.path.dirname(os.path.abspath(__file__)) + '/../../..'
G = json.load(open(SP + '/audit/items_full.json'))
LV = json.load(open(SP + '/a7/levels.json'))
COST = {1: 800, 2: 1600, 3: 3200, 4: 6400}
COL = {'WeaponMod': 'w', 'Tech': 's', 'Armor': 'v'}
# hero_haze (heroes.vdata): HP 730 +33/lvl, bullet 5.26 +0.143/lvl, spirit +0.5/lvl (NOT the generic 1.1), clip 25, cycle 0.105 s, reload 2.35 s, crit x1.65
BASE_RPS = 1 / 0.105
TECH_INV = LV['tech']  # spirit invest bonus table (a7/levels.json)
# weapon invest table: <=4.8k from RULES_KIERAN; above 4.8k NOT in extracted data -> ASSUMED (spirit table x 46/38; 11.2k=74 as in round-12 sim)
GUN_INV = [[800, 9], [1600, 12], [2400, 15], [3200, 18], [4800, 46], [6400, 54], [8000, 63], [11200, 74], [16000, 80], [22400, 91], [28800, 100]]
ORDER = [3,3,1,1,2,3,4,2,2,2,3,4,1,1,4,4]   # data.js haze order; tiers index 0..3 = dagger, smoke, fixation, ult

def lvl_state(souls, order=ORDER):
    lvl = unl = pts = 0
    for x in LV['levels']:
        if souls >= x['gold']:
            lvl = x['l']; unl += x['unl']; pts += x['pts']
    tier = [-1, -1, -1, -1]; u, p = unl, pts
    for a in order:
        i = a - 1
        if tier[i] < 0:
            if u < 1: break
            u -= 1; tier[i] = 0
        else:
            if tier[i] >= 3: continue
            c = [1, 2, 5][tier[i]]
            if p < c: break
            p -= c; tier[i] += 1
    return lvl, tier

def inv_bonus(tab, s):
    b = 0
    for th, v in tab:
        if s >= th: b = v
    return b

def num(v):
    try: return float(str(v).split('(')[0])
    except: return 0.0

def owned_after(path, souls):
    """walk path left to right, buy while affordable; upgrades consume components and cost the difference"""
    owned, spent = [], 0
    for n in path:
        g = G[n]; have = [c for c in g['components'] if c in owned]
        c = COST[g['tier']] - sum(COST[G[h]['tier']] for h in have)
        if spent + c > souls: break
        spent += c; owned = [o for o in owned if o not in have] + [n]
    return owned, spent

def stats(owned, souls):
    lvl, tier = lvl_state(souls)
    S = dict(WD=0, FR=0, CLIP=0, LS=0, HP=0, AMP=0, BR=0, TR=0, SPI=0, REGEN=2.0, DUR=0)
    inv = {'w': 0, 's': 0, 'v': 0}
    for n in owned:
        st = G[n]['stats']; inv[COL[G[n]['slot']]] += COST[G[n]['tier']]
        S['WD'] += num(st.get('BaseAttackDamagePercent', 0))
        S['CLIP'] += num(st.get('BonusClipSizePercent', 0))
        S['HP'] += num(st.get('BonusHealth', 0))
        S['BR'] += num(st.get('BulletResist', 0)); S['TR'] += num(st.get('TechResist', 0))
        S['SPI'] += num(st.get('TechPower', 0)) + num(st.get('SpiritPower', 0))
        S['REGEN'] += num(st.get('BonusHealthRegen', 0))
        if n not in ('Burst Fire', 'Active Reload', 'Healing Tempo', 'Vampiric Burst'):
            S['FR'] += num(st.get('BonusFireRate', 0))
        if n == 'Burst Fire': S['FR'] += 10
        if n == 'Spiritual Overflow': S['FR'] += 0  # charged only, handled in fight
        if n in ('Bullet Lifesteal', 'Vampiric Burst', 'Leech', 'Frenzy'):
            S['LS'] += num(st.get('BulletLifestealPercent', 0))
        if n in ('Healing Booster', 'Healing Tempo'): S['AMP'] = max(S['AMP'], num(st['HealAmpCastPercent']))
        if n in ('Superior Duration',): S['DUR'] += 28
        if n == 'Duration Extender': S['DUR_SMOKE'] = 22
    S['WD'] += inv_bonus(GUN_INV, inv['w'])
    S['SPI'] += inv_bonus(TECH_INV, inv['s']) + 0.5 * (lvl - 1)
    if 'Extra Charge' in owned: S['SPI_SMOKE'] = 7
    if 'Rapid Recharge' in owned: S['SPI_SMOKE'] = 14
    S['HPMAX'] = 730 + 33 * (lvl - 1) + S['HP']
    S.update(lvl=lvl, tier=tier, inv=inv, owned=owned)
    return S

def fight(S, T=10.0, acc=0.5, head=0.2, resist=0.20, targets=1, ricochet_ls=True, tempo='none', amp_on_ls=True,
          enemy_hp=2500, smoke_first=True, ult=False, incoming=0.0):
    o = S['owned']; tier = S['tier']; dt = 0.005
    clip = int(25 * (1 + S['CLIP'] / 100)); ammo = clip
    lvl = S['lvl']; base = 5.26 + 0.143 * (lvl - 1)
    fixT = tier[2]
    cap = 0 if fixT < 0 else (80 if fixT >= 2 else 40)
    per = 0 if fixT < 0 else (0.31 + 0.00035 * S['WD'] if fixT >= 3 else 0.2)
    amp = 1 + (S['AMP'] / 100 if amp_on_ls else 0)
    smokeT = tier[1]
    charges = 0 if smokeT < 2 else 2
    if 'Extra Charge' in o: charges += 1
    if 'Rapid Recharge' in o: charges += 2
    if smokeT >= 0 and charges == 0: charges = 1
    between = 7 * (0.7 if 'Rapid Recharge' in o else 1)
    smoke_buff = 5 * (1 + (S['DUR'] + S.get('DUR_SMOKE', 0)) / 100) if smokeT >= 3 else 0
    t = 0; stacks = 0; dmg = heal = spiritdmg = 0; reload_left = 0; shots = 0
    smoke_end = -1; last_smoke = -99; bf_end = -1; bf_cd = 0; ar_end = -1; ar_cd = 0; vb_end = -1; vb_used = False
    sip_cd = 0; stolen = 0; next_shot = 0; tempo_on = False
    ult_end = -1
    if ult and tier[3] >= 0:
        ult_dur = 3.5 + 0.03 * S['SPI']
        ult_end = ult_dur
    lsdur = 0.0
    hpmax = S['HPMAX']; hp = hpmax; eff = 0.0; dead = None
    inc = incoming * (1 - min(S['BR'], 60) / 100)
    while t < T:
        hp -= inc * dt
        hp = min(hp + S['REGEN'] * (1 + S['AMP'] / 100) * dt, hpmax)
        if hp <= 0 and dead is None: dead = t
        # smoke casts (chain while charges last)
        if smokeT >= 3 and charges > 0 and t >= smoke_end and t - last_smoke >= between and smoke_first:
            charges -= 1; last_smoke = t; smoke_end = t + smoke_buff
        if reload_left > 0:
            reload_left -= dt
            if reload_left <= 0: ammo = clip
            t += dt; continue
        in_ult = t < ult_end
        fr = 1 + S['FR'] / 100
        if t < bf_end: fr += 0.32
        if t < ar_end: fr += 0.25
        if t < vb_end: fr += 0.34
        if tempo_on: fr += 0.35
        if in_ult: fr += 0.25 + (0.10 if tier[3] >= 2 else 0)
        rps = BASE_RPS * fr
        if in_ult: rps = max(rps, 5)
        if t >= next_shot:
            next_shot = t + 1 / rps; shots += 1
            if not in_ult: ammo -= 1   # ASSUMPTION: Bullet Dance does not use magazine ammo [U]
            a = 1.0 if in_ult else acc; h = 0.0 if in_ult else head
            flat = (7 + (7 if tier[3] >= 1 else 0)) if in_ult else 0
            B = base * (1 + S['WD'] / 100) + flat
            if 'Lucky Shot' in o: B *= 1.25
            B += min(stacks, cap) * per
            per_shot = a * ((1 - h) * B + h * B * 1.65) * (1 - resist)
            mult = 1 + (0.65 * min(targets - 1, 2) if 'Ricochet' in o else 0)
            d = per_shot * mult
            dmg += d
            ls = S['LS']
            if t < smoke_end: ls += 50; lsdur += 1 / rps
            if t < ar_end: ls += 16
            if t < vb_end: ls += 70
            lsbase = per_shot * (mult if ricochet_ls else 1)
            hh = lsbase * ls / 100 * amp; heal += hh
            g = min(hh, hpmax - hp); eff += g; hp += g
            if cap:
                ns = stacks + a * ((1 - h) + 3 * h)
                if fixT >= 1 and int(ns // 20) > int(stacks // 20): spiritdmg += 40 + 0.8 * S['SPI']
                stacks = ns
            if 'Burst Fire' in o and t >= bf_cd and a > 0: bf_end = t + 4.5 * (1 + S['DUR'] / 100); bf_cd = t + 9
            if 'Siphon Bullets' in o and t >= sip_cd:
                sip_cd = t + 1.2; st = 0.025 * enemy_hp * a; stolen += st; hpmax += st; hp += st; eff += st
                if tempo == 'siphon' and 'Healing Tempo' in o: tempo_on = True
            if ammo <= 0:
                if 'Vampiric Burst' in o and not vb_used:
                    vb_used = True; vb_end = t + 5 * (1 + S['DUR'] / 100); ammo = int(clip * 0.75)
                    if tempo == 'vb' and 'Healing Tempo' in o: tempo_on = True
                elif 'Active Reload' in o and t >= ar_cd:
                    reload_left = 1.0; ar_end = t + 1.0 + 7 * (1 + S['DUR'] / 100); ar_cd = t + 12   # ASSUMED 1.0 s timed reload
                else:
                    reload_left = 2.35
        t += dt
    regen = S['REGEN'] * T * (1 + S['AMP'] / 100)
    return dict(dead=dead, hpend=hp, eff=eff, dmg=dmg + spiritdmg * (1 - 0.15), heal=heal, stolen=stolen, regen=regen, shots=shots, clip=clip, lsdur=lsdur)

def row(name, path, souls, **kw):
    o, spent = owned_after(path, souls)
    S = stats(o, souls)
    f1 = fight(S, **kw)
    f3 = fight(S, targets=3, **kw)
    fu = fight(S, T=6, ult=True, targets=3, **kw)
    camp = fight(S, T=10, acc=0.9, head=0.0, resist=0.0, targets=3, smoke_first=False)
    return dict(name=name, souls=souls, spent=spent, lvl=S['lvl'], tier=S['tier'], inv=S['inv'], hp=S['HPMAX'], wd=S['WD'], fr=S['FR'],
                clip=f1['clip'], spi=round(S['SPI'], 1), d1=f1['dmg'], h1=f1['heal'], st1=f1['stolen'], d3=f3['dmg'], h3=f3['heal'], du=fu['dmg'], hu=fu['heal'],
                camp=camp['dmg'] / 10, last=o[-1] if o else '-', n=len(o))

CUR = ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Extra Health','Fortitude','Ricochet',
       'Healing Booster','Siphon Bullets','Burst Fire','Bullet Lifesteal','Extra Charge','Lucky Shot','Rapid Recharge','Vampiric Burst','Silencer','Healing Tempo']
PATHS = {
 'CUR (data.js)': CUR,
 'K1 Ricochet-before-greens': ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Ricochet','Extra Health','Fortitude',
       'Healing Booster','Siphon Bullets','Burst Fire','Bullet Lifesteal','Extra Charge','Lucky Shot','Rapid Recharge','Vampiric Burst','Silencer','Healing Tempo'],
 'K2 lifesteal-early, no HB/HT': ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Extra Health','Fortitude','Ricochet',
       'Bullet Lifesteal','Siphon Bullets','Burst Fire','Extra Charge','Lucky Shot','Vampiric Burst','Rapid Recharge','Silencer','Duration Extender','Superior Duration','Frenzy'],
 'K3 = CUR but Leech for VB': ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Extra Health','Fortitude','Ricochet',
       'Healing Booster','Siphon Bullets','Burst Fire','Bullet Lifesteal','Extra Charge','Lucky Shot','Rapid Recharge','Spirit Lifesteal','Leech','Silencer','Healing Tempo'],
 'R1 spirit hybrid': ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Extra Health','Extra Charge','Extra Spirit','Surge of Power','Fortitude','Ricochet',
       'Rapid Recharge','Siphon Bullets','Bullet Lifesteal','Spirit Lifesteal','Spiritual Overflow','Lucky Shot','Vampiric Burst','Silencer'],
 'R2 duration smoke': ['Rapid Rounds','Active Reload','Swift Striker','Extended Magazine','Titanic Magazine','Extra Health','Fortitude','Ricochet',
       'Duration Extender','Siphon Bullets','Burst Fire','Bullet Lifesteal','Extra Charge','Lucky Shot','Rapid Recharge','Vampiric Burst','Silencer','Superior Duration','Frenzy'],
 'B0 conventional (late Ricochet)': ['Rapid Rounds','Active Reload','Extended Magazine','Swift Striker','Titanic Magazine','Extra Health','Burst Fire','Bullet Lifesteal','Fortitude',
       'Ricochet','Extra Spirit','Surge of Power','Lucky Shot','Vampiric Burst','Siphon Bullets','Silencer','Spirit Lifesteal','Spiritual Overflow'],
}
CPS = [5000, 10000, 14400, 18000, 24000, 30000, 41600, 52800]
if __name__ == '__main__':
    tempo = sys.argv[1] if len(sys.argv) > 1 else 'none'
    for nm, p in PATHS.items():
        print('##', nm, '| tempo trigger:', tempo)
        print('souls spent lvl tiers[dag,smk,fix,ult] inv w/s/v  HP  WD% FR% clip SP | 1v1 10s dmg heal(+siphon) | 3-tgt dmg heal | ult6s dmg heal | camp dps | last buy (n)')
        for s in CPS:
            r = row(nm, p, s, tempo=tempo)
            print(f"{s:5d} {r['spent']:5d} {r['lvl']:2d} {r['tier']} {r['inv']['w']}/{r['inv']['s']}/{r['inv']['v']} {r['hp']:5.0f} {r['wd']:3.0f} {r['fr']:3.0f} {r['clip']:3d} {r['spi']:5.1f} | {r['d1']:5.0f} {r['h1']:4.0f}(+{r['st1']:3.0f}) | {r['d3']:5.0f} {r['h3']:4.0f} | {r['du']:5.0f} {r['hu']:4.0f} | {r['camp']:4.0f} | {r['last']} ({r['n']})")

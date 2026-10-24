#!/usr/bin/env python3
"""Ability timeline x item timing + conditional-item rows (WEAKNESS_PROCESS.md section M). Generalises prac/ap.py (ap.py untouched).
usage (from SP):  python3 -I council/tools/abtimeline.py <build id> [--order 1123...]     one build, text
                  python3 -I council/tools/abtimeline.py --gate [<outdir>] [ids...]       JSON verdict per build (exit 1 if any FAIL)
                  python3 -I council/tools/abtimeline.py --all <outdir>                   every build -> <outdir>/<id>.txt + _all.json
Sources: data.js (via node), gt/repo heroes.vdata + abilities.vdata (numbers, levels, invest bonuses, item stats by class),
citadel_mods_english.txt (trigger wording), audit/items_full.json (names/tiers/slots/components only).
Weakness/remedy set (15:19): --weakness <id> <ammo|reach|auto> [--at souls]; discovery (15:16): --discover <id> [--at souls] [--n 3] [--queue].
Interactions (Kieran 14:29): --interactions <id> <item> [--at souls] [--vs item]... [--out f] [--no-requests]  (item x kit matrix + equal-soul comparison + sandbox test requests).
Strategy (Kieran 13:56): --strategy <id> <checkpoints> [--alt f]... [--out f] [--set K=V] [--grid quick|full]; --game-summary <file>; --spikes <id>; --verify-strategy <file>  (see the STRATEGY block).
Overlap / in-build value (section J/L): --overlap [ids] [--build-file f] [--json] [--only-flags]; --context <id> <item> <outfile>; --state <id> <souls> [compared,items]  (see the OVERLAP block below).
Point models (council/sandbox/abtimeline/FOUNDATIONS.md):
  A = game data: unlocks are their own currency (levels 1/3/5/8), cost 0 AP; T1/T2/T3 cost 1/2/5 AP (F4 INFERRED); order followed strictly.
  B = old audit model (gen/ac_tl.js timesB): abilities 1-3 pre-unlocked, every order entry = 1 AP, nth entry of 1-3 = Tn.
Purchase walk = a7/sp.js rules (core boxes L-R, owned components consumed by the first upgrade, 'Sell X for this' drops X).
Every core item with a trigger condition gets a CONDITIONAL row; an item with a condition key but no encoded rule prints UNCHECKED."""
import re, sys, json, subprocess, os
SP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SC = SP + '/gt/repo/game/citadel/pak01_dir/scripts/'
LOC = SP + '/gt/repo/game/citadel/resource/localization/citadel_mods/citadel_mods_english.txt'
TIERCOST = {1: 1, 2: 2, 3: 5}
SOULS = {1: 800, 2: 1600, 3: 3200, 4: 6400, 5: 16000}

def num(v):
    m = re.match(r'\s*(-?[0-9.]+)', str(v)); return float(m.group(1)) if m else None

# ---------------- vdata ----------------
_V = {}
def vfile(n):
    if n not in _V:
        t = open(SC + n, encoding='utf-8', errors='ignore').read()
        idx = {m.group(1): m.start() for m in re.finditer(r'^\t([A-Za-z0-9_]+) = \s*\n\t\{', t, re.M)}
        _V[n] = (t, idx, sorted(idx.values()))
    return _V[n]
def block(f, k):
    t, idx, ks = vfile(f)
    if k not in idx: return None
    s = idx[k]; i = ks.index(s); return t[s:ks[i + 1] if i + 1 < len(ks) else len(t)]

def props(b):
    j = b.find('m_mapAbilityProperties')
    if j < 0: return {}
    e = re.search(r'\n\t\t\}', b[j:]); seg = b[j:j + e.start()] if e else b[j:]
    out = {}
    for m in re.finditer(r'\n\t\t\t([A-Za-z0-9_]+) = \s*\n\t\t\t\{(.*?)\n\t\t\t\}', seg, re.S):
        body = m.group(2); v = re.search(r'm_strValue = "?([^"\n]*)"?', body)
        sc = re.search(r'm_flStatScale = ([0-9.\-]+)', body); st = re.search(r'm_eSpecificStatScaleType = "(\w+)"', body)
        f = re.search(r'm_eApplyFilter = "(\w+)"', body)
        out[m.group(1)] = {'raw': v.group(1) if v else None, 'v': num(v.group(1)) if v else None, 'scale': float(sc.group(1)) if sc else 0.0,
                           'stype': st.group(1) if st else '', 'filter': f.group(1) if f else '', 'isdmg': 'm_bIsAbilityDamageProperty = true' in body,
                           'sfun': ' '.join(re.findall(r'_class = "(scale_function\w*)"', body)) + ' ' + ' '.join(re.findall(r'"(E\w+)"', body))}
    return out

def upgrades(b):
    j = b.find('m_vecAbilityUpgrades')
    if j < 0: return []
    tiers = []
    for m in re.finditer(r'\n\t\t\t\{\s*\n\t\t\t\tm_vecPropertyUpgrades = \s*\n\t\t\t\t\[(.*?)\n\t\t\t\t\]', b[j:], re.S):
        ups = []
        for u in re.finditer(r'\{(.*?)\}', m.group(1), re.S):
            pn = re.search(r'm_strPropertyName = "(\w+)"', u.group(1)); bo = re.search(r'm_strBonus = "?([^"\n]*)"?', u.group(1))
            ty = re.search(r'm_eUpgradeType = "(\w+)"', u.group(1))
            if pn and bo: ups.append((pn.group(1), num(bo.group(1)), ty.group(1) if ty else 'EAddToBase'))
        tiers.append(ups)
        if len(tiers) == 3: break
    return tiers

_HSC = {}
def hero_scaling(hk):
    """hero-level stat scaling from heroes.vdata m_mapScalingStats: {stat: (scaling stat, scale)} (e.g. Haze EClipSize 0.5 x ETechPower).
    Units are read as: clip/bullet damage/regen/melee = flat per point, fire rate/resist = percent per point, move/sprint = m/s per point (ASSUMED units; game data gives only the factor)."""
    if hk not in _HSC:
        b = block('heroes.vdata', hk) or ''; j = b.find('m_mapScalingStats'); seg = b[j:b.find('m_heroStatsDisplay', j)] if j >= 0 else ''
        _HSC[hk] = {s[0]: (s[1] or s[4], float(s[2] or s[3])) for s in re.findall(r'(E\w+) = \s*\{\s*(?:eScalingStat = "(\w+)"\s*flScale = ([0-9.]+)|flScale = ([0-9.]+)\s*eScalingStat = "(\w+)")', seg)}
    return _HSC[hk]
def hsc(R, w, stat):
    """hero scaling bonus for `stat` at this state (unconditional spirit power only; imbued/charged-only spirit does not count: it is not the hero's ETechPower)."""
    s = hero_scaling(R['b']['hk']).get(stat)
    if not s or s[0] != 'ETechPower': return 0.0
    return s[1] * (w.get('sp_unc', w.get('sp', 0.0)) or 0.0)
def hero_info(hk):
    b = block('heroes.vdata', hk); base = block('heroes.vdata', 'hero_base')
    ab = {int(k): v for k, v in re.findall(r'ESlot_Signature_(\d) = "(\w+)"', b)}
    wpn = (re.search(r'ESlot_Weapon_Primary = "(\w+)"', b) or [None, None])[1]
    def levels(bb):
        j = bb.find('m_mapLevelInfo')
        if j < 0: return None
        return [(int(lv), int(g), int((re.search(r'EAbilityUnlocks = (\d+)', r) or [0, 0])[1]), int((re.search(r'EAbilityPoints = (\d+)', r) or [0, 0])[1]),
                 'm_bUseStandardUpgrade = true' in r) for lv, g, r in re.findall(r'"(\d+)" = \s*\{\s*m_unRequiredGold = (\d+)(.*?)\n\t\t\t\}', bb[j:], re.S)]
    def bon(bb, slot):
        k = bb.find('m_MapModCostBonuses')
        if k < 0: return None
        j = bb.find(slot + ' = ', k); seg = bb[j:bb.find(']', j)]
        return [(int(a), float(c)) for a, c in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)', seg)]
    g = lambda pat, d: float((re.search(pat, b) or re.search(pat, base) or [None, d])[1])
    return {'ab': ab, 'wpn': wpn, 'L': levels(b) or levels(base), 'tech': bon(b, 'EItemSlotType_Tech') or bon(base, 'EItemSlotType_Tech'),
            'weap': bon(b, 'EItemSlotType_WeaponMod') or bon(base, 'EItemSlotType_WeaponMod'),
            'tp': g(r'MODIFIER_VALUE_TECH_POWER = ([0-9.]+)', 1.1), 'bdl': g(r'MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL = ([0-9.]+)', 0)}

_AB = {}
def ability(cls):
    if cls not in _AB:
        b = block('abilities.vdata', cls) or ''
        t = re.search(r'\n\t\tm_eAbilityType = "(\w+)"', b); st = re.search(r'\n\t\tm_bStartTrained = (\w+)', b)
        _AB[cls] = {'cls': cls, 'props': props(b), 'ups': upgrades(b), 'type': t.group(1) if t else '', 'start': st.group(1) if st else '?'}
    return _AB[cls]

def at_tier(a, tier):
    P = {k: dict(v) for k, v in a['props'].items()}
    for t in range(min(max(tier, 0), 3)):
        if t >= len(a['ups']): break
        for pn, bo, ty in a['ups'][t]:
            if bo is None: continue
            p = P.setdefault(pn, {'raw': None, 'v': 0.0, 'scale': 0.0, 'stype': '', 'sfun': '', 'filter': ''})
            if ty == 'EAddToScale': p['scale'] = (p['scale'] or 0) + bo
            else: p['v'] = (p['v'] or 0) + bo
    return P
def pv(P, k): return (P.get(k) or {}).get('v')
def charges(a, t): return 0 if t < 0 else int(pv(at_tier(a, t), 'AbilityCharges') or 1)
def charges_raw(a, t): return 0 if t < 0 else int(pv(at_tier(a, t), 'AbilityCharges') or 0)   # 0 = ability has no charge system

def spirit_hits(P, sp):
    """per-instance spirit damage: properties the game scales as tech damage (scale_function_tech_damage), or *Damage props scaled by ETechPower.
    spirit scale applies when the scale type is ETechPower or implicit (empty) inside scale_function_tech_damage."""
    out = {}
    for k, p in P.items():
        if not (p.get('v') and p['v'] > 0) or re.search(r'Percent|Pct|Mult|LowHealth|Cap|Time$|Duration|Radius|Range|Threshold', k): continue
        td = ('tech_damage' in p['sfun'] or 'TechDamage' in p['sfun']); tp = p['stype'] == 'ETechPower'
        if not (td or p.get('isdmg') or (tp and re.search(r'Damage|DPS', k))): continue
        if p['stype'] in ('EWeaponPower', 'EWeaponDPS', 'EBaseWeaponDamageIncrease'): continue   # weapon-scaled ability damage: not computed
        sc = (p['scale'] or 0) if (tp or (td and p['stype'] == '')) else 0
        dmg = p['v'] + sc * sp
        if re.search(r'DPS|PerSecond', k):
            tick = pv(P, 'TickRate'); out[k] = (dmg * tick, True) if tick else (dmg, False)
        else: out[k] = (dmg, True)
    return out   # name -> (instance damage, is_instance)

# ---------------- point models ----------------
def model_A(order, L, strict=False):
    """data model. Unlock entries spend the unlock currency, AP entries spend AP (1/2/5). Default: the two currencies are independent queues
    (an unlock entry is taken as soon as an unlock is available even if an earlier AP entry is still saving up; an AP entry still needs its
    ability unlocked). strict=True = a7/sp.js / prac/ap.py reading (one queue, everything waits)."""
    tier = {1: -1, 2: -1, 3: -1, 4: -1}; U = P = 0; ev = []
    seq = []; cnt = {1: 0, 2: 0, 3: 0, 4: 0}
    for a in order:
        if cnt[a] <= 3: seq.append((a, cnt[a]))
        cnt[a] += 1
    done = [False] * len(seq)
    for lv, g, u, p, _ in L:
        U += u; P += p; moved = True
        while moved:
            moved = False
            for i, (a, t) in enumerate(seq):
                if done[i]: continue
                if t == 0:
                    if U >= 1: U -= 1; tier[a] = 0; ev.append((g, lv, a, 0)); done[i] = True; moved = True; break
                    if strict: break
                    continue
                if tier[a] != t - 1: break   # AP queue keeps its order; a tier on a not-yet-unlocked ability waits
                if P >= TIERCOST[t]: P -= TIERCOST[t]; tier[a] = t; ev.append((g, lv, a, t)); done[i] = True; moved = True; break
                break   # AP queue keeps its order: a costly tier is saved for, later AP entries wait
            # unlock entries after a blocked AP entry are still reachable in non-strict mode
            if not moved and not strict:
                for i, (a, t) in enumerate(seq):
                    if not done[i] and t == 0 and U >= 1:
                        U -= 1; tier[a] = 0; ev.append((g, lv, a, 0)); done[i] = True; moved = True; break
    return ev
def model_B(order, L):
    tier = {1: 0, 2: 0, 3: 0, 4: -1}; cnt = {1: 0, 2: 0, 3: 0, 4: 0}; ap = 0; i = 0; ev = [(0, 1, s, 0) for s in (1, 2, 3)]
    for lv, g, u, p, _ in L:
        ap += p
        while i < len(order) and i < ap:
            a = order[i]; cnt[a] += 1; t = cnt[a] if a != 4 else cnt[a] - 1
            if t <= 3 and t > tier[a]: tier[a] = t; ev.append((g, lv, a, t))
            i += 1
    return ev
def tiers_at(ev, souls):
    t = {1: -1, 2: -1, 3: -1, 4: -1}
    for g, lv, a, nt in ev:
        if g <= souls: t[a] = max(t[a], nt)
    return t
def level_at(L, souls):
    lv = 1; boons = 0; ap = 0
    for l, g, u, p, std in L:
        if g <= souls: lv = l; boons += 1 if std else 0; ap += p
    return lv, boons, ap

# ---------------- items ----------------
G = None; DESC = None
def items():
    global G
    if G is None: G = json.load(open(SP + '/audit/items_full.json'))
    return G
def desc(cls):
    global DESC
    if DESC is None:
        DESC = {}
        for k, v in re.findall(r'"(upgrade_\w+)_desc"\s+"(.*)"', open(LOC, encoding='utf-8', errors='ignore').read()):
            DESC[k] = re.sub(r'<[^>]*>', '', v)
    return DESC.get(cls, '')
_IT = {}
def proc_rules(cls):
    """trigger flags of the item's intrinsic proc modifier (abilities.vdata m_AutoIntrinsicModifiers)."""
    b = block('abilities.vdata', cls) or ''; j = b.find('m_AutoIntrinsicModifiers')
    if j < 0: return ''
    seg = b[j:j + 4000]; out = []
    t = re.findall(r'"CITADEL_DAMAGETYPE_(\w+)"', seg)
    if t: out.append('proc damage types ' + '/'.join(sorted(set(t))))
    for k in ('m_bCanProcFromItems', 'm_bIgnoreResists', 'm_bCanProcByOtherObjects'):
        m = re.search(k + r' = (\w+)', seg)
        if m: out.append(f"{k[3:]}={m.group(1)}")
    return ', '.join(out)
def item(n):
    if n not in _IT:
        g = items().get(n)
        if not g: _IT[n] = None; return None
        b = block('abilities.vdata', g['class']) or ''
        pr = props(b); req = re.search(r'm_eAbilityRequirements = "(\w+)"', b)
        _IT[n] = dict(g, vprops=pr, vstats={k: p['raw'] for k, p in pr.items() if p['raw'] not in (None, '')}, req=req.group(1) if req else '')
    return _IT[n]
def sv(it, k, d=0.0):
    x = num(it['vstats'].get(k, '')) if it['vstats'].get(k) not in (None, '') else None
    return d if x is None else x

COND_SP = {'upgrade_magic_shield': 'only above 65% health', 'upgrade_arcane_surge': 'only the next ability after a dash-jump'}
def item_sp(it, cond=True):
    t = 0.0
    if it['class'] in COND_SP and not cond: return 0.0
    for k, p in it['vprops'].items():
        if k in ('TechPower', 'SpiritPower') and p.get('v'): t += p['v']
    return t
def item_sp_pct(it): return sv(it, 'TechPowerPercent')

def load_builds():
    js = "const fs=require('fs');const B=new Function(fs.readFileSync(process.argv[1],'utf8')+';return B')();process.stdout.write(JSON.stringify(B.map(b=>({id:b.id,hero:b.hero,name:b.name,hk:b.hk,abil:b.abil,order:b.order,rows:b.rows}))))"
    return json.loads(subprocess.run(['node', '-e', js, SP + '/data.js'], capture_output=True, text=True, check=True).stdout)

def walk(b, refund=0.0):
    """core purchase walk. refund = share of a sold item's price returned (0 = old behaviour; --path/--strategy pass STRAT_P REFUND, an UNVERIFIED value)."""
    owned = []; souls = 0; out = []; imbues = {}
    for r in b['rows']:
        for box in r:
            if not re.match(r'^(Early|Mid|Late)', box[0]): continue
            for x in box[3]:
                n = x[0]; note = x[1] if len(x) > 1 else ''; imb = x[2] if len(x) > 2 else None
                it = item(n)
                if not it: out.append({'n': n, 'unknown': True}); continue
                have = [c for c in it['components'] if c in owned]
                souls += max(0, SOULS[it['tier']] - sum(SOULS[item(c)['tier']] for c in have))
                owned = [o for o in owned if o not in have]; owned.append(n)
                sm = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first)', note or '')
                if sm and sm.group(1) in owned: owned.remove(sm.group(1)); souls -= refund * SOULS[item(sm.group(1))['tier']]
                if imb and str(imb).isdigit(): imbues[n] = int(imb)
                out.append({'n': n, 'souls': souls, 'imb': int(imb) if imb and str(imb).isdigit() else None, 'owned': list(owned),
                            'imbues': {k: v for k, v in imbues.items() if k in owned}, 'box': box[0]})
    return out

# ---------------- state per purchase ----------------
def analyse(b, order=None, refund=0.0):
    H = hero_info(b['hk']); order = order or b['order']; L = H['L']
    R = {'b': b, 'H': H, 'L': L, 'order': order, 'evA': model_A(order, L), 'evB': model_B(order, L), 'abil': {s: ability(H['ab'][s]) for s in (1, 2, 3, 4)}}
    W = walk(b, refund); rows = []
    for w in W:
        if w.get('unknown'): rows.append(w); continue
        rows.append(state(R, w))
    R['rows'] = rows
    return R

def state(R, w):
    H = R['H']; s = w['souls']; lv, boons, ap = level_at(R['L'], s)
    own = [item(o) for o in w['owned']]
    def inv(slot): return sum(SOULS[i['tier']] for i in own if i['slot'] == slot)
    tb = max([bo for th, bo in H['tech'] if inv('Tech') >= th] or [0]); wb = max([bo for th, bo in H['weap'] if inv('WeaponMod') >= th] or [0])
    pct = sum(item_sp_pct(i) for i in own) / 100
    sp_all = (boons * H['tp'] + sum(item_sp(i) for i in own) + tb) * (1 + pct)
    sp_unc = (boons * H['tp'] + sum(item_sp(i, False) for i in own) + tb) * (1 + pct)
    chg_sp = sum(sv(i, 'BonusSpiritForChargedAbilities') for i in own)
    return dict(w, lv=lv, boons=boons, ap=ap, sp=sp_all, sp_unc=sp_unc, tb=tb, wb=wb, chg_sp=chg_sp, own=own,
                tA=tiers_at(R['evA'], s), tB=tiers_at(R['evB'], s))

def slot_sp(R, w, sl, t, cond=True, rule2=True):
    """spirit power that applies to ability sl: base + charged-only bonus (if it has 2+ charges, F7) + imbued spirit."""
    a = R['abil'][sl]; x = w['sp'] if cond else w['sp_unc']
    if charges(a, t) >= (2 if rule2 else 1): x += w['chg_sp']
    for n, s2 in w['imbues'].items():
        if s2 == sl: x += sv(item(n), 'ImbuedTechPower')
    return x

def best_hit(R, w, T, thr, only=None, cond=True):
    """(value, slot, prop, list of (slot,prop,value,cd) above thr)"""
    best = (0, None, None); above = []
    for sl in (only or (1, 2, 3, 4)):
        if T[sl] < 0: continue
        P = at_tier(R['abil'][sl], T[sl])
        for k, (v, inst) in spirit_hits(P, slot_sp(R, w, sl, T[sl], cond)).items():
            if not inst: continue
            if v > best[0]: best = (v, sl, k)
            if v > thr: above.append((sl, k, v, pv(P, 'AbilityCooldown')))
    return best[0], best[1], best[2], above

def gun_window(R, w, window):
    """weapon damage in `window` s, 100% body hits, no falloff (upper bound)."""
    b = block('abilities.vdata', R['H']['wpn']) or ''
    g = lambda k, d=0: float((re.search(k + r' = ([0-9.\-]+)', b) or [None, d])[1])
    dmg = g('m_flBulletDamage'); cyc = g('m_flCycleTime', 1) or 1; pel = g('m_iBullets', 1) or 1; clip = g('m_iClipSize', 10)
    own = w['own']; wpct = w['wb'] + sum(sv(i, 'BaseAttackDamagePercent') for i in own if i['class'] not in ('upgrade_magic_shield',))
    fr = sum(sv(i, 'BonusFireRate') + sv(i, 'FireRateBonus') for i in own if i['class'] not in ('upgrade_healbuff', 'upgrade_tech_overflow', 'upgrade_quick_silver', 'upgrade_ethereal_bullets'))
    clip *= 1 + sum(sv(i, 'BonusClipSizePercent') for i in own) / 100
    per = (dmg + w['boons'] * R['H']['bdl']) * (1 + wpct / 100) * pel
    shots = min(int(clip), 1 + int(window * (1 + fr / 100) / cyc))
    return per * shots, per, shots

# ---------------- conditional rule registry ----------------
# kind: hit (one ability instance > MinimumDamage), hitimb (imbued ability instance), win (spirit dmg in window, one target), gunwin (weapon dmg in window),
# charged (needs ability with charges), imbue (needs trained imbued ability with the stat), ult (needs ult), spiritsrc (needs a spirit-damage source),
# cast (needs ability casts), taken (damage taken from enemies), selfhp / enemyhp (health %), range (distance), stack/proc (hits), heal, melee, dash
REG = {
 'upgrade_magic_burst': 'hit', 'upgrade_magic_shock': 'hit', 'upgrade_mystic_reverb': 'hitimb', 'upgrade_spirit_burn': 'win', 'upgrade_rechargingbullets': 'gunwin+charged',
 'upgrade_extra_charge': 'charged', 'upgrade_rapid_recharge': 'charged', 'upgrade_magic_tempo': 'imbue', 'upgrade_ability_power_shard': 'imbue', 'upgrade_arcane_extension': 'imbue',
 'upgrade_magic_reach': 'imbue', 'upgrade_magic_storm': 'imbue', 'upgrade_quick_silver': 'imbue', 'upgrade_ethereal_bullets': 'imbue', 'upgrade_bulletshredimbue': 'imbue',
 'upgrade_ultimate_burst': 'ult', 'upgrade_ability_refresher': 'ult', 'upgrade_escalating_exposure': 'spiritsrc+stack', 'upgrade_magic_vulnerability': 'spiritsrc',
 'upgrade_bullet_resist_shredder': 'spiritsrc', 'upgrade_mystic_regeneration': 'spiritsrc', 'upgrade_infuser': 'spiritsrc', 'upgrade_resonant_healing': 'cast',
 'upgrade_cooldown_reduction': 'cast', 'upgrade_imbued_duration_extender': 'cast', 'upgrade_absorbing_armor': 'taken', 'upgrade_spirit_bubble': 'taken',
 'upgrade_magic_shield': 'selfhp', 'upgrade_regenerating_bullet_shield': 'selfhp', 'upgrade_hollow_point_rounds': 'selfhp', 'upgrade_chonky': 'selfhp',
 'upgrade_tech_purge': 'selfhp', 'upgrade_improved_bullet_armor': 'selfhp', 'upgrade_fervor': 'selfhp', 'upgrade_pristine_emblem': 'enemyhp',
 'upgrade_close_range': 'range', 'upgrade_close_quarter_combat': 'range', 'upgrade_long_range': 'range', 'upgrade_sharpshooter': 'range',
 'upgrade_berserker': 'stack', 'upgrade_siphon_bullets': 'stack', 'upgrade_trophy_collector': 'stack', 'upgrade_enchanted_holsters': 'stack', 'upgrade_spellslinger_headshots': 'stack',
 'upgrade_crushing_fists': 'stack+melee', 'upgrade_split_shot': 'stack', 'upgrade_glass_cannon': 'stack', 'upgrade_reinforcing_casings': 'stack', 'upgrade_tech_overflow': 'stack',
 'upgrade_critshot': 'proc', 'upgrade_headshot_booster': 'proc', 'upgrade_headhunter': 'proc', 'upgrade_chain_lightning': 'proc', 'upgrade_crackshot': 'proc',
 'upgrade_capacitor': 'proc', 'upgrade_medic_bullets': 'proc', 'upgrade_express_shot': 'proc', 'upgrade_proc_silence': 'proc', 'upgrade_banshee_slugs': 'proc',
 'upgrade_healbuff': 'heal', 'upgrade_acolytes_glove': 'melee', 'upgrade_spirit_snatch': 'melee', 'upgrade_boxing_glove': 'melee', 'upgrade_lifestrike_gauntlets': 'melee',
 'upgrade_melee_charge': 'melee', 'upgrade_arcane_surge': 'dash', 'upgrade_weapon_backstabber': 'proc', 'upgrade_non_player_bonus': 'proc', 'upgrade_non_player_bonus_sacrifice': 'proc',
}
CONDKEY = re.compile(r'Threshold|MinimumDamage|MinRange|DamageRange|MaxStacks|ProcChance|DamageWindow|ToStack|PerHit|PerKill')

def tlabel(t): return 'L' if t < 0 else ('U' if t == 0 else 'T%d' % t)
def nm(R, sl): return R['b']['abil'][sl - 1]

def first_met(R, w0, model, test):
    """first moment after w0 (purchase or ability event) at which test(w,T) is true; returns (souls, what)."""
    ev = R['evA'] if model == 'A' else R['evB']
    moments = sorted(set([x['souls'] for x in R['rows'] if not x.get('unknown') and x['souls'] > w0['souls']] + [g for g, lv, a, t in ev if g > w0['souls']]))
    for s in moments:
        # owned items stay as at purchase (the item itself owned) until the next purchase passes
        later = [x for x in R['rows'] if not x.get('unknown') and x['souls'] <= s]
        w = state(R, dict(later[-1], souls=s)) if later else w0
        T = tiers_at(ev, s)
        if test(w, T):
            what = [f"{nm(R,a)} {tlabel(t)}" for g, lv, a, t in ev if g == s] + [x['n'] for x in R['rows'] if not x.get('unknown') and x['souls'] == s]
            return s, ', '.join(what)
    return None, None

def reorder_enable(R, slot, tier, by):
    """move occurrence `tier` of `slot` earlier in the order so it lands by souls `by`; returns (order, landed, slips)."""
    order = R['order']; L = R['L']; occ = [i for i, x in enumerate(order) if x == slot]
    if tier >= len(occ): return None
    j = occ[tier]; prev = occ[tier - 1] if tier >= 1 else -1
    base = {(x[2], x[3]): x[0] for x in R['evA']}
    for k in range(j - 1, prev, -1):   # latest position that still lands it in time = fewest slips
        o2 = order[:j] + order[j + 1:]; o2.insert(k, slot)
        m2 = {(x[2], x[3]): x[0] for x in model_A(o2, L)}
        if m2.get((slot, tier), 10 ** 9) <= by:
            slips = [f"{nm(R,q)[:14]} {tlabel(t)} {base[(q,t)]}->{m2.get((q,t))}" for (q, t) in base if m2.get((q, t)) != base[(q, t)] and (q, t) != (slot, tier)]
            return ''.join(map(str, o2)), m2[(slot, tier)], slips
    return None

def cond_row(R, w, model='A', rule2=True):
    it = item(w['n']); c = it['class']; kind = REG.get(c)
    T = w['t' + model]; s = w['souls']; ab = R['abil']
    if not kind:
        keys = [k for k in it['vstats'] if CONDKEY.search(k) and num(it['vstats'][k]) not in (None, 0, -1)]
        if w['imb']: kind = 'imbue'
        elif keys: return {'item': w['n'], 'souls': s, 'kind': '?', 'rule': 'condition keys ' + ','.join(keys) + ' - rule not encoded', 'verdict': 'UNCHECKED', 'grade': '-', 'flag': 'UNCHECKED'}
        else: return None
    row = {'item': w['n'], 'souls': s, 'kind': kind, 'value': '', 'margin': '', 'rel': '', 'enabler': '', 'verdict': 'buy now', 'grade': 'CALCULATED', 'flag': None, 'gap': None, 'rule': '', 'src': '', 'unver': ''}
    d = desc(c); row['src'] = (d[:150] + ('...' if len(d) > 150 else '')) if d else '(no game text)'
    pr = proc_rules(c)
    if pr: row['src'] += ' | vdata: ' + pr
    parts = kind.split('+')
    if 'hit' in parts or 'hitimb' in parts:
        thr = sv(it, 'MinimumDamage'); only = [w['imb']] if 'hitimb' in parts and w['imb'] else None
        row['rule'] = f"one ability damage instance > {thr:.0f} ({'imbued ability only' if only else 'any ability'}); scaled by spirit at hit time; procs at most every {sv(it,'AbilityChargeUpTime') or sv(it,'AbilityCooldown'):.0f}s"
        row['unver'] = 'pre- vs post-resist damage, whether DoT ticks/item damage count, whether ult counts (code, not data)'
        v, sl, k, above = best_hit(R, w, T, thr, only)
        v2, _, _, above2 = best_hit(R, w, T, thr, only, cond=False)
        row['value'] = f"best {nm(R,sl) if sl else '-'}.{k} {v:.0f} at spirit {w['sp']:.0f}" + (f" ({v2:.0f} without conditional spirit)" if abs(v2 - v) > 0.5 else '')
        row['margin'] = f"{(v/thr-1)*100:+.0f}%" if thr else ''
        spam = [a for a in above if R['abil'][a[0]]['type'] != 'EAbilityType_Ultimate']
        row['rel'] = ('procs from ' + ', '.join(f"{nm(R,a[0])}.{a[1]} {a[2]:.0f} (cd {a[3]:g})" for a in above)) if above else 'no qualifying hit'
        below = [f"{nm(R,q)}.{k} {v:.0f}" for q in (only or (1, 2, 3, 4)) if T[q] >= 0 for k, (v, inst) in spirit_hits(at_tier(ab[q], T[q]), slot_sp(R, w, q, T[q])).items() if inst and v <= thr]
        if below: row['rel'] += '; below threshold: ' + ', '.join(below)
        if any(re.match('Max', a[1]) for a in above) and not any(not re.match('Max', a[1]) for a in above): row['rel'] += ' - ONLY THE FULLY CHARGED/MAX VALUE qualifies'
        if above and not spam: row['rel'] += ' - ULT ONLY (low uptime)'
        wsc = [f"{nm(R,q)}.{k}" for q in (only or (1, 2, 3, 4)) if T[q] >= 0 for k, pp in at_tier(ab[q], T[q]).items() if pp.get('isdmg') and pp['stype'] in ('EWeaponPower', 'EWeaponDPS', 'EBaseWeaponDamageIncrease')]
        if wsc: row['unver'] += '; weapon-scaled ability damage not computed: ' + ', '.join(wsc)
        if v <= thr and wsc and not above:
            row['flag'] = 'UNCOMPUTED-WEAPON-SCALED'; row['verdict'] = 'check by hand / sandbox'; row['grade'] = 'UNTESTABLE-HIGH-RISK'
        elif v <= thr or (above and not spam):
            sm, what = first_met(R, w, model, lambda w2, T2: any(R['abil'][a[0]]['type'] != 'EAbilityType_Ultimate' for a in best_hit(R, w2, T2, thr, only)[3]))
            row['flag'] = 'BELOW-THRESHOLD' if v <= thr else 'ULT-ONLY'; row['gap'] = (sm - s) if sm else None
            row['enabler'] = f"met by a non-ult ability @{sm} ({what})" if sm else 'never met in this build'
            row['verdict'] = f"delay to ~{sm} or reorder/buy enabler first" if sm else 'skip/swap'
        elif v2 <= thr:
            row['flag'] = 'COND-SPIRIT'; row['verdict'] = 'buy now only if the conditional spirit is up (e.g. above 65% hp for Enchanter\'s Emblem)'
        elif v / thr < 1.15: row['verdict'] = 'buy now (thin margin)'
    if 'win' in parts:
        thr = sv(it, 'DamageThreshold'); win = sv(it, 'DamageThresholdDuration') or 5
        row['rule'] = f"{thr:.0f} spirit damage to one enemy within {win:.0f}s (game text: 'significant spirit damage'); per-enemy cooldown"
        row['unver'] = 'pre/post resist; item and DoT damage count (text says any spirit damage)'
        tot = 0; tot_nu = 0; det = []
        for sl in (1, 2, 3, 4):
            if T[sl] < 0: continue
            P = at_tier(ab[sl], T[sl]); hits = spirit_hits(P, slot_sp(R, w, sl, T[sl]))
            if not hits: continue
            ch = charges(ab[sl], T[sl]) + (sum(int(sv(i, 'BonusAbilityCharges')) for i in w['own'] if i['req'] == 'ERequirementChargedAbility') if charges(ab[sl], T[sl]) >= 2 else 0)
            bc = pv(P, 'AbilityCooldownBetweenCharge') or 0
            n = min(ch, 1 + int(win / bc)) if ch > 1 and bc > 0 else 1
            per = 0
            for k, (v, inst) in hits.items():
                dur = pv(P, 'AbilityDuration') or pv(P, 'AbilityChannelTime') or 1
                per += v if inst else v * min(win, dur)
            tot += per * n; det.append(f"{nm(R,sl)[:12]} {per:.0f}x{n}")
            if ab[sl]['type'] != 'EAbilityType_Ultimate': tot_nu += per * n
        row['value'] = f"all abilities in {win:.0f}s ~{tot:.0f} ({'; '.join(det)}), without ult {tot_nu:.0f}"
        row['margin'] = f"{(tot_nu/thr-1)*100:+.0f}% without ult, {(tot/thr-1)*100:+.0f}% with"
        row['grade'] = 'UNTESTABLE-HIGH-RISK'; row['rel'] = 'needs the whole combo on one target (hit rate, travel time)'
        if tot < thr: row['flag'] = 'KIT-ONLY-BELOW'; row['verdict'] = 'check by hand: abilities alone < threshold, item/proc spirit damage not counted'
        elif tot_nu < thr: row['verdict'] = 'buy now (needs ult in the combo)'
    if 'gunwin' in parts:
        thr = sv(it, 'DamageThreshold'); win = sv(it, 'DamageWindow')
        g, per, n = gun_window(R, w, win)
        row['rule'] = f"{thr:.0f} weapon damage within {win}s (game text: 'significant weapon damage'), refills one charge per charged ability; cd {sv(it,'AbilityCooldown'):.0f}s"
        row['value'] = f"gun {per:.0f}/bullet x {n} shots = {g:.0f} in {win}s (100% hits, base + level + weapon-invest + item weapon damage)"
        row['margin'] = f"{(g/thr-1)*100:+.0f}% at 100% hits; needs {thr/per:.1f} hits" if per else ''
        row['unver'] = 'falloff, headshots, accuracy; whether ability weapon-damage counts'
        if g < thr: row['flag'] = 'BELOW-THRESHOLD'; row['verdict'] = 'delay (gun cannot reach the threshold)'
        elif g < thr * 1.5: row['rel'] = f"needs >= {thr/g*100:.0f}% of shots to hit"
    if 'charged' in parts:
        req = 2 if rule2 else 1
        have = {sl: charges_raw(ab[sl], T[sl]) for sl in (1, 2, 3, 4) if T[sl] >= 0}
        multi = [sl for sl, ch in have.items() if ch >= req]
        add = int(sv(it, 'BonusAbilityCharges'))
        row['rule'] = (row['rule'] + '; ' if row['rule'] else '') + f"needs an ability with charges (vdata ERequirementChargedAbility); Kieran's reading = 2+ base charges (F7 UNVERIFIED: does a 1-charge ability count?)"
        row['unver'] = (row['unver'] + '; ' if row['unver'] else '') + 'F7 1-charge abilities'
        if multi:
            row['value'] = (row['value'] + '; ' if row['value'] else '') + ', '.join(f"{nm(R,sl)} {have[sl]}->{have[sl]+add} charges" for sl in multi)
            # burst value: charges usable inside a 5 s window = min(charges, 1 + floor(5 / between-charge delay))
            W = 5.0; bcr = sv(it, 'CooldownBetweenChargeReduction') / 100
            ownadd = sum(int(sv(i, 'BonusAbilityCharges')) for i in w['own'] if i['req'] == 'ERequirementChargedAbility' and i['n'] != w['n'] and i['n'] not in it['components']) if 'n' in (w['own'][0] if w['own'] else {}) else 0
            def burst(ch, bc): return min(ch, 1 + int(W / bc)) if bc and bc > 0 else ch
            gains = []
            for sl in multi:
                P = at_tier(ab[sl], T[sl]); bc = pv(P, 'AbilityCooldownBetweenCharge') or 0; ch = have[sl]
                b0 = burst(ch, bc); b1 = burst(ch + add, bc * (1 - bcr))
                gains.append((sl, b0, b1, bc))
                row['value'] += f"; {nm(R,sl)} shots in {W:g}s {b0}->{b1} (between-charge {bc:g}s)"
            if gains and all(b1 <= b0 for sl, b0, b1, bc in gains):
                ev = R['evA'] if model == 'A' else R['evB']
                for g, lv, a2, t2 in ev:
                    if g > s and a2 in multi and t2 >= 1 and any(pn in ('AbilityCooldownBetweenCharge', 'AbilityCharges') for pn, _, _ in ab[a2]['ups'][t2 - 1]):
                        P2 = at_tier(ab[a2], t2); bc2 = pv(P2, 'AbilityCooldownBetweenCharge') or 0; ch2 = charges(ab[a2], t2)
                        if burst(ch2 + add, bc2 * (1 - bcr)) > burst(ch2, bc2):
                            row['flag'] = 'WEAK-UNTIL-UPGRADE'; row['gap'] = g - s
                            row['enabler'] = f"burst gain starts at {nm(R,a2)} {tlabel(t2)} @{g} (+{g-s}): shots in {W:g}s {burst(ch2,bc2)}->{burst(ch2+add,bc2*(1-bcr))}; until then the extra charge is stored only (+sustained casts, + charged-only spirit)"
                            row['verdict'] = 'buy now if the stored charge / spirit is worth it, else after the upgrade (see worked example)'
                            ro = reorder_enable(R, a2, t2, s) if model == 'A' else None
                            if ro: row['enabler'] += f"; reorder {ro[0]} lands it @{ro[1]} (slips: {', '.join(ro[2]) or 'none'})"
                            break
            if 'CooldownBetweenChargeReduction' in it['vstats']:
                for sl in multi:
                    P = at_tier(ab[sl], T[sl]); cd = pv(P, 'AbilityCooldown') or 0; bc = pv(P, 'AbilityCooldownBetweenCharge') or 0
                    row['value'] += f" (cd {cd:g}->{cd*(1-sv(it,'CooldownReductionOnChargedAbilities')/100):.1f}s, between {bc:g}->{bc*(1-sv(it,'CooldownBetweenChargeReduction')/100):.2f}s)"
        else:
            ev = R['evA'] if model == 'A' else R['evB']
            fut = sorted([(g, a, t) for g, lv, a, t in ev if t >= 0 and charges_raw(ab[a], t) >= req and g > s])
            row['flag'] = 'DEAD-AT-BUY'; row['verdict'] = 'delay / reorder points'
            if fut:
                g, a, t = fut[0]; row['gap'] = g - s; row['enabler'] = f"{nm(R,a)} {tlabel(t)} @{g} (+{g-s})"
                ro = reorder_enable(R, a, t, s) if model == 'A' else None
                if ro: row['enabler'] += f"; reorder {ro[0]} lands it @{ro[1]} (slips: {', '.join(ro[2]) or 'none'})"
            else: row['enabler'] = 'no ability ever reaches the charge count'; row['verdict'] = 'skip/swap'
            row['value'] = 'no ability with charges now: ' + ', '.join(f"{nm(R,sl)} {ch}" for sl, ch in have.items())
    if 'imbue' in parts:
        sl = w['imb']
        if not sl: row['rule'] = 'imbue item with no imbue target in data.js'; row['flag'] = 'NO-IMBUE'; row['verdict'] = 'fix data'
        else:
            t = T[sl]; P = at_tier(ab[sl], max(t, 0)); cd = pv(P, 'AbilityCooldown') or 0; du = pv(P, 'AbilityDuration') or 0
            row['rule'] = f"imbued on {nm(R,sl)}; needs it trained" + (' and non-ultimate' if c == 'upgrade_ability_power_shard' else '') + ' and the stat the item raises'
            if t < 0:
                ev = R['evA'] if model == 'A' else R['evB']; f = [g for g, lv, a, tt in ev if a == sl and tt == 0]
                row['flag'] = 'IMBUED-LOCKED'; row['gap'] = (f[0] - s) if f else None; row['enabler'] = f"{nm(R,sl)} unlock @{f[0] if f else '-'}"; row['verdict'] = 'reorder points / delay'
            else:
                row['value'] = f"{nm(R,sl)} {tlabel(t)}: cd {cd:g}s, duration {du:g}s, charges {charges(ab[sl], t)}"
                if 'CooldownReduction' in it['vstats'] and cd:
                    r = sv(it, 'CooldownReduction') / 100; row['value'] += f"; saves {cd*r:.1f}s/cast ({60/cd:.2f}->{60/(cd*(1-r)):.2f} casts/min)"
                    nx = [(g, tt) for g, lv, a, tt in (R['evA'] if model == 'A' else R['evB']) if a == sl and g > s and tt >= 1 and any(p == 'AbilityCooldown' for p, _, _ in ab[sl]['ups'][tt - 1])]
                    if nx:
                        cd2 = pv(at_tier(ab[sl], nx[0][1]), 'AbilityCooldown'); row['enabler'] = f"after {tlabel(nx[0][1])} @{nx[0][0]} (+{nx[0][0]-s}): cd {cd2:g}, saves {cd2*r:.1f}s/cast, +{60/(cd2*(1-r))-60/cd2:.2f} casts/min vs +{60/(cd*(1-r))-60/cd:.2f} now"
                durp = [k for k, q in P.items() if q.get('v') and ('tech_duration' in q['sfun'] or 'ETechDuration' in q['sfun'] or 'EChannelDuration' in q['sfun'])]
                if 'BonusAbilityDurationPercent' in it['vstats']: row['value'] += '; duration-scaled props: ' + (', '.join(f"{k}={pv(P,k):g}" for k in durp) or 'NONE')
                if 'BonusAbilityDurationPercent' in it['vstats'] and not durp:
                    row['flag'] = 'NO-DURATION-STAT'; row['verdict'] = 'check (no AbilityDuration/ChannelTime on this ability; other duration props may scale)'
                if c == 'upgrade_ability_power_shard' and ab[sl]['type'] == 'EAbilityType_Ultimate': row['flag'] = 'ECHO-ON-ULT'; row['verdict'] = 'fix (Echo Shard is non-ultimate)'
                if 'ImbuedTechPower' in it['vstats']:
                    hits = spirit_hits(P, slot_sp(R, w, sl, t)); row['value'] += '; with imbue: ' + ', '.join(f"{k} {v:.0f}" for k, (v, inst) in hits.items())
                    if not hits: row['rel'] = 'imbued ability has no spirit-scaled damage (spirit only helps other scaled props)'
    if 'ult' in parts:
        t = T[4]; row['rule'] = 'needs the ultimate (damage from ult / reset value mostly from ult)'
        if t < 0:
            ev = R['evA'] if model == 'A' else R['evB']; f = [g for g, lv, a, tt in ev if a == 4 and tt == 0]
            row['flag'] = 'ULT-LOCKED'; row['gap'] = (f[0] - s) if f else None; row['verdict'] = 'delay'
        else: row['value'] = f"ult {tlabel(t)}, cd {pv(at_tier(ab[4], t), 'AbilityCooldown')}"
    if 'spiritsrc' in parts:
        src = [nm(R, sl) for sl in (1, 2, 3, 4) if T[sl] >= 0 and spirit_hits(at_tier(ab[sl], T[sl]), 0)]
        src += [i['class'] for i in w['own'] if i['class'] in ('upgrade_crackshot', 'upgrade_chain_lightning', 'upgrade_ethereal_bullets', 'upgrade_acolytes_glove', 'upgrade_spirit_snatch', 'upgrade_tech_damage_pulse', 'upgrade_magic_burst', 'upgrade_magic_shock')]
        row['rule'] = (row['rule'] + '; ' if row['rule'] else '') + 'needs spirit damage on enemies'; row['value'] = (row['value'] + '; ' if row['value'] else '') + 'spirit sources: ' + (', '.join(src) or 'NONE')
        if not src: row['flag'] = 'NO-SPIRIT-SOURCE'; row['verdict'] = 'delay'
        if 'stack' in parts and c == 'upgrade_escalating_exposure':
            row['rel'] = f"max {sv(it,'MaxStacks'):.0f} stacks, one per {sv(it,'ProcCooldown')}s of spirit hits = {sv(it,'MaxStacks')*sv(it,'ProcCooldown'):.1f}s of continuous spirit damage to max"
    for k in ('cast',):
        if k in parts:
            row['rule'] = row['rule'] or 'value scales with ability casts / trained abilities'
            tr = [sl for sl in (1, 2, 3, 4) if T[sl] >= 0]
            tot = sum((pv(at_tier(ab[sl], T[sl]), 'AbilityCooldown') or 0) for sl in tr)
            row['value'] = f"{len(tr)} abilities trained, summed cooldown {tot:.0f}s" + (f"; {sv(it,'CooldownReduction'):.0f}% saves {tot*sv(it,'CooldownReduction')/100:.1f}s per rotation" if sv(it, 'CooldownReduction') else '')
    for k, txt in (('taken', 'triggers on damage TAKEN from enemies (enemy-dependent)'), ('selfhp', 'depends on your own health %'), ('enemyhp', 'depends on enemy health %'),
                   ('range', 'depends on distance to target'), ('stack', 'needs repeated hits/kills to stack'), ('proc', 'chance/hit-based proc on bullets or kills'),
                   ('heal', 'needs a heal applied (not innate regen/lifesteal)'), ('melee', 'needs melee hits'), ('dash', 'needs a dash-jump then an ability')):
        if k in parts and not row['rule']:
            th = ', '.join(f"{kk}={it['vstats'][kk]}" for kk in it['vstats'] if CONDKEY.search(kk) or kk in ('LifeThreshold', 'EnemyLifeThreshold'))
            row['rule'] = txt + (f" ({th})" if th else ''); row['grade'] = 'UNTESTABLE-HIGH-RISK'; row['verdict'] = 'keep (situational; not a timeline check)'
            row['value'] = row['value'] or 'not computed (needs play data)'
    if c in COND_SP: row['rel'] = (row['rel'] + '; ' if row['rel'] else '') + f"its spirit is conditional: {COND_SP[c]}"
    return row

# ---------------- output ----------------
def fmt(R):
    b = R['b']; H = R['H']; ab = R['abil']; o = []
    o.append(f"# {b['id']} | {b['hero']} | {b['name']}")
    o.append('abilities: ' + ' / '.join(f"{i}={b['abil'][i-1]} ({H['ab'][i]}, start_trained={ab[i]['start']}, {ab[i]['type'].replace('EAbilityType_','')})" for i in (1, 2, 3, 4)))
    o.append('order: ' + ''.join(map(str, R['order'])))
    o.append('model A (data):  ' + '  '.join(f"{nm(R,a)[:10]}:{tlabel(t)}@{g}" for g, lv, a, t in R['evA']))
    o.append('model B (old):   ' + '  '.join(f"{nm(R,a)[:10]}:{tlabel(t)}@{g}" for g, lv, a, t in R['evB'] if g > 0))
    o.append('tier upgrades: ' + ' | '.join(f"{nm(R,i)[:12]}: " + ' / '.join(','.join(f"{p}{v:+g}{'x' if ty=='EAddToScale' else ''}" for p, v, ty in tt) for tt in ab[i]['ups']) for i in (1, 2, 3, 4)))
    o.append('\nsouls  lvl AP spirit  item [imbue]   || per ability: tier(A)[B if different] charges cd/between dur | spirit hit')
    for w in R['rows']:
        if w.get('unknown'): o.append(f"   ?? {w['n']} (not in items_full.json)"); continue
        o.append(f"{w['souls']:>6} L{w['lv']:<2} {w['ap']:>2} {w['sp']:>5.0f}  {w['n']}{' [imbue '+nm(R,w['imb'])+']' if w['imb'] else ''}")
        parts = []
        for sl in (1, 2, 3, 4):
            tA, tB = w['tA'][sl], w['tB'][sl]; lab = tlabel(tA) + ('' if tA == tB else '[' + tlabel(tB) + ']')
            if tA < 0: parts.append(f"{nm(R,sl)[:10]} {lab}"); continue
            P = at_tier(ab[sl], tA); cd = pv(P, 'AbilityCooldown'); bc = pv(P, 'AbilityCooldownBetweenCharge'); du = pv(P, 'AbilityDuration')
            hits = spirit_hits(P, slot_sp(R, w, sl, tA))
            parts.append(f"{nm(R,sl)[:10]} {lab} ch{charges(ab[sl], tA)} cd{cd:g}{'/'+format(bc,'g') if bc and bc>0 else ''}{' d'+format(du,'g') if du else ''}" + (' ' + ','.join(f"{k[:8]}={v:.0f}" for k, (v, inst) in list(hits.items())[:2]) if hits else ''))
        o.append('        ' + ' | '.join(parts))
    o.append('\n## conditional / ability-related items (model A; [B] shown where the verdict differs; F7 = 1-charge question)')
    rows = []
    for w in R['rows']:
        if w.get('unknown'): continue
        ra = cond_row(R, w, 'A'); rb = cond_row(R, w, 'B'); r1 = cond_row(R, w, 'A', rule2=False)
        if not ra: continue
        ra['B'] = rb['flag'] if rb else None; ra['F7'] = r1['flag'] if r1 else None; rows.append(ra)
        dep = []
        if rb and rb['flag'] != ra['flag']: dep.append(f"MODEL-DEPENDENT (B: {rb['flag'] or 'OK'})")
        if r1 and r1['flag'] != ra['flag']: dep.append(f"F7-DEPENDENT (1-charge counts: {r1['flag'] or 'OK'})")
        o.append(f"- @{w['souls']} {w['n']} [{ra['kind']}] -> {ra['flag'] or 'OK'} | verdict: {ra['verdict']} | {ra['grade']}" + (' | ' + ' '.join(dep) if dep else '') + (f" | gap {ra['gap']}" if ra.get('gap') else ''))
        for k, lab in (('rule', 'rule'), ('src', 'game text'), ('value', 'at buy'), ('margin', 'margin'), ('rel', 'reliability'), ('enabler', 'enabler/next'), ('unver', 'unverified')):
            if ra.get(k): o.append(f"    {lab}: {ra[k]}")
    unl = [w['n'] for w in R['rows'] if not w.get('unknown') and not cond_row(R, w, 'A')]
    o.append('\nno trigger condition (plain stats/actives): ' + ', '.join(unl))
    return '\n'.join(o), rows


# ---------------- gate (machine-readable verdict) ----------------
ERR = {'IMBUED-LOCKED', 'ECHO-ON-ULT', 'NO-IMBUE', 'BELOW-THRESHOLD'}
WARN = {'WEAK-UNTIL-UPGRADE', 'ULT-ONLY', 'KIT-ONLY-BELOW', 'UNCOMPUTED-WEAPON-SCALED', 'COND-SPIRIT', 'NO-SPIRIT-SOURCE', 'ULT-LOCKED', 'UNCHECKED', 'NO-DURATION-STAT'}
COLS = {'WeaponMod': 'gun', 'Armor': 'vitality', 'Tech': 'spirit'}
def spikes(R):
    """souls-spent per colour on items held (components consumed, sells dropped) and the purchase at which 4.8k / 6.4k is first held."""
    out = {c: {'4800': None, '6400': None, 'overshoot4800': None} for c in COLS.values()}
    for w in R['rows']:
        if w.get('unknown'): continue
        inv = {c: 0 for c in COLS.values()}
        for i in w['own']: inv[COLS[i['slot']]] += SOULS[i['tier']]
        for c, v in inv.items():
            for th in ('4800', '6400'):
                if out[c][th] is None and v >= int(th):
                    out[c][th] = w['souls']
                    if th == '4800': out[c]['overshoot4800'] = v - 4800; out[c]['at_item'] = w['n']
    return out
def gate(b):
    R = analyse(b); txt, rows = fmt(R)
    errors, warns = [], []
    for r in rows:
        f = r['flag']; base = {'item': r['item'], 'souls': r['souls'], 'kind': r['kind'], 'flag': f, 'gap': r.get('gap'), 'verdict': r['verdict'], 'grade': r['grade'],
                               'model_B': r.get('B'), 'if_1charge_counts': r.get('F7'), 'rule': r.get('rule'), 'value': r.get('value'), 'enabler': r.get('enabler')}
        if f == 'DEAD-AT-BUY':
            # charge item before any charges: error only if dead under BOTH readings of F7, else warning tagged F7
            (errors if r.get('F7') == 'DEAD-AT-BUY' else warns).append(dict(base, code='CHARGE-BEFORE-CHARGES', depends=None if r.get('F7') == 'DEAD-AT-BUY' else 'F7'))
        elif f in ERR: errors.append(dict(base, code=f))
        elif f in WARN: warns.append(dict(base, code=f))
        elif r.get('margin', '').startswith('+') and r['kind'] in ('hit', 'hitimb'):
            try:
                if float(r['margin'].strip('+%')) < 15: warns.append(dict(base, code='THIN-MARGIN'))
            except ValueError: pass
        if r.get('B') != f and f not in ('DEAD-AT-BUY',):
            warns.append(dict(base, code='MODEL-DEPENDENT', note=f"model A {f or 'OK'} vs model B {r.get('B') or 'OK'}"))
    sp = spikes(R)
    for c, d in sp.items():
        if d['overshoot4800'] is not None and d['overshoot4800'] >= 800:
            warns.append({'code': 'SPIKE-OVERSHOOT', 'colour': c, 'souls': d['4800'], 'item': d.get('at_item'), 'value': f"{c} lands at {4800 + d['overshoot4800']} (4.8k + {d['overshoot4800']})"})
    return {'id': b['id'], 'hero': b['hero'], 'order': ''.join(map(str, R['order'])), 'status': 'FAIL' if errors else ('WARN' if warns else 'PASS'),
            'errors': errors, 'warnings': warns, 'spikes': sp,
            'timeline_A': [{'souls': g, 'level': lv, 'ability': nm(R, a), 'tier': tlabel(t)} for g, lv, a, t in R['evA']],
            'rows': [{k: r.get(k) for k in ('item', 'souls', 'kind', 'flag', 'verdict', 'grade', 'margin', 'gap', 'B', 'F7')} for r in rows],
            'assumptions': {'game_build': '6801 (gt repo); installed client 6819 unverified', 'point_model': 'A (unlock currency separate, 1/2/5 AP)', 'charge_rule': "2+ charges (Kieran); F7 alternative reported",
                            'walk': 'core boxes L-R, components consumed, sells dropped'}}, txt

# ======================================================================================================
# OVERLAP-CANDIDATES + IN-BUILD MARGINAL VALUE (WEAKNESS_PROCESS J/L/M; Kieran 12:26 + 12:31 corrections)
# Overlap is only a CANDIDATE signal (same effect class / same need family as an owned item or hero ability at the checkpoint).
# A candidate is then valued INSIDE the complete build: owned items, ability tiers, real cooldowns/durations, a use-rate for actives, with-vs-without
# (components held instead of the upgrade), and vs other items of the same cost already listed in the build. Output class per item:
#   ADDS-VALUE | COMPLEMENTS (different window / damage type) | REDUNDANT-LIKELY | UNKNOWN (+ the test needed).  Nothing here blocks on text similarity.
# usage: python3 -I abtimeline.py --overlap [ids] [--build-file f.js] [--json] [--only-flags]   |   --context <id> <item> <outfile> [--build-file f]
G69 = None
def g69():
    global G69
    if G69 is None:
        try: G69 = json.load(open(SP + '/audit/items_full_6819.json'))
        except Exception: G69 = {}
    return G69
# property-key -> effect class (regex fullmatch on the game-data key), defining? (flat side stats are not "the item's job")
KEYCLASS = [
 (r'BonusClipSizePercent|BonusClipSize|MaxClipBonus|BonusClipPerKill|ExtraLargeClip', 'clip_size', True),
 (r'AmmoReloadPercent|ActiveReloadPercent|ReloadSpeedMultipler|BulletsReloadedPer\w+|AmmoPerSoul', 'reload_refill', True),
 (r'UnlimitedAmmo|NoClipDuration', 'unlimited_ammo', True),
 (r'BonusFireRate|ActiveBonusFireRate|FireRateBonus|FervorFireRate|FireRatePerKill|ActivatedFireRate|AmbushBonusFireRate|PeakFireRateBonus|BonusFireRatePerStack|FireRatePerStack', 'fire_rate', True),
 (r'BaseAttackDamagePercent\w*|BonusDamagePercent|CloseRangeBonusWeaponPower|LongRangeBonusWeaponPower|HeadShotBonusDamage', 'bullet_damage', False),
 (r'BulletLifestealPercent|ActiveBonusLifesteal|BulletLifesteal|LifeStealPercentOnHit', 'bullet_lifesteal', True),
 (r'AbilityLifestealPercentHero\w*|BonusSpiritLifesteal|ImbueAbilityLifesteal|TechLifestealPercent', 'spirit_lifesteal', True),
 (r'MeleeLifesteal|LifestrikeHeal|MeleeLifestealNonHeroPct', 'melee_lifesteal', True),
 (r'HealAmount|HealPercentAmount|HealOnKill|HealOnActivate|HealingPerCast|HealOnSuccess|HealFromHero|HeartHeal|HealingPerSecond|HealMaxHealth\w*|HealOnHit', 'active_heal', True),
 (r'BonusHealthRegen|Regeneration|HealthRegen|HealRegen|TotalHealthRegen', 'regen', True),
 (r'CombatBarrier|VexBarrierCombatBarrier|GuardianWardCombatBarrier|BulletShieldHealth', 'barrier', True),
 (r'HealAmpCastPercent|HealAmpRegenPercent|HealingEffectivenessPercent', 'heal_amp', True),
 (r'BulletResist|BuffBulletResist|BulletResistOnActive|BulletResistPerStack|BulletResistBelowThreshold', 'bullet_resist', True),
 (r'TechResist|BuffTechResist|TechArmorDamageReduction|TechResistBelowThreshold|SpiritResist', 'spirit_resist', True),
 (r'CooldownReduction|ItemCooldownReduction|UltimateCooldownReduction|CooldownReductionOnChargedAbilities|ImbuedCooldownReduction|ImbuedCooldownMultiplier', 'cooldown', True),
 (r'BonusAbilityCharges|BonusAbilityChargesNonCharge|EnableAbilityCharges|CooldownBetweenChargeReduction', 'charges', True),
 (r'BonusAbilityDurationPercent', 'duration', True),
 (r'TechRangeMultiplier|TechRadiusMultiplier|BonusAttackRangePercent|BonusItemRangePercent', 'range', True),
 (r'BonusMoveSpeed|ActiveBonusMoveSpeed|BuffMoveSpeedBonus|MaxBonusMoveSpeedPercent', 'move_speed', True),
 (r'SlowPercent|MovementSpeedSlow|FireRateSlow|MoveSlowPercent|MovementSlowPct', 'slow', True),
 (r'StunDuration|StunDurationSelf', 'stun', True), (r'SilenceDuration', 'silence', True),
 (r'DispelDebuffs|DispelOnUse|StatusResistancePercent|StatusImmuneDuration', 'cleanse', True),
 (r'ProcChance|BuildUpPerShot|BuildUpBulletPercentPerHit', 'bullet_proc', True),
 (r'BulletResistReduction|MagicResistReduction|BulletArmorReduction|SpiritResistReduction|TechResistDebuff', 'resist_shred', True),
 (r'ImbuedTechPower', 'imbue_spirit', True),
 (r'TechPower|SpiritPower|BonusSpirit|TechPowerPercent', 'spirit_power', False), (r'BonusHealth|BonusBaseHealth', 'health', False),
 (r'OutOfCombatHealthRegen', 'regen_ooc', False), (r'BonusSprintSpeed', 'sprint', False),
]
KC = [(re.compile('(?:' + p + ')$'), c, d) for p, c, d in KEYCLASS]
FAMILY = {'clip_size': 'ammo', 'reload_refill': 'ammo', 'unlimited_ammo': 'ammo', 'bullet_lifesteal': 'sustain', 'spirit_lifesteal': 'sustain', 'melee_lifesteal': 'sustain',
          'active_heal': 'sustain', 'regen': 'sustain', 'barrier': 'sustain'}
# classes whose duplication can plausibly waste souls (stacking move speed / procs / range etc. is not treated as overlap; they are still classified and cited)
CAND_CLASSES = {'clip_size', 'reload_refill', 'unlimited_ammo', 'fire_rate', 'bullet_lifesteal', 'spirit_lifesteal', 'melee_lifesteal', 'active_heal', 'regen', 'barrier', 'bullet_resist', 'spirit_resist', 'cooldown', 'cleanse', 'stun', 'silence', 'slow'}
CROSS_CLASS = {'ammo', 'sustain'}     # different mechanisms meeting the same NEED: candidates across classes. Other classes: candidate only on the same class.
WINDOW = {'bullet_lifesteal': 'while shooting', 'spirit_lifesteal': 'while casting', 'melee_lifesteal': 'while meleeing', 'active_heal': 'on cooldown (burst)',
          'regen': 'between/after fights', 'barrier': 'on cooldown (buffer)'}
THR = {'ammo': 8.0, 'rate': 8.0, 'sustain': 20.0, 'resist': 5.0, 'cdr': 8.0}   # % marginal below which the overlapped role is "low"
RELOAD_S = {'citadel_weapon_wraith_set': (2.82, 'measured 2.82 s in council/sandbox/results/wraith_gun_PR-W1.md')}
USE_RATES = (1.0, 0.5)        # fraction of active cooldowns the player actually uses in a fight (1.0 = upper bound for sources, 0.5 = verdict basis)
_MS = {}
def mstats(n):
    if n in _MS: return _MS[n]
    it = item(n); s = {}
    if it: s.update(it['vstats'])
    s.update((g69().get(n) or {}).get('stats', {}))
    _MS[n] = {k: num(v) for k, v in s.items() if num(v) is not None}; return _MS[n]
def classify_props(P, tag=None):
    out = []
    for k, v in P.items():
        if not v: continue
        if v < 0 and not re.search(r'Reload|Reduction|Shred', k) or (v < 0 and k == 'TechArmorDamageReduction'): continue   # negative values are debuffs on enemies (e.g. Mystic Vulnerability TechArmorDamageReduction=-8), not the holder's own stat
        for rx, c, d in KC:
            if rx.match(k): out.append(dict(cls=c, key=k, val=v, defining=d, window=('on cooldown (burst)' if k == 'ActiveBonusLifesteal' else WINDOW.get(c)))); break
    return out
def item_classes(n):
    s = mstats(n); out = classify_props(s)
    txt = ((g69().get(n) or {}).get('text_extra', '') + ' ' + (g69().get(n) or {}).get('desc', '')).lower()
    if not any(c['cls'] == 'reload_refill' for c in out) and 'reload' in txt and 'lifesteal' not in txt:
        out.append(dict(cls='reload_refill', key='text_extra:"reload"', val=1, defining=True, window=None))
    return out
def ability_classes(R, slot, tier):
    if tier < 0: return []
    a = R['abil'][slot]; P = at_tier(a, tier); out = classify_props({k: p.get('v') for k, p in P.items()})
    ch = pv(P, 'AbilityCharges') or 0
    if ch >= 2: out.append(dict(cls='charges', key='AbilityCharges', val=ch, defining=True, window=None))
    return out
def cdr_pct(own): return min(60.0, sum(mstats(i['n'] if 'n' in i else '').get('CooldownReduction', 0) for i in own))
def cite_item(n, c): return f"{n}.{c['key']}={c['val']:g}"
def cite_ab(R, slot, t, c): return f"ability{slot} {R['b']['abil'][slot-1]} {tlabel(t)}: {c['key']}={c['val']:g}"

def sources_at(R, own_names, imbues, T, exclude):
    """owned effect sources at a checkpoint: items (imbue items only if imbued) + hero abilities at their current tier."""
    S = []
    for n in own_names:
        if n in exclude: continue
        for c in item_classes(n):
            if not c['defining']: continue
            if item(n) and R and item(n)['class'] in REG and REG[item(n)['class']] == 'imbue' and n not in imbues:
                S.append(dict(src=n, kind='item', c=dict(c, note='NOT IMBUED: inactive'), active=False, cite=cite_item(n, c) + ' (not imbued)')); continue
            S.append(dict(src=n, kind='item', c=c, active=True, cite=cite_item(n, c)))
    for sl in (1, 2, 3, 4):
        for c in ability_classes(R, sl, T[sl]):
            if c['defining'] or c['cls'] == 'charges': S.append(dict(src=R['b']['abil'][sl - 1], kind='ability', slot=sl, c=c, active=True, cite=cite_ab(R, sl, T[sl], c)))
    return S

# ------------- gun-economy model (ammo / fire rate / damage / lifesteal) -------------
_MI = None
def measured_inputs():
    """ingested sandbox measurements (council/sandbox/results/measured_inputs.json: {weapon class: {reload_s, src}}); only VALID result files may be entered."""
    global _MI
    if _MI is None:
        try: _MI = json.load(open(SP + '/council/sandbox/results/measured_inputs.json'))
        except Exception: _MI = {}
    return _MI
def weapon(R):
    b = block('abilities.vdata', R['H']['wpn']) or ''
    g = lambda k, d=0.0: float((re.search(k + r' = ([0-9.\-]+)', b) or [None, d])[1])
    vr = re.search(r'm_reloadDuration = ([0-9.]+)', b)   # reload duration IS in the weapon block (correction 2026-10-24: earlier text said 'not in vdata' and assumed 2.5 s; Wraith vdata 2.82 equals the sandbox-measured 2.82)
    rl = RELOAD_S.get(R['H']['wpn'], (float(vr.group(1)), 'VERIFIED GAME MECHANIC m_reloadDuration (weapon vdata; Wraith value equals its sandbox measurement)') if vr else (2.5, 'ASSUMED 2.5 s: no m_reloadDuration in the weapon block'))
    mi = measured_inputs().get(R['H']['wpn'], {})
    if mi.get('reload_s'): rl = (float(mi['reload_s']), f"CONTROLLED SANDBOX RESULT {mi.get('src', '?')}")
    if R.get('_rl'): rl = (rl[0] * R['_rl'], rl[1] + f' x{R["_rl"]:g} (UNKNOWN-cell reading)')
    return dict(dmg=g('m_flBulletDamage'), cyc=g('m_flCycleTime', 1) or 1, pel=g('m_iBullets', 1) or 1, clip=g('m_iClipSize', 10), reload=rl[0], reload_src=rl[1])
def contrib(name, R, T=None, cdr=0.0, ability_slot=None):
    """gun-relevant contributions of one item (or one ability at its tier): clip%, damage%, passive/active fire rate, refills, unlimited ammo, bullet lifesteal."""
    if ability_slot:
        s = {k: p.get('v') for k, p in at_tier(R['abil'][ability_slot], T[ability_slot]).items() if p.get('v')}
        cd = (s.get('AbilityCooldown') or 0) * (1 - cdr / 100); dur = s.get('AbilityDuration') or 0; cls = ''
    else:
        s = mstats(name); it = item(name); cls = it['class'] if it else ''
        cd = s.get('AbilityChargeUpTime') or s.get('AbilityCooldown') or 0; dur = s.get('BuffDuration') or s.get('AbilityDuration') or 0
    c = dict(reload_pct=s.get('ReloadSpeedMultipler', 0), clip_pct=s.get('BonusClipSizePercent', 0) + s.get('MaxClipBonus', 0), dmg_pct=s.get('BaseAttackDamagePercent', 0), fr_perm=0.0, fr_act=[], refill=[], unl=None, ls_perm=0.0, ls_act=[])
    cond_fr = cls in ('upgrade_healbuff', 'upgrade_tech_overflow', 'upgrade_quick_silver', 'upgrade_ethereal_bullets')
    fr = s.get('BonusFireRate', 0) + s.get('FireRateBonus', 0) + s.get('FireRatePerKill', 0)
    if fr:
        if ability_slot or cond_fr: c['fr_act'].append((fr, dur or 5, cd or 20, True))
        elif s.get('ActiveBonusFireRate'): pass
        else: c['fr_perm'] += fr
    if s.get('ActiveBonusFireRate'): c['fr_act'].append((s['ActiveBonusFireRate'], s.get('AbilityDuration') or 5, cd or 30, True))
    if s.get('ActivatedFireRate'): c['fr_act'].append((s['ActivatedFireRate'], s.get('AbilityDuration') or 4.5, s.get('AbilityCooldown') or 9.0, False))   # on-hit trigger; 9 s internal cooldown ASSUMED (not in data; scenario harrow_burst_fire_ally)
    c['unmodeled'] = [k for k in s if re.match(r'Fervor\w*FireRate|FireRatePerStack|BonusFireRatePerStack|PeakFireRateBonus|AmbushBonusFireRate', k)]
    if s.get('AmmoReloadPercent'): c['refill'].append((s['AmmoReloadPercent'] / 100, cd or 18))
    if s.get('ActiveReloadPercent'): c['refill'].append((s['ActiveReloadPercent'] / 100, cd or 30))
    if s.get('UnlimitedAmmo'): c['unl'] = (dur or 5, cd or 30)
    ls = s.get('BulletLifestealPercent', 0)
    c['ls_perm'] = ls
    if s.get('ActiveBonusLifesteal'): c['ls_act'].append((s['ActiveBonusLifesteal'], s.get('AbilityDuration') or 5, cd or 30))
    return c
def sim(W, clip, cyc, reload, refills, unl, use):
    """bullets fired in W s of continuous fire: greedy refill use when empty and ready, else reload; unlimited-ammo window cast on cooldown. refills=[(frac,interval)]."""
    t = 0.0; ammo = clip; fired = 0.0; ready = [0.0] * len(refills); un_end = -1.0; un_next = 0.0
    while t < W:
        if unl and t >= un_next: un_end = t + unl[0]; un_next = t + max(unl[1] / use, unl[0])
        if t < un_end or ammo >= 1:
            fired += 1
            if t >= un_end: ammo -= 1
            t += cyc
        else:
            k = next((i for i, r in enumerate(ready) if r <= t), None)
            if k is not None: ammo = min(clip, clip * refills[k][0]); ready[k] = t + refills[k][1] / use
            else: t += reload; ammo = clip
    return fired
def strip_c(c, groups, held=()):
    """the item's contribution with the overlapped groups reduced to what its held components already gave (= 'without the overlapped role')."""
    c = dict(c)
    if 'clip' in groups: c['clip_pct'] = sum(h['clip_pct'] for h in held); c['reload_pct'] = sum(h['reload_pct'] for h in held)
    if 'refill' in groups: c['refill'] = [r for h in held for r in h['refill']]
    if 'unl' in groups: c['unl'] = next((h['unl'] for h in held if h['unl']), None)
    if 'fr' in groups: c['fr_perm'] = sum(h['fr_perm'] for h in held); c['fr_act'] = [f for h in held for f in h['fr_act']]
    return c
def gun_model(R, w, items_in, abil_T, cdr, W, use, strip=None):
    """damage proxy (bullets x per-bullet multiplier) over W s, and bullet-lifesteal heal, for a set of owned items + hero abilities. `only`: restrict to groups."""
    wp = weapon(R); cons = [(strip_c(contrib(n, R, cdr=cdr), strip[1], [contrib(h, R, cdr=cdr) for h in strip[2]]) if strip and n == strip[0] else contrib(n, R, cdr=cdr)) for n in items_in]
    for sl in (1, 2, 3, 4):
        if abil_T[sl] >= 0: cons.append(contrib(None, R, T=abil_T, cdr=cdr, ability_slot=sl))
    allow = lambda g: True
    clip = (wp['clip'] + hsc(R, w, 'EClipSize')) * (1 + (sum(c['clip_pct'] for c in cons) if allow('clip') else 0) / 100)   # hero scaling (e.g. clip per spirit) added to base, then %
    frp = sum(c['fr_perm'] for c in cons) if allow('fr') else 0
    fra = sum(f * min(1.0, d / (cdw / use if sc else cdw)) for c in cons for f, d, cdw, sc in c['fr_act']) if allow('fr') else 0
    cyc = wp['cyc'] / (1 + (frp + fra + hsc(R, w, 'EFireRate')) / 100)
    refills = [r for c in cons for r in c['refill']] if allow('refill') else []
    unl = None
    if allow('unl'):
        u = [c['unl'] for c in cons if c['unl']]
        if u: unl = max(u, key=lambda x: x[0] / x[1])
    dmgm = 1 + (w['wb'] + sum(c['dmg_pct'] for c in cons)) / 100
    # whole-magazine quantisation would make a fixed window jumpy: average the window over +-15% (7 points)
    rl = wp['reload'] * max(0.3, 1 + sum(c['reload_pct'] for c in cons) / 100)   # ReloadSpeedMultipler assumed = % change of reload TIME (-10 = 10% faster); UNVERIFIED
    b = sum(sim(W * (1 + d), max(1, clip), cyc, rl, refills, unl, use) for d in (-.15, -.1, -.05, 0, .05, .1, .15)) / 7
    dmg = b * (wp['dmg'] + w['boons'] * R['H']['bdl'] + hsc(R, w, 'EBulletDamage')) * wp['pel'] * dmgm
    ls = (sum(c['ls_perm'] for c in cons) + sum(p * min(1.0, d / (cdw / use)) for c in cons for p, d, cdw in c['ls_act'])) / 100 if allow('ls') else 0
    return dict(bullets=b, dmg=dmg, heal=dmg * ls, clip=clip, mag_s=clip * cyc, cyc=cyc, ls=ls, n_refill=len(refills), unl=unl)

def pct(a, b): return (a / b - 1) * 100 if b else 0.0

def estimate_item(R, st, n, prev_owned, sources, cands):
    """st: checkpoint dict(own_names, imbues, T, w). Returns dict(verdict, groups[...]) valued inside the complete build."""
    it = item(n); w = st['w']; T = st['T']; imb = st['imbues']
    held = [c for c in it['components'] if c in prev_owned]           # without the upgrade the player still holds its components
    with_items = [x for x in st['own_names']]
    wo_items = [x for x in with_items if x != n] + held
    cdr_w = cdr_pct([dict(n=x) for x in with_items]); cdr_wo = cdr_pct([dict(n=x) for x in wo_items])
    # imbue items are active only when imbued; non-imbued ones contribute nothing to the gun model
    act = lambda L: [x for x in L if not (item(x) and item(x)['class'] in REG and REG[item(x)['class']] == 'imbue' and x not in imb)]
    res = {'groups': []}; fams = sorted({FAMILY.get(x['c']['cls'], x['c']['cls']) for x in cands} & {FAMILY.get(c['cls'], c['cls']) for c in item_classes(n) if c['defining'] and c['cls'] in CAND_CLASSES}) if cands else []
    for fam in fams:
        grp = {'family': fam, 'sources': [s['cite'] for s in cands if FAMILY.get(s['c']['cls'], s['c']['cls']) == fam][:8], 'assumptions': []}
        mine = [c for c in item_classes(n) if c['defining'] and FAMILY.get(c['cls'], c['cls']) == fam]
        ic = {c['cls'] for c in mine}; grp['item_fields'] = [cite_item(n, c) for c in mine]
        if fam == 'ammo' or fam == 'fire_rate':
            part = ['clip', 'refill', 'unl'] if fam == 'ammo' else ['fr']
            wp = weapon(R); grp['assumptions'] += [f"continuous fire at 100% accuracy on a stationary target; reload {wp['reload']} s ({wp['reload_src']})",
                'refill/unlimited sources are used at a rate of `use` (1.0 = every time off cooldown, 0.5 = every other); first use available at fight start',
                'cooldown reduction from owned items applied to hero abilities; item active intervals = AbilityChargeUpTime|AbilityCooldown from data']
            rows = {}
            for W in (10, 20, 60):
                for use in USE_RATES:
                    full_w = gun_model(R, w, act(with_items), T, cdr_w, W, use); full_wo = gun_model(R, w, act(wo_items), T, cdr_wo, W, use)
                    # overlapped role only = with the item's other stats (damage%, fire rate/clip when not the overlapped family) held at the without-values
                    ov_wo = gun_model(R, w, act(with_items), T, cdr_w, W, use, strip=(n, part, held)); ov_w = full_w
                    rows[(W, use)] = dict(total=pct(full_w['dmg'], full_wo['dmg']), overlap_role=pct(ov_w['dmg'], ov_wo['dmg']), mag_with=full_w['mag_s'], mag_wo=full_wo['mag_s'], clip_w=full_w['clip'], clip_wo=full_wo['clip'], refills=full_w['n_refill'])
            grp['table'] = {f"{W}s/use{u}": {k: round(v, 1) for k, v in r.items()} for (W, u), r in rows.items()}
            key = (20, USE_RATES[-1]); v = rows[key]['overlap_role']; grp['metric'] = f"gun damage over 20 s, overlapped role only, use=0.5: {v:+.1f}%  (whole item {rows[key]['total']:+.1f}%)"
            grp['overlap_gain'] = v; grp['total_gain'] = rows[key]['total']; grp['range'] = (min(r['overlap_role'] for (W, u), r in rows.items() if W == 20), max(r['overlap_role'] for (W, u), r in rows.items() if W == 20))
            thr = THR['ammo'] if fam == 'ammo' else THR['rate']
            wd = [r['overlap_role'] for (W, u), r in rows.items() if u == 0.5]
            if v >= thr: grp['verdict'] = 'ADDS-VALUE'
            elif max(wd) >= thr: grp['verdict'] = 'COMPLEMENTS'; grp['why'] = 'overlapped role matters in a different window length (10/20/60 s: ' + ', '.join(f"{x:+.0f}%" for x in wd) + ')'
            else: grp['verdict'] = 'REDUNDANT-LIKELY'
            um = [k for k in contrib(n, R, cdr=0)['unmodeled']] if fam == 'fire_rate' else []
            if um and grp['verdict'] == 'REDUNDANT-LIKELY':
                grp['verdict'] = 'UNKNOWN'; grp['why'] = f"fire rate also comes from conditional keys not modelled ({', '.join(um)}: low-health / stack / ambush triggers)"; grp['needs_test'] = f"build-context test of {n} fire-rate uptime with its trigger condition met"
            if 'why' not in grp: grp['why'] = f"overlapped role adds {v:+.1f}% (threshold {thr}%), remaining roles of the item are valued separately (whole item {rows[key]['total']:+.1f}%)"
        elif fam == 'sustain':
            sw = {s['c'].get('window') for s in cands if FAMILY.get(s['c']['cls']) == 'sustain'}; iw = {c['window'] for c in mine}
            grp['windows'] = {'item': sorted(x for x in iw if x), 'owned sources': sorted(x for x in sw if x)}
            if iw and not (iw & sw):
                grp['verdict'] = 'COMPLEMENTS'; grp['why'] = f"item heals {sorted(iw)}; owned sources heal {sorted(sw)}: different windows of the fight (no stacking on the same damage)"
            elif iw == {'while shooting'}:
                a = gun_model(R, w, act(with_items), T, cdr_w, 20, 0.5); b = gun_model(R, w, act(wo_items), T, cdr_wo, 20, 0.5)
                v = pct(a['heal'], b['heal']) if b['heal'] else 999.0
                grp['metric'] = f"bullet-lifesteal heal over 20 s: {b['heal']:.0f} -> {a['heal']:.0f} hp ({'new source' if not b['heal'] else format(v, '+.0f') + '%'})"
                grp['overlap_gain'] = v; grp['verdict'] = 'ADDS-VALUE' if v >= THR['sustain'] else 'REDUNDANT-LIKELY'
                grp['why'] = 'same window (on bullet damage) and lifesteal % stacks additively on the same damage; weapon damage from the gun model'
                grp['assumptions'] += ['lifesteal fraction x gun damage (100% accuracy, stationary); healing amp, anti-heal and hero healing-output modifiers not applied']
            else:
                grp['verdict'] = 'UNKNOWN'; grp['why'] = 'same-window sustain from non-bullet sources cannot be priced from data alone'
                grp['needs_test'] = f"build-context fight sim: heal per 20 s of {n} with vs without, ability rotation cast (needs spirit damage / cast counts)"
        elif fam in ('bullet_resist', 'spirit_resist'):
            def r_of(L, cl):
                keep = 1.0
                for x in L:
                    for c in item_classes(x):
                        if c['cls'] == cl and c['defining']: keep *= 1 - min(0.9, c['val'] / 100)
                return 1 - keep
            rw, rwo = r_of(with_items, fam), r_of(wo_items, fam); v = ((1 - rwo) / (1 - rw) - 1) * 100
            grp['metric'] = f"effective hp vs that damage type: {v:+.1f}% (resist {rwo*100:.0f}% -> {rw*100:.0f}%)"; grp['overlap_gain'] = v
            grp['assumptions'].append('resist stacking assumed multiplicative on remaining damage (UNVERIFIED in sandbox)')
            grp['verdict'] = 'ADDS-VALUE' if v >= THR['resist'] else 'REDUNDANT-LIKELY'; grp['why'] = 'same damage type resist stacks'
        elif fam == 'cooldown' and not mstats(n).get('CooldownReduction'):
            grp['verdict'] = 'UNKNOWN'; grp['why'] = 'item cooldown effect is not the plain CooldownReduction stat (' + ', '.join(c['key'] for c in mine) + ')'
            grp['needs_test'] = f"build-context test: cast counts of the affected abilities with vs without {n} (charged-ability / imbue / ultimate CDR)"
        elif fam == 'cooldown':
            v = ((1 - cdr_wo / 100) / (1 - cdr_w / 100) - 1) * 100; grp['metric'] = f"ability cast rate: {v:+.1f}% (CDR {cdr_wo:.0f}% -> {cdr_w:.0f}%)"; grp['overlap_gain'] = v
            grp['assumptions'].append('CDR stacking assumed multiplicative, cap 60% (UNVERIFIED)')
            grp['verdict'] = 'ADDS-VALUE' if v >= THR['cdr'] else 'REDUNDANT-LIKELY'; grp['why'] = 'CDR from the same pool'
        else:
            grp['verdict'] = 'UNKNOWN'; grp['why'] = f"no pricing model for effect class '{fam}' in this tool"
            grp['needs_test'] = f"build-context test: {n} with vs without at this checkpoint for the {fam} stat (cast the relevant abilities, real tiers)"
        res['groups'].append(grp)
    ORD = ['UNKNOWN', 'REDUNDANT-LIKELY', 'COMPLEMENTS', 'ADDS-VALUE']
    # item verdict: the best PRICED role of the overlapped roles decides (a role that adds value in this build is not redundant); unpriced roles are listed
    pr = [g['verdict'] for g in res['groups'] if g['verdict'] != 'UNKNOWN']
    gun_total = max([g['total_gain'] for g in res['groups'] if 'total_gain' in g] or [None], key=lambda x: -1e9 if x is None else x)
    res['whole_item_gun_gain'] = gun_total
    res['verdict'] = (min(pr, key=lambda v: -ORD.index(v)) if pr else 'UNKNOWN') if res['groups'] else None
    if res['verdict'] in ('REDUNDANT-LIKELY', 'COMPLEMENTS') and gun_total is not None and gun_total >= THR['ammo']:
        res['verdict'] = 'ADDS-VALUE'; res['verdict_note'] = f"overlapped role is small but the whole item adds {gun_total:+.1f}% gun damage in this build (other roles)"
    res['unpriced_roles'] = [g['family'] for g in res['groups'] if g['verdict'] == 'UNKNOWN']
    return res

def checkpoint_state(R, w, which):
    T = tiers_at(R['evA'], w['souls']); return dict(own_names=list(w['owned']), imbues=dict(w['imbues']), T=T, w=w)
def overlap_build(b):
    R = analyse(b); rows = [r for r in R['rows'] if not r.get('unknown')]
    if not rows: return dict(id=b['id'], items=[])
    last = rows[-1]; endw = state(R, dict(last)); endst = checkpoint_state(R, endw, 'end'); out = []; prev = []
    seen = {}
    for r in rows: seen[r['n']] = r
    core_names = [r['n'] for r in rows]
    def one(n, w, where, st, prev_owned):
        it = item(n)
        if not it: return None
        cls = [c for c in item_classes(n) if c['defining'] and c['cls'] in CAND_CLASSES]
        S = sources_at(R, [x for x in st['own_names']], st['imbues'], st['T'], exclude={n} | set(it['components']))
        cands = []
        for s in S:
            if not s['active']: continue
            for c in cls:
                f1, f2 = FAMILY.get(c['cls'], c['cls']), FAMILY.get(s['c']['cls'], s['c']['cls'])
                if (c['cls'] == s['c']['cls']) or (f1 == f2 and f1 in CROSS_CLASS): cands.append(s); break
        if not cands: return dict(item=n, at=where, souls=w['souls'], candidate=False, verdict='NO-OVERLAP')
        est = estimate_item(R, st, n, prev_owned, S, cands)
        est['alternatives'] = alternatives(R, b, n, est, st, prev_owned)
        if est['verdict'] in ('REDUNDANT-LIKELY', 'UNKNOWN') or est['alternatives'].get('best_alt_beats_item'): est['alternatives'] = alternatives(R, b, n, est, st, prev_owned, True)   # also price same-tier catalog items (other uses of the same souls)
        return dict(item=n, at=where, souls=w['souls'], candidate=True, classes=sorted({c['cls'] for c in cls}), sources=[s['cite'] for s in cands][:10], **est)
    for i, w in enumerate(rows):
        n = w['n']; st = checkpoint_state(R, w, 'buy'); ws = state(R, dict(w))
        a = one(n, ws, 'at-buy', st, prev)
        # same item judged against the complete core (sources bought later, abilities at their final tier)
        endst2 = dict(endst); endst2['own_names'] = [x for x in endst['own_names']]
        if n not in endst2['own_names']: endst2['own_names'] = endst2['own_names'] + [n]   # item itself sold later: judge it as held
        upg = next((x for x in endst['own_names'] if x != n and n in item(x)['components']), None)
        bb = one(n, endw, 'core-end', endst2, prev) if not upg else None   # a component is judged through the upgrade that consumed it
        out.append(dict(item=n, box=w['box'], souls=w['souls'], at_buy=a, core_end=bb))
        prev = list(w['owned'])
    # optional boxes (no buy point): judged against the complete core
    for r in b['rows']:
        for box in r:
            if re.match(r'^(Early|Mid|Late)', box[0]): continue
            for x in box[3]:
                n = x[0]
                if n in core_names or not item(n): continue
                out.append(dict(item=n, box=box[0], souls=None, at_buy=None, core_end=one(n, endw, 'core-end', dict(endst, own_names=endst['own_names'] + [n]), endst['own_names'])))
    return dict(id=b['id'], hero=b['hero'], order=''.join(map(str, b['order'])), items=out)
ALT_NOTE = 'ALT-BETTER'
def alternatives(R, b, n, v, st, prev_owned, need_catalog=False):
    it = item(n); gun = [g for g in v.get('groups', []) if g['family'] in ('ammo', 'fire_rate') and 'total_gain' in g]
    if not gun: return {'note': 'cross-metric: no common metric with other purchases; needs build-context comparison (context file)'}
    held = [c for c in it['components'] if c in prev_owned]; base = [x for x in st['own_names'] if x != n] + held; w = st['w']; T = st['T']
    cost = lambda m: SOULS[item(m)['tier']] - sum(SOULS[item(c)['tier']] for c in item(m)['components'] if c in base)
    my_cost = cost(n); ok_cost = lambda m: abs(cost(m) - my_cost) <= 800   # alternatives must be bought with about the same souls
    z = gun_model(R, w, base, T, cdr_pct([dict(n=q) for q in base]), 20, 0.5); alts = []
    for r in b['rows']:
        for box in r:
            for x in box[3]:
                m = x[0]; mi = item(m)
                if not mi or m == n or m in st['own_names'] or mi['tier'] != it['tier'] or not ok_cost(m): continue
                if any(v < 0 for k, v in mstats(m).items() if k in ('BonusHealth', 'BulletResist', 'TechResist', 'MaxHealthLossPercent', 'HealAmpReceivePenaltyPercent')) or item(m)['class'] in REG and REG[item(m)['class']] in ('stack', 'proc', 'selfhp', 'stack+melee'): continue   # conditional / costed items are not a like-for-like alternative
                if all(c['cls'] not in ('clip_size', 'fire_rate', 'bullet_damage', 'reload_refill', 'unlimited_ammo') for c in item_classes(m)): continue
                a = gun_model(R, w, base + [m], T, cdr_pct([dict(n=q) for q in base + [m]]), 20, 0.5); alts.append((m, round(pct(a['dmg'], z['dmg']), 1)))
    alts = sorted(set(alts), key=lambda x: -x[1])[:4]; cat = []
    if need_catalog:
        for m, g in items().items():
            if g['tier'] != it['tier'] or g['slot'] != it['slot'] or g.get('disabled') or m == n or m in st['own_names'] or m in [a[0] for a in alts]: continue
            if not item(m) or not ok_cost(m) or all(c['cls'] not in ('clip_size', 'fire_rate', 'bullet_damage', 'reload_refill', 'unlimited_ammo') for c in item_classes(m)): continue
            if any(v < 0 for k, v in mstats(m).items() if k in ('BonusHealth', 'BulletResist', 'TechResist', 'MaxHealthLossPercent', 'HealAmpReceivePenaltyPercent')) or item(m)['class'] in REG and REG[item(m)['class']] in ('stack', 'proc', 'selfhp', 'stack+melee'): continue
            a = gun_model(R, w, base + [m], T, cdr_pct([dict(n=q) for q in base + [m]]), 20, 0.5); cat.append((m, round(pct(a['dmg'], z['dmg']), 1)))
        cat = sorted(cat, key=lambda x: -x[1])[:3]
    return {'catalog_alts': cat, 'metric': 'gun damage over 20 s, use=0.5; same-tier items already listed in this build, bought instead of the item', 'item_total': round(gun[0]['total_gain'], 1), 'alts': alts,
            'best_alt_beats_item': bool(alts and alts[0][1] > gun[0]['total_gain'] + 2)}
def needs_context(o):
    """gate trigger: overlap-candidate whose overlapped role is low/unknown at the buy point or in the complete core."""
    for k in ('at_buy', 'core_end'):
        v = o.get(k)
        if v and v.get('candidate') and (v.get('verdict') in ('REDUNDANT-LIKELY', 'UNKNOWN') or (v.get('alternatives') or {}).get('best_alt_beats_item')): return True
    return False
def fmt_overlap(res, only_flags=False):
    L = [f"== {res['id']} ({res.get('hero','')}) order {res.get('order','')}"]
    for o in res['items']:
        if only_flags and not needs_context(o): continue
        if not any((o.get(k) or {}).get('candidate') for k in ('at_buy', 'core_end')): continue
        L.append(f"- {o['item']} [{o['box']}{'' if o['souls'] is None else ' @'+str(o['souls'])}]")
        for k in ('at_buy', 'core_end'):
            v = o.get(k)
            if not v or not v.get('candidate'): continue
            L.append(f"    {k}: {v['verdict']}  classes {v['classes']}  overlap-candidates: {'; '.join(v['sources'][:5])}")
            for g in v['groups']:
                L.append(f"      [{g['family']}] {g['verdict']}: {g.get('metric', g.get('why'))}  | {g['why']}" + (f" | NEEDS: {g['needs_test']}" if g.get('needs_test') else ''))
                L.append(f"        item fields: {', '.join(g.get('item_fields', []))}")
            al = v.get('alternatives')
            if al: L.append(f"      alternatives: {al}")
    return '\n'.join(L)
def write_context(res, item_name, outfile, build_id):
    """build-context comparison file (kind `context`) generated from the model; the stated estimate is CALCULATED, not measured.
    Uses the checkpoint with the smallest margin (item minus best same-souls alternative) so the gate sees the worst case."""
    o = next(x for x in res['items'] if x['item'] == item_name); cps = [(k, o[k]) for k in ('at_buy', 'core_end') if o.get(k) and o[k].get('candidate')]
    def parts(ev):
        g = ev['groups'][0] if ev.get('groups') else {}; al = ev.get('alternatives') or {}
        pool = sorted((al.get('alts') or []) + (al.get('catalog_alts') or []), key=lambda x: -x[1]); best = pool[0] if pool else (None, None)
        tot = ev.get('whole_item_gun_gain'); tot = tot if tot is not None else g.get('overlap_gain')
        return g, al, best, tot, (tot - best[1] if (tot is not None and best[0]) else (tot if tot is not None else -999))
    k, ev = min(cps, key=lambda kv: parts(kv[1])[4]); g, al, best, tot, _ = parts(ev)
    T = ["SCOPE: build-context", "KIND: context", "VALID: yes (CALCULATED from game data by abtimeline.py --context; not a sandbox measurement)", f"BUILD: {build_id}",
         f"CHECKPOINT: {k} ({'souls ' + str(o['souls']) if k == 'at_buy' else 'complete core, item bought at ' + str(o['souls'])})", f"ITEM: {item_name}",
         "WITH: complete build at the checkpoint incl. the item (owned items, ability tiers, imbues; see sources below)",
         "WITHOUT: same build with the item removed and its components held",
         "ALT: " + (f"{best[0]} ({'listed in this build' if best[0] in [a[0] for a in al.get('alts', [])] else 'same-tier catalog item, not in build'}); also {al.get('alts')} {al.get('catalog_alts')}" if best[0] else "<FILL IN: no same-metric alternative computable; name the best alternative use of the same souls and its estimate>"),
         (f"ESTIMATE: {item_name} | item={tot:.1f}% | alt={best[0]} {best[1]:.1f}%" if (best[0] and tot is not None) else f"ESTIMATE: {item_name} | cannot estimate: needs {g.get('needs_test', 'a build-context test (no pricing model / no common metric)')}"),
         f"METRIC: {al.get('metric', g.get('metric', ''))}", f"VERDICT-BASIS: {ev['verdict']} at {k}"]
    for kk, e2 in cps: T.append(f"ESTIMATE-AT {kk}: verdict {e2['verdict']}, whole item {e2.get('whole_item_gun_gain')}")
    for gg in ev.get('groups', []): T += [f"GROUP {gg['family']}: {gg['verdict']} - {gg['why']}"] + ['  assumption: ' + a for a in gg.get('assumptions', [])] + ['  source: ' + s2 for s2 in gg['sources']]
    open(outfile, 'w').write('\n'.join(T) + '\n')


# ======================================================================================================
# STRATEGY: can the hero PLAY EFFECTIVELY with a purchase + ability-point path? (Kieran 13:56; WEAKNESS_PROCESS I/K/L/M/N)
# usage: python3 -I abtimeline.py --strategy <build id> <checkpoints: "4800,9600,16800" | "0-20000[:step]"> [--alt <alt file>]... [--out f]
#        [--set PARAM=value ...] [--grid full|quick]           -> writes a `strategy` evidence file (SCOPE: build-context, KIND: strategy)
#        python3 -I abtimeline.py --game-summary <strategy.txt | scenario.json>   -> the 3-4 GAME_SUMMARY lines (<=200 chars) for the in-game plugin
#        python3 -I abtimeline.py --spikes <build id>                            -> JSON: souls at which each colour first holds 4.8k (used by gate.js)
#        python3 -I abtimeline.py --verify-strategy <strategy.txt>                -> exit 0 if the BODY-SHA matches (not hand-edited after generation)
# Alternatives are generated from data (the build's own items + full item catalog + ability upgrade data), never hand-written:
#   A0 AS-BUILT | A1 RUSH-DMG-4.8K | A2 RUSH-VIT-4.8K | A3 SPREAD | A4 OFFENSIVE-GREENS | A5 DEFENSIVE-GREENS (delay the spike item)
#   A6 DEFENSIVE-POINTS (ability order) | A7 OFF-GREENS+DEF-POINTS | X* user/agent alternative files (--alt): {name, desc, path:[[item,note,imbue]...] | rows, order}
# Every quantity carries a tag: MEASURED (sandbox, validated) / CALCULATED (game data + stated formula) / ASSUMED (parameter, sensitivity-tested).
# The soul-income model is a stylised, explicit model with parameters (STRAT_P); every ranking is recomputed over a parameter grid and the
# conclusion is pre-registered: CHOSEN / DEPENDS ON ASSUMPTION / INSUFFICIENT EVIDENCE. Robustness % = share of grid cells, NOT a probability of being right.
import hashlib, bisect, math, itertools, datetime, glob
STRAT_VERSION = 'strategy-v1'
STRAT_P = {   # ASSUMED parameters (name: (central, grid values, meaning))
 'W':          (8.0, None, 'trade window s (both sides shoot/cast for W seconds)'),
 'I':          (30.0, None, 'seconds between lane trades (cooldown availability, between-trade regen)'),
 'hit':        (0.55, (0.35, 0.55, 0.75), 'share of your bullets that hit the enemy hero'),
 'melee_u':    (0.5, (0.3, 0.5, 0.7), 'share of a trade a melee-relevant hero spends in melee range (0 for non-melee kits)'),
 'close_u':    (0.8, None, 'share of gun damage dealt inside 15 m for close-range weapons (0.3 for others)'),
 'cond_u':     (0.6, None, 'uptime of health-gated item stats (Battle Vest/Enchanter above 65% hp)'),
 'enemy':      (1.0, (0.6, 1.0, 1.6), 'enemy power scale (poke dps and burst) vs the reference enemy'),
 'E_D0':       (70.0, None, 'reference enemy effective dps on you at 0 souls (after their hit rate)'),
 'E_B0':       (350.0, None, 'reference enemy burst (combo) at 0 souls'),
 'E_SPM':      (1000.0, None, 'reference enemy soul income per minute (RULES_KIERAN: ~1k/min early)'),
 'spirit_share': (0.3, None, 'share of enemy damage that is spirit (rest bullet)'),
 'lane_end':   (9.0, None, 'minute the lane phase ends'),
 'LANE_SPM':   (700.0, None, 'lane souls/min with an even lane (troopers + passive), before trade/back/death effects'),
 'FIGHT_SPM':  (500.0, None, 'souls/min from fights/objectives/waves after the lane phase, at trade ratio 1'),
 'beta':       (0.25, (0.0, 0.25, 0.5), 'how much winning trades raises lane/fight income: x(1+beta*tanh(ln TR)); 0 = trades never change income'),
 'F_LANE':     (0.15, (0.15, 0.4), 'share of lane-phase time spent clearing camps (farm-first playstyle = high)'),
 'F_MID':      (0.45, (0.3, 0.6), 'share of post-lane time spent farming camps/waves (farming playstyle = high)'),
 'V_CAMP':     (250.0, None, 'souls per camp'),
 'H_CAMP':     (1500.0, None, 'total camp hp (3 NPCs) at hp scale 1'),
 'hscale':     (1.0, (0.5, 3.0), 'camp hp scale: how much clear speed matters vs walking'),
 'travel':     (25.0, (10.0, 40.0), 'seconds walking between camps (clear-speed independent)'),
 'N_NPC':      (3.0, None, 'NPCs in a camp hit by bounces/chains/AoE'),
 'p2hero':     (0.15, (0.15, 0.5), 'chance a bounce/chain finds a second enemy hero in a fight (0.5 = teamfight-heavy games)'),
 'antiheal':   (0.0, (0.0, 0.35), 'enemy healing reduction on you (items: Healbane/Toxic -35, Inhibitor -40, Spirit Burn -70; GAPS 8: in 47/81 builds)'),
 'omega':      (0.0, (0.0, 0.4), 'wave-clear elasticity of lane/fight income: x(clear/ref_clear)^omega, ref = as-built clear at the reference soul curve (0 = clearing faster never earns more lane souls)'),
 'T_ESC':      (5.0, (3.0, 8.0), 'seconds a losing enemy needs to escape: a won engagement becomes a kill with chance min(1, T_ESC/TTK)'),
 'KILL0':      (150.0, None, 'souls per hero kill at 0 min (+20 per minute)'),
 'lost':       (0, (0, 1), 'lane state: 0 = even lane, 1 = lane lost (lane income x LOST_MULT, enemy +LOST_LEAD souls)'),
 'LOST_MULT':  (0.65, None, 'lane income multiplier when the lane is lost'),
 'LOST_LEAD':  (0.25, None, 'enemy soul lead when your lane is lost'),
 'BACK_S':     (45.0, None, 'seconds of lost income per forced back (walk to base and return)'),
 'ENG_LANE':   (0.25, None, 'all-in engagements per minute in lane'),
 'ENG_MID':    (0.35, None, 'engagements per minute after lane'),
 'ESC':        (0.3, None, 'share of losing engagements survived when an escape/mobility ability is trained'),
 'RESPAWN0':   (10.0, None, 'respawn s at 0 min (+1.2 s per minute)'),
 'OOC_DELAY':  (10.0, None, 's out of combat before out-of-combat regen applies'),
 'NPC_SOULS':  (50.0, None, 'souls of the NPC eaten by Cultist Sacrifice (bonus souls = BonusSoulsPct of it, once per cooldown)'),
 'p_heart':    (0.25, None, 'Card Trick suit odds per card (4 suits)'),
 'card_stored': (0.5, None, 'share of resource-gated card charges already stored when a trade starts'),
 'POKE':       (0.12, None, 'share of lane time you are being hit (HP budget -> forced backs)'),
 'OOC_SHARE':  (0.4, None, 'share of lane time out of combat long enough for out-of-combat regen'),
 'REFUND':     (0.5, None, 'share of the price returned when an item is sold (UNVERIFIED HYPOTHESIS: user-stated "half price", not in game data)'),
 'kappa':      (None, None, 'income calibration factor (CALCULATED each run: as-built earns E_SPM per minute over 0-10 min at central parameters)'),
 'T_END':      (25.0, None, 'simulated minutes'),
}
GRID_KEYS = ('hit', 'enemy', 'beta', 'omega', 'T_ESC', 'hscale', 'travel', 'F_LANE', 'F_MID', 'p2hero', 'antiheal', 'lost', 'melee_u')
MOVE_WORDS = re.compile(r'\bteleport|\bdash(es|ing)? (forward|toward|to)|charge head|charge (forward|into)|\bleap\b|jump (forward|to|into)|\btake flight|\bfly (up|forward|to)|grapple|\bblink\b|\bdive\b|launch yourself', re.I)
DEF_KEYS = re.compile(r'^(CombatBarrier|HeartHeal|MaxHealthMelee|MaxHealthBuffPct|BulletResist|TechResist|\w*Heal\w*|\w*Regen\w*|BonusHealth)$')
_HTXT = None
def hero_text(k):
    global _HTXT
    if _HTXT is None:
        _HTXT = {}
        try:
            for kk, v in re.findall(r'"(\w+)"\s+"(.*)"', open(SP + '/gt/repo/game/citadel/resource/localization/citadel_heroes/citadel_heroes_english.txt', encoding='utf-8', errors='ignore').read()):
                _HTXT[kk] = re.sub(r'<[^>]*>', '', v)
        except Exception: pass
    return _HTXT.get(k, '')
def hero_stats(hk):
    b = block('heroes.vdata', hk) or ''; base = block('heroes.vdata', 'hero_base') or ''
    def g(k, d):
        for bb in (b, base):
            m = re.search(r'\n\t\t\t' + k + r' = ([0-9.\-]+)', bb)
            if m: return float(m.group(1))
        return d
    def arm(bb):
        k = bb.find('m_MapModCostBonuses')
        if k < 0: return None
        j = bb.find('EItemSlotType_Armor = ', k); seg = bb[j:bb.find(']', j)]
        return [(int(a), float(c)) for a, c in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)', seg)]
    attr = (re.search(r'm_eWeaponAttributes = "([^"]*)"', b) or [None, ''])[1]
    return dict(hp=g('EMaxHealth', 780), regen=g('EBaseHealthRegen', 2), move=g('EMaxMoveSpeed', 7), sprint=g('ESprintSpeed', 1.6), light=g('ELightMeleeDamage', 50),
                heavy=g('EHeavyMeleeDamage', 116), hp_lvl=g('MODIFIER_VALUE_BASE_HEALTH_FROM_LEVEL', 62), melee_lvl=g('MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL', 1.58),
                arm=arm(b) or arm(base) or [], close='CloseRange' in attr, attr=attr)
def sraw(n, k):
    s = ((g69().get(n) or {}).get('stats') or {}); v = s.get(k)
    if v in (None, ''):
        it = item(n); v = it['vstats'].get(k) if it else None
    return v
def buff_uptime(n):
    """items whose stats come from a timed buff of an active that must be used on an NPC (Cultist Sacrifice: AbilityDuration/AbilityCooldown)."""
    if sraw(n, 'BonusSoulsPct') and sraw(n, 'AbilityDuration') and sraw(n, 'AbilityCooldown'):
        return min(1.0, num(sraw(n, 'AbilityDuration')) / num(sraw(n, 'AbilityCooldown')))
    return 1.0
BUFF_KEYS = {'BonusHealth', 'BaseAttackDamagePercent', 'NonPlayerBonusWeaponPower', 'NonPlayerBulletResist'}
def sval(n, k, sp=0.0, boons=0, d=0.0):
    """item stat incl. its scaling: '120 (+1.75x spirit)', '50 (+4x ELevelUpBoons)', '325 (+1.8x ETechPower)', '2.0m'. Timed-buff stats x uptime."""
    v = sraw(n, k)
    if k in BUFF_KEYS and buff_uptime(n) < 1.0: return _sval(v, sp, boons, d) * buff_uptime(n)
    return _sval(v, sp, boons, d)
def _sval(v, sp, boons, d):
    if v in (None, ''): return d
    base = num(v)
    if base is None: return d
    for f, kind in re.findall(r'\(\+?([0-9.\-]+)x\s*(\w+)\)', str(v)):
        f = float(f)
        if kind in ('spirit', 'ETechPower', 'TechPower'): base += f * sp
        elif kind == 'ELevelUpBoons': base += f * boons
    return base
def apv(P, k, sp=0.0):
    p = P.get(k) or {}; v = p.get('v') or 0.0
    return v + ((p.get('scale') or 0.0) * sp if p.get('stype') in ('ETechPower', '') else 0.0)
def colour_of(n):
    it = item(n); return COLS.get(it['slot']) if it else None
def melee_relevant(R, names):
    for sl in (1, 2, 3, 4):
        P = R['abil'][sl]['props']
        if any(p.get('stype') in ('ELightMeleeDamage', 'EHeavyMeleeDamage') for p in P.values()) or 'DurationPerLightMelee' in P: return True
    return sum(1 for n in names if any(k in ((g69().get(n) or {}).get('stats') or {}) for k in ('BonusMeleeDamagePercent', 'LifestrikeHeal', 'LifestealHeal'))) >= 2
def mobility_slots(R):
    out = {}
    for sl in (1, 2, 3, 4):
        cls = R['H']['ab'][sl]; t = hero_text(cls + '_desc')
        if MOVE_WORDS.search(t) or 'ChargeSpeed' in R['abil'][sl]['props']: out[sl] = (MOVE_WORDS.search(t) or [None])[0] or 'charge'
    return out

def casts_per_trade(P, W, I):
    cd = pv(P, 'AbilityCooldown') or 0.0; ch = int(pv(P, 'AbilityCharges') or 1); bc = pv(P, 'AbilityCooldownBetweenCharge') or 0.0
    if cd <= 1.0: return W / max(cd, 0.5)
    n = min(ch, 1 + int(W / bc)) if ch > 1 and bc > 0 else ch
    return n * min(1.0, (W + I) / cd)

def seg_metrics(R, w, st):
    """everything the strategy needs at one state (owned items, souls -> level/boons/tiers). Returns raw pieces; the
    hit/melee-uptime/enemy parameters are applied later (linear), so the grid is cheap. Tags in comments: C = CALCULATED, A = ASSUMED."""
    H = R['H']; HS = R['HS']; P0 = {k: v[0] for k, v in STRAT_P.items()}; P0.update(R.get('P_over', {}))
    W, I = P0['W'], P0['I']; T = st['tA']; names = list(w['owned']); own = [item(n) for n in names]; sp = st['sp']; boons = st['boons']
    roles = {}; unpriced = []
    # ---- health / resists / regen (C: vdata hero stats, level table, vitality invest table, item stats) ----
    inv_arm = sum(SOULS[i['tier']] for i in own if i['slot'] == 'Armor')
    ab = max([bo for th, bo in HS['arm'] if inv_arm >= th] or [0])
    hp = (HS['hp'] + HS['hp_lvl'] * boons) * (1 + ab / 100) + sum(sval(n, 'BonusHealth', sp, boons) for n in names)
    regen = HS['regen'] + sum(sval(n, 'BonusHealthRegen', sp, boons) for n in names)
    ooc = sum(sval(n, 'OutOfCombatHealthRegen', sp, boons) for n in names) + sum(sval(n, 'HealLifePercentOutOfCombat') / 100 * hp for n in names)
    keepb = keeps = 1.0
    for n in names:
        u = P0['cond_u'] if sraw(n, 'LifeThreshold') else 1.0
        if sraw(n, 'BulletResist'): keepb *= 1 - u * sval(n, 'BulletResist') / 100
        if sraw(n, 'TechResist'): keeps *= 1 - u * sval(n, 'TechResist') / 100
    # kit resists (e.g. Chain Gang T1 +40/40 while chained): weighted by cast share of a trade
    for sl in (1, 2, 3, 4):
        if T[sl] < 0: continue
        Pa = at_tier(R['abil'][sl], T[sl]); c = min(1.0, casts_per_trade(Pa, W, I)); du = pv(Pa, 'AbilityDuration') or 0
        for k, ref in (('BulletResist', 'b'), ('TechResist', 's')):
            v = pv(Pa, k)
            if v and R['abil'][sl]['type'] != '':
                f = c * min(1.0, (du or W) / W)
                if ref == 'b': keepb *= 1 - f * v / 100
                else: keeps *= 1 - f * v / 100
    keepb *= 1 - hsc(R, st, 'EBulletArmorDamageReduction') / 100; keeps *= 1 - hsc(R, st, 'ETechArmorDamageReduction') / 100
    regen += hsc(R, st, 'EBaseHealthRegen')
    br, sr = 1 - keepb, 1 - keeps
    # ---- barriers per trade (C, trigger share A) ----
    bar_fixed = 0.0; bar_trig = []
    for n in names:
        b = sval(n, 'CombatBarrier', sp, boons) or sval(n, 'GuardianWardCombatBarrier', sp, boons)
        cd = sval(n, 'AbilityCooldown') or 60
        if b and sraw(n, 'DamageThreshold'):   # trigger type from the item's own resist stat: TechResist -> spirit damage, BulletResist -> weapon damage (desc text has the word missing)
            bar_trig.append((b, sval(n, 'DamageThreshold'), sval(n, 'DamageWindow') or 3.5, cd, n, 'spirit' if sraw(n, 'TechResist') else 'bullet'))
        elif b: bar_fixed += b * min(1.0, (W + I) / cd)
        if sraw(n, 'VexBarrierCombatBarrier'): unpriced.append(f"{n}: barrier only when CC'd (no CC in this model)")
    for sl in (1, 2, 3, 4):
        if T[sl] < 0: continue
        Pa = at_tier(R['abil'][sl], T[sl])
        if pv(Pa, 'CombatBarrier'):   # kit barrier (e.g. Project Mind T2): ASSUMED cast during the trade when off cooldown
            bv = apv(Pa, 'CombatBarrier', slot_sp(R, st, sl, T[sl])); bw = min(1.0, (W + I) / (pv(Pa, 'AbilityCooldown') or 60)); bar_fixed += bv * bw
            unpriced.append(f"kit barrier {nm(R,sl)} {tlabel(T[sl])} counted as used in the trade ({bv:.0f} x {bw:.2f}); real use competes with its escape role")
    # ---- gun (C: gun_model = data clip/cycle/reload(measured where known)/fire rate/weapon invest/items) ----
    T2 = dict(T); cdr = cdr_pct([dict(n=x) for x in names])
    act = [x for x in names if not (item(x) and item(x)['class'] in REG and REG[item(x)['class']] == 'imbue' and x not in st['imbues'])]
    g = gun_model(R, st, act, T2, cdr, W, 0.5)
    dmgm = 1 + (st['wb'] + sum(sv(item(x), 'BaseAttackDamagePercent') for x in act)) / 100
    adj = 0.0
    for x in act:
        if sraw(x, 'LifeThreshold') and sv(item(x), 'BaseAttackDamagePercent'): adj -= (1 - P0['cond_u']) * sv(item(x), 'BaseAttackDamagePercent')
        cr = sval(x, 'CloseRangeBonusWeaponPower')
        if cr: adj += cr * (P0['close_u'] if HS['close'] else 0.3)
        lr = sval(x, 'LongRangeBonusWeaponPower')
        if lr: adj += lr * (0.2 if HS['close'] else 0.5)
    gmul = 1 + adj / 100 / dmgm
    G100 = g['dmg'] * gmul; bullets = g['bullets']; ls_b = g['ls']
    ric = [x for x in act if sraw(x, 'RicochetTargets')]
    ric_pct = sval(ric[0], 'RicochetDamagePercent') / 100 if ric else 0.0; ric_hero = 1 + P0['p2hero'] * ric_pct
    # kit amps on bullets (e.g. Billy Blasted 'wrecked' bullet amp from melee hits): weight by melee uptime later
    amp_melee = 0.0
    for sl in (1, 2, 3, 4):
        if T[sl] < 0: continue
        Pa = at_tier(R['abil'][sl], T[sl])
        if pv(Pa, 'BulletDamageAmp'): amp_melee += pv(Pa, 'BulletDamageAmp') / 100
    # ---- abilities (C: spirit_hits at real tier with slot spirit power; casts/trade from cooldown/charges A: W, I) ----
    sp_dmg = 0.0; melee_abil = 0.0; ab_rows = []; card = None; md = None; ehp_kit_u = 0.0; ehp_kit0 = 0.0
    for sl in (1, 2, 3, 4):
        if T[sl] < 0: continue
        Pa = at_tier(R['abil'][sl], T[sl]); s2 = slot_sp(R, st, sl, T[sl]); hits = spirit_hits(Pa, s2)
        c = casts_per_trade(Pa, W, I)
        if 'CardResourcePerBulletHit' in Pa:   # resource-gated cards (Card Trick): stored charges + cards earned from bullet hits in the trade
            per_card_hits = (pv(Pa, 'ResourcePerCard') or 100) / (pv(Pa, 'CardResourcePerBulletHit') or 4)
            card = dict(slot=sl, stored=charges(R['abil'][sl], T[sl]), per_card_hits=per_card_hits, dmg=sum(v for k, (v, inst) in hits.items() if inst),
                        heart=apv(Pa, 'HeartHeal', s2), npc_scale=pv(Pa, 'NonPlayerCardResourceScale') or 0.35)
            ab_rows.append(f"{nm(R,sl)} {tlabel(T[sl])}: card {card['dmg']:.0f} spirit dmg, heart heal {card['heart']:.0f}, {card['stored']} stored + 1 per {per_card_hits:.0f} hits")
            continue
        d = 0.0; du0 = pv(Pa, 'AbilityDuration') or pv(Pa, 'AbilityChannelTime') or 1
        for k, (v, inst) in hits.items():
            if k == 'MagicDamagePerBullet': continue
            if re.search(r'DPS|PerSecond', k): d += apv(Pa, k, s2) * min(W, du0)   # damage over time: per-second value x duration in the trade
            elif inst: d += v
            else: d += v * min(W, du0)
        if pv(Pa, 'MagicDamagePerBullet'):   # Full Auto: spirit damage per bullet during the buff
            du = (pv(Pa, 'AbilityDuration') or 5); up = min(1.0, du / W) * min(1.0, (W + I) / (pv(Pa, 'AbilityCooldown') or 45))
            mdb = apv(Pa, 'MagicDamagePerBullet', s2); ab_rows.append(f"{nm(R,sl)} {tlabel(T[sl])}: +{mdb:.1f} spirit/bullet for {du:g}s, cd {pv(Pa,'AbilityCooldown'):g}")
            md = (mdb, up)
        mel = 0.0
        for k, p in Pa.items():
            if p.get('stype') in ('ELightMeleeDamage', 'EHeavyMeleeDamage') and p.get('isdmg'):
                mel += (p.get('v') or 0) + (p.get('scale') or 0) * (HS['light'] + HS['melee_lvl'] * boons if p['stype'] == 'ELightMeleeDamage' else HS['heavy'] + HS['melee_lvl'] * boons)
        sp_dmg += d * c; melee_abil += mel * c
        if d or mel: ab_rows.append(f"{nm(R,sl)} {tlabel(T[sl])}: {d:.0f} spirit + {mel:.0f} melee-type per cast x {c:.2f} casts/trade")
        if pv(Pa, 'MaxHealthMelee'): ehp_kit_u += apv(Pa, 'MaxHealthMelee', s2) * min(1.0, (W + I) / (pv(Pa, 'AbilityCooldown') or 27)) * 4   # A: per melee hit, ~4 melee hits per trade in range
        if pv(Pa, 'MaxHealthBuffPct'): ehp_kit0 += hp * pv(Pa, 'MaxHealthBuffPct') / 100 * min(1.0, c)
    md_dmg_hit = (md[0] * bullets * md[1]) if md else 0.0      # x hit
    # ---- item procs that are priced; others listed as unpriced (C stats, A trigger counts) ----
    proc_hit = 0.0; proc0 = 0.0; proc_npc_mult = 0.0
    for x in act:
        s = (g69().get(x) or {}).get('stats', {})
        if 'DamagePerChain' in s:   # Tesla: chance per bullet, proc cooldown, chains
            per = sval(x, 'DamagePerChain', sp); rate = min(1 / (sval(x, 'ProcCooldown') or 0.2), bullets / W * sval(x, 'ProcChance') / 100)
            proc_hit += per * min(W / (sval(x, 'ProcCooldown') or 0.2), bullets * sval(x, 'ProcChance') / 100)   # procs in W at hit=1 (x hit later)
            proc_npc_mult = max(proc_npc_mult, min(sval(x, 'ChainCount') or 1, P0['N_NPC']))
        elif 'ProcBonusMagicDamage' in s:
            proc0 += sval(x, 'ProcBonusMagicDamage', sp) * min(1.0, (W + I) / (sval(x, 'AbilityCooldown') or 8))
        elif x in st['imbues'] and 'Damage' in s and 'AmmoReloadPercent' in s:   # Quicksilver/Mercurial: bonus damage on the imbued cast
            proc0 += sval(x, 'Damage', sp) * min(1.0, (W + I) / (sval(x, 'AbilityChargeUpTime') or sval(x, 'AbilityCooldown') or 18))
        elif 'DPS' in s and 'ProcRadius' in s:   # Stalker-like aura in range
            proc0 += sval(x, 'DPS', sp) * W * (P0['close_u'] if HS['close'] else 0.3)
        elif 'SpiritDamage' in s and 'LightMeleeCooldownMult' in s: pass   # melee spirit procs: priced below (mproc)
        elif any(k in s for k in ('ProcChance', 'BuildUpPerShot', 'StealPerHit', 'BulletsBonusMagicDamage', 'BonusShotsDuration', 'MaxStacks', 'DamageToStack')):
            unpriced.append(f"{x}: on-hit/stack effect not priced")
    # ---- melee (C: hero melee stats + level, item melee %; A: 4 light + 1 heavy per trade in range) ----
    mrel = R['melee_rel']; mpct = sum(sval(x, 'BonusMeleeDamagePercent') for x in names) / 100
    light = (HS['light'] + HS['melee_lvl'] * boons) * (1 + mpct); heavy = (HS['heavy'] + HS['melee_lvl'] * boons) * (1 + mpct + sum(sval(x, 'BonusHeavyMeleeDamage') for x in names) / 100)
    melee_trade = (4 * light + heavy + melee_abil) if mrel else 0.0           # x melee_u
    mproc = sum(sval(x, 'SpiritDamage', sp) for x in names if sraw(x, 'SpiritDamage') and sraw(x, 'LightMeleeCooldownMult'))
    # melee heals (C stats; A one proc per trade in range; Lifestrike cooldown not in data -> 8 s of its component ASSUMED)
    mheal = 0.0
    for x in names:
        if sraw(x, 'LifestealHeal'): mheal += sval(x, 'LifestealHeal', sp) + sval(x, 'LifestealHealPercent', sp) / 100 * heavy
        elif sraw(x, 'LifestrikeHeal'): mheal += sval(x, 'LifestrikeHeal', sp)
    if not mrel: mheal *= 0.25   # non-melee kits: occasional melee only (A)
    # ---- spirit lifesteal (C %; applies to spirit damage) ----
    ls_s = sum(sval(x, 'AbilityLifestealPercentHero') for x in names) / 100
    # cards (resource-gated): cards per trade = stored + hits/per_card_hits
    def cards(hit): return (P0['card_stored'] * card['stored'] + hit * bullets / card['per_card_hits']) if card else 0.0
    # ---- clear speed vs a camp (C gun/procs/AoE; A camp size, NPC hit 0.9) ----
    npc_w = 1 + sum(sval(x, 'NonPlayerBonusWeaponPower') for x in names) / 100 / dmgm
    g20 = gun_model(R, st, act, T2, cdr, 20, 0.5); per_target = g20['dmg'] / 20 * 0.9 * gmul * npc_w
    ric_npc = (1 + min(sval(ric[0], 'RicochetTargets'), P0['N_NPC'] - 1) * sval(ric[0], 'RicochetDamagePercent') / 100) if ric else 1.0
    clear = per_target * ric_npc + (proc_hit / W) * 0.9 * max(1.0, proc_npc_mult) * (bullets / max(bullets, 1))
    if md: clear += md[0] * g20['bullets'] / 20 * 0.9 * min(1.0, md[1] * W / 20 + 0.2) * ric_npc
    if card: clear += card['dmg'] * (g20['bullets'] / 20 * 0.9 * card['npc_scale'] / card['per_card_hits'])
    aoe = 0.0
    for sl in (1, 2, 3, 4):
        if T[sl] < 0 or R['abil'][sl]['type'] == 'EAbilityType_Ultimate': continue
        Pa = at_tier(R['abil'][sl], T[sl])
        if any(re.search('Radius', k) for k in Pa) and 'CardResourcePerBulletHit' not in Pa:
            d = sum(v for k, (v, inst) in spirit_hits(Pa, slot_sp(R, st, sl, T[sl])).items() if inst and k != 'MagicDamagePerBullet')
            cd = pv(Pa, 'AbilityCooldown') or 30
            aoe += d * P0['N_NPC'] / max(cd, 2.0)
    clear += aoe
    # ---- mobility (C: move/sprint stats, abilities whose game text describes movement) ----
    move = HS['move'] + sum(sval(x, 'BonusMoveSpeed') for x in names) + hsc(R, st, 'EMaxMoveSpeed'); sprint = HS['sprint'] + sum(sval(x, 'BonusSprintSpeed') for x in names) + hsc(R, st, 'ESprintSpeed')
    mob = {sl: (nm(R, sl), how, pv(at_tier(R['abil'][sl], T[sl]), 'AbilityCooldown')) for sl, how in R['mob'].items() if T[sl] >= 0}
    for x in names:
        for c in item_classes(x):
            roles.setdefault(x, set()).add(c['cls'])
    cult_spm = sum(sval(x, 'BonusSoulsPct') / 100 * P0['NPC_SOULS'] * 60 / (sval(x, 'AbilityCooldown') or 270) for x in names if sraw(x, 'BonusSoulsPct'))
    if cult_spm: unpriced.append('Cultist Sacrifice: +1 ability charge and range/radius of the buff not priced; buff stats x uptime ' + ', '.join(f"{x} {buff_uptime(x):.2f}" for x in names if buff_uptime(x) < 1))
    return dict(cult_spm=cult_spm, hp=hp, regen=regen, ooc=ooc, br=br, sr=sr, inv_arm=inv_arm, arm_bonus=ab, bar_fixed=bar_fixed, bar_trig=bar_trig,
                G100=G100, bullets=bullets, ls_b=ls_b, ric_hero=ric_hero, ric_pct=ric_pct, amp_melee=amp_melee, sp_dmg=sp_dmg, md_hit=md_dmg_hit, proc_hit=proc_hit, proc0=proc0,
                melee_trade=melee_trade, mproc=mproc, mheal=mheal, ls_s=ls_s, card=card, cards=cards, ehp_kit_u=ehp_kit_u, ehp_kit0=ehp_kit0,
                clear=clear, move=move, sprint=sprint, mob=mob, ab_rows=ab_rows, unpriced=sorted(set(unpriced)), roles={k: sorted(v) for k, v in roles.items()},
                wb=st['wb'], tb=st['tb'], sp=sp, lv=st['lv'], boons=boons, T=dict(T), owned=names, mrel=mrel)

def trade(m, P, e):
    """one trade vs the parameterised enemy e (dict dps, ehp, burst, res). Returns my dps to hero, heal/trade, EHP, TTD, TTK, TR, burst margin.
    All linear in hit/melee_u (A). Damage formulas C."""
    W = P['W']; h = P['hit']; u = P['melee_u'] if m['mrel'] else 0.0
    gun = m['G100'] * h * (1 + P['p2hero'] * m['ric_pct']) * (1 + m['amp_melee'] * u)
    cardn = m['cards'](h); card_d = cardn * m['card']['dmg'] if m['card'] else 0.0
    sp_ab = m['sp_dmg'] + m['md_hit'] * h + card_d                    # ability spirit damage (spirit lifesteal applies)
    sp_it = m['proc_hit'] * h + m['proc0'] + m['mproc'] * u            # item-proc spirit damage (spirit lifesteal NOT applied: UNVERIFIED, conservative)
    spirit = sp_ab + sp_it; melee = m['melee_trade'] * u
    dealt = (gun + spirit + melee) * (1 - e['res'])
    heal = (gun * m['ls_b'] + sp_ab * m['ls_s'] + m['mheal'] * (u if m['mrel'] else 1.0) + (cardn * P['p_heart'] * m['card']['heart'] if m['card'] else 0.0) + m['regen'] * W) * (1 - P.get('antiheal', 0.0))
    sh = lambda ty: P['spirit_share'] if ty == 'spirit' else 1 - P['spirit_share']
    bar = m['bar_fixed'] + sum(b * min(1.0, (W + P['I']) / cd) for b, thr, win, cd, n, ty in m['bar_trig'] if e['dps'] * sh(ty) * win >= thr) + m['ehp_kit_u'] * u + m['ehp_kit0']
    mix = (1 - P['spirit_share']) * m['br'] + P['spirit_share'] * m['sr']
    inc = e['dps'] * (1 - mix)
    ttd = (m['hp'] + bar) / max(1.0, inc - heal / W)
    ttk = e['ehp'] / max(1.0, dealt / W)
    tr = max(0.05, min(20.0, ttd / ttk))
    burst_margin = (m['hp'] + bar) - e['burst'] * (1 - mix)
    taken = max(0.0, inc * W - bar - heal)
    return dict(e_dps=e['dps'], dps=dealt / W, gun=gun / W, spirit=spirit / W, melee=melee / W, heal=heal, bar=bar, ehp=(m['hp'] + bar) / max(0.05, 1 - mix),
                ttd=ttd, ttk=ttk, tr=tr, burst_margin=burst_margin, taken=taken)

def enemy_at(t_min, P, HB):
    """reference enemy (A): souls = E_SPM*t*(1+lead); hp from hero_base level table + vitality invest table (C) with 30% of souls in vitality (A);
    dps/burst scale with weapon invest table (C) on 50% of souls (A) and +30%/+80% per 10k souls from items (A)."""
    es = P['E_SPM'] * t_min * (1 + (P['LOST_LEAD'] if P['lost'] else 0.0))
    boons = sum(1 for l, g, u, p, std in HB['L'] if g <= es and std)
    vit = 0.3 * es; ab = max([bo for th, bo in HB['arm'] if vit >= th] or [0]); wbon = max([bo for th, bo in HB['weap'] if 0.5 * es >= th] or [0])
    hp = (HB['hp'] + HB['hp_lvl'] * boons) * (1 + ab / 100) + 0.12 * vit
    res = min(0.35, 0.05 + 0.15 * es / 20000)
    dps = P['enemy'] * P['E_D0'] * (1 + wbon / 100) * (1 + 0.3 * es / 10000)
    burst = P['enemy'] * P['E_B0'] * (1 + 0.8 * es / 10000)
    return dict(souls=es, hp=hp, ehp=hp / (1 - res), res=res, dps=dps, burst=burst)

def income(m, tr_, P, t_min):
    """souls per minute at time t (A, every term explicit). Returns (spm, parts)."""
    lane = t_min < P['lane_end']; tm = 1 + P['beta'] * math.tanh(math.log(max(0.05, tr_['tr'])))
    if P.get('omega') and tr_.get('ref_clear'): tm *= (max(1.0, m['clear']) / max(1.0, tr_['ref_clear'])) ** P['omega']
    camp = 60 * P['V_CAMP'] / (P['H_CAMP'] * P['hscale'] / max(1.0, m['clear']) + P['travel'])
    if lane:
        # HP budget per lane minute: hit POKE share of the time; healed by regen, out-of-combat regen, lifesteal/kit heals on your own poke, barriers per trade
        mix = (1 - P['spirit_share']) * m['br'] + P['spirit_share'] * m['sr']; trades = 60 / (P['W'] + P['I'])
        dmg_in = tr_['e_dps'] * (1 - mix) * 60 * P['POKE']
        heal = (m['regen'] * 60 + m['ooc'] * 60 * P['OOC_SHARE']) * (1 - P.get('antiheal', 0.0) * P['POKE']) + (tr_['heal'] - m['regen'] * P['W']) * trades * (P['POKE'] * (P['W'] + P['I']) / P['W']) + tr_['bar'] * trades * 0.5
        net = dmg_in - heal; ttb = m['hp'] / net if net > 0 else 1e9
        back = (P['BACK_S'] / 60) / (ttb + P['BACK_S'] / 60) if net > 0 else 0.0
        lm = P['LOST_MULT'] if P['lost'] else 1.0
        lane_base = P['LANE_SPM'] * lm; lane_trade = P['LANE_SPM'] * lm * (tm - 1); back_loss = -(lane_base + lane_trade) * back
        lane_spm = lane_base + lane_trade + back_loss
        farm = P['F_LANE'] * camp; fight_base = fight_trade = 0.0; eng = P['ENG_LANE']
    else:
        back = 0.0; lane_spm = lane_base = lane_trade = back_loss = 0.0; farm = P['F_MID'] * camp; fight_base = P['FIGHT_SPM']; fight_trade = P['FIGHT_SPM'] * (tm - 1); eng = P['ENG_MID']
    fight = fight_base + fight_trade
    cult = m.get('cult_spm', 0.0)
    plose = 1 / (1 + tr_['tr'] ** 2)
    kills = eng * (1 - plose) * min(1.0, P['T_ESC'] / max(0.5, tr_['ttk'])); kill_spm = kills * (P['KILL0'] + 20 * t_min)
    deaths = eng * plose * (1 - (P['ESC'] if m['mob'] else 0.0)) + (eng * 0.5 if tr_['burst_margin'] < 0 else 0.0)
    resp = P['RESPAWN0'] + 1.2 * t_min
    alive = max(0.0, 1 - deaths * resp / 60)
    k_ = P.get('kappa') or 1.0; gross = lane_spm + farm + fight + cult + kill_spm
    # LEDGER: one owner per causal effect; the parts sum exactly to the souls/min returned (checked by --selftest)
    ledger = {'lane troopers (base)': lane_base * k_, 'lane: trade advantage': lane_trade * k_, 'lane: forced recalls (HP budget)': back_loss * k_, 'camps/waves farmed': farm * k_,
              'fights/objectives (base)': fight_base * k_, 'fights: trade advantage': fight_trade * k_, 'Cultist-type bonus souls': cult * k_, 'kills': kill_spm * k_, 'time dead': -gross * (1 - alive) * k_}
    return gross * alive * k_, dict(kills=kills, lane=lane_spm, farm=farm, fight=fight, back=back, deaths=deaths, camp=camp, ledger=ledger)

# ---------------- alternatives (generated from data) ----------------
def core_path(b):
    out = []
    for r in b['rows']:
        for box in r:
            if not re.match(r'^(Early|Mid|Late)', box[0]): continue
            for x in box[3]: out.append([x[0], x[1] if len(x) > 1 else '', x[2] if len(x) > 2 else None])
    return out
def topo(path):
    """keep every upgrade after its components when a path is reordered (stable)."""
    out = []; rest = list(path)
    while rest:
        for i, x in enumerate(rest):
            it = item(x[0]); comps = [c for c in (it['components'] if it else []) if any(y[0] == c for y in rest)]
            if not comps: out.append(x); rest.pop(i); break
        else: out += rest; break
    return out
def cum_colour(path, col, upto=None):
    """souls in colour col held after each purchase (components consumed), list of (index, value)."""
    owned = []; vals = []
    for i, x in enumerate(path):
        it = item(x[0])
        if not it: vals.append(0); continue
        owned = [o for o in owned if o not in it['components']] + [x[0]]
        vals.append(sum(SOULS[item(o)['tier']] for o in owned if colour_of(o) == col))
    return vals
def rush(path, col, target=4800):
    """move this colour's items (in build order, with their components) to the front until the colour holds `target`."""
    pick = []; tot = 0
    for x in path:
        if colour_of(x[0]) != col: continue
        it = item(x[0]); add = SOULS[it['tier']] - sum(SOULS[item(c)['tier']] for c in it['components'] if any(p[0] == c for p in pick))
        pick.append(x); tot += add
        if tot >= target: break
    rest = [x for x in path if x not in pick]
    return topo(pick + rest), tot
def spread(path):
    q = {c: [x for x in path if colour_of(x[0]) == c] for c in COLS.values()}; other = [x for x in path if colour_of(x[0]) not in COLS.values()]
    out = []; spent = {c: 0 for c in q}
    while any(q.values()):
        c = min((c for c in q if q[c]), key=lambda c: spent[c]); x = q[c].pop(0); out.append(x); spent[c] += SOULS[item(x[0])['tier']]
    return topo(out + other)
def spike_index(path):
    """the build's big damage item: first purchase of the highest tier among the first half of the path (e.g. Ricochet 6.4k)."""
    best = None
    for i, x in enumerate(path[:max(4, len(path) // 2)]):
        it = item(x[0])
        if it and colour_of(x[0]) != 'vitality' and (best is None or it['tier'] > item(path[best][0])['tier']): best = i
    return best or 0

def strat_R(b, path, order, P_over=None):
    bb = dict(b, order=order, rows=[[['Early · L-R', '', '', [[x[0], x[1] or '', x[2]] if x[2] else [x[0], x[1] or ''] for x in path]]]])
    R = analyse(bb, order, (P_over or {}).get('REFUND', STRAT_P['REFUND'][0])); R['HS'] = hero_stats(b['hk']); R['P_over'] = P_over or {}
    R['melee_rel'] = melee_relevant(R, [x[0] for x in path]); R['mob'] = mobility_slots(R)
    return R
def segments(R):
    """state at every purchase and every level/ability event (souls earned -> level; items held = last affordable purchase)."""
    rows = [r for r in R['rows'] if not r.get('unknown')]
    ev = sorted(set([0] + [r['souls'] for r in rows] + [g for l, g, u, p, std in R['L']] + [g for g, lv, a, t in R['evA']]))
    segs = []
    for s in ev:
        if s > 60000: break
        prev = [r for r in rows if r['souls'] <= s]
        w = dict(prev[-1], souls=s) if prev else {'n': None, 'souls': s, 'owned': [], 'imbues': {}, 'box': ''}
        st = state(R, w); segs.append((s, seg_metrics(R, w, st), w.get('n') if prev and prev[-1]['souls'] == s else None))
    return segs
def candidate_greens(R, path, s_at, kind):
    """kind 'off': Armor items (T1-T3 upgrade of a T1) that add a damage stat this kit uses; 'def': Armor items with health/resist/barrier/regen.
    Value = change in trade ratio vs the central enemy at the spike point per 800 souls (C state model, central A params)."""
    names = {x[0] for x in path}; mrel = R['melee_rel']; out = []
    P = {k: v[0] for k, v in STRAT_P.items()}; HB = R['HB']
    rows = [r for r in R['rows'] if not r.get('unknown') and r['souls'] <= s_at]
    base_w = dict(rows[-1]) if rows else {'n': None, 'souls': s_at, 'owned': [], 'imbues': {}, 'box': ''}
    t_min = s_at / P['E_SPM']; e = enemy_at(t_min, P, HB)
    m0 = seg_metrics(R, base_w, state(R, dict(base_w, souls=s_at))); t0 = trade(m0, P, e)
    for n, gdat in items().items():
        if gdat['slot'] != 'Armor' or gdat.get('disabled') or n in base_w['owned']: continue
        if gdat['tier'] > 2 and not (gdat['tier'] == 3 and gdat['components'] and item(gdat['components'][0])['tier'] == 1): continue
        s = (g69().get(n) or {}).get('stats', {})
        off = any(k in s for k in ('BaseAttackDamagePercent', 'BonusFireRate', 'BulletLifestealPercent')) or (mrel and any(k in s for k in ('BonusMeleeDamagePercent', 'LifestrikeHeal', 'LifestealHeal')))
        dfn = any(k in s for k in ('BonusHealth', 'BulletResist', 'TechResist', 'CombatBarrier', 'BonusHealthRegen')) and not any(k in s for k in ('HealAmpReceivePenaltyPercent', 'DeathImmunityDuration'))
        if (kind == 'off' and not off) or (kind == 'def' and not dfn): continue
        comps = [c for c in gdat['components'] if c not in base_w['owned']]
        w2 = dict(base_w, owned=[o for o in base_w['owned'] if o not in gdat['components']] + comps + [n])
        cost = SOULS[gdat['tier']] - sum(SOULS[item(c)['tier']] for c in gdat['components'] if c in base_w['owned'])
        m1 = seg_metrics(R, w2, state(R, dict(w2, souls=s_at))); t1 = trade(m1, P, e)
        val = (t1['tr'] / t0['tr'] - 1) * 100 if kind == 'off' else (t1['ttd'] / t0['ttd'] - 1) * 100
        out.append((val / (cost / 800), n, cost, round(val, 1), comps))
    return sorted(out, reverse=True)
def defensive_order(R, order):
    """move ability tiers whose upgrade adds barrier/heal/max-health/resist as early as their own previous tier allows (unlock order kept)."""
    ab = R['abil']; seq = []; cnt = {1: 0, 2: 0, 3: 0, 4: 0}
    for a in order: seq.append((a, cnt[a])); cnt[a] += 1
    dfn = lambda a, t: t >= 1 and t - 1 < len(ab[a]['ups']) and any(DEF_KEYS.match(pn) for pn, _, _ in ab[a]['ups'][t - 1])
    if not any(dfn(a, t) for a, t in seq): return None, []
    out = []; rest = list(seq); placed = {1: -1, 2: -1, 3: -1, 4: -1}
    while rest:
        pick = next((i for i, (a, t) in enumerate(rest) if dfn(a, t) and placed[a] == t - 1), None)
        if pick is None: pick = next(i for i, (a, t) in enumerate(rest) if placed[a] == t - 1 or t == 0)
        a, t = rest.pop(pick); out.append((a, t)); placed[a] = max(placed[a], t)
    return [a for a, t in out], [f"{nm(R,a)} {tlabel(t)}" for a, t in seq if dfn(a, t)]
def load_alt(f):
    js = "const fs=require('fs');const o=new Function('return ('+fs.readFileSync(process.argv[1],'utf8').trim().replace(/[,;]\\s*$/,'')+')')();process.stdout.write(JSON.stringify(o))"
    return json.loads(subprocess.run(['node', '-e', js, f], capture_output=True, text=True, check=True).stdout)

def gen_alternatives(b, s1, alt_files):
    path0 = core_path(b); order0 = list(b['order']); R0 = strat_R(b, path0, order0); R0['HB'] = HB_of()
    A = [dict(name='A0', kind='AS-BUILT', desc='the build as it is in data.js', path=path0, order=order0, gen='data.js core boxes L-R')]
    # damage colour = non-vitality colour with the most souls before s1
    dmgcol = max(('gun', 'spirit'), key=lambda c: sum(SOULS[item(x[0])['tier']] for x, s in zip(path0, [r['souls'] for r in R0['rows'] if not r.get('unknown')]) if colour_of(x[0]) == c and s <= s1))
    p, tot = rush(path0, dmgcol); A.append(dict(name='A1', kind='RUSH-DMG-4.8K', desc=f'{dmgcol} items first until {dmgcol} holds 4.8k ({tot}), rest in build order', path=p, order=order0, gen=f'rush({dmgcol}, 4800) over the build\'s own items'))
    p, tot = rush(path0, 'vitality')
    if tot < 4800:   # build lacks 4.8k of greens: add the best defensive catalog greens at the front
        extra = [c for c in candidate_greens(R0, path0, 0, 'def') if c[1] not in [x[0] for x in p]]
        for v, n, cost, val, comps in extra:
            if tot >= 4800: break
            p = [[c, '', None] for c in comps] + [[n, '', None]] + p; tot += cost
        p = topo(p)
    A.append(dict(name='A2', kind='RUSH-VIT-4.8K', desc=f'vitality items first until vitality holds 4.8k ({tot}), rest in build order', path=p, order=order0, gen='rush(vitality, 4800); catalog greens added if the build has < 4.8k'))
    A.append(dict(name='A3', kind='SPREAD', desc='colours interleaved, cheapest colour next (no rush)', path=spread(path0), order=order0, gen='spread(): round-robin by souls spent per colour'))
    si = spike_index(path0); spike_item = path0[si][0]; s_at = [r['souls'] for r in R0['rows'] if not r.get('unknown')][max(0, si - 1)] if si else 0
    for kind, lab in (('off', 'A4'), ('def', 'A5')):
        cl = candidate_greens(R0, path0, s_at, kind); cands = cl[:1]
        for c in cl[1:]:
            if len(cands) >= 2: break
            if not set(item(c[1])['components']) & set(item(cands[0][1])['components']) and c[1] not in item(cands[0][1])['components'] and cands[0][1] not in item(c[1])['components']: cands.append(c)
        if not cands: continue
        ins = []; p = [x for x in path0]
        for v, n, cost, val, comps in cands:
            ex = next((x for x in p if x[0] == n), None)
            if ex: p.remove(ex)
            for c in comps:
                exc = next((x for x in p if x[0] == c), None)
                if exc: p.remove(exc)
                ins.append(exc or [c, '', None])
            ins.append(ex or [n, '', None])
        p = topo(p[:si] + ins + p[si:])
        txt = ', '.join(f"{n} ({'+' if val >= 0 else ''}{val}% {'trade ratio' if kind == 'off' else 'time-to-die'} for {cost})" for v, n, cost, val, comps in cands)
        A.append(dict(name=lab, kind='OFFENSIVE-GREENS' if kind == 'off' else 'DEFENSIVE-GREENS', path=p, order=order0,
                      desc=f"{txt} bought before {spike_item} (delays it by {sum(c[2] for c in cands)} souls)",
                      gen=f"candidate_greens('{kind}') top 2 by marginal value per 800 souls at {s_at} souls, full catalog scan, inserted before the spike item"))
    own_g = []; tot = 0
    for x in path0[si:]:
        if colour_of(x[0]) == 'vitality' and tot < 3200:
            it = item(x[0]); tot += SOULS[it['tier']] - sum(SOULS[item(c)['tier']] for c in it['components'] if any(y[0] == c for y in own_g)); own_g.append(x)
    if own_g:
        p = topo([x for x in path0[:si] if x not in own_g] + own_g + [x for x in path0[si:] if x not in own_g])
        A.append(dict(name='A8', kind='OWN-GREENS-BEFORE-SPIKE', desc=f"the build's own first greens ({', '.join(x[0] for x in own_g)}, {tot}) moved before {spike_item}", path=p, order=order0,
                      gen="build's own vitality items after the spike item, in order, until 3.2k, moved before it"))
    o6, deft = defensive_order(R0, order0)
    if o6 and o6 != order0:
        A.append(dict(name='A6', kind='DEFENSIVE-POINTS', desc='ability points: defensive tiers first (' + ', '.join(deft) + ')', path=path0, order=o6, gen='defensive_order(): tiers whose upgrade adds barrier/heal/max-health/resist moved as early as allowed'))
        a4 = next((a for a in A if a['name'] == 'A4'), None)
        if a4: A.append(dict(name='A7', kind='OFF-GREENS+DEF-POINTS', desc=a4['desc'] + '; plus A6 ability order', path=a4['path'], order=o6, gen='A4 path + A6 order'))
    for i, f in enumerate(alt_files):
        o = load_alt(f); p = [[x[0], x[1] if len(x) > 1 else '', x[2] if len(x) > 2 else None] if isinstance(x, list) else [x, '', None] for x in (o.get('path') or [])] or core_path(o)
        if o.get('fill_from_build', True):   # an alternative that names only its early items continues with the build's remaining core items in build order
            p = p + [x for x in path0 if x[0] not in [y[0] for y in p]]
        order = [int(c) for c in str(''.join(map(str, o['order'])))] if o.get('order') else order0
        unknown = [x[0] for x in p if not item(x[0])]
        A.append(dict(name=o.get('name') or f'X{i+1}', kind='ALT-FILE', desc=o.get('desc', '') + (f" (UNKNOWN items ignored: {unknown})" if unknown else ''), path=topo([x for x in p if item(x[0])]), order=order, gen=f'--alt {f}'))
    # de-duplicate identical alternatives
    seen = {}; out = []
    for a in A:
        k = json.dumps([[x[0] for x in a['path']], a['order']])
        if k in seen: seen[k]['desc'] += f" (= {a['name']} {a['kind']})"; continue
        seen[k] = a; out.append(a)
    return out, dmgcol, spike_item
_HB = None
def HB_of():
    global _HB
    if _HB is None:
        hs = hero_stats('hero_base'); hi = hero_info('hero_base') if block('heroes.vdata', 'hero_base') else None
        _HB = dict(hs, L=hi['L'] if hi else [], weap=hi['weap'] if hi else [])
    return _HB

def enemies(P, HB, dt=15.0):
    n = int(P['T_END'] * 60 / dt) + 1; return [enemy_at(i * dt / 60, P, HB) for i in range(n)]
def simulate(segs, P, HB, E=None):
    """time-stepped soul income (A model) feeding the purchase walk: souls earned -> state -> trade vs enemy at that minute -> income."""
    keys = [s for s, m, n in segs]; dt = 15.0; S = 0.0; t = 0.0; out = dict(tr=[], spm=[], deaths=0.0, backs=0.0, at={}, cp={}, buys=[])
    E = E or enemies(P, HB, dt); step = 0; out['kills'] = 0.0
    while t < P['T_END'] * 60:
        i = bisect.bisect_right(keys, S) - 1; s, m, n = segs[i]
        tm = t / 60; e = E[step]; tr_ = trade(m, P, e)
        if P.get('_refc'): tr_['ref_clear'] = P['_refc'][min(step, len(P['_refc']) - 1)]
        step += 1; spm, parts = income(m, tr_, P, tm)
        if tm >= 1.0 and tm <= 20.0: out['tr'].append(math.log(tr_['tr']))
        out.setdefault('trs', []).append((tm, tr_['tr']))
        out['spm'].append(spm); out['deaths'] += parts['deaths'] * dt / 60; out['kills'] += parts['kills'] * dt / 60
        L_ = out.setdefault('ledger', {})
        for kk, vv in parts['ledger'].items(): L_[kk] = L_.get(kk, 0.0) + vv * dt / 60
        S += spm * dt / 60; t += dt
        for mm in (5, 10, 15, 20):
            if abs(t / 60 - mm) < 1e-6: out['at'][mm] = S
        out.setdefault('S', []).append((t / 60, S))
    return out
def time_to(sim, souls):
    for t, S in sim['S']:
        if S >= souls: return t
    return None

def strategy(b, cps, alt_files, P_over, grid='full', argv=''):
    alts, dmgcol, spike_item = gen_alternatives(b, max(cps), alt_files)
    HB = HB_of(); P0 = {k: v[0] for k, v in STRAT_P.items()}; P0.update(P_over)
    for a in alts:
        a['R'] = strat_R(b, a['path'], a['order'], P_over); a['R']['HB'] = HB; a['segs'] = segments(a['R'])
        a['spk'] = spikes(a['R']); a['walk'] = [(r['n'], r['souls']) for r in a['R']['rows'] if not r.get('unknown')]
    mrel = any(a['R']['melee_rel'] for a in alts)
    keys0 = [s for s, m, n in alts[0]['segs']]
    P0['_refc'] = [alts[0]['segs'][bisect.bisect_right(keys0, P0['E_SPM'] * i * 15 / 60) - 1][1]['clear'] for i in range(int(P0['T_END'] * 4) + 2)]
    if P0.get('kappa') is None:   # calibrate absolute income on the as-built path (relative comparisons do not depend on it)
        k = 1.0
        for _ in range(6):
            P0['kappa'] = k; s10 = simulate(alts[0]['segs'], P0, HB)['at'].get(10, 1.0); k = k * (P0['E_SPM'] * 10 / max(1.0, s10)) ** 0.9
        P0['kappa'] = k
    gk = [k for k in GRID_KEYS if not (k == 'melee_u' and not mrel)]
    if grid == 'quick': gk = [k for k in gk if k in ('hit', 'enemy', 'beta', 'lost')]
    vals = [STRAT_P[k][1] for k in gk]; cells = []
    for combo in itertools.product(*vals):
        P = dict(P0); P.update(dict(zip(gk, combo))); res = {}; E = enemies(P, HB)
        for a in alts:
            sm = simulate(a['segs'], P, HB, E); res[a['name']] = dict(tr=math.exp(sum(sm['tr']) / len(sm['tr'])), s20=sm['at'].get(20, 0), s10=sm['at'].get(10, 0), deaths=sm['deaths'])
        cells.append((dict(zip(gk, combo)), res))
    return dict(alts=alts, dmgcol=dmgcol, spike_item=spike_item, cells=cells, gk=gk, P0=P0, mrel=mrel, HB=HB)

def decide(S):
    """pre-registered decision rule (printed in the file before the results)."""
    names = [a['name'] for a in S['alts']]
    def win(res, key): return max(names, key=lambda n: res[n][key])
    wins = [win(r, 'tr') for c, r in S['cells']]; cnt = {n: wins.count(n) for n in names}
    top = max(names, key=lambda n: cnt[n]); share = cnt[top] / len(wins)
    margins = []
    for c, r in S['cells']:
        others = [r[n]['tr'] for n in names if n != top]
        margins.append((r[top]['tr'] / max(others) - 1) * 100 if others else 0)
    med = sorted(margins)[len(margins) // 2]
    econ = [win(r, 's20') for c, r in S['cells']]; econ_top = max(names, key=lambda n: econ.count(n)); econ_share = econ.count(econ_top) / len(econ)
    # which single assumption decides the winner when it is not robust
    dep = []
    for k in S['gk']:
        by = {}
        for (c, r), wnr in zip(S['cells'], wins): by.setdefault(c[k], []).append(wnr)
        per = {v: max(set(ws), key=ws.count) for v, ws in by.items()}; cons = sum(ws.count(per[v]) for v, ws in by.items()) / len(wins)
        dep.append((cons, k, per))
    dep.sort(reverse=True)
    lost_cells = [(c, r) for c, r in S['cells'] if c.get('lost') == 1]
    lost_top = None
    if lost_cells:
        lw = [win(r, 'tr') for c, r in lost_cells]; lost_top = max(names, key=lambda n: lw.count(n)); lost_share = lw.count(lost_top) / len(lw)
    if share >= 0.8 and med >= 3.0: concl = f"CHOSEN: {top}"; basis = f"{top} has the best time-averaged trade ratio in {share*100:.0f}% of {len(wins)} grid cells (median margin {med:+.1f}% over the runner-up)"
    elif share >= 0.5 and dep and dep[0][0] >= 0.9 and len(set(dep[0][2].values())) > 1:
        k, per = dep[0][1], dep[0][2]
        concl = f"DEPENDS ON ASSUMPTION {k}: " + ', '.join(f"{w} if {k}={v}" for v, w in sorted(per.items())); basis = f"winner changes with {k} (fixing {k} explains {dep[0][0]*100:.0f}% of cells); no robust choice"
    else: concl = 'INSUFFICIENT EVIDENCE - no decision'; basis = f"best alternative {top} wins only {share*100:.0f}% of cells (median margin {med:+.1f}%); below the pre-registered bar (>=80% and >=3%)"
    return dict(concl=concl, basis=basis, top=top, share=share, med=med, cnt=cnt, econ_top=econ_top, econ_share=econ_share, dep=dep, lost_top=lost_top,
                lost_share=(lost_share if lost_cells else None))

SHORT = {'AS-BUILT': 'as built', 'RUSH-DMG-4.8K': 'rush dmg', 'RUSH-VIT-4.8K': 'rush vit', 'SPREAD': 'spread', 'OFFENSIVE-GREENS': 'dmg greens', 'DEFENSIVE-GREENS': 'def greens',
         'OWN-GREENS-BEFORE-SPIKE': 'own greens 1st', 'DEFENSIVE-POINTS': 'def points', 'OFF-GREENS+DEF-POINTS': 'dmg greens+def pts', 'ALT-FILE': 'alt'}
def game_summary(q, hyp, alts, tradeoffs, missing, concl=None):
    """3-4 compact lines (<=200 chars each) for the in-game plugin. Same fields as the scenario metadata (question, hypothesis, alternatives, tradeoffs, missing_evidence)."""
    cut = lambda s, n=200: (s if len(s) <= n else s[:n - 3] + '...')
    alt_s = '; '.join(alts) if isinstance(alts, list) else str(alts)
    tr_s = '; '.join(tradeoffs) if isinstance(tradeoffs, list) else str(tradeoffs)
    mi_s = '; '.join(missing) if isinstance(missing, list) else str(missing)
    L = [cut('Q: ' + q), cut('Test: ' + hyp + ' | Paths: ' + alt_s), cut('Trade-off: ' + tr_s)]
    L.append(cut(('Result: ' + concl + ' | ' if concl else '') + 'Unknown: ' + mi_s))
    return L

def body_sha(text):
    body = '\n'.join(l for l in text.split('\n') if not re.match(r'^(GENERATED|BODY-SHA):', l))
    return hashlib.sha256(body.encode()).hexdigest()
def input_sha():
    h = hashlib.sha256()
    for f in (SP + '/data.js', SC + 'heroes.vdata', SC + 'abilities.vdata', SP + '/audit/items_full.json', SP + '/audit/items_full_6819.json', os.path.abspath(__file__)):
        try: h.update(open(f, 'rb').read())
        except Exception: h.update(b'-')
    return h.hexdigest()

def write_strategy(b, cps, S, D, outfile, argv):
    A = S['alts']; P0 = S['P0']; HB = S['HB']; o = []; hero = b['hero']
    a0 = A[0]; spk0 = a0['spk']
    def first(col, aa): return aa['spk'][col]['4800']
    q = (f"For {hero} ({b['id']}) between {min(cps)} and {max(cps)} souls: does the as-built path ({a0['walk'][0][0]}...; {S['spike_item']} at "
         f"{dict(a0['walk']).get(S['spike_item'])}; vitality 4.8k at {first('vitality', a0)}) let {hero} play more effectively than data-generated alternatives?")
    hyp = (f"A0 AS-BUILT has the best time-averaged trade ratio (1-20 min, income-fed walk) in >=80% of the parameter grid; refuted if another path wins >=80% "
           f"with >=3% median margin, undecided otherwise")
    alt_short = [f"{a['name']} {a['kind']}" for a in A]
    # trade-offs from the equal-souls table (computed below)
    rows = []
    for a in A:
        for c in cps:
            i = bisect.bisect_right([s for s, m, n in a['segs']], c) - 1; s, m, n = a['segs'][i]
            e = enemy_at(c / P0['E_SPM'], P0, HB); t = trade(m, P0, e); rows.append((a['name'], c, m, t))
    def at(nm_, c): return next(r for r in rows if r[0] == nm_ and r[1] == c)
    trade_offs = []
    for a in A[1:]:
        better = [c for c in cps if at(a['name'], c)[3]['tr'] > at('A0', c)[3]['tr'] * 1.03]; worse = [c for c in cps if at(a['name'], c)[3]['tr'] < at('A0', c)[3]['tr'] * 0.97]
        avg = lambda nm_, f: sum(f(at(nm_, c)) for c in cps) / len(cps); d = lambda f: (avg(a['name'], f) / max(1e-9, avg('A0', f)) - 1) * 100
        trade_offs.append(f"{a['name']} vs A0 (equal souls, mean over checkpoints): HP {d(lambda r: r[2]['hp']):+.0f}%, heal/trade {d(lambda r: r[3]['heal']):+.0f}%, damage to heroes {d(lambda r: r[3]['dps']):+.0f}%, "
                          f"clear speed {d(lambda r: r[2]['clear']):+.0f}%; trade ratio better at {better or 'none'}, worse at {worse or 'none'}")
    missing = ['clear speed/camp hp/soul values: no NPC or camp data in the sandbox or vdata (needs a camp-clear scenario per checkpoint, generic_camp_clear)',
               'enemy poke/burst curve: reference enemy is ASSUMED (needs shoot-back mode / real lane logs)',
               'trade->income link (beta), forced-back and death costs: ASSUMED (needs match data: souls vs lane trade outcome)',
               'hit rate on heroes and melee uptime: ASSUMED ranges (needs streak-accuracy sandbox runs or replays)',
               'enemy CC not modelled (GAPS 7): escapes and channels valued without silence/stun; anti-heal only as the grid parameter antiheal',
               'model structure (not in the grid): 1v1 trade ratio TTD/TTK rewards balanced health and damage by construction; teamfight focus, burst before healing lands, positioning, objectives and item actives timing are not modelled; resource-gated cards assume card_stored',
               'model-wide pattern (sweep of all 81 data.js builds, quick grid, 2026-10-24): the as-built path won 0 grid cells on any build and 1-2 cheap defensive greens before the spike item won 51 of 57 decided builds; either the Council builds under-buy early sustain in general or the 1v1 trade-ratio model over-values cheap health. Settle with a shoot-back lane test (GAPS 6/17) at one checkpoint before trusting a single-build verdict']
    unp = sorted(set(u for a in A for s, m, n in a['segs'] for u in m['unpriced']))
    if unp: missing.append('unpriced item effects: ' + '; '.join(unp)[:600])
    if S['mrel']: missing.append('melee semantics: Lifestrike cooldown not in data (8 s ASSUMED), Blasted melee bonus health per hit (field-name reading), Bashdown counting as melee for item procs (UNVERIFIED)')
    ref = D['top'] if D['top'] != 'A0' else max((a['name'] for a in A[1:]), key=lambda n: D['cnt'].get(n, 0), default='A0')
    tline = next((x for x in trade_offs if x.startswith(ref + ' ')), '-')
    tline = re.sub(r' \(equal souls, mean over checkpoints\)', '', tline.split(';')[0])
    gs = game_summary(f"{hero}: which buy/point path plays best {min(cps)}-{max(cps)} souls?", 'as built wins on trade ratio over time',
                      [f"{a['name']} {SHORT.get(a['kind'], a['kind'].lower())}" for a in A], [tline], ['clear speed (no NPC data)', 'enemy poke curve', 'trade->income link'], D['concl'])
    hdr = ['SCOPE: build-context', 'KIND: strategy', 'VALID: yes (CALCULATED + ASSUMED model by abtimeline.py --strategy; not a sandbox measurement)', f'BUILD: {b["id"]}', f'HERO: {hero}',
           f'VERSION: {STRAT_VERSION}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
           f'CHECKPOINTS: {",".join(map(str, cps))}', f'QUESTION: {q}', f'HYPOTHESIS: {hyp}', 'ALTERNATIVES: ' + '; '.join(alt_short),
           'TRADEOFFS: ' + ' | '.join(trade_offs), 'MISSING_EVIDENCE: ' + ' | '.join(missing),
           'DECISION RULE (pre-registered): primary metric = time-averaged (geometric mean) trade ratio TR (my time-to-die / my time-to-kill vs the reference enemy) over minutes 1-20 of the income-fed walk; '
           'CHOSEN if one path is best in >=80% of grid cells with median margin >=3%; DEPENDS ON ASSUMPTION k if >=50% and fixing one parameter k explains >=90% of winners; else INSUFFICIENT EVIDENCE. '
           'Robustness % = share of grid cells, not a probability of being right; model confidence is not accuracy.',
           f'CONCLUSION: {D["concl"]}', f'BASIS: {D["basis"]}',
           'GRADE: CALCULATED (game data) + ASSUMED (income, enemy, hit/melee/trade parameters); no MEASURED input except where tagged; per WEAKNESS_PROCESS H this is a model decision to be tested, not proof']
    if D['concl'].startswith('CHOSEN'):
        ch = next(a for a in A if a['name'] == D['top']); hdr.append('CHOSEN-PATH: ' + ' > '.join(x[0] for x in ch['path'])); hdr.append('CHOSEN-ORDER: ' + ''.join(map(str, ch['order'])))
    hdr += ['GAME_SUMMARY: ' + l for l in gs]
    o += hdr + ['']
    o.append('## TAGS: MEASURED = validated sandbox value; CALCULATED = game data + stated formula; ASSUMED = parameter (see PARAMETERS, sensitivity below). ISOLATED values: none used; every number below is the complete path state at the checkpoint (owned items, ability tiers, imbues, invest bonuses).')
    o.append('## PARAMETERS (ASSUMED unless noted)')
    for k, (v, gv, why) in STRAT_P.items(): o.append(f"  {k} = {P0[k]:g}" + (f"  grid {list(gv)}" if gv and k in S['gk'] else '') + f"  - {why}")
    o.append(f"  reload: {weapon(A[0]['R'])['reload']} s ({weapon(A[0]['R'])['reload_src']})")
    o.append('\n## ALTERNATIVES (concrete purchase + ability-point paths, generated from data)')
    for a in A:
        o.append(f"- {a['name']} {a['kind']}: {a['desc']}  [generator: {a['gen']}]")
        o.append(f"    PATH: " + ' > '.join(f"{n}@{s}" for n, s in a['walk']))
        o.append(f"    ORDER: {''.join(map(str, a['order']))}  timeline(A): " + '  '.join(f"{nm(a['R'],x)[:10]}:{tlabel(t)}@{g}" for g, lv, x, t in a['R']['evA'] if g <= max(cps) * 1.3))
        o.append(f"    SPIKES (souls when first held, CALCULATED): " + ', '.join(f"{c} 4.8k@{d['4800']}" for c, d in a['spk'].items()))
    o.append('\n## PER-CHECKPOINT STATE (equal souls; CALCULATED from data; trade vs reference enemy at central ASSUMED params)')
    o.append('alt  souls lvl  tiers(1/2/3/4)   gun%  vit%  spSP |   HP  regen  ooc  bres sres barrier/trade | dps->hero (gun/spirit/melee) heal/trade lifesteal(b/s) | EHP  TTD  TTK  TR  burst-margin | clear dps | move  escape')
    for nm_, c, m, t in rows:
        a = next(x for x in A if x['name'] == nm_)
        esc = ','.join(f"{v[0][:10]}({v[1]},cd{v[2]:g})" for v in m['mob'].values()) or '-'
        o.append(f"{nm_:<4} {c:>6} L{m['lv']:<2} {'/'.join(tlabel(m['T'][s]) for s in (1,2,3,4)):<15} {m['wb']:>4.0f} {m['arm_bonus']:>4.0f} {m['sp']:>5.0f} | {m['hp']:>5.0f} {m['regen']:>5.1f} {m['ooc']:>4.1f} {m['br']*100:>4.0f}% {m['sr']*100:>3.0f}% {t['bar']:>6.0f} | "
                 f"{t['dps']:>5.0f} ({t['gun']:.0f}/{t['spirit']:.0f}/{t['melee']:.0f}) {t['heal']:>6.0f} {m['ls_b']*100:>3.0f}/{m['ls_s']*100:<3.0f}% | {t['ehp']:>5.0f} {t['ttd']:>4.1f} {t['ttk']:>4.1f} {t['tr']:>4.2f} {t['burst_margin']:>+6.0f} | {m['clear']:>6.0f} | {m['move']:.1f} {esc}")
    o.append('  owned at each checkpoint and item roles (classes from item data; every role of each item, section J):')
    for a in A:
        for c in cps:
            i = bisect.bisect_right([s for s, m, n in a['segs']], c) - 1; m = a['segs'][i][1]
            o.append(f"  {a['name']} @{c}: " + ', '.join(f"{n}[{'/'.join(m['roles'].get(n, [])) or 'stats'}]" for n in m['owned']) + (f" | abilities: {'; '.join(m['ab_rows'])}" if m['ab_rows'] else ''))
    o.append('\n## SOUL INCOME OVER TIME (ASSUMED model, central parameters; lane even / lane lost)')
    o.append('alt   lane | souls@5  @10   @15   @20 | min to ' + ' '.join(f"{c}" for c in cps) + ' | 4.8k spikes (min) gun/vit/spirit | deaths/kills(0-25) | mean TR 1-20 min')
    for lost in (0, 1):
        P = dict(P0); P['lost'] = lost
        for a in A:
            sm = simulate(a['segs'], P, HB); sp_ = {c: (time_to(sm, a['spk'][c]['4800']) if a['spk'][c]['4800'] else None) for c in ('gun', 'vitality', 'spirit')}
            f = lambda x: '-' if x is None else f"{x:.1f}"
            o.append(f"{a['name']:<4} {'lost' if lost else 'even'} | {sm['at'].get(5,0):>6.0f} {sm['at'].get(10,0):>5.0f} {sm['at'].get(15,0):>5.0f} {sm['at'].get(20,0):>5.0f} | "
                     + ' '.join(f(time_to(sm, c)) for c in cps) + f" | {f(sp_['gun'])}/{f(sp_['vitality'])}/{f(sp_['spirit'])} | {sm['deaths']:.2f}/{sm['kills']:.2f} | {math.exp(sum(sm['tr'])/len(sm['tr'])):.3f}")
            if a['name'] == 'A0' and not lost: calib = sm['at'].get(10, 0) / 10
    o.append(f"  calibration (CALCULATED): kappa = {P0['kappa']:.3f} so that A0 earns {calib:.0f} souls/min over 0-10 min with an even lane at central parameters (anchor: RULES_KIERAN ~1k/min early); the same kappa is used for every path and grid cell. Lane-lost penalty = souls@20 even minus lost (per alt, above).")
    o.append('\n## SENSITIVITY (every grid cell re-runs every alternative; ranking by the pre-registered primary metric)')
    o.append(f"  grid parameters: {', '.join(f'{k} {list(STRAT_P[k][1])}' for k in S['gk'])}  ({len(S['cells'])} cells)")
    o.append('  wins on trade ratio: ' + ', '.join(f"{n} {c}" for n, c in sorted(D['cnt'].items(), key=lambda x: -x[1])))
    ew = {}
    for c, r in S['cells']:
        wnr = max(r, key=lambda n: r[n]['s20']); ew[wnr] = ew.get(wnr, 0) + 1
    o.append('  wins on souls@20 (economy only): ' + ', '.join(f"{n} {v}" for n, v in sorted(ew.items(), key=lambda x: -x[1])))
    # is damage-first earning more souls? souls@20 per farming scenario (other grid parameters averaged), A0 vs every alternative
    fk = [k for k in ('hscale', 'travel', 'F_LANE', 'F_MID') if k in S['gk']]
    o.append('  souls@20 by farming scenario (' + '/'.join(fk) + '; mean over the other grid parameters):')
    for combo in itertools.product(*[STRAT_P[k][1] for k in fk]):
        cs = [r for c, r in S['cells'] if all(c[k] == v for k, v in zip(fk, combo))]
        avg = {a['name']: sum(r[a['name']]['s20'] for r in cs) / len(cs) for a in A}; best = max(avg, key=avg.get)
        o.append('    ' + '/'.join(f"{v:g}" for v in combo) + ': ' + ' '.join(f"{n} {v:.0f}" for n, v in avg.items()) + f"  -> most souls {best}" + (f" (+{(avg[best]/avg['A0']-1)*100:.1f}% vs A0)" if best != 'A0' else ''))
    if D['lost_top']: o.append(f"  lane-lost cells only: {D['lost_top']} wins {D['lost_share']*100:.0f}%")
    for cons, k, per in D['dep'][:len(S['gk'])]:
        o.append(f"  by {k}: " + ', '.join(f"{v}->{w}" for v, w in sorted(per.items())) + f"  (fixing {k} explains {cons*100:.0f}% of winners)")
    # per-parameter mean TR per alt
    for k in S['gk']:
        line = []
        for v in STRAT_P[k][1]:
            cs = [r for c, r in S['cells'] if c[k] == v]
            line.append(f"{k}={v}: " + ' '.join(f"{n}{sum(r[n]['tr'] for r in cs)/len(cs):.2f}" for n in [a['name'] for a in A]))
        o.append('  mean TR ' + ' | '.join(line))
    robust = 'ROBUST across the tested grid' if D['share'] >= 0.8 else 'ASSUMPTION-DRIVEN'
    o.append(f"  verdict on robustness: {robust} (top {D['top']} {D['share']*100:.0f}% of cells; median margin {D['med']:+.1f}%). The grid ranges themselves are ASSUMED.")
    o.append('\n## ITEM x KIT INTERACTIONS (damage/fire-rate/stat items the top alternative adds, removes or moves; abtimeline.py --interactions at the A0 buy point, CALCULATED)')
    try:
        top = next(a for a in A if a['name'] == D['top']); p0 = [x[0] for x in A[0]['path']]; p1 = [x[0] for x in top['path']]
        moved = [n for n in p1[:12] if n not in p0 or abs(p1.index(n) - p0.index(n)) >= 2] + [n for n in p0[:12] if n not in p1]
        moved = [n for n in dict.fromkeys(moved) if any(e in ('dmg', 'close', 'long', 'fr', 'clip', 'head', 'proc', 'bounce', 'sp', 'melee', 'ls') for e, k, v in item_effects(n))][:6]
        for n in moved:
            f2, v2, rq = interactions(b, n, None if n in p0 else max(cps) // 2, [], None, False, f'--interactions {b["id"]} {n}')
            o.append(f"  {n}: {v2} [{f2}]")
        if not moved: o.append('  none (no damage/stat item moves between A0 and the top alternative)')
    except Exception as ex: o.append(f'  interaction pass failed: {ex}')
    o.append('\n## KEY TRADE-OFFS'); o += ['  - ' + t for t in trade_offs]
    o.append('\n## MISSING EVIDENCE (what is only assumed; what would settle it)'); o += ['  - ' + m for m in missing]
    o.append(f"\n## CONCLUSION: {D['concl']}\n  {D['basis']}")
    txt = '\n'.join(o) + '\n'
    sha = body_sha(txt); lines = txt.split('\n'); k = next(i for i, l in enumerate(lines) if l.startswith('GENERATED:'))
    lines.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(lines)
    os.makedirs(os.path.dirname(outfile) or '.', exist_ok=True); open(outfile, 'w').write(txt)
    return txt
def verify_strategy(path):
    t = open(path).read(); m = re.search(r'^BODY-SHA: (\w+)', t, re.M)
    return bool(m and m.group(1) == body_sha(t))
def parse_cps(s):
    if '-' in s:
        a, b2 = s.split('-'); step = 2400
        if ':' in b2: b2, step = b2.split(':'); step = int(step)
        a = int(a); return list(range(a if a > 0 else step, int(b2) + 1, step))
    return [int(x) for x in s.split(',') if x]
def strategy_main(a, B):
    bid = a[1]; cps = parse_cps(a[2]); alts = []; P_over = {}; out = None; grid = 'full'; i = 3
    while i < len(a):
        if a[i] == '--alt': alts.append(a[i + 1]); i += 2
        elif a[i] == '--out': out = a[i + 1]; i += 2
        elif a[i] == '--grid': grid = a[i + 1]; i += 2
        elif a[i] == '--set': k, v = a[i + 1].split('='); P_over[k] = float(v); i += 2
        else: i += 1
    b = next(x for x in B if x['id'] == bid)
    argv = ' '.join(x for x in a if x != '--out' and x != out)
    S = strategy(b, cps, alts, P_over, grid, argv); D = decide(S)
    out = out or f"{SP}/council/evidence/strategy/{bid}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')}.txt"
    write_strategy(b, cps, S, D, out, argv); print('wrote', out); print('CONCLUSION:', D['concl'])

# ======================================================================================================
# ITEM x KIT INTERACTION MATRIX (Kieran 14:29; WEAKNESS_PROCESS J): for a candidate item, derive from game data how EACH of its effects interacts with
# normal shooting, every ability at its real tier (incl. the ultimate), passive stacks, owned item procs, lifesteal and the other owned items; price it in
# realistic combat windows (sustained 10 s fight, burst rotation, ult window) against EQUAL-SOUL alternatives inside the complete build state.
# usage: python3 -I abtimeline.py --interactions <build id> <item> [--at <souls>] [--vs <item>]... [--out f] [--no-requests]
#   --at default: the item's buy point in the build (compared against the item bought there), else the build state at 9600 souls (item added on top).
# Cells: WORKS / DOES NOT WORK (reason) / UNKNOWN (what is not in the data -> a sandbox test request, meta kind INTERACTION, queued via queue.js add).
# Grades: CALCULATED = game data + stated formula; ASSUMED = parameter; MEASURED = only when a validated sandbox result is cited (none yet).
IA_P = {'hit': 0.55, 'head': 0.15, 'close_share': 0.6, 'long_share': 0.4, 'W_sus': 10.0, 'W_burst': 3.0}
IA_VERSION = 'interaction-v1'
GUNKEYS = {'BaseAttackDamagePercent': 'dmg', 'CloseRangeBonusWeaponPower': 'close', 'LongRangeBonusWeaponPower': 'long', 'BonusFireRate': 'fr', 'FireRateBonus': 'fr',
           'BonusClipSizePercent': 'clip', 'BonusClipSize': 'clip', 'HeadShotBonusDamage': 'head', 'BulletLifestealPercent': 'ls', 'TechPower': 'sp', 'SpiritPower': 'sp',
           'BonusBulletSpeedPercent': 'vel', 'ProcChance': 'proc', 'BuildUpPerShot': 'proc', 'RicochetDamagePercent': 'bounce', 'NonPlayerBonusWeaponPower': 'npc',
           'BonusMeleeDamagePercent': 'melee', 'ActivatedFireRate': 'fr', 'TechRangeMultiplier': 'range', 'TechRadiusMultiplier': 'range',
           'BulletArmorReduction': 'shred', 'BulletResistReduction': 'shred', 'TechArmorDamageReduction': 'shred', 'MagicResistReduction': 'shred',
           'StackingGoldPerMinute': 'econ', 'BonusGoldPerMinute': 'econ', 'BonusSoulsPct': 'econ', 'ProcBaseAttackDamagePercent': 'oneshot',
           'CombatBarrier': 'active', 'GuardianWardCombatBarrier': 'active', 'TotalHealthRegen': 'active', 'HealPerStack': 'active', 'MaxHealthPercentAsDPS': 'active', 'BonusHealth': 'def', 'BulletResist': 'def', 'TechResist': 'def', 'MeleeResistPercent': 'def', 'BonusHealthRegen': 'def'}
EFF_TXT = {'dmg': 'weapon damage %', 'close': 'weapon damage % within range', 'long': 'weapon damage % beyond range', 'fr': 'fire rate (more bullets)', 'clip': 'magazine size',
           'head': 'headshot damage', 'ls': 'bullet lifesteal', 'sp': 'spirit power', 'vel': 'bullet velocity', 'proc': 'on-hit proc', 'bounce': 'bullet bounces',
           'npc': 'damage vs NPCs', 'melee': 'melee damage %', 'def': 'defence (not damage)',
           'range': 'ability range/radius', 'shred': 'enemy resist reduction', 'econ': 'soul income', 'oneshot': 'one empowered shot per cooldown', 'active': 'active effect (barrier/heal/aura)'}
def item_effects(n):
    s = (g69().get(n) or {}).get('stats', {}); out = []
    for k, v in s.items():
        e = GUNKEYS.get(k)
        if not e or num(v) in (None, 0): continue
        if e == 'proc' and k == 'ProcChance' and 'HeadShotBonusDamage' in s: continue
        if e == 'shred' and (num(v) or 0) > 0: continue
        if e in [x[0] for x in out] and e in ('range', 'active', 'econ', 'shred'): continue
        out.append((e, k, sval(n, k)))
    return out
def kit_components(R, T):
    """classify every ability at its tier from data (props, scale types, game text)."""
    C = []
    for sl in (1, 2, 3, 4):
        a = R['abil'][sl]; t = T[sl]; nmx = nm(R, sl); txt = hero_text(R['H']['ab'][sl] + '_desc')
        if t < 0: C.append(dict(slot=sl, name=nmx, tier='L', kind='locked', txt=txt)); continue
        P = at_tier(a, t); keys = set(P)
        gunmode = ('BonusFireRate' in keys or 'WeaponDamageBonus' in keys) and re.search(r'weapon|fire rate|firing|bullet', txt, re.I)
        stack = 'MaxStacks' in keys and ('DamageBonusFixedPerStack' in keys or re.search(r'per bullet hit|stack', txt, re.I))
        cards = 'CardResourcePerBulletHit' in keys
        wsc = [k for k, p in P.items() if p.get('isdmg') and p.get('stype') in ('EWeaponPower', 'EWeaponDPS', 'EBaseWeaponDamageIncrease', 'EBulletDamage') and k != 'DamageBonusFixedPerStack']
        msc = [k for k, p in P.items() if p.get('isdmg') and p.get('stype') in ('ELightMeleeDamage', 'EHeavyMeleeDamage')]
        sph = {k: v for k, (v, inst) in spirit_hits(P, 0).items() if k != 'MagicDamagePerBullet'}
        kind = 'gun-mode' if gunmode else 'stacks' if stack else 'cards' if cards else 'weapon-scaled' if wsc else 'melee-scaled' if msc else 'spirit' if sph else 'utility'
        attach = bool(re.search(r'\b(jump|attach|latch|hop|ride)\w*\b.{0,40}\ball(y|ies)\b', txt, re.I) or keys & {'HostDamageTakenPct', 'AllowHostOnEnemies'})
        allyweapon = bool(re.search(r'weapon.{0,80}(heal|allies)|syringe', txt, re.I) and any(re.search('Heal', k) for k in keys))
        rng = {k: (p.get('raw'), p.get('stype')) for k, p in P.items() if p.get('stype') in ('ETechRange', 'ETechRadius') and (p.get('v') or 0) > 0}
        C.append(dict(slot=sl, name=nmx, tier=tlabel(t), t=t, kind=kind, P=P, wsc=wsc, msc=msc, sph=list(sph), ult=a['type'] == 'EAbilityType_Ultimate', txt=txt,
                      unl='UnlimitedAmmo' in keys, ls='BulletLifesteal' in keys, mdb='MagicDamagePerBullet' in keys, attach=attach, allyweapon=allyweapon, rng=rng,
                      heal=sum((p.get('v') or 0) for k, p in P.items() if re.search(r'^Heal|HealingPerSecond|HealAmount', k))))
    return C

def ia_state(R, base_w, souls, add=None):
    owned = list(base_w['owned'])
    for ad in ([add] if isinstance(add, str) else (add or [])):
        it = item(ad); owned = [o for o in owned if o not in it['components']] + [ad]
    w = dict(base_w, owned=owned, souls=souls, n=(add if isinstance(add, str) else (add[-1] if add else None)) or base_w.get('n'))
    st = state(R, w); return w, st
def ia_windows(R, w, st, reading):
    """damage delivered in three windows for one complete state. reading: dict of UNKNOWN-cell readings
    ('fix_mult': per-stack flat bonus multiplied by weapon %; 'ult_ammo': ult consumes ammo). All formulas CALCULATED except IA_P (ASSUMED)."""
    HS = R.get('HS') or hero_stats(R['b']['hk']); R['HS'] = HS; R['_rl'] = reading.get('rl', 1.0) if reading.get('rl', 1.0) != 1.0 else None
    T = st['tA']; names = list(w['owned']); wp = weapon(R); C = kit_components(R, T); hit = IA_P['hit']
    attr = HS.get('attr', ''); IA_P['close_share'], IA_P['long_share'] = (0.8, 0.1) if 'CloseRange' in attr else (0.3, 0.6) if 'LongRange' in attr else (0.6, 0.3)   # ASSUMED from m_eWeaponAttributes
    act = [x for x in names if not (item(x) and item(x)['class'] in REG and REG[item(x)['class']] == 'imbue' and x not in st['imbues'])]
    cdr = cdr_pct([dict(n=x) for x in names])
    pct = st['wb'] + sum(sval(x, 'BaseAttackDamagePercent') for x in act if not sraw(x, 'LifeThreshold'))
    close = sum(sval(x, 'CloseRangeBonusWeaponPower') for x in act); longp = sum(sval(x, 'LongRangeBonusWeaponPower') for x in act)
    headp = sum(sval(x, 'HeadShotBonusDamage') for x in act)
    base_b = wp['dmg'] + st['boons'] * R['H']['bdl']
    fr_perm = sum(sval(x, 'BonusFireRate') + sval(x, 'FireRateBonus') for x in act if item(x)['class'] not in ('upgrade_healbuff', 'upgrade_tech_overflow', 'upgrade_quick_silver', 'upgrade_ethereal_bullets'))
    ls = sum(sval(x, 'BulletLifestealPercent') for x in act) / 100
    def gun_part(W, share_close, share_long, stacks_comp, unlimited=False):
        g = gun_model(R, st, act, dict(T), cdr, W, 0.5); bullets = g['bullets']; hits = bullets * hit
        m = 1 + (pct + close * share_close + longp * share_long) / 100
        dmg = hits * base_b * m * (1 + IA_P['head'] * headp / 100 / m) * shred_mult
        fx = 0.0; fx_proc = 0.0
        if stacks_comp:
            P = stacks_comp['P']; ps = apv(P, 'DamageBonusFixedPerStack', st['sp']); mx = pv(P, 'MaxStacks') or 40; per_hit = 1 + IA_P['head'] * ((pv(P, 'HeadshotStacks') or 1) - 1)
            n = hits; ramp = sum(min(i * per_hit, mx) for i in range(int(n))) * ps   # flat bonus summed over hits, stacks start at 0
            fx = ramp * (m if reading['fix_mult'] else 1.0)
            if pv(P, 'ProcDamage'): fx_proc = int(n * per_hit / (pv(P, 'ProcDamageStackCount') or 20)) * apv(P, 'ProcDamage', st['sp'])
        return dict(bullets=bullets, hits=hits, gun=dmg, fix=fx, fix_proc=fx_proc, heal=(dmg + fx) * ls, cyc=g['cyc'])
    stacks = next((c for c in C if c['kind'] == 'stacks'), None)
    # enemy bullet-resist reduction (on-hit/debuff items): damage x (1-(r-s))/(1-r), r = reference enemy resist at these souls; below 0 resist the same linear
    # formula is used (ASSUMED: the game's negative-resist formula is not in data -> UNKNOWN cell, test with eresist readback)
    r_e = enemy_at(st['souls'] / STRAT_P['E_SPM'][0], {k: v[0] for k, v in STRAT_P.items()}, HB_of())['res']
    shred = sum(-(sval(x, 'BulletArmorReduction') or 0) - (sval(x, 'BulletResistReduction') or 0) for x in act) / 100
    shred_mult = (1 - (r_e - shred)) / (1 - r_e) if shred else 1.0
    # procs of owned items (count hits; damage where the item states it)
    def procs(hits, W):
        tot = 0.0; rows = []
        for x in act:
            s = (g69().get(x) or {}).get('stats', {})
            if 'DamagePerChain' in s:
                n = min(hits * sval(x, 'ProcChance') / 100, W / (sval(x, 'ProcCooldown') or 0.2)); d = n * sval(x, 'DamagePerChain', st['sp']); tot += d; rows.append((x, n, d))
            elif 'ProcBonusMagicDamage' in s:
                n = min(hits, W / (sval(x, 'AbilityCooldown') or 8) + 1); d = n * sval(x, 'ProcBonusMagicDamage', st['sp']); tot += d; rows.append((x, n, d))
            elif 'StealPerHit' in s:
                n = min(hits, W / (sval(x, 'ProcCooldown') or 1.2)); rows.append((x, n, 0.0))
            elif 'BuildUpPerShot' in s:
                n = hits * sval(x, 'BuildUpPerShot') / 100; rows.append((x, n, 0.0))   # build-up % gained in the window (proc at 100)
            if 'ProcBaseAttackDamagePercent' in s:   # one empowered bullet per internal cooldown: count procs in THIS window (no continuous bonus)
                n = min(1.0 if hits else 0.0, hits) + int(W / (sval(x, 'AbilityCooldown') or 8)) * (1 if hits > 1 else 0); d = n * base_b * sval(x, 'ProcBaseAttackDamagePercent', st['sp'], st['boons']) / 100
                tot += d; rows.append((x, n, d))
        return tot, rows
    out = {}
    # sustained 10 s fight on one target
    gs = gun_part(IA_P['W_sus'], IA_P['close_share'], IA_P['long_share'], stacks); pr, prow = procs(gs['hits'], IA_P['W_sus'])
    spirit = 0.0
    for c in C:
        if c['kind'] in ('locked', 'utility', 'gun-mode', 'stacks') or c.get('ult'): continue
        if c['kind'] in ('spirit', 'cards'):
            P = c['P']; s2 = slot_sp(R, st, c['slot'], c['t']); hitsd = {k: v for k, (v, inst) in spirit_hits(P, s2).items() if inst and k != 'MagicDamagePerBullet'}
            cd = pv(P, 'AbilityCooldown') or 30
            if c['kind'] == 'cards':
                ncards = gs['hits'] / ((pv(P, 'ResourcePerCard') or 100) / (pv(P, 'CardResourcePerBulletHit') or 4)) + 0.5 * charges(R['abil'][c['slot']], c['t'])
                spirit += ncards * sum(hitsd.values()); c['cards'] = ncards
            else: spirit += sum(hitsd.values()) * (1 + int(IA_P['W_sus'] / max(cd, 1)))
    md = 0.0
    for c in C:
        if c.get('mdb') and c['kind'] != 'locked':
            P = c['P']; up = min(1.0, (pv(P, 'AbilityDuration') or 5) / IA_P['W_sus']); md += apv(P, 'MagicDamagePerBullet', slot_sp(R, st, c['slot'], c['t'])) * gs['hits'] * up
    # melee (melee-relevant kits only; same ASSUMED cadence as --strategy: 4 light + 1 heavy per 8 s in range, melee_u 0.5)
    mel_s = mel_b = 0.0
    if melee_relevant(R, names):
        mp = sum(sval(x, 'BonusMeleeDamagePercent') for x in names) / 100; L_ = (HS['light'] + HS['melee_lvl'] * st['boons']) * (1 + mp)
        H_ = (HS['heavy'] + HS['melee_lvl'] * st['boons']) * (1 + mp + sum(sval(x, 'BonusHeavyMeleeDamage') for x in names) / 100)
        mab = sum((p.get('scale') or 0) * (HS['light'] + HS['melee_lvl'] * st['boons']) for c in C if c['kind'] == 'melee-scaled' for k, p in c['P'].items() if p.get('stype') == 'ELightMeleeDamage' and p.get('isdmg'))
        mel_s = 0.5 * (4 * L_ + H_) * IA_P['W_sus'] / 8 + mab; mel_b = L_ + H_ + mab
    out['sustained'] = dict(total=gs['gun'] + gs['fix'] + gs['fix_proc'] + pr + spirit + md + mel_s, melee=mel_s, gun=gs['gun'], fix=gs['fix'] + gs['fix_proc'], procs=pr, spirit=spirit + md, heal=gs['heal'], bullets=gs['bullets'], prow=prow,
                            stack_time=(None if not stacks else (pv(stacks['P'], 'MaxStacks') or 40) / max(1e-9, gs['hits'] / IA_P['W_sus'] * (1 + IA_P['head'] * ((pv(stacks['P'], 'HeadshotStacks') or 1) - 1)))))
    # burst rotation: every trained non-ult ability once + W_burst s of gun from 0 stacks
    gb = gun_part(IA_P['W_burst'], IA_P['close_share'], IA_P['long_share'], stacks); pb, _ = procs(gb['hits'], IA_P['W_burst']); sb = 0.0
    for c in C:
        if c['kind'] in ('spirit',) and not c.get('ult'):
            sb += sum(v for k, (v, inst) in spirit_hits(c['P'], slot_sp(R, st, c['slot'], c['t'])).items() if inst and k != 'MagicDamagePerBullet')
    out['burst'] = dict(total=gb['gun'] + gb['fix'] + gb['fix_proc'] + pb + sb + mel_b, melee=mel_b, gun=gb['gun'], fix=gb['fix'], procs=pb, spirit=sb, heal=gb['heal'], bullets=gb['bullets'])
    # ult window
    u = next((c for c in C if c.get('ult') or (c['slot'] == 4 and c['kind'] == 'locked')), None)
    if not u or u['kind'] == 'locked': out['ult'] = dict(total=0.0, note='ultimate not trained at this checkpoint')
    elif u['kind'] == 'gun-mode':
        P = u['P']; dur = apv(P, 'AbilityDuration', st['sp']); fr_u = pv(P, 'BonusFireRate') or 0; floor = pv(P, 'MinRoundsPerSecond') or 0
        rps = max(floor, (1 / wp['cyc']) * (1 + (fr_perm + fr_u) / 100)); bullets = rps * dur
        if reading['ult_ammo']:   # ult consumes the magazine: clip, then a reload inside the window
            clip = wp['clip'] * (1 + sum(sval(x, 'BonusClipSizePercent') for x in act) / 100) + sum(sval(x, 'BonusClipSize') for x in act)
            rl = wp['reload']; bullets = min(bullets, clip + max(0.0, dur - clip / rps - rl) * rps)
        r_u = num(str((P.get('Radius') or {}).get('raw') or '16')) or 16; r_c = max([num(str(sraw(x, 'CloseRangeBonusDamageRange') or '15')) or 15 for x in act if sraw(x, 'CloseRangeBonusWeaponPower')] or [15])
        share_c = min(1.0, (r_c / r_u) ** 2)   # ASSUMED: targets spread uniformly over the ult area
        m = 1 + (pct + close * share_c) / 100; flat = apv(P, 'WeaponDamageBonus', st['sp'])
        hits = bullets   # 'perfect accuracy' (game text)
        dmg = hits * (base_b + flat) * m
        fx = 0.0
        if stacks:
            ps = apv(stacks['P'], 'DamageBonusFixedPerStack', st['sp']); mx = pv(stacks['P'], 'MaxStacks') or 40
            fx = sum(min(i, mx) for i in range(int(hits))) * ps * (m if reading['fix_mult'] else 1.0)   # all hits on ONE target (upper bound; ASSUMED)
        pu, _ = procs(hits, dur)
        out['ult'] = dict(total=dmg + fx + pu, gun=dmg, fix=fx, procs=pu, heal=(dmg + fx) * ls, bullets=bullets, dur=dur, share_close=share_c, rps=rps)
    else:
        P = u['P']; s2 = slot_sp(R, st, u['slot'], u['t']); d = 0.0; du = pv(P, 'AbilityDuration') or pv(P, 'AbilityChannelTime') or 1
        for k, (v, inst) in spirit_hits(P, s2).items():
            d += apv(P, k, s2) * du if re.search('DPS|PerSecond', k) else v
        mel = sum((p.get('scale') or 0) * (HS['light'] + HS['melee_lvl'] * st['boons']) for k, p in P.items() if p.get('stype') == 'ELightMeleeDamage' and p.get('isdmg'))
        out['ult'] = dict(total=d + mel, gun=0.0, spirit=d, note=f"{u['name']} damage is {u['kind']} (no weapon bullets)")
    R['_rl'] = None
    return out, C

def item_targeting(n):
    it = item(n); b = block('abilities.vdata', it['class']) if it else ''; b = b or ''
    g = lambda k: (re.search(k + r' = "?([^"\n]*)"?', b) or [None, ''])[1]
    return dict(act=g('m_eAbilityActivation').replace('CITADEL_ABILITY_ACTIVATION_', ''), loc=g('m_eAbilityTargetingLocation').replace('CITADEL_ABILITY_TARGETING_LOCATION_', ''),
                types=g('m_nAbilityTargetTypes').replace('CITADEL_UNIT_TARGET_', ''), shape=g('m_eAbilityTargetingShape').replace('CITADEL_ABILITY_TARGETING_SHAPE_', ''),
                bits=g('m_AbilityBehaviorsBits'), imbue=g('m_TargetAbilityEffectsToApply').replace('CITADEL_TARGET_ABILITY_BEHAVIOR_', ''))
def ia_matrix(R, C, cand, st_with):
    """cells (effect x component) with status/reason/grade."""
    E = item_effects(cand); cells = []; names = st_with['own_names']
    pool_dmg = st_with['pool_dmg']; pool_fr = st_with['pool_fr']
    for e, k, v in E:
        row = {'effect': f"{EFF_TXT[e]} ({k}={v:g})", 'e': e, 'cells': []}
        def add(comp, status, why, grade='CALCULATED'): row['cells'].append((comp, status, why, grade))
        # normal shooting
        if e in ('dmg', 'head', 'fr', 'clip', 'ls', 'proc', 'bounce'): add('normal shooting', 'WORKS', {'dmg': f'multiplies every bullet (weapon % pool now {pool_dmg:.0f}%: +{v:g} adds {v/(100+pool_dmg)*100:.1f}% relative)', 'head': f'headshot share {IA_P["head"]} ASSUMED',
                'fr': f'more bullets per second (fire-rate pool now {pool_fr:.0f}%: +{v:g} adds {v/(100+pool_fr)*100:.1f}% bullets)', 'clip': 'fewer reloads in long fights', 'ls': 'heals a share of bullet damage', 'proc': 'per-bullet proc', 'bounce': f"bounces need a 2nd enemy within {sraw(cand,'RicochetRadius') or '?'}: 0 in these single-target windows; vs groups/camps priced in --strategy (p2hero, N_NPC)"}[e])
        elif e == 'close': add('normal shooting', 'WORKS (conditional)', f"only within {sraw(cand,'CloseRangeBonusDamageRange') or '15m'}; close-range share {IA_P['close_share']} ASSUMED", 'CALCULATED+ASSUMED')
        elif e == 'long': add('normal shooting', 'WORKS (conditional)', f"only beyond {sraw(cand,'LongRangeBonusWeaponPowerMinRange') or '15m'}; share {IA_P['long_share']} ASSUMED", 'CALCULATED+ASSUMED')
        elif e == 'vel': add('normal shooting', 'UNKNOWN', 'bullet speed changes hit rate on moving targets; no accuracy model in data or sandbox (GAPS 16)', 'UNKNOWN')
        elif e == 'sp': add('normal shooting', 'DOES NOT WORK', 'weapon damage does not scale with spirit power (gun has no spirit-scaled property)')
        elif e == 'npc': add('normal shooting', 'DOES NOT WORK (vs heroes)', 'NPC-only bonus; farming value priced in --strategy')
        elif e == 'melee': add('normal shooting', 'DOES NOT WORK', 'melee % does not touch bullets')
        elif e == 'shred': add('normal shooting', 'WORKS' if 'Bullet' in k else 'DOES NOT WORK', ('lowers enemy bullet resist: value from the resist formula (RESIST SHRED section)' if 'Bullet' in k else 'spirit-resist shred does not change bullet damage'), 'CALCULATED+ASSUMED' if 'Bullet' in k else 'CALCULATED')
        elif e == 'oneshot': add('normal shooting', 'WORKS (once per cooldown)', f"one empowered bullet every {sraw(cand,'AbilityCooldown') or '?'} s: averaged over the window, not a continuous bonus (PROC/BUFF section)", 'CALCULATED')
        elif e in ('range', 'econ', 'active'): add('normal shooting', 'n/a', {'range': 'ability range/radius only', 'econ': 'soul income: ECONOMY section', 'active': 'active item effect: see self / ally columns'}[e])
        else: add('normal shooting', 'n/a', 'defensive stat; valued by --strategy (survival), not damage')
        for c in C:
            comp = f"{c['slot']}={c['name']} {c['tier']}{' (ULT)' if c.get('ult') else ''} [{c['kind']}]"
            if c['kind'] == 'locked': add(comp, 'n/a', 'not trained at this checkpoint', 'CALCULATED'); continue
            K = c['kind']
            if e == 'range':
                if not c['rng']: add(comp, 'DOES NOT WORK', 'ability has no range/radius property (no ETechRange/ETechRadius stat)')
                else: add(comp, 'WORKS', 'scales ' + ', '.join(f"{kk}={vv[0]}" for kk, vv in c['rng'].items()) + (' (imbue: only the ONE imbued ability)' if REG.get(item(cand)['class']) == 'imbue' else '') + '; value in IMBUE/RANGE section', 'CALCULATED')
                continue
            if e == 'shred':
                hit_t = ('Bullet' in k and K in ('gun-mode', 'stacks')) or ('Bullet' not in k and K in ('spirit', 'cards'))
                add(comp, 'WORKS' if hit_t else 'DOES NOT WORK', 'its damage type is the one shredded' if hit_t else 'shred type does not match this damage', 'CALCULATED'); continue
            if e in ('econ', 'active', 'oneshot'):
                add(comp, 'UNKNOWN' if (e == 'oneshot' and K == 'gun-mode') else 'n/a', 'whether the empowered shot fires inside the ability is not in data' if (e == 'oneshot' and K == 'gun-mode') else 'no interaction with this ability', 'UNKNOWN' if (e == 'oneshot' and K == 'gun-mode') else 'CALCULATED'); continue
            if c.get('attach') and e in ('def',): add(comp + ' (attached ally)', 'UNKNOWN', 'passive stat while attached to an ally: data does not say if it is shared; attach ability has ' + ', '.join(x for x in ('BonusItemRangePercent', 'BonusItemDurationPercent', 'BonusBarrierAmpPercent') if x in c['P']), 'UNKNOWN')
            if e == 'def': add(comp, 'n/a', 'defensive stat'); continue
            if K == 'gun-mode':
                if e in ('dmg', 'head', 'proc', 'ls', 'bounce'): add(comp, 'WORKS', f"ability fires the weapon (game text: '{c['txt'][:60]}...'); bullets take weapon bonuses" + (' and its own flat WeaponDamageBonus' if 'WeaponDamageBonus' in c['P'] else ''))
                elif e == 'close':
                    r = (c['P'].get('Radius') or {}).get('raw'); add(comp, 'WORKS (partly)', f"bullets within {sraw(cand,'CloseRangeBonusDamageRange') or '15m'} of a {r or '?'} radius: share (15/r)^2 ASSUMED uniform targets" if r else 'range of the ability not in data', 'CALCULATED+ASSUMED')
                elif e == 'long': add(comp, 'WORKS (partly)', 'only targets beyond the range threshold inside the ability area', 'CALCULATED+ASSUMED')
                elif e == 'fr': add(comp, 'WORKS', f"adds to the ability's own BonusFireRate={pv(c['P'],'BonusFireRate') or 0:g}" + (f"; floor MinRoundsPerSecond={pv(c['P'],'MinRoundsPerSecond'):g}" if pv(c['P'], 'MinRoundsPerSecond') else '') + ' (additive stacking ASSUMED)', 'CALCULATED+ASSUMED')
                elif e == 'clip':
                    if c.get('unl'): add(comp, 'DOES NOT WORK', 'ability has UnlimitedAmmo at this tier')
                    else: add(comp, 'UNKNOWN', 'whether the ability consumes the magazine is not in the data (no ammo key); both readings priced', 'UNKNOWN')
                elif e == 'sp': add(comp, 'WORKS (duration only)' if (c['P'].get('AbilityDuration') or {}).get('scale') else 'DOES NOT WORK', 'spirit scales AbilityDuration (more bullets)' if (c['P'].get('AbilityDuration') or {}).get('scale') else 'no spirit-scaled property')
                else: add(comp, 'DOES NOT WORK', 'no matching mechanic')
            elif K == 'stacks':
                if e == 'fr': add(comp, 'WORKS', f"stacks per bullet hit (game text; HeadshotStacks={pv(c['P'],'HeadshotStacks') or 1:g}): more bullets -> max stacks sooner" + ('; also more ProcDamage procs per 20 stacks' if pv(c['P'], 'ProcDamage') else ''))
                elif e in ('dmg', 'close', 'long', 'head'): add(comp, 'UNKNOWN', 'per-stack bonus is a FLAT bullet damage add (EBaseWeaponDamageIncrease); whether weapon % multiplies it is not in the data; both readings priced. Stack RATE is unchanged (counts hits, not damage)', 'UNKNOWN')
                elif e == 'clip': add(comp, 'WORKS (indirect)', 'fewer reload gaps; stacks expire after AbilityDuration if you stop hitting')
                elif e == 'ls': add(comp, 'WORKS', 'heals from the stacked bonus damage too')
                else: add(comp, 'DOES NOT WORK', 'stacks count bullet hits only')
            elif K == 'cards':
                if e == 'fr': add(comp, 'WORKS', f"cards are earned per bullet hit (CardResourcePerBulletHit={pv(c['P'],'CardResourcePerBulletHit'):g}, {pv(c['P'],'ResourcePerCard') or 100:g} per card)")
                elif e == 'sp': add(comp, 'WORKS', 'card damage scales with spirit power')
                elif e in ('dmg', 'close', 'long', 'head'): add(comp, 'DOES NOT WORK', 'card resource counts hits, card damage is spirit-scaled (Damage ETechPower)')
                else: add(comp, 'DOES NOT WORK', 'no matching mechanic')
            elif K == 'weapon-scaled':
                if e == 'dmg': add(comp, 'WORKS (data scale function)', f"{c['wsc']} use weapon-damage scaling; exact formula with item % not verified", 'CALCULATED')
                elif e in ('close', 'long', 'head'): add(comp, 'UNKNOWN', 'conditional weapon % on weapon-scaled ability damage: not in data', 'UNKNOWN')
                elif e == 'sp': add(comp, 'DOES NOT WORK', 'weapon-scaled, not spirit')
                else: add(comp, 'DOES NOT WORK', 'ability damage is not bullets')
            elif K == 'melee-scaled':
                if e == 'melee': add(comp, 'WORKS', 'scales with melee damage')
                elif e in ('dmg', 'close', 'long', 'fr', 'head'): add(comp, 'UNKNOWN' if e != 'fr' else 'DOES NOT WORK', f"damage {c['msc']} scales with melee damage; whether weapon-% bonuses also apply is not in data" if e != 'fr' else 'melee-scaled hit, no bullets', 'UNKNOWN' if e != 'fr' else 'CALCULATED')
                elif e == 'sp': add(comp, 'WORKS' if c['sph'] else 'DOES NOT WORK', 'spirit part ' + str(c['sph'][:2]) if c['sph'] else 'no spirit-scaled part')
                else: add(comp, 'DOES NOT WORK', f"damage {c['msc']} scales with melee damage")
            elif K == 'spirit':
                bullet_trig = bool(re.search(r'\bbullets?\b|\bshots?\b|\bshooting\b|your weapon', c['txt'], re.I))
                if e == 'sp': add(comp, 'WORKS', f"spirit-scaled damage {c['sph'][:3]}")
                elif bullet_trig and e in ('fr', 'clip', 'proc', 'bounce'): add(comp, 'UNKNOWN', f"spirit damage triggered by shooting (game text: '{c['txt'][:70]}...'): whether more bullets trigger it more often is not in data (trigger rate/limit)", 'UNKNOWN')
                else: add(comp, 'DOES NOT WORK', f"damage {c['sph'][:3]} scales with spirit power (ETechPower), not weapon damage/bullets")
            else:
                if c.get('ls') and e in ('dmg', 'close', 'fr', 'ls'): add(comp, 'WORKS (sustain)', 'tier adds BulletLifesteal after use: more bullet damage -> more healing')
                elif c.get('mdb') and e == 'fr': add(comp, 'WORKS', 'spirit damage per bullet: more bullets -> more spirit damage')
                else: add(comp, 'NO INTERACTION', 'ability has no damage/bullet/stack property at this tier')
            if c.get('mdb') and K != 'utility':
                if e == 'fr': add(comp + ' bullets', 'WORKS', 'MagicDamagePerBullet: more bullets -> more spirit damage')
                elif e in ('dmg', 'close'): add(comp + ' bullets', 'DOES NOT WORK', 'per-bullet spirit damage is spirit-scaled, not weapon %')
        # owned item procs / lifesteal / other items
        # ordinary melee (every hero)
        if e == 'melee': add('melee (light/heavy)', 'WORKS', 'melee damage %')
        elif e in ('dmg', 'close', 'long'): add('melee (light/heavy)', 'UNKNOWN', 'melee damage is ELightMeleeDamage/EHeavyMeleeDamage; whether weapon-% (incl. range-conditional) bonuses apply to melee is not in data', 'UNKNOWN')
        # self-cast vs ally: item targeting from vdata (m_eAbilityActivation / m_eAbilityTargetingLocation / m_nAbilityTargetTypes)
        tg = item_targeting(cand); att = [c for c in C if c.get('attach') and c['kind'] != 'locked']; aw = [c for c in C if c.get('allyweapon') and c['kind'] != 'locked']
        if e == 'active':
            add('self', 'WORKS' if tg['loc'] in ('SELF', '') or 'ALLOW_SELF_CAST' in tg['bits'] else 'n/a', f"activation {tg['act'] or '?'}, targeting {tg['loc'] or '?'}, targets {tg['types'] or 'self'}", 'CALCULATED')
            if 'HERO_FRIENDLY' in tg['types'] and tg['loc'] == 'UNIT': add('targeted ally', 'WORKS', 'item can target a friendly hero (data)', 'CALCULATED')
            elif 'HERO_FRIENDLY' in tg['types']: add('allies nearby', 'WORKS', f"affects friendly heroes around you (data: {tg['types']}, shape {tg['shape'] or '?'})", 'CALCULATED')
            for c in (att if not ('HERO_FRIENDLY' in tg['types'] and tg['loc'] == 'UNIT') else []): add(f"attached ally via {c['name']}", 'UNKNOWN', f"self-targeted item ({tg['loc']}) while attached: transfer to the host is not stated in data; attach ability has {', '.join(x for x in ('BonusItemRangePercent', 'BonusItemDurationPercent', 'BonusBarrierAmpPercent') if x in c['P']) or 'no item keys'}", 'UNKNOWN')
        elif e in ('def', 'ls') and att: add(f"attached ally via {att[0]['name']}", 'UNKNOWN' if e != 'def' else 'DOES NOT WORK (ASSUMED)', 'passive stat on the holder; sharing with the host is not in data' if e != 'def' else 'passive health/resist stays on the holder (no sharing rule in data)', 'UNKNOWN' if e != 'def' else 'ASSUMED')
        for c in aw:
            if k in ('ActivatedFireRate',) or (k or '').startswith('Activated'): add(f"ally hits via {c['name']}", 'UNKNOWN', 'on-hit trigger ("bullets hit a hero"): whether bullets that hit ALLIES count as hero hits is not in data', 'UNKNOWN')
            elif e in ('fr', 'clip'): add(f"ally hits via {c['name']}", 'WORKS', f"more {'shots' if e == 'fr' else 'shots per magazine'} = more heal bullets (heal keys {[x for x in c['P'] if 'Heal' in x][:3]})", 'CALCULATED')
            elif e in ('proc', 'oneshot', 'bounce') or k == 'ActivatedFireRate': add(f"ally hits via {c['name']}", 'UNKNOWN', 'whether bullets that hit ALLIES trigger this on-hit effect is not in data', 'UNKNOWN')
            elif e in ('dmg', 'close', 'long', 'head'): add(f"ally hits via {c['name']}", 'DOES NOT WORK' if not any(c['P'][x].get('stype') in ('EWeaponPower', 'EBulletDamage', 'EBaseWeaponDamageIncrease') for x in c['P'] if 'Heal' in x) else 'UNKNOWN', 'heal per shot is not weapon-damage scaled (heal keys have no weapon scale type)', 'CALCULATED')
        prow = [x for x in names if any(kk in ((g69().get(x) or {}).get('stats', {})) for kk in ('ProcChance', 'BuildUpPerShot', 'StealPerHit', 'DamagePerChain', 'ActivatedFireRate')) and x != cand]
        for x in prow:
            s = (g69().get(x) or {}).get('stats', {})
            if e == 'fr': add(f'owned proc {x}', 'WORKS', 'more bullets -> more procs/build-up' + (f" (capped by cooldown {s.get('ProcCooldown') or s.get('AbilityCooldown')})" if s.get('ProcCooldown') or s.get('AbilityCooldown') else ''))
            elif e in ('dmg', 'close', 'long', 'head'): add(f'owned proc {x}', 'DOES NOT WORK', 'proc count follows hits, its damage is fixed/spirit')
            elif e == 'clip': add(f'owned proc {x}', 'WORKS (indirect)', 'less reload downtime -> more hits')
        lsrc = [x for x in names if sraw(x, 'BulletLifestealPercent') and x != cand]
        if lsrc and e in ('dmg', 'close', 'long', 'fr', 'head'): add('lifesteal ' + ','.join(lsrc), 'WORKS', 'heal = bullet damage x lifesteal %')
        if e == 'dmg' and pool_dmg: add('other weapon % items', 'WORKS (diminishing)', f'additive pool {pool_dmg:.0f}% (incl. invest bonus): relative gain {v/(100+pool_dmg)*100:.1f}%')
        if e == 'fr' and pool_fr: add('other fire-rate items', 'WORKS (diminishing)', f'additive pool {pool_fr:.0f}%: relative gain {v/(100+pool_fr)*100:.1f}%')
        cells.append(row)
    return cells

SEL_KINDS = ('build-decision', 'discovery', 'weakness-remedy', 'requested', 'calibration')
def interactions(b, cand, at=None, vs=None, out=None, requests=True, argv='', sel=None):
    R = analyse(b); R['HS'] = hero_stats(b['hk']); rows = [r for r in R['rows'] if not r.get('unknown')]
    inb = next((r for r in rows if r['n'] == cand), None)
    if not sel:   # selection provenance, pre-registered (never written after the result)
        sel = (dict(kind='build-decision', reason=f"{cand} is bought at {inb['souls']} souls in {b['id']}: checking what it improves in the kit against equal-soul options") if inb else
               dict(kind='requested', reason=f"{cand} is not in {b['id']}; compared on request (worked example / explicit --vs), not derived from a {b['hero']} weakness"))
    R['_sel'] = sel
    if at is None and inb: at = inb['souls']; mode = 'buy-point'
    else: at = at or 9600; mode = 'buy-point' if (inb and inb['souls'] == at) else 'add-on-top'
    if mode == 'buy-point':
        prev = [r for r in rows if r['souls'] < at]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': 0, 'owned': [], 'imbues': {}, 'box': ''}
        base_w = dict(base_w, owned=[o for o in base_w['owned']]); souls_base = base_w['souls']
    else:
        prev = [r for r in rows if r['souls'] <= at]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': 0, 'owned': [], 'imbues': {}, 'box': ''}; souls_base = at
    cost = lambda m: SOULS[item(m)['tier']] - sum(SOULS[item(c)['tier']] for c in item(m)['components'] if c in base_w['owned'])
    my = cost(cand)
    upg_owned = lambda m: any(m in item(o)['components'] for o in base_w['owned'])
    alts = []
    for m2, g in items().items():
        if m2 == cand or g.get('disabled') or m2 in base_w['owned'] or upg_owned(m2) or not item(m2): continue
        if cost(m2) != my: continue
        ef = {e for e, k, v in item_effects(m2)}
        if not ef & {'dmg', 'close', 'long', 'fr', 'clip', 'head', 'proc', 'bounce'}: continue
        if any(num(v) is not None and num(v) < 0 for kk, v in ((g69().get(m2) or {}).get('stats', {})).items() if kk in ('BonusHealth', 'BulletResist', 'TechResist', 'MaxHealthLossPercent')): continue
        alts.append(m2)
    if inb and mode == 'buy-point' and cand not in alts: pass
    for v2 in (vs or []):
        if v2 not in alts and item(v2): alts.append(v2)
    rl_unknown = weapon(R)['reload_src'].startswith('ASSUMED')
    if not out: out = f"{SP}/council/evidence/interaction/{b['id']}_{re.sub(r'\W+', '_', cand)}_{at}.txt"
    out = os.path.relpath(out, SP) if out.startswith(SP) else out
    readings = [dict(fix_mult=fm, ult_ammo=ua, rl=rs) for fm in (True, False) for ua in (False, True) for rs in ((1.0, 0.6) if rl_unknown else (1.0,))]
    S = souls_base + (my if mode == 'add-on-top' else at - souls_base)
    def eval_item(m2):
        w, st = ia_state(R, base_w, souls_base + (cost(m2) if mode == 'add-on-top' else at - souls_base), m2)
        res = [ia_windows(R, w, st, rd)[0] for rd in readings]; return w, st, res
    wb0, stb0 = ia_state(R, base_w, S, None); base = [ia_windows(R, wb0, stb0, rd)[0] for rd in readings]
    wc, stc, resc = eval_item(cand); _, C = ia_windows(R, wc, stc, readings[0])
    pool_dmg = stc['wb'] + sum(sval(x, 'BaseAttackDamagePercent') for x in wc['owned'] if x != cand)
    pool_fr = sum(sval(x, 'BonusFireRate') + sval(x, 'FireRateBonus') for x in wc['owned'] if x != cand)
    cells = ia_matrix(R, C, cand, dict(own_names=wc['owned'], pool_dmg=pool_dmg, pool_fr=pool_fr))
    AR = {cand: resc}
    for m2 in alts: AR[m2] = eval_item(m2)[2]
    keep = sorted([m2 for m2 in alts if m2 not in (vs or [])], key=lambda m2: -AR[m2][0]['sustained']['total'])[:8]
    AR = {m2: v for m2, v in AR.items() if m2 == cand or m2 in keep or m2 in (vs or [])}
    flags = {}
    for m2 in AR:
        f_ = []
        if cost(m2) != my: f_.append(f"NOT EQUAL SOULS ({cost(m2)} vs {my})")
        s_ = (g69().get(m2) or {}).get('stats', {})
        if any(k in s_ for k in ('BonusFireRate', 'FireRateBonus')) and ('AbilityDuration' in s_ or 'BuffDuration' in s_) and 'ActivatedFireRate' not in s_ and item(m2)['class'] not in ('upgrade_ricochet', 'upgrade_quick_silver', 'upgrade_tech_overflow', 'upgrade_ethereal_bullets'):
            f_.append('fire rate is a timed buff, counted as always on (upper bound)')
        if sraw(m2, 'LifeThreshold'): f_.append('stats only above a health threshold')
        if sraw(m2, 'HealthDrainedPerSecond'): f_.append(f"costs {sraw(m2, 'HealthDrainedPerSecond')} health per second while on (not netted)")
        if item(m2)['class'] in REG and REG[item(m2)['class']] in ('heal', 'selfhp', 'taken', 'stack'): f_.append(f"conditional item ({REG[item(m2)['class']]}): counted as if its condition is met (upper bound)")
        flags[m2] = f_
    eqall = [m2 for m2 in AR if not any(x.startswith('NOT EQUAL') for x in flags[m2])]
    eq = [m2 for m2 in eqall if not flags[m2] or m2 == cand]   # unconditional equal-soul options decide; conditional ones are upper bounds
    WIN = ('sustained', 'burst', 'ult')
    # ranking per window per reading; verdict
    rank = {}
    for wi in WIN:
        for ri, rd in enumerate(readings):
            vals = {m2: AR[m2][ri][wi]['total'] for m2 in eq}; rank[(wi, ri)] = sorted(vals, key=lambda m2: -vals[m2])
    top_by_win = {wi: {rank[(wi, ri)][0] for ri in range(len(readings))} for wi in WIN}
    unknown_flip = [wi for wi in WIN if len(top_by_win[wi]) > 1]
    def rel(wi, m2, ri=0):
        a = AR[m2][ri][wi]['total']; b0 = base[ri][wi]['total']; return (a / b0 - 1) * 100 if b0 else 0.0
    best_alt = {wi: max([m2 for m2 in AR if m2 != cand] or [None], key=lambda m2: AR[m2][0][wi]['total'] if m2 else 0) for wi in WIN}
    wins = [wi for wi in WIN if base[0][wi]['total'] and rank[(wi, 0)][0] == cand]
    real = [wi for wi in WIN if base[0][wi]['total'] > 0]
    ub = sorted({m2 for m2 in eqall if m2 not in eq for wi in WIN if base[0][wi]['total'] and AR[m2][0][wi]['total'] > AR[cand][0][wi]['total'] * 1.02})
    if unknown_flip: verdict = f"INSUFFICIENT EVIDENCE: the best item in the {', '.join(unknown_flip)} window depends on UNKNOWN cells (see test requests)"
    elif real and all(rank[(wi, 0)][0] == cand for wi in real): verdict = f"{cand} delivers the most damage of the equal-soul options in every window ({', '.join(real)})"
    elif real and not any(rank[(wi, 0)][0] == cand for wi in real):
        verdict = f"{cand} is beaten in every window: " + '; '.join(f"{wi}: {rank[(wi,0)][0]}" for wi in real)
    else: verdict = 'DEPENDS ON COMBAT WINDOW: ' + '; '.join(f"{wi} -> {rank[(wi,0)][0]}" for wi in real)
    pair = []
    for v2 in (vs or []):
        if v2 not in AR: continue
        ws = []
        for wi in WIN:
            if not base[0][wi]['total'] and not AR[cand][0][wi]['total']: continue
            d = [(AR[cand][ri][wi]['total'] / max(1e-9, AR[v2][ri][wi]['total']) - 1) * 100 for ri in range(len(readings))]
            ws.append(f"{wi}: {cand} {min(d):+.0f}..{max(d):+.0f}% vs {v2} -> " + ('WINS in every reading' if min(d) > 2 else 'LOSES in every reading' if max(d) < -2 else 'TIE (within 2% in every reading)' if max(abs(x) for x in d) <= 2 else 'DEPENDS on UNKNOWN cells'))
        pair.append(f"{cand} vs {v2}" + (' [' + '; '.join(flags.get(v2, [])) + ']' if flags.get(v2) else '') + ': ' + ' | '.join(ws))
    # test requests for UNKNOWN cells
    if rl_unknown: cells.append({'effect': f"reload time of {b['hero']}'s gun (ASSUMED {weapon(R)['reload']} s)", 'e': 'reload', 'cells': [('normal shooting', 'UNKNOWN', 'reload duration is animation-defined, not in vdata; magazine/fire-rate items change reload count; readings x1.0 and x0.6 priced', 'UNKNOWN')]})
    unk = [(r['effect'], c) for r in cells for c in r['cells'] if c[1] == 'UNKNOWN']
    reqs = []
    o = []; hero = b['hero']
    hdr = ['SCOPE: build-context', 'KIND: interaction', 'VALID: yes (CALCULATED from game data + ASSUMED shares; no MEASURED input)', f'BUILD: {b["id"]}', f'HERO: {hero}', f'ITEM: {cand}',
           f'CHECKPOINT: {mode} at {at} souls (state souls {S}; item cost {my})', f'VERSION: {IA_VERSION}', f'ARGS: {argv}',
           f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
           f'ALTERNATIVES (equal souls {my}, unconditional, ranked): ' + ', '.join(a for a in eq if a != cand) + ('; also shown, not ranked (conditional or unequal cost): ' + ', '.join(a for a in AR if a not in eq) if len(eq) < len(AR) else ''),
           f'VERDICT: {verdict}' + ('' if any(any(e == 'fr' for e, k, v in item_effects(a)) and not flags[a] for a in eq if a != cand) or any(e == 'fr' for e, k, v in item_effects(cand)) else ' (no permanent equal-soul fire-rate item exists at this checkpoint)'),
           f'UNKNOWN_CELLS: {len(unk)}', f"SELECTION: {R['_sel']['kind']} | {R['_sel']['reason']}", f"ALTERNATIVES CONSIDERED: every unconditional catalog item at the same souls ({my}) with a damage/fire-rate/magazine/proc stat, top 8 by sustained damage" + (f"; plus requested {vs}" if vs else '')] + ([f'CANDIDATE FLAGS: {"; ".join(flags[cand])}'] if flags.get(cand) else []) + [f'PAIRWISE: {x}' for x in pair] + ([f'UPPER-BOUND OPTIONS THAT BEAT IT (their trigger condition decides; UNKNOWN uptime): {", ".join(ub)}'] if ub else [])
    o += hdr
    o.append('PARAMETERS (ASSUMED): ' + ', '.join(f"{k}={v}" for k, v in IA_P.items()) + f"; reload {weapon(R)['reload']} s ({weapon(R)['reload_src']})")
    o.append(f"STATE: owned {wc['owned']} | tiers " + ' '.join(f"{c['name']}={c['tier']}({c['kind']})" for c in C) + f" | weapon invest bonus {stc['wb']:.0f}% | spirit {stc['sp']:.0f}")
    o.append('\n## INTERACTION MATRIX (item effect x kit component)')
    for r in cells:
        o.append(f"- {r['effect']}")
        for comp, status, why, grade in r['cells']: o.append(f"    {comp:<44} {status:<26} [{grade}] {why}")
    o.append(f'\n## DAMAGE DELIVERED (complete build state; total over the window; reading 1 = flat stack bonus multiplied by weapon %, ult does not use ammo, reload as assumed; {len(readings)} readings of the UNKNOWN cells)')
    o.append('item                         | ' + ' | '.join(f"{wi:>22}" for wi in WIN) + f' | heal(sustained)  [range over the {len(readings)} UNKNOWN readings]')
    for m2 in [None] + list(AR):
        res = base if m2 is None else AR[m2]
        cellv = []
        for wi in WIN:
            vs_ = [r[wi]['total'] for r in res]; b0 = [r[wi]['total'] for r in base]
            d = [(v / bb - 1) * 100 if bb else 0 for v, bb in zip(vs_, b0)]
            cellv.append(f"{vs_[0]:>7.0f} ({min(d):+.0f}..{max(d):+.0f}%)" if m2 else f"{vs_[0]:>7.0f}{'':>13}")
        o.append(f"{(m2 or '(without: state before the buy)' if mode == 'buy-point' else (m2 or '(build state, nothing added)'))[:28]:<28} | " + ' | '.join(f"{x:>22}" for x in cellv) + f" | {res[0]['sustained']['heal']:.0f}" + (('  ! ' + '; '.join(flags[m2])) if m2 and flags.get(m2) else ''))
    s0 = resc[0]['sustained']
    o.append(f"  candidate detail (reading 1): sustained bullets {s0['bullets']:.0f}, gun {s0['gun']:.0f}, stacks {s0['fix']:.0f}, procs {s0['procs']:.0f}, spirit {s0['spirit']:.0f}" + (f", time to max stacks {s0['stack_time']:.1f}s" if s0.get('stack_time') else '') +
             (f" | ult: {resc[0]['ult'].get('bullets',0):.0f} bullets in {resc[0]['ult'].get('dur',0):.1f}s, close-range share {resc[0]['ult'].get('share_close',0):.2f}" if resc[0]['ult'].get('bullets') else f" | ult: {resc[0]['ult'].get('note','')}"))
    for wi in WIN:
        if not base[0][wi]['total'] and not resc[0][wi]['total']: o.append(f"  {wi}: not ranked ({resc[0][wi].get('note', 'no damage in this window')})"); continue
        o.append(f"  {wi}: rank (reading 1) " + ' > '.join(rank[(wi, 0)]) + ('' if wi not in unknown_flip else '  <- changes with UNKNOWN readings: ' + ' / '.join(rank[(wi, ri)][0] for ri in range(len(readings)))))
    o.append('  matters in realistic combat: sustained window = every long trade/teamfight; burst = picks and lane all-ins; ult window = once per ultimate cooldown ' +
             (f"({pv(at_tier(R['abil'][4], stc['tA'][4]), 'AbilityCooldown'):g}s)" if stc['tA'][4] >= 0 else '(not trained)'))
    if requests and unk:
        od = SP + '/council/sandbox/autorun/scenarios/interaction'; os.makedirs(od, exist_ok=True)
        seen = set()
        for eff, (comp, status, why, grade) in unk:
            key = re.sub(r'\W+', '_', (comp.split(' [')[0] + '_' + eff.split(' (')[0]))[:50]
            if key in seen: continue
            pref = [v2 for v2 in (vs or []) if v2 in eq] + [m2 for m2 in eq if m2 != cand and any(e == 'fr' for e, k, v in item_effects(m2))] + [m2 for m2 in eq if m2 != cand]
            seen.add(key); reqs.append(write_ia_request(b, R, cand, eff, comp, why, wc, stc, S, od, key, pref, out))
    o.append('\n## TEST REQUESTS (UNKNOWN cells -> sandbox; meta kind INTERACTION, queue via `node council/tools/queue.js add <build> <exp> <file>`)')
    o += ['  ' + r for r in reqs] or ['  none']
    o.append('\n## NOT DETERMINED FROM DATA')
    o += ['  - ' + f"{e}: {c[0]}: {c[2]}" for e, c in unk] or ['  - nothing beyond the ASSUMED shares above']
    o.append('  - hit rate, headshot share, close-range share and ult target spread are ASSUMED (IA_P); item procs without a stated damage value are counted (procs) but not priced')
    o.append('  - windows price DAMAGE only: healing/lifesteal/defence value of an item is shown (heal column, defence rows) but ranked in --strategy, not here; melee cadence ASSUMED (4 light + 1 heavy per 8 s, 50% in range)')
    txt = '\n'.join(o) + '\n'
    sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out if os.path.isabs(out) else SP + '/' + out
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, verdict, reqs

def write_ia_request(b, R, cand, eff, comp, why, w, st, S, od, key, alts, strat_src):
    """plain-English sandbox test request (.txt, lint_meta contract, kind INTERACTION). The procedure depends on the UNKNOWN cell:
    reload -> one probe arm, 20 s of continuous fire (reload gaps in the damage log); passive stacks -> arms A (item) / B (alternative), low-stack then high-stack
    fire blocks at 350u and 900u; ultimate / active ability -> cast it; normal shooting -> fire. Every arm gives the complete build state."""
    hero = b['hero']; cls = item(cand)['class']; safe_c = re.sub(r'\W+', '_', cand)
    slot = int(comp.split('=')[0]) if comp[:1].isdigit() else None
    kind = re.search(r'\[([\w-]+)\]', comp); kind = kind.group(1) if kind else ''
    own = [o for o in w['owned'] if o != cand]; give = [item(o)['class'] for o in own if item(o)]
    alt = alts[0] if alts else None
    tiers = st['tA']; bits = lambda t: 0 if t < 0 else (1, 3, 7, 15)[t]; abil = ' '.join(str(bits(tiers[s])) for s in (1, 2, 3, 4))
    ab = (re.match(r'\d=(.+?) (?:U|L|T\d)\b', comp) or [None, None])[1] or (comp.split('=')[1].split(' ')[0] if '=' in comp else comp)
    reload = eff.startswith('reload time'); melee = comp.startswith('melee'); ally = 'ally' in comp
    sel = R.get('_sel') or dict(kind='requested', reason='not recorded')
    owned_act = [o for o in own if item_targeting(o)['act'] not in ('PASSIVE', '') or (item(o) and REG.get(item(o)['class']) == 'imbue' and sraw(o, 'AmmoReloadPercent'))]
    def fit(*cands, lim=32):   # first complete phrase within the limit (32; player_short 26 per lint_meta); never clip mid-word (none fits -> lint fails)
        cands = [re.sub(r'\s+', ' ', c).strip() for c in cands if c]
        return next((c for c in cands if len(c) <= lim), cands[0])
    if reload:
        q = f"Checking how long {hero}'s reload takes, so magazine and fire-rate items can be compared."; arms = [('P', None)]
        title = fit(f"{hero} reload time?", 'Reload time?'); what = fit('Shoot 20s, time the reloads'); short = fit('Reload timing', lim=26)
    elif melee:
        q = f"Checking whether {cand}'s weapon bonus also raises {hero}'s melee damage."; arms = [('A', cls), ('B0', 'NONE')]; alt = None
        title = fit(f"{cand} boosts melee?", f"Melee gain from {cand}?", 'Does it boost melee?'); what = fit('Melee hits with vs without it'); short = fit(f"{cand} on melee", 'Melee test', lim=26)
    elif ally:
        host = comp.split(' via ')[-1] if ' via ' in comp else 'the ally'
        q = f"Checking whether {cand}'s effect reaches the ally {hero} is attached to through {host}." if 'attached' in comp else f"Checking whether {hero}'s bullets on allies trigger {cand}."
        arms = [('A', cls), ('B0', 'NONE')]; alt = None
        title = fit(f"{cand} reaches the ally?", f"{cand} on an ally?", 'Does it reach the ally?'); what = fit(f"Attached via {host}?" if 'attached' in comp else 'Shooting an ally triggers it?', 'Ally effect test'); short = fit(f"{cand} via {host}", f"{cand} on ally", 'Ally test', lim=26)
    else:
        q = f"Checking whether {cand} boosts {hero}'s {ab}{' (ultimate)' if '(ULT)' in comp else ''}" + (f" more than {alt}." if alt else '.'); arms = [('A', cls), ('B', item(alt)['class'] if alt else None)]
        title = fit(f"{cand} help {ab}?", f"{cand} on {ab}?", f"Does {cand} help?", f"{cand}?")
        what = fit(f"More than {alt}?", f"Beats {alt}?", 'Better than the alternative?') if alt else fit(f"Does {ab} gain from it?", 'Does it change anything?')
        short = fit(f"{cand} on {ab}", f"{cand} test", cand, lim=26)
    f = f"{od}/int_{b['id']}_reload_probe.txt" if reload else f"{od}/int_{b['id']}_{safe_c}_{key}.txt"
    gives_all = give + ([] if reload else [cls] + ([item(alt)['class']] if alt else []))
    if melee or ally: gives_all = give + [cls]
    L = [f"# interaction test request generated by abtimeline.py --interactions ({IA_VERSION}); UNKNOWN cell: {eff} x {comp}: {why}",
         'meta kind INTERACTION', f"meta question {q}", f"meta purpose decide one UNKNOWN interaction cell ({eff.split(' (')[0]} x {ab}) for {b['id']}; the planner records the answer, it does not reason around it",
         f"meta mechanics {why[:220]}", f"meta expectedstate souls={S} items={','.join(gives_all)} tiers={abil}", f"meta build {b['id']}", f"meta checkpoint {S}",
         f"meta items {' '.join(gives_all)}", f"meta strategy_source {strat_src or ''}", f"meta feeds interaction matrix {b['id']} {cand}",
         f"meta selection_kind {sel['kind']}", f"meta selection_reason {sel['reason']}",
         f"meta alternative_reason {('none (single probe)' if reload else (alt + ': ' + ('requested comparison' if alt in (sel.get('vs') or []) else 'first equal-soul unconditional option preferring a permanent fire-rate item, else the best by sustained damage')) if alt else 'none')}",
         f"meta cond_scope {('gun-only reload timing' if reload else 'melee only' if melee else 'ally-target test' if ally else ('ability ' + str(slot) + ' cast + gun' if slot and kind not in ('stacks', 'utility') else 'gun-only, complete build state'))}",
         f"meta cond_abilities_used {('cast ' + str(slot)) if (slot and kind not in ('stacks', 'utility')) else 'none (passives active)'}",
         f"meta cond_abilities_excluded {'all other active abilities' if not reload else 'all'}",
         f"meta cond_accuracy {'any; misses allowed (reload timing only)' if reload else 'all shots on target (aimoff calibrated at 350u)'}",
         f"meta cond_misses {'deliberate allowed' if reload else 'none'}",
         f"meta cond_start_stacks {'0 (verify before each block)' if kind == 'stacks' else 'n/a'}",
         f"meta cond_activations {','.join(owned_act + ([cand] if item_targeting(cand)['act'] not in ('PASSIVE', '') or (ally and 'ally hits' in comp) else [])) or 'none'}",
         f"meta cond_distance {'350u and 900u: read back the measured metres and whether the range condition is active' if not reload else '350u'}",
         f"meta cond_targets enemies=1 allies={1 if ally else 0}",
         f"meta readbacks " + ','.join(x for x in ['equipped_items', 'ability_tiers', 'distance_m', ('stacks_per_block' if kind == 'stacks' else ''), ('reload_gaps_s' if reload else ''), ('magazine_size' if reload or 'clip' in eff else ''),
                                                    ('activation:' + a for a in owned_act) and ','.join('activation:' + a for a in owned_act), ('ally_effect_applied' if ally else ''), ('activation:' + cand if ally and 'ally hits' in comp else ''), ('ability_cast:' + str(slot) if slot and kind not in ('stacks', 'utility') else '')] if x),
         f"meta player_title {title}", f"meta player_what {what}", f"meta player_why {fit('Game text unclear; testing it')}", f"meta player_short {short}", f"meta player_expect {fit('Gap between magazines (s)' if reload else 'Ally gets it: yes or no' if ally else 'Melee damage per hit' if melee else 'More damage: A or B?')}",
         (f"meta result_says WORKS if {cand} activates (readback activation:{cand}) while only the ALLY is being hit (enemy out of line of fire); DOES NOT WORK if it activates only on enemy hits; then compare heal and enemy damage per 20 s with/without the buff" if ally and 'ally hits' in comp else
          f"meta result_says WORKS if the ally shows the item's effect (barrier/heal/buff readback ally_effect_applied) only in arm A; DOES NOT WORK if only {hero}/self gets it; CONDITIONAL if it depends on the hop/attach state" if ally else
          "meta result_says WORKS if melee damage per hit in arm A exceeds arm B (no item) by about the item's weapon %; DOES NOT WORK if equal within noise" if melee else
          "meta result_says reload seconds = gap between the last bullet of a magazine and the first of the next (MEASURED); replaces the ASSUMED 2.5 s" if reload else
          f"meta result_says WORKS if arm A's damage per bullet rises with stacks by the item's % (reading 1) / DOES NOT WORK if only the flat stack part rises (reading 2); A vs B damage per window" if kind == 'stacks' else
          f"meta result_says WORKS if arm A deals more {ab} damage than B by the item's effect; DOES NOT WORK if equal (within noise)"),
         f"setup {R['b']['hk'].replace('hero_', '').capitalize()} Haze", 'raw citadel_unlock_flex_slots', f"abil {abil}", f"souls {S}"]
    if ally: L.insert(6, 'meta blocked_by ally bot op missing in the runner (GAPS 10); recorded in PLANNER_GAP')
    acts_pl = item_acts(R, w['owned'], w.get('imbues', {})) + ([f"cast{slot}|ability|{ability_frag(R, slot)}|1"] if slot and kind not in ('stacks', 'utility') else [])
    rbs = (['reload_measured|reload_s|>|0'] if reload else []) + (['clip_known|clipmax|>|0'] if 'clip' in eff or reload else [])
    Lm, rot_op = plugin_meta(R, st, w['owned'], w.get('imbues', {}), purpose='interaction cell test', acts=acts_pl, readbacks=rbs, stack_frag=(ability_frag(R, slot) if kind == 'stacks' and slot else None),
                             rng=((f"{num(str(sraw(cand, 'CloseRangeBonusDamageRange') or '15')) * M_TO_U:.0f}", 'mixed') if sraw(cand, 'CloseRangeBonusWeaponPower') else None))
    L += Lm
    def block(arm, it, dist):
        B2 = ['hardreset', f"souls {S}"] + [f"give {g}" for g in give] + ([f"give {it}"] if it and it != 'NONE' else []) + ['basemods', 'enemies 1 300 4', f"fetch {dist}", 'cast reload 2.5']
        tag = f"{arm}_{dist}"
        if reload: B2 += [f"mark {tag}_reload", 'fire 4', 'rl none 4', 'rb clipmax clipmax']
        elif melee: B2 += [f"mark {tag}_melee", 'cast melee', 'wait 1', 'cast melee', 'wait 1', 'cast melee']
        elif ally: B2 += [f"mark {tag}_ally", '# needs an allied bot (GAPS 10: no ally op yet) - blocked until the runner supports allies', 'fire 5']
        elif kind == 'stacks': B2 += [f"mark {tag}_lowstacks", 'fire 2', f"mark {tag}_highstacks", 'fire 8']
        elif slot and kind != 'utility': B2 += [f"mark {tag}_cast{slot}", f"cast {slot} {7 if slot == 4 else 0.5}"] + (['fire 6'] if slot != 4 else [])   # cast then shoot (abilities that empower or are triggered by bullets)
        else: B2 += [f"mark {tag}_fire10", 'fire 10']
        return B2 + ['mark none', 'wait 3']
    for arm, it in arms:
        if arm != 'P' and not it: continue
        for dist in ((350,) if reload else (150,) if melee else (350, 900)): L += block(arm, it, dist)
    if not reload and alt:   # counterbalance: B then A again
        for arm, it in arms[::-1]:
            if it: L += block(arm + '2', it, 350)
    L.append('end')
    open(f, 'w').write('\n'.join(L) + '\n')
    return f
def interactions_main(a, B):
    bid, cand = a[1], a[2]; at = None; vs = []; out = None; req = True; i = 3
    while i < len(a):
        if a[i] == '--at': at = int(a[i + 1]); i += 2
        elif a[i] == '--vs': vs.append(a[i + 1]); i += 2
        elif a[i] == '--out': out = a[i + 1]; i += 2
        elif a[i] == '--no-requests': req = False; i += 1
        else: i += 1
    b = next(x for x in B if x['id'] == bid)
    argv = ' '.join(x for x in a if x not in ('--out', out))
    f, v, reqs = interactions(b, cand, at, vs, out, req, argv); print('wrote', f); print('VERDICT:', v); print('TEST REQUESTS:', len(reqs))

# ======================================================================================================
# WEAKNESS -> ROOT CAUSE -> REMEDY SET -> COMPLETE-BUILD SCORE (Kieran 15:19/15:20; WEAKNESS_PROCESS B/C)
# usage: python3 -I abtimeline.py --weakness <build id> <ammo|reach|auto> [--at souls] [--out f]
# Remedy classes are generated from data predicates over the full catalog and the kit's ability upgrades (not a fixed item list). The plain direct
# remedy of the class (e.g. magazine items for ammo, move-speed items for reach) is ALWAYS generated; 'do nothing' is always scored.
# Neutral scoring, same for every candidate: change in trade ratio (time-to-die / time-to-kill, --strategy trade model, central parameters) per 1000 souls
# in the complete build state at the checkpoint, plus damage in a realistic 8 s window and a 20 s uninterrupted window. No bonus for novelty or category match.
WK_VERSION = 'weakness-v1'
def wk_eval(R, base_w, souls, add=(), remove=(), P_over=None):
    w = dict(base_w, owned=[o for o in base_w['owned'] if o not in remove]); w, st = ia_state(R, w, souls, list(add))
    m = seg_metrics(R, w, st); P = {k: v[0] for k, v in STRAT_P.items()}; P.update(P_over or {})
    e = enemy_at(souls / P['E_SPM'], P, HB_of()); tr_ = trade(m, P, e)
    g8 = gun_model(R, st, w['owned'], dict(st['tA']), cdr_pct([dict(n=x) for x in w['owned']]), 8, 0.5); g20 = gun_model(R, st, w['owned'], dict(st['tA']), cdr_pct([dict(n=x) for x in w['owned']]), 20, 0.5)
    return dict(tr=tr_['tr'], dps=tr_['dps'], ttd=tr_['ttd'], d8=g8['dmg'], d20=g20['dmg'], b8=g8['bullets'], b20=g20['bullets'], cyc=g8['cyc'], clip=g8['clip'], m=m, w=w, st=st)
def wk_cost(base_w, n):
    it = item(n); return SOULS[it['tier']] - sum(SOULS[item(c)['tier']] for c in it['components'] if c in base_w['owned'])
def wk_catalog(base_w, pred, maxtier=4):
    out = []
    for n, g in items().items():
        if g.get('disabled') or n in base_w['owned'] or not item(n) or g['tier'] > maxtier: continue
        if any(n in item(o)['components'] for o in base_w['owned']): continue
        s = (g69().get(n) or {}).get('stats', {})
        if pred(n, s): out.append(n)
    return out
def weakness(b, wclass, at=None, out=None, argv=''):
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); rows = [r for r in R['rows'] if not r.get('unknown')]
    at = at or 9600; prev = [r for r in rows if r['souls'] <= at]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': 0, 'owned': [], 'imbues': {}, 'box': ''}
    R['melee_rel'] = melee_relevant(R, base_w['owned']); R['mob'] = mobility_slots(R)
    P0 = {k: v[0] for k, v in STRAT_P.items()}; base = wk_eval(R, base_w, at)
    wp = weapon(R); C = kit_components(R, base['st']['tA'])
    if wclass == 'auto':
        mag_s = base['clip'] * base['cyc']; loss20 = 1 - base['b20'] / max(1e-9, 20 / base['cyc']); loss8 = 1 - base['b8'] / max(1e-9, 8 / base['cyc'])
        wclass = 'ammo' if loss20 > 0.2 else ('reach' if R['melee_rel'] else 'ammo')
    o = []; remedies = []   # (class, name, add, remove, cost, note, grade)
    if wclass == 'ammo':
        mag_s = base['clip'] * base['cyc']; ideal8 = 8 / base['cyc']; ideal20 = 20 / base['cyc']
        loss8 = 1 - base['b8'] / ideal8; loss20 = 1 - base['b20'] / ideal20
        root = (f"magazine {base['clip']:.0f} bullets empties in {mag_s:.1f} s at {1/base['cyc']:.1f} bullets/s (fire-rate pool {sum(sval(x,'BonusFireRate')+sval(x,'FireRateBonus') for x in base_w['owned']):.0f}% from {[x for x in base_w['owned'] if sval(x,'BonusFireRate') or sval(x,'FireRateBonus')]}); "
                f"reload {wp['reload']} s ({wp['reload_src']}). Time not firing: {loss8*100:.0f}% of an 8 s trade, {loss20*100:.0f}% of 20 s uninterrupted fire")
        nofix = loss8 < 0.10
        o.append(f"NO-FIX CHECK (CALCULATED, reload ASSUMED unless measured): realistic 8 s trade loses {loss8*100:.0f}% of firing time to reloads vs {loss20*100:.0f}% in a 20 s uninterrupted test -> " +
                 ("NO FIX NEEDED in realistic trades (the weakness appears mainly in long uninterrupted shooting)" if nofix else "the weakness is present in realistic trades"))
        # data predicates per remedy class
        cap = wk_catalog(base_w, lambda n, s: ('BonusClipSizePercent' in s or 'BonusClipSize' in s) and not item_targeting(n)['act'] in ('PRESS',))
        auto = wk_catalog(base_w, lambda n, s: 'AmmoReloadPercent' in s or 'ActiveReloadPercent' in s)
        clipstat = [(c['name'], k) for c in C if c['kind'] != 'locked' for k, p in c['P'].items() if re.search('Clip|Ammo', k) and p.get('stype') in ('ETechPower', 'EWeaponPower')]
        wb = block('abilities.vdata', R['H']['wpn']) or ''; wstat = re.findall(r'(m_\w*(?:Clip|Ammo)\w*) = ([^\n]+)', wb)[:4]
        for n in cap: remedies.append(('capacity (direct)', n, [n], [], wk_cost(base_w, n), 'more bullets per magazine', 'CALCULATED'))
        for n in auto:
            tg = item_targeting(n); imb = REG.get(item(n)['class']) == 'imbue'
            legal = [c for c in C if c['kind'] != 'locked' and (pv(c['P'], 'AbilityCooldown') or 0) > 0 and not (('NON_ULT' in tg['imbue']) and c.get('ult'))]
            best = min(legal, key=lambda c: pv(c['P'], 'AbilityCooldown') or 999) if (imb and legal) else None
            trig = (f"imbue on {best['name']} (cd {pv(best['P'],'AbilityCooldown'):g}s): refills on that cast, at most every {sval(n,'AbilityChargeUpTime') or sval(n,'AbilityCooldown'):g}s" if best else
                    f"active item ({tg['act']}): refills {sval(n,'ActiveReloadPercent') or sval(n,'AmmoReloadPercent'):g}% of the magazine when activated, cooldown {sval(n,'AbilityCooldown'):g}s; activation must be verified" if 'ActiveReloadPercent' in ((g69().get(n) or {}).get('stats', {})) else f"activation {tg['act']}: see item text (trigger not encoded)")
            remedies.append(('auto-reload / reload-through-ability', n, [n], [], wk_cost(base_w, n), trig, 'CALCULATED (trigger) + ASSUMED (use rate 0.5)'))
        if clipstat: remedies.append(('ammo-scaling stat', 'spirit/weapon power', [], [], 0, f"kit properties scale ammo: {clipstat}", 'CALCULATED'))
        o.append('AMMO-SCALING CHECK (CALCULATED): ' + (f"ammo properties scaled by a stat: {clipstat}" if clipstat else f"no ability or weapon property scales magazine size with spirit or other power (weapon ammo fields: {wstat or 'clip only'}): spirit items cannot fix ammo; imbued/charged-only spirit (ImbuedTechPower, BonusSpiritForChargedAbilities) is per-ability anyway"))
        # trade fire rate for per-bullet damage: replace each owned fire-rate item with the best equal-cost weapon-% item
        for fr_it in [x for x in base_w['owned'] if (sval(x, 'BonusFireRate') or sval(x, 'FireRateBonus')) and item(x)['slot'] == 'WeaponMod']:
            c0 = SOULS[item(fr_it)['tier']]
            subs = [n for n in wk_catalog(dict(base_w, owned=[o2 for o2 in base_w['owned'] if o2 != fr_it]), lambda n, s: 'BaseAttackDamagePercent' in s and 'BonusFireRate' not in s and 'LifeThreshold' not in s and 'BulletLifestealPercent' not in s and item(n)['slot'] == 'WeaponMod') if SOULS[item(n)['tier']] == c0]
            if subs:
                best = max(subs, key=lambda n: wk_eval(R, base_w, at, [n], [fr_it])['tr'])
                remedies.append(('trade fire rate for per-bullet damage', f"{best} instead of {fr_it}", [best], [fr_it] + [c for c in item(fr_it)['components']], 0, 'same souls; fewer bullets: fewer procs/stacks/lifesteal hits, more damage per bullet', 'CALCULATED'))
    elif wclass == 'reach':
        speed = R['HS']['move'] + sum(sval(x, 'BonusMoveSpeed') for x in base_w['owned']); mob = [(c['name'], pv(c['P'], 'AbilityCooldown')) for c in C if c['slot'] in R['mob'] and c['kind'] != 'locked']
        ENEMY_SPEED, GAP = 7.2, 8.0
        root = (f"melee-relevant kit; move speed {speed:.1f} m/s vs a kiting enemy at {ENEMY_SPEED} m/s (ASSUMED hero_base speed) -> walking never closes an {GAP:g} m gap (ASSUMED); gap-closers at this checkpoint: {mob or 'none'}")
        u0 = P0['melee_u']; cover = min(1.0, (P0['W'] + P0['I']) / mob[0][1]) if mob and mob[0][1] else 0.0
        nofix = cover >= 0.9
        o.append(f"NO-FIX CHECK (CALCULATED cooldown, ASSUMED trade cadence): gap-closer available in {cover*100:.0f}% of trades (cd {mob[0][1] if mob else '-'} s vs {P0['W']+P0['I']:.0f} s cycle) -> " + ("NO FIX NEEDED: the kit closes the gap in almost every trade" if nofix else "some trades start out of reach"))
        mv = wk_catalog(base_w, lambda n, s: 'BonusMoveSpeed' in s and (num(s['BonusMoveSpeed']) or 0) > 0, 3)
        sl = wk_catalog(base_w, lambda n, s: any(k in s for k in ('SlowPercent', 'MovementSpeedSlow')) and 'BonusMoveSpeed' not in s, 3)
        for n in mv:
            s_ = (g69().get(n) or {}).get('stats', {}); timed = bool(item_targeting(n)['act'] != 'PASSIVE' or 'AbilityDuration' in s_ or 'BuffDuration' in s_ or 'MovementSpeedBonusDuration' in s_ or REG.get(item(n)['class'], '').split('+')[0] in ('proc', 'stack', 'selfhp', 'heal', 'taken'))
            remedies.append(('move speed (direct)' if not timed else 'move speed (timed/active buff)', n, [n], [], wk_cost(base_w, n), f"+{sval(n,'BonusMoveSpeed'):g} m/s" + (' while the buff runs (uptime = duration/cooldown)' if timed else ' permanent'), 'CALCULATED + ASSUMED reach model'))
        for n in sl: remedies.append(('slow the target', n, [n], [], wk_cost(base_w, n), f"slow {sval(n,'SlowPercent') or sval(n,'MovementSpeedSlow'):g}%", 'CALCULATED + ASSUMED reach model'))
        rem_w = [n for n in wk_catalog(base_w, lambda n, s: 'BaseAttackDamagePercent' in s and 'LongRangeBonusWeaponPower' not in s and 'LifeThreshold' not in s, 2)]
        if rem_w: remedies.append(('fight without closing (gun)', max(rem_w, key=lambda n: wk_eval(R, base_w, at, [n])['tr']), [], [], 0, 'best weapon-% item at T1/T2', 'CALCULATED'))
        if remedies and remedies[-1][0].startswith('fight'): n = remedies[-1][1]; remedies[-1] = (remedies[-1][0], n, [n], [], wk_cost(base_w, n), remedies[-1][5], remedies[-1][6])
    else:
        root = f"weakness class '{wclass}' has no root-cause model yet (ammo, reach implemented)"; nofix = False
    # ability-upgrade remedies: tiers in the kit whose upgrade adds charges / sustain / mobility / cleanse / ammo (verified at this checkpoint)
    for c in C:
        a = R['abil'][c['slot']]
        for tt, ups in enumerate(a['ups'], 1):
            keys = [pn for pn, _, _ in ups]
            hit = [k for k in keys if re.search(r'Charges|Lifesteal|Dispel|UnlimitedAmmo|Clip|Ammo|BonusMoveSpeed|CombatBarrier|Heal', k)]
            if hit and (c['kind'] == 'locked' or c['t'] < tt):
                remedies.append(('ability upgrade', f"{c['name']} T{tt} ({','.join(hit)})", [], [], 0, f"needs ability points: tier T{tt}; current {c['tier']} at {at} souls (reorder points, no souls)", 'CALCULATED (tier data)'))
    if not any(r[0] == 'ability upgrade' for r in remedies): o.append('ABILITY-UPGRADE CHECK (CALCULATED): no untaken ability tier in this kit adds charges, sustain, mobility, cleanse or ammo at this checkpoint')
    for n in candidate_greens(dict(R, HB=HB_of()), core_path(b), at, 'def')[:2]: remedies.append(('survive and keep fighting', n[1], [n[1]], [], n[2], 'best defensive green by time-to-die per 800 souls', 'CALCULATED'))
    remedies.append(('do nothing / behaviour', 'no purchase', [], [], 0, 'reload during ability casts and repositioning; no souls spent', 'CALCULATED'))
    # neutral scoring
    def u_for(add):
        if wclass != 'reach': return None
        def upt(x):   # passive untimed stat = 1; timed/active buff = duration/cooldown (data); ally-targeted actives count only on self-cast
            s = (g69().get(x) or {}).get('stats', {}); du = sval(x, 'AbilityDuration') or sval(x, 'BuffDuration'); cd = sval(x, 'AbilityCooldown')
            cond = 'MovementSpeedBonusDuration' in s or REG.get(item(x)['class'], '').split('+')[0] in ('proc', 'stack', 'selfhp', 'heal', 'taken')
            return 1.0 if (item_targeting(x)['act'] == 'PASSIVE' and not du and not cond) else (min(1.0, du / cd) if du and cd else 0.5)
        sp = sum(sval(x, 'BonusMoveSpeed') * upt(x) for x in add); slw = max([sval(x, 'SlowPercent') or sval(x, 'MovementSpeedSlow') for x in add] or [0])
        return min(0.9, P0['melee_u'] * (1 + 0.5 * sp + slw / 100))   # ASSUMED reach model: +0.5x uptime per m/s, +slow% share
    scored = []
    for cls, name, add, remove, cost, note, grade in remedies:
        if cls == 'ability upgrade' or cls == 'ammo-scaling stat':
            scored.append((cls, name, cost, None, None, None, note, grade)); continue
        u = u_for(add); ev = wk_eval(R, base_w, at, add, remove, {'melee_u': u} if u is not None else None)
        dtr = (ev['tr'] / base['tr'] - 1) * 100; per = dtr / max(cost, 1) * 1000 if cost else dtr
        scored.append((cls, name, cost, dtr, per, (ev['d8'] / max(1e-9, base['d8']) - 1) * 100, note + (f"; reload loss 8s {1-ev['b8']/(8/ev['cyc']):.0%}" if wclass == 'ammo' else '') + (f"; melee uptime {u:.2f}" if u is not None else ''), grade))
    simple_cls = {'ammo': 'capacity (direct)', 'reach': 'move speed (direct)'}.get(wclass)
    simple = [s for s in scored if s[0] == simple_cls and s[4] is not None]
    priced = [s for s in scored if s[4] is not None and s[0] != 'do nothing / behaviour']
    win = max(priced, key=lambda s: s[4]) if priced else None; sbest = max(simple, key=lambda s: s[4]) if simple else None
    if nofix: concl = 'NO FIX NEEDED: ' + ('the weakness mainly shows in an artificial long test' if wclass == 'ammo' else 'the kit already covers it in realistic trades')
    elif not win or win[4] < 1.0: concl = 'INSUFFICIENT EVIDENCE: no remedy changes the trade ratio by >=1% per 1000 souls (within model noise)'
    elif sbest and win is sbest: concl = f"SIMPLE REMEDY WINS: {win[1]} ({win[4]:+.1f}% trade ratio per 1000 souls)"
    else: concl = f"{win[1]} [{win[0]}] beats the best simple remedy {sbest[1] if sbest else '(none generated!)'} ({win[4]:+.1f}% vs {sbest[4] if sbest else float('nan'):+.1f}% trade ratio per 1000 souls)"
    hdr = ['SCOPE: build-context', 'KIND: weakness', f'BUILD: {b["id"]}', f'HERO: {b["hero"]}', f'WEAKNESS: {wclass}', f'CHECKPOINT: {at}', f'VERSION: {WK_VERSION}', f'ARGS: {argv}',
           f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}', f'ROOT-CAUSE: {root}',
           f"NO-FIX: {'yes' if nofix else 'no'}", 'REMEDY-SET: ' + '; '.join(sorted({s[0] for s in scored})),
           f"SIMPLE-REMEDY: {(sbest[1] + f' {sbest[4]:+.1f}%/1000 souls') if sbest else 'MISSING (generator flag)'}", f'CONCLUSION: {concl}',
           'SCORING: same for every candidate: change in trade ratio per 1000 souls (complete build, central --strategy parameters), plus damage in 8 s; no bonus for novelty or category match',
           'GRADE: CALCULATED from game data + ASSUMED (trade model, reload unless measured, reach model); test requests below for what the data cannot answer']
    o = hdr + [''] + o
    o.append(f"\n## REMEDIES (base trade ratio {base['tr']:.2f}, base 8 s damage {base['d8']:.0f}, owned {base_w['owned']})")
    o.append('class                                  | candidate                                   | souls | dTR%  | dTR%/1000 souls | d8s dmg% | notes [grade]')
    for cls, name, cost, dtr, per, d8, note, grade in sorted(scored, key=lambda s: -(s[4] if s[4] is not None else -1e9)):
        o.append(f"{cls[:38]:<38} | {name[:43]:<43} | {cost:>5} | {'' if dtr is None else f'{dtr:+5.1f}':>5} | {'' if per is None else f'{per:+6.1f}':>15} | {'' if d8 is None else f'{d8:+6.1f}':>8} | {note} [{grade}]")
    o.append('\n## UNKNOWN / NEEDS TESTS')
    o.append('  - reload duration: ' + ('MEASURED' if not wp['reload_src'].startswith('ASSUMED') else 'ASSUMED (queued reload probe, readback reload_gaps_s)'))
    o.append('  - auto-reload use rate (0.5 of charges) and whether the imbued ability is cast in the firing window: readback activation:<item>, ability_cast:<slot>')
    if wclass == 'reach': o.append('  - reach model (uptime vs move speed/slow) is ASSUMED: needs a chase scenario (GAPS 24: emove/flee bot) with readback distance_m over time')
    o.append('  - ability-upgrade remedies need points at the tier: verify ability_tiers readback at the checkpoint before trusting them')
    o.append('  - score per 1000 souls favours cheap items when gains are not linear in souls; absolute dTR is shown too (an equal-souls bundle comparison is the next step: --strategy alternatives)')
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/weakness/{b['id']}_{wclass}_{at}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True)
    # test request: best remedy vs best simple remedy vs no purchase, same complete state; readbacks declared so the runner can verify the mechanics fired
    rq = None
    if win and not nofix:
        od = SP + '/council/sandbox/autorun/scenarios/interaction'; os.makedirs(od, exist_ok=True)
        arms = [('R', win[1])] + ([('S', sbest[1])] if sbest and sbest is not win else []) + [('N', None)]
        give = [item(x)['class'] for x in base_w['owned'] if item(x)]; tiers = base['st']['tA']; bits = lambda t2: 0 if t2 < 0 else (1, 3, 7, 15)[t2]
        imb_slot = next((c['slot'] for c in C if c['kind'] != 'locked' and (pv(c['P'], 'AbilityCooldown') or 0) > 0 and not c.get('ult')), None)
        acts = [a2 for _, a2 in arms if a2 and item(a2) and (item_targeting(a2)['act'] not in ('PASSIVE', '') or sraw(a2, 'AmmoReloadPercent'))]
        def fit(*cs, lim=32): cs = [c for c in cs if c]; return next((c for c in cs if len(c) <= lim), cs[0])
        nm_ = {'ammo': 'running out of ammo', 'reach': 'reaching enemies'}.get(wclass, wclass)
        L = [f"# weakness remedy test generated by abtimeline.py --weakness ({WK_VERSION}); root cause: {root[:200]}", 'meta kind INTERACTION',
             f"meta question Checking whether {win[1]} fixes {b['hero']}'s {nm_} better than {sbest[1] if sbest and sbest is not win else 'buying nothing'}.",
             f"meta purpose score the remedy set for {wclass} on {b['id']} with measured numbers (planner records the result)", f"meta mechanics {win[6][:200]}",
             f"meta expectedstate souls={at} items={','.join(give)} tiers={' '.join(str(bits(tiers[s])) for s in (1,2,3,4))}", f"meta build {b['id']}", f"meta checkpoint {at}",
             f"meta items {' '.join(give + [item(a2)['class'] for _, a2 in arms if a2])}", f"meta strategy_source {os.path.relpath(out, SP)}", f"meta feeds weakness remedy set {b['id']} {wclass}",
             'meta selection_kind weakness-remedy', f"meta selection_reason {wclass} weakness at {at} souls: {root[:150]}; arms are the best-scored remedy, the best plain direct remedy and no purchase",
             f"meta alternative_reason simple direct remedy is always tested (neutrality rule); 'no purchase' is the do-nothing arm",
             f"meta cond_scope {'gun + the reload-trigger ability cast' if wclass == 'ammo' else 'melee trade at closing distance'}", f"meta cond_abilities_used {('cast ' + str(imb_slot)) if imb_slot and wclass == 'ammo' else 'gap-closer if trained'}",
             'meta cond_abilities_excluded ultimate', 'meta cond_accuracy all shots on target', 'meta cond_misses none', 'meta cond_start_stacks 0 (verify)',
             f"meta cond_activations {','.join(acts) or 'none'}", f"meta cond_distance {'350u' if wclass == 'ammo' else 'start 900u, close to 150u'}", 'meta cond_targets enemies=1 allies=0',
             'meta readbacks ' + ','.join(['equipped_items', 'ability_tiers', 'distance_m'] + (['magazine_size', 'reload_gaps_s'] if wclass == 'ammo' else ['time_to_reach_s']) + [f'activation:{a2}' for a2 in acts] + ([f'ability_cast:{imb_slot}'] if imb_slot and wclass == 'ammo' else [])),
             f"meta player_title {fit(f'Fix for {nm_}?', 'Which fix works?')}", f"meta player_what {fit(f'{win[1]} vs {sbest[1]}' if sbest and sbest is not win else f'{win[1]} vs nothing', 'Remedy vs simple fix')}",
             f"meta player_why {fit('Pick the fix by measurement')}", f"meta player_short {fit(f'{wclass} remedies', 'Remedy test', lim=26)}", f"meta player_expect {fit('Firing time and damage, 8s' if wclass == 'ammo' else 'Time to reach, damage')}",
             f"meta result_says the arm with most damage in 8 s (and least reload time) wins; if 'no purchase' is within noise the weakness needs no fix",
             f"setup {b['hk'].replace('hero_', '').capitalize()} Haze", 'raw citadel_unlock_flex_slots', f"abil {' '.join(str(bits(tiers[s])) for s in (1,2,3,4))}", f"souls {at}"]
        for tag, a2 in arms * 2:
            L += ['hardreset', f"souls {at}"] + [f"give {g}" for g in give] + ([f"give {item(a2)['class']}"] if a2 else []) + ['basemods', 'enemies 1 300 4', f"fetch {350 if wclass == 'ammo' else 900}", 'cast reload 2.5', f"mark {tag}_{wclass}"]
            L += ([f"cast {imb_slot} 0.5"] if imb_slot and wclass == 'ammo' else []) + (['fire 8'] if wclass == 'ammo' else ['cast 2 1', 'cast melee', 'cast melee', 'cast melee']) + ['mark none', 'wait 3']
        L.append('end'); rq = f"{od}/int_{b['id']}_weakness_{wclass}.txt"; open(rq, 'w').write('\n'.join(L) + '\n')
        txt = txt.replace('## UNKNOWN / NEEDS TESTS', f'## UNKNOWN / NEEDS TESTS\n  - queued request: {os.path.relpath(rq, SP)}')
        sha = body_sha(txt); txt = re.sub(r'^BODY-SHA: \w+', f'BODY-SHA: {sha}', txt, flags=re.M)
    open(out, 'w').write(txt)
    return out, concl, (sbest is not None)
def weakness_main(a, B):
    bid, wc = a[1], a[2]; at = int(a[a.index('--at') + 1]) if '--at' in a else None; out = a[a.index('--out') + 1] if '--out' in a else None
    b = next(x for x in B if x['id'] == bid); f, c, ok = weakness(b, wc, at, out, ' '.join(x for x in a if x not in ('--out', out)))
    print('wrote', f); print('CONCLUSION:', c); print('SIMPLE REMEDY GENERATED:', 'yes' if ok else 'NO (flag)')

# ======================================================================================================
# GENERIC EXPERIMENT DISCOVERY (Kieran 15:16 A/B): which interaction experiments are worth running for THIS kit, chosen BEFORE any run, with the reason recorded.
# usage: python3 -I abtimeline.py --discover <build id> [--at souls] [--n 3] [--queue]
# For every affordable unowned catalog item the matrix is built; UNKNOWN cells are weighted by the value of the kit component they touch (that component's share of
# the hero's damage or healing at the checkpoint; ally-attach / ally-weapon components = the hero's support role, valued at the top component, ASSUMED).
# The top N items become interaction files + test requests with selection_kind discovery and the reason text; nothing is chosen after a result.
def comp_values(R, st):
    C = kit_components(R, st['tA']); v = {}
    g = gun_model(R, st, list(st['owned']), dict(st['tA']), 0, 10, 0.5); v['normal shooting'] = g['dmg'] * IA_P['hit']
    v['melee (light/heavy)'] = 4 * (R['HS']['light'] + R['HS']['melee_lvl'] * st['boons']) * (1 if melee_relevant(R, st['owned']) else 0.2)
    for c in C:
        if c['kind'] == 'locked': continue
        s2 = slot_sp(R, st, c['slot'], c['t']); d = sum(x for k, (x, inst) in spirit_hits(c['P'], s2).items() if inst) + c.get('heal', 0)
        key = f"{c['slot']}={c['name']}"; v[key] = d * (1 + int(10 / max(pv(c['P'], 'AbilityCooldown') or 30, 1)))
    top = max(v.values() or [1])
    for c in C:
        if c.get('attach'): v[f"attached ally via {c['name']}"] = top
        if c.get('allyweapon'): v[f"ally hits via {c['name']}"] = top
    tot = sum(v.values()) or 1
    return {k: x / tot for k, x in v.items()}, C
def discover(b, at=None, n=3, queue=False, argv=''):
    R = analyse(b); R['HS'] = hero_stats(b['hk']); rows = [r for r in R['rows'] if not r.get('unknown')]
    at = at or 9600; prev = [r for r in rows if r['souls'] <= at]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': 0, 'owned': [], 'imbues': {}, 'box': ''}
    w, st = ia_state(R, base_w, at, None); share, C = comp_values(R, st); picks = []
    for cand, g in items().items():
        if g.get('disabled') or cand in base_w['owned'] or not item(cand) or g['tier'] > 3 or any(cand in item(o)['components'] for o in base_w['owned']): continue
        if not item_effects(cand): continue
        w2, st2 = ia_state(R, base_w, at, cand)
        cells = ia_matrix(R, kit_components(R, st2['tA']), cand, dict(own_names=w2['owned'], pool_dmg=st2['wb'], pool_fr=0))
        unk = [(r['effect'], c) for r in cells for c in r['cells'] if c[1] == 'UNKNOWN' and not c[0].startswith('normal shooting')]
        best = None
        for eff, c in unk:
            key = next((k for k in share if c[0].startswith(k)), None)
            if key is None: continue
            sc = share[key]
            if not best or sc > best[0]: best = (sc, eff, c, key)
        if best: picks.append((best[0], cand, best))
    picks.sort(key=lambda x: (-x[0], SOULS[item(x[1])['tier']]))
    seen_comp = {}; chosen = []
    for sc, cand, (s0, eff, c, key) in picks:   # at most 2 per component so different questions get asked
        if seen_comp.get(key, 0) >= 1: continue
        seen_comp[key] = seen_comp.get(key, 0) + 1; chosen.append((sc, cand, eff, c, key))
        if len(chosen) >= n: break
    out = []
    for sc, cand, eff, c, key in chosen:
        reason = (f"discovery: {cand}'s {eff.split(' (')[0]} has an UNKNOWN interaction with {key} ({c[2][:110]}); {key} is {sc*100:.0f}% of {b['hero']}'s output at {at} souls "
                  f"(component share, CALCULATED; support components ASSUMED top), so the answer can change a purchase")
        f, v, reqs = interactions(b, cand, at, [], None, True, argv + f' (discover {cand})', dict(kind='discovery', reason=reason))
        if queue:
            for rq in reqs:
                exp = 'interaction:' + os.path.basename(rq)[4:-4][len(b['id']) + 1:]
                subprocess.run(['node', SP + '/council/tools/queue.js', 'add', b['id'], exp, os.path.relpath(rq, SP)], cwd=SP, capture_output=True, text=True)
        out.append((cand, key, sc, v, f, reqs))
    return out, share
def discover_main(a, B):
    bid = a[1]; at = int(a[a.index('--at') + 1]) if '--at' in a else None; n = int(a[a.index('--n') + 1]) if '--n' in a else 3
    b = next(x for x in B if x['id'] == bid); res, share = discover(b, at, n, '--queue' in a, ' '.join(a))
    print('component shares (CALCULATED/ASSUMED):', ', '.join(f"{k} {v*100:.0f}%" for k, v in sorted(share.items(), key=lambda x: -x[1])))
    for cand, key, sc, v, f, reqs in res: print(f"PICK {cand} -> {key} ({sc*100:.0f}%): {v} | {f} | requests {len(reqs)}")

# ======================================================================================================
# 15:33 / 15:35 / 15:39 additions: plugin meta helper (levels, rotation, activations, readbacks), conditional items, investment-threshold-aware
# selling, situational swaps by enemy composition. All generic from data; every assumption is labelled.
# ---------------- plugin meta helper (field names deployed by the plugin agent, 15:3x) ----------------
def plugin_levels(R, T):
    """required_levels in the plugin convention (upgrade bits incl. unlock: U=1, T1=2, T2=3, T3=4; locked=0) from the build's real progression."""
    return ';'.join(f"{s}={T[s] + 1 if T[s] >= 0 else 0}" for s in (1, 2, 3, 4))
def ability_frag(R, sl):
    return re.sub(r'^(citadel_)?ability_', '', R['H']['ab'][sl])
def rotation(R, T, owned, imbues, window=8.0, purpose='complete-build'):
    """generic rotation from the kit at its real tiers: openers (CC/debuff) first, self-buffs before firing, damage abilities on cooldown, the ability an
    owned reload item is imbued on when the magazine empties, the ultimate once if it adds damage; escapes/utility excluded and declared. Returns (spec text, rot op)."""
    C = kit_components(R, T); ev = []; spec = []; excl = []
    wp = weapon(R); mag_s = wp['clip'] * wp['cyc']
    reload_imb = {sl for n, sl in (imbues or {}).items() if n in owned and (sraw(n, 'AmmoReloadPercent') or sraw(n, 'ActiveReloadPercent'))}
    for c in C:
        if c['kind'] == 'locked': continue
        P = c['P']; cd = pv(P, 'AbilityCooldown') or 0; keys = set(P)
        cc = any(re.search(r'Sleep|Stun|Slow|Silence|Root|Immobil|Pull', k) for k in keys)
        buff = c['kind'] == 'gun-mode' and not c.get('ult')
        esc = c['slot'] in R.get('mob', {}) and not c['sph']
        if c['slot'] in reload_imb: ev.append((round(max(0.5, mag_s), 1), c['slot'])); spec.append(f"{c['name']}: cast when the magazine empties (~{mag_s:.1f}s) - triggers the imbued reload item"); continue
        if c.get('ult'):
            if c['sph'] or c['kind'] == 'gun-mode': ev.append((2.0, c['slot'])); spec.append(f"{c['name']} (ult): once at 2s")
            else: excl.append(f"{c['name']} (ult, no damage)")
            continue
        if esc or c['kind'] == 'utility' or cd <= 0: excl.append(f"{c['name']} ({'escape' if esc else 'utility/passive'})"); continue
        t0 = 0.0 if cc else 0.2 if buff else 0.5
        n = 1 + (int((window - t0) / cd) if cd and cd < window else 0)
        for i in range(n): ev.append((round(t0 + i * cd, 1), c['slot']))
        spec.append(f"{c['name']}: {'opener (CC)' if cc else 'before firing (buff)' if buff else 'damage on cooldown'} at {t0:g}s" + (f", every {cd:g}s" if n > 1 else ''))
    ev.sort()
    txt = '; '.join(spec) + (f"; excluded: {', '.join(excl)}" if excl else '') + f" ({purpose}, derived from kit data at these tiers)"
    return txt, ('rot ' + ' '.join(f"{sl}@{t:g}" for t, sl in ev) + ' fire') if ev else 'fire 8'
def plugin_meta(R, st, owned, imbues, *, purpose='complete-build', levels_mode='progression', acts=(), readbacks=(), rng=None, stack_frag=None, inactive=None, condition=None):
    """meta lines in the plugin's deployed format (required_levels, levels_mode, required_activation, required_readback, activation_range/range_expect,
    stack_track, effect_inactive_on_purpose, condition, rotation)."""
    T = st['tA']; L = [f"meta required_levels {plugin_levels(R, T)}", f"meta levels_mode {levels_mode}",
                       'meta ability_levels ' + ', '.join(f"{nm(R,s)} {tlabel(T[s])}" for s in (1, 2, 3, 4)) + f" (souls {st['souls']}, order {''.join(map(str, R['order']))}, game progression model A)"]
    if acts: L.append('meta required_activation ' + ' ; '.join(acts))
    if readbacks: L.append('meta required_readback ' + ' ; '.join(readbacks))
    if rng: L += [f"meta activation_range {rng[0]}", f"meta range_expect {rng[1]}"]
    if stack_frag: L.append(f"meta stack_track {stack_frag}")
    if inactive: L.append(f"meta effect_inactive_on_purpose {inactive}")
    if condition: L.append(f"meta condition {condition}")
    rt, op = rotation(R, T, owned, imbues, purpose=purpose); L.append(f"meta rotation {rt}")
    return L, op
M_TO_U = 39.37   # ASSUMED unit scale (Source: 1 unit = 1 inch); GAPS 3 notes 590-790u for 15 m is unverified -> range_expect readback decides
def item_acts(R, owned, imbues):
    """required_activation specs for owned items that need an action to work (plugin kinds: modifier | ability | event)."""
    out = []
    for n in owned:
        s = (g69().get(n) or {}).get('stats', {}); cls = item(n)['class'] if item(n) else ''
        if 'AmmoReloadPercent' in s and n in (imbues or {}):
            out.append(f"{re.sub(r'\W+', '_', n)}_refill|event|refill|1"); out.append(f"{re.sub(r'\W+', '_', n)}_cast|ability|{ability_frag(R, imbues[n])}|1")
        elif item_targeting(n)['act'] in ('INSTANT_CAST', 'PRESS') or 'ActiveReloadPercent' in s:
            out.append(f"{re.sub(r'\W+', '_', n)}|modifier|{cls.replace('upgrade_', '')}|1")
    return out

# ---------------- conditional items (15:33 #5/#6) ----------------
def cond_class(n):
    s = (g69().get(n) or {}).get('stats', {})
    if 'DamageToStack' in s: return 'damage-taken stacks'
    if 'LowHealthThreshold' in s or 'LifeThreshold' in s: return 'health-gated'
    if 'EnemyLifeThreshold' in s or 'CurrentHealthDamage' in s: return 'enemy-health dependent'
    if ('AbilityDuration' in s or 'BuffDuration' in s) and any(k in s for k in ('BonusFireRate', 'ActivatedFireRate', 'TechPower', 'BaseAttackDamagePercent')): return 'timed buff'
    return None
def conditional(b, cand, at=None, out=None, argv=''):
    """separates unconditional value, peak value, time to activation, active window, useful window and checkpoint availability; three scenario designs."""
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = False; R['mob'] = mobility_slots(R)
    rows = [r for r in R['rows'] if not r.get('unknown')]; inb = next((r for r in rows if r['n'] == cand), None)
    s = (g69().get(cand) or {}).get('stats', {}); kind = cond_class(cand) or 'unconditional'
    cps = sorted({5000, 10000, 15000, 20000} | ({inb['souls']} if inb else set()))
    o = []; P0 = {k: v[0] for k, v in STRAT_P.items()}; tab = []
    for cp in cps:
        prev = [r for r in rows if r['souls'] <= cp]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': cp, 'owned': [], 'imbues': {}, 'box': ''}
        base_w = dict(base_w, owned=[x for x in base_w['owned'] if x != cand])
        for esc in (0.6, 1.0, 1.6):
            P = dict(P0, enemy=esc); e = enemy_at(cp / P['E_SPM'], P, R['HB'])
            w0, st0 = ia_state(R, base_w, cp, None); m0 = seg_metrics(R, w0, st0); t0 = trade(m0, P, e)
            w1, st1 = ia_state(R, base_w, cp, cand); m1 = seg_metrics(R, w1, st1); t1 = trade(m1, P, e)
            mix = (1 - P['spirit_share']) * m1['br'] + P['spirit_share'] * m1['sr']; inc = e['dps'] * (1 - mix); net = max(1.0, inc - t1['heal'] / P['W'])
            hp = m1['hp'] + t1['bar']; ttd = hp / net; fight = 12.0
            gun_share = t1['gun'] / max(1e-9, t1['dps']); pool = st1['wb'] + sum(sval(x, 'BaseAttackDamagePercent') for x in w1['owned'])
            pool_fr = sum(sval(x, 'BonusFireRate') + sval(x, 'FireRateBonus') for x in w1['owned'])
            uncond = (t1['dps'] / max(1e-9, t0['dps']) - 1) * 100   # stats that are always on (health, base fire rate...): what a full-health dummy test sees
            peak = act_t = active = useful = 0.0; note = ''
            if kind == 'health-gated':
                thr = (sval(cand, 'LowHealthThreshold') or sval(cand, 'LifeThreshold')) / 100
                below = 'LowHealthThreshold' in s
                act_t = (1 - thr) * hp / net if below else 0.0
                fr_b = sval(cand, 'FervorFireRate')
                peak = (fr_b / (100 + pool_fr) * gun_share * 100) if fr_b else 0.0
                active = max(0.0, min(fight, ttd) - act_t) if below else min(fight, max(0.0, (1 - thr) * hp / net))
                useful = active * (1 - 0.3)   # ASSUMED: 30% of the low-health window is spent retreating/reloading/CC'd
                note = f"active below {thr*100:.0f}% hp: reached after {act_t:.1f}s under {inc:.0f} dps, dead at {ttd:.1f}s" if below else f"active above {thr*100:.0f}% hp for {active:.1f}s"
            elif kind == 'damage-taken stacks':
                per = sval(cand, 'DamageToStack'); dur = sval(cand, 'DamageDuration') or 10; wps = sval(cand, 'WeaponPowerPerStack')
                stacks_at = lambda t: (min(t, dur) * inc) / per   # stacks from damage taken in the last `dur` seconds (raw damage after resist, ASSUMED)
                tl = min(fight, ttd); avg = sum(stacks_at(i * 0.1) for i in range(int(tl * 10))) / max(1, int(tl * 10))
                peak = wps * stacks_at(tl) / (100 + pool) * gun_share * 100
                active = tl; useful = tl; act_t = per / max(1.0, inc)
                note = f"{stacks_at(tl):.1f} stacks when the fight ends or you die ({tl:.1f}s), average {avg:.1f} stacks; first stack after {act_t:.1f}s"
                peak_avg = wps * avg / (100 + pool) * gun_share * 100
            elif kind == 'timed buff':
                du = sval(cand, 'AbilityDuration') or sval(cand, 'BuffDuration'); cd = sval(cand, 'AbilityCooldown') or 30
                active = min(fight, du); useful = active * min(1.0, P['W'] / fight + 0.5); note = f"{du:g}s buff every {cd:g}s"
            gain = uncond + (peak * useful / fight if kind == 'health-gated' else (peak_avg if kind == 'damage-taken stacks' else 0.0))
            tab.append((cp, esc, uncond, peak, act_t, active, useful, gain, (t1['tr'] / t0['tr'] - 1) * 100, note))
    # equal-souls alternative at the same checkpoint (the build's own buy point if any)
    hdr = ['SCOPE: build-context', 'KIND: conditional', f'BUILD: {b["id"]}', f'ITEM: {cand}', f'CONDITION: {kind}', f'ARGS: {argv}',
           f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
           'METHOD: unconditional value (always-on stats) + peak value x useful active window / 12 s fight; activation from the --strategy enemy model at each checkpoint (ASSUMED enemy dps, CALCULATED item numbers); not buff duration, not a full-health dummy test']
    o += hdr + ['', 'checkpoint | enemy | unconditional dmg% | peak dmg% (gun share) | t_activate s | active s | useful s | fight-avg dmg% | dTR% (stats only) | notes']
    for r in tab: o.append(f"{r[0]:>6} | x{r[1]:<4} | {r[2]:+7.1f} | {r[3]:+7.1f} | {r[4]:5.1f} | {r[5]:5.1f} | {r[6]:5.1f} | {r[7]:+7.1f} | {r[8]:+6.1f} | {r[9]}")
    o.append('\n## SCENARIO DESIGNS (three phases; each its own request file, kind INTERACTION)')
    files = scen_conditional(b, R, cand, kind, cps, rows)
    o += ['  ' + f for f in files]
    o.append('\n## READING THE EVIDENCE')
    o.append('  - inactive baseline: only the unconditional part; it is never evidence that the item is weak (meta effect_inactive_on_purpose).')
    o.append('  - deliberately activated: measures the peak value with the condition forced (health-gated: lowhp; damage-taken: NOT forceable - artificial damage does not trigger it, plugin pauses it).')
    o.append('  - realistic encounter: needs real enemy damage (shoot-back bot); until it exists the fight-avg column above is CALCULATED+ASSUMED and the verdict stays INSUFFICIENT for damage-taken items.')
    o.append('  - conclusion changes: if the measured activated peak is below the modelled peak, scale the fight-avg column by measured/modelled; if the realistic run shows activation later than t_activate, recompute useful s.')
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/conditional/{b['id']}_{re.sub(r'\W+', '_', cand)}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, files, tab
def scen_conditional(b, R, cand, kind, cps, rows):
    od = SP + '/council/sandbox/autorun/scenarios/interaction'; os.makedirs(od, exist_ok=True); files = []
    inb = next((r for r in rows if r['n'] == cand), None); cp = inb['souls'] if inb else cps[len(cps) // 2]
    prev = [r for r in rows if r['souls'] <= cp]; base_w = dict(prev[-1]) if prev else {'n': None, 'souls': cp, 'owned': [], 'imbues': {}, 'box': ''}
    w, st = ia_state(R, dict(base_w, owned=[x for x in base_w['owned'] if x != cand]), cp, cand)
    give = [item(x)['class'] for x in w['owned'] if item(x)]; cls = item(cand)['class']; frag = cls.replace('upgrade_', '')
    tiers = st['tA']; bits = lambda t2: 0 if t2 < 0 else (1, 3, 7, 15)[t2]
    s = (g69().get(cand) or {}).get('stats', {}); thr = sval(cand, 'LowHealthThreshold') or sval(cand, 'LifeThreshold')
    def fit(*cs, lim=32): cs = [c for c in cs if c]; return next((c for c in cs if len(c) <= lim), cs[0])
    for phase in ('inactive', 'activated', 'realistic'):
        dmg_taken = kind == 'damage-taken stacks'
        cond = None; inactive = None; acts = [f"{frag}|modifier|{frag}|1"]; rb = ["levels_ok|1|==|1"]
        if phase == 'inactive': inactive = f"{kind} condition kept OFF on purpose (full health / no damage taken): measures only the always-on stats"; acts = []
        elif phase == 'activated': cond = ('damage taken from enemies (artificial incoming damage does not trigger it)' if dmg_taken else f"own health below {thr:g}% forced with lowhp")
        else: cond = 'real enemy damage taken in a shoot-back exchange; activation timing and survival measured (damage taken)'
        L, op = plugin_meta(R, st, w['owned'], w['imbues'], purpose=f"conditional {phase}", acts=acts, readbacks=[], stack_frag=frag if dmg_taken else None, inactive=inactive, condition=cond)
        q = {'inactive': f"Measuring {cand} with its condition off on purpose, as the baseline for {b['hero']}.",
             'activated': f"Checking {cand}'s full bonus on {b['hero']} with its condition switched on.",
             'realistic': f"Checking how long {cand} is really active for {b['hero']} in a fight where the enemy shoots back."}[phase]
        head = [f"# conditional item scenario ({phase}) generated by abtimeline.py --conditional; kind of condition: {kind}", 'meta kind INTERACTION', f"meta question {q}",
                f"meta purpose {phase} phase of the three-phase conditional test for {cand} on {b['id']}", f"meta mechanics {kind}: " + ', '.join(f"{k}={v}" for k, v in s.items() if k != 'AbilityUnitTargetLimit')[:200],
                f"meta expectedstate souls={cp} items={','.join(give)}", f"meta build {b['id']}", f"meta checkpoint {cp}", f"meta items {' '.join(give)}",
                f"meta strategy_source council/evidence/conditional/{b['id']}_{re.sub(r'\W+', '_', cand)}.txt", f"meta feeds conditional model {b['id']} {cand}",
                'meta selection_kind build-decision' if inb else 'meta selection_kind requested', f"meta selection_reason {cand} {'is bought at ' + str(cp) + ' in ' + b['id'] if inb else 'is a requested conditional-item example'}; phase {phase} of inactive/activated/realistic",
                f"meta alternative_reason none: each phase isolates one part of the conditional value", f"meta scenario_phase {phase}",
                f"meta evidence_use {'baseline only: never evidence the item is weak' if phase == 'inactive' else 'peak value with the condition forced' if phase == 'activated' else 'realistic uptime and survival'}",
                f"meta measurement_requirement {'real enemy damage (no supported source yet)' if (dmg_taken and phase != 'inactive') or phase == 'realistic' else 'lowhp op' if phase == 'activated' else 'none'}",
                f"meta cond_scope {'complete build, rotation' if phase != 'inactive' else 'complete build, rotation, condition off'}", 'meta cond_abilities_used rotation (see meta rotation)', 'meta cond_abilities_excluded escapes',
                'meta cond_accuracy all shots on target', 'meta cond_misses none', f"meta cond_start_stacks {'0 (verify)' if dmg_taken else 'n/a'}", f"meta cond_activations {cand if phase != 'inactive' else 'none (off on purpose)'}",
                'meta cond_distance 350u', f"meta cond_targets enemies=1 allies=0", f"meta readbacks equipped_items,ability_tiers{',stacks_per_block' if dmg_taken else ''},activation:{cand}",
                f"meta player_title {fit(f'{cand}: {phase} test', f'{cand} {phase}', f'Conditional {phase}')}", f"meta player_what {fit({'inactive': 'Condition off on purpose', 'activated': 'Condition forced on', 'realistic': 'Enemy shoots back'}[phase])}",
                f"meta player_why {fit({'inactive': 'Baseline, not a verdict', 'activated': 'Full bonus when active', 'realistic': 'How long it really works'}[phase])}",
                f"meta player_short {fit(f'{cand} {phase}', phase.capitalize(), lim=26)}", f"meta player_expect {fit({'inactive': 'Always-on part only', 'activated': 'Peak damage gain', 'realistic': 'Active seconds, damage'}[phase])}",
                f"meta result_says {'baseline numbers only' if phase == 'inactive' else 'activation count, stacks/uptime and damage while active; compare with the --conditional table'}"]
        if (dmg_taken and phase != 'inactive') or phase == 'realistic': head.insert(6, 'meta blocked_by no real enemy damage source in the runner (artificial incoming damage does not trigger damage-taken effects); paused-needs-design')
        proc = ['setup ' + b['hk'].replace('hero_', '').capitalize() + ' Haze', 'raw citadel_unlock_flex_slots', f"abil {' '.join(str(bits(tiers[x])) for x in (1,2,3,4))}", f"souls {cp}", 'hardreset', f"souls {cp}"] + [f"give {g}" for g in give] + ['basemods', 'enemies 1 300 4', 'fetch 350', 'cast reload 2.5']
        if phase == 'activated' and kind == 'health-gated': proc += [f"lowhp {max(1, int(thr) - 10)}"]
        proc += [f"mark {phase}", op, 'mark none', 'lowhp 0', 'end']
        f = f"{od}/int_{b['id']}_{re.sub(r'\W+', '_', cand)}_cond_{phase}.txt"; open(f, 'w').write('\n'.join(head + L + proc) + '\n'); files.append(os.path.relpath(f, SP))
    return files

# ---------------- investment-threshold-aware selling (15:35) ----------------
def inv_walk(b, policy='oldest-cheapest', slots=12, sells=None):
    """purchase walk with sells: 'Sell X for this' notes, then the slot cap (12) forces a sale chosen by policy:
    oldest-cheapest (ASSUMED default player habit) | preserve-spike (cheapest sale that keeps every category already >=4.8k at >=4.8k, if any exists).
    Investment counted = full tier price of every HELD item (upgrades include their consumed components; sold items stop counting) - ASSUMED rule, not verified in data."""
    path = core_path(b); owned = []; ev = []; souls = 0
    def inv(L): return {c: sum(SOULS[item(o)['tier']] for o in L if colour_of(o) == c) for c in COLS.values()}
    est = set()
    for x in path:
        n = x[0]; it = item(n)
        if not it: continue
        before = inv(owned); have = [c for c in it['components'] if c in owned]
        souls += max(0, SOULS[it['tier']] - sum(SOULS[item(c)['tier']] for c in have)); owned = [o for o in owned if o not in have] + [n]
        sold = []
        sm = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first)', x[1] or '')
        if sm and sm.group(1) in owned: owned.remove(sm.group(1)); sold.append(sm.group(1))
        while len(owned) > slots:
            cands = [o for o in owned if o != n and not REG.get(item(o)['class'], '') == 'imbue' or (o != n)]
            cands = [o for o in owned if o != n]
            if policy == 'preserve-spike':
                ok = [o for o in cands if all(v >= 4800 for c, v in inv([y for y in owned if y != o]).items() if c in est)]
                pick = min(ok or cands, key=lambda o: (SOULS[item(o)['tier']], owned.index(o)))
            else: pick = min(cands, key=lambda o: (SOULS[item(o)['tier']], owned.index(o)))
            owned.remove(pick); sold.append(pick)
        after = inv(owned)
        gained = [f"{c} {th}" for c in after for th in (4800, 6400, 8000) if before[c] < th <= after[c]]
        lost = [f"{c} {th}" for c in after for th in (4800, 6400, 8000) if after[c] < th <= before[c]]
        drop = [c for c in est if after[c] < 4800]
        for c, v in after.items():
            if v >= 4800: est.add(c)
        ev.append(dict(n=n, souls=souls, sold=sold, before=before, after=after, gained=gained, lost=lost, drop=drop, owned=list(owned)))
    return ev
def investment(b, out=None, argv=''):
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in core_path(b)]); R['mob'] = mobility_slots(R)
    A = inv_walk(b, 'oldest-cheapest'); Bp = inv_walk(b, 'preserve-spike'); P0 = {k: v[0] for k, v in STRAT_P.items()}
    def tr_at(ev):
        w = {'n': ev['n'], 'souls': ev['souls'], 'owned': ev['owned'], 'imbues': {}, 'box': ''}; st = state(R, w); m = seg_metrics(R, w, st)
        t = trade(m, P0, enemy_at(ev['souls'] / P0['E_SPM'], P0, R['HB'])); return t, m
    o = ['SCOPE: build-context', 'KIND: investment', f'BUILD: {b["id"]}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         'COUNTING: ASSUMED - held items count their full tier price (an upgrade includes its consumed components once); a sold item stops counting; sale refunds are not modelled (refund % not in data). Bonus tiers: heroes.vdata m_MapModCostBonuses (CALCULATED).']
    drops = [(i, e) for i, e in enumerate(A) if e['drop']]
    o.append(f"DROPS (oldest-cheapest sells, 12 slots): {len(drops)}" + ('' if drops else ' - no established 4.8k category is ever lost'))
    o.append('\n## TRANSACTIONS (default policy)  souls | bought | sold | gun/vit/spirit invest after | thresholds gained | lost')
    for e in A:
        if e['sold'] or e['gained'] or e['lost']: o.append(f"  {e['souls']:>6} | {e['n']} | {', '.join(e['sold']) or '-'} | {e['after']['gun']}/{e['after']['vitality']}/{e['after']['spirit']} | {', '.join(e['gained']) or '-'} | {', '.join(e['lost']) or '-'}")
    verdicts = []
    for i, e in drops:
        tA, mA = tr_at(e); tB, mB = tr_at(Bp[i])
        share = {'gun': tA['gun'] / max(1e-9, tA['dps']), 'spirit': tA['spirit'] / max(1e-9, tA['dps']), 'vitality': None}
        for c in e['drop']:
            sh = share.get(c); pres = Bp[i]['after'][c] >= 4800
            d = (tB['tr'] / tA['tr'] - 1) * 100
            pivot = sh is not None and sh < 0.2
            v = ('PRESERVE: a different sale keeps it and the build is ' + f"{d:+.1f}% trade ratio better" if pres and d > 2 else
                 'ABANDON OK: ' + (f"{c} delivers only {sh*100:.0f}% of damage now (pivot away from {c})" if pivot else f"keeping it changes trade ratio by {d:+.1f}% only") if (pivot or (pres and d <= 2)) else
                 f"DROP WITHOUT A PRESERVING SALE: no sale keeps {c} >= 4.8k at {e['souls']}; {c} share of damage {('n/a' if sh is None else f'{sh*100:.0f}%')}")
            verdicts.append(f"{c} at {e['souls']} (bought {e['n']}, sold {', '.join(e['sold'])}): {v}; preserving sale: {', '.join(Bp[i]['sold']) or '-'} (TR {tA['tr']:.2f} -> {tB['tr']:.2f}, CALCULATED+ASSUMED)")
    o.append('\n## DROP VERDICTS (value of the lost bonus for this playstyle vs the preserving alternative)'); o += ['  - ' + v for v in verdicts] or ['  none']
    o.append('\n## PRESERVE-SPIKE SEQUENCE (policy preserve-spike)')
    for e in Bp:
        if e['sold']: o.append(f"  {e['souls']:>6} | {e['n']} | sold {', '.join(e['sold'])} | {e['after']['gun']}/{e['after']['vitality']}/{e['after']['spirit']}")
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/investment/{b['id']}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, verdicts, drops

# ---------------- situational swaps by enemy composition (15:39) ----------------
def roster():
    """every hero in heroes.vdata: base health, health per level, starting resists from hero scaling (ASSUMED 0 base resist when absent)."""
    t = open(SC + 'heroes.vdata', encoding='utf-8', errors='ignore').read(); out = {}
    for h in re.findall(r'\n\t(hero_\w+) = ', t):
        if h == 'hero_base': continue
        hs = hero_stats(h); out[h] = dict(hp=hs['hp'], hp_lvl=hs['hp_lvl'])
    return out
def composition_enemy(P, t_min, hp_mult, res_add=0.0, heal_frac=0.0):
    e = enemy_at(t_min, P, HB_of()); e = dict(e); e['hp'] *= hp_mult; e['res'] = min(0.6, e['res'] + res_add); e['ehp'] = e['hp'] / (1 - e['res']) * (1 + heal_frac); return e
def situational(b, cand, replace=None, at=None, margin=5.0, out=None, argv=''):
    """value of a situational item vs the default item it replaces, across enemy compositions (target health pool multiplier, resist, enemy healing),
    at several checkpoints; trigger = derived enemy-state range where the swap beats the default by >= margin (pre-registered) in every reading."""
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in core_path(b)]); R['mob'] = mobility_slots(R)
    rows = [r for r in R['rows'] if not r.get('unknown')]; P0 = {k: v[0] for k, v in STRAT_P.items()}
    ros = roster(); hps = sorted(v['hp'] for v in ros.values()); med = hps[len(hps) // 2]
    mults = sorted({round(h / med, 2) for h in (hps[0], hps[len(hps) // 4], med, hps[3 * len(hps) // 4], hps[-1])} | {1.5, 2.0})   # roster spread (CALCULATED) + tank items (ASSUMED)
    cps = [c for c in (10000, 15000, 20000, 25000)]; tab = []
    s = (g69().get(cand) or {}).get('stats', {})
    for cp in cps:
        prev = [r for r in rows if r['souls'] <= cp]
        if not prev: continue
        base_w = dict(prev[-1]); own = list(base_w['owned'])
        rep = replace if replace in own else next((x for x in reversed(own) if item(x)['tier'] == item(cand)['tier'] and x != cand), None)
        if not rep: continue
        for hm in mults:
            for heal in (0.0, 0.3):
                P = dict(P0); e = composition_enemy(P, cp / P['E_SPM'], hm, 0.0, heal)
                wD, stD = ia_state(R, base_w, cp, None); mD = seg_metrics(R, wD, stD); tD = trade(mD, P, e)
                wS, stS = ia_state(R, dict(base_w, owned=[x for x in own if x != rep]), cp, cand); mS = seg_metrics(R, wS, stS); tS = trade(mS, P, e)
                extra = 0.0
                if 'CurrentHealthDamage' in s:   # % current-health proc on ability hits >= MinimumDamage, one per AbilityChargeUpTime (CALCULATED trigger; hit rate ASSUMED 1 per cooldown)
                    extra = (sval(cand, 'Damage', stS['sp']) + sval(cand, 'CurrentHealthDamage') / 100 * e['hp'] * 0.75) * min(1.0, P['W'] / (sval(cand, 'AbilityChargeUpTime') or 14) + 0.5) / P['W']
                if any(k in s for k in ('HealAmpReceivePenaltyPercent',)):   # anti-heal: enemy effective EHP shrinks by the healing it loses
                    e2 = dict(e); e2['ehp'] = e['hp'] / (1 - e['res']) * (1 + heal * (1 + sval(cand, 'HealAmpReceivePenaltyPercent') / 100)); tS = trade(mS, P, e2)
                ttk = e['ehp'] / max(1.0, tS['dps'] + extra); tr = tS['ttd'] / ttk
                gain = (tr / tD['tr'] - 1) * 100
                tab.append((cp, rep, hm, heal, gain))
    # trigger ranges: per checkpoint the smallest health multiplier where the swap beats default by >= margin at BOTH healing readings
    trig = {}
    for cp in cps:
        rs = [r for r in tab if r[0] == cp]
        if not rs: continue
        ok = sorted({r[2] for r in rs if all(x[4] >= margin for x in rs if x[2] == r[2])})
        trig[cp] = (rs[0][1], ok[0] if ok else None, max(r[4] for r in rs), min(r[4] for r in rs))
    default_stays = all(v[1] is None for v in trig.values())
    best_cp = min((cp for cp, v in trig.items() if v[1] is not None), default=None)
    o = ['SCOPE: build-context', 'KIND: situational', f'BUILD: {b["id"]}', f'ITEM: {cand}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f'MARGIN (pre-registered): swap must beat the default by >= {margin:g}% trade ratio at both enemy-healing readings (0%, 30% of their pool)',
         'ENEMY MODEL: reference enemy (--strategy) with its health pool scaled by the roster spread of heroes.vdata base health (CALCULATED) and x1.5/x2.0 for health-stacked tanks (ASSUMED); resists and healing ASSUMED; target choice = the enemy you fight',
         ('VERDICT: DEFAULT STAYS - no composition in the tested range gives the margin' if default_stays else f"VERDICT: SITUATIONAL - swap when the target's health pool is >= the trigger below; earliest worthwhile checkpoint {best_cp}"),
         'GRADE: CALCULATED item numbers + ASSUMED enemy composition/healing/hit rate']
    o.append('\n## TRIGGERS (derived): checkpoint | replaces | health-pool multiplier from which swap wins by margin | gain range %')
    for cp, (rep, hm, mx, mn) in trig.items(): o.append(f"  {cp:>6} | {rep} | {('x' + format(hm, 'g') + ' of median hero health (' + format(hm * med, '.0f') + ' base hp)') if hm else 'never in range'} | {mn:+.1f} .. {mx:+.1f}")
    o.append('\n## TABLE: checkpoint | replaces | health mult | enemy healing | gain %')
    for r in tab: o.append(f"  {r[0]:>6} | {r[1]} | x{r[2]:<4} | {r[3]:.1f} | {r[4]:+6.1f}")
    o.append('\n## COST / WHAT BREAKS: selling the replaced item refunds an unknown share (not in data, ASSUMED 50%); check --investment for spike loss; the replaced item\'s other roles (sustain/mobility) are lost (see the interaction matrix of the replaced item)')
    o.append("\n## HOW IT WOULD BE RECORDED (read-only design, data.js untouched): an optional box ['Situational', '<trigger in plain words>', '', [['" + cand + "', 'Swap for " + (tab[0][1] if tab else '?') + " when <trigger>.']]]")
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/situational/{b['id']}_{re.sub(r'\W+', '_', cand)}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, ('DEFAULT STAYS' if default_stays else f'SITUATIONAL from {best_cp}'), trig
def k1533_main(a, B):
    mode = a[0]; bid = a[1]; b = next(x for x in B if x['id'] == bid); argv = ' '.join(a)
    at = int(a[a.index('--at') + 1]) if '--at' in a else None
    if mode == '--conditional':
        f, files, tab = conditional(b, a[2], at, None, argv); print('wrote', f); [print('  scenario', x) for x in files]
    elif mode == '--investment':
        f, v, d = investment(b, None, argv); print('wrote', f); [print('  ', x) for x in v] or print('  no 4.8k drop under the default sell policy')
    elif mode == '--situational':
        rep = a[a.index('--replace') + 1] if '--replace' in a else None; f, v, trig = situational(b, a[2], rep, at, 5.0, None, argv); print('wrote', f); print('VERDICT:', v)
        for cp, t in trig.items(): print('  ', cp, t)

# ======================================================================================================
# PURCHASE PATHS (Kieran 15:35-15:44): compare complete buy/upgrade/keep/sell sequences with the --strategy income walk.
# usage: python3 -I abtimeline.py --path <build> temporary --at <souls> [--tier 1] [--queue]   candidate purchases scanned from the full catalog at a checkpoint
#        python3 -I abtimeline.py --path <build> audit [--out f]                              branch structure + computed sale checklist + alternative sequences
#        python3 -I abtimeline.py --path ALL detect                                           read-only detectors over every data.js build (central parameters)
#        python3 -I abtimeline.py --selftest                                                  ledger sums / no double counting / branch parsing
# Every number carries a provenance tier: VERIFIED GAME MECHANIC (game data) | CONTROLLED SANDBOX RESULT (validated result file) |
# MODELLED ESTIMATE (formula + assumptions) | UNVERIFIED HYPOTHESIS (stated by someone, not in data or tests).
# Verdict classes: SUPPORTED (decisive inputs measured) | MODEL-ONLY (robust across the grid) | MODEL-ONLY, assumption-sensitive (flips if ...) | INSUFFICIENT.
# Value of an item = the ledger difference between complete paths with and without it (souls earned by mechanism, one owner per effect) plus the
# fight-strength difference (trade ratio); nothing is added twice: economic effects live only in the ledger, combat strength only in the trade ratio.
PT = ('VERIFIED GAME MECHANIC', 'CONTROLLED SANDBOX RESULT', 'MODELLED ESTIMATE', 'UNVERIFIED HYPOTHESIS')
PATH_GRID = {'hit': (0.35, 0.55, 0.75), 'enemy': (0.6, 1.0, 1.6), 'beta': (0.0, 0.25, 0.5), 'POKE': (0.06, 0.12, 0.2), 'lost': (0, 1)}
def branch_types(b):
    out = []
    for r in b['rows']:
        for box in r:
            t = box[0]
            k = ('main path (sequential)' if re.match(r'^(Early|Mid|Late)', t) else 'counter menu (mutually exclusive, buy only if needed)' if re.match(r'^Counters', t)
                 else 'luxury ending (optional branch, each item separately)' if re.search(r'rich', t, re.I) else 'optional upgrade (branch)' if re.search(r'Slot locked', t)
                 else 'lane alternative (branch)' if re.search(r'lane', t, re.I) else 'alternative/optional (branch)')
            out.append((t, k, [x[0] for x in box[3]], [(x[0], x[1]) for x in box[3] if len(x) > 1 and re.search(r'Sell ', x[1] or '')]))
    return out
def path_eval(b, variants, grid=None, T_END=None, base_name=None):
    """variants: {name: path}. Each simulated over the grid (central + listed values). Returns per variant per cell: souls earned at minutes, mean ln trade ratio,
    ledger (souls by mechanism), purchase times."""
    order = list(b['order']); P0 = {k: v[0] for k, v in STRAT_P.items()}; HB = HB_of()
    R0 = strat_R(b, list(variants.values())[0], order); R0['HB'] = HB
    P0['kappa'] = None; segs = {}
    for nmv, pth in variants.items():
        R = strat_R(b, pth, order); R['HB'] = HB; segs[nmv] = (R, segments(R))
    if P0.get('kappa') is None:
        k = 1.0; ref = segs[base_name or list(variants)[0]][1]
        for _ in range(6):
            P0['kappa'] = k; s10 = simulate(ref, P0, HB)['at'].get(10, 1.0); k = k * (P0['E_SPM'] * 10 / max(1.0, s10)) ** 0.9
        P0['kappa'] = k
    if T_END: P0['T_END'] = T_END
    G_ = grid if grid is not None else PATH_GRID; keys = list(G_.keys()); cells = []
    for combo in [()] + (list(itertools.product(*[G_[k] for k in keys])) if keys else []):
        P = dict(P0); P.update(dict(zip(keys, combo))) if combo else None; E = enemies(P, HB); res = {}
        for nmv, (R, sg) in segs.items():
            sm = simulate(sg, P, HB, E)
            res[nmv] = dict(S=dict(sm['S']), trs=sm['trs'], tr=math.exp(sum(sm['tr']) / max(1, len(sm['tr']))), ledger=sm['ledger'], deaths=sm['deaths'],
                            buys=[(r['n'], r['souls'], time_to(sm, r['souls'])) for r in R['rows'] if not r.get('unknown')])
        cells.append((dict(zip(keys, combo)) if combo else 'central', res))
    return cells, P0
def S_at(res, t):
    best = None
    for tm, v in res['S'].items():
        if tm <= t + 1e-9: best = v
    return best or 0.0
def ledger_delta(a, b):
    return {k: a['ledger'].get(k, 0) - b['ledger'].get(k, 0) for k in set(a['ledger']) | set(b['ledger'])}
def verdict_class(deltas, keyname, cells, noise):
    """deltas = list of (cell, value); sign robustness and which single assumption flips it."""
    vals = [v for c, v in deltas]; med = sorted(vals)[len(vals) // 2]; pos = sum(1 for v in vals if v > noise) / len(vals); neg = sum(1 for v in vals if v < -noise) / len(vals)
    flips = []
    for k in PATH_GRID:
        by = {}
        for c, v in deltas:
            if c == 'central': continue
            by.setdefault(c[k], []).append(v)
        signs = {val: (sum(1 for x in vs if x > noise) / len(vs)) for val, vs in by.items()}
        if any(s >= 0.5 for s in signs.values()) and any(s < 0.5 for s in signs.values()): flips.append(f"{k} (" + ', '.join(f"{val}: {'+' if s >= 0.5 else '-'}" for val, s in sorted(signs.items())) + ')')
    if abs(med) <= noise and max(pos, neg) < 0.8: cls = 'INSUFFICIENT (effect within model noise)'
    elif max(pos, neg) >= 0.8: cls = 'MODEL-ONLY (sign robust in ' + f"{max(pos, neg)*100:.0f}% of cells; no measured inputs)"
    else: cls = 'MODEL-ONLY, assumption-sensitive (flips with ' + ('; '.join(flips) or 'several parameters together') + ')'
    return med, pos, neg, cls
def mechanism_rows(n, R=None):
    """how each data stat of an item enters the model, with provenance (no claim beyond the model)."""
    s = (g69().get(n) or {}).get('stats', {}); rows = []
    M = {'BonusHealthRegen': 'regen -> lane HP budget -> forced recalls (lane troopers lost) and trade time-to-die', 'OutOfCombatHealthRegen': 'out-of-combat regen x OOC_SHARE -> lane HP budget -> forced recalls',
         'BonusHealth': 'max health -> time-to-die (trade ratio -> lane/fight income via beta, deaths) and HP budget', 'CombatBarrier': 'barrier per trade (cooldown-limited) -> time-to-die, HP budget',
         'BaseAttackDamagePercent': 'weapon damage -> time-to-kill -> trade ratio, kills; clear speed -> farm', 'BonusFireRate': 'more bullets -> damage, clear speed, lifesteal hits',
         'BulletLifestealPercent': 'heal from bullet damage -> time-to-die, HP budget', 'TechPower': 'spirit power -> ability damage, ability-scaled heals/barriers, hero spirit scalings',
         'NonPlayerBonusWeaponPower': 'damage vs NPCs -> clear speed -> camps/waves farmed', 'BonusMoveSpeed': 'move speed (not priced in income; escape flag only)',
         'BonusSprintSpeed': 'sprint (not priced: travel time between camps is a fixed parameter)', 'TotalHealthRegen': 'active heal (cooldown) -> HP budget via heal per trade (if modelled for actives: NOT priced unless barrier/heal key is read)',
         'LifestrikeHeal': 'melee heal -> time-to-die', 'BonusClipSizePercent': 'magazine -> bullets per window -> damage', 'StackingGoldPerMinute': 'NOT priced in the income walk (gap)', 'BonusGoldPerMinute': 'NOT priced in the income walk (gap)'}
    for k, v in s.items():
        if k == 'AbilityUnitTargetLimit': continue
        rows.append((f"{n}.{k} = {v}", PT[0], M.get(k, 'not used by the model (no mechanism encoded) -> contributes 0 here')))
    return rows
def path_temporary(b, at, tier=1, queue=False, argv='', out=None):
    path0 = core_path(b); R0 = analyse(b); rows = [r for r in R0['rows'] if not r.get('unknown')]
    pos = len([r for r in rows if r['souls'] <= at]); owned_at = rows[pos - 1]['owned'] if pos else []
    cands = [n for n, g in items().items() if not g.get('disabled') and g['tier'] == tier and n not in [x[0] for x in path0] and item(n) and item_effects(n)
             and not any(n in item(o)['components'] for o in owned_at)]
    holds = {'sold +4k souls later': 4000, 'sold +8k souls later': 8000, 'kept (never sold)': None}
    variants = {'no purchase (A0 path)': path0}
    for n in cands:
        for hl, dh in holds.items():
            p = [list(x) for x in path0]; p.insert(pos, [n, '', None])
            if dh is not None:
                cum = 0; j = None
                for i2, x in enumerate(p):
                    it = item(x[0]); cum += SOULS[it['tier']] if it else 0
                    if i2 > pos and cum >= at + dh: j = i2; break
                if j is None: continue
                p[j] = [p[j][0], (p[j][1] + ' ' if p[j][1] else '') + f"Sell {n} for this.", p[j][2]]
            variants[f"{n} | {hl}"] = p
    cells, P0 = path_eval(b, variants, base_name='no purchase (A0 path)', T_END=25.0)
    ref = 'no purchase (A0 path)'; T1, T2 = 10.0, 20.0
    res = []
    for nmv in variants:
        if nmv == ref: continue
        d10 = [(c, S_at(r[nmv], T1) - S_at(r[ref], T1)) for c, r in cells]; d20 = [(c, S_at(r[nmv], T2) - S_at(r[ref], T2)) for c, r in cells]
        dtr = [(c, (r[nmv]['tr'] / r[ref]['tr'] - 1) * 100) for c, r in cells]
        med10, p10, n10, cls10 = verdict_class(d10, 'S10', cells, 50.0); med20, p20, n20, cls20 = verdict_class(d20, 'S20', cells, 50.0); mtr, ptr, ntr, clstr = verdict_class(dtr, 'tr', cells, 1.0)
        cen = next(r for c, r in cells if c == 'central'); led = ledger_delta(cen[nmv], cen[ref])
        res.append((nmv, med10, med20, mtr, cls20, clstr, led, S_at(cen[nmv], 99) - S_at(cen[ref], 99)))   # ledger covers the whole simulated window (0-T_END)
    res.sort(key=lambda x: -x[2])
    # self-check of the ledger: the parts must add up to the difference in souls earned (central cell)
    chk = [(r[0], sum(r[6].values()), r[7]) for r in res[:5]]
    o = ['SCOPE: build-context', 'KIND: path', 'MODE: temporary', f'BUILD: {b["id"]}', f'CHECKPOINT: {at} (after {rows[pos-1]["n"] if pos else "nothing"}; owned {owned_at})', f'ARGS: {argv}',
         f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f'CANDIDATES: every unowned tier-{tier} catalog item with a modelled stat ({len(cands)}), each held for 3 windows; reference = no purchase (souls stay in the build path)',
         'METHOD: complete paths through the --strategy soul-income walk; value = ledger difference of souls earned (one owner per mechanism) + trade-ratio difference; resale refund applied at the sale (REFUND, UNVERIFIED HYPOTHESIS)',
         'VERDICT CLASSES: SUPPORTED needs measured inputs (none exist for this build: no shoot-back, no lane economy measurements) -> every row below is at best MODEL-ONLY']
    o.append('\n## RESULTS (median over grid cells; sign robustness; central-cell ledger)')
    o.append('candidate | hold | d souls @10 | d souls @20 | d trade ratio % | verdict (souls @20) | verdict (trade ratio)')
    for nmv, m10, m20, mtr, c20, ctr, led, cen20 in res[:20]:
        it, hl = nmv.split(' | '); o.append(f"{it} | {hl} | {m10:+.0f} | {m20:+.0f} | {mtr:+.1f} | {c20} | {ctr}")
    o.append(f"  ... {max(0, len(res) - 20)} more rows in the full list below")
    o.append('\n## LEDGER (central cell, souls earned 0-25 min by mechanism, candidate minus no purchase; each effect has exactly one owner; MODELLED ESTIMATE)')
    for nmv, m10, m20, mtr, c20, ctr, led, cen20 in res[:5]:
        o.append(f"- {nmv}: " + ', '.join(f"{k} {v:+.0f}" for k, v in sorted(led.items(), key=lambda x: -abs(x[1])) if abs(v) >= 1) + f" | sum {sum(led.values()):+.0f} = total {cen20:+.0f}")
    o.append('LEDGER CHECK: ' + ('; '.join(f"{n_} parts {a:+.1f} vs total {t:+.1f} ({'OK' if abs(a - t) < 1.0 else 'MISMATCH'})" for n_, a, t in chk)))
    o.append('\n## PROVENANCE (top 3 candidates): input | tier | how it enters the model')
    for itn in list(dict.fromkeys(r[0].split(' | ')[0] for r in res))[:3]:
        for row in mechanism_rows(itn): o.append(f"  {row[0]} | {row[1]} | {row[2]}")
    o.append(f"  REFUND {STRAT_P['REFUND'][0]} | {PT[3]} | resale share at the sale")
    for k in ('POKE', 'E_D0', 'LANE_SPM', 'BACK_S', 'beta', 'hit', 'enemy', 'OOC_SHARE'): o.append(f"  {k} = {STRAT_P[k][0]} | {PT[2]} | {STRAT_P[k][2]}")
    o.append(f"  kappa = {P0['kappa']:.3f} | {PT[2]} | income calibrated to ~1000 souls/min (RULES_KIERAN anchor) on the no-purchase path")
    o.append('\n## SENSITIVITY: which grid parameter flips the sign is shown in each verdict; parameters not in the grid (enemy model shape, POKE->recall link, trade model) are structural and untested')
    o.append('\n## FULL LIST'); o += [f"  {r[0]}: d@20 {r[2]:+.0f}, dTR {r[3]:+.1f}% | {r[4]}" for r in res]
    reqs = []
    if queue:
        reqs = path_requests(b, R0, at, owned_at, list(dict.fromkeys(r[0].split(' | ')[0] for r in res))[:3])
        o.append('\n## QUEUED TESTS (to turn MODEL-ONLY inputs into measured ones)'); o += ['  ' + x for x in reqs]
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/path/{b['id']}_temporary_{at}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, res, chk, reqs
def path_requests(b, R, at, owned, cands):
    """one request per candidate: measure the item's own contribution that the model uses (heal/regen, barrier, damage), with readbacks; inputs that need real
    enemy damage (HP lost per trade) are declared blocked."""
    od = SP + '/council/sandbox/autorun/scenarios/interaction'; os.makedirs(od, exist_ok=True); out = []
    w = {'n': None, 'souls': at, 'owned': list(owned), 'imbues': {}, 'box': ''}
    for n in cands:
        w2, st = ia_state(R, w, at, n); s = (g69().get(n) or {}).get('stats', {}); cls = item(n)['class']; give = [item(x)['class'] for x in w2['owned'] if item(x)]
        heal = any(k in s for k in ('BonusHealthRegen', 'OutOfCombatHealthRegen', 'TotalHealthRegen', 'HealOnHit', 'HealFromHero', 'LifestrikeHeal', 'BulletLifestealPercent'))
        bar = any(k in s for k in ('CombatBarrier',)); dmg = any(k in s for k in ('BaseAttackDamagePercent', 'BonusFireRate', 'ProcBonusMagicDamage', 'CloseRangeBonusWeaponPower'))
        what = 'healing per minute' if heal else 'barrier per activation' if bar else 'damage per 8 s trade' if dmg else 'its effect'
        acts = [f"{cls.replace('upgrade_', '')}|modifier|{cls.replace('upgrade_', '')}|1"] if item_targeting(n)['act'] not in ('PASSIVE', '') else []
        Lm, op = plugin_meta(R, st, w2['owned'], {}, purpose='measure one model input', acts=acts, readbacks=['items_ok|1|==|1'])
        def fit(*cs, lim=32): cs = [c for c in cs if c]; return next((c for c in cs if len(c) <= lim), cs[0])
        head = [f"# path-temporary input measurement generated by abtimeline.py --path temporary; candidate {n} at {at} souls", 'meta kind INTERACTION',
                f"meta question Measuring how much {what} {n} really gives {b['hero']} at {at} souls, to replace a modelled number.",
                f"meta purpose turn a MODELLED ESTIMATE in council/evidence/path/{b['id']}_temporary_{at}.txt into a CONTROLLED SANDBOX RESULT", f"meta mechanics " + ', '.join(f"{k}={v}" for k, v in s.items() if k != 'AbilityUnitTargetLimit')[:200],
                f"meta expectedstate souls={at} items={','.join(give)}", f"meta build {b['id']}", f"meta checkpoint {at}", f"meta items {' '.join(give)}",
                f"meta strategy_source council/evidence/path/{b['id']}_temporary_{at}.txt", f"meta feeds path temporary {b['id']} {n}",
                'meta selection_kind discovery', f"meta selection_reason {n} ranked in the top 3 of {b['id']}'s full catalog scan at {at} souls by modelled souls earned; its inputs are unmeasured",
                'meta alternative_reason none: this measures one input; the comparison is done by the model once the input is measured',
                f"meta cond_scope {'heal measurement' if heal else 'barrier measurement' if bar else 'gun-only damage'}", 'meta cond_abilities_used none', 'meta cond_abilities_excluded all',
                'meta cond_accuracy all shots on target', 'meta cond_misses none', 'meta cond_start_stacks n/a', f"meta cond_activations {n if acts else 'none'}", 'meta cond_distance 350u', 'meta cond_targets enemies=1 allies=0',
                f"meta readbacks equipped_items,ability_tiers{',activation:' + n if acts else ''}", f"meta measurement_requirement {'HP lost per trade needs real enemy damage (blocked); this run measures only the item side' if heal or bar else 'none'}",
                f"meta player_title {fit(f'How much does {n} give?', f'Measuring {n}', 'Measuring one item')}", f"meta player_what {fit(what.capitalize())}", f"meta player_why {fit('Replace a guess with a number')}",
                f"meta player_short {fit(f'{n} input', 'Input test', lim=26)}", f"meta player_expect {fit('One measured number')}", f"meta result_says the measured {what}; the path model is re-run with it and the verdict tier may move from MODEL-ONLY towards SUPPORTED"]
        proc = ['setup ' + b['hk'].replace('hero_', '').capitalize() + ' Haze', 'raw citadel_unlock_flex_slots', f"souls {at}", 'hardreset', f"souls {at}"] + [f"give {g}" for g in give] + ['basemods', 'enemies 1 300 4', 'fetch 350', 'cast reload 2.5']
        proc += (['lowhp 50', 'mark heal_60s', 'wait 30', 'healsum', 'lowhp 0'] if heal else ['mark barrier', 'cast i1 0.5', 'rb bar mod:' + cls.replace('upgrade_', '')] if bar else ['mark dmg_8s', 'fire 8']) + ['mark none', 'end']
        f = f"{od}/int_{b['id']}_path_{re.sub(r'\W+', '_', n)}_{at}.txt"; open(f, 'w').write('\n'.join(head + Lm + proc) + '\n'); out.append(os.path.relpath(f, SP))
    return out

# ======================================================================================================
# DECISION SELECTION (Kieran 15:46): pick the next unresolved build decision deterministically from existing outputs.
# score = impact x evidence_gap x testability (each 0..1, rules printed in the output); ties broken by name. No hero is preferred by name.
def select_decisions():
    D = []; rd = SP + '/council/sandbox/results'; measured = ' '.join(os.listdir(rd)).lower() if os.path.isdir(rd) else ''
    gap = lambda bid: 0.5 if bid.lower() in measured else 1.0
    measurable = lambda n: any(e in ('dmg', 'close', 'long', 'fr', 'clip', 'head', 'proc', 'oneshot', 'melee') for e, k, v in item_effects(n)) if item(n) else False
    # 1) blocked proposals (gate re-check outputs)
    for f in sorted(glob.glob(SP + '/council/work/strategy_tests/recheck/recheck_*.out')):
        t = open(f).read(); bid = (re.search(r'^BUILD (\S+)', t, re.M) or [None, '?'])[1]
        sp = re.findall(r'(gun|vitality|spirit) (\d+) -> (\d+)', (re.search(r'4\.8k spike timing \(([^)]*)\)', t) or [None, ''])[1])
        imp = min(1.0, sum(abs(int(a) - int(c)) for _, a, c in sp) / 20000 + 0.2)
        its = re.findall(r'INTERACTION BLOCK (.+)', t); tst = 1.0 if its and all(measurable(x.strip()) for x in its) else 0.6 if its else 0.3
        D.append(dict(src=os.path.relpath(f, SP), bid=bid, q=f"proposal {os.path.basename(f)[8:-4]}: change of purchase order/spike timing ({', '.join(f'{c} {a}->{d}' for c, a, d in sp) or 'order'})", imp=imp, gap=gap(bid), tst=tst,
                      why=f"blocked by STRATEGY/INTERACTION rules; items {its or 'none'}"))
    # 2) interaction files with an open verdict
    for f in sorted(glob.glob(SP + '/council/evidence/interaction/*.txt')):
        t = open(f).read(); bid = (re.search(r'^BUILD: (\S+)', t, re.M) or [None, '?'])[1]; itn = (re.search(r'^ITEM: (.+)$', t, re.M) or [None, '?'])[1]
        v = (re.search(r'^VERDICT: (.+)$', t, re.M) or [None, ''])[1]; unk = int((re.search(r'^UNKNOWN_CELLS: (\d+)', t, re.M) or [None, '0'])[1])
        if not (v.startswith('INSUFFICIENT') or v.startswith('DEPENDS')): continue
        ally = 'ally' in t and 'UNKNOWN' in t and re.search(r'ally.*UNKNOWN', t); tst = 0.2 if ally else 0.9 if unk else 0.5
        D.append(dict(src=os.path.relpath(f, SP), bid=bid, q=f"is {itn} the right purchase at its checkpoint in {bid}", imp=0.4, gap=gap(bid), tst=tst, why=f"verdict {v[:80]}; {unk} UNKNOWN cells"))
    # 3) weakness files whose winner is model-only
    for f in sorted(glob.glob(SP + '/council/evidence/weakness/*.txt')):
        t = open(f).read(); bid = (re.search(r'^BUILD: (\S+)', t, re.M) or [None, '?'])[1]; c = (re.search(r'^CONCLUSION: (.+)$', t, re.M) or [None, ''])[1]; w = (re.search(r'^WEAKNESS: (\S+)', t, re.M) or [None, ''])[1]
        if c.startswith('NO FIX'): continue
        D.append(dict(src=os.path.relpath(f, SP), bid=bid, q=f"how (or whether) to address {w} in {bid}", imp=0.6, gap=gap(bid), tst=0.8 if w == 'ammo' else 0.3, why=f"remedy set conclusion {c[:90]} (MODEL-ONLY)"))
    # 4) strategy sweep: builds whose path decision is undecided
    sw = SP + '/tmp_sweep/summary.txt'
    if os.path.exists(sw):
        for l in open(sw):
            bid, _, c = l.partition(' | ')
            if 'INSUFFICIENT' in c or 'DEPENDS' in c: D.append(dict(src='tmp_sweep/summary.txt', bid=bid.strip(), q=f"early purchase path of {bid.strip()}", imp=0.6, gap=gap(bid.strip()), tst=0.15, why=c.strip()[:80] + ' (needs lane economy / shoot-back data the sandbox lacks)'))
    for d in D: d['score'] = round(d['imp'] * d['gap'] * d['tst'], 3)
    D.sort(key=lambda d: (-d['score'], d['bid'], d['q']))
    return D
def decision_record(d, B, out_dir):
    """self-contained record for independent specialists: hero, checkpoint, current state, question, constraints, data paths. No candidates, no conclusions."""
    b = next(x for x in B if x['id'] == d['bid']); R = analyse(b); rows = [r for r in R['rows'] if not r.get('unknown')]
    src = open(SP + '/' + d['src']).read() if os.path.exists(SP + '/' + d['src']) else ''
    cp = int((re.search(r'^CHECKPOINT: (?:[\w-]+ at )?(\d+)', src, re.M) or [None, '12000'])[1]); ctx = ''
    pf = SP + '/council/proposals/' + os.path.basename(d['src'])[8:-4] + '.json' if 'recheck_' in d['src'] else None
    if pf and os.path.exists(pf):   # proposal: checkpoint = first purchase where the proposed core differs from data.js
        P_ = json.load(open(pf)); js = "const fs=require('fs');const o=new Function('return ('+fs.readFileSync(process.argv[1],'utf8').trim().replace(/[,;]\\s*$/,'')+')')();process.stdout.write(JSON.stringify(o))"
        nb = json.loads(subprocess.run(['node', '-e', js, SP + '/' + P_['buildFile']], capture_output=True, text=True, check=True).stdout)
        new = [x[0] for x in core_path(nb)]; old = [r['n'] for r in rows]; k = next((i for i, (x, y) in enumerate(zip(old, new)) if x != y), min(len(old), len(new)))
        cp = rows[k - 1]['souls'] if k else 0
        ctx = f"EXISTING INPUT (not a research candidate): blocked proposal {os.path.basename(pf)} diverges at purchase {k + 1}: data.js '{old[k] if k < len(old) else '-'}' vs proposal '{new[k] if k < len(new) else '-'}'; proposal ability order {''.join(map(str, nb['order']))}"
    prev = [r for r in rows if r['souls'] <= cp]; w = dict(prev[-1]) if prev else {'owned': [], 'imbues': {}, 'souls': cp, 'n': None, 'box': ''}
    st = state(R, dict(w, souls=cp)); T = st['tA']
    L = [f"DECISION RECORD {d['bid']} @ {cp} souls (generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})",
         f"QUESTION: {d['q']}. Decide what to buy, keep, sell or do instead at this checkpoint, including keeping the current build or buying nothing.",
         f"WHY THIS DECISION: selected by abtimeline.py --select-decision (score {d['score']} = impact {d['imp']} x evidence gap {d['gap']} x testability {d['tst']}); source {d['src']}",
         f"HERO: {b['hero']} ({b['hk']}); BUILD: {b['id']} '{b['name']}'; ability order {''.join(map(str, b['order']))}"] + ([ctx] if ctx else []) + [
         f"STATE AT CHECKPOINT (game progression model A, abtimeline.py): owned {w['owned']}; imbues {w['imbues']}; ability tiers " + ', '.join(f"{nm(R,s)} {tlabel(T[s])}" for s in (1, 2, 3, 4)) + f"; level {st['lv']}; weapon invest bonus {st['wb']}%; spirit power {st['sp']:.0f}",
         'FULL CORE PATH (data.js, read-only): ' + ' > '.join(f"{r['n']}@{r['souls']}" for r in rows),
         'CONSTRAINTS: data.js frozen (never edit/apply); 12 item slots; equal-soul comparison at the checkpoint; RULES_KIERAN.md and CHECKLIST.md are build rules (defaults, waivable only with computed evidence)',
         'GAME DATA: gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata, heroes.vdata (incl. m_mapScalingStats hero scalings, m_MapModCostBonuses investment tiers); audit/items_full_6819.json; localization gt/repo/game/citadel/resource/localization/',
         'SANDBOX: ops and meta fields in council/sandbox/AUTORUN.md and council/sandbox/SCHEMA.md (required_levels, required_activation, required_readback, levels_mode, rot, rl, rb); no shoot-back enemy, no allied bot, no NPC camps, artificial incoming damage does not trigger damage-taken effects',
         'EXCLUDED ON PURPOSE: the research side candidate list and conclusions (sealed: see CANDIDATES-SHA256 line; revealed after the blind lists are in)']
    os.makedirs(out_dir, exist_ok=True); f = f"{out_dir}/{d['bid']}_{cp}_record.txt"; open(f, 'w').write('\n'.join(L) + '\n')
    return f, b, cp, w
def select_main(a, B):
    D = select_decisions(); od = SP + '/council/evidence/decision'; os.makedirs(od, exist_ok=True)
    L = ['DECISION RANKING (abtimeline.py --select-decision): score = impact x evidence_gap x testability',
         'rules: impact = spike souls moved/20000+0.2 (proposals), 0.4 (one item), 0.6 (weakness / whole path); evidence_gap = 1.0 no sandbox result for the build, 0.5 some; testability = 1.0 if every changed item has a sandbox-measurable effect (damage/fire rate/clip/proc/stacks/melee), 0.9 open UNKNOWN cells, 0.8 ammo weakness, 0.6 mixed, 0.3 defensive/economy only, 0.2 needs allies, 0.15 needs lane economy']
    for i, d in enumerate(D[:20], 1): L.append(f"{i:>2}. {d['score']:.3f}  {d['bid']:<16} {d['q'][:90]}  [{d['why'][:110]}]  ({d['src']})")
    f = od + '/ranking.txt'; open(f, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:14])); print('wrote', f)
    rec, b, cp, w = decision_record(D[0], B, od); print('decision record', rec)
    return D[0], rec

# ---------------- ordinary builds vs allied composition (Kieran 16:15/16:20): options for MY hero only ----------------
# usage: python3 -I abtimeline.py --team <build id> --allies <hk,hk|SEED> [--at souls]
# Allies are context from game data (their weapon vs ability damage split). Ordinary teammate behaviour (attacking enemies, following up) is assumed
# at a stated shared-target share; no prearranged plan is assumed. Approaches come from catalog predicates, not from named items.
APPROACH = {'disruption': lambda s: any(k in s for k in ('SilenceDuration', 'StunDuration', 'FreezeDuration')) or ('SlowPercent' in s and 'AbilityCooldown' in s and 'AbilityCastRange' in s),
            'debuff for allies (bullet resist)': lambda s: any(k in s for k in ('BulletArmorReduction', 'BulletResistReduction')),
            'debuff for allies (spirit resist)': lambda s: any(k in s for k in ('TechArmorDamageReduction', 'MagicResistReduction')) and 'BulletArmorReduction' not in s,
            'debuff for allies (anti-heal)': lambda s: 'HealAmpReceivePenaltyPercent' in s and (num(s['HealAmpReceivePenaltyPercent']) or 0) < 0 and 'DeathImmunityDuration' not in s,
            'enemy damage reduction': lambda s: 'OutgoingDamagePenaltyPercent' in s and 'BonusGoldPerMinute' not in s}
def ally_profile(hk, sp=30.0):
    H = hero_info(hk); b = block('abilities.vdata', H['wpn']) or ''; g = lambda k, d=0.0: float((re.search(k + r' = ([0-9.\-]+)', b) or [None, d])[1])
    gun10 = g('m_flBulletDamage') * (g('m_iBullets', 1) or 1) / (g('m_flCycleTime', 1) or 1) * 10 * 0.55; sp10 = 0.0
    for s_ in (1, 2, 3):
        a = ability(H['ab'][s_]); P = at_tier(a, 1); cd = pv(P, 'AbilityCooldown') or 30
        sp10 += sum(v for k, (v, inst) in spirit_hits(P, sp).items() if inst) * (1 + int(10 / max(cd, 1)))
    tot = gun10 + sp10 or 1.0
    return dict(gun_share=gun10 / tot, spirit_share=sp10 / tot)
def team(b, allies, at=None, out=None, argv='', p_same=(0.3, 0.6)):
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in core_path(b)]); R['mob'] = mobility_slots(R)
    rows = [r for r in R['rows'] if not r.get('unknown')]; at = at or 12000; base_w = dict([r for r in rows if r['souls'] <= at][-1]); own = list(base_w['owned'])
    P = {k: v[0] for k, v in STRAT_P.items()}; e = enemy_at(at / P['E_SPM'], P, R['HB'])
    wD, stD = ia_state(R, base_w, at, None); tD = trade(seg_metrics(R, wD, stD), P, e)
    prof = {a: ally_profile(a) for a in allies}; ally_dps = P['E_D0'] * (1 + 0.3 * at / 10000); out_rows = []
    for apr, pred in APPROACH.items():
        best = None
        for n, g in items().items():
            if g.get('disabled') or n in own or not item(n) or g['tier'] > 3 or not pred((g69().get(n) or {}).get('stats', {})): continue
            rep = next((x for x in reversed(own) if item(x)['tier'] == item(n)['tier']), None)
            if not rep: continue
            wS, stS = ia_state(R, dict(base_w, owned=[x for x in own if x != rep]), at, n); tS = trade(seg_metrics(R, wS, stS), P, e); s = (g69().get(n) or {}).get('stats', {}); tg = {}
            for ps in p_same:
                g_ = 0.0
                for a, pf in prof.items():
                    if 'BulletArmorReduction' in s or 'BulletResistReduction' in s:
                        sh = -(sval(n, 'BulletArmorReduction') or sval(n, 'BulletResistReduction')) / 100; g_ += ally_dps * pf['gun_share'] * ((1 - (e['res'] - sh)) / (1 - e['res']) - 1) * ps
                    if 'TechArmorDamageReduction' in s or 'MagicResistReduction' in s:
                        sh = -(sval(n, 'TechArmorDamageReduction') or sval(n, 'MagicResistReduction')) / 100; g_ += ally_dps * pf['spirit_share'] * ((1 - (e['res'] - sh)) / (1 - e['res']) - 1) * ps
                    if 'HealAmpReceivePenaltyPercent' in s: g_ += ally_dps * 0.3 * (-sval(n, 'HealAmpReceivePenaltyPercent') / 100) * ps
                tg[ps] = g_
            my = (tS['tr'] / tD['tr'] - 1) * 100; team_pct = (tS['dps'] - tD['dps'] + sum(tg.values()) / len(tg)) / max(1, tD['dps'] + ally_dps * len(allies)) * 100
            if not best or team_pct > best[4]: best = (n, rep, my, tS['dps'] - tD['dps'], team_pct, tg)
        if best: out_rows.append((apr,) + best)
    o = ['SCOPE: build-context', 'KIND: team', f'BUILD: {b["id"]}', f'ALLIES: {allies}', f'CHECKPOINT: {at}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         'RULE: only MY purchases are optimised; allies are context; ordinary teammate behaviour (attacking the enemy I debuff) is assumed at a shared-target share of 0.3 / 0.6 (MODELLED ESTIMATE); no prearranged plan',
         'ALLY PROFILES (kit data, VERIFIED GAME MECHANIC inputs; split MODELLED at spirit 30, 55% hits): ' + '; '.join(f"{a}: gun {p['gun_share']*100:.0f}% / spirit {p['spirit_share']*100:.0f}%" for a, p in prof.items()),
         'MARGIN (pre-registered): an option is shown as an optional pivot only if team damage (mine + allies) rises >= 5% at the 0.3 share, or my trade ratio rises >= 5%']
    o.append('\n## OPTIONS FOR MY HERO (best catalog item per approach, replacing my newest same-tier item)')
    o.append('approach | item (replaces) | my trade ratio % | my dps change | ally dps added (share 0.3 / 0.6) | team damage % | result | tier')
    o.append('conventional (as built) | - | +0.0 | +0 | 0 / 0 | +0.0 | default | baseline')
    for apr, n, rep, my, ddps, tp, tg in sorted(out_rows, key=lambda r: -r[5]):
        ok = tp >= 5 or my >= 5
        tier = 'INSUFFICIENT (disruption value: denying enemy farm/picks has no model)' if apr == 'disruption' else 'MODEL-ONLY'
        o.append(f"{apr} | {n} ({rep}) | {my:+.1f} | {ddps:+.0f} | {tg[p_same[0]]:.0f} / {tg[p_same[1]]:.0f} | {tp:+.1f} | {'OPTIONAL PIVOT' if ok and apr != 'disruption' else 'default stays'} | {tier}")
    o.append('\n## UNKNOWN: how often allies hit my debuffed target (share ASSUMED), disruption value, team win effect; not measurable in the sandbox (no allied bots, no economy).')
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L)
    out = out or f"{SP}/council/evidence/team/{b['id']}_{'_'.join(a.replace('hero_', '') for a in allies)}_{at}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, out_rows
def team_main(a, B):
    b = next(x for x in B if x['id'] == a[1]); allies = a[a.index('--allies') + 1].split(','); at = int(a[a.index('--at') + 1]) if '--at' in a else None
    if allies == ['SEED']:   # arbitrary composition: two heroes from heroes.vdata picked by sha256 of the build id (chosen by nobody)
        hs = sorted(h for h in roster() if h != b['hk'] and hero_info(h)['ab'] and hero_info(h)['wpn']); hh = int(hashlib.sha256(b['id'].encode()).hexdigest(), 16); allies = [hs[hh % len(hs)], hs[(hh // 97) % len(hs)]]
    f, r = team(b, allies, at, None, ' '.join(a)); print('wrote', f, allies)

# ---------------- purchase timing (Kieran 16:22): value NOW vs later, delay alternative ----------------
# usage: python3 -I abtimeline.py --timing <build id|ALL>
# value_now = trade-ratio change from the item at its buy point (complete state, central parameters); value_later = the same at +8000 souls.
# weak-now = value_now < 2% while value_later >= value_now + 3 points and the item completes no 4.8k threshold at purchase. Delay alternative = the item moved
# two purchases later; both paths through the soul-income walk (central); MODELLED ESTIMATE throughout.
def timing(b):
    """PURCHASE-TIMING rule (Kieran 16:22): an item must give meaningful value NOW or serve a genuinely imminent spike. Future synergy alone is never enough.
    value now = trade-ratio gain of the complete build state at the buy point with vs without the item (MODELLED, central parameters); per-1000-souls value is compared with the
    build's own median (data-derived bar, not a fixed %). A purchase is a TIMING REVIEW when value-now per 1000 souls is below 25% of the build median AND it is not imminent:
    imminent = completes a 4.8k/6.4k colour threshold, or is a component of an upgrade bought within the next 2 purchases, or later value >= now + 3 points is NOT accepted as a reason."""
    R = analyse(b); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in core_path(b)]); R['mob'] = mobility_slots(R)
    rows = [r for r in R['rows'] if not r.get('unknown')]; P = {k: v[0] for k, v in STRAT_P.items()}; out = []
    def tr_with(w, souls, drop=None):
        w2 = dict(w, owned=[x for x in w['owned'] if x != drop] + ([c for c in item(drop)['components'] if drop] if drop and drop in w['owned'] else []), souls=souls)
        st = state(R, w2); return trade(seg_metrics(R, w2, st), P, enemy_at(souls / P['E_SPM'], P, R['HB']))['tr']
    sp = spikes(R); data = []
    for i, r in enumerate(rows):
        n = r['n']; prev = rows[i - 1]['owned'] if i else []
        net = SOULS[item(n)['tier']] - sum(SOULS[item(c)['tier']] for c in item(n)['components'] if c in prev)
        now = (tr_with(r, r['souls']) / tr_with(r, r['souls'], n) - 1) * 100
        later_rows = [x for x in rows if x['souls'] >= r['souls'] + 8000 and n in x['owned']]
        later = (tr_with(later_rows[0], later_rows[0]['souls']) / tr_with(later_rows[0], later_rows[0]['souls'], n) - 1) * 100 if later_rows else None
        thr = [c for c, d in sp.items() if d['4800'] == r['souls'] or d.get('6400') == r['souls']]
        nxt = [x['n'] for x in rows[i + 1:i + 3]]; imminent = [f"component of {z} bought within 2 purchases" for z in nxt if item(z) and n in item(z)['components']] + [f"completes the {c} colour threshold" for c in thr]
        mod = [x for x in mechanism_rows(n) if 'not used by the model' not in x[2]]
        data.append(dict(i=i, n=n, souls=r['souls'], net=net, now=now, later=later, imminent=imminent, nmod=len(mod), ntot=len(mechanism_rows(n)), r=r, prev=prev, later_souls=(later_rows[0]['souls'] if later_rows else None)))
    vals = sorted(d['now'] / max(1, d['net']) * 1000 for d in data if d['nmod'] and d['net'] > 0); med = vals[len(vals) // 2] if vals else 0.0
    for d in data:
        d['pk'] = d['now'] / max(1, d['net']) * 1000; d['med'] = med
        if d['i'] + 2 >= len(data) and not d['imminent']: pass
        if d['nmod'] and not d['imminent'] and d['pk'] < 0.25 * med and d['i'] + 2 < len(data):
            # what the same souls buy now (equal-or-lower cost, modelled unconditional stats), by trade-ratio gain at that state
            alts = []
            try:
                w0 = dict(d['r'], owned=list(d['prev']), souls=d['souls'])
                base_tr = tr_with(dict(d['r'], owned=list(d['prev'])), d['souls'])
                for c in wk_catalog(w0, lambda nn, ss: bool(item_effects(nn)) and SOULS[item(nn)['tier']] <= d['net'] and item_targeting(nn)['act'] in ('PASSIVE', ''), maxtier=item(d['n'])['tier']):
                    e = wk_eval(R, w0, d['souls'], add=(c,)); alts.append((e['tr'] / base_tr * 100 - 100, c, wk_cost(w0, c)))
                alts.sort(reverse=True)
            except Exception as ex: alts = []
            out.append(dict(build=b['id'], item=d['n'], souls=d['souls'], net=d['net'], now=d['now'], pk=d['pk'], med=med, later=d['later'], at_later=d['later_souls'], alts=alts[:3], modelled=f"{d['nmod']}/{d['ntot']}"))
    return out
def timing_main(a, B):
    sel = B if a[1] == 'ALL' else [x for x in B if x['id'] == a[1]]; F = []
    for b in sel:
        try: F += timing(b)
        except Exception as ex: print('skip', b['id'], ex)
    # delay alternative for the flagged items (path comparison through the walk, central parameters)
    for f in F:
        b = next(x for x in B if x['id'] == f['build']); p0 = core_path(b); j = next(i for i, x in enumerate(p0) if x[0] == f['item'])
        p1 = [list(x) for x in p0]; it = p1.pop(j); p1.insert(min(len(p1), j + 2), it)
        try:
            cells, P0 = path_eval(b, {'as built': p0, 'delayed 2 purchases': p1}, grid={}, T_END=25.0)
            c = cells[0][1]; f['d_souls20'] = S_at(c['delayed 2 purchases'], 20) - S_at(c['as built'], 20); f['d_tr'] = (c['delayed 2 purchases']['tr'] / c['as built']['tr'] - 1) * 100
        except Exception as ex: f['d_souls20'] = None; f['d_tr'] = None
    F.sort(key=lambda f: -((f['d_tr'] or 0)))
    o = ['KIND: timing', f'ARGS: {" ".join(a)}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         'RULE (Kieran 16:22): an item must give meaningful value NOW or serve a genuinely imminent spike; future synergy alone never justifies the purchase point.',
         'TEST: value now = trade-ratio gain of the whole build at the buy point with vs without the item (MODELLED ESTIMATE, central parameters). Weak-now = value per 1000 net souls below 25% of the build\'s own median over items with a modelled stat; EXEMPT if imminent (completes a 4.8k/6.4k threshold, or is a component of an upgrade within the next 2 purchases). Items with no modelled stat are skipped (not a finding either way).',
         'DELAY ALTERNATIVE: the item moved 2 purchases later through the soul-income walk (souls at 20 min, trade ratio over 1-20 min). Same-cost ALTERNATIVES NOW: unconditional catalog items with modelled stats at the same state, by trade-ratio gain.',
         'OUTPUT IS A REVIEW FLAG for the build browser / captions (council/captions reads this file), not a verdict: no build is changed; a change needs the gate. Tier of every number: MODELLED ESTIMATE; items\' stats are VERIFIED GAME MECHANIC.',
         'CAUTION: the trade model values cheap defensive/regen items very highly at every checkpoint (a known structural limit, see --strategy notes: the as-built path wins no grid cell in any of the 81 builds), so the alternatives column lists CANDIDATES to test, not recommended replacements; large gains there are model-driven.',
         'build | item | bought at | net cost | value now % | per 1000 souls | build median | value later % (at souls) | delay: d souls@20 | delay: d trade ratio % | same-cost alternatives now (trade-ratio gain %) | modelled stats | review']
    for f in F:
        rv = 'DELAY LOOKS BETTER (model)' if (f['d_tr'] or 0) > 1 else 'BUY-NOW HOLDS (model)' if (f['d_tr'] or 0) < -1 else 'NO CLEAR DIFFERENCE'
        gap_ = [x for x in (['range/radius not priced'] if any(e == 'range' for e, k, v in item_effects(f['item'])) else []) + (['CC-triggered barrier not priced'] if sraw(f['item'], 'VexBarrierCombatBarrier') else []) + (['imbue: value only on the imbued ability'] if REG.get(item(f['item'])['class']) == 'imbue' else [])]
        if gap_: rv = 'MODEL GAP (' + '; '.join(gap_) + ') - not a finding'
        al = '; '.join(f"{c} {g:+.1f}% ({cs})" for g, c, cs in f['alts']) or 'none modelled'
        lt = '' if f['later'] is None else f"{f['later']:+.1f} ({f['at_later']})"
        o.append(f"{f['build']} | {f['item']} | {f['souls']} | {f['net']} | {f['now']:+.1f} | {f['pk']:+.2f} | {f['med']:+.2f} | {lt} | {'' if f['d_souls20'] is None else f'{f["d_souls20"]:+.0f}'} | {'' if f['d_tr'] is None else f'{f["d_tr"]:+.1f}'} | {al} | {f['modelled']} | {rv}")
    out = SP + '/council/evidence/timing/' + ('ALL' if a[1] == 'ALL' else a[1]) + '.txt'; os.makedirs(os.path.dirname(out), exist_ok=True)
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L = txt.split('\n'); k = next(i for i, l in enumerate(L) if l.startswith('GENERATED:')); L.insert(k + 1, f'BODY-SHA: {sha}'); open(out, 'w').write('\n'.join(L))
    print('wrote', out, len(F), 'findings'); [print('  ', l) for l in o[6:18]]

# ---------------- purchase-path audit (Kieran 15:41-15:43): branch structure + computed checklist for every sale ----------------
# usage: python3 -I abtimeline.py --path <build> audit     |  --path ALL audit (read-only detectors, central parameters)
def fam_of(n):
    return sorted({FAMILY.get(c['cls'], c['cls']) for c in item_classes(n) if c['defining']}) if item(n) else []
def ammo_sim(R, owned, imbues, W):
    """bullets fired, reloads and dry time in a W s continuous-fire window for one complete state (gun_model; refill items used on their charge-up)."""
    w = {'n': None, 'souls': 0, 'owned': list(owned), 'imbues': dict(imbues), 'box': ''}; st = state(R, dict(w, souls=40000))
    act = [x for x in owned if not (item(x) and REG.get(item(x)['class']) == 'imbue' and x not in imbues)]
    out = {}
    for use in (1.0, 0.5):
        g = gun_model(R, st, act, dict(st['tA']), cdr_pct([dict(n=x) for x in owned]), W, use); ideal = W / g['cyc']
        out[use] = dict(bullets=g['bullets'], clip=g['clip'], dry=(1 - g['bullets'] / ideal) * 100, mags=g['bullets'] / max(1, g['clip']), dmg=g['dmg'], refills=g['n_refill'])
    return out
def path_audit(b, out=None, argv=''):
    R = analyse(b, None, STRAT_P['REFUND'][0]); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in core_path(b)]); R['mob'] = mobility_slots(R)
    rows = [r for r in R['rows'] if not r.get('unknown')]; BT = branch_types(b); later_all = [n for t, k, its, s in BT for n in its]
    P = {k: v[0] for k, v in STRAT_P.items()}; ref = STRAT_P['REFUND'][0]
    end = inv_walk(b, 'oldest-cheapest')[-1] if rows else None; end_owned = end['owned'] if end else []; end_souls = rows[-1]['souls'] if rows else 0
    imb_end = {n: s for n, s in (rows[-1]['imbues'] if rows else {}).items()}
    IMB = {x[0]: int(x[2]) for r_ in b['rows'] for box in r_ for x in box[3] if len(x) > 2 and str(x[2]).isdigit()}   # imbue slot written on ANY box (branches included)
    def tr_state(owned, souls, imbues=None):
        w = {'n': None, 'souls': souls, 'owned': list(owned), 'imbues': dict(imbues or {}), 'box': ''}; st = state(R, w); m = seg_metrics(R, w, st)
        return trade(m, P, enemy_at(souls / P['E_SPM'], P, R['HB'])), m
    def inv(L): return {c: sum(SOULS[item(o)['tier']] for o in L if colour_of(o) == c) for c in COLS.values()}
    tx = []
    # core sales (notes) and luxury/optional branch sales, each from the state where it happens
    for t, kind, its, sells in BT:
        for n, note in sells:
            m_ = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first)', note or '')
            if not m_: continue
            x = re.sub(r'\s*\(or ([^)]*)\)', r'|\1', m_.group(1)); xs = [y.strip() for y in x.split('|') if item(y.strip())]; x = xs[0] if xs else x
            alts_named = xs[1:]
            if kind.startswith('main'):
                r = next((r for r in rows if r['n'] == n), None); before = [o for o in (rows[rows.index(r) - 1]['owned'] if r and rows.index(r) else [])] + [n]
                souls = r['souls'] if r else 0
            else: before = list(end_owned) + [n]; souls = end_souls + SOULS[item(n)['tier']]
            if x not in before and alts_named and alts_named[0] in before: x = alts_named[0]
            tx.append(dict(branch=kind, box=t, buy=n, sell=x, before=before, souls=souls))
    o = ['SCOPE: build-context', 'KIND: path', 'MODE: audit', f'BUILD: {b["id"]}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f"COUNTING: REFUND {ref} of the price on sale ({PT[3]}); investment = full tier price of held items ({PT[3]}: counting rule not in data); state values = --strategy trade model ({PT[2]})"]
    o.append('\n## BRANCH STRUCTURE (data.js boxes; abtimeline walk() and the strategy walk use ONLY the main path; counters/luxury are branches evaluated one at a time)')
    for t, k, its, s in BT: o.append(f"  {t[:24]:<24} -> {k}: {', '.join(its)}")
    o.append('\n## SALE CHECKLIST (computed)')
    findings = []
    for T_ in tx:
        x, n = T_['sell'], T_['buy']; bef = [y for y in T_['before'] if y != n]
        imb_end_ = imb_end; imb_end = dict(imb_end_, **({n: IMB[n]} if n in IMB else {}))
        held = x in bef
        if not held:
            inmain = any(r['n'] == x for r in rows); why_ = ('dropped earlier by the walk\'s 12-slot policy (oldest-cheapest) or by an earlier sale note' if inmain else 'only bought in a conditional branch: the note applies only if that branch was taken (no issue)')
            o.append(f"- {T_['box']}: buy {n}, sell {x}: {x} is not held at that point in the walk - {why_}")
            if inmain: findings.append((b['id'], 'sale of an item already gone (slot policy or earlier sale)', n, x, 0))
            continue
        after = [y for y in T_['before'] if y != x]
        fut = [z for z in later_all if item(z) and x in item(z)['components'] and z != n]
        bought_at = next((r['souls'] for r in rows if r['n'] == x), None)
        dur = (T_['souls'] - bought_at) if bought_at is not None else None
        net = SOULS[item(x)['tier']] * (1 - ref)
        ib, ia = inv([y for y in bef]), inv(after)
        lost = [f"{c} 4.8k" for c in ib if ib[c] >= 4800 > ia[c]]
        fx, fn = fam_of(x), fam_of(n); lostf = [f for f in fx if f not in fn]
        t0, m0 = tr_state(bef + [n] if x not in bef else [y for y in bef if y != x] + [x, n], T_['souls'], imb_end)   # keep x AND buy n (slot permitting) - upper bound
        t1, m1 = tr_state(after, T_['souls'], imb_end)
        # best alternative sale: cheapest held item that is not a component of a later purchase and shares no family with n's missing roles
        is_act = lambda y: item_targeting(y)['act'] not in ('PASSIVE', '')
        alts = sorted([y for y in bef if y not in (x, n) and not is_act(y) and not any(item(z) and y in item(z)['components'] for z in later_all)], key=lambda y: (SOULS[item(y)['tier']], fam_of(y)))
        alt = alts[0] if alts else None
        ta, ma = tr_state([y for y in T_['before'] if y != alt], T_['souls'], imb_end) if alt else (None, None)
        L_ = [f"- {T_['box']} ({T_['branch'].split(' (')[0]}): buy {n}, sell {x}",
              f"    function of {x}: {', '.join(fx) or 'stats only'}; replacement {n}: {', '.join(fn) or 'stats only'}; roles lost: {', '.join(lostf) or 'none'}  [{PT[0]}]",
              f"    {x} is a component of later items: {', '.join(fut) or 'no'}" + (f" -> selling now and rebuying costs {SOULS[item(x)['tier']]} again later (net extra {SOULS[item(x)['tier']] - net:.0f} vs keeping, {PT[3]} refund)" if fut else ''),
              f"    held for {dur if dur is not None else '?'} souls of purchases; resale {SOULS[item(x)['tier']] * ref:.0f}, net cost of having owned it {net:.0f}",
              f"    investment before/after gun/vit/spirit {ib['gun']}/{ib['vitality']}/{ib['spirit']} -> {ia['gun']}/{ia['vitality']}/{ia['spirit']}; thresholds lost: {', '.join(lost) or 'none'}",
              f"    trade ratio after the sale {t1['tr']:.2f}" + (f"; selling {alt} instead: {ta['tr']:.2f} ({(ta['tr']/t1['tr']-1)*100:+.1f}%)" if alt else '') + f"  [{PT[2]}]"]
        if 'ammo' in fx or any(sraw(n, k) for k in ('AmmoReloadPercent', 'ActiveReloadPercent')):
            for lab, own_, imb_ in (('as instructed (sell ' + x + ')', after, imb_end), ('keep ' + x + ', sell ' + (alt or '-'), [y for y in T_['before'] if y != alt], imb_end), ('neither (keep ' + x + ', no ' + n + ')', bef, imb_end)):
                a20, a60 = ammo_sim(R, own_, imb_, 20), ammo_sim(R, own_, imb_, 60)
                L_.append(f"    ammo {lab}: 20 s {a20[0.5]['bullets']:.0f} bullets (clip {a20[0.5]['clip']:.0f}, {a20[0.5]['mags']:.1f} magazines, {a20[0.5]['dry']:.0f}% not firing; refill items used every other charge) | 60 s {a60[0.5]['bullets']:.0f} bullets, {a60[0.5]['dry']:.0f}% not firing | damage 60 s {a60[0.5]['dmg']:.0f}  [{PT[2]}; reload {weapon(R)['reload']}s {weapon(R)['reload_src'][:30]}]")
        unpriced = [y for y in (x,) if is_act(y)]; sat = alt and max(ta['tr'], t1['tr']) >= 19.9
        if unpriced: L_.append(f"    model limit: {x} has an active effect ({item_targeting(x)['act']}) the trade model does not price -> the alternative-sale comparison is not a finding")
        if sat: L_.append("    model limit: trade ratio saturates at the cap (20) in one state -> comparison not a finding")
        cls = ('component sold before its planned upgrade' if fut else '') or ('established 4.8k lost' if lost else '') or ('a cheaper non-component sale keeps more strength' if alt and not unpriced and not sat and ta['tr'] > t1['tr'] * 1.05 else '')
        L_.append(f"    review: {cls or 'no issue found by the computed checks'}; evidence tier: MODEL-ONLY (no measured inputs)")
        if cls: findings.append((b['id'], cls, n, x, (ta['tr'] / t1['tr'] - 1) * 100 if alt else 0))
        o += L_; imb_end = imb_end_
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L2 = txt.split('\n'); k = next(i for i, l in enumerate(L2) if l.startswith('GENERATED:')); L2.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L2)
    out = out or f"{SP}/council/evidence/path/{b['id']}_audit.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, findings


# ======================================================================================================
# P2 (new owner, 2026-10-24): whole-SEQUENCE audit of sales/upgrades, item roles, detectors for the gate.
#   python3 -I abtimeline.py --seq <build>            -> council/evidence/path/<build>_sequence.txt
#   python3 -I abtimeline.py --sales <build>          -> one JSON line (detectors used by gate.js rules INVESTMENT/SALES)
SEQ_GRID = {'hit': (0.35, 0.75), 'enemy': (0.6, 1.6), 'beta': (0.0, 0.5), 'POKE': (0.06, 0.2), 'lost': (0, 1)}
def _sell_target(note, held, path_names):
    m_ = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first)', note or '')
    if not m_: return None, []
    x = re.sub(r'\s*\(or ([^)]*)\)', r'|\1', m_.group(1)); xs = [y.strip() for y in x.split('|') if item(y.strip())]
    if not xs: return None, []
    pick = next((y for y in xs if y in held), None) or next((y for y in xs if y in path_names), None) or xs[0]
    return pick, [y for y in xs if y != pick]
def sale_tx(b):
    """every sale instruction in the build: main-path notes AND branch (counter/luxury/optional) notes, each from the state where it happens."""
    R = analyse(b, None, STRAT_P['REFUND'][0]); rows = [r for r in R['rows'] if not r.get('unknown')]; BT = branch_types(b); names = [r['n'] for r in rows]
    end = inv_walk(b, 'oldest-cheapest')[-1] if rows else None; end_owned = end['owned'] if end else []; end_souls = rows[-1]['souls'] if rows else 0
    tx = []
    for t, kind, its, sells in BT:
        for n, note in sells:
            main = kind.startswith('main'); r = next((r for r in rows if r['n'] == n), None) if main else None
            held = (rows[rows.index(r) - 1]['owned'] if r and rows.index(r) else []) + [n] if main else list(end_owned) + [n]
            x, alts_named = _sell_target(note, held, names)
            if not x: continue
            tx.append(dict(box=t, kind=kind, branch='main' if main else ('luxury' if 'luxury' in kind else 'counter' if 'counter' in kind else 'optional'), buy=n, sell=x, alts_named=alts_named,
                           before=held, souls=(r['souls'] if r else end_souls + SOULS[item(n)['tier']]), held=x in held, idx=(rows.index(r) if r else None)))
    return tx, rows, end_owned, end_souls
def item_roles(b):
    """three roles: temporary (bought to be sold), retained-or-upgraded, situational-luxury (only in a conditional branch). Derived from the sale notes and upgrade components."""
    tx, rows, end_owned, end_souls = sale_tx(b); path = [x[0] for x in core_path(b)]; BT = branch_types(b); later_all = [n for t, k, its, s in BT for n in its]
    sold_main = {t_['sell'] for t_ in tx if t_['branch'] == 'main'}; roles = {}
    for n in path:
        comp_of_later = [z for z in path[path.index(n) + 1:] if item(z) and n in item(z)['components']]
        if n in sold_main and not comp_of_later: roles[n] = 'temporary (bought to be sold)'
        elif n in sold_main: roles[n] = 'temporary but a component of ' + ','.join(comp_of_later) + ' (sale then rebuy)'
        elif comp_of_later: roles[n] = 'retained-or-upgraded (-> ' + ','.join(comp_of_later) + ')'
        else: roles[n] = 'retained'
    for t, k, its, s in BT:
        if not k.startswith('main'):
            for n in its: roles.setdefault(n, 'situational-luxury' if 'luxury' in k else 'conditional branch (' + k.split(' (')[0] + ')')
    return roles
def _sale_path(path0, buy, sell, mode, alt=None, branch='main', skip=None):
    p = [list(x) for x in path0]
    def strip(p_, who=None):
        out = []
        for x in p_:
            xx = list(x)
            if xx[1] and re.search(r'Sell ' + re.escape(who or sell), xx[1] or ''): xx[1] = re.sub(r'\s*Sell [^.]*?(?:for this|first)\.?', '', xx[1]).strip()
            out.append(xx)
        return out
    if mode == 'as built':
        return p + ([[buy, 'Sell ' + sell + ' for this.', None]] if branch != 'main' else [])
    if mode == 'keep':
        return strip(p) + ([[buy, '', None]] if branch != 'main' else [])
    if mode == 'sell other':
        q = strip(p)
        if branch == 'main':
            for x in q:
                if x[0] == buy: x[1] = ((x[1] + ' ') if x[1] else '') + 'Sell ' + alt + ' for this.'
            return q
        return q + [[buy, 'Sell ' + alt + ' for this.', None]]
    if mode == 'skip':
        q = [x for x in strip(p) if x[0] != sell]
        return q + ([[buy, '', None]] if branch != 'main' else [])
def _win_tr(res, t0):
    xs = [math.log(v) for tm, v in res['trs'] if tm >= max(1.0, t0)]
    return math.exp(sum(xs) / len(xs)) if xs else res['tr']
def _t_of(res, name):
    for n, s, t in res['buys']:
        if n == name: return t
    return None
def seq_audit(b, out=None, argv=''):
    tx, rows, end_owned, end_souls = sale_tx(b); roles = item_roles(b); path0 = core_path(b); ref = STRAT_P['REFUND'][0]; BT = branch_types(b); later_all = [n for t, k, its, s in BT for n in its]
    R = analyse(b, None, ref); R['HS'] = hero_stats(b['hk']); R['HB'] = HB_of(); R['melee_rel'] = melee_relevant(R, [x[0] for x in path0]); R['mob'] = mobility_slots(R)
    P = {k: v[0] for k, v in STRAT_P.items()}
    o = ['SCOPE: build-context', 'KIND: path', 'MODE: sequence', f'BUILD: {b["id"]}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f"COUNTING: resale {ref} of price ({PT[3]}); investment = full tier price of held items ({PT[3]}: counting rule not in data); slots capped at 12 only in the investment walk (sequence variants ignore the slot cap = upper bound for 'keep')",
         'METHOD: each sale instruction is evaluated as a whole progression through the --strategy soul-income walk: AS BUILT vs KEEP vs SELL-OTHER vs SKIP-THE-SOLD-ITEM; value = souls earned by the end of the window and the mean trade ratio from the time the sold item was first bought; grid = ' + str(SEQ_GRID) + ' (assumptions flip the verdict -> listed)',
         'TIERS: SUPPORTED = decisive inputs VERIFIED/measured; MODEL-ONLY = robust in >=80% of grid cells but model-derived; MODEL-ONLY, assumption-sensitive = flips with listed parameters; INSUFFICIENT = effect inside model noise. Whole-build values here are never above MODEL-ONLY (trade/income model has no measured inputs)']
    o.append('\n## ITEM ROLES (derived from sale notes, branch type and upgrade components)')
    for n, r_ in roles.items(): o.append(f"  {n}: {r_}")
    o.append('\n## BRANCH STRUCTURE')
    for t, k, its, s in BT: o.append(f"  {t[:26]:<26} -> {k}: {', '.join(its)}")
    findings = []; blocks = []
    for T_ in tx:
        x, n = T_['sell'], T_['buy']; br = T_['branch']
        bt_rows = [r for r in rows if r['n'] == x]; bought_at = bt_rows[0]['souls'] if bt_rows else None
        fut = [z for z in later_all if item(z) and x in item(z)['components'] and z != n]
        inmain = bool(bt_rows)
        hdr = f"\n## {x}: sold when buying {n} ({T_['box']}, {br})"
        if not T_['held'] and br == 'main':
            o += [hdr, f"  {x} is not held at that point in the walk (dropped earlier by an earlier sale note or by the 12-slot policy): redundant instruction", "  verdict: INSTRUCTION INCONSISTENT (data-derived, no model needed) [VERIFIED GAME MECHANIC: walk of the build's own boxes]"]
            findings.append(dict(build=b['id'], cls='sale of an item already gone', buy=n, sell=x, tier='VERIFIED (walk)')); continue
        if not inmain and br == 'main': continue
        if not inmain:
            o += [hdr, f"  {x} is not bought in the main path: the note applies only in the branch that bought it (no issue)"]; continue
        tot = sum(SOULS[item(r['n'])['tier']] for r in rows) + (SOULS[item(n)['tier']] if br != 'main' else 0)
        T_END = min(95.0, max(25.0, tot / P['E_SPM'] * 1.25))
        # alternative sale: cheapest held non-component, non-active item
        is_act = lambda y: item_targeting(y)['act'] not in ('PASSIVE', '')
        alts = sorted([y for y in T_['before'] if y not in (x, n) and not is_act(y) and not any(item(z) and y in item(z)['components'] for z in later_all) and [r_ for r_ in mechanism_rows(y) if 'not used by the model' not in r_[2]]], key=lambda y: (SOULS[item(y)['tier']], fam_of(y)))
        alt = alts[0] if alts else None   # only items whose stats the model prices can be compared as the sold item
        V = {'as built': _sale_path(path0, n, x, 'as built', branch=br), 'keep ' + x + (' (slot cap ignored)' if br != 'main' else ''): _sale_path(path0, n, x, 'keep', branch=br),
             'skip ' + x: _sale_path(path0, n, x, 'skip', branch=br)}
        if alt: V['sell ' + alt + ' instead'] = _sale_path(path0, n, x, 'sell other', alt=alt, branch=br)
        try: cells, P0 = path_eval(b, V, grid=SEQ_GRID, T_END=T_END, base_name='as built')
        except Exception as ex: o += [hdr, f'  sequence evaluation failed: {ex}']; continue
        cen = next(r for c, r in cells if c == 'central'); t_x = _t_of(cen['as built'], x) or 0.0; t_sale = _t_of(cen['as built'], n) or T_END
        net = SOULS[item(x)['tier']] * (1 - ref); hold_min = max(0.0, t_sale - t_x)
        ib = {c: sum(SOULS[item(o_)['tier']] for o_ in T_['before'] if colour_of(o_) == c) for c in COLS.values()}
        ia = {c: sum(SOULS[item(o_)['tier']] for o_ in T_['before'] if o_ != x and colour_of(o_) == c) for c in COLS.values()}
        # replacement keeps its colour investment only if the replacement belongs to the same colour
        ia2 = dict(ia); cn = colour_of(n)
        if cn in ia2 and br != 'main': ia2[cn] = ia2[cn]  # the new item counts in the 'after' totals below
        ia3 = {c: sum(SOULS[item(o_)['tier']] for o_ in ([y for y in T_['before'] if y != x] + ([] if n in T_['before'] else [n])) if colour_of(o_) == c) for c in COLS.values()}
        lost = [f"{c} {th}" for c in ib for th in (4800, 6400, 8000) if ib[c] >= th > ia3[c]]; gained = [f"{c} {th}" for c in ib for th in (4800, 6400, 8000) if ia3[c] >= th > ib[c]]
        o += [hdr, f"  role of {x}: {roles.get(x, '?')}; role of {n}: {roles.get(n, '?')}",
              f"  {x}: price {SOULS[item(x)['tier']]}, resale {SOULS[item(x)['tier']] * ref:.0f}, net cost of owning it {net:.0f} souls ({net / P['E_SPM']:.1f} min of reference income); first bought at {bought_at} souls (~{t_x:.1f} min), replaced at ~{t_sale:.1f} min -> owned ~{hold_min:.1f} min  [{PT[2]}]",
              f"  component of later purchases: {', '.join(fut) or 'none'}" + (f" -> selling and rebuying adds {SOULS[item(x)['tier']] * (1 - ref):.0f} souls vs keeping it in the upgrade ({PT[3]} resale)" if fut else ''),
              f"  investment gun/vit/spirit before {ib['gun']}/{ib['vitality']}/{ib['spirit']} -> after {ia3['gun']}/{ia3['vitality']}/{ia3['spirit']}; thresholds lost: {', '.join(lost) or 'none'}; gained: {', '.join(gained) or 'none'}  [{PT[3]}: counting rule]"]
        # ledger of variants (central) - souls earned and window trade ratio
        names = list(V); base = 'as built'
        o.append(f"  {'variant':<44}| souls at {T_END:.0f} min | window TR | key purchase times (min)")
        for nm_ in names:
            r_ = cen[nm_]; kt = ', '.join(f"{a} {t:.0f}" for a, s_, t in r_['buys'] if a in (x, n) and t is not None)
            o.append(f"  {nm_:<44}| {S_at(r_, 999):>14.0f} | {_win_tr(r_, t_x):>9.2f} | {kt}")
        cls_out = {}
        for nm_ in names[1:]:
            dS = [(c, S_at(r[nm_], 999) - S_at(r[base], 999)) for c, r in cells]; dT = [(c, (_win_tr(r[nm_], t_x) / _win_tr(r[base], t_x) - 1) * 100) for c, r in cells]
            mS, pS, nS, cS = verdict_class(dS, 'S', cells, 50.0); mT, pT, nT, cT = verdict_class(dT, 'tr', cells, 1.0)
            cls_out[nm_] = (mS, mT, pS, pT, nS, nT, cS, cT)
            o.append(f"  {nm_} vs as built: d souls {mS:+.0f}, d window TR {mT:+.1f}% | souls: {cS} | TR: {cT}")
        # classification of the instruction
        unmod = [e for e in (x, n) if not [r_ for r_ in mechanism_rows(e) if 'not used by the model' not in r_[2]]]
        better = [nm_ for nm_, v in cls_out.items() if v[2] >= 0.8 and v[3] >= 0.8 or (v[3] >= 0.8 and v[0] > -50) or (v[2] >= 0.8 and v[1] > -1)]
        if unmod and better: o.append(f"  note: the variants {better} differ from 'as built' only through items with no modelled stat ({', '.join(unmod)} contributes 0 here), so the apparent gain is an artefact of leaving them out: NOT a finding"); better = []
        worse = [nm_ for nm_, v in cls_out.items() if v[4] >= 0.8 or v[5] >= 0.8]
        issue = []
        if fut: issue.append('component sold before its planned upgrade')
        if lost: issue.append('established 4.8k lost')
        if br != 'main' and net > 0 and hold_min < 2 * net / P['E_SPM']: issue.append(f"briefly-held purchase: owned ~{hold_min:.1f} min for a net cost of {net:.0f} souls ({net / P['E_SPM']:.1f} min of reference income); review flag only")
        if better and not fut: issue.append('a computed alternative sequence is better: ' + '; '.join(better))
        # ammo mechanics (VERIFIED inputs) when the transaction touches ammo
        fx, fn = fam_of(x), fam_of(n)
        if 'ammo' in fx or 'ammo' in fn:
            wp = weapon(R); imbs = dict(rows[-1]['imbues']) if rows else {}
            IMB = {x_[0]: int(x_[2]) for r_ in b['rows'] for box in r_ for x_ in box[3] if len(x_) > 2 and str(x_[2]).isdigit()}
            for y_ in (n, x): 
                if y_ in IMB: imbs[y_] = IMB[y_]
            L_ = []; D20 = {}
            states_ = [('as built (sell ' + x + ')', [y for y in T_['before'] if y != x]), ('keep ' + x, list(T_['before'])), ('without ' + n + ' (keep ' + x + ')', [y for y in T_['before'] if y != n])]
            if alt: states_.append(('sell ' + alt + ' instead', [y for y in T_['before'] if y != alt]))
            for lab, own_ in states_:
                a8, a20 = ammo_sim(R, own_, imbs, 8), ammo_sim(R, own_, imbs, 20); D20[lab] = a20[0.5]['dmg']
                L_.append(f"    {lab}: 8 s trade {a8[0.5]['bullets']:.0f} bullets ({max(0, a8[0.5]['dry']):.0f}% not firing), 20 s {a20[0.5]['bullets']:.0f} bullets ({max(0, a20[0.5]['dry']):.0f}% not firing, {a20[0.5]['mags']:.1f} magazines), damage 20 s {a20[0.5]['dmg']:.0f}, refill uses {a20[0.5]['refills']:.1f}")
            ks_ = list(D20); loss = (1 - D20[ks_[0]] / D20[ks_[1]]) * 100 if D20[ks_[1]] else 0; gain_n = (D20[ks_[1]] / D20[ks_[2]] - 1) * 100 if D20[ks_[2]] else 0
            L_.append(f"    sustained 20 s gun damage: selling {x} costs {loss:.0f}% vs keeping it (both with {n}); {n} adds {gain_n:+.0f}% on top of {x}" + (f"; selling {alt} instead: {(D20[ks_[3]] / D20[ks_[1]] - 1) * 100:+.0f}% vs keeping all" if alt else '') + f"  [{PT[0]} clip/reload/cycle, {PT[2]} rotation]")
            if loss >= 5: issue.append(f"the sale of {x} lowers modelled sustained gun damage by {loss:.0f}% (ammo mechanics)"); ammo_loss = loss
            o += [f"  ammo mechanics (clip {wp['clip']:.0f}, reload {wp['reload']} s [{wp['reload_src'][:40]}], refill items on their cooldown; rotation/hit-rate share 0.5 of charges ASSUMED) [{PT[0]} inputs, {PT[2]} rotation]:"] + L_
        if is_act(x): o.append(f"  model limit: {x} has an active effect ({item_targeting(x)['act']}) that the trade model does not price: its own value is under-counted -> a 'keep' preference is not a finding")
        if is_act(n): o.append(f"  model limit: {n} has an active effect ({item_targeting(n)['act']}) not priced")
        if unmod: o.append(f"  model limit: no modelled stat for {', '.join(unmod)} (its contribution is 0 in the walk) -> not a finding for it")
        tier = ('INSUFFICIENT' if (not issue or all(i.startswith('briefly') for i in issue)) and not better else 'MODEL-ONLY')
        if fut or lost: tier = 'VERIFIED GAME MECHANIC (walk arithmetic) + MODEL-ONLY value'
        if any(is_act(e) or e in unmod for e in (x, n)) and not (fut or lost): tier = 'INSUFFICIENT (item effects not modelled)' if unmod else tier
        # recommendation (never applied; the gate is the only path)
        if issue and 'a computed alternative sequence is better' in ' '.join(issue): rec = 'CHANGE SUGGESTED (as a proposal through the gate): ' + '; '.join(better)
        elif fut: rec = f"REVIEW: keep {x} until the {','.join(fut)} upgrade unless the freed slot is needed earlier (quantified above); proposal needs the gate"
        elif tier.startswith('INSUFFICIENT'): rec = 'KEEP AS WRITTEN (no evidence to change); open question listed'
        else: rec = 'KEEP AS WRITTEN (as-built sequence is not beaten robustly by the alternatives)'
        if issue and any(i.startswith('the sale of') for i in issue) and not fut: rec = f"REVIEW: selling {x} costs sustained gun output; {n} does not replace its ammo role (quantified above). Alternatives for the slot: " + (f"sell {alt} (modelled)" if alt else "none with a modelled stat") + "; proposal needs the gate"; tier = 'MODEL-ONLY (ammo mechanics VERIFIED; rotation/hit share ASSUMED)'
        if any(i.startswith('briefly-held') for i in issue) and not fut and not tier.startswith('MODEL-ONLY (ammo'): rec = f"REVIEW (timing, insufficient evidence either way): {x} is owned ~{hold_min:.1f} min before {n} replaces it, for a net {net:.0f} souls; its value over that window is {'NOT PRICED by the model (' + x + ' has no modelled stat)' if x in unmod else 'priced above'}, so it cannot be called wasted or justified. Settle by measuring {x}'s contribution (queued interaction/path requests) or by deciding the branch ending is not reached; proposal needs the gate"
        flips = []
        for nm_, v in cls_out.items():
            if 'flips with' in v[6] or 'flips with' in v[7]: flips.append(nm_ + ': ' + (v[7] if 'flips with' in v[7] else v[6]))
        o += [f"  FINDINGS: {'; '.join(issue) or 'none'}", f"  VERDICT: {rec}; evidence tier: {tier}" + (f"; flipping assumptions: {' | '.join(flips)}" if flips else '')]
        if issue: findings.append(dict(build=b['id'], cls='; '.join(issue), buy=n, sell=x, tier=tier, rec=rec))
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L2 = txt.split('\n'); k = next(i for i, l in enumerate(L2) if l.startswith('GENERATED:')); L2.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L2)
    out = out or f"{SP}/council/evidence/path/{b['id']}_sequence.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, findings
def sales_json(b):
    """cheap detectors for the gate (no simulation): established 4.8k dropped in the investment walk; component sold before its planned upgrade; sale of an item already gone;
    briefly-held luxury is NOT computed here (needs the sequence run)."""
    tx, rows, end_owned, end_souls = sale_tx(b); BT = branch_types(b); later_all = [n for t, k, its, s in BT for n in its]; f = []
    for ev in inv_walk(b, 'oldest-cheapest'):
        for c in ev['drop']: f.append(dict(kind='4.8k drop', item=ev['n'], detail=f"{c} below 4800 after buying {ev['n']} (sold {','.join(ev['sold']) or 'none'})"))
    for T_ in tx:
        x, n = T_['sell'], T_['buy']
        if not T_['held'] and T_['branch'] == 'main': f.append(dict(kind='sale of item already gone', item=x, detail=f'{x} sold when buying {n} but not held'))
        elif T_['held']:
            fut = [z for z in later_all if item(z) and x in item(z)['components'] and z != n]
            if fut: f.append(dict(kind='component sold before planned upgrade', item=x, detail=f'{x} sold at {n}; component of {",".join(fut)}'))
            ib = {c: sum(SOULS[item(o_)['tier']] for o_ in T_['before'] if colour_of(o_) == c) for c in COLS.values()}
            ia = {c: sum(SOULS[item(o_)['tier']] for o_ in T_['before'] if o_ != x and colour_of(o_) == c) + (SOULS[item(n)['tier']] if colour_of(n) == c and n not in T_['before'] else 0) for c in COLS.values()}
            for c in ib:
                if ib[c] >= 4800 > ia[c]: f.append(dict(kind='4.8k drop', item=x, detail=f'{c} {ib[c]} -> {ia[c]} selling {x} for {n}'))
    for p in item_path_breaks(b): f.append(p)
    return f
def item_path_breaks(b):
    """broken upgrade path: an upgrade whose components are neither owned nor bought before it (full price paid) is fine; an upgrade bought while one of ITS components was sold earlier IS flagged; a core item bought twice is redundant."""
    out = []; seen = set()
    for x in core_path(b):
        if x[0] in seen: out.append(dict(kind='redundant purchase', item=x[0], detail=f'{x[0]} appears twice in the core path'))
        seen.add(x[0])
    return out

# ======================================================================================================
# P2: CONTRIBUTION PROFILE (Kieran 16:49). An item is judged by what it contributes across the match phases it actually affects, never by its best scenario alone.
#   python3 -I abtimeline.py --profile <build> [--out f]  -> council/evidence/profile/<build>.txt
# Value of X in this build = complete path AS BUILT minus complete path WITHOUT X (its souls flow to the following purchases): souls earned by phase (ledger: ONE owner per effect)
# and the mean trade ratio. Phases: lane = trooper income + lane trade advantage + forced recalls; farm = camps/waves (+Cultist-type bonus); fights = fight income + trade advantage + kills;
# survive = time dead. Combat strength lives only in the trade ratio, economy only in the ledger: nothing is added twice.
PHASES = {'lane': ('lane troopers (base)', 'lane: trade advantage', 'lane: forced recalls (HP budget)'), 'farm': ('camps/waves farmed', 'Cultist-type bonus souls'),
          'fights': ('fights/objectives (base)', 'fights: trade advantage', 'kills'), 'survive': ('time dead',)}
ASSUME_OF = {'close': ['close_u (share of damage inside the range)'], 'long': ['close_u (inverse share)'], 'bounce': ['p2hero (second hero found by a bounce)', 'N_NPC (NPCs per camp hit)'],
             'npc': ['N_NPC', 'F_LANE/F_MID (farming time share)', 'hscale (camp hp)', 'omega (clear speed -> income elasticity)'], 'econ': ['NPC_SOULS / uptime'], 'oneshot': ['ICD: one empowered shot per cooldown'],
             'proc': ['hit (accuracy)'], 'dmg': ['hit (accuracy)'], 'fr': ['hit (accuracy)'], 'ls': ['hit (accuracy)', 'POKE (damage taken)'], 'def': ['POKE/enemy (damage taken)'],
             'range': ['NOT MODELLED (ability range/radius)'], 'shred': ['enemy resists'], 'active': ['NOT MODELLED (active effect)'], 'head': ['head (headshot share)'], 'melee': ['melee_u'], 'sp': ['spirit scaling'], 'vel': ['NOT MODELLED'], 'clip': ['reload (VERIFIED m_reloadDuration)']}
ROUTE = {'dmg': ('lane', 'fights'), 'close': ('lane', 'fights'), 'long': ('lane', 'fights'), 'fr': ('lane', 'fights'), 'clip': ('lane', 'fights'), 'head': ('lane', 'fights'), 'proc': ('lane', 'fights'),
         'ls': ('lane', 'fights', 'survive'), 'shred': ('lane', 'fights'), 'sp': ('lane', 'fights'), 'melee': ('lane', 'fights'), 'vel': ('lane', 'fights'), 'npc': ('farm',), 'bounce': ('farm', 'fights'),
         'econ': ('farm',), 'def': ('lane', 'survive', 'fights'), 'active': ('lane', 'fights', 'survive'), 'range': ('fights',), 'oneshot': ('lane', 'fights')}
def relevance(b, names):
    """which activities matter for THIS hero/build, with the basis (derived, not scored for every activity)."""
    effs = {e for n in names for e, k, v in item_effects(n)}; R = analyse(b); out = {}
    out['lane'] = (True, f"every build starts in lane (lane ends at minute {STRAT_P['lane_end'][0]:g} in the walk)")
    fm = effs & {'npc', 'bounce', 'econ'}
    out['farm'] = (bool(fm), ('the build owns farm-affecting stats: ' + ', '.join(sorted(fm))) if fm else 'no item in the core path changes clearing or soul income; farm time share is a fixed parameter (F_LANE/F_MID), clear speed does not differ between variants except through damage stats')
    out['fights'] = (True, 'every build fights; fight income and kills come from the trade ratio')
    out['survive'] = (True, 'time dead and forced recalls cost income in every build')
    return out
def R0_wpn(b): return hero_info(b['hk'])['wpn']
def profile(b, out=None, argv=''):
    path0 = core_path(b); names = [x[0] for x in path0]; roles = item_roles(b)
    tot = sum(SOULS[item(n)['tier']] for n in names if item(n)); P = {k: v[0] for k, v in STRAT_P.items()}; T_END = min(95.0, max(25.0, tot / P['E_SPM'] * 1.1))
    V = {'as built': path0}
    for n in names:
        V['minus ' + n] = [[y[0], re.sub(r'\s*Sell ' + re.escape(n) + r'[^.]*?(?:for this|first)\.?', '', y[1] or '').strip(), y[2]] for y in path0 if y[0] != n]
    cells, P0 = path_eval(b, V, grid={}, T_END=T_END, base_name='as built'); cen = cells[0][1]; base = cen['as built']
    R = analyse(b, None, STRAT_P['REFUND'][0]); rows = [r for r in R['rows'] if not r.get('unknown')]
    o = ['SCOPE: build-context', 'KIND: profile', f'BUILD: {b["id"]}', f'HERO: {b["hero"]}', f'ARGS: {argv}', f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f'WINDOW: 0-{T_END:.0f} min of the soul-income walk, central parameters ({PT[2]}); value of X = AS BUILT minus WITHOUT X (X\'s souls flow to the following purchases, so this is the value of X net of its best in-path alternative use)',
         'PHASES: lane / farm / fights / survive are ledger groups (one owner per effect; ' + '; '.join(f"{k}: {', '.join(v)}" for k, v in PHASES.items()) + ')',
         'TIERS per cell: VERIFIED GAME MECHANIC (a stat the item has in game data) | CONTROLLED SANDBOX RESULT (none ingested for profiles yet) | MODELLED ESTIMATE (the number below) | ASSUMED (activation frequency parameters listed per item)',
         'DECISION USE: this is a contribution profile, not a verdict; an item with a low total can still be worth buying for a phase the model does not price (see NOT MODELLED), a high total never proves the item beats an unlisted alternative. Compare through --strategy/--path/--seq files.',
         'KNOWN MODEL LIMITS: camp respawn / wave spawn caps and contested lanes are NOT modelled (camps/min = share of time x (hp/clear speed + travel)); extra souls from faster clearing therefore appear only through F_LANE/F_MID, travel, hscale and the omega elasticity (omega=0 means saved seconds never become souls)']
    REL = relevance(b, names)
    o.append('\n## RELEVANCE (activities scored only where they matter for this hero/build; basis stated)')
    for k_, (yes, why) in REL.items(): o.append(f"  {k_}: {'RELEVANT' if yes else 'NOT RELEVANT (n/r)'} - {why}")
    o.append('MEASURED vs MODELLED: measured inputs ingested for this hero: ' + (json.dumps(measured_inputs().get(R0_wpn(b), {})) if measured_inputs().get(R0_wpn(b)) else 'none') + '. Every number in the table is a MODELLED ESTIMATE; "direct" = ledger effect in the phases the item\'s stats feed, "reallocation" = the remainder, caused by the following purchases arriving earlier (not a property of the item). VERIFIED stats are named in the stat columns.')
    o.append('\nitem | role | price | d souls lane | farm | fights | survive | d souls total | d window TR % | modelled stats | NOT MODELLED stats | activation assumptions (labelled)')
    rowsout = []
    for n in names:
        r_ = cen['minus ' + n]; led = ledger_delta(base, r_); ph = {k: sum(led.get(g, 0.0) for g in gs) for k, gs in PHASES.items()}
        dS = S_at(base, 999) - S_at(r_, 999); dT = (_win_tr(base, 1.0) / _win_tr(r_, 1.0) - 1) * 100
        mr = mechanism_rows(n); mod = [x[0].split(' = ')[0].split('.')[-1] for x in mr if 'not used by the model' not in x[2]]; unmod = [x[0].split(' = ')[0].split('.')[-1] for x in mr if 'not used by the model' in x[2]]
        eff = [e for e, k, v in item_effects(n)]; asm = []
        for e in eff:
            for a_ in ASSUME_OF.get(e, []):
                if a_ not in asm: asm.append(a_)
        if item_targeting(n)['act'] not in ('PASSIVE', ''): asm.append('active effect: cooldown/uptime not priced')
        rowsout.append((n, dS, dT))
        route = {p_ for e in eff for p_ in ROUTE.get(e, ())}; direct = sum(ph[p_] for p_ in route); realloc = dS - direct
        cell = lambda p_: (f"{ph[p_]:+.0f}" if p_ in route and REL[p_][0] else ('n/r' if not REL[p_][0] else 'via realloc'))
        o.append(f"{n} | {roles.get(n, '?').split(' (')[0]} | {SOULS[item(n)['tier']]} | {cell('lane')} | {cell('farm')} | {cell('fights')} | {cell('survive')} | direct {direct:+.0f} + reallocation {realloc:+.0f} = {dS:+.0f}{(' [LOW COVERAGE ' + str(len(mod)) + '/' + str(len(mod) + len(unmod)) + ' stats modelled: a negative value here is an under-count, not a finding]') if (len(mod) < len(unmod) and dS < 0) else ''} | {dT:+.1f} | {', '.join(mod) or '-'} | {', '.join(unmod) or '-'} | {'; '.join(asm) or '-'}")
    # ledger identity check (sum of phase deltas == total delta), per item
    bad = []
    for n in names:
        led = ledger_delta(base, cen['minus ' + n]); s1 = sum(led.values()); s2 = S_at(base, 999) - S_at(cen['minus ' + n], 999)
        if abs(s1 - s2) > 1.0: bad.append(f'{n}: parts {s1:+.1f} vs total {s2:+.1f}')
    o.append('\nLEDGER CHECK (phase deltas add up to the total souls difference for every item; no double counting): ' + ('OK for all ' + str(len(names)) + ' items' if not bad else 'MISMATCH ' + '; '.join(bad)))
    o.append('\n## READING GUIDE (items whose profile is dominated by one phase)')
    for n, dS, dT in sorted(rowsout, key=lambda x: -abs(x[1]))[:8]:
        led = ledger_delta(base, cen['minus ' + n]); ph = {k: sum(led.get(g, 0.0) for g in gs) for k, gs in PHASES.items()}; top = max(ph, key=lambda k: abs(ph[k]))
        o.append(f"  {n}: largest modelled effect is {top} ({ph[top]:+.0f} souls); total {dS:+.0f} souls, window trade ratio {dT:+.1f}%")
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L2 = txt.split('\n'); k = next(i for i, l in enumerate(L2) if l.startswith('GENERATED:')); L2.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L2)
    out = out or f"{SP}/council/evidence/profile/{b['id']}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, rowsout, bad

# ======================================================================================================
# P2: RANGE + MULTI-TARGET planner (Kieran f0e68e72, 4e2e797c, 16:49/16:55).
#   python3 -I abtimeline.py --range <build> [--at souls] [--item X]... [--vs Y]... [--queue]   -> council/evidence/range/<build>_<souls>.txt (+ scenario requests with --queue)
# Distances come from game data (weapon falloff, item range thresholds, ability ranges), never a fixed list. 1 m = 39.37 u (UNVERIFIED conversion; weapon falloff start 787 u = 20.0 m and end 1811 u = 46.0 m
# are round numbers in that unit, which supports it; the scenario requests read the achieved distance back).
U_M = 39.37
def weapon_ranges(R):
    b = block('abilities.vdata', R['H']['wpn']) or ''
    g = lambda k, d=None: (float(re.search(k + r' = ([0-9.\-]+)', b).group(1)) if re.search(k + r' = ([0-9.\-]+)', b) else d)
    return dict(f0=g('m_flDamageFalloffStartRange'), f1=g('m_flDamageFalloffEndRange'), s0=g('m_flDamageFalloffStartScale', 1.0), s1=g('m_flDamageFalloffEndScale'), speed=g('m_flBulletSpeed'), rng=g('m_flRange'), radius=g('m_flBulletRadius'))
def falloff_scale(W, d_u):
    if W['f0'] is None or W['f1'] is None or W['s1'] is None: return 1.0
    if d_u <= W['f0']: return W['s0']
    if d_u >= W['f1']: return W['s1']
    return W['s0'] + (W['s1'] - W['s0']) * (d_u - W['f0']) / (W['f1'] - W['f0'])   # linear; m_flDamageFalloffBias is ignored (MODELLED simplification)
def _m(v):
    x = num(v); return x
def item_range_thresholds(n):
    s = (g69().get(n) or {}).get('stats', {}); out = []
    if 'CloseRangeBonusDamageRange' in s: out.append(('close', _m(s['CloseRangeBonusDamageRange']), f"{n}: +{s.get('CloseRangeBonusWeaponPower')}% weapon damage within {s['CloseRangeBonusDamageRange']}"))
    if 'LongRangeBonusWeaponPowerMinRange' in s: out.append(('long', _m(s['LongRangeBonusWeaponPowerMinRange']), f"{n}: +{s.get('LongRangeBonusWeaponPower')}% weapon damage beyond {s['LongRangeBonusWeaponPowerMinRange']}"))
    return out
def item_area_radii(n):
    s = (g69().get(n) or {}).get('stats', {}); out = []
    for k, mode in (('RicochetRadius', 'radius-from-primary'), ('ChainRadius', 'chain'), ('AuraRadius', 'radius-from-source'), ('DebuffRadius', 'radius-from-primary'), ('ProcRadius', 'radius-from-primary'), ('ExplosionRadius', 'radius-from-primary'), ('Radius', 'radius-from-source'), ('HealRadius', 'radius-from-source')):
        if k in s and _m(s[k]): out.append((k, mode, _m(s[k])))
    return out
def ability_ranges(R, T):
    out = []
    for sl in (1, 2, 3, 4):
        t = T[sl]
        if t < 0: continue
        P = at_tier(R['abil'][sl], t)
        for k, p in P.items():
            if re.search(r'(Range|Radius|Distance)$', k) and not re.search(r'Multiplier|Scale|Visual|Bullet', k) and (p.get('v') or 0) > 0:
                if p.get('stype') in ('ETechRange', 'ETechRadius') or k in ('AbilityCastRange', 'Range', 'Radius'): out.append((sl, nm(R, sl), k, p['v']))
    return out
def ring_affected(n, rho, r, mode):
    """sandbox layout: main target + (n-1) others on a ring of radius rho around it (`enemies n rho`). Returns how many OTHERS the effect reaches."""
    if n <= 1: return 0
    k = n - 1
    if mode == 'radius-from-source': return k if rho <= r else 0   # aura centred on the player/main target
    if rho > r: return 0
    if mode == 'radius-from-primary': return k
    # chain: primary -> ring members; hop between neighbours on the ring = chord
    chord = 2 * rho * math.sin(math.pi / k) if k >= 2 else 0.0
    return k if (k == 1 or chord <= r) else 1
def range_plan(b, at=None, cands=(), vs=(), queue=False, out=None, argv=''):
    R = analyse(b); rows = [r for r in R['rows'] if not r.get('unknown')]; at = at or (rows[min(len(rows) - 1, len(rows) // 2)]['souls'] if rows else 0)
    pos = len([r for r in rows if r['souls'] <= at]); w = rows[pos - 1] if pos else rows[0]; owned = list(w['owned']); st = state(R, dict(w, souls=at)); T = dict(st['tA'])
    W = weapon_ranges(R); wp = weapon(R); items_ = list(dict.fromkeys(owned + list(cands) + list(vs)))
    D = []   # (metres, label, kind, source tier)
    def add(m_, lab, kind, tier): 
        if m_ and m_ > 0: D.append((round(m_, 1), lab, kind, tier))
    add(100 / U_M, 'contact / point blank (100 u)', 'melee', 'sandbox operator practice (100-150 u for melee), NOT game data: melee reach is verified by readback')
    add(150 / U_M, 'melee reach upper (150 u)', 'melee', 'sandbox operator practice, NOT game data')
    for n in items_:
        for kind, rm, lab in item_range_thresholds(n):
            if not rm: continue
            d = max(1.0, 0.1 * rm); add(rm - d, f'just inside {lab}', 'item threshold', PT[0]); add(rm + d, f'just outside {lab}', 'item threshold', PT[0])
    if W['f0']: add(W['f0'] / U_M - 1.0, f"just inside weapon falloff start ({W['f0']:.0f} u)", 'gun falloff', PT[0]); add(W['f0'] / U_M + 1.0, 'just beyond falloff start', 'gun falloff', PT[0])
    if W['f0'] and W['f1']: add((W['f0'] + W['f1']) / 2 / U_M, 'middle of the falloff band', 'gun falloff', PT[0]); add(W['f1'] / U_M, f"falloff end ({W['f1']:.0f} u, scale {W['s1']})", 'gun falloff', PT[0])
    for sl, nmx, k, v in ability_ranges(R, T):
        if v < 80: add(v, f'{nmx} {k}={v:g}', 'ability range', PT[0])
    D.sort(); merged = []
    for d in D:
        if merged and abs(d[0] - merged[-1][0]) < 0.75 and d[2] == merged[-1][2]: continue
        merged.append(d)
    # active-item table per distance
    thr = [(n,) + t for n in items_ for t in item_range_thresholds(n)]
    def mult(d_m, its):
        bonus = 0.0; act = []
        for n in its:
            s = (g69().get(n) or {}).get('stats', {})
            if 'BaseAttackDamagePercent' in s: bonus += (_m(s['BaseAttackDamagePercent']) or 0) / 100
            for kind, rm, lab in item_range_thresholds(n):
                v = (_m(s.get('CloseRangeBonusWeaponPower')) if kind == 'close' else _m(s.get('LongRangeBonusWeaponPower'))) or 0
                if (kind == 'close' and d_m <= rm) or (kind == 'long' and d_m >= rm): bonus += v / 100; act.append(n)
        return 1 + bonus, act
    base_set = [x for x in owned if x not in vs and x not in cands]; sets = {'owned (as built)': base_set}
    for c in list(cands) + list(vs): sets[f'+ {c}'] = base_set + [c]
    o = ['SCOPE: build-context', 'KIND: range', f'BUILD: {b["id"]}', f'HERO: {b["hero"]}', f'CHECKPOINT: {at} souls (state after {w["n"]}); owned {owned}', f'ARGS: {argv}',
         f'GENERATED: {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}', f'INPUT-SHA: {input_sha()}',
         f"UNIT: 1 m = {U_M} u ({PT[3]}; supported by round-number falloff 787 u = 20.0 m, 1811 u = 46.0 m)",
         f"WEAPON ({R['H']['wpn']}): falloff {W['f0']} u -> {W['f1']} u, scale {W['s0']} -> {W['s1']}, bullet speed {W['speed']} u/s, reload {wp['reload']} s [{PT[0]}]. Falloff curve between the ends is linear here (bias {PT[2]} simplification)",
         'WHAT IS MEASURED: nothing yet. RAW rows = game numbers multiplied out (VERIFIED inputs, MODELLED combination). PRACTICAL effectiveness (hit rate vs distance, reaching/holding the range, danger) is UNKNOWN: no data and no measurement, so it is shown as labelled SCENARIOS and sensitivity, with sandbox requests queued']
    o.append('\n## DISTANCE SET (from data; distances in m / u; kind; source tier)')
    for d in merged: o.append(f"  {d[0]:>5.1f} m  {d[0] * U_M:>5.0f} u  [{d[2]}] {d[1]}  <{d[3] if len(d[3]) < 60 else d[3][:57] + '...'}>")
    o.append('\n## RAW RELATIVE GUN DAMAGE PER BULLET HIT (falloff x weapon-% items active at that distance; MODELLED from VERIFIED stats; 1.00 = unmodified bullet at no falloff)')
    o.append('distance | falloff | flight time ms | ' + ' | '.join(sets) + ' | range items active (any set)')
    for d in merged:
        du = d[0] * U_M; fs_ = falloff_scale(W, du); ft = du / W['speed'] * 1000 if W['speed'] else 0
        vals = [mult(d[0], ss) for ss in sets.values()]
        o.append(f"{d[0]:>5.1f} m | {fs_:.2f} | {ft:.0f} | " + ' | '.join(f"{fs_ * v[0]:.3f}" for v in vals) + f" | {', '.join(sorted({x for v_ in vals for x in v_[1]})) or '-'}")
    # scenario distributions: bands derived from the data distances (labelled scenarios, NOT probabilities)
    close_r = [rm for n_, kind, rm, lab in thr if kind == 'close' and rm]; cr = min(close_r) if close_r else None
    fa0 = (W['f0'] or 0) / U_M; fa1 = (W['f1'] or 0) / U_M
    bands = {'brawl (all inside the closest item threshold / melee band)': (0.5, cr or 6.0), 'skirmish (between that threshold and the falloff start)': (cr or 6.0, fa0 or 20.0), 'poke (falloff band)': (fa0 or 20.0, fa1 or 46.0)}
    def band_val(its, lo, hi, N=40):
        xs = [lo + (hi - lo) * (i + .5) / N for i in range(N)]; return sum(falloff_scale(W, x * U_M) * mult(x, its)[0] for x in xs) / N
    o.append('\n## SCENARIO DISTRIBUTIONS (explicit labelled scenarios, uniform within each band; NOT measured frequencies, no probabilities claimed)')
    o.append('scenario | ' + ' | '.join(sets) + ' | best')
    scen = {}
    for lab, (lo, hi) in bands.items():
        v = [band_val(ss, lo, hi) for ss in sets.values()]; scen[lab] = v; o.append(f"{lab} {lo:.1f}-{hi:.1f} m | " + ' | '.join(f'{x:.3f}' for x in v) + f" | {list(sets)[v.index(max(v))]}")
    mixes = {'mix 70/25/5': (.7, .25, .05), 'mix 40/40/20': (.4, .4, .2), 'mix 15/45/40': (.15, .45, .4), 'mix 5/25/70': (.05, .25, .7)}
    ks = list(scen)
    for lab, wts in mixes.items():
        v = [sum(w_ * scen[k][i] for w_, k in zip(wts, ks)) for i in range(len(sets))]; o.append(f"{lab} (brawl/skirmish/poke shares) | " + ' | '.join(f'{x:.3f}' for x in v) + f" | {list(sets)[v.index(max(v))]}")
    # break-even: first set (index 1) against second (index 2) over brawl share, remainder skirmish/poke 50/50
    if len(sets) >= 3:
        names_ = list(sets); a, b2 = 1, 2; cross = None
        for pct in range(0, 101):
            p_ = pct / 100; va = p_ * scen[ks[0]][a] + (1 - p_) * (0.5 * scen[ks[1]][a] + 0.5 * scen[ks[2]][a]); vb = p_ * scen[ks[0]][b2] + (1 - p_) * (0.5 * scen[ks[1]][b2] + 0.5 * scen[ks[2]][b2])
            if va >= vb: cross = pct; break
        o.append(f"BREAK-EVEN: {names_[a]} out-damages {names_[b2]} per bullet hit once the brawl-band share is >= {cross}% (rest split evenly skirmish/poke); below that the other wins [RAW, hit rate equal at all ranges ASSUMED]" if cross is not None else f"BREAK-EVEN: {names_[a]} never beats {names_[b2]} in this model")
    # hit-rate sensitivity: practical value = raw x hit(d); hit(d) UNKNOWN -> three labelled shapes
    o.append('\n## PRACTICAL SENSITIVITY (hit rate vs distance is UNKNOWN; three labelled shapes, RAW value x hit(d); a ranking that survives all three does not depend on the unknown)')
    shapes = {'flat 1.0': lambda d: 1.0, 'mild (-1% per m)': lambda d: max(0.2, 1 - 0.01 * d), 'steep (-2.5% per m)': lambda d: max(0.2, 1 - 0.025 * d)}
    for sn, f in shapes.items():
        v = []
        for ss in sets.values():
            tot = 0
            for lab, wts in (('mix 40/40/20', mixes['mix 40/40/20']),):
                for (blab, (lo, hi)), w_ in zip(bands.items(), wts):
                    xs = [lo + (hi - lo) * (i + .5) / 40 for i in range(40)]; tot += w_ * sum(falloff_scale(W, x * U_M) * mult(x, ss)[0] * f(x) for x in xs) / 40
            v.append(tot)
        o.append(f"  {sn:<20} mix 40/40/20: " + ' | '.join(f"{list(sets)[i]} {x:.3f}" for i, x in enumerate(v)) + f" | best {list(sets)[v.index(max(v))]}")
    # multi-target layouts from item/ability radii
    o.append('\n## MULTI-TARGET LAYOUTS (ring geometry of `enemies n rho`: main target + n-1 others on a ring of radius rho; radii from item/ability data)')
    areas = [(n, k, mode, r, 0) for n in items_ for k, mode, r in item_area_radii(n)]
    for sl, nmx, k, v in ability_ranges(R, T):
        if 'Radius' in k: areas.append((f'{nmx} (ability {sl})', k, 'radius-from-source', v, sl))
    LAY = []
    if not areas: o.append('  (no owned/candidate item or ability has an area radius in data: single-target layouts only)')
    for n, k, mode, r, _sl in areas:
        o.append(f"  {n} {k}={r:g} m [{mode}] ({PT[0]})")
        for lab, f in (('tight', 0.4), ('medium (just inside)', 0.9), ('wide (just outside)', 1.3), ('spread (2x)', 2.0)):
            rho = f * r; row = [f"n={nn}: {ring_affected(nn, rho, r, mode)} of {nn - 1} others reached" for nn in (2, 3, 5)]
            o.append(f"    {lab:<22} rho {rho:5.1f} m ({rho * U_M:4.0f} u): " + '; '.join(row))
            LAY.append((n, k, mode, r, lab, rho))
    bnc = [n for n in items_ if any(e == 'bounce' for e, kk, v in item_effects(n))]
    for n in bnc:
        pct = sval(n, 'RicochetDamagePercent') or 0
        o.append(f"  total vs useful damage, {n} (bounce {pct:g}% of primary damage per extra target, MODELLED): " + '; '.join(f"{lab} n=5: total {1 + ring_affected(5, f * (dict((x[0], x[3]) for x in areas).get(n, 8)), dict((x[0], x[3]) for x in areas).get(n, 8), 'radius-from-primary') * pct / 100:.2f}x of primary, primary-target (kill-relevant) {1.0:.2f}x" for lab, f in (('tight', .4), ('wide', 1.3))))
    o.append('  RULE: secondary-target damage and debuff coverage are reported per target (primary / secondary / kills); a total across targets is never the headline; bounce and splash damage is counted once, on the target that receives it.')
    # requests
    reqs = []
    if queue: reqs = range_requests(b, R, at, w, owned, cands, vs, merged, W, LAY, areas, sets)
    o.append('\n## SANDBOX REQUESTS (planner fields: council/sandbox/PLANNER_FIELDS.md)' if reqs else '\n## SANDBOX REQUESTS: not generated (run with --queue)')
    o += ['  ' + x for x in reqs]
    o.append('\n## NOT DETERMINED: hit rate vs distance, strafing hit rate (no moving-target op in the runner: blocked_by estrafe), engagement-distance frequencies per hero, ability-range-limited reach; each shows as a labelled scenario or a queued request, never as a number')
    txt = '\n'.join(o) + '\n'; sha = body_sha(txt); L2 = txt.split('\n'); k = next(i for i, l in enumerate(L2) if l.startswith('GENERATED:')); L2.insert(k + 1, f'BODY-SHA: {sha}'); txt = '\n'.join(L2)
    out = out or f"{SP}/council/evidence/range/{b['id']}_{at}.txt"; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(txt)
    return out, merged, reqs
def range_requests(b, R, at, w, owned, cands, vs, merged, W, LAY, areas, sets):
    od = SP + '/council/sandbox/autorun/scenarios/range'; os.makedirs(od, exist_ok=True); out = []
    def cls(n): return item(n)['class']
    hero = b['hk'].replace('hero_', '').capitalize()
    def give(its): return [f"give {cls(x)}" for x in its if item(x)]
    base_set = [x for x in owned if x not in vs and x not in cands]
    # pick the distances: closest point blank, then just inside / outside of the first item threshold, falloff start, mid, end (<= 8 distinct)
    pick = []
    for d in merged:
        if d[2] in ('melee', 'item threshold', 'gun falloff') and d[0] not in [p[0] for p in pick]: pick.append(d)
    pick = pick[:9]
    arms = [('A', base_set + ([cands[0]] if cands else [])), ('B', base_set + ([vs[0]] if vs else []))] if (cands or vs) else [('A', base_set)]
    st = state(R, dict(w, souls=at)); T = dict(st['tA']); lv = ' '.join(str(max(0, T[s] + 1)) for s in (1, 2, 3, 4))
    def block_lines(tag, its, d_u, n=1, rho=300):
        return ['hardreset', f'souls {at}'] + give(its) + ['basemods', 'statecheck start_state', f'enemies {n} {rho:.0f} 3', f'fetch {d_u:.0f}', 'accuracy 1.0 0', 'cast reload 2.5', f'mark {tag}', 'fire 6', 'mark none', 'acclog', 'wait 2']
    def write(name, head, body):
        f = f"{od}/rng_{b['id']}_{name}.txt"; open(f, 'w').write('\n'.join(head + body + ['end']) + '\n'); out.append(os.path.relpath(f, SP))
    iv = list(dict.fromkeys([*owned, *cands, *vs])); itemclasses = ' '.join(cls(x) for x in iv if item(x))
    def head(kind_q, ranges, layout, extra=()):
        return [f"# range/multi-target request generated by abtimeline.py --range (planner fields: council/sandbox/PLANNER_FIELDS.md)", 'meta kind INTERACTION',
                f"meta question {kind_q}", f"meta purpose turn the RAW/PRACTICAL range or layout comparison in council/evidence/range/{b['id']}_{at}.txt from MODELLED to MEASURED", 'meta mechanics distance bands from weapon falloff and item thresholds; ring layouts from item radii',
                f"meta expectedstate souls={at} items={','.join(cls(x) for x in iv if item(x))}", f"meta build {b['id']}", f"meta checkpoint {at}", f"meta items {itemclasses}",
                f"meta strategy_source council/evidence/range/{b['id']}_{at}.txt", f"meta feeds range plan {b['id']}", 'meta selection_kind requested' if (cands or vs) else 'meta selection_kind discovery',
                f"meta selection_reason {'compare the candidate with the alternative across data-derived distances, enemy counts and spacings' if (cands or vs) else 'baseline range coverage for every build (no assumed fighting distance)'}; written before the run",
                'meta alternative_reason arm B = the equal-soul alternative named in the interaction file', 'meta cond_scope gun-only plus listed abilities per request', 'meta cond_abilities_used none', 'meta cond_abilities_excluded all except where stated', 'meta cond_accuracy 100% on target (stationary)',
                'meta cond_misses none', 'meta cond_start_stacks 0 (verify with statecheck before every block)', 'meta cond_activations range items at distances inside their threshold', f"meta cond_distance {ranges}", f"meta cond_targets {layout}",
                'meta readbacks equipped_items,ability_tiers,distance_m,enemy_positions,targets_hit,start_state', f"meta ranges {ranges}", f"meta layout {layout}", 'meta movement none (stationary)', 'meta required_start_state stacks=0 buffs=none cooldowns=ready ammo=full hp=full target_hp=keepalive',
                'meta aba A-B-A (baseline repeated after the alternative; invalid if the repeated baseline differs by more than the A/A noise floor)', 'meta order_alternation second repetition runs B first', 'meta invalid_if distance_m differs from the intended by >5% | hit count != fired | unexpected modifier present | start_state mismatch | item activation missing inside threshold',
                'meta result_says per distance and per target: damage per bullet hit, whether each range item activated; MEASURED replaces the MODELLED row only if A-B-A agrees',
                f"meta player_title {'Range check: ' + hero if len('Range check: ' + hero) <= 32 else 'Range check'}", 'meta player_what Same item at many distances', 'meta player_why No assumed fighting range', 'meta player_short Range sweep', 'meta player_expect Damage vs distance', *extra]
    # request 1: distance sweep, arms A-B-A
    body = []
    for rep, arr in (('1', arms + [arms[0]]), ('2', [arms[-1]] + arms[:1] + [arms[-1]] if len(arms) > 1 else arms)):
        for arm, its in arr:
            for d in pick:
                body += block_lines(f"{arm}_r{rep}_{d[0]:g}m", its, d[0] * U_M)
    write(f'distance_sweep_{at}', head(f"How does damage per bullet change with distance for {b['hero']} at {at} souls, inside and outside each range threshold?", ','.join(f"{d[0]:g}m" for d in pick), 'enemies=1 allies=0', ['meta blocked_by none']), body)
    # request 2: multi-target layouts for each area item
    seen = set()
    for n, k, mode, r, lab, rho in LAY:
        if (n, lab) in seen or n not in iv + [x for x in iv]: continue
        seen.add((n, lab))
    for n, k, mode, r, slot in sorted({(a[0], a[1], a[2], a[3], a[4]) for a in areas if a[0] in iv or a[4]}):
        body = []
        for rep in ('1', '2'):
            for lab, f in (('single', None), ('tight', 0.4), ('medium', 0.9), ('wide', 1.3), ('spread', 2.0)):
                for nn in ((1,) if f is None else (3, 5)):
                    for arm, its in (arms if rep == '1' else arms[::-1]):
                        rho_u = (f or 0.0) * r * U_M if f else 300
                        bl_ = block_lines(f"{arm}_r{rep}_{lab}_n{nn}", its, 350, n=nn, rho=rho_u)
                        if slot: bl_.insert(bl_.index('mark none'), f'cast {slot} 3')
                        body += bl_
        write(f"layout_{re.sub(r'\W+', '_', n)}_{at}", head(f"How many enemies does {n} really reach at tight, medium and wide spacing, and what happens to each target?", '350u', f"enemies=1,3,5 ring rho={0.4}r,{0.9}r,{1.3}r,{2.0}r of {r:g}m", ['meta metrics per_target_damage,targets_hit,secondary_damage,kills,debuff_coverage,healing', 'meta blocked_by none for stationary rings; moving targets: blocked_by estrafe (no runner op)']), body)
    # request 3: moving-target accuracy (declared blocked)
    write(f'moving_{at}', head(f"What hit rate and useful damage does {b['hero']} get on a strafing target at the same distances?", ','.join(f"{d[0]:g}m" for d in pick[:4]), 'enemies=1',
          ['meta movement strafe left-right period 1.5-3 s amplitude 3 m (controlled)', 'meta blocked_by estrafe (runner has no enemy-movement op; `move` steers only the player). Do NOT report expected damage as measured; report hits/fired']),
          [x for (arm, its) in (arms + [arms[0]]) for d in pick[:4] for x in block_lines(f"{arm}_strafe_{d[0]:g}m", its, d[0] * U_M)])
    return out

def main():
    a = sys.argv[1:]
    if a and a[0] == '--game-summary':
        f = a[1]; txt = open(f).read()
        if f.endswith('.json'):
            s = json.loads(txt); L = game_summary(s.get('question', ''), s.get('hypothesis', ''), s.get('alternatives', []), s.get('tradeoffs', []), s.get('missing_evidence', []), s.get('conclusion'))
        else: L = [l[len('GAME_SUMMARY: '):] for l in txt.split('\n') if l.startswith('GAME_SUMMARY: ')]
        print('\n'.join(L)); return
    B = load_builds()
    if '--build-file' in a:   # what-if / candidate build (JS or JSON object literal of the full build); replaces the build with the same id
        bf = a[a.index('--build-file') + 1]; a = [x for x in a if x not in ('--build-file', bf)]
        js = "const fs=require('fs');const o=new Function('return ('+fs.readFileSync(process.argv[1],'utf8').trim().replace(/[,;]\\s*$/,'')+')')();process.stdout.write(JSON.stringify({id:o.id,hero:o.hero,name:o.name,hk:o.hk,abil:o.abil,order:o.order,rows:o.rows}))"
        nb = json.loads(subprocess.run(['node', '-e', js, bf], capture_output=True, text=True, check=True).stdout)
        B = [nb if x['id'] == nb['id'] else x for x in B] + ([] if any(x['id'] == nb['id'] for x in B) else [nb])
    if a and a[0] == '--seq':
        for b in [x for x in B if x['id'] in a[1:]]:
            f, fi = seq_audit(b, None, ' '.join(a)); print('wrote', f); [print('  FINDING', x['cls'], '|', x['buy'], '/', x['sell'], '|', x['tier']) for x in fi]
        return
    if a and a[0] == '--sales':
        b = next(x for x in B if x['id'] == a[1]); print(json.dumps(sales_json(b))); return
    if a and a[0] == '--profile':
        for b in [x for x in B if x['id'] in a[1:]]:
            f, ro, bad = profile(b, None, ' '.join(a)); print('wrote', f, 'ledger mismatches:', len(bad))
        return
    if a and a[0] == '--range':
        b = next(x for x in B if x['id'] == a[1]); at = int(a[a.index('--at') + 1]) if '--at' in a else None
        cands = [a[i + 1] for i, x in enumerate(a) if x == '--item']; vs = [a[i + 1] for i, x in enumerate(a) if x == '--vs']
        f, mg, rq = range_plan(b, at, cands, vs, '--queue' in a, None, ' '.join(a)); print('wrote', f); [print('  request', x) for x in rq]; return
    if a and a[0] == '--strategy': return strategy_main(a, B)
    if a and a[0] == '--input-sha': print(input_sha()); return
    if a and a[0] == '--interactions': return interactions_main(a, B)
    if a and a[0] == '--weakness': return weakness_main(a, B)
    if a and a[0] == '--discover': return discover_main(a, B)
    if a and a[0] in ('--conditional', '--investment', '--situational'): return k1533_main(a, B)
    if a and a[0] == '--select-decision': select_main(a, B); return
    if a and a[0] == '--team': return team_main(a, B)
    if a and a[0] == '--timing': return timing_main(a, B)
    if a and a[0] == '--path' and a[2] == 'audit':
        sel = B if a[1] == 'ALL' else [x for x in B if x['id'] == a[1]]; F = []
        for b in sel:
            try: f, fi = path_audit(b, None, ' '.join(a)); F += fi
            except Exception as ex: print('skip', b['id'], ex)
        if a[1] != 'ALL': print('wrote', f)
        F.sort(key=lambda x: (x[1], -x[4])); out = SP + '/council/evidence/path/ALL_audit_findings.txt' if a[1] == 'ALL' else None
        if out: open(out, 'w').write('build | finding | bought | sold | trade-ratio gain of the alternative sale %\n' + '\n'.join(f"{x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]:+.1f}" for x in F) + '\n'); print('wrote', out, len(F), 'findings')
        for x in F[:25]: print('  ', x)
        return
    if a and a[0] == '--path' and a[2] == 'temporary':
        b = next(x for x in B if x['id'] == a[1]); at = int(a[a.index('--at') + 1]); tier = int(a[a.index('--tier') + 1]) if '--tier' in a else 1
        f, res, chk, reqs = path_temporary(b, at, tier, '--queue' in a, ' '.join(a)); print('wrote', f); [print('  ', r[0], f"d@20 {r[2]:+.0f}", r[4]) for r in res[:8]]; print('LEDGER CHECK', chk[:3]); [print('  request', x) for x in reqs]; return
    if a and a[0] == '--spikes':
        b = next(x for x in B if x['id'] == a[1]); R = analyse(b); print(json.dumps({c: d['4800'] for c, d in spikes(R).items()})); return
    if a and a[0] == '--verify-strategy':
        ok = verify_strategy(a[1]); print('BODY-SHA', 'OK' if ok else 'MISMATCH (edited after generation)'); sys.exit(0 if ok else 1)
    if a and a[0] == '--overlap':
        ids = [x for x in a[1:] if not x.startswith('--')]; res = [overlap_build(b) for b in B if not ids or b['id'] in ids]
        if '--json' in a: print(json.dumps(res, default=str))
        else:
            for r in res: print(fmt_overlap(r, '--only-flags' in a))
        return
    if a and a[0] == '--state':   # --state <build id> <souls> [compared item,item]: build state at a checkpoint for the scenario lint
        b = next(x for x in B if x['id'] == a[1]); souls = int(a[2]); cmp_ = [x for x in (a[3].split(',') if len(a) > 3 else []) if x]
        R = analyse(b); rows = [r for r in R['rows'] if not r.get('unknown') and r['souls'] <= souls]
        if not rows: print(json.dumps({'owned': [], 'imbues': {}, 'tiers': {}, 'relevant_actives': []})); return
        w = rows[-1]; T = tiers_at(R['evA'], souls); fam = lambda n: {FAMILY.get(c['cls'], c['cls']) for c in item_classes(n) if c['defining'] and c['cls'] in CAND_CLASSES}
        cf = set().union(*[fam(x) for x in cmp_]) if cmp_ else set(); rel = []
        for n in w['owned']:
            if n in cmp_: continue
            st = (g69().get(n) or {}).get('stats', {}); active = any(k in st for k in ('AbilityCooldown', 'AbilityChargeUpTime', 'ActiveReloadPercent', 'ActiveBonusFireRate'))
            if active and (fam(n) & cf or (item(n)['class'] in REG and REG[item(n)['class']] == 'imbue')): rel.append({'kind': 'item', 'name': n})
        for sl in (1, 2, 3, 4):
            if T[sl] >= 0 and {FAMILY.get(c['cls'], c['cls']) for c in ability_classes(R, sl, T[sl]) if c['cls'] in CAND_CLASSES} & cf: rel.append({'kind': 'ability', 'name': b['abil'][sl - 1], 'slot': sl})
        print(json.dumps({'owned': w['owned'], 'imbues': w['imbues'], 'tiers': {str(k): tlabel(v) for k, v in T.items()}, 'souls_of_last_purchase': w['souls'], 'relevant_actives': rel})); return
    if a and a[0] == '--context':
        bid, itn, outf = a[1], a[2], a[3]; bb = next(b for b in B if b['id'] == bid); r = overlap_build(bb); write_context(r, itn, outf, bid)
        try:   # item x kit interaction matrix for the same item (Kieran 14:29)
            f2, v2, rq = interactions(bb, itn, None, [], re.sub(r'\.txt$', '', outf) + '_interaction.txt', False, f'--interactions {bid} {itn}')
            open(outf, 'a').write(f"INTERACTION_FILE: {f2}\nINTERACTION_VERDICT: {v2}\n")
        except Exception as ex: open(outf, 'a').write(f"INTERACTION_FILE: none (error: {ex})\n")
        print('wrote', outf); return
    if a and a[0] == '--all':
        od = a[1]; os.makedirs(od, exist_ok=True); allr = []
        for b in B:
            R = analyse(b); txt, rows = fmt(R)
            open(f"{od}/{b['id']}.txt", 'w').write(txt + '\n')
            allr.append({'id': b['id'], 'hero': b['hero'], 'order': ''.join(map(str, b['order'])), 'evA': R['evA'], 'evB': R['evB'], 'rows': rows})
        json.dump(allr, open(f"{od}/_all.json", 'w'), default=str); print(len(allr), 'builds'); return
    if a and a[0] == '--gate':
        od = a[1] if len(a) > 1 and not a[1].startswith('-') and a[1] not in [x['id'] for x in B] else None
        ids = [x for x in a[1:] if x != od]; sel = [b for b in B if not ids or b['id'] in ids]; res = []
        for b in sel:
            g, txt = gate(b); res.append(g)
            if od: os.makedirs(od, exist_ok=True); json.dump(g, open(f"{od}/{b['id']}.json", 'w'), indent=1, default=str)
        print(json.dumps([{'id': g['id'], 'status': g['status'], 'errors': [(e['code'], e['item'], e['souls']) for e in g['errors']], 'warnings': len(g['warnings'])} for g in res]))
        sys.exit(1 if any(g['status'] == 'FAIL' for g in res) else 0)
    order = [int(c) for c in a[a.index('--order') + 1]] if '--order' in a else None
    b = next(x for x in B if x['id'] == a[0]); R = analyse(b, order); print(fmt(R)[0])

if __name__ == '__main__':
    main()

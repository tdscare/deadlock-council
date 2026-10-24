"""Incremental-value model. Uses the Council's own stylised trade model (council/tools/abtimeline.py, imported READ-ONLY via importlib)
so the baseline is the same ASSUMED/CALCULATED model the strategy planner uses. Nothing here is MEASURED.
Output is a CONVERSION DELTA (kill probability per won engagement, per the Council's p_kill = min(1, T_ESC/ttk)) plus a break-even landing frequency,
never an invented probability that the coordination succeeds."""
import os, sys, importlib.util, bisect, math
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
_abt = None
def abt():
    global _abt
    if _abt is None:
        spec = importlib.util.spec_from_file_location('abtimeline_ro', SP + '/council/tools/abtimeline.py')
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _abt = m
    return _abt

_builds = None
def builds():
    global _builds
    if _builds is None: _builds = {b['id']: b for b in abt().load_builds()}
    return _builds

def P_default(over=None):
    a = abt()
    P = {k: v[0] for k, v in a.STRAT_P.items()}; P['kappa'] = 1.0; P['_refc'] = [1.0] * 200
    if over: P.update(over)
    return P

CHECKPOINTS = (3000, 6000, 10000, 15000, 20000)

class CarryModel:
    def __init__(self, build_id, order=None, path=None):
        a = abt(); b = builds()[build_id]; self.b = b
        self.path = path or a.core_path(b)
        self.R = a.strat_R(b, self.path, order or b['order']); self.R['HB'] = a.HB_of()
        self.segs = a.segments(self.R); self.keys = [s for s, _, _ in self.segs]
    def seg(self, S):
        i = bisect.bisect_right(self.keys, S) - 1
        return self.segs[max(0, i)]
    def trade(self, S, P, enemy_souls=None):
        a = abt(); s, m, n = self.seg(S)
        tmin = (enemy_souls if enemy_souls is not None else S) / P['E_SPM']
        e = a.enemy_at(tmin, P, a.HB_of()); tr = a.trade(m, P, e)
        return m, e, tr
    def slot_of(self, cls):
        for sl, ab in self.R['abil'].items():
            if ab['cls'] == cls: return sl
        return None
    def payload(self, S, cls, prop, P):
        """spirit-scaled per-instance payload damage of ability cls.prop at soul total S (CALCULATED from vdata + the build's spirit/tier), or None."""
        a = abt(); sl = self.slot_of(cls)
        if sl is None or not prop: return None
        s, m, n = self.seg(S); T = m['T'][sl]
        if T < 0: return None
        Pa = a.at_tier(self.R['abil'][sl], T); p = Pa.get(prop) or {}
        if p.get('stype') in ('EWeaponPower', 'EWeaponDPS', 'EBaseWeaponDamageIncrease', 'ELightMeleeDamage', 'EHeavyMeleeDamage'): return None
        c = a.casts_per_trade(Pa, P['W'], P['I'])
        return dict(dmg=a.apv(Pa, prop, m['sp']), casts=c, tier=T, slot=sl, sp=m['sp'])
    def cost_slope(self, S, souls_cost, P):
        """seconds of time-to-kill lost if the NEXT souls_cost souls of purchases are not made (the build's own model): ttk(S) - ttk(S+cost)"""
        _, _, t0 = self.trade(S, P); _, _, t1 = self.trade(S + souls_cost, P, enemy_souls=S)
        return t0['ttk'] - t1['ttk'], t0['ttk'], t1['ttk']

def pk(ttk, P):
    return min(1.0, P['T_ESC'] / max(0.5, ttk))

def ttk_with(e, tr, extra_dmg, P, minus_dmg=0.0):
    dps = tr['dps'] + (extra_dmg - minus_dmg) * (1 - e['res']) / P['W']
    return e['ehp'] / max(1.0, dps)

HOLD_KINDS = ('cc_stun', 'cc_immobilize', 'cc_sleep')

def kill_value(t_min):
    """souls of a hero kill (Council model: KILL0 + 20/min). Economy rules (SECONDARY-WEB wiki): a 2-player kill pays 57% each (114% total) vs 125% for a lone killer."""
    P = P_default(); b = P['KILL0'] + 20 * t_min
    return dict(base=b, solo=1.25 * b, duo_total=1.14 * b, duo_each=0.57 * b)

def eval_payload_hold(cm, match, P, h_list=(0.3, 0.5, 0.7), S_list=CHECKPOINTS):
    """HOLD rule value. independent: payload lands with frequency h (unmeasured, swept); coordinated: lands with frequency rel*(hold lands).
    Returns rows per checkpoint with ttk, p_kill, delta. Sleep: carry's own fire during the hold is forgone (cost)."""
    n = match['need']; o = match['offer']; out = []
    for S in S_list:
        pl = cm.payload(S, n['ability'], n.get('dmg_prop'), P)
        if pl is None: out.append(dict(S=S, err='payload damage not computable (weapon-scaled / untrained / unknown property)')); continue
        m, e, tr = cm.trade(S, P)
        full = pl['dmg'] * pl['casts']
        rel = match.get('rel', 1.0); av = 1.0
        for h in h_list:
            # model baseline already counts the payload at 100% landing; scale it to h (independent) and to rel (coordinated)
            ind = ttk_with(e, tr, 0.0, P, minus_dmg=(1 - h) * full)
            forgo = (match.get('forgone_fire_s') or 0.0) * tr['dps'] if match.get('sleep') else 0.0
            co = ttk_with(e, tr, 0.0, P, minus_dmg=(1 - rel) * full + forgo / (1 - e['res']))
            pi, pc = pk(ind, P), pk(co, P)
            out.append(dict(S=S, h=h, ttk_ind=ind, ttk_co=co, p_ind=pi, p_co=pc, dp=pc - pi, payload=full, tier=pl['tier'], base_ttk=tr['ttk']))
    return out

def break_even_h(rows_S, thr):
    """largest independent landing frequency h at which coordination still improves kill conversion by >= thr (None if never)"""
    best = None
    for r in rows_S:
        if r.get('dp') is not None and r['dp'] >= thr: best = r['h'] if best is None else max(best, r['h'])
    return best

def eval_zone(cm, match, P, h_list=(0.3, 0.5, 0.7), S_list=CHECKPOINTS):
    """ZONE rule: carry zone DPS applies only while the enemy is inside. independent: fraction h of the zone duration spent inside (unmeasured, swept);
    coordinated: h + (1-h)*cover/T*rel where cover = seconds the partner keeps the enemy inside (slow: extra dwell gain)."""
    n = match['need']; o = match['offer']; out = []
    T = n.get('duration') or 0.0
    cover = match.get('hold') if match.get('hold') is not None else match.get('gain')
    for S in S_list:
        pl = cm.payload(S, n['ability'], n.get('dps_prop'), P)
        if pl is None: out.append(dict(S=S, err='zone DPS not computable (weapon-scaled / untrained)')); continue
        m, e, tr = cm.trade(S, P)
        full = pl['dmg'] * min(P['W'], T or P['W']) * pl['casts']
        rel = match.get('rel', 1.0) if match.get('rel') else 1.0
        for h in h_list:
            fr = min(1.0, h + (1 - h) * (cover or 0) / max(T, 1.0) * rel)
            ind = ttk_with(e, tr, 0.0, P, minus_dmg=(1 - h) * full)
            co = ttk_with(e, tr, 0.0, P, minus_dmg=(1 - fr) * full)
            pi, pc = pk(ind, P), pk(co, P)
            out.append(dict(S=S, h=h, ttk_ind=ind, ttk_co=co, p_ind=pi, p_co=pc, dp=pc - pi, payload=full, tier=pl['tier'], base_ttk=tr['ttk']))
    return out

def evaluate(cm, row, P):
    if row['rule'] == 'HOLD': return eval_payload_hold(cm, row['match'], P)
    if row['rule'] == 'ZONE': return eval_zone(cm, row['match'], P)
    return None

def summarise(rows, h=0.5):
    ok = [r for r in rows if 'dp' in r and r['h'] == h]
    if not ok: return None
    return dict(dp_mean=sum(r['dp'] for r in ok) / len(ok), dp_max=max(r['dp'] for r in ok), dp_min=min(r['dp'] for r in ok), n=len(ok))

def order_max_first(order, slot):
    """variant ability order: every pick of `slot` moved as early as possible; picks of the ultimate (slot 4) keep their positions (unlock timing is a game rule)."""
    n = len(order); new = [None] * n
    for i, s in enumerate(order):
        if s == 4: new[i] = 4
    rest = [s for s in order if s != 4]
    first = [s for s in rest if s == slot]; other = [s for s in rest if s != slot]
    seq = first + other
    j = 0
    for i in range(n):
        if new[i] is None: new[i] = seq[j]; j += 1
    return new

def eval_ub(cm, need, P, h_list=(0.3, 0.5, 0.7), S_list=CHECKPOINTS):
    """UPPER BOUND of the coordination value if the interaction works perfectly (landing 100%, partner always available): the damage of the needed ability becomes certain.
    Used to PRUNE unproven ideas: if even this is below the bar the idea is rejected without any test."""
    out = []
    prop = need.get('dps_prop') or need.get('dmg_prop')
    T = need.get('duration') or need.get('channel') or 1.0
    for S in S_list:
        pl = cm.payload(S, need['ability'], prop, P)
        if pl is None: out.append(dict(S=S, err='ability damage not computable (weapon-scaled/untrained)')); continue
        m, e, tr = cm.trade(S, P)
        dpsprop = bool(need.get('dps_prop')) and prop == need.get('dps_prop')
        full = pl['dmg'] * (min(P['W'], T) if dpsprop else 1.0) * pl['casts']
        for h in h_list:
            ind = ttk_with(e, tr, 0.0, P, minus_dmg=(1 - h) * full)
            co = ttk_with(e, tr, 0.0, P, minus_dmg=0.0)
            pi, pc = pk(ind, P), pk(co, P)
            out.append(dict(S=S, h=h, ttk_ind=ind, ttk_co=co, p_ind=pi, p_co=pc, dp=pc - pi, payload=full, tier=pl['tier'], base_ttk=tr['ttk']))
    return out

def item_dps_profile(cls, sp):
    """(dps0, inc, dpsmax, radius, duration, shred_pct, cd) of a zone item at spirit sp (base tier; vdata + spirit scale)"""
    a = abt(); P = a.at_tier(a.ability(cls), 0)
    g = lambda k: a.apv(P, k, sp)
    return dict(dps0=g('DPS'), inc=g('DPSIncrease'), dpsmax=g('DPSMax') or g('DPS'), radius=a.pv(P, 'Radius'), dur=a.pv(P, 'AbilityDuration'), shred=-g('BulletArmorReduction'), cd=a.pv(P, 'AbilityCooldown'))

def zone_damage(pr, dwell):
    """integral of min(dpsmax, dps0 + inc*t) over [0, dwell]; DPSIncrease taken as per second (UNVERIFIED unit)"""
    if dwell <= 0: return 0.0
    if pr['inc'] <= 0: return pr['dps0'] * dwell
    t_cap = max(0.0, (pr['dpsmax'] - pr['dps0']) / pr['inc'])
    if dwell <= t_cap: return pr['dps0'] * dwell + 0.5 * pr['inc'] * dwell ** 2
    return pr['dps0'] * t_cap + 0.5 * pr['inc'] * t_cap ** 2 + pr['dpsmax'] * (dwell - t_cap)

def eval_item_zone(cm, cls, cost, cover_s, rel, P, h_list=(0.3, 0.5, 0.7), S_list=CHECKPOINTS):
    """a ground-zone item bought by the carry. independent: fraction h of the item's duration inside; coordinated: partner keeps the enemy inside for `cover_s` extra seconds (x rel).
    compared with the best alternative use of the same souls: the build's own next purchases (ttk at S+cost)."""
    out = []
    for S in S_list:
        m, e, tr = cm.trade(S, P); _, _, trN = cm.trade(S + cost, P, enemy_souls=S)
        pr = item_dps_profile(cls, m['sp']); T = pr['dur'] or 5.0
        per_cd = min(1.0, (P['W'] + P['I']) / (pr['cd'] or 30.0))       # uses within a trade
        base_dps = tr['dps']; gun = tr['gun']
        def with_dwell(dw):
            dmg = zone_damage(pr, dw) * (1 - e['res']) * per_cd
            shred_gain = gun * ((1 - (e['res'] - pr['shred'] / 100.0)) / (1 - e['res']) - 1.0) * (1 - e['res']) * (dw / P['W']) * per_cd if pr['shred'] else 0.0
            return (dmg + shred_gain * P['W']) / P['W']      # extra dps over the window
        p_alt = pk(e['ehp'] / max(1.0, trN['dps']), P)
        for h in h_list:
            ind = pk(e['ehp'] / max(1.0, base_dps + with_dwell(h * T)), P)
            co = pk(e['ehp'] / max(1.0, base_dps + with_dwell(min(T, h * T + (1 - h) * cover_s * rel))), P)
            best_wo = max(p_alt, ind, pk(e['ehp'] / max(1.0, base_dps), P))
            out.append(dict(S=S, h=h, p_ind=best_wo, p_co=co, dp=co - best_wo, p_item_ind=ind, p_alt=p_alt, item_dps_ind=with_dwell(h * T), item_dps_co=with_dwell(min(T, h * T + (1 - h) * cover_s * rel)), tier=0))
    return out

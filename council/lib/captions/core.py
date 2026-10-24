"""CAPTION CORE (council/lib/captions/core.py): progression reconstruction, claim generators, claim verifier, caption composer, linter.
READ-ONLY with respect to data.js and to other agents' files (imports abtimeline as a library, reads effects json).
Evidence tiers: VERIFIED DATA (value/structure read from game files, or arithmetic over such values with no behavioural assumption)
                MEASURED (sandbox result; none exist yet -> never produced here)
                MODELLED (depends on a model/assumption, e.g. which point-model is right, hit rates) -> REVIEW only
                UNVERIFIED (hypothesis / legacy note text) -> REVIEW only
Temporal rule: a tier/unlock claim is VERIFIED only if BOTH ability-point models (A = data, B = old audit) agree at that purchase."""
import os, re, sys, json, hashlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(SP, 'council', 'tools'))
import abtimeline as A

EFFECTS = os.path.join(SP, 'council', 'evidence', 'interactions', 'effects')
MECH = os.path.join(SP, 'council', 'evidence', 'interactions', 'validated', 'mechanics_verified.json')
SOULS = A.SOULS
COLN = {'WeaponMod': 'weapon', 'Armor': 'vitality', 'Tech': 'spirit'}
IMMINENT_SOULS = 3000      # openly stated threshold: enabling event within 3,000 souls (~3 min at the council reference 1,000 souls/min, STRAT_P E_SPM, ASSUMED)
IMMINENT_PURCHASES = 3     # and within 3 purchases
SPM = 1000.0
CORE_BOX = re.compile(r'^(Early|Mid|Late)')
V, M, MOD, UNV = 'VERIFIED DATA', 'MEASURED', 'MODELLED', 'UNVERIFIED'
PUBLISHABLE = (V, M)

BANNED = [r'great synergy', r'\bmore damage\b', r'very strong', r'helps? you survive', r'\bgood item\b', r'\bpowerful\b', r'\bstrong\b', r'\bsolid\b',
          r'\bamazing\b', r'\bessential\b', r'must[- ]buy', r'\bdeals? more\b', r'\bboosts? your\b', r'increases? your (spirit|weapon|damage)', r'\bsynergi[sz]es? well\b', r'\bgreat\b']
FUTURE_MARK = re.compile(r'^(From |After |Once |Later|Becomes |Pays off |Builds toward |Upgrade path)')

_cache = {}
def builds():
    if 'B' not in _cache:
        _cache['B'] = {b['id']: b for b in A.load_builds()}
    return _cache['B']

def data_sha():
    return hashlib.sha256(open(os.path.join(SP, 'data.js'), 'rb').read()).hexdigest()[:16]

def legacy_notes(bid):
    """item notes / box descs exactly as in data.js (read-only)."""
    out = {}
    for r in builds()[bid]['rows']:
        for bx in r:
            for it in bx[3]:
                out[(bx[0], it[0])] = it[1] if len(it) > 1 else ''
    return out

# ---------------------------------------------------------------- hero invest tables (units: weapon = % weapon damage, spirit = spirit power, vitality = hero bonus value)
def bonus_table(hk, slot):
    def tab(bb):
        k = bb.find('m_MapModCostBonuses')
        if k < 0: return None
        j = bb.find('EItemSlotType_' + slot + ' = ', k)
        if j < 0: return None
        seg = bb[j:bb.find(']', j)]
        return [(int(a), float(c)) for a, c in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)', seg)]
    return tab(A.block('heroes.vdata', hk) or '') or tab(A.block('heroes.vdata', 'hero_base') or '')
def bonus_at(tab, inv):
    return max([b for th, b in tab if inv >= th] or [0.0])

# ---------------------------------------------------------------- progression
def progression(bid):
    """-> dict(R, pts, core, noncore). pts = ordered core purchase points with state; each has idx, prev_own, inv_before/after per colour."""
    if ('P', bid) in _cache: return _cache[('P', bid)]
    b = builds()[bid]
    R = A.analyse(b)
    rows = [r for r in R['rows'] if not r.get('unknown')]
    prev_own = []
    for i, r in enumerate(rows):
        r['idx'] = i
        r['prev_own'] = list(prev_own)
        pi = [A.item(o) for o in prev_own]
        r['inv_before'] = {c: sum(SOULS[x['tier']] for x in pi if x['slot'] == s) for s, c in COLN.items()}
        r['inv_after'] = {c: sum(SOULS[x['tier']] for x in r['own'] if x['slot'] == s) for s, c in COLN.items()}
        prev_own = list(r['owned'])
    sold_for = {}; self_sell = {}
    for r_ in b['rows']:
        for bx in r_:
            for it_ in bx[3]:
                note = it_[1] if len(it_) > 1 else ''
                for m in re.finditer(r'Sell ([A-Z][^.]*?) (?:for this|first)', note or ''):
                    sold_for.setdefault(m.group(1), []).append((it_[0], bx[0]))
                m = re.match(r'^Sell it (once [^.]*|for [^.]*)\.', note or '')
                if m: self_sell[it_[0]] = m.group(1)
    P = dict(R=R, pts=rows, b=b, sold_for=sold_for, self_sell=self_sell)
    _cache[('P', bid)] = P
    return P

def tmin(w, slot):
    return min(w['tA'][slot], w['tB'][slot])
def tmax(w, slot):
    return max(w['tA'][slot], w['tB'][slot])
def agree(w, slot):
    return w['tA'][slot] == w['tB'][slot]

def swap_sold(note):
    """item(s) the build says to sell for this one (data.js note text): 'Sell X for this', 'instead of X'"""
    m = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first)', note or '') or re.search(r'[Ii]nstead of ([A-Z][^.]*?)(?: when|\.|,|$)', note or '')
    return m.group(1) if m else None

def noncore_point(P, name, imb, box, note=''):
    """state for a situational/luxury item: bought once the 12-slot core is complete. The slot it takes is known only when the build note names the item sold;
    otherwise inventory-dependent claims (spikes) are suppressed (w['swap_unknown'])."""
    R = P['R']; last = P['pts'][-1]
    sold = swap_sold(note)
    base = list(last['owned'])
    unknown = False
    if sold and sold in base: base.remove(sold)
    elif len(base) >= 12: unknown = True
    owned = base + [name]
    imbues = {k: v for k, v in last['imbues'].items() if k in base}
    if imb and str(imb).isdigit(): imbues[name] = int(imb)
    w = dict(n=name, souls=last['souls'], owned=owned, imb=int(imb) if imb and str(imb).isdigit() else None, imbues=imbues, box=box)
    st = A.state(R, w)
    st['idx'] = len(P['pts']); st['prev_own'] = list(last['owned'])
    st['inv_before'] = last['inv_after']
    st['inv_after'] = {c: sum(SOULS[x['tier']] for x in st['own'] if x['slot'] == s_) for s_, c in COLN.items()}
    st['noncore'] = True; st['swap_unknown'] = unknown; st['sold_item'] = sold if (sold and sold in last['owned']) else None
    return st

def ab_name(P, slot): return P['b']['abil'][slot - 1]
def hum(prop):
    prop = prop.replace('MinDPS', 'MinDamagePerSecond').replace('MaxDPS', 'MaxDamagePerSecond').replace('DPS', 'DamagePerSecond').replace('HPS', 'HealPerSecond')
    s = re.sub(r'(?<!^)(?=[A-Z])', ' ', prop).lower()
    return s.replace('ability ', '').replace('duration', 'duration').strip()

# ---------------------------------------------------------------- claim record
_ctr = [0]
CONTEXT_KINDS = ('upgrade_of', 'component_for', 'sell_swap', 'spike_progress')   # context/instruction claims: appended to a caption that already has a reason, never a reason themselves
def claim(P, w, kind, phrase, tier, sources, score, timing=('now', 0, ''), check=None, numbers=(), specific=False, **extra):
    _ctr[0] += 1
    c = dict(id=f"{P['b']['id']}:{w['idx']}:{kind}:{_ctr[0]}", kind=kind, phrase=phrase, tier=tier, sources=sources, score=score,
             point=dict(idx=w['idx'], item=w['n'], souls=w['souls'], noncore=bool(w.get('noncore')), imb=w.get('imb'), note=w.get('_note', '')),
             timing=dict(when=timing[0], delta_souls=timing[1], event=timing[2]), check=check or {}, numbers=[str(n) for n in numbers], hero_specific=specific, role='context' if kind in CONTEXT_KINDS else 'reason')
    c.update(extra)
    return c

VD = 'gt/repo/game/citadel/pak01_dir/scripts/'
SRC_ITEM = lambda it: f"{VD}abilities.vdata:{it['class']}"
SRC_HERO = lambda hk: f"{VD}heroes.vdata:{hk}"
def SRC_AB(P, slot): return f"{VD}abilities.vdata:{P['R']['H']['ab'][slot]}"
def fmt(x):
    return f"{x:,.0f}" if abs(x) >= 100 else (f"{x:.0f}" if abs(x - round(x)) < 0.05 else f"{x:.1f}")

# ---------------------------------------------------------------- generators
def spirit_inst(R, w, T, sl, tier, cond=False, only_item=None, drop_imbue=None):
    """non-ult, non-DoT spirit-scaled per-instance values of ability sl at tier -> {prop: value}"""
    a = R['abil'][sl]
    if a['type'] == 'EAbilityType_Ultimate': return {}
    ww = w
    if drop_imbue:
        ww = dict(w, imbues={k: v for k, v in w['imbues'].items() if k != drop_imbue})
    Pp = A.at_tier(a, tier)
    out = {}
    for k, (v, inst) in A.spirit_hits(Pp, A.slot_sp(R, ww, sl, tier, cond)).items():
        if not inst or re.search(r'DPS|PerSecond|Tick|DoT', k): continue
        out[k] = v
    return out



def is_dur(p): return bool(re.search(r'ETechDuration|tech_duration', (p.get('sfun') or '') + ' ' + (p.get('stype') or '')))
def is_rng(p): return bool(re.search(r'ETechRange|ETechRadius|tech_range', (p.get('sfun') or '') + ' ' + (p.get('stype') or '')))
def is_spirit(p): return (p.get('stype') == 'ETechPower' or 'tech_damage' in (p.get('sfun') or '') or 'healing_spirit' in (p.get('sfun') or '')) and (p.get('scale') or 0) > 0

def tier_where(R, slot, test):
    """lowest tier (0..3) of ability `slot` whose property table satisfies test(P), else None"""
    for t in range(0, 4):
        if test(A.at_tier(R['abil'][slot], t)): return t
    return None

def when_tier(R, w, slot, tier):
    """('imminent'|'future'|'never', delta souls, event) until BOTH point models have `slot` at >= tier"""
    ss = [A.first_met(R, w, m, lambda ww, T: T[slot] >= tier)[0] for m in 'AB']
    if None in ss: return ('never', 0, '')
    d = max(ss) - w['souls']
    return ('imminent' if d <= IMMINENT_SOULS else 'future', d, None)

def lab_t(t): return 'unlocks' if t == 0 else f'reaches T{t}'

def fut_or_contra(P, w, kind_later, kind_none, slots_tests, ph_later, ph_none, src, check, **kw):
    """slots_tests: list of (slot, test). If some slot gets a satisfying tier later -> a future claim (timing from the point models); if none ever -> contradiction."""
    R = P['R']; best = None
    for sl, test in slots_tests:
        t = tier_where(R, sl, test)
        if t is None: continue
        if tmin(w, sl) >= t: continue     # satisfied now: caller should not call us
        wt = when_tier(R, w, sl, t)
        if wt[0] == 'never': continue
        if best is None or wt[1] < best[1][1]: best = (sl, wt, t)
    if best:
        sl, wt, t = best
        ev = f"{ab_name(P, sl)} {lab_t(t)}"
        return claim(P, w, kind_later, ph_later.format(ev=ev), V, src, 30, timing=(wt[0], wt[1], ev), check=check, specific=True, **kw)
    return claim(P, w, kind_none, ph_none, V, src, 0, timing=('never', 0, ''), check=check, contradiction=True, specific=True, **kw)

def g_spike(P, w):
    cs = []
    if w.get('noncore') and w.get('swap_unknown'): return cs
    it = A.item(w['n']); col = COLN[it['slot']]
    slot = it['slot']
    tabn = {'weapon': 'WeaponMod', 'spirit': 'Tech', 'vitality': 'Armor'}[col]
    tab = bonus_table(P['b']['hk'], tabn)
    b0, b1 = w['inv_before'][col], w['inv_after'][col]
    unit = {'weapon': '% weapon damage', 'spirit': ' spirit power', 'vitality': ' vitality bonus'}[col]
    TH = [t for t in (4800, 6400, 8000, 11200, 16000, 22400, 28800) if b0 < t <= b1]
    fmtk = lambda t: f"{t/1000:g}k"
    if 4800 in TH or TH:
        lo, hi = bonus_at(tab, b0), bonus_at(tab, b1)
        crossed = ', '.join(fmtk(t) for t in TH)
        extra = '' if len(TH) == 1 else f", crossing the {crossed} tiers"
        if 4800 in TH:
            cs.append(claim(P, w, 'spike_complete', f"Completes the 4.8k {col} tier ({fmt(b0)} to {fmt(b1)} invested{extra}): bonus {fmt(lo)} to {fmt(hi)}{unit}.", V,
                            [SRC_HERO(P['b']['hk']) + ' m_MapModCostBonuses', 'build purchase walk'], 92, check=dict(kind='spike', colour=col, threshold=4800),
                            numbers=['4.8k', b0, b1, lo, hi] + [fmtk(t) for t in TH], specific=False, colour=col, threshold=4800))
        else:
            cs.append(claim(P, w, 'invest_step', f"Takes {col} from {fmt(b0)} to {fmt(b1)} invested{extra}: bonus {fmt(lo)} to {fmt(hi)}{unit}.", V,
                            [SRC_HERO(P['b']['hk']) + ' m_MapModCostBonuses', 'build purchase walk'], 30, check=dict(kind='spike', colour=col, threshold=TH[0]),
                            numbers=[b0, b1, lo, hi] + [fmtk(t) for t in TH], specific=False, colour=col, threshold=TH[0]))
    if not cs and b1 > b0:
        nxt = next((t for t in (4800, 6400, 8000) if b1 < t), None)
        if nxt:
            cs.append(claim(P, w, 'spike_progress', f"Takes {col} to {fmt(b1)} of the {nxt/1000:g}k tier.", V, ['build purchase walk'], 24,
                            check=dict(kind='progress', colour=col, upto=b1), numbers=[b1, f"{nxt/1000:g}k"], colour=col, target=nxt))
    return cs

def later_completion(P, w, col, th):
    """purchases after w until `col` investment reaches th; -> (delta souls, purchases, item) or None"""
    for r in P['pts']:
        if r['idx'] > w['idx'] and r['inv_after'][col] >= th:
            return r['souls'] - w['souls'], r['idx'] - w['idx'], r['n']
    return None

def imminent(delta, npurch): return delta <= IMMINENT_SOULS and npurch <= IMMINENT_PURCHASES

def g_threshold(P, w):
    it = A.item(w['n']); kind = A.REG.get(it['class'])
    if kind not in ('hit', 'hitimb'): return []
    R = P['R']; thr = A.sv(it, 'MinimumDamage')
    if not thr: return []
    slots = [1, 2, 3]
    if kind == 'hitimb':
        if not w.get('imb'): return []
        slots = [w['imb']]
    def split(ww, T):
        above, below = [], []
        for sl in slots:
            if T[sl] < 0: continue
            for k, v in spirit_inst(R, ww, T, sl, T[sl]).items():
                (above if v > thr else below).append((sl, k, v, T[sl]))
        return above, below
    Tn = {s: tmin(w, s) for s in (1, 2, 3, 4)}
    ab, be = split(w, Tn)
    cs = []
    src = [SRC_ITEM(it) + ' MinimumDamage=%g' % thr] + [SRC_AB(P, s) for s in slots]
    pubs = [x for x in ab if x[2] >= 1.5 * thr]       # published only with a >=50% margin (pre/post-resist comparison is UNVERIFIED)
    if pubs:
        best = {}
        for s_, k, v, t in pubs: best[s_] = max(best.get(s_, 0), v)
        pubs = sorted([x for x in pubs if x[2] == best[x[0]]], key=lambda x: -x[2])
        names = ', '.join(f"{ab_name(P, s_)} ({fmt(v)})" for s_, k, v, t in pubs[:2])
        under = sorted({x[0] for x in be} - {x[0] for x in ab})
        extra = f"; {', '.join(ab_name(P, s_) for s_ in under)} {'stays' if len(under) == 1 else 'stay'} under it" if under else ''
        verb = 'clears' if len(pubs[:2]) == 1 else 'clear'
        cs.append(claim(P, w, 'threshold_now', f"{names} {verb} its {fmt(thr)}-damage trigger{extra}.", V, src, 85, check=dict(kind='threshold', thr=thr, slots=slots),
                        numbers=[thr] + [fmt(v) for s_, k, v, t in pubs[:2]], specific=True, margin=round(pubs[0][2] / thr, 2),
                        caveat='pre- vs post-resist comparison not in data; published only with >=50% margin'))
    elif ab:
        cs.append(claim(P, w, 'threshold_marginal', f"{ab_name(P, ab[0][0])} ({fmt(ab[0][2])}) is within 50% of the {fmt(thr)}-damage trigger; resist handling unverified.", MOD, src, 0, check=dict(kind='threshold', thr=thr, slots=slots), specific=True))
    else:
        # when does an instance first clear it
        def test(ww, T):
            return bool(split(ww, T)[0])
        for_model = {}
        for model in 'AB':
            s, what = A.first_met(R, w, model, test)
            for_model[model] = (s, what)
        sA, sB = for_model['A'][0], for_model['B'][0]
        if sA is not None and sB is not None:
            s = max(sA, sB); what = for_model['A'][1] if sA >= sB else for_model['B'][1]
            d = s - w['souls']
            cs.append(claim(P, w, 'threshold_later', f"From {what}: first ability hit above its {fmt(thr)}-damage trigger (nothing clears it at this purchase).", V,
                            src, 30, timing=('imminent' if d <= IMMINENT_SOULS else 'future', d, what), check=dict(kind='threshold_later', thr=thr, slots=slots), numbers=[thr], specific=True,
                            best_now=max([v for s2, k, v, t in be] or [0])))
        else:
            last = P['pts'][-1]; Tm = {s_: 3 for s_ in (1, 2, 3, 4)}; wide = []
            for sl in (slots if kind == 'hitimb' else [1, 2, 3, 4]):
                for k, (v, inst) in A.spirit_hits(A.at_tier(R['abil'][sl], 3), A.slot_sp(R, last, sl, 3, False)).items():
                    if v > thr: wide.append((ab_name(P, sl), k, v))
            if wide:
                cs.append(claim(P, w, 'threshold_unverified', f"Only {wide[0][0]} ({hum(wide[0][1])}, {fmt(wide[0][2])}) reaches the {fmt(thr)}-damage trigger, and whether an ultimate or damage-over-time tick counts is not established.", UNV, src, 0,
                                timing=('never', 0, ''), check=dict(kind='threshold_later', thr=thr, slots=slots), numbers=[thr], specific=True))
            else:
                cs.append(claim(P, w, 'threshold_never', f"Nothing in the kit (ultimate and damage-over-time ticks included) reaches the {fmt(thr)}-damage trigger even at max ability tiers.", V, src, 0,
                                timing=('never', 0, ''), check=dict(kind='threshold_later', thr=thr, slots=slots), contradiction=True, numbers=[thr], specific=True))
    if kind == 'hitimb':      # Mystic Reverb has no game text in the localisation files: the trigger semantics are the Council's reading (abtimeline REG), not verified
        for c in cs:
            c['tier'] = MOD if c['tier'] == V else c['tier']; c['contradiction'] = False; c['caveat'] = 'item has no localisation text; trigger semantics are modelled'
    return cs

def g_imbue(P, w):
    it = A.item(w['n']); imb = w.get('imb')
    cs = []
    if not imb: return cs
    R = P['R']; c = it['class']; sl = imb; name = ab_name(P, sl)
    a = R['abil'][sl]; isult = a['type'] == 'EAbilityType_Ultimate'
    src = [SRC_ITEM(it), SRC_AB(P, sl)]
    t = tmin(w, sl)
    if t < 0:
        # not trained at this purchase (both-model min)
        def test(ww, T): return T[sl] >= 0
        ss = [A.first_met(R, w, m, test)[0] for m in 'AB']
        if None in ss: when = ('never', 0, '')
        else:
            d = max(ss) - w['souls']; when = ('imminent' if d <= IMMINENT_SOULS else 'future', d, f"{name} unlocks")
        cs.append(claim(P, w, 'imbue_untrained', f"From {name} unlocking: the imbue has nothing to act on yet.", V, src, 10, timing=when, check=dict(kind='imbue_trained', slot=sl), specific=True))
        return cs
    Pp = A.at_tier(a, t)
    if c == 'upgrade_magic_tempo':
        cd = A.pv(Pp, 'AbilityCooldown'); pct = A.sv(it, 'CooldownReduction')
        if cd:
            cs.append(claim(P, w, 'imbue_cooldown', f"Imbued on {name}: takes {fmt(pct)}% off its {fmt(cd)}s base cooldown.", V, src, 50, check=dict(kind='imbue_cd', slot=sl),
                            numbers=[pct, cd], specific=True))
        else:
            cs.append(fut_or_contra(P, w, 'imbue_later', 'imbue_no_effect', [(sl, lambda Q: bool(A.pv(Q, 'AbilityCooldown')))], "From {ev}: the imbue has a cooldown to cut.", f"{name} has no cooldown to reduce.", src, dict(kind='imbue_cd', slot=sl)))
    elif c == 'upgrade_magic_reach':
        ps = sorted({k for k, p in Pp.items() if is_rng(p) and (p.get('v') or 0) > 0 and k != 'AbilityCastRange'} |
                    ({'AbilityCastRange'} if (A.pv(Pp, 'AbilityCastRange') or 0) > 0 else set()))
        if ps:
            what = ' and '.join(sorted({'range' if ('Range' in (Pp[k].get('stype') or '') or 'range' in (Pp[k].get('sfun') or '').lower() or k == 'AbilityCastRange') else 'radius' for k in ps}))
            nm_ = [hum(k) for k in ps[:3] if hum(k) not in ('radius', 'range', 'cast range')]
            cs.append(claim(P, w, 'imbue_reach', f"Imbued on {name}: widens its {what}" + (f" ({', '.join(nm_)})." if nm_ else "."), V, src, 40,
                            check=dict(kind='imbue_scale', slot=sl, stats=['ETechRange', 'ETechRadius']), specific=True))
        else:
            tst = lambda Q: any(is_rng(p) and (p.get('v') or 0) > 0 for p in Q.values())
            cs.append(fut_or_contra(P, w, 'imbue_later', 'imbue_no_effect', [(sl, tst)], "From {ev}: the imbue has a range or radius to widen.", f"{name} has no range- or radius-scaled property at any tier.", src, dict(kind='imbue_scale', slot=sl, stats=['ETechRange', 'ETechRadius'])))
    elif c == 'upgrade_arcane_extension':
        ps = {k: p['v'] for k, p in Pp.items() if is_dur(p) and (p.get('v') or 0) > 0}
        if ps:
            pri = sorted(ps.items(), key=lambda kv: (0 if re.search('Channel|AbilityDuration', kv[0]) else 1, -kv[1]))
            txt = ', '.join(f"{hum(k)} {fmt(v)}s" for k, v in pri[:2])
            pct = A.sv(it, 'BonusAbilityDurationPercent')
            cs.append(claim(P, w, 'imbue_duration', f"Imbued on {name}: its duration-scaled parts ({txt}) get +{fmt(pct)}%.", V, src, 58,
                            check=dict(kind='imbue_scale', slot=sl, stats=['ETechDuration']), numbers=[pct] + [fmt(v) for k, v in pri[:2]], specific=True))
        else:
            tst = lambda Q: any(is_dur(p) and (p.get('v') or 0) > 0 for p in Q.values())
            cs.append(fut_or_contra(P, w, 'imbue_later', 'imbue_no_effect', [(sl, tst)], "From {ev}: the imbue has a duration to extend.", f"{name} has no duration-scaled property at any tier, so a duration imbue has nothing to extend there.", src,
                                    dict(kind='imbue_scale', slot=sl, stats=['ETechDuration'])))
    elif c == 'upgrade_magic_storm':
        sp = A.sv(it, 'ImbuedTechPower')
        tg = [x for x in spirit_targets(P, w, {s_: (t if s_ == sl else -1) for s_ in (1, 2, 3, 4)}) if x[0] == sl]
        if tg:
            tg.sort(key=lambda x: (0 if x[3] == 'damage' else 1, -x[2]))
            x = tg[0]; g = x[2] * sp; per = ' per second' if re.search('DPS|PerSecond|HPS|Regen', x[1]) else ''
            cs.append(claim(P, w, 'imbue_spirit', f"Imbued on {name}: +{fmt(sp)} spirit on that ability only, about +{fmt(g)}{per} on its {hum(x[1])} ({x[2]:.2f}x scaling).", V, src, 60,
                            check=dict(kind='imbue_spirit', slot=sl), numbers=[sp, fmt(g), f"{x[2]:.2f}"], specific=True))
        else:
            tst = lambda Q: any(is_spirit(p_) and (p_.get('v') or 0) >= 0 and not re.search('Percent|Pct|Mult|Cooldown|Radius|Length|Duration', k_) for k_, p_ in Q.items())
            cs.append(fut_or_contra(P, w, 'imbue_later', 'imbue_no_effect', [(sl, tst)], "From {ev}: the imbued spirit has a scaling effect to raise.", f"{name} has no spirit-scaled effect at any tier, so the imbued spirit has nothing to raise there (the item's move-speed and fire-rate part still works).", src, dict(kind='imbue_spirit', slot=sl)))
    elif c == 'upgrade_ability_power_shard':
        if isult:
            cs.append(claim(P, w, 'imbue_invalid', f"Echo Shard resets non-ultimate abilities only and {name} is the ultimate.", V, src, 0, check=dict(kind='imbue_nonult', slot=sl), contradiction=True, specific=True))
        else:
            cd = A.pv(Pp, 'AbilityCooldown')
            cs.append(claim(P, w, 'imbue_reset', f"Imbued on {name}: resets its {fmt(cd)}s cooldown for a second cast; the shard's own 30s cooldown grows by that ability's cooldown.", V, src, 55,
                            check=dict(kind='imbue_nonult', slot=sl), numbers=[cd, 30], specific=True))
    elif c in ('upgrade_quick_silver', 'upgrade_ethereal_bullets'):
        fr = A.sv(it, 'BonusFireRate'); dur = A.sv(it, 'BuffDuration'); chg = A.sv(it, 'AbilityChargeUpTime')
        cs.append(claim(P, w, 'imbue_reload', f"Imbued on {name}: the imbue charges up over {fmt(chg)}s; the charged use reloads the clip and gives {fmt(fr)}% fire rate for {fmt(dur)}s.", V, src, 45,
                        check=dict(kind='imbue_trained', slot=sl), numbers=[chg, fr, dur], specific=True))
    elif c == 'upgrade_mystic_reverb':
        pass   # handled by g_threshold (hitimb)
    else:
        cs.append(claim(P, w, 'imbue_generic', f"Imbued on {name}.", V, src, 10, check=dict(kind='imbue_trained', slot=sl), specific=True))
    return cs

def g_upgrade_chain(P, w):
    it = A.item(w['n']); cs = []
    have = [c for c in it['components'] if c in w['prev_own']]
    if have:
        paid = sum(SOULS[A.item(c)['tier']] for c in have)
        cost = SOULS[it['tier']] - paid
        cs.append(claim(P, w, 'upgrade_of', f"Upgrade of {', '.join(have)} (already owned): costs {fmt(cost)} souls more, not {fmt(SOULS[it['tier']])}.", V,
                        ['audit/items_full.json components', 'build purchase walk'], 25, check=dict(kind='upgrade_of', comps=have), numbers=[cost, SOULS[it['tier']]]))
    else:
        for r in P['pts']:
            if r['idx'] > w['idx'] and w['n'] in A.item(r['n'])['components'] and not w.get('noncore'):
                d = r['souls'] - w['souls']; k = r['idx'] - w['idx']
                cs.append(claim(P, w, 'component_for', f"From {r['n']}: this becomes its component and counts toward the upgrade price.", V, ['audit/items_full.json components', 'build purchase walk'], 20,
                                timing=('imminent' if imminent(d, k) else 'future', d, r['n']), check=dict(kind='component_for', target=r['n'])))
                break
    return cs

def g_sell(P, w, note):
    m = re.search(r'Sell ([A-Z][^.]*?) (?:for this|first|once|to)', note or '')
    cs = []
    if m:
        x = m.group(1)
        nowned = len(w['prev_own'])
        if x in w['prev_own'] or w.get('noncore'):
            slot_full = nowned >= 12
            txt = f"Replaces {x}: sell it when you buy this" + (" (all 12 slots are full)." if slot_full else ".")
            cs.append(claim(P, w, 'sell_swap', txt, V, ['build note', 'build purchase walk'], 10, check=dict(kind='sell', old=x, slots_full=slot_full), numbers=[12] if slot_full else [], sold=x))
    return cs

def g_temporary(P, w):
    n = w['n']; it = A.item(n); cs = []
    npb = [k for k in it['vstats'] if k.startswith('NonPlayer') and A.num(str(it['vstats'][k])) not in (None, 0)]
    farm = ''
    if npb and it['class'] in ('upgrade_non_player_bonus',):
        farm = f" Until then it speeds up camps: +{fmt(A.sv(it, 'NonPlayerBonusWeaponPower'))}% weapon damage and +{fmt(A.sv(it, 'NonPlayerBulletResist'))}% bullet resist against non-hero targets."
    nums = [fmt(A.sv(it, 'NonPlayerBonusWeaponPower')), fmt(A.sv(it, 'NonPlayerBulletResist'))] if farm else []
    later = [(y, bx) for y, bx in P['sold_for'].get(n, [])]
    if later:
        core_b = [(y, bx) for y, bx in later if CORE_BOX.match(bx)]
        if core_b:
            y = core_b[0][0]
            cs.append(claim(P, w, 'temporary_sold', f"Temporary, sold when you buy {y} later.{farm}", V, ['build notes (planned sale)', SRC_ITEM(it)] if farm else ['build notes (planned sale)'], 52 if farm else 34,
                            check=dict(kind='planned_sale', item=n, buyer=y), numbers=nums, specific=bool(farm)))
        else:
            y, bx = later[0]
            cs.append(claim(P, w, 'swap_candidate', f"First item sold if you buy {y} later (listed under {bx}).", V, ['build notes (planned sale)'], 10, check=dict(kind='planned_sale', item=n, buyer=y)))
            cs[-1]['role'] = 'context'
    elif n in P['self_sell']:
        cs.append(claim(P, w, 'temporary_sold', f"Temporary: sell it later, {P['self_sell'][n]}.{farm}", V, ['build notes (planned sale)'], 40, check=dict(kind='planned_sale', item=n, buyer=None), numbers=nums))
    return cs

def g_charges(P, w):
    it = A.item(w['n']); R = P['R']; cs = []
    bc = A.sv(it, 'BonusAbilityCharges')
    if not bc or it['class'] not in ('upgrade_extra_charge', 'upgrade_rapid_recharge'): return cs
    have = []
    for sl in (1, 2, 3, 4):
        t = tmin(w, sl)
        if t >= 0 and A.charges_raw(R['abil'][sl], t) >= 1: have.append((sl, A.charges_raw(R['abil'][sl], t)))
    if have:
        prior = sum(A.sv(A.item(c_), 'BonusAbilityCharges') for c_ in it['components'] if c_ in w['prev_own'])
        add = int(bc - prior)
        txt = ', '.join(f"{ab_name(P, s)} ({n + int(prior)} to {n + int(bc)})" for s, n in have)
        cs.append(claim(P, w, 'charges', f"Adds {add} more charge{'s' if add > 1 else ''} to {txt}.", V, [SRC_ITEM(it)] + [SRC_AB(P, s) for s, n in have], 52,
                        check=dict(kind='charges', slots=[s for s, n in have]), numbers=[add] + [n + int(prior) for s, n in have] + [n + int(bc) for s, n in have], specific=True))
    else:
        tests = [(sl, (lambda Q: int(A.pv(Q, 'AbilityCharges') or 0) >= 1)) for sl in (1, 2, 3, 4)]
        cs.append(fut_or_contra(P, w, 'charges_later', 'charges_none', tests, "From {ev}: gives that ability a charge to add to.", "None of your abilities has a charge system at any tier.", [SRC_ITEM(it)], dict(kind='charges', slots=[])))
    return cs

def spirit_targets(P, w, tiers):
    """(slot, prop, gain-per-spirit, kind) for ETechPower-scaled damage / heal / barrier properties of abilities trained at `tiers`"""
    R = P['R']; out = []
    for sl in (1, 2, 3, 4):
        t = tiers[sl]
        if t < 0: continue
        for k, p in A.at_tier(R['abil'][sl], t).items():
            if is_spirit(p) and not re.search('Percent|Pct|Mult|Cooldown|Radius|Length|Duration|Resource|Cost|Health$|Summon', k) and (p.get('isdmg') or re.search(r'Heal|Barrier|Shield|Regen|HPS|DPS|Damage', k)):
                kind = 'damage' if (p.get('isdmg') or re.search('Damage|DPS', k)) else 'heal'
                out.append((sl, k, p['scale'], kind))
    return out

def g_spirit_stat(P, w):
    """spirit-power items: what the kit's spirit scaling gives per point (arithmetic on vdata scale; ult scaling counts here, it is not a trigger)."""
    it = A.item(w['n']); sp = A.item_sp(it)
    if not sp or it['slot'] != 'Tech' or A.REG.get(it['class']) in ('hit', 'hitimb', 'imbue'): return []
    R = P['R']; Tn = {s: tmin(w, s) for s in (1, 2, 3, 4)}
    tg = spirit_targets(P, w, Tn)
    nonult = [x for x in tg if x[0] != 4 or True]
    if tg:
        dmg = sorted([x for x in tg if x[3] == 'damage'], key=lambda x: -x[2]); heal = sorted([x for x in tg if x[3] == 'heal'], key=lambda x: -x[2])
        best = (dmg or heal)[0]
        g = best[2] * sp
        top = len(tg) > 1 and best[2] >= max(x[2] for x in tg)
        per = ' per second' if re.search('DPS|PerSecond|HPS|Regen', best[1]) else ''
        what = hum(best[1])
        return [claim(P, w, 'spirit_scaling', f"+{fmt(sp)} spirit adds about {fmt(g)}{per} to {ab_name(P, best[0])}'s {what} ({best[2]:.2f}x scaling)" + (", your steepest spirit scaling." if top and g >= 10 else "."), V,
                      [SRC_ITEM(it), SRC_AB(P, best[0])], (48 if top else 38) if g >= 10 else 25, check=dict(kind='spirit_scaling', slot=best[0], prop=best[1]), numbers=[sp, fmt(g), f"{best[2]:.2f}"], specific=True)]
    allt = []
    for sl in (1, 2, 3, 4):
        tt = tier_where(R, sl, lambda Q: any(is_spirit(p) and (p.get('isdmg') or re.search(r'Heal|Barrier|Shield|Regen|HPS|DPS|Damage', k)) for k, p in Q.items()))
        if tt is not None: allt.append((sl, (lambda Q: any(is_spirit(p) and (p.get('isdmg') or re.search(r'Heal|Barrier|Shield|Regen|HPS|DPS|Damage', k)) for k, p in Q.items()))))
    return [fut_or_contra(P, w, 'spirit_later', 'spirit_no_target', allt, "From {ev}: the first spirit-scaled effect your spirit can raise.", "Nothing in this hero's kit scales with spirit power at any tier.", [SRC_ITEM(it)], dict(kind='spirit_scaling', slot=0, prop=''))]

def g_dur_global(P, w):
    it = A.item(w['n']); R = P['R']
    if it['class'] != 'upgrade_imbued_duration_extender': return []
    pct = A.sv(it, 'BonusAbilityDurationPercent'); items = []
    for sl in (1, 2, 3, 4):
        t = tmin(w, sl)
        if t < 0: continue
        for k, p in A.at_tier(R['abil'][sl], t).items():
            if is_dur(p) and (p.get('v') or 0) > 0 and not re.search('PostCast|CastDelay|Linger', k):
                items.append((sl, k, p['v']))
    if not items: return []
    items.sort(key=lambda x: (0 if x[0] == 4 else 1, -x[2]))
    txt = ', '.join(f"{ab_name(P, s)} {hum(k)} ({fmt(v)}s)" for s, k, v in items[:3])
    return [claim(P, w, 'dur_global', f"+{fmt(pct)}% to every duration-scaled effect you have: {txt}.", V, [SRC_ITEM(it)] + [SRC_AB(P, s) for s in sorted({x[0] for x in items})], 50,
                  check=dict(kind='dur_global'), numbers=[pct] + [fmt(v) for s, k, v in items[:3]], specific=True)]

def g_cdr(P, w):
    it = A.item(w['n']); R = P['R']
    if it['class'] not in ('upgrade_cooldown_reduction',): return []
    pct = A.sv(it, 'CooldownReduction'); tot = []
    for sl in (1, 2, 3, 4):
        t = tmin(w, sl)
        if t >= 0:
            cd = A.pv(A.at_tier(R['abil'][sl], t), 'AbilityCooldown')
            if cd: tot.append((sl, cd))
    if len(tot) < 2: return []
    s = sum(c for _, c in tot)
    return [claim(P, w, 'cdr_rotation', f"With {len(tot)} abilities trained their base cooldowns total {fmt(s)}s; {fmt(pct)}% off is {fmt(s * pct / 100)}s per full rotation.", V,
                  [SRC_ITEM(it)] + [SRC_AB(P, sl) for sl, _ in tot], 33, check=dict(kind='cdr', slots=[sl for sl, _ in tot]), numbers=[len(tot), fmt(s), pct, fmt(s * pct / 100)], specific=True)]

_HE = {}
def hero_eff(hk):
    if not _HE: _HE.update(json.load(open(os.path.join(EFFECTS, 'heroes.json')))['heroes'])
    return _HE.get(hk, {}).get('abilities', [])
def stun_exposed(P, w):
    """this hero's trained non-ultimate abilities that a stun stops AND that are channelled or movement abilities (effects json behaviors + interrupted_by)."""
    exp = []
    for ad in hero_eff(P['b']['hk']):
        sl = ad['slot']
        if not isinstance(sl, int) or sl > 3: continue
        if tmin(w, sl) < 0 and not w.get('noncore'): continue
        bh = set(ad['behaviors'])
        if ('CHANNELLED' in bh or 'MOVEMENT' in bh) and 'MODIFIER_STATE_STUNNED' in ad['interrupted_by']:
            exp.append((sl, 'channelled' if 'CHANNELLED' in bh else 'movement'))
    return exp

def g_counter(P, w):
    it = A.item(w['n']); c = it['class']; cs = []
    src = [SRC_ITEM(it), 'council/evidence/interactions/effects/heroes.json behaviors+interrupted_by']
    if c == 'upgrade_unstoppable':
        exp = stun_exposed(P, w)
        if exp:
            txt = ' and '.join(f"{ab_name(P, s)} ({k})" for s, k in exp[:2])
            cs.append(claim(P, w, 'cc_exposure', f"A stun cancels your {txt}. Activate this before the stun lands (it cannot be used while stunned): {fmt(A.sv(it, 'AbilityDuration'))}s immune to stun, silence, sleep, root and disarm, {fmt(A.sv(it, 'AbilityCooldown'))}s cooldown.", V,
                            src, 56, check=dict(kind='cc_exposure', slots=[s for s, k in exp]), numbers=[fmt(A.sv(it, 'AbilityDuration')), fmt(A.sv(it, 'AbilityCooldown'))], specific=True))
    elif c == 'upgrade_reduce_debuff_duration':
        exp = stun_exposed(P, w)
        base = f"Purges non-ultimate debuffs (silence, slow, disarm) and heals {fmt(A.sv(it, 'HealOnActivate'))}, but cannot be used while stunned or asleep, so it answers a hex or silence and not a stun already on you."
        cs.append(claim(P, w, 'defence_purge', base, V, src, 46, check=dict(kind='stat', item=w['n'], keys=['HealOnActivate']), numbers=[fmt(A.sv(it, 'HealOnActivate'))]))
    return cs

def num_(it, k): return abs(A.num(str(it['vstats'].get(k, ''))) or 0)
def g_defence(P, w):
    it = A.item(w['n']); c = it['class']; cs = []
    if c == 'upgrade_metal_skin':
        cs.append(claim(P, w, 'defence_bullet', f"Immune to bullets only, for {fmt(A.sv(it, 'AbilityDuration'))}s on a {fmt(A.sv(it, 'AbilityCooldown'))}s cooldown, at {num_(it, 'ActiveMoveSpeedPenalty'):g}m/s slower: buy it against one gun carry, not against ability damage.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['AbilityDuration', 'AbilityCooldown']), numbers=[fmt(A.sv(it, 'AbilityDuration')), fmt(A.sv(it, 'AbilityCooldown')), f"{num_(it, 'ActiveMoveSpeedPenalty'):g}"]))
    elif c == 'upgrade_deflecting_armor':
        cs.append(claim(P, w, 'defence_gun', f"Passive: {fmt(A.sv(it, 'DeflectionPercent'))}% chance to deflect a bullet and {fmt(A.sv(it, 'BulletProcDeflectionPercent'))}% to block its on-hit effects; it helps against several gun heroes at once where a timed bullet immunity covers only one.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['DeflectionPercent']), numbers=[fmt(A.sv(it, 'DeflectionPercent')), fmt(A.sv(it, 'BulletProcDeflectionPercent'))]))
    elif c == 'upgrade_tech_purge':
        cs.append(claim(P, w, 'defence_spirit', f"Spirit resist {fmt(A.sv(it, 'TechResist'))}, plus {fmt(A.sv(it, 'TechResistBelowThreshold'))} more below {fmt(A.sv(it, 'HealthThreshold'))}% health: buy it when enemy spirit damage is what kills you.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['TechResist', 'TechResistBelowThreshold']), numbers=[fmt(A.sv(it, 'TechResist')), fmt(A.sv(it, 'TechResistBelowThreshold')), fmt(A.sv(it, 'HealthThreshold'))]))
    elif c == 'upgrade_counterspell':
        cs.append(claim(P, w, 'defence_parry', f"Your next parry blocks an enemy ability's damage and effects ({A.sv(it, 'SpellParryDuration'):g}s window, {fmt(A.sv(it, 'AbilityCooldown'))}s cooldown), so it only answers an ability you can see coming.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['SpellParryDuration', 'AbilityCooldown']), numbers=[f"{A.sv(it, 'SpellParryDuration'):g}", fmt(A.sv(it, 'AbilityCooldown'))]))
    elif c == 'upgrade_divine_barrier':
        cs.append(claim(P, w, 'defence_barrier', f"Cast on yourself or an ally: removes non-stun debuffs and gives a {fmt(A.sv(it, 'CombatBarrier'))} barrier for {fmt(A.sv(it, 'BuffDuration'))}s, {fmt(A.sv(it, 'AbilityCooldown'))}s cooldown (halved when cast on an ally), so it covers debuffs and burst damage but not a stun.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['CombatBarrier', 'BuffDuration']), numbers=[fmt(A.sv(it, 'CombatBarrier')), fmt(A.sv(it, 'BuffDuration')), fmt(A.sv(it, 'AbilityCooldown'))]))
    elif c == 'upgrade_glitch':
        cs.append(claim(P, w, 'defence_curse', f"Silences, disarms and blocks item use on one enemy for {A.sv(it, 'AbilityDuration'):g}s and strips their non-ultimate buffs, at -{fmt(num_(it, 'OutgoingDamagePenaltyPercent'))}% damage for you and a {fmt(A.sv(it, 'AbilityCooldown'))}s cooldown: a single-target answer to a buffed carry or engage.", V,
                        [SRC_ITEM(it)], 46, check=dict(kind='stat', item=w['n'], keys=['AbilityDuration', 'AbilityCooldown']), numbers=[f"{A.sv(it, 'AbilityDuration'):g}", fmt(num_(it, 'OutgoingDamagePenaltyPercent')), fmt(A.sv(it, 'AbilityCooldown'))]))
    return cs

def ult_state(P, w):
    R = P['R']; t = tmin(w, 4)
    return t, (A.at_tier(R['abil'][4], t) if t >= 0 else None)

def g_kit_items(P, w):
    """items whose value is defined by this hero's own abilities: ultimate triggers, global range, refresher, upgrade deltas."""
    it = A.item(w['n']); c = it['class']; R = P['R']; cs = []
    t4, P4 = ult_state(P, w)
    ultn = ab_name(P, 4)
    if c == 'upgrade_diviners_kevlar':
        if P4 is not None:
            cd = A.pv(P4, 'AbilityCooldown')
            cs.append(claim(P, w, 'ult_trigger', f"Casting {ultn} gives a {fmt(A.sv(it, 'CombatBarrier'))} barrier and +{fmt(A.sv(it, 'TechPower'))} spirit for {fmt(A.sv(it, 'BuffDuration'))}s, available once per ultimate cooldown ({fmt(cd)}s at your current ultimate tier), so it is a once-per-fight burst of defence.", V,
                            [SRC_ITEM(it), SRC_AB(P, 4)], 56, check=dict(kind='ult_tier', min_tier=t4), numbers=[fmt(A.sv(it, 'CombatBarrier')), fmt(A.sv(it, 'TechPower')), fmt(A.sv(it, 'BuffDuration')), fmt(cd)], specific=True))
        else:
            cs.append(claim(P, w, 'ult_trigger_later', "From the ultimate unlocking: this item's trigger is casting your ultimate.", V, [SRC_ITEM(it)], 20, timing=('future', 0, 'ultimate unlock'), check=dict(kind='ult_tier', min_tier=-1)))
    elif c == 'upgrade_ultimate_burst':     # Lightning Scroll
        if P4 is not None:
            dm = [k for k, p_ in P4.items() if p_.get('isdmg') and (p_.get('v') or 0) > 0]
            if dm:
                cs.append(claim(P, w, 'ult_trigger', f"{ultn} deals damage ({', '.join(hum(k) for k in dm[:2])}), so it applies the item's {A.sv(it, 'StunDuration'):g}s stun after a {fmt(A.sv(it, 'DelayBeforeStun'))}s delay plus {fmt(A.sv(it, 'Damage'))} damage.", V,
                                [SRC_ITEM(it), SRC_AB(P, 4)], 52, check=dict(kind='ult_dmg'), numbers=[f"{A.sv(it, 'StunDuration'):g}", fmt(A.sv(it, 'DelayBeforeStun')), fmt(A.sv(it, 'Damage'))], specific=True))
            else:
                cs.append(claim(P, w, 'ult_no_damage', f"{ultn} deals no damage, so a trigger on ultimate damage never fires.", V, [SRC_ITEM(it), SRC_AB(P, 4)], 0, check=dict(kind='ult_dmg'), contradiction=True, specific=True))
    elif c == 'upgrade_ability_refresher':
        tot = []; 
        for sl in (1, 2, 3, 4):
            t = tmin(w, sl)
            if t >= 0:
                cd = A.pv(A.at_tier(R['abil'][sl], t), 'AbilityCooldown')
                if cd: tot.append((sl, cd))
        if tot:
            u = [cd for sl, cd in tot if sl == 4]
            cs.append(claim(P, w, 'refresher', f"Resets every ability and charge: up to {fmt(sum(cd for sl, cd in tot))}s of base cooldown across your kit, {fmt(u[0]) + 's of it the ultimate' if u else 'ultimate not yet trained'}; the item has its own cooldown of {fmt(A.sv(it, 'AbilityCooldown'))}s.", V,
                            [SRC_ITEM(it)] + [SRC_AB(P, sl) for sl, _ in tot], 50, check=dict(kind='cdr', slots=[sl for sl, _ in tot]), numbers=[fmt(sum(cd for sl, cd in tot))] + ([fmt(u[0])] if u else []) + [fmt(A.sv(it, 'AbilityCooldown'))], specific=True))
    elif c == 'upgrade_tech_range':        # Greater Expansion (global)
        items = []
        for sl in (1, 2, 3, 4):
            t = tmin(w, sl)
            if t < 0: continue
            for k, p_ in A.at_tier(R['abil'][sl], t).items():
                if is_rng(p_) and (p_.get('v') or 0) > 0 and k != 'AbilityCastRange' and not re.search('Height|Width|Offset|Camera', k): items.append((sl, k, p_['v']))
        if items:
            items.sort(key=lambda x: (0 if x[0] == 4 else 1, -x[2]))
            txt = ', '.join(f"{ab_name(P, s_)} {hum(k)} ({fmt(v)}m)" for s_, k, v in items[:3])
            cs.append(claim(P, w, 'global_reach', f"+{fmt(A.sv(it, 'TechRangeMultiplier'))}% range and radius on everything that scales with them: {txt}.", V,
                            [SRC_ITEM(it)] + [SRC_AB(P, s_) for s_ in sorted({x[0] for x in items})], 50, check=dict(kind='global_reach'), numbers=[fmt(A.sv(it, 'TechRangeMultiplier'))] + [fmt(v) for s_, k, v in items[:3]], specific=True))
    # upgrade deltas: only when the component(s) are owned
    have = [c_ for c_ in it['components'] if c_ in w['prev_own']]
    if have and w.get('noncore'):
        comp = A.item(have[0]); ch = []
        WL = re.compile(r'CooldownReduction|TechPower|BulletResist|TechResist|FireRate|Lifesteal|BaseAttackDamagePercent|MoveSpeed|Barrier|Duration$|Regen|StatusResistance|Charges|Damage$|Slow')
        for k, v in it['vstats'].items():
            if k.startswith('Ability') or k in ('BonusHealth', 'OutOfCombatHealthRegen') or not WL.search(k) or re.search('Multiplier|Range|Radius|Height', k): continue
            a_ = A.num(str(v)) or 0; b_ = A.num(str(comp['vstats'].get(k, 0))) or 0
            if a_ != b_ and b_ != 0 and re.match(r'^[A-Za-z]+$', k): ch.append((k, b_, a_))
            elif a_ != b_ and b_ == 0 and re.search('CooldownReduction|FireRate|Lifesteal|Resist', k) and abs(a_) >= 5: ch.append((k, b_, a_))
        ch.sort(key=lambda x: -abs(x[2] - x[1]) / max(abs(x[1]), 1))
        if ch:
            txt = '; '.join(f"{hum(k)} {fmt(b_)} to {fmt(a_)}" for k, b_, a_ in ch[:2])
            cost = SOULS[it['tier']] - sum(SOULS[A.item(x)['tier']] for x in have)
            cs.append(claim(P, w, 'upgrade_delta', f"Same-slot upgrade of {have[0]} for {fmt(cost)} more souls: {txt}..", V,
                            [SRC_ITEM(it), SRC_ITEM(comp)], 46, check=dict(kind='upgrade_delta', comp=have[0]), numbers=[fmt(cost)] + [fmt(x) for k, b_, a_ in ch[:2] for x in (b_, a_)], specific=False))
    return cs

def g_spirit_burn(P, w):
    it = A.item(w['n'])
    if it['class'] != 'upgrade_spirit_burn': return []
    R = P['R']; thr = A.sv(it, 'DamageThreshold'); win = A.sv(it, 'DamageThresholdDuration')
    inst = []
    for sl in (1, 2, 3):
        t = tmin(w, sl)
        if t < 0: continue
        v = spirit_inst(R, w, {s_: tmin(w, s_) for s_ in (1, 2, 3, 4)}, sl, t)
        if v: inst.append((sl, max(v.values())))
    tot = sum(v for _, v in inst)
    if not inst: return []
    names = ' + '.join(f"{ab_name(P, sl)} ({fmt(v)})" for sl, v in inst)
    one = max(v for _, v in inst)
    if one >= 1.5 * thr:
        return [claim(P, w, 'burn_trigger', f"One {ab_name(P, max(inst, key=lambda x: x[1])[0])} hit ({fmt(one)}) alone passes the {fmt(thr)} spirit-damage trigger.", V, [SRC_ITEM(it)], 60, check=dict(kind='stat', item=w['n'], keys=['DamageThreshold']), numbers=[fmt(one), fmt(thr)], specific=True)]
    return [claim(P, w, 'burn_trigger_modelled', f"One rotation of {names} = {fmt(tot)} against the {fmt(thr)} trigger within {fmt(win)}s; needs the abilities to land together on one target (hit and timing assumed).", MOD, [SRC_ITEM(it)], 0, check=dict(kind='stat', item=w['n'], keys=['DamageThreshold']), numbers=[fmt(tot), fmt(thr), fmt(win)], specific=True)]

GEN = [g_kit_items, g_spirit_burn, g_spike, g_threshold, g_imbue, g_upgrade_chain, g_temporary, g_charges, g_spirit_stat, g_dur_global, g_cdr, g_counter, g_defence]

def claims_for(P, w, note):
    cs = []
    for g in GEN:
        try: cs += g(P, w)
        except Exception as e:
            cs.append(claim(P, w, 'generator_error', f"{g.__name__}: {e}", UNV, [], 0, timing=('error', 0, '')))
    cs += g_sell(P, w, note)
    return cs

# ---------------------------------------------------------------- claim verification (re-derives from raw data at the stated progression point)
def verify_claim(P, c):
    """re-run the check recorded in the claim at its progression point; -> (ok, why). Independent paths where cheap (raw regex on vdata)."""
    k = c.get('check', {}).get('kind'); ch = c['check']; R = P['R']
    pts = P['pts']
    w = pts[c['point']['idx']] if c['point']['idx'] < len(pts) and not c['point']['noncore'] else None
    if w is None and c['point']['noncore']:
        w = noncore_point(P, c['point']['item'], c['point'].get('imb'), 'x', c['point'].get('note', ''))
        # imbue slot is not stored on the claim point; checks that need it carry slot
    if k == 'spike':
        col = ch['colour']; th = ch['threshold']
        b0 = w['inv_before'][col]; b1 = w['inv_after'][col]
        # raw recomputation of inventory from names
        tot = lambda names: sum(SOULS[A.item(n)['tier']] for n in names if COLN[A.item(n)['slot']] == col)
        r0, r1 = tot(w['prev_own']), tot(w['owned'])
        ok = r0 < th <= r1 and b0 == r0 and b1 == r1
        return ok, f"inventory {col}: before {r0}, after {r1}, threshold {th}"
    if k == 'progress':
        r1 = sum(SOULS[A.item(n)['tier']] for n in w['owned'] if COLN[A.item(n)['slot']] == ch['colour'])
        return r1 == ch['upto'], f"{r1}"
    if k == 'threshold':
        it = A.item(w['n']); thr = A.sv(it, 'MinimumDamage')
        mm = re.search(r'MinimumDamage = \s*\{[^}]*?m_strValue = "?([0-9.]+)', A.block('abilities.vdata', it['class']) or '')
        raw = float(mm.group(1)) if mm else None
        if raw is not None and abs(raw - ch['thr']) > 1e-6: return False, f"MinimumDamage raw {raw} != {ch['thr']}"
        if c['kind'] == 'threshold_now':
            Tn = {s: tmin(w, s) for s in (1, 2, 3, 4)}
            above = [(s, v) for s in ch['slots'] if Tn[s] >= 0 for kk, v in spirit_inst(R, w, Tn, s, Tn[s]).items() if v >= 1.5 * ch['thr']]
            return bool(above), f"instances above: {above}"
        return True, 'later-claim: re-derived by generator'
    if k == 'imbue_trained':
        return tmin(w, ch['slot']) >= 0 if c['kind'] != 'imbue_untrained' else tmin(w, ch['slot']) < 0, ''
    if k in ('imbue_cd', 'imbue_scale', 'imbue_spirit', 'imbue_nonult'):
        sl = ch['slot']; t = tmin(w, sl)
        if c['kind'] in ('imbue_later',): return t < 0 or True, 'future claim: timing re-derived by generator'
        if t < 0 and not c.get('contradiction'): return False, 'ability not trained under both models'
        if c.get('contradiction'): t = 3          # contradictions hold only if the effect is absent at every tier
        Pp = A.at_tier(R['abil'][sl], t)
        if k == 'imbue_cd': return bool(A.pv(Pp, 'AbilityCooldown')) == (not c.get('contradiction')), ''
        if k == 'imbue_scale':
            fn = {'ETechDuration': is_dur, 'ETechRange': is_rng}[ch['stats'][0]]
            has = any(fn(p_) and (p_.get('v') or 0) > 0 for p_ in Pp.values())
            return has == (not c.get('contradiction')), ''
        if k == 'imbue_nonult': return (R['abil'][sl]['type'] != 'EAbilityType_Ultimate') == (not c.get('contradiction')), ''
        has = any(x[0] == sl for x in spirit_targets(P, w, {s_: (t if s_ == sl else -1) for s_ in (1, 2, 3, 4)}))
        return has == (not c.get('contradiction')), ''
    if k == 'upgrade_of':
        return all(x in w['prev_own'] for x in ch['comps']) and all(x in A.item(w['n'])['components'] for x in ch['comps']), ''
    if k == 'component_for':
        return w['n'] in A.item(ch['target'])['components'] and any(r['n'] == ch['target'] and r['idx'] > w['idx'] for r in pts), ''
    if k == 'sell':
        return (ch['old'] in w['prev_own'] or w.get('noncore')) and ((len(w['prev_own']) >= 12) == ch['slots_full'] or w.get('noncore')), ''
    if k == 'charges':
        sl = [s for s in (1, 2, 3, 4) if tmin(w, s) >= 0 and A.charges_raw(R['abil'][s], tmin(w, s)) >= 1]
        return sl == ch['slots'], f"{sl}"
    if k == 'spirit_scaling':
        if not ch['slot']: return True, ''
        p = A.at_tier(R['abil'][ch['slot']], tmin(w, ch['slot'])).get(ch['prop'], {})
        return is_spirit(p) and tmin(w, ch['slot']) >= 0, ''
    if k in ('ult_tier', 'ult_dmg', 'global_reach', 'upgrade_delta'):
        if k == 'ult_tier': return (tmin(w, 4) >= ch['min_tier']) if ch['min_tier'] >= 0 else (tmin(w, 4) < 0), ''
        if k == 'upgrade_delta': return ch['comp'] in A.item(w['n'])['components'], ''
        return True, 'structural; re-derived by generator'
    if k == 'planned_sale':
        return (ch['buyer'] in [y for y, bx in P['sold_for'].get(ch['item'], [])]) if ch['buyer'] else (ch['item'] in P['self_sell']), ''
    if k in ('dur_global', 'cdr', 'cc_exposure', 'stat', 'threshold_later'):
        return True, 'structural; re-derived by generator'
    return False, f'no verifier for check kind {k}'

# ---------------------------------------------------------------- classification + caption
REASON_MIN = 45     # a reason claim must score >= 45 to be published (hero-/build-/timing-specific); 25-44 = accurate but generic (held)
def first_spike_colour(P):
    best = None
    for col in ('weapon', 'spirit', 'vitality'):
        for r in P['pts']:
            if r['inv_after'][col] >= 4800:
                if best is None or r['souls'] < best[1]: best = (col, r['souls'])
                break
    return best

def classify(P, w, cs):
    """a useful now | b justified imminent spike / path to first spike | c preparatory, weak now -> timing review | g accurate but generic (held) | d no rationale established | x contradiction"""
    if any(c.get('contradiction') for c in cs): return 'x', 'contradiction: ' + next(c['phrase'] for c in cs if c.get('contradiction'))
    reasons = [c for c in cs if c['role'] == 'reason' and c['timing']['when'] == 'now' and c['tier'] in PUBLISHABLE]
    if any(c['score'] >= REASON_MIN for c in reasons): return 'a', ''
    fs = first_spike_colour(P)
    for c in cs:
        if c['kind'] == 'spike_progress':
            col = c['colour']; r = later_completion(P, w, col, c['target'])
            if r and (imminent(r[0], r[1]) or (fs and fs[0] == col and c['target'] == 4800)) and not [x for x in reasons if x['score'] >= REASON_MIN]:
                why = 'imminent' if imminent(r[0], r[1]) else f"on the path to the build's first 4.8k ({col})"
                c['timing'] = dict(when='imminent', delta_souls=r[0], event=f"{r[2]} completes the {c['target']/1000:g}k {col} tier")
                c['phrase'] = f"Builds toward the {c['target']/1000:g}k {col} tier, which {r[2]} completes {fmt(r[0])} souls on."
                c['numbers'] += [r[0], f"{c['target']/1000:g}k"]
                return 'b', f"{why}: {r[2]} completes {c['target']/1000:g}k {col} in {r[0]} souls (~{r[0]/SPM:.1f} min), {r[1]} purchases"
            if r: return 'c', f"{col} investment only; its {c['target']/1000:g}k tier completes at {r[2]}, {r[0]} souls (~{r[0]/SPM:.1f} min) later and {col} is not the first spike colour: timing review (delay, or is a lane/stat reason missing?)"
            if reasons: break
            return 'c', f"{col} investment only and the build never reaches the {c['target']/1000:g}k {col} tier through the core: timing review"
    for c in cs:
        if c['timing']['when'] == 'imminent' and c['kind'] in ('threshold_later', 'imbue_untrained', 'component_for') and c['role'] == 'reason':
            return 'b', f"payoff {c['timing']['event']} in {c['timing']['delta_souls']} souls (~{c['timing']['delta_souls']/SPM:.1f} min)"
    for c in cs:
        if c['timing']['when'] == 'future' and c['role'] == 'reason':
            return 'c', f"gives little now; payoff {c['timing']['event']} in {c['timing']['delta_souls']} souls (~{c['timing']['delta_souls']/SPM:.1f} min): timing review"
    if reasons: return 'g', 'only generic accurate reasons: ' + ' | '.join(c['phrase'] for c in reasons)
    ctx = [c for c in cs if c['role'] == 'context']
    return 'd', 'no hero-, build- or timing-specific reason established from the data layers implemented' + (' (only context: ' + ctx[0]['kind'] + ')' if ctx else '')

def compose(P, w, cs, cls):
    """caption from publishable claims only. reasons first (highest score, one per kind, max 2), then at most one context sentence."""
    if cls not in ('a', 'b'): return None, []
    pub = [c for c in cs if c['tier'] in PUBLISHABLE and not c.get('contradiction') and c['timing']['when'] in ('now', 'imminent')]
    reasons = sorted([c for c in pub if (c['role'] == 'reason' and (c['score'] >= 18 or c['timing']['when'] == 'imminent')) or (cls == 'b' and c['timing']['when'] == 'imminent' and c['kind'] in ('spike_progress', 'component_for'))], key=lambda c: -c['score'])
    ctx = sorted([c for c in pub if c['role'] == 'context'], key=lambda c: -c['score'])
    used = []; kinds = set()
    for c in reasons:
        if c['kind'] in kinds: continue
        if used and c['score'] < 30: continue
        if len(used) >= 2: break
        used.append(c); kinds.add(c['kind'])
    if not used: return None, []
    sells = [c for c in ctx if c['kind'] == 'sell_swap']
    ups = [c for c in ctx if c['kind'] == 'upgrade_of']
    if any(c['kind'] == 'upgrade_delta' for c in used): ups = []
    for c in (sells[:1] or ups[:1]):
        txt = ' '.join(u['phrase'] for u in used + [c])
        if len(txt) <= 320 and len(sentences(txt)) <= 3: used.append(c)
    while len(used) > 1 and (len(' '.join(u['phrase'] for u in used)) > 330 or len(sentences(' '.join(u['phrase'] for u in used))) > 3): used.pop()
    return ' '.join(c['phrase'] for c in used), [c['id'] for c in used]

# ---------------------------------------------------------------- linter / validator
def tooltip_text(it):
    return A.desc(it['class']) or ''
def trigrams(s):
    t = re.findall(r'[a-z0-9]+', s.lower()); return {tuple(t[i:i + 3]) for i in range(len(t) - 2)}

ALLNAMES = None
def all_item_names():
    global ALLNAMES
    if ALLNAMES is None: ALLNAMES = sorted(A.items().keys(), key=len, reverse=True)
    return ALLNAMES

def sentences(t): return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', t) if s.strip()]

def lint_caption(P, w, text, cs_used, item_name):
    """-> list of (rule, detail). Empty = pass."""
    errs = []
    if not text: return errs
    sents = sentences(text)
    if len(sents) > 3: errs.append(('length', f'{len(sents)} sentences'))
    if len(text) > 330: errs.append(('length', f'{len(text)} chars'))
    for pat in BANNED:
        if re.search(pat, text, re.I): errs.append(('banned-filler', pat))
    it = A.item(item_name)
    if it:
        tt = tooltip_text(it)
        if tt:
            a, b = trigrams(text), trigrams(tt)
            if a and len(a & b) / len(a) > 0.4: errs.append(('tooltip-restatement', f'{len(a & b)}/{len(a)} trigrams shared with game text'))
    for c in cs_used:
        if c['tier'] not in PUBLISHABLE: errs.append(('unverified-claim', c['id']))
    # numbers must come from claims (tolerance 1%)
    allv = []
    for c in cs_used:
        for x in c['numbers']:
            try: allv.append(abs(float(str(x).replace(',', '').replace('k', ''))))
            except ValueError: pass
    for m in re.findall(r'(?<![A-Za-z])[0-9][0-9,]*\.?[0-9]*k?', text):
        try: v = float(m.rstrip('.').replace(',', '').replace('k', ''))
        except ValueError: continue
        if not any(abs(v - u) <= max(0.06, 0.01 * abs(u)) for u in allv): errs.append(('number-not-in-claims', m))
    # temporal: mentions of this hero's abilities / tiers / other items
    for si, s in enumerate(sents):
        fut = bool(FUTURE_MARK.match(s)) or bool(re.search(r'\blater\b', s)) or bool(re.search(r'\bcompletes? [0-9,]+ souls on\b', s))
        for sl, an in enumerate(P['b']['abil'], 1):
            if an and an in s and not fut and tmin(w, sl) < 0 and an != item_name:
                errs.append(('temporal-ability', f'{an} is not trained at this purchase (min over models)'))
            for m in re.finditer(re.escape(an) + r' T([123])', s):
                if not fut and tmin(w, sl) < int(m.group(1)): errs.append(('temporal-tier', f'{an} T{m.group(1)} not reached'))
        for n in all_item_names():
            if n == item_name or n not in s or any(n in an_ for an_ in P['b']['abil']): continue
            held = set(w['owned']) | set(w['prev_own'])
            if not fut and n not in held and not any(n in c.get('sold', '') for c in cs_used) :
                if re.search(r'\b' + re.escape(n) + r'\b', s): errs.append(('temporal-item', f'{n} not owned at this purchase'))
            if fut:
                later = [r['n'] for r in P['pts'] if r['idx'] > w['idx']]
                later += [it_[0] for r_ in P['b']['rows'] for bx in r_ if not CORE_BOX.match(bx[0]) for it_ in bx[3]]
                if n not in later and n not in w['owned'] and re.search(r'\b' + re.escape(n) + r'\b', s): errs.append(('future-ref-false', f'{n} is not bought later in this build'))
    # spike claims
    for m in re.finditer(r'(4\.8k|6\.4k)', text):
        if not any(c['kind'] in ('spike_complete', 'spike_progress', 'invest_step') and m.group(1) in [str(x) for x in c['numbers']] for c in cs_used): errs.append(('spike-claim-unbacked', m.group(1)))
    if re.search(r'\bcompletes\b', text, re.I):
        for s in sents:
            if re.search(r'\bcompletes\b', s, re.I) and not FUTURE_MARK.match(s) and not any(c['kind'] == 'spike_complete' for c in cs_used): errs.append(('completes-unbacked', s[:40]))
    # future effects in present tense
    for c in cs_used:
        if c['timing']['when'] in ('future', 'imminent') and not (FUTURE_MARK.match(c['phrase']) or re.search(r'souls on', c['phrase'])): errs.append(('future-in-present-tense', c['id']))
    return errs

# ---------------------------------------------------------------- phases
def big_spirit_hit(P, w):
    R = P['R']; best = None
    for sl in (1, 2, 3):
        t = tmin(w, sl)
        if t < 0: continue
        for k, v in spirit_inst(R, w, {x: tmin(w, x) for x in (1, 2, 3, 4)}, sl, t).items():
            if best is None or v > best[2]: best = (sl, k, v)
    return best

def phase_desc(P, boxname, pts):
    """capability / spike description derived only from the real progression (no tactical prose: that needs researched claims)."""
    if not pts: return None, []
    R = P['R']; a0, a1 = pts[0], pts[-1]
    prevs = [r for r in P['pts'] if r['idx'] < a0['idx']]
    p0 = prevs[-1] if prevs else None
    start = p0['souls'] if p0 else 0
    lab = lambda t: 'locked' if t < 0 else ('unlocked' if t == 0 else 'T%d' % t)
    gains = []
    for s_ in (1, 2, 3, 4):
        t0 = tmin(p0, s_) if p0 else -1; t1 = tmin(a1, s_)
        if t1 > t0 and agree(a1, s_): gains.append(f"{ab_name(P, s_)} {lab(t1)}")
    cs = []
    txt = f"Souls {fmt(start)}-{fmt(a1['souls'])} (levels {(p0 or a0)['lv'] if p0 else 1}-{a1['lv']})."
    cs.append(claim(P, a1, 'phase_range', txt, V, ['build purchase walk', SRC_HERO(P['b']['hk']) + ' m_mapLevelInfo'], 20, check=dict(kind='stat', item=a1['n'], keys=[]), numbers=[fmt(start), fmt(a1['souls']), (p0 or a0)['lv'] if p0 else 1, a1['lv']]))
    out = txt
    if gains:
        t2 = f"Abilities gained (both point models agree): {', '.join(gains)}."
        out += ' ' + t2
        cs.append(claim(P, a1, 'phase_abilities', t2, V, ['ability point models A+B (abtimeline)'], 20, check=dict(kind='stat', item=a1['n'], keys=[])))
    if p0 is not None:
        h0, h1 = big_spirit_hit(P, p0), big_spirit_hit(P, a1)
        if h0 and h1 and h1[2] >= 1.25 * h0[2]:
            t3 = f"Your biggest single spirit hit ({ab_name(P, h1[0])}, {hum(h1[1])}) grows from {fmt(h0[2])} to {fmt(h1[2])}."
            out += ' ' + t3
            cs.append(claim(P, a1, 'phase_power', t3, V, [SRC_AB(P, h1[0]), 'spirit from owned items (vdata)'], 20, check=dict(kind='stat', item=a1['n'], keys=[]), numbers=[fmt(h0[2]), fmt(h1[2])]))
    spikes = []
    for r in pts:
        for c in g_spike(P, r):
            if c['kind'] == 'spike_complete' and c['threshold'] == 4800: spikes.append(f"{c['colour']} 4.8k at {r['n']}")
    if spikes:
        t4 = f"4.8k spikes: {', '.join(spikes)}."
        out += ' ' + t4
        cs.append(claim(P, a1, 'phase_spikes', t4, V, ['build purchase walk', SRC_HERO(P['b']['hk'])], 20, check=dict(kind='stat', item=a1['n'], keys=[]), numbers=['4.8k']))
    ult = [r for r in pts if tmin(r, 4) >= 0 and (p0 is None or tmin(p0, 4) < 0)]
    if ult and agree(ult[0], 4):
        t5 = f"Ultimate ({ab_name(P, 4)}) is available from {ult[0]['n']}."
        out += ' ' + t5
        cs.append(claim(P, a1, 'phase_ult', t5, V, ['ability point models A+B (abtimeline)'], 20, check=dict(kind='stat', item=a1['n'], keys=[])))
    return out, cs

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
KC = [(re.compile(p + '$'), c, d) for p, c, d in KEYCLASS]
FAMILY = {'clip_size': 'ammo', 'reload_refill': 'ammo', 'unlimited_ammo': 'ammo', 'bullet_lifesteal': 'sustain', 'spirit_lifesteal': 'sustain', 'melee_lifesteal': 'sustain',
          'active_heal': 'sustain', 'regen': 'sustain', 'barrier': 'sustain'}
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
def weapon(R):
    b = block('abilities.vdata', R['H']['wpn']) or ''
    g = lambda k, d=0.0: float((re.search(k + r' = ([0-9.\-]+)', b) or [None, d])[1])
    rl = RELOAD_S.get(R['H']['wpn'], (2.5, 'ASSUMED 2.5 s: reload duration is animation-defined, not in vdata'))
    return dict(dmg=g('m_flBulletDamage'), cyc=g('m_flCycleTime', 1) or 1, pel=g('m_iBullets', 1) or 1, clip=g('m_iClipSize', 10), reload=rl[0], reload_src=rl[1])
def contrib(name, R, T=None, cdr=0.0, ability_slot=None):
    """gun-relevant contributions of one item (or one ability at its tier): clip%, damage%, passive/active fire rate, refills, unlimited ammo, bullet lifesteal."""
    if ability_slot:
        s = {k: p.get('v') for k, p in at_tier(R['abil'][ability_slot], T[ability_slot]).items() if p.get('v')}
        cd = (s.get('AbilityCooldown') or 0) * (1 - cdr / 100); dur = s.get('AbilityDuration') or 0; cls = ''
    else:
        s = mstats(name); it = item(name); cls = it['class'] if it else ''
        cd = s.get('AbilityChargeUpTime') or s.get('AbilityCooldown') or 0; dur = s.get('BuffDuration') or s.get('AbilityDuration') or 0
    c = dict(clip_pct=s.get('BonusClipSizePercent', 0) + s.get('MaxClipBonus', 0), dmg_pct=s.get('BaseAttackDamagePercent', 0), fr_perm=0.0, fr_act=[], refill=[], unl=None, ls_perm=0.0, ls_act=[])
    cond_fr = cls in ('upgrade_healbuff', 'upgrade_tech_overflow', 'upgrade_quick_silver', 'upgrade_ethereal_bullets')
    fr = s.get('BonusFireRate', 0) + s.get('FireRateBonus', 0) + s.get('FireRatePerKill', 0)
    if fr:
        if ability_slot or cond_fr: c['fr_act'].append((fr, dur or 5, cd or 20))
        elif s.get('ActiveBonusFireRate'): pass
        else: c['fr_perm'] += fr
    if s.get('ActiveBonusFireRate'): c['fr_act'].append((s['ActiveBonusFireRate'], s.get('AbilityDuration') or 5, cd or 30))
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
def strip_c(c, groups):
    c = dict(c)
    if 'clip' in groups: c['clip_pct'] = 0
    if 'refill' in groups: c['refill'] = []
    if 'unl' in groups: c['unl'] = None
    if 'fr' in groups: c['fr_perm'] = 0.0; c['fr_act'] = []
    return c
def gun_model(R, w, items_in, abil_T, cdr, W, use, strip=None):
    """damage proxy (bullets x per-bullet multiplier) over W s, and bullet-lifesteal heal, for a set of owned items + hero abilities. `only`: restrict to groups."""
    wp = weapon(R); cons = [(strip_c(contrib(n, R, cdr=cdr), strip[1]) if strip and n == strip[0] else contrib(n, R, cdr=cdr)) for n in items_in]
    for sl in (1, 2, 3, 4):
        if abil_T[sl] >= 0: cons.append(contrib(None, R, T=abil_T, cdr=cdr, ability_slot=sl))
    allow = lambda g: True
    clip = wp['clip'] * (1 + (sum(c['clip_pct'] for c in cons) if allow('clip') else 0) / 100)
    frp = sum(c['fr_perm'] for c in cons) if allow('fr') else 0
    fra = sum(f * min(1.0, d / (cdw / use)) for c in cons for f, d, cdw in c['fr_act']) if allow('fr') else 0
    cyc = wp['cyc'] / (1 + (frp + fra) / 100)
    refills = [r for c in cons for r in c['refill']] if allow('refill') else []
    unl = None
    if allow('unl'):
        u = [c['unl'] for c in cons if c['unl']]
        if u: unl = max(u, key=lambda x: x[0] / x[1])
    dmgm = 1 + (w['wb'] + sum(c['dmg_pct'] for c in cons)) / 100
    b = sim(W, max(1, clip), cyc, wp['reload'], refills, unl, use)
    dmg = b * (wp['dmg'] + w['boons'] * R['H']['bdl']) * wp['pel'] * dmgm
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
    res = {'groups': []}; fams = sorted({FAMILY.get(c['cls'], c['cls']) for c in cands}) if cands else []
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
                    ov_wo = gun_model(R, w, act(with_items), T, cdr_w, W, use, strip=(n, part)); ov_w = full_w
                    rows[(W, use)] = dict(total=pct(full_w['dmg'], full_wo['dmg']), overlap_role=pct(ov_w['dmg'], ov_wo['dmg']), mag_with=full_w['mag_s'], mag_wo=full_wo['mag_s'], clip_w=full_w['clip'], clip_wo=full_wo['clip'], refills=full_w['n_refill'])
            grp['table'] = {f"{W}s/use{u}": {k: round(v, 1) for k, v in r.items()} for (W, u), r in rows.items()}
            key = (20, USE_RATES[-1]); v = rows[key]['overlap_role']; grp['metric'] = f"gun damage over 20 s, overlapped role only, use=0.5: {v:+.1f}%  (whole item {rows[key]['total']:+.1f}%)"
            grp['overlap_gain'] = v; grp['total_gain'] = rows[key]['total']; grp['range'] = (min(r['overlap_role'] for (W, u), r in rows.items() if W == 20), max(r['overlap_role'] for (W, u), r in rows.items() if W == 20))
            thr = THR['ammo'] if fam == 'ammo' else THR['rate']
            wd = [r['overlap_role'] for (W, u), r in rows.items() if u == 0.5]
            if v >= thr: grp['verdict'] = 'ADDS-VALUE'
            elif max(wd) >= thr: grp['verdict'] = 'COMPLEMENTS'; grp['why'] = 'overlapped role matters in a different window length (10/20/60 s: ' + ', '.join(f"{x:+.0f}%" for x in wd) + ')'
            else: grp['verdict'] = 'REDUNDANT-LIKELY'
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
            def r_of(L, cl): return sum(c['val'] for x in L for c in item_classes(x) if c['cls'] == cl and c['defining']) / 100
            rw, rwo = min(0.9, r_of(with_items, fam)), min(0.9, r_of(wo_items, fam)); v = ((1 - rwo) / (1 - rw) - 1) * 100
            grp['metric'] = f"effective hp vs that damage type: {v:+.1f}% (resist {rwo*100:.0f}% -> {rw*100:.0f}%)"; grp['overlap_gain'] = v
            grp['assumptions'].append('resist stacking assumed multiplicative on remaining damage (UNVERIFIED in sandbox)')
            grp['verdict'] = 'ADDS-VALUE' if v >= THR['resist'] else 'REDUNDANT-LIKELY'; grp['why'] = 'same damage type resist stacks'
        elif fam == 'cooldown':
            v = ((1 - cdr_wo / 100) / (1 - cdr_w / 100) - 1) * 100; grp['metric'] = f"ability cast rate: {v:+.1f}% (CDR {cdr_wo:.0f}% -> {cdr_w:.0f}%)"; grp['overlap_gain'] = v
            grp['assumptions'].append('CDR stacking assumed multiplicative, cap 60% (UNVERIFIED)')
            grp['verdict'] = 'ADDS-VALUE' if v >= THR['cdr'] else 'REDUNDANT-LIKELY'; grp['why'] = 'CDR from the same pool'
        else:
            grp['verdict'] = 'UNKNOWN'; grp['why'] = f"no pricing model for effect class '{fam}' in this tool"
            grp['needs_test'] = f"build-context test: {n} with vs without at this checkpoint for the {fam} stat (cast the relevant abilities, real tiers)"
        res['groups'].append(grp)
    ORD = ['UNKNOWN', 'REDUNDANT-LIKELY', 'COMPLEMENTS', 'ADDS-VALUE']
    res['verdict'] = min((g['verdict'] for g in res['groups']), key=ORD.index) if res['groups'] else None
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
        cls = [c for c in item_classes(n) if c['defining']]
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
        return dict(item=n, at=where, souls=w['souls'], candidate=True, classes=sorted({c['cls'] for c in cls}), sources=[s['cite'] for s in cands][:10], **est)
    for i, w in enumerate(rows):
        n = w['n']; st = checkpoint_state(R, w, 'buy'); ws = state(R, dict(w))
        a = one(n, ws, 'at-buy', st, prev)
        # same item judged against the complete core (sources bought later, abilities at their final tier)
        endst2 = dict(endst); endst2['own_names'] = [x for x in endst['own_names']]
        if n not in endst2['own_names']: endst2['own_names'] = endst2['own_names'] + [n]   # item itself sold later: judge it as held
        bb = one(n, endw, 'core-end', endst2, prev)
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
def alternatives(R, b, n, v, st, prev_owned):
    it = item(n); gun = [g for g in v.get('groups', []) if g['family'] in ('ammo', 'fire_rate') and 'total_gain' in g]
    if not gun: return {'note': 'cross-metric: no common metric with other purchases; needs build-context comparison (context file)'}
    held = [c for c in it['components'] if c in prev_owned]; base = [x for x in st['own_names'] if x != n] + held; w = st['w']; T = st['T']
    z = gun_model(R, w, base, T, cdr_pct([dict(n=q) for q in base]), 20, 0.5); alts = []
    for r in b['rows']:
        for box in r:
            for x in box[3]:
                m = x[0]; mi = item(m)
                if not mi or m == n or m in st['own_names'] or mi['tier'] != it['tier']: continue
                if all(c['cls'] not in ('clip_size', 'fire_rate', 'bullet_damage', 'reload_refill', 'unlimited_ammo') for c in item_classes(m)): continue
                a = gun_model(R, w, base + [m], T, cdr_pct([dict(n=q) for q in base + [m]]), 20, 0.5); alts.append((m, round(pct(a['dmg'], z['dmg']), 1)))
    alts = sorted(set(alts), key=lambda x: -x[1])[:4]
    return {'metric': 'gun damage over 20 s, use=0.5; same-tier items already listed in this build, bought instead of the item', 'item_total': round(gun[0]['total_gain'], 1), 'alts': alts,
            'best_alt_beats_item': bool(alts and alts[0][1] > gun[0]['total_gain'] + 2)}
def needs_context(o):
    """gate trigger: overlap-candidate whose overlapped role is low/unknown at the buy point or in the complete core."""
    for k in ('at_buy', 'core_end'):
        v = o.get(k)
        if v and v.get('candidate') and v.get('verdict') in ('REDUNDANT-LIKELY', 'UNKNOWN'): return True
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
    """build-context comparison file (kind `context`) generated from the model; the stated estimate is CALCULATED, not measured."""
    o = next(x for x in res['items'] if x['item'] == item_name); ev = o['core_end'] or o['at_buy']
    g = ev['groups'][0] if ev and ev.get('groups') else {}; al = (ev or {}).get('alternatives') or {}
    best = al.get('alts', [[None, None]])[0] if isinstance(al.get('alts'), list) and al.get('alts') else (None, None)
    T = [f"SCOPE: build-context", f"KIND: context", f"VALID: yes (CALCULATED from game data by abtimeline.py --overlap; not a sandbox measurement)", f"BUILD: {build_id}",
         f"CHECKPOINT: {o['souls'] if o['souls'] is not None else 'core-end'}", f"ITEM: {item_name}",
         "WITH: complete build at the checkpoint incl. the item (owned items, ability tiers, imbues; see sources below)",
         "WITHOUT: same build with the item removed and its components held",
         f"ALT: " + (f"{best[0]} (same-tier item listed in this build)" if best[0] else "none computable on the gun metric (cross-metric)"),
         f"ESTIMATE: {item_name} | item={g.get('total_gain', g.get('overlap_gain', 0)):.1f}% | alt={best[0] or 'none'} {best[1] if best[1] is not None else 0:.1f}%",
         f"METRIC: {al.get('metric', g.get('metric', ''))}", f"VERDICT-BASIS: {ev['verdict'] if ev else ''}"]
    for gg in (ev or {}).get('groups', []): T += [f"GROUP {gg['family']}: {gg['verdict']} - {gg['why']}"] + ['  assumption: ' + a for a in gg.get('assumptions', [])] + ['  source: ' + s for s in gg['sources']]
    open(outfile, 'w').write('\n'.join(T) + '\n')


#!/usr/bin/env python3
"""Section N path comparison for geist and ratking_grenade (CALCULATED from gt/repo 6801 vdata == 6819 per council/audit/GAMEDATA_6819.md).
usage (from SP): python3 -I council/work/tri2/paths.py geist|ratking_grenade
Uses council/tools/abtimeline.py walk/state/model_A/model_B. Each variant = full core order; metrics at soul checkpoints.
Assumptions (stated, not verified in game): vitality invest flBonus = % base health; Life Drain heal = drained damage (LifeDrainHealthMult 100)
x (1 + HealAmpCastPercent); grenade per detonation = DamagePerShrapnel + 0.6 x (weapon invest bonus + item Weapon Damage %), Battle Vest /
Hollow Point counted only above 65% health (shown separately as 'cond'); Compress/Superior Cooldown multiplicative; no resists."""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../tools'))
import abtimeline as T

def armor_bonus(hk):
    b = T.block('heroes.vdata', hk); k = b.find('m_MapModCostBonuses'); j = b.find('EItemSlotType_Armor = ', k); seg = b[j:b.find(']', j)]
    return [(int(a), float(c)) for a, c in re.findall(r'nGoldThreshold = (\d+)\s*flBonus = ([0-9.]+)', seg)]

def mk(base, core, imb=None):
    b = json.loads(json.dumps(base)); imb = imb or {}
    b['rows'] = [[['Early · L-R', '', '', [[n, ''] + ([str(imb[n])] if n in imb else []) for n in core]]]]
    return b

CK = [3200, 4800, 6400, 8000, 9600, 11200, 12800, 14400, 16000, 17600, 19200, 20800, 22400, 24000, 28800, 33600, 36800, 43200]

def inv(w):
    o = {'w': 0, 's': 0, 'v': 0}
    for i in w['own']: o[{'WeaponMod': 'w', 'Tech': 's', 'Armor': 'v'}[i['slot']]] += T.SOULS[i['tier']]
    return o

def run(base, variants, order, metric):
    H = T.hero_info(base['hk']); AB = armor_bonus(base['hk']); out = {}
    for lab, core, imb in variants:
        b = mk(base, core, imb); R = T.analyse(b, order)
        evS = T.model_A(order, R['L'], strict=True); rows = [r for r in R['rows'] if not r.get('unknown')]
        sp = {c: None for c in 'wsv'}; sp64 = {c: None for c in 'wsv'}
        for r in rows:
            v = inv(r)
            for c in 'wsv':
                if sp[c] is None and v[c] >= 4800: sp[c] = r['souls']
                if sp64[c] is None and v[c] >= 6400: sp64[c] = r['souls']
        pts = []
        for s in CK:
            w = [r for r in rows if r['souls'] <= s]
            if not w: continue
            w = T.state(R, dict(w[-1], souls=s)); w['tS'] = T.tiers_at(evS, s)
            pts.append(dict(souls=s, inv=inv(w), **metric(R, w, H, AB)))
        out[lab] = {'core': core, 'spike4800': sp, 'spike6400': sp64, 'end': rows[-1]['souls'], 'points': pts}
    return out

# ---------------- geist ----------------
def geist_metric(R, w, H, AB):
    own = w['own']; names = [i['name'] if 'name' in i else '' for i in own]
    vb = max([bo for th, bo in AB if inv(w)['v'] >= th] or [0])
    hp = (880 + 51 * w['boons']) * (1 + vb / 100) + sum(T.sv(i, 'BonusHealth') for i in own)
    if any(i.get('class') == 'upgrade_non_player_bonus_sacrifice' for i in own): hp += 4 * w['boons']
    amp = sum(T.sv(i, 'HealAmpCastPercent') for i in own)
    wd = w['wb'] + sum(T.sv(i, 'BaseAttackDamagePercent') for i in own)
    tr = 1.0
    for i in own:
        x = T.sv(i, 'TechResist')
        if x: tr *= (1 - x / 100)
    extra = sum(T.sv(i, 'BonusAbilityCharges') for i in own if i.get('class') != 'upgrade_non_player_bonus_sacrifice')   # Cultist's +1 is its timed buff: shown as '+C'
    cult = any(i.get('class') == 'upgrade_non_player_bonus_sacrifice' for i in own)
    ls_b = sum(T.sv(i, 'BulletLifestealPercent') for i in own); ls_s = sum(T.sv(i, 'AbilityLifestealPercentHero') for i in own)
    res = {'hp': round(hp), 'spirit': round(w['sp']), 'wd%': round(wd), 'healamp%': amp, 'spiritres%': round((1 - tr) * 100), 'lifesteal b/s': f"{ls_b:g}/{ls_s:g}"}
    a = R['abil'][2]
    for m, tt in (('A', w['tA']), ('Astrict', w['tS']), ('B', w['tB'])):
        t = tt[2]
        if t < 0: res['LD_' + m] = 'locked'; continue
        P = T.at_tier(a, t); base_ch = T.charges_raw(a, t)
        ch = base_ch + (extra if base_ch >= 2 else 0) if base_ch else 1   # 0-charge ability: Extra Charge adds nothing under either F7 reading
        ch_if1 = base_ch + (extra if base_ch >= 1 else 0) if base_ch else 1
        spl = w['sp'] + (w['chg_sp'] if base_ch >= 2 else 0)
        dps = T.pv(P, 'LifeDrainPerSecond') + (P['LifeDrainPerSecond']['scale']) * spl
        dur = T.pv(P, 'AbilityDuration')
        heal1 = dps * dur * (1 + amp / 100)
        res['LD_' + m] = f"{T.tlabel(t)} ch{ch:g}{'+C' if cult and base_ch >= 2 else ''}{'' if ch == ch_if1 else '(1-counts:' + format(ch_if1, 'g') + ')'} {heal1:.0f}/charge bank {heal1 * ch:.0f}"
    return res

GEIST_COMMON_EARLY = ['Monster Rounds', 'Extra Regen', 'Mystic Regeneration', 'Extra Stamina', 'Kinetic Dash', 'Cultist Sacrifice', 'Radiant Regeneration']
GEIST_TAIL = ['Spellslinger', 'Blood Tribute', 'Leech']
G = {
 'G0_cleanbase': GEIST_COMMON_EARLY + ['Healing Booster', 'Spirit Resilience', 'Berserker', 'Extra Charge', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
 'G1_current': GEIST_COMMON_EARLY + ['Spirit Resilience', 'Berserker', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal', 'Healing Booster'] + GEIST_TAIL + ['Extra Charge', 'Rapid Recharge', 'Refresher'],
 'G2_HBearly_EClate': GEIST_COMMON_EARLY + ['Healing Booster', 'Spirit Resilience', 'Berserker', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal'] + GEIST_TAIL + ['Extra Charge', 'Rapid Recharge', 'Refresher'],
 'G3_lifesteal_as_health_spike': GEIST_COMMON_EARLY + ['Healing Booster', 'Bullet Lifesteal', 'Spirit Lifesteal', 'Berserker', 'Extra Charge', 'Bullet Resist Shredder', 'Spirit Resilience'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
 'G4_berserker_before_health': GEIST_COMMON_EARLY + ['Healing Booster', 'Berserker', 'Spirit Resilience', 'Extra Charge', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
 'G5_EC_right_after_drainT3': ['Monster Rounds', 'Extra Regen', 'Mystic Regeneration', 'Extra Stamina', 'Kinetic Dash', 'Cultist Sacrifice', 'Extra Charge', 'Radiant Regeneration', 'Healing Booster', 'Spirit Resilience', 'Berserker', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
 'G7_lifesteal_before_berserker (all T2 by 20k)': GEIST_COMMON_EARLY + ['Healing Booster', 'Spirit Resilience', 'Extra Charge', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal', 'Berserker'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
 'G6_health_rush_before_gun': ['Monster Rounds', 'Extra Regen', 'Mystic Regeneration', 'Extra Stamina', 'Healing Booster', 'Spirit Resilience', 'Kinetic Dash', 'Cultist Sacrifice', 'Radiant Regeneration', 'Berserker', 'Extra Charge', 'Bullet Resist Shredder', 'Bullet Lifesteal', 'Spirit Lifesteal'] + GEIST_TAIL + ['Rapid Recharge', 'Refresher'],
}

# ---------------- rat king grenade ----------------
def rk_metric(R, w, H, AB):
    own = w['own']
    vb = max([bo for th, bo in AB if inv(w)['v'] >= th] or [0])
    bh = sum(T.sv(i, 'BonusBaseHealth') for i in own)
    hp = (800 + 50 * w['boons']) * (1 + (vb + bh) / 100) + sum(T.sv(i, 'BonusHealth') for i in own)
    if any(i.get('class') == 'upgrade_non_player_bonus_sacrifice' for i in own): hp += 4 * w['boons']
    cond = {'upgrade_regenerating_bullet_shield', 'upgrade_hollow_point_rounds'}
    def wdsum(c):
        x = w['wb']
        for i in own:
            if i.get('class') in cond and not c: continue
            x += T.sv(i, 'BaseAttackDamagePercent')
            if i.get('class') == 'upgrade_non_player_bonus_sacrifice': x += 0.8 * w['boons']
        return x
    wd_c, wd_u = wdsum(True), wdsum(False)
    br = 1.0
    for i in own:
        x = T.sv(i, 'BulletResist')
        if x: br *= (1 - x / 100)
    ms = sum(T.sv(i, 'BonusMoveSpeed') for i in own); spr = sum(T.sv(i, 'BonusSprintSpeed') for i in own)
    res = {'hp': round(hp), 'cape(15%/25%maxhp)': None, 'wd% >65%hp/<65%': f"{wd_c:.0f}/{wd_u:.0f}", 'bulletres%': round((1 - br) * 100), 'move/sprint m': f"{ms:g}/{spr:g}"}
    a = R['abil'][1]; cdr = 1.0
    for i in own:
        x = T.sv(i, 'CooldownReduction')
        if x and i.get('class') in ('upgrade_cooldown_reduction', 'upgrade_magic_tempo', 'upgrade_absorbing_armor'): cdr *= (1 - x / 100)   # Superior / Compress (imbued on grenade) / Witchmail
    for m, tt in (('A', w['tA']), ('Astrict', w['tS']), ('B', w['tB'])):
        t = tt[1]; P = T.at_tier(a, t)
        per = T.pv(P, 'DamagePerShrapnel') + 0.6 * wd_c; det = T.pv(P, 'Detonations')
        big = (300 + 1.0 * wd_c) if t >= 3 else 0
        cd = T.pv(P, 'AbilityCooldown') * cdr
        res['gren_' + m] = f"{T.tlabel(t)} {per:.0f}x{det:g}{'+' + format(big, '.0f') if big else ''} = {per * det + big:.0f} cd{cd:.1f} -> {(per * det + big) * 60 / cd:.0f}/min"
    t3 = w['tA'][3]; res['cape(15%/25%maxhp)'] = round(hp * (0.25 if t3 >= 3 else 0.15)) if t3 >= 0 else 'locked'
    return res

RK_MID = ['Extra Health', 'Fortitude', 'Hollow Point', 'Mystic Expansion', 'Compress Cooldown', 'Ballistic Enchantment', 'Superior Cooldown', 'Greater Expansion']
RK_LATE = ['Echo Shard', 'Witchmail', 'Colossus']
RIMB = {'Mystic Expansion': 1, 'Compress Cooldown': 1, 'Ballistic Enchantment': 1, 'Echo Shard': 1}
RK = {
 'R0_cleanbase': ['Extended Magazine', 'Monster Rounds', 'Cultist Sacrifice', 'Titanic Magazine', 'Battle Vest', 'Sprint Boots', 'Enduring Speed'] + RK_MID + RK_LATE,
 'R1_current': ['Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Sprint Boots', 'Enduring Speed', 'Cultist Sacrifice'] + RK_MID + ['Battle Vest'] + RK_LATE,
 'R2_titanic_first_BV_early': ['Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Cultist Sacrifice', 'Battle Vest', 'Sprint Boots', 'Enduring Speed'] + RK_MID + RK_LATE,
 'R3_health_before_boots': ['Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Cultist Sacrifice', 'Battle Vest', 'Extra Health', 'Fortitude', 'Sprint Boots', 'Enduring Speed'] + RK_MID[2:] + RK_LATE,
 'R4_boots_first_BV_early': ['Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Sprint Boots', 'Enduring Speed', 'Cultist Sacrifice', 'Battle Vest'] + RK_MID + RK_LATE,
 'R6_health_4800_by_8000 (validator main=health)': ['Extra Health', 'Battle Vest', 'Fortitude', 'Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Cultist Sacrifice', 'Sprint Boots', 'Enduring Speed', 'Hollow Point'] + RK_MID[3:] + RK_LATE,
 'R5_hollow_before_health': ['Extended Magazine', 'Monster Rounds', 'Titanic Magazine', 'Cultist Sacrifice', 'Battle Vest', 'Sprint Boots', 'Enduring Speed', 'Hollow Point', 'Extra Health', 'Fortitude'] + RK_MID[3:] + RK_LATE,
}

if __name__ == '__main__':
    bid = sys.argv[1]; base = [x for x in T.load_builds() if x['id'] == bid][0]
    order = [int(c) for c in (sys.argv[2] if len(sys.argv) > 2 else ''.join(map(str, base['order'])))]
    V = G if bid == 'geist' else RK; met = geist_metric if bid == 'geist' else rk_metric
    res = run(base, [(k, v, RIMB if bid != 'geist' else None) for k, v in V.items()], order, met)
    print('# path comparison', bid, 'order', ''.join(map(str, order)), '(CALCULATED, unvalidated; gt/repo 6801 data == 6819)')
    for lab, r in res.items():
        print(f"\n## {lab}  end {r['end']}  4.8k: {r['spike4800']}  6.4k: {r['spike6400']}")
        print('   core: ' + ' > '.join(r['core']))
        for p in r['points']:
            print(f"   @{p['souls']:>5} g{p['inv']['w']}/s{p['inv']['s']}/v{p['inv']['v']} | " + ' | '.join(f"{k} {v}" for k, v in p.items() if k not in ('souls', 'inv')))

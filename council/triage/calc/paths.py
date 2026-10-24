# Section N path comparison for candidate builds (not data.js). usage: python3 -I paths.py <label>=<build.json> ... [--ck 2400,3200,...]
# Uses council/tools/abtimeline.py (analyse/state) unchanged; reports, at each soul checkpoint, the state of the last purchase <= checkpoint:
# investment per colour + bonus, spirit power (all / unconditional), weapon damage % (all / unconditional on HP%), bullet/spirit resist, bonus health,
# barrier, ability tiers under model A (default queues), model A strict (single queue) and model B, and the key ability numbers.
import sys, os, json, re
SP = '/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad'
sys.path.insert(0, SP + '/council/tools'); import abtimeline as T
args = sys.argv[1:]; ck = [2400, 3200, 4000, 4800, 5600, 6400, 8000, 9600, 12000, 16000, 20000, 25600, 30400, 36800]
if '--ck' in args: i = args.index('--ck'); ck = [int(x) for x in args[i + 1].split(',')]; args = args[:i] + args[i + 2:]
COND = {'upgrade_magic_shield', 'upgrade_regenerating_bullet_shield', 'upgrade_hollow_point_rounds', 'upgrade_arcane_surge'}  # self-HP or dash-conditional bonuses
def sv(i, k): return T.sv(i, k)
for a in args:
    lab, f = a.split('=', 1); b = json.load(open(f))
    R = T.analyse(b); evS = T.model_A(R['order'], R['L'], strict=True); sp = T.spikes(R)
    print(f"## {lab}  ({f})  order {''.join(map(str, R['order']))}")
    print('   4.8k/6.4k held at: ' + ', '.join(f"{c} {d['4800']}/{d['6400']}" for c, d in sp.items()))
    rows = [w for w in R['rows'] if not w.get('unknown')]
    for s in ck:
        w = [x for x in rows if x['souls'] <= s]
        if not w: continue
        w = T.state(R, dict(w[-1], souls=s)); own = w['own']
        inv = {c: sum(T.SOULS[i['tier']] for i in own if i['slot'] == k) for k, c in T.COLS.items()}
        wd_all = w['wb'] + sum(sv(i, 'BaseAttackDamagePercent') for i in own if i['class'] != 'upgrade_magic_shield')
        wd_unc = w['wb'] + sum(sv(i, 'BaseAttackDamagePercent') for i in own if i['class'] not in COND)
        # Cultist: +0.8/boon on weapon damage, +4/boon health (buff, 160s of 270s)
        for i in own:
            if i['class'] == 'upgrade_non_player_bonus_sacrifice': wd_all += 0.8 * w['boons']; wd_unc += 0.8 * w['boons']
        fr = sum(sv(i, 'BonusFireRate') for i in own if i['class'] not in ('upgrade_magic_shield',))
        br = 1.0; sr = 1.0
        for i in own: br *= 1 - sv(i, 'BulletResist') / 100; sr *= 1 - sv(i, 'TechResist') / 100
        hp = sum(sv(i, 'BonusHealth') for i in own) + sum(4 * w['boons'] for i in own if i['class'] == 'upgrade_non_player_bonus_sacrifice') \
             + sum(5 * w['boons'] for i in own if False)
        bar = sum(sv(i, 'CombatBarrier') for i in own)
        def tl(ev, sl): t = T.tiers_at(ev, s)[sl]; return T.tlabel(t)
        tiers = ' '.join(f"{T.nm(R, sl)[:8]}:{tl(R['evA'], sl)}/{tl(evS, sl)}/{tl(R['evB'], sl)}" for sl in (1, 2, 3, 4))
        key = []
        for sl in (1, 2, 3, 4):
            t = w['tA'][sl]
            if t < 0: continue
            P = T.at_tier(R['abil'][sl], t); cd = T.pv(P, 'AbilityCooldown'); du = T.pv(P, 'AbilityDuration')
            h = T.spirit_hits(P, T.slot_sp(R, w, sl, t))
            if h: key.append(f"{T.nm(R, sl)[:8]} " + ','.join(f"{k[:6]}={v:.0f}" for k, (v, inst) in list(h.items())[:2]) + (f" cd{cd:g}" if cd else '') + (f" d{du:g}" if du else ''))
        if b['hero'] == 'Venator':  # weapon-scaled abilities (EBaseWeaponDamageIncrease)
            key.append(f"grenade {35 + wd_all:.0f} ({35 + wd_unc:.0f} <65%hp)  gutshot {60 + 0.7 * wd_all:.0f}")
        print(f"  @{s:>5} last={w['n'][:20]:<20} inv g{inv['gun']}/s{inv['spirit']}/v{inv['vitality']} bonus g+{w['wb']:.0f}% s+{w['tb']:.0f} | SP {w['sp']:.0f} (unc {w['sp_unc']:.0f}) | wd% {wd_all:.0f} (unc {wd_unc:.0f}) fr+{fr:.0f}% | BR {100*(1-br):.0f}% SR {100*(1-sr):.0f}% | +hp {hp:.0f} barrier {bar:.0f}")
        print(f"         tiers A/Astrict/B: {tiers}")
        if key: print('         ' + ' | '.join(key))
    print()

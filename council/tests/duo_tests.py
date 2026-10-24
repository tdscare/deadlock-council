"""Known-answer tests against raw vdata + false-positive spot checks for the duo engine. Run: python3 -I council/tests/duo_tests.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'lib', 'duo'))
import gamedata as G, kit, shred, synergy, engine, rules
R = []
def T(name, ok, detail=''):
    R.append(ok); print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
def close(a, b, e=1e-6): return a is not None and abs(a - b) < e

# ---- known answers from raw vdata (SteamDatabase dump gt6819)
a = G.Ability('ability_deadpack_flamethrower')
T('Danny Jettison Fuel BulletResistReduction base -15', close(a.p('BulletResistReduction', 0), -15), a.p('BulletResistReduction', 0))
T('Danny Jettison Fuel BulletResistReduction tier3 -25', close(a.p('BulletResistReduction', 3), -25), a.p('BulletResistReduction', 3))
inv = {(i['item'], i['type']): i for i in shred.item_inventory()}
T('Bullet Resist Shredder base 10', close(inv[('Bullet Resist Shredder', 'bullet')]['pct'], 10))
T('Hollow Point base 10', close(inv[('Hollow Point', 'bullet')]['pct'], 10))
ac = inv[('Alchemical Fire', 'bullet')]
T('Alchemical Fire 7 + 0.055/spirit', close(ac['pct'], 7) and close(ac['spirit_scale'], 0.055), (ac['pct'], ac['spirit_scale']))
K = kit.all_kits()
T('Hunter\'s Aura is an aura-trigger shred', inv[("Hunter's Aura", 'bullet')]['trigger'] == 'aura (range)')
# Warden Binding Word hold is conditional; Shocking Reanimation slow is death-triggered -> unusable
warden = K['hero_warden']
bw = [o for o in warden.offers if o['aname'] == 'Binding Word' and o['kind'].startswith('cc')]
T('Warden Binding Word offer carries a condition', bool(bw) and all(o.get('condition') or o.get('conditional') for o in bw), [sorted(o.keys())[:6] for o in bw][:1])
sr = [o for o in K['hero_necro'].offers if 'Reanimation' in o['aname']] + [o for k in K.values() for o in k.offers if 'Reanimation' in o['aname']]
T('Shocking Reanimation slow is death-triggered/unusable', bool(sr) and all(o.get('unusable') for o in sr if o['kind'].startswith('slow')), len(sr))
# Burrow is not a rooted channel
b = G.Ability('ability_burrow')
T('Burrow ChannelMoveSpeed -1 (not rooted)', close(b.p('ChannelMoveSpeed', 0), -1) or b.p('ChannelMoveSpeed', 0) is None, b.p('ChannelMoveSpeed', 0))
# Sleep wakes 0.1s after damage
s = G.Ability('ability_sleep_dagger')
T('Sleep Dagger SleepWakeUpDelay 0.1', close(s.p('SleepWakeUpDelay', 0), 0.1), s.p('SleepWakeUpDelay', 0))

# ---- false-positive spot checks on the engine
out, _ = engine.run_ability()
by = {}
for c in out: by.setdefault(c['classification'], []).append(c)
def find(cn, pn, rule=None, need=None):
    return [c for c in out if c['cname'] == cn and c['pname'] == pn and (rule is None or c['rule'] == rule) and (need is None or c['need']['aname'] == need)]
sleep_holds = [c for c in out if c['pname'] == 'Haze' and c['rule'] == 'HOLD' and c['classification'] in ('GENUINE MECHANICAL SYNERGY', 'DEDICATED DUO STRATEGY (candidate)')]
T('no sleep-based HOLD promoted (sleep breaks on damage)', not sleep_holds, len(sleep_holds))
T('no pair is promoted to genuine/dedicated on unverified mechanics', not by.get('GENUINE MECHANICAL SYNERGY') and not by.get('DEDICATED DUO STRATEGY (candidate)'), {k: len(v) for k, v in by.items()})
rej = by.get('REJECTED', [])
T('rejections each carry a numeric reason', rej and all(c['reasons'] and any(ch.isdigit() for ch in c['reasons'][0]) for c in rej), len(rej))
top = [c for c in by.get('UNPROVEN IDEA', []) if c['stats'] and c['stats']['median'] > 0.2]
T('top unproven names its unknown', top and all(c['unknown'] for c in top), [(c['cname'], c['pname']) for c in top][:3])
out2, _ = engine.run_ability()
T('rank is deterministic (two runs identical classification counts)', sorted(c['classification'] for c in out) == sorted(c['classification'] for c in out2))
print('%d/%d passed' % (sum(R), len(R))); sys.exit(0 if all(R) else 1)

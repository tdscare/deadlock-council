#!/usr/bin/env python3
"""Generate lint-valid sandbox test requests for the independent (novel) hypotheses N01-N10 (offline; queues nothing).
usage: python3 -I council/tools/novel_scenarios.py [--out DIR]    default DIR=/mnt/user-data/outputs/arena/sc_novel
Each file carries: question, why it matters for a build decision, predicted outcomes per explanation (pre-registered, numbers computed here
from game-data fields), the decision rule, the builds the answer changes, and an A-B-A bracketed, order-reversed block sequence.
Only verified runner ops are used: hardreset basemods give imbueown enemies fetch eitem accuracy fire cast(1-4,iN,reload) mods cds eresist lowhp wait mark.
"""
import json, os, sys, ast, subprocess, itertools
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(C, 'tools'))
import imbue_audit as A
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/mnt/user-data/outputs/arena/sc_novel'
SRC = 'council/evidence/interactions/novel/novel_hypotheses.json'
B = json.load(open('/tmp/builds_dump.json'))
W = {n: c for c, v in A.I.items() for n in [v['name']]}   # item name -> class

def builds_with(names, hero_ok=None):
    return [b['id'] for b in B if any(i['name'] in names for i in b['items']) and (hero_ok is None or hero_ok(b))]
def cls(n): return W[n]

# ---------------------------------------------------------------- generic file writer
def write(fn, meta, setup, blocks):
    L = ['# novel-hypothesis test request (council/tools/novel_scenarios.py). Offline-generated; the tester agent is the only executor.']
    for k, v in meta:
        assert '#' not in v, (k, v)
        L.append('meta %s %s' % (k, v))
    L += setup
    for b in blocks: L += b
    L.append('end')
    open(os.path.join(OUT, fn), 'w').write('\n'.join(L) + '\n')

def block(label, gives=(), imbues=(), ops=(), pre=(), enemies='enemies 1 300 4', fetch='fetch 350', reload=False, lowhp=None, after=('wait 2',)):
    b = ['hardreset', 'souls 30000']
    b += ['give ' + g for g in gives]
    b += ['imbueown %s %s' % (i, s) for i, s in imbues]
    b += ['basemods', enemies]
    b += list(pre)
    b += [fetch]
    if lowhp: b.append('lowhp %d' % lowhp)
    if reload: b.append('cast reload 2.5')
    b.append('mark ' + label)
    b += list(ops)
    b += ['mark none']
    if lowhp: b.append('lowhp 0')
    b += list(after)
    return b

def aba(arms):
    """arms: list of (label, kwargs). Sequence: forward, then reversed with a prime on each label (order alternation, first arm brackets)."""
    fw = [(l, kw) for l, kw in arms]
    bw = [(l + '_rev', kw) for l, kw in reversed(arms)]
    return fw + bw

def common_meta(kind_q, purpose, mechanics, hero, items, expected, checkpoint=30000, extra=()):
    m = [('kind', 'INTERACTION'), ('question', kind_q), ('purpose', purpose), ('mechanics', mechanics),
         ('expectedstate', 'souls=%d items=%s' % (checkpoint, ','.join(items))), ('build', hero), ('checkpoint', str(checkpoint)),
         ('items', ' '.join(items)), ('strategy_source', SRC)]
    return m + list(extra)

def cond_meta(scope, used, excl, acc, misses, act, dist, targets, readbacks):
    return [('cond_scope', scope), ('cond_abilities_used', used), ('cond_abilities_excluded', excl), ('cond_accuracy', acc), ('cond_misses', misses),
            ('cond_start_stacks', '0 (hardreset before every block)'), ('cond_activations', act), ('cond_distance', dist), ('cond_targets', targets), ('readbacks', readbacks)]

def player(title, what, why, short, expect):
    return [('player_title', title), ('player_what', what), ('player_why', why), ('player_short', short), ('player_expect', expect)]

os.makedirs(OUT, exist_ok=True)
written = []

# ================================================================ N01 multi-imbue on one ability (Haze, Sleep Dagger = Signature1)
CC, SG = cls('Compress Cooldown'), cls('Surge of Power')
n01_builds = [b for b in A.audit(B).values() if any(f[0] == 'DEPENDS-ON-N01' for f in b['findings'])]
arms = [('P0_none', {}),
        ('A_CC_only', dict(gives=[CC], imbues=[(CC, 'Signature1')])),
        ('B_Surge_only', dict(gives=[SG], imbues=[(SG, 'Signature1')])),
        ('C_CC_then_Surge', dict(gives=[CC, SG], imbues=[(CC, 'Signature1'), (SG, 'Signature1')])),
        ('D_Surge_then_CC', dict(gives=[CC, SG], imbues=[(SG, 'Signature1'), (CC, 'Signature1')])),
        ('G_Surge_on_other_slot', dict(gives=[SG], imbues=[(SG, 'Signature2')]))]
body = ['cast 1 0.8', 'cds', 'wait 1.5', 'cds']
blocks = [block(l, ops=body, **kw) for l, kw in aba(arms)] + [block('P0_end', ops=body)]
meta = common_meta(
    "Checking what happens when two imbue items are put on the same ability: do both work, does the last one replace the first, or is the second refused?",
    "decides how %d of %d builds should use their imbue items: %d builds put 2-5 imbue items on one ability (%d item placements would be unused if the game allows only one per ability)" % (len(n01_builds), len(B), len(n01_builds), 104),
    "game data (abilities.vdata) gives each imbue item a behaviour type (ACTIVE / ACTIVE_NON_ULT / MODIFIER_VALUE) but no per-ability capacity field; replace vs refuse vs stack is not in the data (UNRESOLVED). Sleep Dagger is used because both effects are readable: Compress Cooldown shows in the ability cooldown (cds), Surge of Power adds imbued Spirit Power (ImbuedTechPower 28 x damage scale 2.2 = +61.6 dagger damage before resists, MODELLED)",
    'haze', [CC, SG], '',
    extra=[('feeds', 'novel hypothesis N01 (imbue capacity); council/evidence/interactions/imbue_audit/IMBUE_AUDIT.txt section C lists the %d affected builds' % len(n01_builds)),
           ('prediction_STACK', 'both effects show in C and D, in either order: dagger cooldown in C/D is about the same as A, and dagger damage is about B (+61.6 over P0)'),
           ('prediction_REPLACE_LAST', 'C shows only Surge (damage up, cooldown = P0); D shows only Compress Cooldown (cooldown down, damage = P0): the order of purchase decides'),
           ('prediction_FIRST_WINS_OR_REFUSE', 'C shows only Compress Cooldown, D only Surge; the plugin log line for the second imbueown says refused/false/error'),
           ('prediction_SURGE_GLOBAL', 'in G dagger damage rises although Surge sits on another ability: then its Spirit Power is not ability-bound and must be valued as a flat stat'),
           ('decision_rule', 'STACK: keep all builds, model adds the effects. REPLACE or REFUSE: every build with 2+ imbue items on one ability loses the extra items (IMBUE_AUDIT.txt section C): re-split the imbues across abilities or drop the surplus items, builds owner proposes through the gate. Mixed (same-type refused, different-type stacks): this file cannot separate it (needs a duration readback), record as PARTIAL'),
           ('changes_builds', ', '.join(b['build'] for b in n01_builds[:60])),
           ('unresolved_if', 'cooldown readback is garbage (cds reports end=0 or values above 1000 s) in P0: INVALID, report the raw cds lines'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: largest build exposure of any open question (56 of 81 builds) and no capacity field in the game data, so the answer cannot be reasoned out'),
           ('alternative_reason', 'P0 and single-imbue arms A, B are the controls; C vs D tests order; G tests whether Surge is bound to its ability'),
           ('required_levels', '1=4;2=1;3=1;4=1'), ('levels_mode', 'fixed'),
           ('required_activation', 'cast1|ability|ability_sleep_dagger|1'), ('required_readback', 'items_ok|1|==|1 ; dmg_hits|hits|>|0'),
           ('rotation', 'P0, A, B, C, D, G then the same arms in reverse order, P0 last (bracketing control); one Sleep Dagger cast per block, 350u'),
           ('stack_track', 'none')] + cond_meta('ability 1 cast only (no gun)', 'cast 1', 'gun, other abilities', 'n/a', 'none', 'imbueown for each item, Sleep Dagger', '350u', 'enemies=1 allies=0',
            'equipped_items,ability_tiers,ability_cast:1,imbueown_log,cds_after_cast,dmg_row_of_ability_1') + player('Two imbues on one ability', 'Compress + Surge on a dagger', 'Do extra imbues stack?', 'Stacking imbues', 'Both work, or one is lost') + [('result_says', 'WORKS (stack) if C and D show both effects; DOES NOT WORK if only one effect shows or the second imbueown is refused; the order of C and D says which one survives')])
write('nv_N01_multi_imbue.txt', meta, ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 15 1 1 1', 'souls 30000'], blocks)
written.append('nv_N01_multi_imbue.txt')

# ================================================================ N02 bullet-resist reducer stacking (Haze)
BRS, HA, CH = cls('Bullet Resist Shredder'), cls("Hunter's Aura"), cls('Crippling Headshot')
BASE = cls('Bullet Resilience')
base = 0.30
def pred(reds, b, model):
    if model == 'ADD': r = b - sum(reds)
    elif model == 'MAX': r = b - max(reds or [0])
    elif model == 'FRAC': r = b
    else: r = b
    if model == 'FRAC':
        for x in reds: r *= (1 - x)
    if model == 'ADD_DIM':
        rs = sorted(reds, reverse=True); r = b - sum(x * (1 if i == 0 else 0.5) for i, x in enumerate(rs))
    return (1 - r) / (1 - b)
RED = dict(BRS=0.10, HA=0.20, CH=0.16)  # HA doubled with one enemy hero nearby (SingleTargetPlayerMultiplier 2.0 on BulletArmorReduction -10)
conds = [('N_30', [], 0.30), ('BRS_30', ['BRS'], 0.30), ('HA_30', ['HA'], 0.30), ('BRS_HA_30', ['BRS', 'HA'], 0.30),
         ('Nh_30', [], 0.30), ('CH_30', ['CH'], 0.30), ('BRS_CH_30', ['BRS', 'CH'], 0.30), ('N_0', [], 0.0), ('BRS_HA_0', ['BRS', 'HA'], 0.0)]
tbl = []
for lab, rs, b in conds:
    v = [RED[x] for x in rs]
    tbl.append('%s: ADD %.3f | ADD with 2nd source x0.5 %.3f | MAX %.3f | FRACTION-OF-RESIST %.3f' % (lab, pred(v, b, 'ADD'), pred(v, b, 'ADD_DIM'), pred(v, b, 'MAX'), pred(v, b, 'FRAC')))
gv = {'BRS': [BRS], 'HA': [HA], 'CH': [CH]}
def arm2(lab, rs, b, head=False):
    gives = [x for r in rs for x in gv[r]]
    pre = ['eitem ' + BASE] if b > 0 else []
    ops = ['accuracy 1 %d' % (1 if head else 0), 'cast 1 0.8', 'wait 0.6', 'fire 2', 'acclog']
    return (lab, dict(gives=gives, pre=pre, ops=ops, reload=False))
arms = [arm2(l, rs, b, head=l.startswith(('Nh', 'CH', 'BRS_CH'))) for l, rs, b in conds]
blocks = [block(l, **kw) for l, kw in aba(arms)] + [block('N_30_end', pre=['eitem ' + BASE], ops=['accuracy 1 0', 'cast 1 0.8', 'wait 0.6', 'fire 2', 'acclog'])]
pairs_b = [b['id'] for b in B if {'Bullet Resist Shredder', 'Crippling Headshot'} <= {i['name'] for i in b['items']} or {'Bullet Resist Shredder', "Hunter's Aura"} <= {i['name'] for i in b['items']}]
meta = common_meta(
    "Checking whether two bullet-resist reducers add up, take only the stronger one, or each remove a share of what is left (and whether they do anything on an enemy with no bullet resist).",
    "decides whether the second reducer is worth its souls: %d builds hold Bullet Resist Shredder together with Hunter's Aura or Crippling Headshot, and 22 builds hold 2+ reducers of any kind" % len(pairs_b),
    "each reducer applies its own debuff (items.json: BulletArmorReduction on Bullet Resist Shredder -10 and Hunter's Aura -10, doubled with one enemy hero near = -20 (SingleTargetPlayerMultiplier 2); BulletResistReduction on Crippling Headshot -16 with DiminishingMultiplier 0.5). The combining rule and whether the number is percentage points or a share of the target's resist are engine-side (UNRESOLVED). The target gets 30 percent bullet resist from Bullet Resilience (verified 34.8 -> 24.4 per bullet); two arms use 0 percent",
    'haze', [BRS, HA, CH], '',
    extra=[('feeds', 'novel hypothesis N02 (resist reducer stacking); extends duo_D1_shred_formula with the cross-family pair and the diminishing multiplier'),
           ('prediction_table', 'ratio of mean damage per bullet to the matching no-reducer arm, for resist 30 percent unless the label ends _0. ' + ' || '.join(tbl)),
           ('prediction_reading', 'ADD column = reductions are percentage points and add; ADD with 2nd source x0.5 = the DiminishingMultiplier halves every later source; MAX = only the strongest applies; FRACTION = each takes that share of the remaining resist (then BRS_HA_0 must be 1.00: nothing to remove). If ADD or ADD-with-x0.5 holds on an enemy with 0 resist, the ratio exceeds 1 (negative resist amplifies)'),
           ('decision_rule', 'match each arm to the nearest column (within 0.02). ADD: both reducers are worth their price, model credits the sum. MAX or ADD with x0.5: the second reducer is worth less than half in the builds in changes_builds, builds owner replaces it. FRACTION: reducers matter only against high-resist enemies, so value them by target resist in the model. No column within 0.02: INSUFFICIENT, report the three ratios'),
           ('changes_builds', ', '.join(pairs_b)),
           ('unresolved_if', 'N_30 vs N_30_end per-bullet damage differ by more than 3 percent (drift), or Nh_30 is not about 1.65 times N_30 (headshots not registering): head arms INVALID; BRS arms need the Sleep Dagger hit to land (dmg row for ability 1 present)'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: reducers are bought in 22 builds, the combining rule is not in the data, and the data hints at three different rules (two property names, a DiminishingMultiplier on one item)'),
           ('alternative_reason', 'the same sequence with Sleep Dagger cast in every arm so the only difference is the items'),
           ('required_levels', '1=4;2=1;3=1;4=1'), ('levels_mode', 'fixed'),
           ('required_activation', 'cast1|ability|ability_sleep_dagger|1'), ('required_readback', 'items_ok|1|==|1 ; dmg_hits|hits|>|0'),
           ('rotation', 'Sleep Dagger once, 0.6 s later 3 s of gun fire at 350u, 100 percent accuracy (body only; head arms use all-head), arms bracketed by the no-reducer control and run in reverse in the second half'),
           ('stack_track', 'none')] + cond_meta('ability 1 cast + gun', 'cast 1, gun', 'abilities 2-4', '100 percent body (head arms: 100 percent head)', 'none', 'Bullet Resist Shredder (needs the dagger hit), Hunter\'s Aura (passive), Crippling Headshot (needs headshots)', '350u', 'enemies=1 allies=0',
            'equipped_items,ability_tiers,distance_m,ability_cast:1,dmg_per_bullet_by_arm,enemy_resist_modifier') + player('Do resist shreds stack?', 'Two bullet shreds on one target', 'Is the 2nd shred worth buying?', 'Shred stacking', 'More damage, or none extra') + [('result_says', 'WORKS if the two-reducer arms deal clearly more per bullet than the best single reducer arm (ADD or FRACTION column); DOES NOT WORK if they equal the best single arm (MAX)')])
write('nv_N02_resist_reducer_stacking.txt', meta, ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 15 1 1 1', 'souls 30000'], blocks)
written.append('nv_N02_resist_reducer_stacking.txt')

# ================================================================ N03 ability-only procs vs bullet-borne spirit damage (Haze with Mystic Shot as the carrier)
MS, SLOW = cls('Mystic Shot'), cls('Mystic Slow')
five = ['Mystic Slow', 'Suppressor', 'Healbane', 'Escalating Exposure', 'Mystic Vulnerability']
b45 = builds_with(set(five))
arms = [('K_slow_dagger', dict(gives=[SLOW], ops=['cast 1 0.8', 'wait 0.3', 'mods', 'wait 0.5', 'mods'])),
        ('N_slow_bullets', dict(gives=[SLOW], ops=['accuracy 1 0', 'fire 0.5', 'mods', 'wait 0.5', 'mods'])),
        ('T_slow_MysticShot', dict(gives=[SLOW, MS], ops=['accuracy 1 0', 'fire 0.5', 'mods', 'wait 0.5', 'mods'])),
        ('T2_MysticShot_only', dict(gives=[MS], ops=['accuracy 1 0', 'fire 0.5', 'mods']))]
blocks = [block(l, **kw) for l, kw in aba(arms)] + [block('K_end', gives=[SLOW], ops=['cast 1 0.8', 'wait 0.3', 'mods'])]
meta = common_meta(
    "Checking whether spirit damage that rides on a bullet (Mystic Shot's bonus) is counted as ability damage by items that only react to ability damage (Mystic Slow).",
    "decides if the five ability-damage-only items (Mystic Slow, Suppressor, Healbane, Escalating Exposure, Mystic Vulnerability, held by %d builds) work on heroes whose spirit damage is attached to bullets; 7 of those builds are such heroes (Seven, Victor, Wraith, Mina, Vindicta)" % len(b45),
    "abilities.vdata lists only CITADEL_DAMAGETYPE_ABILITY in m_vecProcDamageTypes for all five (VERIFIED MECHANIC). The damage type of bullet-attached spirit damage is not in the data. PROXY: Mystic Shot (ProcBonusMagicDamage on the next bullet) is the only bullet-borne spirit damage a verified hero (Haze) can produce; transfer to the hero-specific kits (Wraith Full Auto, Gigawatt Power Surge) is UNVERIFIED and is the follow-up once a cast/state check exists for them",
    'haze', [SLOW, MS], '',
    extra=[('feeds', 'novel hypothesis N03 (ability-only proc items)'),
           ('prediction_K', 'positive control: the dagger (ABILITY damage) applies the Mystic Slow modifier to the enemy within 1 s (mods shows a new enemy modifier). If it does not, the whole file is INVALID'),
           ('prediction_N', 'negative control: plain bullets (BULLET damage) do NOT apply it (text and proc list say ABILITY only)'),
           ('prediction_T_if_ability', 'the Mystic Shot bonus row in the damage csv has dmg_type Ability and the slow modifier appears after the first bullet'),
           ('prediction_T_if_bullet', 'the bonus row has dmg_type Bullet (or merges into the bullet row) and no slow modifier appears'),
           ('decision_rule', 'bonus row Ability AND slow appears: bullet-borne spirit damage counts, the five items stay in the builds in changes_builds (follow-up on Wraith/Gigawatt for confirmation). Bonus row Bullet or no slow: bullet-borne spirit damage does NOT trigger them: builds owner reviews the %d builds in changes_builds on bullet-spirit heroes and swaps the five items there; INCONCLUSIVE if K fails' % len(b45)),
           ('changes_builds', ', '.join(b45)),
           ('unresolved_if', 'K arm shows no slow modifier, or T2 shows no extra spirit row (Mystic Shot did not fire; its cooldown is 8 s so only the first shot of each block can carry it)'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: five items are bought in 45 builds and the data says they only react to ability damage, so the damage type of bullet-attached spirit is a build-relevant unknown'),
           ('alternative_reason', 'K and N are the positive and negative controls inside the file'),
           ('required_levels', '1=4;2=1;3=1;4=1'), ('levels_mode', 'fixed'), ('required_readback', 'items_ok|1|==|1 ; dmg_hits|hits|>|0'),
           ('rotation', 'K dagger cast; N 0.5 s of gun fire; T gun fire with Mystic Shot; T2 Mystic Shot only; bracketed and reversed; mods read twice per block'),
           ('stack_track', 'none')] + cond_meta('gun only, except arm K (ability 1 cast)', 'gun; cast 1 in K only', 'abilities 2-4', '100 percent body', 'none', 'Mystic Shot on the first bullet', '350u', 'enemies=1 allies=0',
            'equipped_items,distance_m,enemy_modifier_names,dmg_type_of_bonus_row') + player('Spirit on bullets: ability?', 'Mystic Shot vs Mystic Slow', 'Do slow items fire on it?', 'Bullet spirit test', 'Slow appears or not') + [('result_says', 'WORKS if the Mystic Shot bonus is typed Ability and Mystic Slow appears; DOES NOT WORK if it is typed Bullet and no slow appears (while K shows the slow)')])
write('nv_N03_ability_proc_on_bullet_spirit.txt', meta, ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 15 1 1 1', 'souls 30000'], blocks)
written.append('nv_N03_ability_proc_on_bullet_spirit.txt')

# ================================================================ N04 next-bullet items on pellets (Haze 1 bullet vs Drifter 3 pellets)
EXP = cls('Express Shot')
def weapon_info():
    L = open('/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/gt6819/game/citadel/pak01_dir/scripts/abilities.vdata', errors='replace').read().split('\n')
    import re
    out = {}
    for i, l in enumerate(L):
        m = re.match(r'^\t(citadel_weapon_\w+_set)\s*=\s*$', l)
        if m:
            e = i + 1
            while L[e] != '\t}': e += 1
            d = {}
            for j in range(i, e):
                for k in ('m_iBullets', 'm_iBurstShotCount'):
                    mm = re.match(r'\s*%s = (\d+)' % k, L[j])
                    if mm: d[k] = int(mm.group(1))
            out[m.group(1)] = d
    return out
WI = weapon_info()
def multi(b):
    h = A.H.get(b['hk']);
    if not h: return False
    for a in h['abilities']:
        if a['slot'] == 'weapon' and a['cls'] in WI:
            d = WI[a['cls']]; return d.get('m_iBullets', 1) > 1 or d.get('m_iBurstShotCount', 1) > 1
    return False
nb = {'Headshot Booster', 'Mystic Shot', 'Headhunter', 'Express Shot', 'Restorative Shot'}
b04 = builds_with(nb, multi)
def arms04():
    r = []
    for lab, gv_ in [('X0', []), ('M', [MS]), ('E', [EXP]), ('ME', [MS, EXP])]:
        r.append((lab, dict(gives=gv_, ops=['accuracy 1 0', 'fire 1.3', 'acclog'], reload=True)))
    return r
blocksH = [block('H_' + l, **kw) for l, kw in aba(arms04())]
blocksD = [block('D_' + l, **kw) for l, kw in aba(arms04())]
meta = common_meta(
    "Checking whether a 'next bullet' item gives its bonus to one pellet or to every pellet of a multi-pellet shot, and what Express Shot does to a shotgun-style shot.",
    "decides if next-bullet items (Mystic Shot, Headshot Booster, Headhunter, Restorative Shot, Express Shot) are worth buying on multi-pellet or burst weapons: %d builds hold one on such a hero" % len(b04),
    "the data caps these items at one bullet per shot (m_flMaxBulletsToProcInShot=1, no multiple procs per shot or per target; VERIFIED MECHANIC). Drifter's weapon fires m_iBullets=3 per shot (cycle 0.441 s), Haze 1 per shot (cycle 0.105 s). Whether the cap means 1 pellet of 3, and what Express Shot does (fires twice, uses extra ammo) is UNRESOLVED",
    'drifter', [MS, EXP], '',
    extra=[('feeds', 'novel hypothesis N04 (next-bullet items on pellet/burst weapons)'),
           ('prediction_haze_control', 'Haze: exactly one extra spirit row on the first bullet of M, nothing further inside 8 s (item cooldown); E: first shot comes out twice with more damage and a larger ammo drop'),
           ('prediction_drifter_CAP', 'Drifter M: one extra spirit row in total (cap of 1 respected) attached to one of the three first-shot pellets'),
           ('prediction_drifter_ALL', 'Drifter M: three extra rows on the first shot (cap counts shots, not pellets)'),
           ('prediction_drifter_ME', 'ME: the bonus rides on the first bullet of the first volley only (Express Shot extra volley carries none) if the cap is per shot'),
           ('decision_rule', 'CAP: a next-bullet bonus is worth one pellet of three; the model divides its value by the pellet count on Drifter, Yamato (5), Calico (9), Shiv (6) style weapons and the builds in changes_builds drop or downgrade the item where the share is under about a third. ALL: item value counts every pellet, no change. Express Shot rows without ammo readback: report volleys and damage only'),
           ('changes_builds', ', '.join(b04)),
           ('unresolved_if', 'Drifter blocks show no pellet rows (gun not firing: statecheck first); per-row timestamps cannot separate shots (report row counts per 0.5 s instead)'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: item text says next bullet, data caps it at 1 bullet per shot, and many heroes fire several bullets per shot'),
           ('alternative_reason', 'Haze (1 bullet per shot) is the control hero in the same file'),
           ('required_levels', '1=1;2=1;3=1;4=1'), ('levels_mode', 'fixed'), ('required_readback', 'items_ok|1|==|1 ; dmg_hits|hits|>|0'),
           ('rotation', 'two heroes in sequence (the setup line switches); blocks X0, M, E, ME then reversed; 1.3 s of fire per block'),
           ('blocked_by', 'ammo count after the shot is not a runner readback (only GunFired/BulletHit counts via acclog); Drifter gun operation not yet exercised in a queue run: run a statecheck block first'),
           ('stack_track', 'none')] + cond_meta('gun only', 'none', 'all abilities', '100 percent body', 'none', 'Mystic Shot, Express Shot', '350u', 'enemies=1 allies=0',
            'equipped_items,distance_m,rows_per_shot,extra_rows_per_shot') + player('Next bullet: one pellet?', 'Pellet gun vs next-bullet item', 'Worth it on shotguns?', 'Pellet item test', 'One pellet or all') + [('result_says', 'WORKS if the bonus lands on every pellet of the first shot; DOES NOT WORK (cap) if exactly one pellet carries it')])
# two heroes: write as two files so each file has one setup line
metaD = [(k, v) for k, v in meta]
write('nv_N04a_next_bullet_haze_control.txt', [(k, ('haze' if k == 'build' else v)) for k, v in meta], ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 1 1 1 1', 'souls 30000'], blocksH)
write('nv_N04b_next_bullet_drifter_pellets.txt', meta, ['setup Drifter Haze', 'raw citadel_unlock_flex_slots', 'abil 1 1 1 1', 'souls 30000'], blocksD)
written += ['nv_N04a_next_bullet_haze_control.txt', 'nv_N04b_next_bullet_drifter_pellets.txt']

# ================================================================ N07 Healing Tempo scope (Haze)
TEMPO, VB, NOVA, LS = cls('Healing Tempo'), cls('Vampiric Burst'), cls('Healing Nova'), cls('Bullet Lifesteal')
b07 = builds_with({'Healing Tempo'})
arms = [('T0_tempo_alone', dict(gives=[TEMPO], ops=['accuracy 1 0', 'fire 1.0', 'mods'])),
        ('P_passive_lifesteal', dict(gives=[TEMPO, LS], ops=['accuracy 1 0', 'fire 1.5', 'mods', 'wait 0.5', 'mods'])),
        ('D_healing_nova', dict(gives=[TEMPO, NOVA], ops=['cast i1 0.6', 'mods', 'wait 1.0', 'mods'])),
        ('V_vampiric_burst', dict(gives=[TEMPO, VB], ops=['cast i1 0.6', 'accuracy 1 0', 'fire 1.5', 'mods', 'wait 0.5', 'mods']))]
blocks = [block(l, lowhp=50, reload=True, **kw) for l, kw in aba(arms)]
meta = common_meta(
    "Checking whether Healing Tempo's speed buff turns on when healing comes from Vampiric Burst's lifesteal, from a direct heal item, from passive bullet lifesteal, or from nothing.",
    "decides where Healing Tempo (a late, expensive item) belongs: %d builds hold it, most of them pair it with lifesteal items whose heals may not count" % len(b07),
    "item text (VERIFIED MECHANIC, citadel_mods_english.txt upgrade_healbuff_desc): applying healing grants fire rate and move speed; does not apply on innate regen or passive Bullet/Spirit Lifesteals. Whether lifesteal granted by an active (Vampiric Burst, Infuser) counts as passive is not in the data (UNRESOLVED). Healing Nova is the positive control (a direct heal), passive Bullet Lifesteal the negative control (excluded by the text)",
    'haze', [TEMPO, VB, NOVA, LS], '',
    extra=[('feeds', 'novel hypothesis N07 (Healing Tempo scope)'),
           ('prediction_D', 'positive control: a new self modifier (the Tempo buff) appears after the Healing Nova cast; its name is then the detector for the other arms. If none appears Healing Tempo does not trigger on self-cast heals at all and the file is read as INCONCLUSIVE for V'),
           ('prediction_P', 'negative control (text): no Tempo modifier after passive lifesteal hits'),
           ('prediction_V_counts', 'Tempo modifier appears while Vampiric Burst lifesteal heals: active-granted lifesteal counts'),
           ('prediction_V_not', 'no Tempo modifier: active-granted lifesteal is treated as passive'),
           ('decision_rule', 'V counts: Healing Tempo stays where Vampiric Burst or Infuser is the main heal. V not: Healing Tempo is only valuable with direct heals (Healing Nova, Rescue Beam, ally heals), builds owner reviews the builds in changes_builds that rely on lifesteal heals. D fails: INCONCLUSIVE, no change'),
           ('changes_builds', ', '.join(b07)),
           ('unresolved_if', 'D shows no modifier (detector unproven); lowhp clamps health every frame, so a heal that is fully clamped may not register: if D fails repeat D at lowhp 30'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: the item text names an exclusion (passive lifesteals) but not the active-granted case, and 21 builds pay for it'),
           ('alternative_reason', 'D and P are the positive and negative controls inside the file'),
           ('required_levels', '1=1;2=1;3=1;4=1'), ('levels_mode', 'fixed'), ('required_readback', 'items_ok|1|==|1'),
           ('rotation', 'lowhp 50 in every block; active item cast first, then 1.5 s of gun fire; mods read after each step'),
           ('stack_track', 'none')] + cond_meta('gun + item actives', 'item active i1', 'abilities 1-4', '100 percent body', 'none', 'Vampiric Burst or Healing Nova', '350u', 'enemies=1 allies=0',
            'equipped_items,self_modifier_names,healDiffObserved') + player('Healing Tempo and lifesteal', 'Which heals trigger Tempo?', 'Worth it with lifesteal?', 'Tempo heal test', 'Buff on a heal, or not') + [('result_says', 'WORKS if the Tempo buff appears during Vampiric Burst; DOES NOT WORK if it appears only after the Healing Nova')])
write('nv_N07_healing_tempo_scope.txt', meta, ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 1 1 1 1', 'souls 30000'], blocks)
written.append('nv_N07_healing_tempo_scope.txt')

# ================================================================ N10 projectile-fired-as-bullet (Nurse Leech Therapy)
CAS = cls('Escalating Resilience')
b10 = [b['id'] for b in B if b['hk'] in ('hero_nurse',)]
arms = [('K_bullets_casings', dict(gives=[CAS], ops=['accuracy 1 0', 'fire 1.0', 'mods'], reload=True)),
        ('L_leech_casings', dict(gives=[CAS], ops=['cast 1 0.8', 'wait 1.0', 'mods', 'wait 2.0', 'mods'])),
        ('L_leech_resist_none', dict(ops=['cast 1 0.8', 'wait 4.0'])),
        ('L_leech_resist_gun50', dict(pre=['eresist gun 50'], ops=['cast 1 0.8', 'wait 4.0'])),
        ('L_leech_resist_spirit50', dict(pre=['eresist spirit 50'], ops=['cast 1 0.8', 'wait 4.0']))]
blocks = [block(l, **kw) for l, kw in aba(arms)]
meta = common_meta(
    "Checking whether Nurse's Leech Therapy jar counts as a bullet hit (bullet-hit items, bullet resist) or as plain ability damage.",
    "decides how the 12 abilities flagged as fired like bullets (Nurse Leech Therapy, Viper daggers, Werewolf, Kelvin, Hornet, Ratking and others) should be itemised: gun-hit items and bullet shreds help only if the projectile counts as a bullet; %d Nurse build(s) test it directly and the rest of the flagged heroes follow the answer by inference" % len(b10),
    "behaviours list PROJECTILE_FIRED_AS_BULLET for these abilities (VERIFIED MECHANIC); Leech Therapy's damage is listed as ability damage (DPS, ABILITY). What the flag means for item procs and for which resist reduces it is engine-side (UNRESOLVED). Escalating Resilience (text: Bullet Resist when your bullets hit a hero) is the detector; K proves the detector works on real bullets",
    'nurse', [CAS], '',
    extra=[('feeds', 'novel hypothesis N10 (PROJECTILE_FIRED_AS_BULLET)'),
           ('prediction_K', 'positive control: bullets produce an Escalating Resilience modifier on the player (mods shows a new self modifier). If not, the detector is unproven: INVALID'),
           ('prediction_bullet', 'L also produces the modifier and the damage rows of the jar fall with eresist gun 50 (not with spirit 50)'),
           ('prediction_ability', 'L produces no modifier and the rows fall with eresist spirit 50 only'),
           ('prediction_mixed', 'modifier appears but rows follow spirit resist (or the reverse): the flag affects procs and resist separately; report both'),
           ('decision_rule', 'bullet: for the flagged heroes gun-hit items and bullet-resist shreds apply to the ability; the builds owner re-classes them in changes_builds. ability: no change. mixed: record both and test each flagged hero before any change. K fails: INCONCLUSIVE'),
           ('changes_builds', ', '.join(b10) + ' (and builds of Viper, Werewolf, Kelvin, Vindicta, Ratking, Graves, Chrono by inference only)'),
           ('unresolved_if', 'Nurse cast 1 does not throw the jar (statecheck/ability_cast readback), or the damage csv has no rows for the leech (DPS ticks may be logged under another ability name)'),
           ('selection_kind', 'discovery'),
           ('selection_reason', 'independent theorycraft: the flag exists on 12 abilities and the data does not say how the engine treats them for procs and resist'),
           ('alternative_reason', 'K is the positive control; the three resist arms separate gun vs spirit scaling'),
           ('required_levels', '1=4;2=1;3=1;4=1'), ('levels_mode', 'fixed'), ('required_readback', 'items_ok|1|==|1 ; dmg_hits|hits|>|0'),
           ('rotation', 'K fire; L jar with item; three resist arms with the jar only; bracketed and reversed'),
           ('blocked_by', 'Nurse jar needs the aim to land on a stationary bot at 350u: verify with ability_cast:1 and a damage row before reading the arms'),
           ('stack_track', 'none')] + cond_meta('ability 1 cast (K: gun)', 'cast 1', 'abilities 2-4', 'n/a', 'none', 'Escalating Resilience', '350u', 'enemies=1 allies=0',
            'equipped_items,ability_cast:1,self_modifier_names,dmg_rows_by_arm') + player('Leech jar: bullet or spell?', 'Nurse jar vs bullet items', 'Which items help Nurse?', 'Jar bullet test', 'Bullet buff or not') + [('result_says', 'WORKS if the jar triggers the bullet-hit item and bullet resist reduces it; DOES NOT WORK if neither happens')])
write('nv_N10_projectile_as_bullet_nurse.txt', meta, ['setup Nurse Haze', 'raw citadel_unlock_flex_slots', 'abil 15 1 1 1', 'souls 30000'], blocks)
written.append('nv_N10_projectile_as_bullet_nurse.txt')

# ================================================================ extra: Echo Shard on an ultimate (confirms the graves_ult data fact; cheap)
ES = cls('Echo Shard')
arms = [('S2_nonult', dict(gives=[ES], imbues=[(ES, 'Signature2')], ops=['cast 2 0.6', 'cds', 'cast i1 0.6', 'cds'])),
        ('S4_ult', dict(gives=[ES], imbues=[(ES, 'Signature4')], ops=['cast 4 0.6', 'cds', 'cast i1 0.6', 'cds']))]
blocks = [block(l, **kw) for l, kw in aba(arms)]
meta = common_meta(
    "Checking what the game does when Echo Shard is imbued on an ultimate, which its own text excludes.",
    "confirms the graves_ult proposal (Echo Shard on Borrowed Decree): data says non-ultimate only; this shows whether the game refuses the imbue or accepts it with no effect",
    "abilities.vdata upgrade_ability_power_shard m_TargetAbilityEffectsToApply = IMBUE_ACTIVE_NON_ULT, text 'imbued non-ultimate ability' (VERIFIED MECHANIC). Runtime behaviour on an ultimate is UNRESOLVED",
    'haze', [ES], '',
    extra=[('feeds', 'proposal council/proposals/graves_ult_echo_fix.json'),
           ('prediction_refused', 'the imbueown log line for Signature4 reports a refusal/false/error while Signature2 succeeds'),
           ('prediction_noeffect', 'both imbues are accepted, but after the Echo Shard press the ultimate cooldown (cds) is unchanged while the Smoke Bomb cooldown is reset'),
           ('prediction_works', 'the ultimate cooldown resets too (the data name would then be wrong): the proposal is withdrawn'),
           ('decision_rule', 'refused or no effect: the graves_ult data-fact proposal stands. Works: withdraw it and correct the audit'),
           ('changes_builds', 'graves_ult'),
           ('unresolved_if', 'cds readback shows garbage values for the ultimate (see AUTORUN DANGER notes)'),
           ('selection_kind', 'discovery'), ('selection_reason', 'independent audit of imbue placements found one build with an item type placed outside its stated target'),
           ('alternative_reason', 'the same item on Smoke Bomb (non-ultimate) is the control'),
           ('required_levels', '1=1;2=4;3=1;4=1'), ('levels_mode', 'fixed'), ('required_readback', 'items_ok|1|==|1'),
           ('rotation', 'cast the imbued ability, press the item, read cooldowns; bracketed and reversed'),
           ('stack_track', 'none')] + cond_meta('ability 2 or 4 cast + item', 'cast 2 or 4', 'others', 'n/a', 'none', 'Echo Shard', 'n/a (self)', 'enemies=1 allies=0', 'equipped_items,imbueown_log,cds') + player('Echo Shard on an ultimate', 'Item says non-ultimate only', 'Does the game stop it?', 'Echo on ultimate', 'Refused or no effect') + [('result_says', 'WORKS if the ultimate cooldown resets after the item press; DOES NOT WORK if the imbue is refused or the cooldown stays')])
write('nv_graves_echo_on_ult.txt', meta, ['setup Haze Haze', 'raw citadel_unlock_flex_slots', 'abil 1 1 1 1', 'souls 30000'], blocks)
written.append('nv_graves_echo_on_ult.txt')

paths = [os.path.join(OUT, f) for f in written]
r = subprocess.run([sys.executable, '-I', os.path.join(C, 'tools', 'lint_meta.py')] + paths, capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[:500])
sys.exit(r.returncode)

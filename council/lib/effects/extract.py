#!/usr/bin/env python3
"""EFFECT EXTRACTOR  (council/lib/effects/extract.py)  -- reusable module, format version 1

Turns the game's own definition files into a typed list of EFFECTS for every hero ability (each upgrade tier) and every item.
Generic: no hero/ability/item name appears in any rule (see taxonomy.py; tests/test_effects.py::test_no_seeded_names).

INPUT   gt6819/game/citadel/pak01_dir/scripts/{abilities,heroes}.vdata + resource/localization/{citadel_heroes,citadel_mods,
        citadel_gc_mod_names}  (SteamDatabase GameTracking dumps; see council/audit/GAMEDATA_6819.md). Override with env EFFECTS_GT=<dir>.
OUTPUT  council/evidence/interactions/effects/heroes.json   {meta, heroes:{<hero_id>:{name, abilities:[ABILITY...]}}}
        council/evidence/interactions/effects/items.json    {meta, items:{<item_class>:ITEM}}
        (written by `python3 -I council/tools/discover_interactions.py extract`; format_version bumps on any schema change)

API (python):   import sys; sys.path.insert(0, 'council/lib/effects'); import extract
    D = extract.load()                    # parsed data (cached per process)
    H = extract.hero_effects(D)           # dict hero_id -> {name, abilities:[ABILITY]}
    I = extract.item_effects(D)           # dict item_class -> ITEM
    extract.write_all(outdir)             # writes heroes.json / items.json
ABILITY = {cls, name, slot (1-4 | 'weapon' | 'melee' | 'innate_N'), is_ult, tiers:3, cooldown_by_tier:[base,t1,t2,t3],
           duration_by_tier, cast_delay, channel_time_by_tier, charges_by_tier, targeting:{location,target_types,self_cast,flags},
           behaviors:[...], interrupted_by:[...], phase_states:{precast,channel,postcast:[non-trivial MODIFIER_STATEs]},
           modifiers:[{field,class,attributes,debuff_type,states,extendible}], props:{name:{by_tier:[...], scale:...}}, desc:{key:text},
           effects:[EFFECT]}
ITEM    = {cls, name, tier (1-5; price 800/1600/3200/6400 for 1-4 is SECONDARY evidence, not in game files), slot, active, disabled,
           imbue:null|'active'|'active_non_ult'|'modifier_value', cooldown_s, props, desc, effects:[EFFECT]}
EFFECT  = {id, producer:{kind,key,name,hero,slot}, op, state, subtype, target:self|ally|self_or_ally|enemy|area|unknown,
           tier_needed:0|1|2|3|'item', magnitude:{prop,by_tier}|null, duration_s:'UNKNOWN'|{...}, cooldown_s, conditions:[...],
           flags:[...], evidence:[{src,file,key,value|text,grade:STRUCTURED|NAME-INFERRED|TEXT}], unknown:[fields not determinable from data]}
Fields that cannot be determined from data are the string 'UNKNOWN' (never guessed).
"""
import os, re, sys, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kv3, taxonomy as T
FORMAT_VERSION = 1
COUNCIL = os.path.abspath(os.path.join(HERE, '..', '..'))
SCRATCH = os.path.abspath(os.path.join(COUNCIL, '..'))

def gt_root():
    r = os.environ.get('EFFECTS_GT') or os.path.join(SCRATCH, 'gt6819', 'game', 'citadel')
    return r

def _loc(path):
    d = {}
    if not os.path.exists(path):
        return d
    rx = re.compile(r'^\s*"([^"]+)"\s+"((?:[^"\\]|\\.)*)"\s*(?://.*)?$')
    for line in open(path, encoding='utf-8', errors='ignore'):
        m = rx.match(line)
        if m:
            k, v = m.groups()
            if k not in d or d[k] == k:      # some files carry an alias line key->key before the real text
                d[k] = v
    return d

_CACHE = {}
def load():
    if 'D' in _CACHE:
        return _CACHE['D']
    root = gt_root()
    sc = os.path.join(root, 'pak01_dir', 'scripts')
    rl = os.path.join(root, 'resource', 'localization')
    ab = kv3.parse_file(os.path.join(sc, 'abilities.vdata'))
    he = kv3.parse_file(os.path.join(sc, 'heroes.vdata'))
    hnames = _loc(os.path.join(rl, 'citadel_heroes', 'citadel_heroes_english.txt'))
    for alt in (os.path.join(SCRATCH, 'gt', 'repo', 'game', 'citadel', 'resource', 'localization', 'citadel_gc_hero_names', 'citadel_gc_hero_names_english.txt'),):
        for k, v in _loc(alt).items():
            hnames.setdefault(k, v)
    D = dict(ab=ab, he=he, loc_heroes=hnames,
             loc_mods=_loc(os.path.join(rl, 'citadel_mods', 'citadel_mods_english.txt')),
             loc_names=_loc(os.path.join(rl, 'citadel_gc_mod_names', 'citadel_gc_mod_names_english.txt')),
             root=root)
    h = hashlib.sha256()
    for f in ('abilities.vdata', 'heroes.vdata'):
        h.update(open(os.path.join(sc, f), 'rb').read())
    D['sha'] = h.hexdigest()[:16]
    _CACHE['D'] = D
    return D

# ------------------------------------------------------------------ numbers
def num(v):
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.match(r'^\s*(-?[0-9]*\.?[0-9]+)', v)
        if m:
            return float(m.group(1))
    return None

def tier_values(block, prop):
    """[base, t1, t2, t3] cumulative values of a property (additive upgrades; EAddToScale upgrades change scaling, not the value)."""
    P = (block.get('m_mapAbilityProperties') or {}).get(prop) or {}
    base = num(P.get('m_strValue'))
    if base is None:
        return None
    vals = [base]
    cur = base
    for up in (block.get('m_vecAbilityUpgrades') or [])[:3]:
        for pu in (up.get('m_vecPropertyUpgrades') or []):
            if pu.get('m_strPropertyName') == prop and pu.get('m_eUpgradeType') in (None, 'EAdd', 'EAddToBase'):
                b = num(pu.get('m_strBonus'))
                if b is not None:
                    cur += b
        vals.append(cur)
    while len(vals) < 4:
        vals.append(cur)
    return vals

def upgrade_touch(block, prop):
    """tiers (1..3) in which `prop` is touched by an upgrade."""
    t = []
    for i, up in enumerate((block.get('m_vecAbilityUpgrades') or [])[:3]):
        if any(pu.get('m_strPropertyName') == prop for pu in (up.get('m_vecPropertyUpgrades') or [])):
            t.append(i + 1)
    return t

def split_bits(s):
    return [x.strip() for x in (s or '').split('|') if x.strip()]

# ------------------------------------------------------------------ structure helpers
def modifiers_of(block):
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            c = o.get('_class')
            if isinstance(c, str) and (c.startswith('modifier') or any(k in o for k in ('m_nEnabledStateMask', 'm_nAttributes', 'm_eDebuffType'))):
                out.append(dict(field=path.split('/')[-1] if path else '', path=path, cls=c,
                                attributes=split_bits(o.get('m_nAttributes')), debuff_type=o.get('m_eDebuffType'),
                                states=split_bits(o.get('m_nEnabledStateMask')), disabled_states=split_bits(o.get('m_nDisabledStateMask')),
                                extendible=bool(o.get('m_bDurationExtendible')), auto_props=o.get('m_vecAutoRegisterModifierValueFromAbilityPropertyName') or []))
            for k, v in o.items():
                if k in ('m_mapAbilityProperties', 'm_vecAbilityUpgrades', 'm_mapWeaponInfos', 'm_mapProjectileInfos') and k != 'm_mapProjectileInfos':
                    continue
                walk(v, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + '[%d]' % i)
    walk(block, '')
    return out

def targeting(block):
    tt = split_bits(block.get('m_nAbilityTargetTypes'))
    bh = split_bits(block.get('m_AbilityBehaviorsBits'))
    loc = block.get('m_eAbilityTargetingLocation') or ''
    friendly = any('FRIENDLY' in x for x in tt)
    enemy = any('ENEMY' in x or 'NEUTRAL' in x for x in tt)
    self_cast = 'CITADEL_ABILITY_BEHAVIOR_ALLOW_SELF_CAST' in bh or loc.endswith('_SELF')
    if loc.endswith('_SELF') or (not tt and 'CITADEL_ABILITY_BEHAVIOR_NO_TARGET' in bh):
        side = 'self'
    elif friendly and not enemy:
        side = 'self_or_ally' if self_cast else 'ally'
    elif enemy and not friendly:
        side = 'enemy'
    elif friendly and enemy:
        side = 'any'
    else:
        side = 'unknown'
    return dict(location=loc.replace('CITADEL_ABILITY_TARGETING_LOCATION_', ''), target_types=tt, self_cast=self_cast, side=side,
                flags=split_bits(block.get('m_nAbilityTargetFlags')), shape=(block.get('m_eAbilityTargetingShape') or '').replace('CITADEL_ABILITY_TARGETING_SHAPE_', ''))

# ------------------------------------------------------------------ effect builder
class Eff:
    n = 0

def mk_effect(prod, op, state, subtype, **kw):
    e = dict(id='', producer=prod, op=op, state=state, subtype=subtype, target=kw.pop('target', 'unknown'),
             tier_needed=kw.pop('tier_needed', 0), magnitude=kw.pop('magnitude', None), duration_s=kw.pop('duration_s', 'UNKNOWN'),
             cooldown_s=kw.pop('cooldown_s', 'UNKNOWN'), conditions=kw.pop('conditions', []), flags=kw.pop('flags', []),
             evidence=kw.pop('evidence', []), unknown=kw.pop('unknown', []))
    e.update(kw)
    return e

def side_for(op, subtype, tg, debuffish):
    if debuffish:
        return 'enemy'
    if op in ('apply_cc', 'amplify') and subtype in ('slow', 'hard_cc', 'vulnerability', 'heal_reduction', 'stun', 'sleep', 'root', 'disarm', 'silence', 'muted', 'chained', 'shooting_disabled', 'healing_disabled', 'melee_disabled', 'dash_disabled', 'movement_silence'):
        return 'enemy' if tg['side'] in ('enemy', 'any', 'unknown') else tg['side']
    if op in ('lockout_target',):
        return tg['side'] if tg['side'] in ('self', 'self_or_ally', 'ally', 'enemy') else 'unknown'
    if op in ('grant', 'absorb', 'prevent') and tg['side'] == 'enemy':
        return 'self'      # a protective grant on an enemy-targeting ability applies to the caster
    if op in ('grant', 'heal', 'absorb', 'reduce', 'prevent', 'defer', 'delayed_cost', 'remove_cc', 'redirect', 'ammo', 'add_charge', 'reset_cd', 'reduce_cd', 'extend_cd', 'recast', 'extend_duration', 'time_scale'):
        return tg['side'] if tg['side'] in ('self', 'self_or_ally', 'ally') else ('self' if tg['side'] == 'unknown' else tg['side'])
    return tg['side']

def hero_of(D, cls):
    for hk, h in D['he'].items():
        if isinstance(h, dict) and 'm_mapBoundAbilities' in h and cls in h['m_mapBoundAbilities'].values():
            return hk
    return None

def desc_keys(loc, cls):
    """localisation entries describing an ability/item: key -> (tier_needed, text)"""
    out = {}
    for k, v in loc.items():
        if not k.startswith(cls):
            continue
        rest = k[len(cls):]
        if rest and re.match(r'^(_desc|_active|_passive|_active_desc|_passive_desc|_desc2|_t[123]_desc|_[a-z_]*desc)$', rest):
            m = re.match(r'^_t([123])_desc$', rest)
            out[k] = (int(m.group(1)) if m else 0, T.clean_text(v))
    return out

PROC_KEYS = {'m_vecProcDamageTypes': 'proc_damage_types', 'm_bCanProcByOtherObjects': 'can_proc_by_other_objects', 'm_flMaxBulletsToProcInShot': 'max_bullets_to_proc_in_shot',
             'm_bCanProcMultipleTimesFromSameShot': 'multi_proc_same_shot', 'm_bCanProcMultipleTimesOnOneTarget': 'multi_proc_one_target',
             'm_bProcOnFriendlyBulletHits': 'proc_on_friendly_bullet_hits', 'm_bProcAppliesBuildup': 'proc_applies_buildup'}
def proc_semantics(b):
    """proc-eligibility fields found anywhere inside an ability/item block (VERIFIED MECHANIC = field present with this value; engine semantics as named)."""
    out = {}
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in PROC_KEYS:
                    if isinstance(v, list):
                        v = sorted(str(x).replace('CITADEL_DAMAGETYPE_', '') for x in v)
                    out[PROC_KEYS[k]] = v
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(b)
    return out

SCALE_TYPE = {'ELightMeleeDamage': 'MELEE', 'EHeavyMeleeDamage': 'MELEE', 'ETechPower': 'ABILITY', 'EBaseWeaponDamageIncrease': 'BULLET', 'EWeaponPower': 'BULLET'}
CSS_TYPE = {'melee_damage': 'MELEE', 'tech_damage': 'ABILITY', 'bullet_damage': 'BULLET', 'weapon_damage': 'BULLET'}
def damage_split(b, P):
    """damage-instance type split per damage property: type from the property's CSS class and the stat it scales with (STRUCTURED). Rend measured: Damage (melee_damage, ELightMeleeDamage) +49% with Crushing Fists, BonusDamage (tech_damage, ETechPower) unchanged."""
    out = []
    for p, pd in (b.get('m_mapAbilityProperties') or {}).items():
        if not isinstance(pd, dict):
            continue
        if p.startswith('Self') or 'SelfDamage' in p:
            continue   # damage dealt to the caster, not an output instance
        css = pd.get('m_strCSSClass'); sf = pd.get('m_subclassScaleFunction') or {}; stat = sf.get('m_eSpecificStatScaleType')
        if not (pd.get('m_bIsAbilityDamageProperty') or (css or '').endswith('_damage')):
            continue
        ty = SCALE_TYPE.get(stat) or CSS_TYPE.get(css) or 'UNCLASSIFIED'
        out.append(dict(prop=p, damage_type=ty, css_class=css, scale_stat=stat, scale_mult=sf.get('m_flStatScale'),
                        by_tier=(P.get(p) or {}).get('by_tier'), grade='STRUCTURED', src='abilities.vdata:m_mapAbilityProperties.%s' % p))
    return out

def ability_record(D, cls, hero=None, slot=None, item=False):
    b = D['ab'][cls]
    prods = dict(kind='item' if item else 'ability', key=cls, hero=hero, slot=slot)
    loc = D['loc_mods'] if item else D['loc_heroes']
    name = (D['loc_names'].get(cls) if item else D['loc_heroes'].get(cls)) or cls
    prods['name'] = name
    tg = targeting(b)
    beh = [x.replace('CITADEL_ABILITY_BEHAVIOR_', '') for x in split_bits(b.get('m_AbilityBehaviorsBits'))]
    ult = b.get('m_eAbilityType') == 'EAbilityType_Ultimate'
    P = {}
    for p in (b.get('m_mapAbilityProperties') or {}):
        tv = tier_values(b, p)
        if tv is None:
            continue
        pd = (b['m_mapAbilityProperties'][p])
        sf = pd.get('m_subclassScaleFunction') or {}
        P[p] = dict(by_tier=tv, scale=(sf.get('m_eSpecificStatScaleType') or sf.get('_class')), scale_mult=sf.get('m_flStatScale'),
                    provides=pd.get('m_eProvidedPropertyType'), hidden=bool(pd.get('m_bIsHidden')), touched_tiers=upgrade_touch(b, p))
    if item:
        # item property upgrades are not ability tiers: keep base; 'enhanced' = m_vecAbilityUpgrades[0], 'corrupted' = m_CorruptedItemInfo (acquisition rule UNKNOWN)
        corr = {pu.get('m_strPropertyName'): num(pu.get('m_strBonus')) for pu in ((b.get('m_CorruptedItemInfo') or {}).get('m_Upgrade') or {}).get('m_vecPropertyUpgrades') or []}
        for p, pd in P.items():
            v = pd['by_tier']
            pd['enhanced'] = v[1] if v[1] != v[0] else None
            pd['corrupted_delta'] = corr.get(p)
            pd['by_tier'] = [v[0]] * 4
    def bt(p):
        return P[p]['by_tier'] if p in P else None
    rec = dict(cls=cls, name=name, hero=hero, slot=slot, is_ult=ult, ability_type=b.get('m_eAbilityType'),
               cooldown_by_tier=bt('AbilityCooldown'), duration_by_tier=bt('AbilityDuration'),
               cast_delay=(bt('AbilityCastDelay') or [None])[0], channel_time_by_tier=bt('AbilityChannelTime'),
               charges_by_tier=bt('AbilityCharges'), cast_range_by_tier=bt('AbilityCastRange'),
               targeting=tg, behaviors=beh,
               interrupted_by=[x for x in split_bits(b.get('m_bitsInterruptingStates'))],
               phase_states={ph: [s for s in split_bits(b.get('m_bits%sEnabledStateMask' % ph)) if s not in T.STATE_TRIVIAL]
                             for ph in ('PreCast', 'Channel', 'PostCast')},
               modifiers=modifiers_of(b), props=P, desc={}, effects=[], imbue=None, damage_split=damage_split(b, P), proc_semantics=proc_semantics(b))
    ta = b.get('m_TargetAbilityEffectsToApply')
    if ta:
        rec['imbue'] = ta.replace('CITADEL_TARGET_ABILITY_BEHAVIOR_IMBUE_', '').lower()
    for k, (tr, tx) in desc_keys(loc, cls).items():
        rec['desc'][k] = dict(tier=tr, text=tx)
    if item:
        rec['tier'] = int(re.sub(r'\D', '', str(b.get('m_iItemTier') or '0')) or 0)
        rec['item_slot'] = (b.get('m_eItemSlotType') or '').replace('EItemSlotType_', '')
        rec['disabled'] = bool(b.get('m_bDisabled'))
        rec['active'] = b.get('m_eAbilityActivation') not in (None, 'CITADEL_ABILITY_ACTIVATION_PASSIVE')
        rec['component_of'] = None
        rec['components'] = [x for x in (b.get('m_vecComponentItems') or [])]
        rec['cooldown_s'] = (bt('AbilityCooldown') or [None])[0]
    rec['text_source'] = 'localization' if rec['desc'] else 'EMPTY-IN-LOCALIZATION (token exists with empty text in citadel_mods/heroes english; value comes from props only)'
    rec['effects'] = effects_for(D, rec, b, prods, item)
    return rec

def _first_tier(vals):
    if not vals:
        return None
    for i, v in enumerate(vals):
        if v not in (0, 0.0, -1, -1.0):
            return i
    return None

def effects_for(D, rec, b, prod, item):
    E = []
    tg = rec['targeting']
    cdv = rec['cooldown_by_tier']
    durv = rec['duration_by_tier']
    def evid(src, key, **kw):
        return dict(src=src, file='abilities.vdata' if src == 'vdata' else 'localization', key=key, **kw)
    def add(op, st, sub, tier, grade, ev, target, mag=None, cond=None, flags=None, unknown=None, duration=None):
        e = mk_effect(dict(prod), op, st, sub, target=target, tier_needed='item' if item else tier,
                      magnitude=mag, duration_s=duration if duration is not None else ({'prop': 'AbilityDuration', 'by_tier': durv} if durv and any(durv) else 'UNKNOWN'),
                      cooldown_s={'by_tier': cdv} if cdv and any(v for v in cdv) else 'UNKNOWN',
                      conditions=list(cond or []), flags=list(flags or []), evidence=[dict(ev, grade=grade)], unknown=list(unknown or []))
        e['id'] = '%s#%d' % (rec['cls'], len(E))
        E.append(e)
        return e
    # 1) properties
    debuff_mods = [m for m in rec['modifiers'] if m['debuff_type'] in ('MODIFIER_DEBUFF_YES',)]
    for p, pd in rec['props'].items():
        vals = pd['by_tier']
        ft = _first_tier(vals)
        if ft is None:
            continue
        for op, st, sub in T.classify_prop(p):
            isdur = p.endswith('Duration') and not sub in ('hard_cc', 'named_immunity', 'displacement')
            if isdur and op not in ('apply_cc',):
                pass
            mag = dict(prop=p, by_tier=vals, scale=pd['scale'])
            side = side_for(op, sub, tg, False)
            unk = []
            if op in ('grant', 'prevent') and st == 'incoming_damage':
                unk += ['damage_types_blocked', 'sources_blocked', 'whether_other_effects_ignore_it']
            if op == 'defer':
                unk += ['application_timing', 'single_hit_or_over_time']
            add(op, st, sub, ft, 'NAME-INFERRED' if not pd['provides'] else 'STRUCTURED',
                evid('vdata', 'm_mapAbilityProperties.' + p, value=vals, provides=pd['provides']), side, mag, unknown=unk)
    # 2) modifier states / attributes
    for m in rec['modifiers']:
        debuff = m['debuff_type'] == 'MODIFIER_DEBUFF_YES'
        for s in m['states']:
            if s in T.STATE_TRIVIAL or s not in T.STATE_LEX:
                continue
            op, st, sub = T.STATE_LEX[s]
            tgt = 'enemy' if (debuff or op in ('apply_cc',)) else (tg['side'] if tg['side'] in ('self', 'self_or_ally', 'ally') else 'self')
            add(op, st, sub, 0, 'NAME-INFERRED', evid('vdata', m['path'] + '.m_nEnabledStateMask', value=s, modifier=m['cls']), tgt,
                flags=['via_modifier:' + m['cls']], unknown=['exact engine semantics of ' + s])
        for a in m['attributes']:
            if a in ('MODIFIER_ATTRIBUTE_IGNORE_INVULNERABLE', 'MODIFIER_ATTRIBUTE_CANNOT_BE_PURGED'):
                add('modifier_flag', 'status' if 'PURGED' in a else 'incoming_damage', 'ignore_invulnerable' if 'INVULN' in a else 'cannot_be_purged', 0, 'STRUCTURED',
                    evid('vdata', m['path'] + '.m_nAttributes', value=a, modifier=m['cls'], meaning=T.ATTR_MEANING[a]), 'enemy' if debuff else 'self_or_ally',
                    flags=['modifier:' + m['cls']], unknown=['which damage sources/effects the flag actually affects'])
        if m['extendible']:
            add('modifier_flag', 'duration', 'duration_extendible', 0, 'STRUCTURED', evid('vdata', m['path'] + '.m_bDurationExtendible', value=True, modifier=m['cls']),
                tg['side'], flags=['modifier:' + m['cls']], unknown=['which effects extend it'])
    # 3) cast-phase states
    for ph, ss in rec['phase_states'].items():
        for s in ss:
            if s in T.STATE_LEX:
                op, st, sub = T.STATE_LEX[s]
                add(op if op != 'lockout_target' else 'lockout_self', st, sub, 0, 'NAME-INFERRED', evid('vdata', 'm_bits%sEnabledStateMask' % ph, value=s), 'self',
                    cond=['during ' + ph.lower()], unknown=['exact engine semantics of ' + s])
    # 4) behaviours
    if 'CHANNELLED' in rec['behaviors']:
        add('modifier_flag', 'actions', 'channelled', 0, 'STRUCTURED', evid('vdata', 'm_AbilityBehaviorsBits', value='CHANNELLED'), 'self',
            cond=['interrupted by ' + ','.join(rec['interrupted_by'] or ['UNKNOWN'])])
    if 'CITADEL_UNIT_TARGET_FLAG_PENETRATE_INVULNERABLE' in tg['flags']:
        add('modifier_flag', 'incoming_damage', 'targets_through_invulnerable', 0, 'STRUCTURED', evid('vdata', 'm_nAbilityTargetFlags', value='PENETRATE_INVULNERABLE'), 'enemy')
    # 5) description text
    for k, d in rec['desc'].items():
        for op, st, sub, phrase in T.classify_text(d['text']):
            add(op, st, sub, d['tier'], 'TEXT', evid('loc', k, text=d['text'][:260], matched=phrase), side_for(op, sub, tg, False),
                unknown=['numbers/timing not in the text'])
    return E

# ------------------------------------------------------------------ public
def hero_effects(D=None):
    D = D or load()
    out = {}
    for hk, h in D['he'].items():
        if not (isinstance(h, dict) and 'm_mapBoundAbilities' in h) or hk == 'hero_base':
            continue
        if h.get('m_bDisabled') or h.get('m_bInDevelopment'):
            continue
        bound = h['m_mapBoundAbilities']
        abs_ = []
        for sl, cls in bound.items():
            m = re.match(r'ESlot_Signature_(\d)', sl)
            if m:
                key = int(m.group(1))
            elif sl == 'ESlot_Weapon_Primary':
                key = 'weapon'
            elif sl == 'ESlot_Weapon_Melee':
                key = 'melee'
            elif re.match(r'ESlot_Ability_Innate_(\d)', sl):
                key = 'innate_' + sl[-1]
            else:
                continue
            if cls not in D['ab']:
                continue
            abs_.append(ability_record(D, cls, hero=hk, slot=key))
        out[hk] = dict(hero=hk, hero_id=h.get('m_HeroID'), name=D['loc_heroes'].get(hk) or hk.replace('hero_', '').title(),
                       abilities=sorted(abs_, key=lambda a: str(a['slot'])))
    return out

def item_effects(D=None):
    D = D or load()
    out = {}
    for cls, b in D['ab'].items():
        if not (isinstance(b, dict) and cls.startswith('upgrade_') and b.get('m_iItemTier')):
            continue
        if cls not in D['loc_names']:
            continue
        out[cls] = ability_record(D, cls, item=True)
    return out

def meta(D):
    return dict(format_version=FORMAT_VERSION, game_build='6819 (gt repo 17462b2, see council/audit/GAMEDATA_6819.md)', source_sha=D['sha'],
                source_root=os.path.relpath(D['root'], SCRATCH), price_note='tier->souls 800/1600/3200/6400 is SECONDARY (wiki), not in game files')

def write_all(outdir):
    D = load()
    os.makedirs(outdir, exist_ok=True)
    H = hero_effects(D)
    I = item_effects(D)
    json.dump(dict(meta=meta(D), heroes=H), open(os.path.join(outdir, 'heroes.json'), 'w'), indent=1, sort_keys=True)
    json.dump(dict(meta=meta(D), items=I), open(os.path.join(outdir, 'items.json'), 'w'), indent=1, sort_keys=True)
    return H, I

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(COUNCIL, 'evidence', 'interactions', 'effects')
    H, I = write_all(out)
    print('heroes', len(H), 'abilities', sum(len(h['abilities']) for h in H.values()), 'items', len(I),
          'effects', sum(len(a['effects']) for h in H.values() for a in h['abilities']) + sum(len(i['effects']) for i in I.values()))

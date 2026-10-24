"""Duo engine game-data layer. Reads the SteamDatabase 'gt' dump directly (heroes.vdata, abilities.vdata, localization).
Everything returned carries its source key so any claim can be traced to a raw vdata field or a localisation string.
Own file; does not depend on or modify lib/effects (other agent)."""
import os, re, sys, json, pickle, html
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
GT = os.path.join(SP, 'gt/repo/game/citadel')
sys.path.insert(0, os.path.join(SP, 'council/lib/effects'))
import kv3  # noqa  (shared tolerant KV3 parser, read-only use)
CACHE = os.path.join(SP, 'council/work/duo/cache.pkl')
LOC = GT + '/resource/localization'

def _src_sig():
    fs = [GT + '/pak01_dir/scripts/abilities.vdata', GT + '/pak01_dir/scripts/heroes.vdata']
    return [(f, os.path.getmtime(f), os.path.getsize(f)) for f in fs]

def _parse_loc(path):
    out = {}
    rx = re.compile(r'^\s*"([^"]+)"\s+"((?:[^"\\]|\\.)*)"', re.M)
    t = open(path, encoding='utf-8-sig', errors='ignore').read()
    for k, v in rx.findall(t):
        out[k] = v.replace('\\"', '"').replace('\\n', '\n')
    return out

class Data:
    def __init__(self):
        sig = _src_sig()
        if os.path.exists(CACHE):
            try:
                d = pickle.load(open(CACHE, 'rb'))
                if d['sig'] == sig:
                    self.__dict__.update(d); return
            except Exception:
                pass
        self.abil = kv3.parse_file(sig[0][0])
        self.heroes = kv3.parse_file(sig[1][0])
        self.loc = {}
        for f in ['citadel_heroes/citadel_heroes_english.txt', 'citadel_mods/citadel_mods_english.txt',
                  'citadel_gc_hero_names/citadel_gc_hero_names_english.txt', 'citadel_main/citadel_main_english.txt',
                  'citadel_gc_mod_names/citadel_gc_mod_names_english.txt']:
            self.loc.update(_parse_loc(os.path.join(LOC, f)))
        self.sig = sig
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        pickle.dump(dict(abil=self.abil, heroes=self.heroes, loc=self.loc, sig=sig), open(CACHE, 'wb'))

_D = None
def D():
    global _D
    if _D is None: _D = Data()
    return _D

# ---------- values ----------
def num(s):
    """'35m' -> 35.0 ; '1.5' -> 1.5 ; 20 -> 20.0 ; other -> None"""
    if isinstance(s, bool): return None
    if isinstance(s, (int, float)): return float(s)
    if isinstance(s, str):
        m = re.match(r'^\s*(-?[0-9]*\.?[0-9]+)\s*(m|s|%)?\s*$', s)
        if m: return float(m.group(1))
    return None

def hero_ids(include_unreleased=False):
    d = D()
    out = []
    for k, v in d.heroes.items():
        if not k.startswith('hero_') or k in ('hero_base',): continue
        if not isinstance(v, dict): continue
        st = v.get('m_eHeroDevelopmentState')
        if v.get('m_bDisabled'): continue
        if st != 'EHeroDevState_Release' and not include_unreleased: continue
        out.append(k)
    return out

def hero_name(hk):
    return D().loc.get(hk + ':n') or hk

def hero_abilities(hk):
    b = D().heroes[hk].get('m_mapBoundAbilities', {})
    sig = [(s, v) for s, v in b.items() if s.startswith('ESlot_Signature_')]
    sig.sort()
    return [v for _, v in sig], b

def loc_clean(t):
    if t is None: return ''
    t = re.sub(r'<br\s*/?>|</br>', ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

# ---------- ability facts ----------
class Ability:
    """Facts of one ability/item class at a given upgrade tier (0 = base, 1..3 = after that tier's upgrade)."""
    def __init__(self, cls, tier=3):
        self.cls = cls
        self.raw = D().abil.get(cls)
        if self.raw is None: raise KeyError(cls)
        self.tier = tier
        self.name = D().loc.get(cls) or cls
        self.props0 = {}     # base
        for p, v in (self.raw.get('m_mapAbilityProperties') or {}).items():
            if isinstance(v, dict):
                self.props0[p] = dict(val=v.get('m_strValue'), ptype=v.get('m_eProvidedPropertyType'),
                                      css=v.get('m_strCSSClass'), scale=v.get('m_subclassScaleFunction'))
        self.upgrades = []  # per tier list of (prop, bonus_str, type, scale_filter)
        for u in (self.raw.get('m_vecAbilityUpgrades') or []):
            self.upgrades.append([(x.get('m_strPropertyName'), x.get('m_strBonus'), x.get('m_eUpgradeType'),
                                   x.get('m_eScaleStatFilter')) for x in (u.get('m_vecPropertyUpgrades') or [])])

    def p(self, name, tier=None, default=None):
        """numeric property value at tier; adds plain upgrades (no EAddToScale)."""
        tier = self.tier if tier is None else tier
        e = self.props0.get(name)
        if e is None: return default
        v = num(e['val'])
        if v is None: return default
        for t in range(min(tier, len(self.upgrades))):
            for (pn, b, ty, flt) in self.upgrades[t]:
                if pn == name and not ty:
                    bv = num(b)
                    if bv is not None: v += bv
        return v

    def tier_of(self, name):
        """earliest tier whose upgrade makes the prop positive (0 if base positive, None if never)"""
        for t in range(0, 4):
            v = self.p(name, t)
            if v is not None and v > 0: return t
        return None

    def has(self, name): return name in self.props0
    @property
    def behaviors(self): return set(re.findall(r'CITADEL_ABILITY_BEHAVIOR_\w+', str(self.raw.get('m_AbilityBehaviorsBits', ''))))
    @property
    def targets(self): return set(re.findall(r'CITADEL_UNIT_TARGET_\w+', str(self.raw.get('m_nAbilityTargetTypes', ''))))
    @property
    def atype(self): return self.raw.get('m_eAbilityType')
    @property
    def interrupting(self): return set(re.findall(r'MODIFIER_STATE_\w+', str(self.raw.get('m_bitsInterruptingStates', ''))))
    def render(self, text, tier=3, bonus_tier=None):
        def sub_s(m):
            nm = m.group(1)
            if bonus_tier and len(self.upgrades) >= bonus_tier:
                tot = 0.0; hit = False
                for (pn, b, ty, flt) in self.upgrades[bonus_tier - 1]:
                    if pn == nm and not ty and num(b) is not None:
                        tot += num(b); hit = True
                if hit: return '%g' % round(tot, 2)
            v = self.p(nm, tier)
            if v is None: v = self.p(nm, 0)
            if v is None: return '<%s>' % nm
            return ('%g' % round(v, 2))
        t = re.sub(r'\{s:([A-Za-z0-9_]+)\}', sub_s, text or '')
        t = re.sub(r"\{g:citadel_inline_attribute:'([A-Za-z_]+)'\}", lambda m: '[' + m.group(1) + ']', t)
        t = re.sub(r'\{[a-z]:[^}]*\}', '?', t)
        return loc_clean(t)
    def desc(self): return self.render(D().loc.get(self.cls + '_desc'))
    def tier_desc(self, t): return self.render(D().loc.get('%s_t%d_desc' % (self.cls, t)), t, bonus_tier=t)
    def fulltext(self):
        return ' | '.join(x for x in [self.desc()] + [self.tier_desc(t) for t in (1, 2, 3)] if x)

    def modifier_states(self):
        """[(path, modifier_class, [states])] for every m_nEnabledStateMask found anywhere in the ability (states a modifier APPLIES)."""
        out = []
        def walk(o, path, cur):
            if isinstance(o, dict):
                c = o.get('_class', cur)
                if 'm_nEnabledStateMask' in o:
                    st = re.findall(r'MODIFIER_STATE_\w+', str(o['m_nEnabledStateMask']))
                    if st: out.append(('/'.join(path), c, st))
                for k, v in o.items():
                    if isinstance(v, (dict, list)): walk(v, path + [k], c)
            elif isinstance(o, list):
                for i, v in enumerate(o): walk(v, path + [str(i)], cur)
        walk(self.raw, [], None)
        return out

    def ptypes(self):
        return {p: e['ptype'] for p, e in self.props0.items() if e['ptype']}

    def stat_summary(self, tier=None):
        t = self.tier if tier is None else tier
        s = {}
        for p in self.props0:
            v = self.p(p, t)
            if v is not None and v != 0 and not p.startswith('Ability') and p not in ('TechPower', 'WeaponPower'):
                s[p] = round(v, 3)
        return s

def hero_kit(hk, tier=3):
    ids, bound = hero_abilities(hk)
    abs_ = []
    for c in ids:
        try: abs_.append(Ability(c, tier))
        except KeyError: pass
    return abs_

def hero_stats(hk):
    """base stats from heroes.vdata m_mapStartingStats (raw)"""
    return D().heroes[hk].get('m_mapStartingStats', {})

if __name__ == '__main__':
    d = D()
    ids = hero_ids()
    print(len(ids), [hero_name(i) for i in ids])

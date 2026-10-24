"""Independent provenance verifier: re-checks effect/hypothesis citations against the RAW files with plain text search
(no kv3 parser, no extractor code), so a parser or extractor bug cannot hide itself."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import extract as X

_RAW = {}
def raw():
    if _RAW: return _RAW
    root = X.gt_root(); sc = os.path.join(root, 'pak01_dir', 'scripts'); rl = os.path.join(root, 'resource', 'localization')
    _RAW['ab'] = open(os.path.join(sc, 'abilities.vdata'), encoding='utf-8', errors='ignore').read()
    _RAW['loc'] = (open(os.path.join(rl, 'citadel_heroes', 'citadel_heroes_english.txt'), encoding='utf-8', errors='ignore').read() + '\n' +
                   open(os.path.join(rl, 'citadel_mods', 'citadel_mods_english.txt'), encoding='utf-8', errors='ignore').read())
    return _RAW

def block(cls):
    ab = raw()['ab']
    m = re.search(r'\n\t%s =\s*\n\t\{' % re.escape(cls), ab)
    if not m: return None
    n = re.search(r'\n\t[A-Za-z0-9_]+ =\s*\n\t\{', ab[m.end():])
    return ab[m.start(): m.end() + (n.start() if n else len(ab))]

def check(cls, src, value=None):
    """returns (ok, why). src like 'abilities.vdata:m_mapAbilityProperties.Prop' | 'abilities.vdata:/m_Mod.m_nAttributes' | 'localization:key'"""
    f, _, key = src.partition(':')
    if f == 'localization':
        m = re.search(r'"%s"\s+"((?:[^"\\]|\\.)*)"' % re.escape(key), raw()['loc'])
        if not m: return False, 'loc key missing'
        if isinstance(value, str) and value.lower().split()[0] not in m.group(1).lower(): return False, 'phrase not in text'
        return True, 'loc'
    b = block(cls)
    if b is None: return False, 'block missing'
    if key.startswith('m_mapAbilityProperties.'):
        p = key.split('.', 1)[1]
        m = re.search(r'\n\t\t\t%s =\s*\n\t\t\t\{(.*?)\n\t\t\t\}' % re.escape(p), b, re.S)
        if not m: return False, 'property missing'
        if isinstance(value, list) and value:
            mv = re.search(r'm_strValue = "?(-?[0-9.]+)', m.group(1))
            if mv and abs(float(mv.group(1)) - value[0]) > 1e-6: return False, 'base value differs %s vs %s' % (mv.group(1), value[0])
        return True, 'prop'
    leaf = key.split('.')[-1]
    if isinstance(value, str) and value.startswith('MODIFIER'):
        return (value in b), 'state/attr string in block'
    if leaf.startswith('m_') and leaf in b: return True, 'field'
    return False, 'field missing'

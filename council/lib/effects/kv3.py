"""Minimal tolerant parser for Valve KV3 text (.vdata) as shipped in the SteamDatabase GameTracking dumps.
Returns nested dict/list/scalars. Subclass objects keep their `_class`; the `subclass:` prefix is dropped.
Typed-string prefixes (resource_name:, soundevent:, panorama:) are kept as str 'prefix:value'.
Duplicate keys are kept (last wins) -- the dumps contain none inside one object that matter here."""
import re
_TOK = re.compile(r'''
   (?P<ws>\s+)
 | (?P<cmt><!--.*?-->|//[^\n]*)
 | (?P<str>"(?:[^"\\]|\\.)*")
 | (?P<punct>[{}\[\]=,:])
 | (?P<word>[^\s{}\[\]=,:"]+)
''', re.X | re.S)

def tokenize(text):
    pos, n = 0, len(text)
    out = []
    m = _TOK.match
    while pos < n:
        mo = m(text, pos)
        if not mo:
            raise ValueError('kv3 tokenizer stuck at %d: %r' % (pos, text[pos:pos+40]))
        pos = mo.end()
        k = mo.lastgroup
        if k in ('ws', 'cmt'):
            continue
        out.append((k, mo.group(k)))
    return out

def _scalar(tok):
    k, v = tok
    if k == 'str':
        return bytes(v[1:-1], 'utf-8').decode('unicode_escape', 'ignore') if '\\' in v else v[1:-1]
    if v in ('true', 'false'):
        return v == 'true'
    if v == 'null':
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v

def parse(text):
    toks = tokenize(text)
    i = 0
    N = len(toks)

    def value():
        nonlocal i
        k, v = toks[i]
        if k == 'punct' and v == '{':
            return obj()
        if k == 'punct' and v == '[':
            return arr()
        # typed prefix  word ':' (str | subclass-marker)
        if k == 'word' and i + 1 < N and toks[i+1] == ('punct', ':'):
            prefix = v
            i += 2
            if prefix == 'subclass':
                return value()
            k2, v2 = toks[i]
            if k2 == 'str':
                i += 1
                return prefix + ':' + v2[1:-1]
            return prefix + ':'
        i += 1
        return _scalar((k, v))

    def obj():
        nonlocal i
        i += 1  # {
        d = {}
        while toks[i] != ('punct', '}'):
            k, v = toks[i]
            key = v[1:-1] if k == 'str' else v
            i += 1
            if toks[i] != ('punct', '='):
                raise ValueError('expected = after %r at token %d' % (key, i))
            i += 1
            d[key] = value()
            if i < N and toks[i] == ('punct', ','):
                i += 1
        i += 1
        return d

    def arr():
        nonlocal i
        i += 1
        a = []
        while toks[i] != ('punct', ']'):
            a.append(value())
            if toks[i] == ('punct', ','):
                i += 1
        i += 1
        return a

    # top: single object
    return value()

def parse_file(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        return parse(f.read())

"""Unit tests: known-answer checks against RAW vdata (plain regex on the files, independent of the parser), generator invariants,
and the self-check that no rule depends on seeded names.  Run: python3 -I council/lib/effects/tests/test_effects.py"""
import os, re, sys, json, unittest
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.path.dirname(HERE); COUNCIL = os.path.abspath(os.path.join(LIB, '..', '..'))
sys.path.insert(0, LIB); sys.path.insert(0, os.path.join(COUNCIL, 'tools'))
import kv3, extract as X, taxonomy as T, provenance as P
import discover_interactions as DI

class TestKV3(unittest.TestCase):
    def test_basic(self):
        d = kv3.parse('{ a = 1 b = "x" c = [ 1, 2 ] d = { e = subclass: { _class = "q" } } f = resource_name:"p/q" }')
        self.assertEqual(d['a'], 1); self.assertEqual(d['c'], [1, 2]); self.assertEqual(d['d']['e']['_class'], 'q'); self.assertEqual(d['f'], 'resource_name:p/q')

class TestKnownAnswers(unittest.TestCase):
    """each expected value is read from the raw file text with a regex here, not from the extractor."""
    @classmethod
    def setUpClass(cls):
        cls.D = X.load(); cls.H = X.hero_effects(cls.D); cls.I = X.item_effects(cls.D)
    def ab(self, hero, cls_):
        return next(a for a in self.H[hero]['abilities'] if a['cls'] == cls_)
    def test_channel_immunity_tier_from_raw(self):
        b = P.block('ability_nurse_fear')
        self.assertRegex(b, r'ChannelDamageImmune =\s*\n\t\t\t\{\s*\n\t\t\t\tm_strValue = "0"')
        self.assertRegex(b, r'm_strPropertyName = "ChannelDamageImmune"\s*\n\s*m_strBonus = "1"')
        # the bonus sits in the THIRD upgrade block in the raw file
        ups = b[b.index('m_vecAbilityUpgrades'):]
        third = re.split(r'\n\t\t\t\{\s*\n\t\t\t\tm_vecPropertyUpgrades', ups)[3]
        self.assertIn('ChannelDamageImmune', third)
        a = self.ab('hero_nurse', 'ability_nurse_fear')
        e = [x for x in a['effects'] if x['evidence'][0].get('key', '').endswith('ChannelDamageImmune')][0]
        self.assertEqual(e['tier_needed'], 3); self.assertEqual(e['magnitude']['by_tier'], [0, 0, 0, 1]); self.assertEqual((e['op'], e['subtype']), ('grant', 'damage_immune'))
    def test_crash_modifier_flags_from_raw(self):
        b = P.block('ability_nurse_adrenaline_rush')
        self.assertRegex(b, r'(?s)m_CrashModifier = subclass:.*?m_nAttributes = "MODIFIER_ATTRIBUTE_IGNORE_INVULNERABLE \| MODIFIER_ATTRIBUTE_CANNOT_BE_PURGED"')
        a = self.ab('hero_nurse', 'ability_nurse_adrenaline_rush')
        subs = {e['subtype'] for e in a['effects'] if e['op'] == 'modifier_flag'}
        self.assertTrue({'ignore_invulnerable', 'cannot_be_purged'} <= subs)
    def test_cooldown_tiers_from_raw(self):
        b = P.block('viscous_restorative_goo')
        self.assertRegex(b, r'AbilityCooldown =\s*\n\t\t\t\{\s*\n\t\t\t\tm_strValue = 42\.0')
        self.assertRegex(b, r'm_strPropertyName = "AbilityCooldown"\s*\n\s*m_strBonus = -20\.0')
        self.assertEqual(self.ab('hero_viscous', 'viscous_restorative_goo')['cooldown_by_tier'], [42.0, 42.0, 42.0, 22.0])
    def test_item_imbue_and_cooldown_from_raw(self):
        b = P.block('upgrade_ability_power_shard')
        self.assertIn('CITADEL_TARGET_ABILITY_BEHAVIOR_IMBUE_ACTIVE_NON_ULT', b); self.assertRegex(b, r'AbilityCooldown =\s*\n\t\t\t\{\s*\n\t\t\t\tm_strValue = 30\.0')
        it = self.I['upgrade_ability_power_shard']
        self.assertEqual(it['imbue'], 'active_non_ult'); self.assertEqual(it['cooldown_s'], 30.0); self.assertEqual(it['tier'], 4)
        self.assertTrue(any(e['op'] == 'reset_cd' for e in it['effects']))
    def test_all_cited_sources_exist_in_raw(self):
        bad = []
        for h in self.H.values():
            for a in h['abilities']:
                for e in a['effects']:
                    ev = e['evidence'][0]
                    if ev['src'] == 'vdata':
                        ok, why = P.check(a['cls'], 'abilities.vdata:' + ev['key'], ev.get('value'))
                        if not ok: bad.append((a['cls'], ev['key'], why))
        self.assertEqual(bad[:5], [], 'unverifiable citations: %d' % len(bad))

class TestGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.D, cls.H, cls.I, cls.hy = DI.generate()
    def test_ult_never_in_non_ult_imbue_template(self):
        for x in self.hy:
            if x['template'].startswith('T2'):
                ab = next(a for a in self.H[x['hero']]['abilities'] if a['name'] == x['title'].split(' imbued on ')[1].split(' (')[0])
                self.assertFalse(ab['is_ult'])
    def test_cost_must_be_borne_by_recipient(self):
        for x in self.hy:
            if x['template'].startswith('T1'):
                B = next(a for a in self.H[x['hero']]['abilities'] if a['cls'] == x['components'][0]['ability'])
                self.assertIn(B['targeting']['side'], ('self', 'self_or_ally', 'ally'))
    def test_every_hypothesis_has_ladder_and_unknowns(self):
        for x in self.hy:
            self.assertEqual(len(x['ladder']['stages']), 5); self.assertTrue(x['unknown_fields']); self.assertIn(x['sandbox']['status'].split('-')[0].split(' ')[0], ('TESTABLE', 'UNTESTABLE', 'PARTIAL', 'MEASURED'))
    def test_untestable_never_claims_measured(self):
        for x in self.hy:
            for s in x['ladder']['stages']:
                self.assertNotIn('MEASURED', s['evidence_tier'].replace('NOT-MEASURED', ''))
    def test_ladder_cap_contiguous(self):
        for x in self.hy:
            st = [s['status'] for s in x['ladder']['stages']]
            cap = 0
            for i, s in enumerate(st):
                if s == 'EVIDENCED': cap = i + 1
                else: break
            self.assertEqual(cap, x['ladder']['cap'])
            self.assertLess(x['ladder']['cap'], 2)   # no sandbox evidence exists, so nothing may claim stage 2+

class TestNoSeeding(unittest.TestCase):
    FORBIDDEN = ['nurse', 'harrow', 'viscous', 'cube', 'echo', 'shard', 'specter', 'lurking', 'wretched', 'venator', 'doorman', 'graves', 'ivy', 'dynamo', 'bebop', 'krill', 'crash', 'rush', 'goo']
    def test_source_has_no_seeded_names(self):
        files = [os.path.join(LIB, f) for f in ('kv3.py', 'taxonomy.py', 'extract.py', 'provenance.py')] + [os.path.join(COUNCIL, 'tools', 'discover_interactions.py'), os.path.join(COUNCIL, 'tools', 'interaction_scenarios.py')]
        hits = []
        for f in files:
            for n, ln in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
                code = ln.split('#')[0] if not ln.strip().startswith(('"""', "'''")) else ln
                for w in self.FORBIDDEN:
                    if re.search(r'\b%s\b' % w, code, re.I) and 'FORBIDDEN' not in code and 'examples' not in ln.lower():
                        hits.append((os.path.basename(f), n, w, ln.strip()[:90]))
        self.assertEqual(hits, [])

class TestDamageSplit(unittest.TestCase):
    """damage-instance type split (added after the Rend measurement). Expected values are read from the RAW block text, not from the extractor."""
    @classmethod
    def setUpClass(cls):
        cls.D = X.load(); cls.H = X.hero_effects(cls.D); cls.I = X.item_effects(cls.D)
    def test_rend_split_known_answer(self):
        b = P.block('drifter_blood_blast')
        self.assertRegex(b, r'(?s)\tDamage =.*?m_strCSSClass = "melee_damage".*?m_eSpecificStatScaleType = "ELightMeleeDamage"')
        self.assertRegex(b, r'(?s)\tBonusDamage =.*?m_strCSSClass = "tech_damage".*?m_eSpecificStatScaleType = "ETechPower"')
        a = next(x for x in self.H['hero_drifter']['abilities'] if x['cls'] == 'drifter_blood_blast')
        ty = {d['prop']: d['damage_type'] for d in a['damage_split']}
        self.assertEqual(ty['Damage'], 'MELEE'); self.assertEqual(ty['BonusDamage'], 'ABILITY'); self.assertNotIn('SelfDamagePct', ty)
    def test_negative_pure_spirit_ability_has_no_melee_part(self):
        a = next(x for x in self.H['hero_haze']['abilities'] if x['cls'] == 'ability_sleep_dagger')
        self.assertNotIn('MELEE', {d['damage_type'] for d in a['damage_split']})
    def test_proc_semantics_known_answer(self):
        b = P.block('upgrade_healbane')
        self.assertRegex(b, r'(?s)m_vecProcDamageTypes =\s*\[\s*"CITADEL_DAMAGETYPE_ABILITY",?\s*\]')
        self.assertEqual(self.I['upgrade_healbane']['proc_semantics']['proc_damage_types'], ['ABILITY'])
        self.assertTrue(self.I['upgrade_critshot']['proc_semantics']['multi_proc_same_shot'])
        self.assertNotIn('can_proc_by_other_objects', self.I['upgrade_healbane']['proc_semantics'])


class TestLearningLoop(unittest.TestCase):
    def mk(self, hero, ab, item, ev='heavy_melee', match=True):
        return dict(id='T5-%s-%s' % (ab, item), template='T5 x', hero=hero, ability_cls=ab, item_cls=item, event=ev, damage_type_match=match,
                    scoring=dict(total=3.0), sandbox=dict(status='TESTABLE-NOW'), ladder=dict(stages=[dict(status='PARTIAL')] * 5, cap=0, cap_text=''), verdict='', components=[])
    def run_rule(self, outcome):
        h = [self.mk('h1', 'a1', 'i1'), self.mk('h2', 'a2', 'i1'), self.mk('h1', 'a1', 'i2'), self.mk('h3', 'a3', 'i9', ev='other'), self.mk('h2', 'a2', 'i1', match=False)]
        h[4]['id'] = 'T5-nomatch'
        m = [dict(id='M', tier='CONTROLLED SANDBOX RESULT', fact='x', links=[dict(template='T5', hero='h1', ability='a1', item='i1', event='heavy_melee', outcome=outcome)])]
        DI.apply_measured(h, m); return {x['id']: x for x in h}
    def test_confirmed_promotes_siblings_only(self):
        r = self.run_rule('confirmed')
        self.assertEqual(r['T5-a1-i1']['scoring']['total'], 0.0); self.assertTrue(r['T5-a1-i1']['measured'])
        self.assertEqual(r['T5-a2-i1']['scoring']['total'], 3.6)       # same item, other ability, type match
        self.assertEqual(r['T5-a1-i2']['scoring']['total'], 3.3)       # same ability, other item
        self.assertEqual(r['T5-a3-i9']['scoring']['total'], 3.0)       # unrelated event: untouched (negative)
        self.assertEqual(r['T5-nomatch']['scoring']['total'], 3.0)     # sibling whose ability lacks the item's damage type: not promoted (negative)
    def test_rejected_demotes_siblings(self):
        r = self.run_rule('rejected')
        self.assertEqual(r['T5-a2-i1']['scoring']['total'], 1.5); self.assertEqual(r['T5-a1-i2']['scoring']['total'], 2.0)
        self.assertEqual(r['T5-a1-i1']['ladder']['stages'][1]['status'], 'REFUTED')


if __name__ == '__main__':
    unittest.main(verbosity=2)

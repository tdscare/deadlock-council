// node test.js  : unit tests on synthetic input in an OS temp dir
const fs = require('fs'), os = require('os'), path = require('path'), assert = require('assert');
const { generate } = require('./gen_cfg.js'), { run } = require('./parse_log.js');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sbxtest-'));
const sc = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'scenarios', 'wraith_leech_vs_vampiric.json'), 'utf8'));
const g = generate(sc, { team: 3, loadout: true, wait: 0 });
const names = Object.keys(g.files);
assert(names.includes('sbx_common.cfg') && names.some((n) => /_setup\.cfg$/.test(n)) && names.includes('sbx_' + sc.id + '.cfg'));
const setupA = g.files[names.find((n) => /_setup\.cfg$/.test(n))];
assert(/giveitem upgrade_damage_recycler/.test(setupA), 'Leech code in arm A');
const setupB = g.files[names.filter((n) => /_setup\.cfg$/.test(n))[1]];
assert(!/upgrade_damage_recycler/.test(setupB), 'arm B has no Leech');
assert(/alias t_\w+_1 "t_reset; bind F8 e_/.test(g.files['sbx_' + sc.id + '.cfg']));
for (const c of Object.values(g.files)) for (const l of c.split('\n')) if (l && !l.startsWith('//') && !l.startsWith('alias')) assert(/\/\/ (CONFIRMED|UNVERIFIED)/.test(l), 'untagged: ' + l);
// parser: timestamps present
const log = `
[10:00:00.000] SBXMARK START t_sc A 1
[10:00:01.500] player dealt 100 damage
[10:00:02.000] healed 30
[10:00:05.000] player dealt 50 damage
[10:00:06.000] enemy hero_haze died
[10:00:09.000] SBXMARK END t_sc A 1
[10:01:00.000] SBXMARK START t_sc B 1
[10:01:01.000] player dealt 10 damage
[10:01:02.000] you died
[10:01:03.000] SBXMARK END t_sc B 1
`;
const f = path.join(tmp, 'a.log'); fs.writeFileSync(f, log);
const scn = { id: 't_sc', metrics: [{ name: 'damage_dealt' }, { name: 'hp_healed_30s' }, { name: 'time_to_first_kill' }, { name: 'survival_time' }, { name: 'enemies_killed' }, { name: 'weird_thing' }] };
fs.writeFileSync(path.join(tmp, 's.json'), JSON.stringify(scn));
const r = run([f, f], { scenario: path.join(tmp, 's.json'), date: '2026-10-22', out: path.join(tmp, 'res') });
assert.strictEqual(r.length, 2, 'duplicates merged');
const A = r.find((x) => x.arm === 'A'), B = r.find((x) => x.arm === 'B');
assert.strictEqual(A.metrics.damage_dealt, 150); assert.strictEqual(A.metrics.hp_healed_30s, 30);
assert.strictEqual(A.metrics.time_to_first_kill, 6); assert.strictEqual(A.metrics.enemies_killed, 1);
assert.strictEqual(A.metrics.survival_time, 9); assert(A.anomalies.some((x) => /lower bound/.test(x)));
assert.strictEqual(A.metrics.weird_thing, null); assert.strictEqual(A.grade.weird_thing, null);
assert.strictEqual(B.metrics.survival_time, 2); assert.strictEqual(B.metrics.damage_dealt, 10);
assert(fs.existsSync(path.join(tmp, 'res', '2026-10-22_t_sc_A_t1.json')));
// fallback: log with only markers, no signal, no timestamps
fs.writeFileSync(path.join(tmp, 'b.log'), 'SBXMARK START t_sc A 1\nnoise\nSBXMARK END t_sc A 1\n');
const r2 = run([path.join(tmp, 'b.log')], { scenario: path.join(tmp, 's.json'), date: 'd' });
assert.strictEqual(r2[0].metrics.damage_dealt, null); assert(r2[0].missing.length >= 5); assert(r2[0].anomalies.some((x) => /timestamps/.test(x)));
// manual override
fs.writeFileSync(path.join(tmp, 'm.json'), JSON.stringify({ 't_sc A 1': { damage_dealt: { value: 777, grade: 'B', evidence: 'shot.png' } } }));
const r3 = run([path.join(tmp, 'b.log')], { scenario: path.join(tmp, 's.json'), date: 'd', manual: path.join(tmp, 'm.json') });
assert.strictEqual(r3[0].metrics.damage_dealt, 777); assert.strictEqual(r3[0].grade.damage_dealt, 'B');
fs.rmSync(tmp, { recursive: true });
console.log('all tests passed');

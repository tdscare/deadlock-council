#!/usr/bin/env node
// Console log / condump -> results/<date>_<scenario>_<arm>_t<n>.json (SCHEMA.md).
// usage: node parse_log.js <log files...> [--scenario scenario.json] [--patterns patterns.json] [--out DIR] [--patch X] [--date YYYY-MM-DD] [--manual manual.json]
// A trial is the text between "SBXMARK START <sc> <arm> <n>" and the matching END (or next START / EOF = anomaly).
// FALLBACK: a metric whose line type never appears in the log is value:null, grade:null and listed in `missing`;
// supply it by hand via --manual {"<scenario> <arm> <n>":{"metric":{"value":12.3,"grade":"B","evidence":"shot_031.png"}}}.
// Same-text copies of a log (condump + con_logfile) are fine: duplicate trial blocks are merged by keeping the one with most matched events.
const fs = require('fs'), path = require('path');
const HERE = __dirname;

const rx = (s) => new RegExp(s.replace(/\(\?<(\w+)>/g, '(?<$1>'), 'i');
function loadPatterns(f) {
  const j = JSON.parse(fs.readFileSync(f || path.join(HERE, 'patterns.json'), 'utf8'));
  const P = { ts: j.timestamp.map(rx), mark: rx(j.mark) };
  for (const k of ['damage_dealt', 'damage_taken', 'healing', 'enemy_death', 'player_death']) P[k] = j[k].map(rx);
  return P;
}
function stamp(line, P) {
  for (const r of P.ts) {
    const m = line.match(r); if (!m) continue;
    const g = m.groups;
    if (g.t !== undefined) return +g.t;
    return +g.h * 3600 + +g.m * 60 + +g.s + (g.ms ? +('0.' + g.ms) : 0);
  }
  return null;
}
function first(line, rs) { for (const r of rs) { const m = line.match(r); if (m) return m; } return null; }

function parseText(text, P) {
  const lines = text.split(/\r?\n/);
  const trials = []; let cur = null; const prints = {};
  const close = (endLine, ended) => { if (cur) { cur.ended = ended; cur.endT = endLine; trials.push(cur); cur = null; } };
  for (const line of lines) {
    const t = stamp(line, P);
    const mk = line.match(P.mark);
    if (mk) {
      const g = mk.groups;
      if (g.kind.toUpperCase() === 'START') { close(null, false); cur = { scenario: g.scenario, arm: g.arm, trial: +g.trial, t0: t, events: [], lines: 0, ended: false }; }
      else if (cur && cur.scenario === g.scenario && cur.arm === g.arm && cur.trial === +g.trial) { cur.t1 = t; close(t, true); }
      continue;
    }
    if (!cur) continue;
    cur.lines++;
    const add = (type, m, extra) => { prints[type] = true; cur.events.push({ type, t: t != null && cur.t0 != null ? t - cur.t0 : null, v: m && m.groups && m.groups.v !== undefined ? +m.groups.v : 1, ...extra }); };
    let m;
    if ((m = first(line, P.damage_dealt))) add('damage_dealt', m);
    else if ((m = first(line, P.damage_taken))) add('damage_taken', m);
    else if ((m = first(line, P.healing))) add('healing', m);
    else if ((m = first(line, P.enemy_death))) add('enemy_death', m, { victim: m.groups.victim });
    else if ((m = first(line, P.player_death))) add('player_death', m);
  }
  close(null, false);
  return { trials, prints };
}

// scenario metric name -> canonical extractor
const MAP = [
  [/time_to_first_kill|ttfk/, 'ttfk'],
  [/time_to_kill|^ttk$/, 'ttk'],
  [/survival|survived_time|channel_survived/, 'survival'],
  [/enem(y|ies)_killed|kills?$|kill_count/, 'kills'],
  [/hp_heal|heal|lifesteal|leech/, 'healing'],
  [/hp_lost|damage_taken|hp_lost_total/, 'damage_taken'],
  [/damage|dmg|dealt|hp_removed/, 'damage_dealt'],
];
function canon(name) { const n = name.toLowerCase(); for (const [r, c] of MAP) if (r.test(n)) return c; return null; }
function windowOf(name) { const m = name.match(/_(\d+)s$/); return m ? +m[1] : null; }

function compute(tr, prints, metricNames) {
  const ev = tr.events;
  const hasT = tr.t0 != null;
  const dur = tr.t0 != null && tr.t1 != null ? tr.t1 - tr.t0 : null;
  const sum = (type, w) => ev.filter((e) => e.type === type && (w == null || (e.t != null && e.t <= w))).reduce((a, e) => a + e.v, 0);
  const deaths = ev.filter((e) => e.type === 'enemy_death');
  const pd = ev.find((e) => e.type === 'player_death');
  const out = { metrics: {}, grade: {}, missing: [], anomalies: [] };
  const set = (n, v, why) => { if (v == null) { out.metrics[n] = null; out.grade[n] = null; out.missing.push(n + ': ' + why); } else { out.metrics[n] = Math.round(v * 1000) / 1000; out.grade[n] = 'A'; } };
  for (const n of metricNames) {
    const c = canon(n), w = windowOf(n);
    if (!c) { set(n, null, 'no console signal defined for this metric (read from screen, pass via --manual)'); continue; }
    if (c === 'damage_dealt' || c === 'damage_taken' || c === 'healing') {
      const type = c;
      if (!prints[type]) { set(n, null, `log has no "${type}" lines (command/format not found; see HARNESS.md probe)`); continue; }
      if (w != null && !hasT) { set(n, null, 'window metric needs timestamps; log has none'); continue; }
      set(n, sum(type, w));
    } else if (c === 'kills') {
      if (!prints.enemy_death) set(n, null, 'log has no enemy death lines'); else set(n, deaths.length);
    } else if (c === 'ttfk' || c === 'ttk') {
      if (!prints.enemy_death) set(n, null, 'log has no enemy death lines');
      else if (!hasT) set(n, null, 'no timestamps in log');
      else { const d = c === 'ttk' ? deaths[deaths.length - 1] : deaths[0]; set(n, d && d.t != null ? d.t : null, 'no kill occurred in this trial'); }
    } else if (c === 'survival') {
      if (pd && pd.t != null) set(n, pd.t);
      else if (hasT && dur != null) { set(n, dur); out.anomalies.push('survival_time = END marker time (player death not seen): treat as cap/lower bound unless you pressed END at death'); }
      else set(n, null, 'no timestamps / no player death line');
    }
  }
  if (!tr.ended) out.anomalies.push('no matching END marker (trial cut off or END not pressed)');
  if (tr.lines === 0) out.anomalies.push('no log lines between START and END: logging not active or wrong file');
  if (!hasT) out.anomalies.push('log lines carry no timestamps: all time metrics are null');
  return out;
}

function run(files, o) {
  const P = loadPatterns(o.patterns);
  const sc = o.scenario ? JSON.parse(fs.readFileSync(o.scenario, 'utf8')) : null;
  const manual = o.manual ? JSON.parse(fs.readFileSync(o.manual, 'utf8')) : {};
  const best = {}; let prints = {};
  for (const f of files) {
    const r = parseText(fs.readFileSync(f, 'utf8'), P);
    Object.assign(prints, r.prints);
    for (const t of r.trials) { const k = `${t.scenario} ${t.arm} ${t.trial}`; if (!best[k] || t.events.length + (t.ended ? 1 : 0) > best[k].events.length + (best[k].ended ? 1 : 0)) best[k] = t; }
  }
  const results = [];
  for (const [k, t] of Object.entries(best)) {
    const names = sc && sc.id === t.scenario ? sc.metrics.map((m) => m.name) : ['damage_dealt', 'damage_taken', 'hp_healed', 'enemies_killed', 'time_to_first_kill', 'survival_time'];
    const c = compute(t, prints, names);
    const man = manual[k] || {};
    for (const [mn, mv] of Object.entries(man)) {
      c.metrics[mn] = mv.value; c.grade[mn] = mv.grade || 'B';
      c.missing = c.missing.filter((x) => !x.startsWith(mn + ':'));
    }
    results.push({ scenario: t.scenario, arm: t.arm, trial: t.trial, date: o.date, patch: o.patch || null,
      metrics: c.metrics, grade: c.grade, evidence: Object.values(man).map((m) => m.evidence).filter(Boolean),
      notes: c.missing.length ? 'missing from log: ' + c.missing.join(' | ') : 'all metrics from log',
      anomalies: c.anomalies, missing: c.missing });
  }
  results.sort((a, b) => a.scenario.localeCompare(b.scenario) || a.trial - b.trial || a.arm.localeCompare(b.arm));
  if (o.out) {
    fs.mkdirSync(o.out, { recursive: true });
    for (const r of results) fs.writeFileSync(path.join(o.out, `${r.date}_${r.scenario}_${r.arm}_t${r.trial}.json`), JSON.stringify(r, null, 1));
  }
  return results;
}
module.exports = { parseText, run, loadPatterns, canon };

if (require.main === module) {
  const a = process.argv.slice(2), files = [], o = { date: new Date().toISOString().slice(0, 10) };
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--scenario') o.scenario = a[++i]; else if (a[i] === '--patterns') o.patterns = a[++i];
    else if (a[i] === '--out') o.out = a[++i]; else if (a[i] === '--patch') o.patch = a[++i];
    else if (a[i] === '--date') o.date = a[++i]; else if (a[i] === '--manual') o.manual = a[++i]; else files.push(a[i]);
  }
  if (!files.length) { console.error('usage: node parse_log.js <log...> [--scenario f] [--out dir] [--patch p] [--date d] [--manual f]'); process.exit(1); }
  const r = run(files, o);
  for (const x of r) console.log(`${x.scenario} ${x.arm} t${x.trial}: ` + JSON.stringify(x.metrics) + (x.missing.length ? '  MISSING ' + x.missing.length : '') + (x.anomalies.length ? '  ANOM ' + x.anomalies.length : ''));
  if (!r.length) console.log('no SBXMARK START blocks found: markers not logged (see HARNESS.md PROBE 5)');
}

#!/usr/bin/env node
// Scenario JSON -> exec-able Deadlock cfg files.
// usage: node gen_cfg.js <scenario.json> [--out DIR] [--enemy-team N] [--spawn "x y z"] [--enemy-pos "x y z"] [--enemy-hero Haze] [--use-wait SECONDS] [--no-loadout]
// Every emitted command carries a trailing "// CONFIRMED" or "// UNVERIFIED" tag taken from commands.json.
// Files written to DIR (copy them flat into <Deadlock>\game\citadel\cfg):
//   sbx_common.cfg                 cheats, logging, readouts, aliases that are scenario independent
//   sbx_<sc>_<arm>_setup.cfg       reset + level/souls + giveitem lines for that arm
//   sbx_<sc>_enemies.cfg           spawn enemies + behaviour
//   sbx_<sc>.cfg                   master: defines aliases  arm_<arm>  spawn_enemies  reset  t_<arm>_<n>  t_end  t_next
const fs = require('fs'), path = require('path'), cp = require('child_process');
const HERE = __dirname, SBX = path.join(HERE, '..');
const REG = JSON.parse(fs.readFileSync(path.join(HERE, 'commands.json'), 'utf8')).cmds;
const HEROES = JSON.parse(fs.readFileSync(path.join(HERE, 'hero_names.json'), 'utf8'));
const ITEMS = JSON.parse(fs.readFileSync(path.join(SBX, 'item_commands.json'), 'utf8'));

function tag(cmd) {
  const name = cmd.split(/\s+/)[0];
  const r = REG[name];
  if (!r) return 'UNVERIFIED';
  return r.s === 'CONFIRMED' && /unverified|PROBE|unknown|CONTRADICTION/i.test(r.note || '') ? 'CONFIRMED(name only; args/effect UNVERIFIED)' : r.s;
}
const L = (cmd) => cmd + ' // ' + tag(cmd);          // tagged cfg line
const slug = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');

function parseArgs(argv) {
  const o = { out: null, team: 3, spawn: null, enemyPos: null, wait: 0, loadout: true, file: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') o.out = argv[++i];
    else if (a === '--enemy-team') o.team = +argv[++i];
    else if (a === '--spawn') o.spawn = argv[++i];
    else if (a === '--enemy-pos') o.enemyPos = argv[++i];
    else if (a === '--use-wait') o.wait = +argv[++i];
    else if (a === '--enemy-hero') o.enemyHero = argv[++i];
    else if (a === '--no-loadout') o.loadout = false;
    else if (!o.file) o.file = a;
  }
  return o;
}

function soulsOf(...texts) {
  for (const t of texts) {
    if (t == null) continue;
    const m = String(t).match(/(\d+(?:\.\d+)?)\s*k\b/i) || String(t).match(/\b(\d{4,7})\b/);
    if (m) return m[1].match(/^\d{4,}$/) && !/k/i.test(m[0]) ? +m[1] : Math.round(parseFloat(m[1]) * 1000);
  }
  return null;
}

function heroId(display) {
  const h = HEROES[display];
  return { id: h ? h.id : 'hero_' + slug(display), known: !!h, confirm: !!(h && h.confirm) };
}
function enemyList(sc, opt) {
  const out = [], warn = [];
  for (const e of (sc.setup && sc.setup.enemies) || []) {
    const names = Object.keys(HEROES).filter((n) => new RegExp('\\b' + n + '\\b', 'i').test(e.hero || ''));
    const count = e.count || 1;
    if (/camp|neutral/i.test(e.hero || '')) { out.push({ camp: true, beh: '' }); continue; }
    if (!names.length && opt && opt.enemyHero && HEROES[opt.enemyHero]) { for (let i = 0; i < count; i++) out.push({ ...heroId(opt.enemyHero), name: opt.enemyHero, beh: e.behaviour || '' }); continue; }
    if (!names.length) { warn.push(`enemy "${e.hero}" x${count} not a known hero: using placeholder, pass --enemy-hero <Name> or edit the cfg (names via dump_hero_names)`); for (let i = 0; i < count; i++) out.push({ id: 'hero_haze', placeholder: e.hero, beh: e.behaviour || '' }); continue; }
    for (let i = 0; i < count; i++) out.push({ ...heroId(names[i % names.length]), name: names[i % names.length], beh: e.behaviour || '' });
  }
  return { out, warn };
}
function behaviourCmds(beh) {
  const b = (beh || '').toLowerCase();
  const c = [];
  if (/stand|stationary|idle|dummy/.test(b)) {
    c.push('citadel_bot_brain_disable_movement true', 'citadel_bot_brain_disable_attacks true');
  } else if (/attack|fire back|focus|chase|brawl/.test(b)) {
    c.push('citadel_bot_brain_disable_movement false', 'citadel_bot_brain_disable_attacks false');
  } else if (/walk|loop|record/.test(b)) {
    c.push('citadel_bot_brain_disable_attacks true');
    c.push('// MANUAL: movement "' + beh + '" needs a recorded puppet loop (bot_puppet / citadel_bot_record / citadel_bot_playrecording, args unverified). Record once, reuse for every trial.');
  }
  return c;
}

function loadoutLines(arm, sc) {
  const lines = [], warn = [];
  const items = arm.items;
  const imb = arm.imbues || {};
  const give = (name, idx) => {
    const code = ITEMS[name];
    if (!code) { warn.push('no item code for ' + name); lines.push('// MISSING item code: ' + name); return; }
    const i = imb[name] !== undefined ? ' ' + imb[name] : (idx !== undefined ? ' ' + idx : '');
    lines.push(L('giveitem ' + code + i));
  };
  if (Array.isArray(items)) {
    for (const it of items) give(it.replace(/\s*\(.*\)$/, '') in ITEMS ? it.replace(/\s*\(.*\)$/, '') : it);
  } else if (typeof items === 'string' && items.startsWith('build:')) {
    const m = items.match(/^build:(\S+)(?:\s+core(?:\s+(\d+))?)?/);
    try {
      const args = [path.join(SBX, '..', 'tools', 'loadout.js'), m[1]];
      if (m[2]) args.push('--max', m[2]);
      const r = cp.spawnSync('node', args, { encoding: 'utf8' });
      for (const ln of r.stdout.split('\n')) {
        if (!ln || /^(resetme|givelevelupgold)\b/.test(ln)) continue;
        lines.push(ln.startsWith('giveitem') ? L(ln) : ln);
      }
      if (r.status) warn.push(`loadout.js ${m[1]} exit ${r.status}: ${r.stderr.trim() || 'missing item codes'}`);
    } catch (e) { warn.push('loadout.js failed: ' + e.message); }
  } else if (items) warn.push('items not understood: ' + JSON.stringify(items));
  return { lines, warn };
}

function generate(sc, opt) {
  const files = {}, warn = [];
  const id = slug(sc.id);
  const souls = (arm) => soulsOf(arm.souls, sc.setup && sc.setup.level_or_boons);

  files['sbx_common.cfg'] = [
    '// sbx_common.cfg  generated; run once per session AFTER loading the sandbox map: exec sbx_common',
    L('sv_cheats true'),
    L('citadel_hero_testing_enabled true'),
    L('citadel_allow_purchasing_anywhere true'),
    L('citadel_unlock_flex_slots'),
    L('citadel_enable_fast_cooldowns') + '   // 1-2s cooldowns accepted by Kieran',
    L('hud_damagemeter true'),
    L('developer 1'),
    '// ---- logging: try in this order; probe.cfg tells you which works',
    L('con_logfile sbx_console.log'),
    L('debug_takedamage_summaries true') + '   // may print per-hit damage; unknown',
    L('echo SBXMARK COMMON_LOADED'),
    '// ---- scenario independent aliases',
    'alias sbx_dump "condump"   // ' + tag('condump') + '  writes condumpNN file with the console buffer',
    L('bind F9 sbx_dump'),
  ].join('\n') + '\n';

  const arms = sc.arms || [];
  const armSlugs = arms.map((a) => slug(a.name));
  arms.forEach((arm, ai) => {
    const lo = opt.loadout ? loadoutLines(arm, sc) : { lines: ['// loadout skipped'], warn: [] };
    lo.warn.forEach((w) => warn.push(`arm ${arm.name}: ${w}`));
    const s = souls(arm);
    const f = [
      `// ${id} arm ${arm.name}: ${arm.notes || ''}`,
      `// level/boons: ${sc.setup && sc.setup.level_or_boons}   souls field: ${arm.souls}`,
      L('resetme') + '   // semantics unknown: PROBE 4 checks it clears items',
      L('healthpct 100'),
      s ? L('citadel_give_gold ' + s) + `   // adds ${s} souls to ALL players; level from souls unverified` : '// no souls number parsed; set manually',
      ...(opt.spawn ? [L('setpos ' + opt.spawn)] : []),
      ...lo.lines,
      L(`echo SBXMARK ARM_READY ${id} ${armSlugs[ai]}`),
    ];
    if (arm.ability_order) f.push('// MANUAL: ability order ' + arm.ability_order + ' (no documented command to set ability points; click, or citadel_hero_testing_infinite_money true gives points)');
    files[`sbx_${id}_${armSlugs[ai]}_setup.cfg`] = f.join('\n') + '\n';
  });

  const en = enemyList(sc, opt); en.warn.forEach((w) => warn.push(w));
  const ef = [`// ${id} enemies`, L('bot_kick_all')];
  const behs = new Set();
  en.out.forEach((e) => {
    if (e.camp) { ef.push(L('citadel_spawn_nearby_neutrals') + '   // stand next to a camp first'); return; }
    ef.push(L(`citadel_create_unit ${e.id} ${opt.team}`) + (e.confirm ? '' : `   // hero id ${e.known ? 'from memory, check dump_hero_names' : 'GUESSED'}${e.placeholder ? ' PLACEHOLDER for "' + e.placeholder + '"' : ''}; team ${opt.team} UNVERIFIED`));
    behs.add(e.beh);
  });
  [...behs].forEach((b) => behaviourCmds(b).forEach((c) => ef.push(c.startsWith('//') ? c : L(c) + '   // applies to bots? PROBE 6')));
  if (opt.enemyPos) ef.push(L('setpos ' + opt.enemyPos) + '   // moves YOU; enemies spawn in front of crosshair. Aim before running');
  if (!en.out.length) ef.push('// scenario has no enemies');
  ef.push(L(`echo SBXMARK ENEMIES_READY ${id}`));
  files[`sbx_${id}_enemies.cfg`] = ef.join('\n') + '\n';

  const m = [`// sbx_${id}.cfg master. In game: exec sbx_common ; exec sbx_${id}`,
    `// Order per trial:  arm_<arm> (when arm changes) -> t_<arm>_<n> (resets, spawns enemies, binds F8, prints START) -> fight -> F9? no: press F8 at trial end (prints END + condump)`];
  armSlugs.forEach((a) => m.push(`alias arm_${a} "exec sbx_${id}_${a}_setup"`));
  m.push(`alias spawn_enemies "exec sbx_${id}_enemies"`);
  m.push(`alias t_reset "bot_kick_all; healthpct 100; citadel_enable_fast_cooldowns; exec sbx_${id}_enemies"   // ${tag('healthpct')}`);
  const n = sc.trials || 5;
  armSlugs.forEach((a) => {
    for (let t = 1; t <= n; t++) {
      const endPart = opt.wait ? `; wait ${opt.wait * 64}; echo SBXMARK END ${id} ${a} ${t}; condump` : '';
      m.push(`alias t_${a}_${t} "t_reset; bind F8 e_${a}_${t}; echo SBXMARK START ${id} ${a} ${t}${endPart}"`);
    }
  });
  // t_end must carry real scenario/arm/trial: provide per-trial end aliases and a 'next' sequence
  armSlugs.forEach((a) => { for (let t = 1; t <= n; t++) m.push(`alias e_${a}_${t} "echo SBXMARK END ${id} ${a} ${t}; condump"`); });
  m.push('// Interleaved A,B,A,B order. t_<arm>_<n> rebinds F8 to the matching e_<arm>_<n>.');
  const seq = []; for (let t = 1; t <= n; t++) armSlugs.forEach((a) => seq.push(`${a}_${t}`));
  m.push('// Trial order: ' + seq.join(', '));
  if (opt.wait) m.push(L('wait') + '   // --use-wait used: trial end is automatic, 64 ticks/s assumed UNVERIFIED');
  m.push(L(`echo SBXMARK SCENARIO_LOADED ${id}`));
  files[`sbx_${id}.cfg`] = m.join('\n') + '\n';

  return { files, warn, sequence: seq };
}

module.exports = { generate, soulsOf, enemyList, parseArgs };

if (require.main === module) {
  const o = parseArgs(process.argv.slice(2));
  if (!o.file) { console.error('usage: node gen_cfg.js <scenario.json> [--out DIR]'); process.exit(1); }
  const sc = JSON.parse(fs.readFileSync(o.file, 'utf8'));
  const r = generate(sc, o);
  const out = o.out || path.join(HERE, 'out', sc.id);
  fs.mkdirSync(out, { recursive: true });
  for (const [f, c] of Object.entries(r.files)) fs.writeFileSync(path.join(out, f), c);
  console.log('wrote ' + Object.keys(r.files).length + ' files to ' + out);
  console.log('trial order: ' + r.sequence.join(' '));
  r.warn.forEach((w) => console.log('WARN: ' + w));
}

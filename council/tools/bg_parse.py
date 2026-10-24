#!/usr/bin/env python3
"""Parse plugin.log into per-task, per-block metrics for the background-focus comparison.
usage: bg_parse.py plugin.log [taskIdPrefix ...]   (default: all tasks whose id starts with 'bg:')
Block = a `mark <label>` step; ACC/EVENTS lines (acclog) are attributed to the label active when they were printed.
UCSTAT lines (FocusStat.cs) are attributed by their own label=.
"""
import re, sys, json, statistics as st

log = sys.argv[1]
pref = sys.argv[2:] or ['bg:']
tasks = {}      # key id#attempt -> dict
cur = None
label = 'none'
last = 'none'
for ln in open(log, errors='replace'):
    m = re.search(r'QR TASK-START (\S+)#(\d+)', ln)
    if m:
        cur = m.group(1) + '#' + m.group(2)
        tasks[cur] = dict(id=m.group(1), att=int(m.group(2)), blocks=[], uc={}, perf=None, fg=[], end=None, t0=ln[:23])
        label = 'none'
        continue
    if cur is None:
        continue
    T = tasks[cur]
    m = re.search(r'SC step \d+: mark (.*)$', ln)
    if m:
        label = m.group(1).strip()
        if label != 'none': last = label
    m = re.search(r'SC ACC p=(\S+) head=(\S+): windows=(\d+) missWindows=(\d+) headWindows=(\d+) dmgHitsOnEnemy=(\d+)', ln)
    if m:
        T['_acc'] = dict(label=last, p=m.group(1), windows=int(m.group(3)), miss=int(m.group(4)), head=int(m.group(5)), hits=int(m.group(6)))
    m = re.search(r'SC EVENTS (.*)$', ln)
    if m and '_acc' in T:
        ev = m.group(1)
        g = re.search(r'GunFired:me=(\d+)', ev); b = re.search(r'BulletHit:me=(\d+)', ev); c = re.search(r'BulletCreated:me=(\d+)', ev)
        a = T.pop('_acc'); a['fired'] = int(g.group(1)) if g else 0; a['bhit'] = int(b.group(1)) if b else 0; a['created'] = int(c.group(1)) if c else 0
        if not (T['blocks'] and T['blocks'][-1]['label'] == a['label'] and T['blocks'][-1]['hits'] == a['hits'] and T['blocks'][-1]['fired'] == a['fired']):
            T['blocks'].append(a)
    m = re.search(r'UCSTAT label=(\S*) secs=([\d.]+) calls=(\d+) cmds=(\d+) calls/s=([\d.]+) cmds/call=([\d.]+) perCall\S+ gapMs mean=([\d.]+) p50=(\S+) p95=(\S+) p99=(\S+) max=(\S+) gap>32ms=(\d+) gap>50ms=(\d+)(?: allSlotCalls=(\d+) allSlotCalls/frame=([\d.]+) slots=(\S*))? \| frames=(\d+) emptyFrames\(no human cmd\)=(\d+) frameGapMs p50=(\S+) p99=(\S+) max=(\S+) \| fgSamples=(\d+) fgPct=(-?\d+) minimizedPct=(-?\d+)', ln)
    if m:
        g = m.groups()
        T['uc'].setdefault(g[0], []).append(dict(secs=float(g[1]), calls=int(g[2]), cps=float(g[4]), cpc=float(g[5]), gmean=float(g[6]), p50=g[7], p95=g[8], p99=g[9], gmax=g[10], late32=int(g[11]), late50=int(g[12]),
                                                 allpf=float(g[14]) if g[14] else None, slots=g[15], frames=int(g[16]), empty=int(g[17]), fgpct=int(g[22]), minpct=int(g[23])))
    m = re.search(r'PERF tick n=(\d+).*usercmd n=(\d+)', ln)
    if m:
        T['perf'] = (int(m.group(1)), int(m.group(2)))
    if 'FG client' in ln:
        T['fg'].append(ln[11:23] + ' ' + ln.strip().split('FG client ')[1])
    if re.search(r'QR TASK-(END|ABORT|RESULT)', ln):
        T['end'] = ln.strip()[24:]
        if 'TASK-RESULT' in ln:
            cur = None

out = {k: v for k, v in tasks.items() if any(v['id'].startswith(p) for p in pref)}
for k, T in out.items():
    print('=== %s start %s  end: %s  perf(ticks,usercmd)=%s ratio=%s fg=%s' % (k, T['t0'], T['end'], T['perf'], ('%.2f' % (T['perf'][1] / T['perf'][0])) if T['perf'] else '-', T['fg']))
    for b in T['blocks']:
        u = T['uc'].get(b['label'], [None])[-1]
        us = ('calls/s=%.1f cmds/call=%.2f gap p50/p95/p99/max=%s/%s/%s/%s late>32=%d empty=%d%% allSlot/frame=%s fg%%=%d' % (u['cps'], u['cpc'], u['p50'], u['p95'], u['p99'], u['gmax'], u['late32'], 100 * u['empty'] / max(1, u['frames']), u['allpf'], u['fgpct'])) if u else ''
        print('  %-34s p=%s win=%3d miss=%3d head=%3d fired=%3d bhit=%3d hits=%3d  %s' % (b['label'], b['p'], b['windows'], b['miss'], b['head'], b['fired'], b['bhit'], b['hits'], us))
json.dump(out, open(sys.argv[1] + '.bg.json', 'w'), indent=1)

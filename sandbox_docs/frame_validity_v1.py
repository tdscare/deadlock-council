#!/usr/bin/env python3
"""Offline frame-spike validity check. Usage: frame_validity.py <sbx_logs dir> [timing-sensitive task-id substring ...]
Maps server_stdout.log IN_PROGRESS_LONG_FRAME lines (uptime seconds) to wall clock using the deadworks
timestamped lines as anchors, then reports per task window (plugin.log TASK-START..TASK-END/ABORT):
max frame, count >100 ms, >250 ms. Timing-sensitive tasks overlapping a >100 ms spike are flagged NOT CLEAN (>250 = INVALID)."""
import re,sys,bisect,datetime as dt
d=sys.argv[1]; sens=sys.argv[2:] or ['act_ar','ar2','reload','cap_test']
base=dt.datetime(2026,10,24)
ts=[];lf=[]
for n,l in enumerate(open(d+'/server_stdout.log',errors='replace'),1):
    m=re.match(r'\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)\]',l)
    if m: ts.append((n,dt.datetime.strptime(m.group(1),'%Y-%m-%d %H:%M:%S.%f')))
    m=re.match(r'([\d.]+) IN_PROGRESS_LONG_FRAME TOOK ([\d.]+)ms',l)
    if m: lf.append((n,float(m.group(1)),float(m.group(2))))
tl=[t[0] for t in ts];lo,hi=-1e18,1e18
b0=ts[0][1].replace(hour=0,minute=0,second=0,microsecond=0)
for n,u,_ in lf:
    i=bisect.bisect(tl,n)
    if i>0: lo=max(lo,(ts[i-1][1]-b0).total_seconds()-u)
    if i<len(ts): hi=min(hi,(ts[i][1]-b0).total_seconds()-u)
off=(lo+hi)/2
print(f'clock offset bounds [{lo:.3f},{hi:.3f}] (width {hi-lo:.3f}s)'); assert hi>=lo-0.05,'offset inconsistent (server restarted mid-log?)'
sp=[(b0+dt.timedelta(seconds=u+off),ms) for _,u,ms in lf]
cov0=ts[0][1]
tasks={};last={}
pat=re.compile(r'^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+) QR (TASK-START|TASK-END|TASK-ABORT) (\S+?)#(\d+)')
for l in open(d+'/plugin.log',errors='replace'):
    m=pat.match(l)
    if not m: continue
    t=dt.datetime.strptime(m.group(1),'%Y-%m-%d %H:%M:%S.%f');k=(m.group(3),m.group(4))
    if m.group(2)=='TASK-START': tasks[(k,t)]=[t,None,m.group(2)]; last[k]=(k,t)
    elif k in last: tasks[last[k]][1]=t;tasks[last[k]][2]=m.group(2)
print(f'stdout coverage starts {cov0}; tasks before that are NOT covered')
for ((tid,a),_t),(t0,t1,how) in tasks.items():
    if t1 is None or t0<cov0: continue
    ov=[(w,ms) for w,ms in sp if t0<=w<=t1]
    mx=max([ms for _,ms in ov],default=0);n100=sum(1 for _,ms in ov if ms>=100);n250=sum(1 for _,ms in ov if ms>=250)
    ts_=any(s in tid for s in sens)
    verdict='clean' if n100==0 else ('INVALID(timing-sensitive, >250ms)' if ts_ and n250 else ('NOT CLEAN(timing-sensitive, >100ms)' if ts_ else 'flag(non-timing)'))
    print(f'{tid}#{a} {t0:%H:%M:%S}-{t1:%H:%M:%S} {how} maxFrameMs={mx:.0f} >100ms={n100} >250ms={n250} sens={ts_} -> {verdict}')
    for w,ms in ov:
        if ms>=100: print(f'    spike {w:%H:%M:%S} {ms:.0f}ms')
print('ALL >=250ms spikes:'); [print(f'  {w:%H:%M:%S.%f}'[:-3],f'{ms:.0f}ms') for w,ms in sp if ms>=250]

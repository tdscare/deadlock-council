"""Offline model of the QueueRunner session gate / abort-refund / PAUSE / maintenance state machine.
Mirrors QueueRunner11.cs (QMonitor, QAbort, QOrphanReset, QIdle, QFinalize accept gate), Scenario8.cs (step dispatch gate), Maint.cs.
It is a MODEL (python), not the C# itself: it proves the design; the C# still needs a real compile + live check."""
import copy, sys
class W:
    def __init__(s, gate=True):
        s.now=0; s.client=True; s.pawn=True; s.pid=100; s.ent=7
        s.tasks=[dict(id='A',state='pending',attempts=0,pauses=0,log=[]),dict(id='B',state='pending',attempts=0,pauses=0,log=[])]
        s.pause=False; s.pausemsg=''; s.status=''; s.cmds=[]; s.qr=None; s.running=False; s.gate=gate
        s.maint=False; s.events=[]; s.ready_since=0; s.si=0; s.nsteps=10; s.noctl=0; s.nopawn=0; s.stepend=0
    def key(s): return f'{s.pid}:{s.ent}' if s.client else ''
    def problem(s, hero=False):
        if not s.client: return 'no client'
        if not s.pawn: return 'no pawn'
        return None
    def tick(s, dt=1000):
        s.now+=dt
        # scenario step dispatch (Scenario8): only when running
        if s.running and s.now>=s.stepend:
            if s.gate and s.problem() is not None: s.stepend=s.now+250
            else:
                s.cmds.append((s.now,s.qr['id'],s.si)); s.si+=1; s.stepend=s.now+1000
                if s.si>=s.nsteps: s.running=False; s.endwhy='end of script'; s.qr['ended']=True; s.qr['finat']=s.now
        # QrStep
        if s.pause:
            if s.qr: s.abort('paused by user',True,'pending',op=True)
            return
        if s.qr: return s.monitor()
        s.idle()
    def monitor(s):
        r=s.qr
        if r['ended']:
            if s.now-r['finat']>=2000: s.finalize(r)
            return
        h=s.client; 
        if not h: r['noctl']=r['noctl'] or s.now
        else: r['noctl']=0
        if h and not s.pawn: r['nopawn']=r['nopawn'] or s.now
        else: r['nopawn']=0
        sp=None
        if r['noctl'] and s.now-r['noctl']>3000: sp='client disconnected'
        elif r['nopawn'] and s.now-r['nopawn']>20000: sp='no pawn 20s'
        elif r['key'] and h and s.key()!=r['key']: sp='session changed'
        if sp: s.abort('session lost: '+sp,True,'pending',op=True); s.sessionpause(sp)
    def sessionpause(s,sp): s.status='Sandbox disconnected - testing paused'; s.pause=True; s.pausemsg='AUTO-PAUSE '+sp
    def abort(s,why,refund,state,op=False):
        r=s.qr
        if not r: return
        if s.running and not r['ended']: s.running=False
        s.qr=None; t=r['t']; t['pauses']+=1
        if refund and (op or t['pauses']<=5): t['attempts']=max(0,t['attempts']-1)
        t['state']=state; t['log'].append(('aborted',why))
    def finalize(s,r):
        t=r['t']
        spf = 'session changed before accepted' if (r['key'] and s.key()!=r['key']) else s.problem()
        if spf: s.abort('session lost before accept: '+spf,True,'pending',op=True); s.sessionpause(spf); return
        s.qr=None; t['state']='done'; t['log'].append(('done',''))
    def idle(s):
        pick=next((t for t in s.tasks if t['state'] in('pending','paused')),None)
        if not pick: return
        if not s.client or not s.pawn: s.ready_since=0; pick['state']='paused'; return
        if s.ready_since==0: s.ready_since=s.now
        if s.now-s.ready_since<5000: return
        pick['state']='running'; pick['attempts']+=1
        s.qr=dict(id=pick['id'],t=pick,ended=False,noctl=0,nopawn=0,key=s.key(),finat=0); s.running=True; s.si=0; s.stepend=s.now
    # orphan reset on plugin load (server restart): running -> pending refunded, PAUSE written
    def reload(s):
        n=0
        for t in s.tasks:
            if t['state']=='running': t['state']='pending'; t['attempts']=max(0,t['attempts']-1); t['log'].append(('orphan-refund','')); n+=1
        s.qr=None; s.running=False; s.status=''
        if n: s.pause=True; s.status='Sandbox disconnected - testing paused'
        s.pid+=1
    def resume(s): s.pause=False; s.status=''
    # maintenance (Maint.cs)
    def idle_runner(s): return s.qr is None and not s.running
    def build_refusal(s):
        if not s.idle_runner(): return 'task in flight'
        if not s.maint: return 'no maintenance window'
        return None
    def maint_begin(s):
        s.pause=True; 
        if s.qr: s.abort('MAINTENANCE',True,'pending',op=True)
        s.maint=True; s.events.append('MAINT BEGIN')
def run(gate=True):
    res=[]
    # T1 trip: disconnect mid task
    w=W(gate)
    for _ in range(15): w.tick()
    assert w.running and len(w.cmds)>0, 'task should be running'
    n0=len(w.cmds); w.client=False
    for _ in range(40): w.tick()
    nl=len(w.cmds)
    res.append(('T1 no commands dispatched after disconnect', nl==n0))
    tA=w.tasks[0]
    res.append(('T1 task interrupted: pending + attempts refunded to 0', tA['state']=='pending' and tA['attempts']==0))
    res.append(('T1 PAUSE + single status', w.pause and w.status=='Sandbox disconnected - testing paused'))
    res.append(('T1 not counted as failure', all(k!='fail' for k,_ in tA['log'])))
    # T2 reconnect but still paused: must NOT start
    w.client=True; w.pawn=True
    for _ in range(30): w.tick()
    res.append(('T2 no auto-resume after reconnect (PAUSE holds)', w.qr is None and not w.running and tA['state']=='pending'))
    # T3 explicit resume with valid session: runs again, queue advances to B after A done
    w.resume()
    for _ in range(80): w.tick()
    res.append(('T3 resumed: A done, B started/done', tA['state']=='done' and w.tasks[1]['state'] in('running','done')))
    # T4 loss exactly at end (finalize gate)
    w=W(gate)
    for _ in range(30):
        w.tick()
        if w.qr and w.qr['ended']: break
    w.client=False
    for _ in range(5): w.tick()
    res.append(('T4 result not accepted when session lost before accept', w.tasks[0]['state']=='pending' and w.pause and w.tasks[0]['attempts']==0))
    # T5 server restart orphan
    w=W(gate)
    for _ in range(12): w.tick()
    w.reload()
    res.append(('T5 orphan: refunded, pending, PAUSE, no start', w.tasks[0]['state']=='pending' and w.tasks[0]['attempts']==0 and w.pause))
    for _ in range(30): w.tick()
    res.append(('T5 stays idle until resume', w.qr is None))
    # T6 pawn lost (hideout-like) for >20s
    w=W(gate)
    for _ in range(12): w.tick()
    w.pawn=False; c=len(w.cmds)
    for _ in range(40): w.tick()
    res.append(('T6 pawn lost: no new commands, paused', len(w.cmds)==c and w.pause and w.tasks[0]['attempts']==0))
    # T7 no infinite retries: repeated trips capped by pause count but still never failing the task
    w=W(gate)
    for k in range(8):
        w.resume(); w.client=True; w.pawn=True
        for _ in range(12): w.tick()
        w.client=False
        for _ in range(8): w.tick()
    res.append(('T7 8 trips: no auto-restart loops, task never marked fail', w.tasks[0]['state']!='fail' and w.pause))
    # T8 maintenance
    w=W(gate)
    for _ in range(12): w.tick()
    res.append(('T8 build refused while task runs', w.build_refusal() is not None))
    w.maint_begin()
    res.append(('T8 build allowed only after begin + idle', w.build_refusal() is None and w.tasks[0]['attempts']==0 and w.pause))
    return res
if __name__=='__main__':
    bad=0
    for gate in (True,False):
        print('--- gate', 'ON' if gate else 'OFF (mutation: must show failures)')
        for n,ok in run(gate):
            print(('PASS ' if ok else 'FAIL ')+n)
            if gate and not ok: bad+=1
    sys.exit(1 if bad else 0)

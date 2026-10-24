// OFFLINE MODEL of QueueRunner.cs decision logic (no dotnet in this container, so this is a line-by-line JS port of the
// pure rules, NOT the compiled code). Purpose: exercise the state machine on crafted histories. Run: node qr_model_test.js
const assert=require('assert');let pass=0;const T=(n,f)=>{try{f();pass++;console.log('PASS',n)}catch(e){console.log('FAIL',n,e.message);process.exitCode=1}};
const NOW=()=>Date.now();
// ---- ports ----
function forgn(lock,me,now){ if(!lock)return null; if(lock.owner===me.owner||lock.released)return null; if(lock.pid===me.pid)return null;
  const age=(now-Date.parse(lock.hb))/1000; if(age>15)return null; return {age}; }
function orphanReset(q,cause){let n=0;for(const t of q.tasks){if(t.state!=='running')continue;let att=t.attempts||0,p=t.pauses||0;const refund=p<5;
  if(refund){t.attempts=Math.max(0,att-1);t.pauses=p+1;att=t.attempts}t.state=att>=3?'blocked':'pending';if(att>=3)t.blockedReason='interrupted at attempt 3';n++}return n}
function failTask(t,reasons,backoffSec=30){const att=t.attempts;t.lastReasons=reasons;if(att>=3){t.state='blocked';t.blockedReason=reasons.join('; ')}else{t.state='pending';t.notBefore=Date.now()+backoffSec*(1<<Math.max(0,att-1))*1000}}
function abort(t,{refund,operator}){t.pauses=(t.pauses||0)+1;if(refund&&(operator||t.pauses<=5))t.attempts=Math.max(0,t.attempts-1)}
const STATES=['pending','running','paused','paused-needs-foreground','done','blocked'];
function reconcile(q){const sum=STATES.reduce((a,k)=>a+q.tasks.filter(t=>t.state===k).length,0);const ids=q.tasks.map(t=>t.id);return {ok:sum===q.tasks.length&&new Set(ids).size===ids.length,sum,total:q.tasks.length}}
const FGOPS=new Set('key keys keypress keydown keyup sendkeys sendinput type typetext click dblclick rightclick mouse mousemove mousedown mouseup scroll drag focus foreground activate alttab screenshot screen launch startgame openapp shell cmd powershell os osinput input reconnect connect disconnect restartclient restartgame clientrestart relaunch'.split(' '));
const FGRAW=new Set('connect reconnect disconnect retry quit exit kick kickid killserver restart startgame'.split(' '));
function fgScan(text){let ln=0;for(const raw of text.split('\n')){ln++;let l=raw;const h=l.indexOf('#');if(h>=0)l=l.slice(0,h);l=l.trim();if(!l)continue;const w=l.split(/ +/);const op=w[0].toLowerCase();
  if(FGOPS.has(op))return `line ${ln}: ${op}`;if(op==='raw'&&w[1]&&(FGRAW.has(w[1].toLowerCase())||/steam:\/\//i.test(l)))return `line ${ln}: raw ${w[1]}`}return null}
const mk=(id,state,att=0)=>({id,state,attempts:att});
// ---- tests ----
const me={owner:'sbx-plugin:100:aaa',pid:100};
T('lock: fresh foreign (other pid) is foreign',()=>assert(forgn({owner:'x',pid:5,hb:new Date(NOW()-3000).toISOString()},me,NOW())));
T('lock: stale >15s is taken over',()=>assert(!forgn({owner:'x',pid:5,hb:new Date(NOW()-16000).toISOString()},me,NOW())));
T('lock: released is free',()=>assert(!forgn({owner:'x',pid:5,hb:new Date().toISOString(),released:true},me,NOW())));
T('lock: own previous instance in same process (reload) is not foreign',()=>assert(!forgn({owner:'y',pid:100,hb:new Date().toISOString()},me,NOW())));
T('lock: far-future hb (demo fake controller) stays foreign',()=>assert(forgn({owner:'x',pid:99999,hb:'2099-01-01T00:00:00Z'},me,NOW())));
T('kill+restart inside 15s window: OLD code stranded the running task, NEW adopts it on lock-free',()=>{
  const q={tasks:[mk('a','running',1)]};const lock={owner:'dead',pid:5,hb:new Date(NOW()-8000).toISOString()};
  const f=forgn(lock,me,NOW());assert(f); // new process starts while dead owner's hb still fresh -> yields
  const oldFixed=f?0:orphanReset(q);assert.strictEqual(oldFixed,0); // old: nothing, and never revisited
  // 10 s later lock is stale -> takeover re-reads + resets
  assert(!forgn(lock,me,NOW()+10000));assert.strictEqual(orphanReset(q),1);assert.strictEqual(q.tasks[0].state,'pending');assert.strictEqual(q.tasks[0].attempts,0)});
T('interrupted run refunds attempt, state pending',()=>{const q={tasks:[mk('a','running',2)]};orphanReset(q);assert.deepStrictEqual([q.tasks[0].state,q.tasks[0].attempts],['pending',1])});
T('crash loop: after 5 interruptions the attempt counts and 3 attempts -> blocked',()=>{const t=mk('a','running',3);t.pauses=5;const q={tasks:[t]};orphanReset(q);assert.strictEqual(t.state,'blocked')});
T('failing scenario: attempts 1,2 retry with backoff 30s,60s; attempt 3 -> blocked',()=>{const t=mk('b','running',1);failTask(t,['x']);assert.strictEqual(t.state,'pending');assert(Math.abs(t.notBefore-Date.now()-30000)<500);
  t.attempts=2;failTask(t,['x']);assert(Math.abs(t.notBefore-Date.now()-60000)<500);t.attempts=3;failTask(t,['unknown op']);assert.strictEqual(t.state,'blocked');assert.strictEqual(t.blockedReason,'unknown op')});
T('user pause of attempt 1 task refunds attempt, even after 10 pauses',()=>{const t=mk('c','running',1);t.pauses=9;abort(t,{refund:true,operator:true});assert.strictEqual(t.attempts,0)});
T('automatic abort (client lost) is capped after 5 pauses',()=>{const t=mk('c','running',1);t.pauses=5;abort(t,{refund:true,operator:false});assert.strictEqual(t.attempts,1)});
T('reconcile: 9 tasks = 5 done + 1 paused + 3 pending',()=>{const q={tasks:[...Array(5)].map((_,i)=>mk('d'+i,'done',1)).concat([mk('p','paused',1)],[...Array(3)].map((_,i)=>mk('n'+i,'pending')))};const r=reconcile(q);assert(r.ok&&r.sum===9)});
T('reconcile detects unknown state and duplicate id',()=>{assert(!reconcile({tasks:[mk('a','weird')]}).ok);assert(!reconcile({tasks:[mk('a','done'),mk('a','done')]}).ok)});
T('fg scan: existing sandbox scenarios are NOT flagged',()=>{const fs=require('fs'),d=__dirname+'/../autorun/scenarios';let n=0;for(const f of fs.readdirSync(d)){const r=fgScan(fs.readFileSync(d+'/'+f,'utf8'));assert.strictEqual(r,null,f+': '+r);n++}console.log('   scanned',n,'scenario files')});
T('fg scan: crafted OS-input steps are flagged',()=>{for(const s of ['click 100 100','key w 2','focus deadlock','screenshot','raw connect localhost:27067','raw reconnect','raw  steam://run/1422450','Alttab','sendkeys ^c','launch deadlock','# click\nwait 1\nmouse 5 5'])assert(fgScan(s),s)});
T('fg scan: comments and normal ops are not flagged',()=>assert.strictEqual(fgScan('# click here\nwait 1 # key\nfire 3\ncast 1 1\nraw citadel_unlock_flex_slots\nbtn Attack 1'),null));
// ---- added 14:35: exhausted => blocked and the runner moves on; interruptions never read as failures ----
function pick(q,nowMs){let p=null;for(const t of q.tasks){if(t.state!=='pending')continue;if((t.notBefore||0)>nowMs)continue;if(!p||(t.prio||0)>(p.prio||0))p=t}return p}
T('3rd failed attempt => blocked with reason, and pick() moves to the next pending task',()=>{const a=mk('bad','running',3),b=mk('next','pending');const q={tasks:[a,b]};failTask(a,['2x unknown op']);assert.strictEqual(a.state,'blocked');assert.strictEqual(a.blockedReason,'2x unknown op');assert.strictEqual(pick(q,Date.now()).id,'next');b.state='done';assert.strictEqual(pick(q,Date.now()),null)});
T('failed attempt 1 backs off: pick() skips it and starts the next task meanwhile',()=>{const a=mk('flaky','running',1),b=mk('other','pending');const q={tasks:[a,b]};failTask(a,['x']);assert.strictEqual(pick(q,Date.now()).id,'other')});
T('6th interruption of one task counts as an attempt (no endless reload loop) and 3 counted => blocked',()=>{const t=mk('r','running',3);t.pauses=5;const q={tasks:[t,mk('n','pending')]};orphanReset(q);assert.strictEqual(t.state,'blocked');assert.strictEqual(pick(q,Date.now()).id,'n')});
function runKind(log){let ls=-1;log.forEach((x,i)=>{if(x==='start')ls=i});for(let i=ls-1;i>=0;i--){const k=log[i];if(k==='interrupted'||k==='aborted')return 'rerun';if(k==='invalid'||k==='retry')return 'retry';if(k==='done')break}return 'new'}
T('label: interruption is Re-run, never Retry; failure is Retry; first is New',()=>{assert.strictEqual(runKind(['start']),'new');assert.strictEqual(runKind(['start','interrupted','start']),'rerun');assert.strictEqual(runKind(['start','aborted','start']),'rerun');assert.strictEqual(runKind(['start','invalid','retry','start']),'retry');assert.strictEqual(runKind(['start','invalid','retry','start','interrupted','start']),'rerun')});
console.log(pass,'passed');

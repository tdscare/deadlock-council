// Persistent Sandbox work queue. State: council/sandbox/queue.json (atomic writes, safe to resume after crash/restart).
// node queue.js init|status|next|start <id>|done <id> <resultfile>|fail <id> "<why>"|invalid <id> "<why>"|add <build> <experiment>|reopen <buildIds> <why>|reset-stale
// Result header convention: a `SCOPE: isolated|build-context` line (first 1500 chars) is REQUIRED for `done` (isolated = item/ability tested alone, a datum for mechanism only; build-context = the complete build at the checkpoint with relevant actives cast).
// Task states: pending -> running -> done | blocked.  A task is `done` ONLY with a result file whose header says VALID and the instrument checks (setup/A-A) passed. invalid/failed results never count as done.
// PC queue (runs inside the game-server plugin, authoritative for PC tasks): `sync` stages E:\deadworks-server\sbx_queue\* into council/sandbox/queue_pc/ (stage the files first with the device tool, see SYNC below); `report` prints the builds x scenarios matrix; `done <id> pc:<pcTaskId>|<result.json>` accepts a PC result only with VALID: yes.
// Retry: max 3 attempts, then `blocked` with the reasons (never loops on a broken scenario). running > 45 min with no heartbeat -> reset-stale returns it to pending (attempt counted).
const fs=require('fs'),path=require('path');const SP=path.resolve(__dirname,'../..');process.chdir(SP);
const QF=process.env.QUEUE_FILE||'council/sandbox/queue.json',GB=process.env.GAME_BUILD||'6801';
const load=()=>JSON.parse(fs.readFileSync(QF,'utf8'));const save=q=>{fs.writeFileSync(QF+'.tmp',JSON.stringify(q,null,1));fs.renameSync(QF+'.tmp',QF)};
const now=()=>new Date().toISOString();const [cmd,a,b]=process.argv.slice(2);
const STAGES=['stage0-setup-truth','stage0-known-answer','plan-experiments'];  // experiments for each build are added by sandbox-planner via `add`
const PCD='council/sandbox/queue_pc',STAGE=process.env.PC_STAGE||'/mnt/user-data/uploads/e/deadworks-server/sbx_queue';
const safe=id=>id.replace(/[^A-Za-z0-9_.\-]/g,'_');
function cp(src,dst){fs.mkdirSync(path.dirname(dst),{recursive:true});fs.copyFileSync(src,dst)}
if(cmd==='sync'){ // SYNC: first stage the PC files (device_stage_files E:\deadworks-server\sbx_queue\queue.json, progress.txt, controller.lock, results\*.json), then run this.
 const src=a||STAGE;if(!fs.existsSync(src+'/queue.json')){console.log('nothing staged at',src);process.exit(1)}
 let n=0;for(const f of ['queue.json','progress.txt','controller.lock','PAUSE']){if(fs.existsSync(src+'/'+f)){cp(src+'/'+f,PCD+'/'+f);n++}}
 if(fs.existsSync(src+'/results'))for(const f of fs.readdirSync(src+'/results')){cp(src+'/results/'+f,PCD+'/results/'+f);n++}
 console.log('synced',n,'files ->',PCD);process.exit(0)}
if(cmd==='report'){
 const qf=PCD+'/queue.json';if(!fs.existsSync(qf)){console.log('no PC queue synced; run sync');process.exit(1)}
 const q=JSON.parse(fs.readFileSync(qf,'utf8'));const T=q.tasks;const builds=[...new Set(T.map(t=>t.build))],exps=[...new Set(T.map(t=>t.exp))];
 const sym={done:'DONE',pending:'.',running:'RUN',paused:'PAUSE','paused-needs-foreground':'FG-WAIT',blocked:'BLOCK'};const cell=(b,e)=>{const t=T.find(t=>t.build===b&&t.exp===e);if(!t)return '-';let s=sym[t.state]||t.state;if(t.attempts&&t.state!=='done')s+='('+t.attempts+'/3)';return s};
 const w=Math.max(...exps.map(e=>e.length),8);
 console.log('PC QUEUE REPORT (synced',fs.existsSync(PCD+'/progress.txt')?(fs.readFileSync(PCD+'/progress.txt','utf8').split('\n')[0]):'?',')');
 console.log('matrix: build x scenario/checkpoint  (DONE = validly completed with result VALID: yes; .=unfinished; BLOCK = blocked)');
 console.log('build'.padEnd(18)+exps.map(e=>e.padEnd(w+2)).join(''));
 for(const b of builds)console.log(b.padEnd(18)+exps.map(e=>cell(b,e).padEnd(w+2)).join(''));
 const c={};T.forEach(t=>c[t.state]=(c[t.state]||0)+1);const sum=Object.values(c).reduce((x,y)=>x+y,0);
 console.log('\ncounts:',JSON.stringify(c),'total',T.length,sum===T.length?'(reconciled)':'(MISMATCH)');
 console.log('validly completed:',T.filter(t=>t.state==='done').map(t=>t.id).join(', ')||'none');
 console.log('unfinished/remaining:',T.filter(t=>!['done','blocked'].includes(t.state)).map(t=>t.id+'['+t.state+(t.pauseReason?': '+t.pauseReason:'')+']').join(', ')||'none');
 for(const t of T.filter(t=>t.state==='blocked'))console.log('BLOCKED',t.id,'after',t.attempts,'attempts: WHY =',t.blockedReason||(t.log.slice(-1)[0]||{}).why);
 for(const t of T.filter(t=>t.state==='pending'&&t.attempts>0))console.log('RETRYING',t.id,'attempts',t.attempts,'last reason:',(t.lastReasons||[]).join('; '));
 const lk=PCD+'/controller.lock';if(fs.existsSync(lk)){const l=JSON.parse(fs.readFileSync(lk,'utf8'));console.log('controller:',l.owner,'hb',l.hb,l.released?'(released)':'')}
 if(fs.existsSync(PCD+'/PAUSE'))console.log('PAUSED:',fs.readFileSync(PCD+'/PAUSE','utf8').trim());
 const lin=path.resolve(QF);if(fs.existsSync(lin)){const L=JSON.parse(fs.readFileSync(lin,'utf8')).tasks;const lc={};L.forEach(t=>lc[t.state]=(lc[t.state]||0)+1);console.log('\nstage queue (council/sandbox/queue.json):',JSON.stringify(lc),'of',L.length)}
 process.exit(0)}
if(cmd==='init'){if(fs.existsSync(QF)){console.log('exists');process.exit(0)}
 const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();const t=[];
 for(const x of B)for(const s of STAGES)t.push({id:x.id+':'+s,build:x.id,exp:s,state:'pending',attempts:0,log:[]});
 save({created:now(),tasks:t});console.log(t.length,'tasks')}
else{const q=load();const T=id=>q.tasks.find(t=>t.id===id)||(()=>{throw Error('no task '+id)})();
 if(cmd==='status'){const c={};q.tasks.forEach(t=>c[t.state]=(c[t.state]||0)+1);console.log(JSON.stringify(c),'of',q.tasks.length);
  const per={};q.tasks.forEach(t=>{(per[t.build]=per[t.build]||{d:0,n:0,bl:0}).n++;if(t.state==='done')per[t.build].d++;if(t.state==='blocked')per[t.build].bl++});
  console.log('builds fully done:',Object.values(per).filter(p=>p.d===p.n).length,'/',Object.keys(per).length,'; with blocked:',Object.values(per).filter(p=>p.bl).length);
  q.tasks.filter(t=>t.state==='blocked').forEach(t=>console.log('BLOCKED',t.id,'-',t.log.slice(-1)[0].why))}
 else if(cmd==='next'){const t=q.tasks.find(t=>t.state==='pending');console.log(t?t.id:'none')}
 else if(cmd==='start'){const t=T(a);if(t.state==='blocked')throw Error('blocked');t.state='running';t.attempts++;t.started=t.hb=now();save(q);console.log('started',a,'attempt',t.attempts)}
 else if(cmd==='done'){const t=T(a);let f=b;if(f&&f.startsWith('pc:'))f=path.join(PCD,'results',safe(f.slice(3))+'.json');if(!f||!fs.existsSync(f))throw Error('result file required');const raw=fs.readFileSync(f,'utf8');const h=raw.slice(0,1500);
  let pcOk=null;if(f.endsWith('.json')){try{const j=JSON.parse(raw);pcOk=/^VALID:\s*yes$/i.test(j.verdict||'')&&Array.isArray(j.reasons)&&j.reasons.length===0&&(j.checks||{}).setupVerifyOk>0&&(j.damageCsvBytes||0)>0&&(j.samplesCsvBytes||0)>0&&/end of script|end step/.test(j.endWhy||'')}catch(e){pcOk=false}}
  if(pcOk===false||(pcOk===null&&(!/VALID:\s*yes/i.test(h)||/INVALID|UNVALIDATED|unseeded/i.test(h)))||(pcOk===null?false:/UNVALIDATED|unseeded/i.test(h))){t.log.push({at:now(),why:'result not VALID: yes (header/PC checks) -> not counted'});t.state=t.attempts>=3?'blocked':'pending';save(q);console.log('REJECTED: result not valid; task',t.state);process.exit(1)}
  t.state='done';t.result=f;t.gameBuild=GB;t.finished=now();save(q);console.log('done',a)}
 else if(cmd==='fail'||cmd==='invalid'){const t=T(a);t.log.push({at:now(),kind:cmd,why:b});t.state=t.attempts>=3?'blocked':'pending';save(q);console.log(a,cmd,'->',t.state)}
 else if(cmd==='add'){const sf=process.argv[5];if(q.tasks.some(t=>t.id===a+':'+b)){console.log('exists',a+':'+b);process.exit(0)}  // optional 3rd arg: scenario file (meta contract, checked by design-sweep/lint_meta)
  const tk={id:a+':'+b,build:a,exp:b,state:'pending',attempts:0,log:[]};if(sf){if(!fs.existsSync(sf))throw Error('scenario file missing: '+sf);tk.scenarioFile=sf;
   const m={};for(const l of fs.readFileSync(sf,'utf8').split('\n')){const r=l.match(/^meta (\w+) (.*)$/);if(r)m[r[1]]=(m[r[1]]?m[r[1]]+' ':'')+r[2]}tk.meta=m}
  q.tasks.push(tk);save(q);console.log('added',tk.id,sf?'with '+sf:'')}
 else if(cmd==='reopen'){/* targeted patch handling: node queue.js reopen "<comma list of build ids>" "<why e.g. patch notes: Item X changed>"  - only the listed builds' done tasks are reopened; everything else keeps its validated result */
  const ids=a.split(',');let n=0;q.tasks.forEach(t=>{if(t.state==='done'&&ids.includes(t.build)){t.state='pending';t.log.push({at:now(),why:'reopened: '+b});n++}});save(q);console.log(n,'tasks reopened for',ids.length,'builds')}
 else if(cmd==='design-sweep'){/* tasks with no scenario file that passes lint_meta.py (incl. plain-English player_* + strategy_source for build experiments) must not run: state paused-needs-design */
  const cp=require('child_process');let n=0,ok=0;q.tasks.forEach(t=>{if(t.state!=='pending')return;const f=t.scenarioFile&&fs.existsSync(t.scenarioFile)?t.scenarioFile:null;let why=null;
   if(!f)why='no scenario file with meta contract exists for this task (planner has not produced one)';
   else{const r=cp.spawnSync('python3',[__dirname+'/lint_meta.py',f],{encoding:'utf8'});if(r.status!==0)why=(r.stdout||'').trim().slice(0,300)}
   if(why){t.state='paused-needs-design';t.designGap=why;t.log.push({at:now(),why:'design-sweep: '+why});n++}else ok++});save(q);console.log(n,'-> paused-needs-design;',ok,'lint-clean pending')}
 else if(cmd==='retire-unplanned'){/* paused-needs-design tasks are activity, not work: relabel them not-a-queue so they are never counted, shown or run as queued experiments; they come back only through a real scenario file (queue.js add ... <scenario>) */
  let n=0;q.tasks.forEach(t=>{if(t.state==='paused-needs-design'){t.log.push({at:now(),why:'retired: not-a-queue (no scenario file with a meta contract; planner output required before it is a task)'});t.state='not-a-queue';n++}});save(q);console.log(n,'-> not-a-queue')}
 else if(cmd==='reset-stale'){let n=0;q.tasks.forEach(t=>{if(t.state==='running'&&Date.now()-Date.parse(t.hb)>45*60e3){t.log.push({at:now(),why:'stale running task reset (crash/disconnect)'});t.state=t.attempts>=3?'blocked':'pending';n++}});save(q);console.log(n,'reset')}
 else console.log('see header')}

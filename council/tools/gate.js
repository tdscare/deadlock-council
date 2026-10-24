// THE ONLY WAY TO CHANGE A BUILD.  node council/tools/gate.js check|apply council/proposals/<name>.json
// proposal: {id, buildFile (JS/JSON object literal of the FULL new build, without `changes`), reason, evidence:[{path,kind:"data"|"calc"|"measured",note}], 
//            (kind `context` = build-context comparison file: header lines SCOPE: build-context / BUILD: <id> / ITEM: <name> / ESTIMATE: <name> | item=<x>% | alt=<name> <y>%; see section 6 below and abtimeline.py --context)
//            waive:[{rule,why}] (optional, explicit, recorded), expect:{add:[...],remove:[...]} (optional, what you claim the change does)}
//            (kind `strategy` = abtimeline.py --strategy file: KIND: strategy / SCOPE: build-context / BUILD / CONCLUSION / CHOSEN-PATH / CHOSEN-ORDER / BODY-SHA / INPUT-SHA; see section 4c)
// check: runs every validator on OLD and NEW data, blocks on any NEW violation, missing reason/evidence, stale base, or sandbox evidence marked invalid.
// apply: requires council/approvals/<name>.ok (written only after Kieran approves; contains sha256 of the proposal file). Snapshots, unlocks, writes, relocks, records.
const fs=require('fs'),cp=require('child_process'),cr=require('crypto'),path=require('path');
const SP=path.resolve(__dirname,'../..');process.chdir(SP);
const [mode,pf]=process.argv.slice(2);if(!mode||!pf){console.log('usage: gate.js check|apply <proposal.json>');process.exit(2)}
const sha=f=>cr.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const P=JSON.parse(fs.readFileSync(pf,'utf8'));const name=path.basename(pf,'.json');
const block=[],warn=[];const bl=m=>block.push(m),wn=m=>warn.push(m);
// 0. base must be the recorded head
const HEAD='council/history/HEAD.sha';
if(!fs.existsSync(HEAD))fs.writeFileSync(HEAD,sha('data.js'));
if(fs.readFileSync(HEAD,'utf8').trim()!==sha('data.js'))bl('data.js differs from recorded head (council/history/HEAD.sha): it was modified outside the gate');
// 1. paperwork
if(!P.id)bl('no build id');if(!P.reason||P.reason.length<30)bl('reason missing/too short');
if(!Array.isArray(P.evidence)||!P.evidence.length)bl('no evidence listed');
const scopeOf=t=>(t.slice(0,3000).match(/^\s*(?:>\s*)?SCOPE:\s*(isolated|build-context)\b/mi)||[])[1]?.toLowerCase();
for(const e of P.evidence||[]){if(!fs.existsSync(e.path)){bl('evidence file missing: '+e.path);continue}
 {const t=fs.readFileSync(e.path,'utf8'),sc=scopeOf(t),isRes=/council\/sandbox\/results\//.test(e.path);
  if(e.kind==='measured'||e.kind==='context'){ if(!sc)bl(e.kind+' evidence has no `SCOPE: isolated|build-context` header line: '+e.path);
   else if(e.kind==='measured'&&sc==='isolated')bl('isolated-scope result cited as measured evidence for a purchase: '+e.path+' (an isolated item test may only be cited as kind `data`, for mechanism)');
   else if(e.kind==='context'&&sc!=='build-context')bl('context evidence must be SCOPE: build-context: '+e.path)}
  else if(isRes&&sc==='isolated')wn('isolated-scope sandbox result cited as '+e.kind+' (mechanism only, not a purchase verdict): '+e.path)
  else if(isRes&&!sc)wn('sandbox result has no SCOPE line, treat as isolated: '+e.path)}
 if(e.kind==='measured'){const t=fs.readFileSync(e.path,'utf8');if(/INVALID|UNVALIDATED|unseeded/i.test(t.slice(0,2000)))bl('measured evidence marked invalid/unvalidated: '+e.path);
  bl('measured evidence not accepted until the Sandbox results path is validated (audit sandbox.md gap 1): '+e.path)}
 if(!['data','calc','measured','context','strategy','interaction','weakness'].includes(e.kind))bl('evidence kind must be data|calc|measured|context|strategy|interaction|weakness: '+e.path)}
if(!P.evidence?.some(e=>e.kind==='data'||e.kind==='calc'))bl('need at least one data/calc evidence file (recomputable from game data)');
// 2. load builds
const src=fs.readFileSync('data.js','utf8');const a=src.indexOf('const B=[');const e=src.indexOf('\n];',a);
const pre=src.slice(0,a),post=src.slice(e+3);const B=new Function(src+';return B;')();
const i=B.findIndex(x=>x.id===P.id);
const nb=new Function('return ('+fs.readFileSync(P.buildFile,'utf8').trim().replace(/[,;]\s*$/,'')+')')();
if(nb.id!==P.id)bl('buildFile id '+nb.id+' != '+P.id);
const old=i>=0?B[i]:null;if(!old)wn('new build (not a replacement)');
nb.changes=old?(old.changes||[]).slice():[];
const K=s=>JSON.stringify(s);
const ser=b=>{const head=Object.keys(b).filter(k=>k!=='rows'&&k!=='changes').map(k=>k+':'+K(b[k])).join(',');
 return '{'+head+',\n rows:[\n'+b.rows.map(r=>'  ['+r.map(x=>K(x)).join(',\n   ')+']').join(',\n')+'\n ],\n changes:'+K(b.changes||[])+'}'};
const flat=b=>{const o=[];b.rows.forEach(r=>r.forEach(([t,d,op,its])=>its.forEach(it=>o.push(t+'|'+it[0]))));return o};
// 3. auto diff -> changes line (cannot be skipped or edited)
let diff=[];if(old){const A=flat(old),Bn=flat(nb);const add=Bn.filter(x=>!A.includes(x)),rem=A.filter(x=>!Bn.includes(x));
 const ord=b=>b.rows.flat().filter(([t])=>/^(Early|Mid|Late)/.test(t)).flatMap(([t,d,o,its])=>its.map(x=>x[0])).join(' > ');
 if(add.length)diff.push('added '+add.join(', '));if(rem.length)diff.push('removed '+rem.join(', '));
 if(ord(old)!==ord(nb)&&!add.length&&!rem.length)diff.push('core order changed');
 if(old.order.join('')!==nb.order.join(''))diff.push('ability order '+old.order.join('')+' -> '+nb.order.join(''));
 {const nt=b=>{const o={};b.rows.forEach(r=>r.forEach(([t,d,op,its])=>its.forEach(it=>{o[it[0]]=(it[1]||'')+'|'+(it[2]||'')})));return o};const NO=nt(old),NN=nt(nb);
  const nc=Object.keys(NN).filter(k=>k in NO&&NO[k]!==NN[k]);if(nc.length)diff.push('notes/imbues changed on '+nc.join(', '))}
 if(!diff.length)bl('proposal makes no change');}
// 4. validators on OLD vs NEW (regression gate: no new violations; existing ones are listed, not hidden)
const tmp='council/history/_tmp_'+name;fs.mkdirSync(tmp,{recursive:true});
nb.changes=[...(old?.changes||[]),'(pending) '+P.reason.trim()+' | '+diff.join('; ')];  // validators see the reason (e.g. Threshold: lines)
const candB=B.slice();if(i>=0)candB[i]=nb;else candB.push(nb);
fs.writeFileSync(tmp+'/data.js',pre+'const B=[\n'+candB.map(ser).join(',\n\n')+'\n];'+post);
const sub=(txt)=>txt.replace(/fs\.readFileSync\('data\.js'/g,"fs.readFileSync(process.env.DATA||'data.js'").replace(/process\.chdir\(__dirname\+'\/\.\.\/\.\.'\)/,"process.chdir('"+SP+"')").replace(/council\/audit\/tmp\/builds_check_full\.json/,'council/history/_tmp_'+name+'/bc_'+'${TAG}.json');
function violations(dataFile,tag){const out={};
 // (a) builds_check (structure, spikes, rich/counters/slot-locked, names, sells, round-trip)
 let t=sub(fs.readFileSync('council/audit/builds_check.js','utf8')).replace('${TAG}',tag);fs.writeFileSync(tmp+'/bc_'+tag+'.js',t);
 try{cp.execSync('node '+tmp+'/bc_'+tag+'.js >/dev/null',{env:{...process.env,DATA:dataFile,N:'999'},stdio:['ignore','pipe','pipe']})}catch(x){bl('VALIDATOR CRASHED (builds_check, '+tag+'): '+(x.stderr||x.message).toString().slice(0,200))}
 try{const F=JSON.parse(fs.readFileSync(tmp+'/bc_'+tag+'.json','utf8'));for(const r in F)for(const m of F[r])if(m.startsWith(P.id+':'))(out.bc=out.bc||[]).push(r+' '+m)}catch(x){bl('VALIDATOR PRODUCED NO OUTPUT (builds_check, '+tag+')')}
 // (b) walk1 FLAGS + check12 on the single build
 const get=()=>{const s=fs.readFileSync(dataFile,'utf8');return new Function(s+';return B')().find(x=>x.id===P.id)};
 const bb=get();if(bb){fs.writeFileSync(tmp+'/b_'+tag+'.json',JSON.stringify(bb));
  const w=cp.execSync('node a3/walk1.js '+tmp+'/b_'+tag+'.json').toString();const f=w.split('FLAGS:')[1]||'';out.walk=/^\s*none/.test(f)?[]:f.trim().split('\n').filter(Boolean);
  const c=cp.execSync('node a12/check.js '+tmp+'/b_'+tag+'.json').toString();out.c12=/CHECK12: none/.test(c)?[]:c.trim().split('\n').filter(Boolean);}
 // (c) ability-point/charge/threshold timeline gate
 try{const t2=fs.readFileSync('council/tools/abtimeline.py','utf8').split(SP+"/data.js").join(dataFile).replace(/SP \+ '\/data\.js'/g,"os.environ.get('DATA', SP + '/data.js')");fs.writeFileSync(tmp+'/abt_'+tag+'.py',t2.replace(/^SP = .*$/m,"SP = '"+SP+"'"));
  let o='';try{o=cp.execSync('python3 -I '+tmp+'/abt_'+tag+'.py --gate '+P.id,{env:{...process.env,DATA:path.resolve(dataFile)}}).toString()}catch(x){o=(x.stdout||'').toString()}
  const j=JSON.parse(o.trim().split('\n').pop());out.abt=j.flatMap(g=>g.errors.map(e=>e.join(' ')));}catch(x){bl('VALIDATOR CRASHED (abtimeline, '+tag+'): '+x.message.slice(0,120))}
 return out}
const vo=old?violations('data.js','old'):{},vn=violations(tmp+'/data.js','new');
const norm=s=>s.replace(/\d+(\.\d+)?k?/g,'#');const newV=[],fixed=[],kept=[];
for(const k of new Set([...Object.keys(vo),...Object.keys(vn)])){const o=(vo[k]||[]).map(norm),n=vn[k]||[];
 for(const m of n)(o.includes(norm(m))?kept:newV).push(k+': '+m);
 for(const m of vo[k]||[])if(!(vn[k]||[]).map(norm).includes(norm(m)))fixed.push(k+': '+m)}
const IGN=/^bc: (RT_|SITE_STALE|CODES_JSON_STALE)/;  // export round-trip is re-verified after rebuild (see apply)
const waived=(P.waive||[]).filter(w=>w.rule&&w.why&&w.why.length>20&&w.evidence&&fs.existsSync(w.evidence));  // a waiver (e.g. delaying a 4.8k spike to fix a weakness) must cite a computed path comparison file
(P.waive||[]).forEach(w=>{if(!waived.includes(w))bl('waiver for '+w.rule+' lacks why(>20 chars) or an existing evidence file with the computed comparison')});
for(const m of newV){if(IGN.test(m))continue;const w=waived.find(w=>m.includes(w.rule));if(w){wn('WAIVED '+m.slice(0,100)+' because: '+w.why);continue}bl('NEW violation introduced: '+m)}
// 4b. overlap-candidates valued inside the complete build (abtimeline.py --overlap). Overlap is a CANDIDATE signal only; it blocks nothing by itself.
// A proposal that ADDS an item or moves one EARLIER, whose item is an overlap-candidate with a LOW (REDUNDANT-LIKELY) or UNKNOWN marginal estimate (or a same-cost
// alternative already listed in the build that gives more on the same metric), must cite a passing `context` file. Flagged items already in the build are listed UNRESOLVED.
const flatCore=b=>b.rows.flat().filter(([t])=>/^(Early|Mid|Late)/.test(t)).flatMap(([t,d,o,its])=>its.map(x=>x[0]));
const flatAll=b=>b.rows.flat().flatMap(([t,d,o,its])=>its.map(x=>x[0]));
const needsCtx=o=>['at_buy','core_end'].some(k=>{const v=o[k];return v&&v.candidate&&(['REDUNDANT-LIKELY','UNKNOWN'].includes(v.verdict)||(v.alternatives&&v.alternatives.best_alt_beats_item))});
let OV=null;const ovLines=[],ovUnres=[];
try{const t2=fs.readFileSync('council/tools/abtimeline.py','utf8').split(SP+"/data.js").join(tmp+'/data.js').replace(/SP \+ '\/data\.js'/g,"os.environ.get('DATA', SP + '/data.js')");
 fs.writeFileSync(tmp+'/abt_ov.py',t2.replace(/^SP = .*$/m,"SP = '"+SP+"'"));
 OV=JSON.parse(cp.execSync('python3 -I '+tmp+'/abt_ov.py --overlap '+P.id+' --json',{env:{...process.env,DATA:path.resolve(tmp+'/data.js')},maxBuffer:1<<28}).toString().trim().split('\n').pop())[0];
}catch(x){bl('VALIDATOR CRASHED (overlap): '+(x.stderr||x.message).toString().slice(0,200))}
if(OV){const oldC=old?flatCore(old):[],newC=flatCore(nb),oldA=old?flatAll(old):[];const changed=[];
 for(const n of newC){if(!old||!oldA.includes(n)){changed.push([n,'added']);continue}
  if(!oldC.includes(n)){changed.push([n,'moved optional->core']);continue}
  const pb=oldC.slice(0,oldC.indexOf(n)),pn=newC.slice(0,newC.indexOf(n));if(pb.some(y=>newC.includes(y)&&!pn.includes(y)))changed.push([n,'moved earlier'])}
 for(const n of flatAll(nb))if(!newC.includes(n)&&!oldA.includes(n)&&old)changed.push([n,'added (optional)']);
 const ctxFiles=(P.evidence||[]).filter(e=>e.kind==='context'&&fs.existsSync(e.path)&&scopeOf(fs.readFileSync(e.path,'utf8'))==='build-context').map(e=>({e,t:fs.readFileSync(e.path,'utf8')}));
 const rep1=o=>['at_buy','core_end'].map(k=>o[k]&&o[k].candidate?k+'='+o[k].verdict+(o[k].whole_item_gun_gain!=null?'('+o[k].whole_item_gun_gain.toFixed(1)+'% whole item)':'')+(o[k].alternatives&&o[k].alternatives.best_alt_beats_item?' ALT-BETTER '+JSON.stringify(o[k].alternatives.alts[0]):''):null).filter(Boolean).join('; ');
 for(const [n,why] of changed){const o=OV.items.find(i=>i.item===n);if(!o||!['at_buy','core_end'].some(k=>o[k]&&o[k].candidate)){ovLines.push('  overlap '+n+' ('+why+'): no overlap-candidate'); continue}
  ovLines.push('  overlap '+n+' ('+why+'): '+rep1(o));
  if(!needsCtx(o))continue;
  const cf=ctxFiles.find(c=>new RegExp('^BUILD:\\s*'+P.id+'\\s*$','m').test(c.t)&&c.t.split('\n').some(l=>l.replace(/^ITEM:\s*/,'')===n&&/^ITEM:/.test(l)));
  if(!cf){bl('OVERLAP: '+n+' ('+why+') is an overlap-candidate with a low/unknown in-build marginal ('+rep1(o)+') and no `context` evidence file (SCOPE: build-context, BUILD: '+P.id+', ITEM: '+n+') compares the complete build with/without it vs the alternative use of the same souls');continue}
  const m=cf.t.match(new RegExp('^ESTIMATE:\\s*'+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\s*\\|\\s*item=(-?[\\d.]+)%\\s*\\|\\s*alt=(.+?)\\s+(-?[\\d.]+)%','m'));
  if(!m){bl('OVERLAP: context file for '+n+' states no numeric estimate (`ESTIMATE: '+n+' | item=<x>% | alt=<name> <y>%`): "cannot estimate" does not unblock, run the named test first: '+cf.e.path);continue}
  if(+m[1]<+m[3])bl('OVERLAP: context file '+cf.e.path+' itself shows the alternative use of the souls ('+m[2]+' '+m[3]+'%) beats '+n+' ('+m[1]+'%); change the proposal or waive with evidence');
  else ovLines.push('  context OK for '+n+': item '+m[1]+'% vs alt '+m[2]+' '+m[3]+'% ('+cf.e.path+')')}
 const chN=new Set(changed.map(c=>c[0]));
 for(const o of OV.items)if(!chN.has(o.item)&&needsCtx(o))ovUnres.push('overlap-candidate '+o.item+' ['+rep1(o)+']');
}
// 4c. STRATEGY rule (Kieran 13:56): a proposal that changes the purchase order, the green (vitality) items or a 4.8k spike's timing in the core must cite a
// `strategy` evidence file (abtimeline.py --strategy) for this build that (1) is unedited (BODY-SHA) and current (INPUT-SHA = today's data/vdata/tool),
// (2) concludes CHOSEN (not INSUFFICIENT EVIDENCE / DEPENDS ON ASSUMPTION), and (3) whose CHOSEN-PATH equals the proposed core purchase sequence and CHOSEN-ORDER
// the proposed ability order. Otherwise BLOCK, unless waived with waive:[{rule:'STRATEGY',why,evidence:<computed file>}] (recorded).
const strat={trig:[],lines:[]};
{const IFJ=JSON.parse(fs.readFileSync('audit/items_full.json','utf8'));const vit=n=>(IFJ[n]||{}).slot==='Armor';
 const oc=old?flatCore(old):[],ncr=flatCore(nb);
 const common=ncr.filter(x=>oc.includes(x)),commonOld=oc.filter(x=>ncr.includes(x));
 if(old&&common.join('>')!==commonOld.join('>'))strat.trig.push('purchase order');
 // greens: set of core vitality items, and each green's place among the items present in BOTH cores (insertions elsewhere do not count)
 const gset=c=>c.filter(vit).sort().join(','),both=x=>oc.includes(x)&&ncr.includes(x);
 const gpos=c=>c.filter(both).map((x,i,a)=>vit(x)?x+'@'+a.slice(0,i).filter(y=>!vit(y)).length:null).filter(Boolean).join(',');
 if(old&&(gset(oc)!==gset(ncr)||gpos(oc)!==gpos(ncr)))strat.trig.push('greens ('+(oc.filter(vit).join(',')||'none')+' -> '+(ncr.filter(vit).join(',')||'none')+')');
 let so=null,sn=null;
 try{so=JSON.parse(cp.execSync('python3 -I council/tools/abtimeline.py --spikes '+P.id).toString().trim().split('\n').pop())}catch(x){}
 try{sn=JSON.parse(cp.execSync('python3 -I '+tmp+'/abt_new.py --spikes '+P.id,{env:{...process.env,DATA:path.resolve(tmp+'/data.js')}}).toString().trim().split('\n').pop())}catch(x){}
 if(old&&so&&sn){const d=Object.keys(sn).filter(c=>so[c]!==sn[c]);if(d.length)strat.trig.push('4.8k spike timing ('+d.map(c=>c+' '+so[c]+' -> '+sn[c]).join(', ')+')')}
 else if(old)bl('VALIDATOR CRASHED (spikes): cannot compute 4.8k spike timing for the strategy rule');
 if(strat.trig.length){
  const sw=(P.waive||[]).find(w=>w.rule==='STRATEGY'&&waived.includes(w));
  const SF=(P.evidence||[]).filter(e=>e.kind==='strategy'&&fs.existsSync(e.path));
  const ish=(()=>{try{return cp.execSync('python3 -I council/tools/abtimeline.py --input-sha').toString().trim()}catch(x){return null}})();
  const errs=[];let ok=null;
  if(!SF.length)errs.push('cites no `strategy` evidence file (run abtimeline.py --strategy '+P.id+' <checkpoints> and cite it as kind `strategy`)');
  for(const e of SF){const s=fs.readFileSync(e.path,'utf8'),h=k=>(s.match(new RegExp('^'+k+':\\s*(.*)$','m'))||[])[1];const why=[];
   if(h('KIND')!=='strategy'||!/^build-context/.test(h('SCOPE')||''))why.push('not a strategy file (KIND: strategy, SCOPE: build-context)');
   if(h('BUILD')!==P.id)why.push('BUILD '+h('BUILD')+' != '+P.id);
   const v=cp.spawnSync('python3',['-I','council/tools/abtimeline.py','--verify-strategy',e.path],{encoding:'utf8'});if(v.status!==0)why.push('BODY-SHA mismatch: edited after generation (post-hoc)');
   if(ish&&h('INPUT-SHA')!==ish)why.push('stale: INPUT-SHA differs from current data.js/vdata/items/tool (regenerate before citing)');
   const c=h('CONCLUSION')||'';
   if(!/^CHOSEN:/.test(c))why.push('conclusion is "'+c+'" (needs CHOSEN; INSUFFICIENT EVIDENCE / DEPENDS ON ASSUMPTION cannot justify a path change)');
   else{const cpth=(h('CHOSEN-PATH')||'').split(' > ').map(x=>x.trim()).filter(Boolean),cord=(h('CHOSEN-ORDER')||'').trim();
    if(cpth.join('>')!==ncr.join('>')){const k=cpth.findIndex((x,i)=>x!==ncr[i]);why.push('chosen alternative '+c.slice(8)+' path differs from the proposed core at position '+k+' ('+cpth[k]+' vs '+ncr[k]+')')}
    if(cord&&cord!==nb.order.join(''))why.push('chosen ability order '+cord+' != proposed '+nb.order.join(''))}
   if(why.length)errs.push(e.path+': '+why.join('; '));else ok=e.path}
  if(ok)strat.lines.push('STRATEGY OK: '+strat.trig.join(' + ')+' justified by '+ok);
  else if(sw){wn('WAIVED STRATEGY ('+strat.trig.join(' + ')+') because: '+sw.why+' | '+errs.join(' | '));strat.lines.push('STRATEGY WAIVED')}
  else{bl('STRATEGY: proposal changes '+strat.trig.join(' + ')+' but '+errs.join(' | '));strat.lines.push('STRATEGY BLOCK')}}
 else strat.lines.push('STRATEGY: not triggered (no purchase-order/greens/spike-timing change)')}
// 4d. INTERACTION rule (Kieran 14:29): every damage / fire-rate / stat item that the proposal adds to, removes from or reorders in the core must cite an
// `interaction` evidence file (abtimeline.py --interactions <id> <item>): KIND: interaction, BUILD, ITEM, unedited (BODY-SHA), current (INPUT-SHA). Missing -> BLOCK.
// A matrix whose VERDICT says the item is beaten in every window, or INSUFFICIENT EVIDENCE, is flagged (WARN) with its open test requests.
const inter={lines:[]};
{const I69=JSON.parse(fs.readFileSync('audit/items_full_6819.json','utf8'));
 const STATK=/^(BaseAttackDamagePercent|CloseRangeBonusWeaponPower|LongRangeBonusWeaponPower|BonusFireRate|FireRateBonus|BonusClipSizePercent|BonusClipSize|HeadShotBonusDamage|BulletLifestealPercent|TechPower|SpiritPower|BonusBulletSpeedPercent|ProcChance|BuildUpPerShot|RicochetDamagePercent|BonusMeleeDamagePercent|ImbuedTechPower|ActivatedFireRate)$/;
 const isStat=n=>Object.keys((I69[n]||{}).stats||{}).some(k=>STATK.test(k));
 const oc=old?flatCore(old):[],ncr=flatCore(nb);const ch=[];
 for(const n of ncr)if(!oc.includes(n))ch.push([n,'added']);
 for(const n of oc)if(!ncr.includes(n))ch.push([n,'removed']);
 {const A1=oc.filter(x=>ncr.includes(x)),B1=ncr.filter(x=>oc.includes(x));const L=A1.map(()=>new Array(B1.length+1).fill(0));L.push(new Array(B1.length+1).fill(0));
  for(let i=A1.length-1;i>=0;i--)for(let j=B1.length-1;j>=0;j--)L[i][j]=A1[i]===B1[j]?L[i+1][j+1]+1:Math.max(L[i+1][j],L[i][j+1]);
  const keep=new Set();let i=0,j=0;while(i<A1.length&&j<B1.length){if(A1[i]===B1[j]){keep.add(A1[i]);i++;j++}else if(L[i+1][j]>=L[i][j+1])i++;else j++}
  for(const n of B1)if(!keep.has(n))ch.push([n,'reordered'])}   // moved items = not in the longest common subsequence of the old/new core order
 const IFs=(P.evidence||[]).filter(e=>e.kind==='interaction'&&fs.existsSync(e.path)).map(e=>({e,t:fs.readFileSync(e.path,'utf8')}));
 const ish=(()=>{try{return cp.execSync('python3 -I council/tools/abtimeline.py --input-sha').toString().trim()}catch(x){return null}})();
 for(const [n,why] of ch){if(!isStat(n))continue;const h=(t,k)=>(t.match(new RegExp('^'+k+':\\s*(.*)$','m'))||[])[1];
  const f=IFs.find(x=>h(x.t,'KIND')==='interaction'&&h(x.t,'BUILD')===P.id&&h(x.t,'ITEM')===n);
  if(!f){bl('INTERACTION: '+n+' ('+why+') is a damage/fire-rate/stat item and no `interaction` evidence (abtimeline.py --interactions '+P.id+' "'+n+'") is cited');inter.lines.push('INTERACTION BLOCK '+n);continue}
  const v=cp.spawnSync('python3',['-I','council/tools/abtimeline.py','--verify-strategy',f.e.path],{encoding:'utf8'});
  if(v.status!==0){bl('INTERACTION: '+f.e.path+' BODY-SHA mismatch (edited after generation)');continue}
  if(ish&&h(f.t,'INPUT-SHA')!==ish){bl('INTERACTION: '+f.e.path+' is stale (INPUT-SHA differs from current data/tool); regenerate');continue}
  const vd=h(f.t,'VERDICT')||'';const nreq=(f.t.match(/^\s+\S+autorun\/scenarios\/interaction\/\S+$/mg)||[]).length;
  if(/^INSUFFICIENT|beaten in every window/.test(vd))wn('INTERACTION FLAG '+n+' ('+why+'): '+vd.slice(0,160)+(nreq?' | open test requests: '+nreq:''));
  inter.lines.push('INTERACTION OK '+n+' ('+why+'): '+vd.slice(0,140)+' ['+f.e.path+']')}
 if(!inter.lines.length)inter.lines.push('INTERACTION: no damage/fire-rate/stat item added, removed or reordered')}
// 4e. WEAKNESS rule (Kieran 15:19/15:20): a proposal justified by a weakness (field `weakness`, or reason says weakness/fix/problem) must cite a `weakness` file
// (abtimeline.py --weakness) for this build: unedited, current, ROOT-CAUSE + REMEDY-SET + NO-FIX + SIMPLE-REMEDY generated (not MISSING). If that file concludes
// NO FIX NEEDED or INSUFFICIENT EVIDENCE, a purchase made for the weakness is blocked.
const weak={lines:[]};
if(P.weakness||/\b(weakness|to fix|fixes|fixing|problem)\b/i.test(P.reason||'')){const h=(t,k)=>(t.match(new RegExp('^'+k+':\\s*(.*)$','m'))||[])[1];
 const WF=(P.evidence||[]).filter(e=>e.kind==='weakness'&&fs.existsSync(e.path)).map(e=>({e,t:fs.readFileSync(e.path,'utf8')})).filter(x=>h(x.t,'KIND')==='weakness'&&h(x.t,'BUILD')===P.id);
 const ish=(()=>{try{return cp.execSync('python3 -I council/tools/abtimeline.py --input-sha').toString().trim()}catch(x){return null}})();
 if(!WF.length){bl('WEAKNESS: proposal is justified by a weakness but cites no `weakness` file with the remedy set (abtimeline.py --weakness '+P.id+' <class>)');weak.lines.push('WEAKNESS BLOCK')}
 for(const f of WF){const why=[];const v=cp.spawnSync('python3',['-I','council/tools/abtimeline.py','--verify-strategy',f.e.path],{encoding:'utf8'});if(v.status!==0)why.push('BODY-SHA mismatch');
  if(ish&&h(f.t,'INPUT-SHA')!==ish)why.push('stale INPUT-SHA');for(const k of ['ROOT-CAUSE','REMEDY-SET','NO-FIX','SIMPLE-REMEDY'])if(!h(f.t,k))why.push(k+' missing');
  if(/MISSING/.test(h(f.t,'SIMPLE-REMEDY')||''))why.push('simple direct remedy was not generated/scored');const c=h(f.t,'CONCLUSION')||'';
  if(/^(NO FIX NEEDED|INSUFFICIENT)/.test(c))why.push('its conclusion is "'+c.slice(0,80)+'": no purchase is justified by this weakness');
  if(why.length){bl('WEAKNESS: '+f.e.path+': '+why.join('; '));weak.lines.push('WEAKNESS BLOCK')}else weak.lines.push('WEAKNESS OK: '+c.slice(0,140)+' ['+f.e.path+']')}}
else weak.lines.push('WEAKNESS: proposal is not justified by a weakness');
// 4f. INVESTMENT / SALES rule (Kieran 15:35, a862015c): detectors over the proposed build vs the old one (abtimeline.py --sales). A NEW finding of kind `4.8k drop`
// (an established 4.8k colour investment falls below 4.8k), `component sold before planned upgrade`, `sale of item already gone` or `redundant purchase` BLOCKS unless
// waived with waive:[{rule:'INVESTMENT'|'SALES', why(>20 chars), evidence:<computed file, e.g. abtimeline.py --seq / --path audit output>}]. Pre-existing findings are listed, not blocking.
const sales={lines:[]};
{const run=(py,env)=>{try{return JSON.parse(cp.execSync('python3 -I '+py+' --sales '+P.id,{env:{...process.env,...env},maxBuffer:1<<26}).toString().trim().split('\n').pop())}catch(x){return null}};
 const fo=old?run('council/tools/abtimeline.py',{}):[],fn=run(tmp+'/abt_new.py',{DATA:path.resolve(tmp+'/data.js')});
 if(fn===null)bl('VALIDATOR CRASHED (sales detectors)');
 else{const key=f=>f.kind+'|'+f.item,ok=new Set((fo||[]).map(key));const nw=fn.filter(f=>!ok.has(key(f)));
  const wv=r=>(P.waive||[]).find(w=>w.rule===r&&waived.includes(w));
  for(const f of nw){const r=f.kind==='4.8k drop'?'INVESTMENT':'SALES',w=wv(r);
   if(w){wn('WAIVED '+r+' '+f.detail+' because: '+w.why);sales.lines.push(r+' WAIVED '+f.item)}
   else{bl(r+': new finding "'+f.kind+'": '+f.detail+' (cite a computed comparison and waive, or change the proposal)');sales.lines.push(r+' BLOCK '+f.item)}}
  fn.filter(f=>ok.has(key(f))).forEach(f=>sales.lines.push('SALES pre-existing: '+f.kind+': '+f.detail));
  if(!fn.length)sales.lines.push('SALES: no investment drop, sale-before-upgrade or redundant purchase detected')}}
// 5. record text
const stamp=new Date().toISOString().slice(0,16).replace('T',' ');
const line='['+stamp+'] '+P.reason.trim()+' | '+diff.join('; ')+' | evidence: '+P.evidence.map(e=>e.kind+':'+e.path).join(', ')+' | gate: '+(newV.length?'FAIL':'pass; fixed '+fixed.length+', pre-existing '+kept.length);
nb.changes=[...(old?.changes||[]),line];  // final text (note: written only on apply)
console.log('BUILD',P.id,'| diff:',diff.join('; '));console.log('fixed:',fixed.length,'| UNRESOLVED in resulting build:',kept.length,'| NEW:',newV.length);
const KEPT_ALL=[...kept,...(vn.walk||[]).map(x=>'walk: '+x),...(vn.c12||[]).map(x=>'c12: '+x)];
fixed.slice(0,8).forEach(x=>console.log('  fixed  ',x.slice(0,200)));KEPT_ALL.forEach(x=>console.log('  UNRESOLVED',x.slice(0,200)));
strat.lines.forEach(x=>console.log(x));inter.lines.forEach(x=>console.log(x));weak.lines.forEach(x=>console.log(x));sales.lines.forEach(x=>console.log(x));console.log('OVERLAP check (changed items):');ovLines.forEach(x=>console.log(x));console.log('UNRESOLVED overlap-candidates in resulting build (not part of this change):',ovUnres.length);ovUnres.slice(0,6).forEach(x=>console.log('  UNRESOLVED',x.slice(0,230)));
warn.forEach(w=>console.log('WARN',w));block.forEach(b=>console.log('BLOCK',b));
const report={strategy:strat,interaction:inter,weakness:weak,overlap:{changed:ovLines,unresolved:ovUnres},unresolved:KEPT_ALL,proposal:name,id:P.id,diff,block,warn,fixed,kept,newV,when:stamp,line};fs.writeFileSync('council/history/'+name+'.report.json',JSON.stringify(report,null,1));
if(block.length){console.log('RESULT: BLOCKED');process.exit(1)}
if(mode==='check'){console.log('RESULT: PASSES GATE (not applied; needs approval file council/approvals/'+name+'.ok)');process.exit(0)}
// apply
const okf='council/approvals/'+name+'.ok';
if(!fs.existsSync(okf)||fs.readFileSync(okf,'utf8').trim()!==sha(pf)){console.log('BLOCKED: no approval for this exact proposal (council/approvals/'+name+'.ok must contain sha256 of the proposal)');process.exit(1)}
const snap='council/history/'+stamp.replace(/[ :-]/g,'')+'_'+P.id+'.before.js';fs.copyFileSync('data.js',snap);
const out=pre+'const B=[\n'+candB.map(ser).join(',\n\n')+'\n];'+post;
new Function(out+';return B')();
cp.execSync('chattr -i data.js');fs.writeFileSync('data.js',out);cp.execSync('chmod 444 data.js; chattr +i data.js');
fs.writeFileSync(HEAD,sha('data.js'));fs.appendFileSync('council/history/LOG.jsonl',JSON.stringify({...report,pre:snap,post:sha('data.js')})+'\n');
console.log('APPLIED',P.id,'; snapshot',snap,'; run rebuild.sh to refresh site/exports (not done automatically)');

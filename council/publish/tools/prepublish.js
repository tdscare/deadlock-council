#!/usr/bin/env node
// Pre-publish checker (wrapper around, never replacing, council/tools/gate.js).
//   node prepublish.js check <id> [--build-file f.json] [--checklist f.json] [--json]
//   node prepublish.js scaffold <id>        write checklists/<id>.json skeleton with attached existing evidence (all items unproven)
// exit 0 = validated, 1 = not validated, 2 = usage
const C=require('../lib/common');const R=require('../lib/record');const E=require('../lib/evidence');const L=require('../lib/lint');const RT=require('./roundtrip');const I=require('../lib/identity');const {fs,path,PUB,SP}=C;
const ALWAYS=['progression_spikes','ability_upgrades','thresholds_sales','alternative_comparison','limitations_listed','naming_coherence','description_basis','captions_complete','tags_verified','export_roundtrip'];
const PURPOSE_ALL=['damage','sustain','survivability','farming','activations_rotations','synergies','temporary_purchases','situational_swaps','utility_contribution'];
function purposeFor(classes){const p=new Set(['activations_rotations','synergies','temporary_purchases','situational_swaps']);
 for(const c of classes){if(/damage/.test(c)){p.add('damage');p.add('farming');p.add('survivability')}if(/support/.test(c)){p.add('utility_contribution');p.add('survivability')}if(/fighter|tank/.test(c)){p.add('sustain');p.add('survivability');p.add('damage')}}return [...p]}
const coreSeq=c=>C.items(c).filter(i=>i.core&&!i.opt).map(i=>i.name);
function check(id,opts={}){
 const ctx=C.loadGame();ctx.data=C.loadData();
 let rec;if(opts.buildFile){const content=new Function('return ('+fs.readFileSync(opts.buildFile,'utf8').trim().replace(/[,;]\s*$/,'')+')')();rec={schema:1,kind:'build-record',id,slot:'candidate',content:R.strip(content),revision:{n:0,content_sha:R.contentSha(content),ref:R.refOf(id,0,R.contentSha(content))}}}else rec=R.liveRecord(id);
 const c=rec.content;const out={build:id,revision:rec.revision.ref,content_sha:rec.revision.content_sha,items:{},blockers:[],notes:[]};
 const cl=opts.checklist||path.join(PUB,'checklists',id+'.json');let ck=null;if(fs.existsSync(cl)){try{ck=JSON.parse(fs.readFileSync(cl,'utf8'))}catch(e){out.blockers.push('checklist unreadable: '+e.message)}}
 if(!ck)out.blockers.push('no checklist file ('+path.relative(SP,cl)+'): nothing has been claimed or evidenced');
 else{if(ck.format!=='build-validation-checklist/1')out.blockers.push('wrong checklist format');if(ck.content_sha!==rec.revision.content_sha)out.blockers.push('checklist is for different build content (content_sha mismatch): re-validate this revision')}
 const lint=L.lintBuild(c,ctx,E.buildContext(id).length>0);const classes=lint.res.classes;const purpose=purposeFor(classes);
 if(ck&&ck.purpose){const miss=purpose.filter(p=>!ck.purpose.includes(p));if(miss.length)out.blockers.push('checklist purpose omits evidence-derived requirements: '+miss.join(', '))}
 const AUTO={progression_spikes:['strategy','investment'],ability_upgrades:['strategy'],thresholds_sales:['investment'],alternative_comparison:['strategy','decision'],synergies:['interaction','team','context'],temporary_purchases:['path','investment'],situational_swaps:['situational'],activations_rotations:['interaction','conditional']};
 const MEASURED_KEYS=['damage','sustain','survivability','farming','activations_rotations','synergies','temporary_purchases','utility_contribution'];
 const evOf=key=>{const listed=((ck&&ck.items&&ck.items[key]&&ck.items[key].evidence)||[]).map(e=>e.path);
  const auto=[...(AUTO[key]?E.forBuild(id).filter(e=>AUTO[key].includes(e.kind)):[]),...(MEASURED_KEYS.includes(key)?E.buildContext(id):[])].map(e=>e.path);
  return [...new Set([...listed,...auto])].map(p=>({e:{path:p},idx:E.index().find(x=>x.path===p)||(fs.existsSync(path.join(SP,p))?{path:p,build:null,kind:'unindexed',scope:null,valid:null,measured:false,h:{}}:null)})).map(x=>({...x,adm:x.idx?E.admissible(x.idx,id):{ok:false,why:['file does not exist: '+x.e.path]}}))};
 const res=(key,status,why,ev)=>out.items[key]={status,why,evidence:(ev||[]).map(x=>({path:x.e.path,kind:x.idx&&x.idx.kind,admissible:x.adm.ok,problems:x.adm.why}))};
 const needKinds=(key,kinds)=>{const ev=evOf(key);const good=ev.filter(x=>x.idx&&kinds.includes(x.idx.kind)&&x.adm.ok);const bad=ev.filter(x=>!good.includes(x));return {ev,good,bad}};
 const seq=coreSeq(c);
 // --- evidence-gated items
 {const {ev,good,bad}=needKinds('progression_spikes',['strategy']);const inv=needKinds('progression_spikes',['investment']);let st='missing',why=[];
  const s=good.find(x=>x.idx.h['CONCLUSION']&&/^CHOSEN:/.test(x.idx.h['CONCLUSION'])&&(x.idx.h['CHOSEN-PATH']||'').split(' > ').map(z=>z.trim()).join('>')===seq.join('>'));
  if(!s)why.push('no admissible `strategy` file with CONCLUSION: CHOSEN whose CHOSEN-PATH equals this build\'s core purchase sequence (strong final items do not prove a progression)');
  if(!inv.good.length)why.push('no admissible `investment` file');
  if(s&&inv.good.length){st='pass'}else if(ev.length)st='fail';bad.forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')));res('progression_spikes',st,why,ev)}
 {const {ev,good,bad}=needKinds('ability_upgrades',['strategy']);const s=good.find(x=>x.idx.h['CHOSEN-ORDER']&&x.idx.h['CHOSEN-ORDER'].trim()===(c.order||[]).join(''));const why=[];
  if(!s)why.push('no admissible `strategy` file with CHOSEN-ORDER == '+(c.order||[]).join(''));bad.forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')));res('ability_upgrades',s?'pass':ev.length?'fail':'missing',why,ev)}
 {const inv=needKinds('thresholds_sales',['investment']);const rtc=RT.run(rec).checks;const sale=rtc.find(x=>x.check==='sale_instructions_reference_real_items');const why=[];
  if(!inv.good.length)why.push('no admissible `investment` file (thresholds gained/lost, sold items)');if(!sale.ok)why.push('sale instruction check: '+sale.detail);inv.bad.forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')));res('thresholds_sales',inv.good.length&&sale.ok?'pass':inv.ev.length||!sale.ok?'fail':'missing',why,inv.ev)}
 {const n=needKinds('alternative_comparison',['strategy','decision']);const why=[];if(!n.good.length)why.push('no admissible `strategy`/`decision` file comparing alternatives at comparable investment');n.bad.forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')));res('alternative_comparison',n.good.length?'pass':n.ev.length?'fail':'missing',why,n.ev)}
 {const L_=(ck&&ck.limitations)||[];res('limitations_listed',L_.length&&L_.every(x=>x&&x.length>15)?'pass':'missing',L_.length?[]:['no limitations listed (an unproven interaction must be stated, not omitted)'],[])}
 {const f=lint.issues.filter(i=>i.sev==='fail'&&['name','class','tags'].includes(i.area));res('naming_coherence',f.length?'fail':'pass',f.map(i=>i.code+': '+i.msg).concat(['evidence level: '+lint.level+(lint.level==='composition-only'?' (no behavioural/sandbox evidence: role claims are checked for contradiction, not confirmed)':'')]),[])}
 {const f=lint.issues.filter(i=>i.area==='description'&&(i.sev==='fail'||i.code==='LABEL_ONLY'||i.code==='EMPTY'));res('description_basis',f.length?'fail':'pass',f.map(i=>i.code+': '+i.msg),[])}
 {const f=lint.issues.filter(i=>i.area==='captions');res('captions_complete',f.length?'fail':'pass',f.map(i=>i.code+': '+i.msg),[])}
 {const t=lint.issues.filter(i=>i.area==='tags'&&(i.sev==='fail'||i.code==='TAGS_HERO_DEFAULT'));const rtc=RT.run(rec).checks.find(x=>x.check==='tags');res('tags_verified',!t.length&&rtc.ok?'pass':'fail',t.map(i=>i.code+': '+i.msg).concat(rtc.ok?[]:['round-trip: '+rtc.detail]),[])}
 {const rtc=RT.run(rec).checks.filter(x=>!x.ok);res('export_roundtrip',rtc.length?'fail':'pass',rtc.map(x=>x.check+': '+x.detail),[])}
 // --- purpose items
 const meas=id2=>E.buildContext(id2).filter(e=>E.admissible(e,id2).ok);
 for(const key of PURPOSE_ALL){const req=purpose.includes(key);const ev=evOf(key);const mgood=ev.filter(x=>x.idx&&x.idx.measured&&x.adm.ok);const why=[];let st='missing';
  const claim=ck&&ck.items&&ck.items[key];
  const kindsFor={damage:null,sustain:null,survivability:null,farming:null,activations_rotations:null,utility_contribution:null,synergies:['interaction','team','context'],temporary_purchases:['path','investment'],situational_swaps:['situational']}[key];
  if(kindsFor){const k=needKinds(key,kindsFor);k.bad.forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')));
   if(key==='synergies'){st=k.good.length&&mgood.length?'pass':k.good.length?'limited':'missing';if(st!=='pass')why.push('needs interaction/team evidence AND >=1 measured build-context result of the full set'+(k.good.length?' (only calculated evidence present)':''))}
   else if(key==='temporary_purchases'){st=k.good.length&&mgood.length?'pass':k.good.length?'limited':'missing';if(st!=='pass')why.push('while-owned value is calculated only; no measured while-owned result')}
   else {st=k.good.length?'pass':'missing';if(st!=='pass')why.push('no admissible `situational` file')}}
  else{const need=key==='damage'||key==='survivability'?2:1;if(mgood.length>=need)st='pass';else{st=ev.length||claim?'limited':'missing';why.push(`needs >= ${need} admissible MEASURED build-context result(s) (have ${mgood.length}); calculated/modelled files and isolated tests give at most "limited"; one controlled test is not sufficient`);ev.filter(x=>!x.adm.ok).forEach(x=>why.push(x.e.path+': '+x.adm.why.join('; ')))}}
  if(st!=='pass'&&claim&&claim.limitation)why.push('declared limitation: '+claim.limitation);
  out.items[key]={status:st,required:req,why,evidence:ev.map(x=>({path:x.e.path,admissible:x.adm.ok,problems:x.adm.why}))}}
 for(const k of ALWAYS)out.items[k].required=true;
 const missing=[];for(const [k,v] of Object.entries(out.items)){if(v.required&&v.status!=='pass')missing.push(k+' ['+v.status+']')}
 out.classes=classes;out.purpose=purpose;out.evidence_level=lint.level;out.missing=missing;
 out.validated=!out.blockers.length&&!missing.length;
 out.notes.push('gate.js currently rejects kind `measured` evidence until the Sandbox results path is validated (audit/sandbox.md gap 1): measured-dependent items cannot be admitted through the gate yet');
 out.notes.push('evidence admissibility uses the evidence owners\' own BODY-SHA / INPUT-SHA verifiers (abtimeline.py); evidence made before the latest data/tool change is stale and must be regenerated');
 return out}
function scaffold(id){const rec=R.liveRecord(id);const ev=E.forBuild(id);const byKind=k=>ev.filter(e=>k.includes(e.kind)).map(e=>({path:e.path,note:'attached by scaffold; unverified'}));
 const items={progression_spikes:{status:'na',evidence:byKind(['strategy','investment'])},ability_upgrades:{status:'na',evidence:byKind(['strategy'])},thresholds_sales:{status:'na',evidence:byKind(['investment'])},alternative_comparison:{status:'na',evidence:byKind(['strategy','decision'])},synergies:{status:'na',evidence:byKind(['interaction','team','context'])},temporary_purchases:{status:'na',evidence:byKind(['path','investment'])},situational_swaps:{status:'na',evidence:byKind(['situational'])},activations_rotations:{status:'na',evidence:byKind(['interaction','conditional'])}};
 const f={format:'build-validation-checklist/1',build:id,revision_ref:rec.revision.ref,content_sha:rec.revision.content_sha,purpose:[],items,limitations:[],reviewer:null,date:new Date().toISOString()};
 const p=path.join(PUB,'checklists',id+'.json');fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(f,null,1));return p}
module.exports={check,scaffold,ALWAYS,PURPOSE_ALL,purposeFor};
if(require.main===module){const a=process.argv.slice(2);const [cmd,id]=a;if(!cmd||!id){console.log('usage: prepublish.js check|scaffold <id> [--build-file f] [--checklist f] [--json]');process.exit(2)}
 if(cmd==='scaffold'){console.log(scaffold(id));process.exit(0)}
 const o={};if(a.includes('--build-file'))o.buildFile=a[a.indexOf('--build-file')+1];if(a.includes('--checklist'))o.checklist=a[a.indexOf('--checklist')+1];
 const r=check(id,o);if(a.includes('--json'))console.log(JSON.stringify(r,null,1));else{console.log(`PREPUBLISH ${r.build} ${r.revision} -> ${r.validated?'VALIDATED':'NOT VALIDATED'} (evidence level: ${r.evidence_level}; classes: ${r.classes.join(' + ')})`);
  r.blockers.forEach(b=>console.log('BLOCKER',b));for(const [k,v] of Object.entries(r.items))console.log(`  ${(v.required?'*':' ')} ${k.padEnd(24)} ${v.status.toUpperCase().padEnd(8)} ${(v.why||[]).slice(0,2).join(' | ').slice(0,200)}`);r.notes.forEach(n=>console.log('NOTE',n))}
 process.exit(r.validated?0:1)}

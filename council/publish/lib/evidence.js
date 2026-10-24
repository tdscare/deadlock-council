// Evidence index: reads the Council's existing evidence/result files READ-ONLY, parses their header lines, checks integrity with the owners' own verifiers.
const C=require('./common');const cp=require('child_process');const {fs,path,SP}=C;
const ABT='council/tools/abtimeline.py';
let _ish;function inputSha(){if(_ish!==undefined)return _ish;try{_ish=cp.execFileSync('python3',['-I',ABT,'--input-sha'],{cwd:SP}).toString().trim()}catch(e){_ish=null}return _ish}
const _ver={};function bodyOk(rel){if(rel in _ver)return _ver[rel];const r=cp.spawnSync('python3',['-I',ABT,'--verify-strategy',rel],{cwd:SP,encoding:'utf8'});return _ver[rel]=r.status===0}
function walk(d,o=[]){if(!fs.existsSync(d))return o;for(const f of fs.readdirSync(d)){const p=path.join(d,f);const st=fs.statSync(p);if(st.isDirectory()){if(!/\/(effects|hypotheses|validated|alts|w|chunk)\b/.test(p))walk(p,o)}else if(/\.(txt|md|json)$/.test(f))o.push(p)}return o}
function head(file){const t=fs.readFileSync(file,'utf8').slice(0,6000);const h={};for(const m of t.matchAll(/^\s*(?:>\s*)?(SCOPE|KIND|VALID|BUILD|BODY-SHA|INPUT-SHA|GENERATED|CONCLUSION|VERDICT|GRADE|CHOSEN-PATH|CHOSEN-ORDER|ITEM|CHECKPOINT):\s*(.*)$/gmi)){const k=m[1].toUpperCase();if(!(k in h))h[k]=m[2].trim()}return {h,t}}
let IDX=null;
function index(){if(IDX)return IDX;const ids=C.loadData().B.map(b=>b.id).sort((a,b)=>b.length-a.length);const out=[];
 for(const root of ['council/evidence','council/sandbox/results']){for(const f of walk(path.join(SP,root))){const rel=path.relative(SP,f);if(/\.json$/.test(f)&&!/results\//.test(rel))continue;
  let hd;try{hd=head(f)}catch(e){continue}const h=hd.h;let build=h.BUILD;if(!build){const base=path.basename(f);build=ids.find(i=>base.startsWith(i+'_')||base.startsWith(i+'.'))||null}
  if(!build&&!h.KIND)continue;
  const inRes=/sandbox\/results\//.test(rel);const grade=/MEASURED/.test((h.GRADE||'')+(h.VALID||''))||inRes&&/^yes/i.test(h.VALID||'');
  out.push({path:rel,build,kind:(h.KIND||(inRes?'sandbox-result':path.basename(path.dirname(rel)))).toLowerCase(),scope:(h.SCOPE||'').toLowerCase()||null,valid:h.VALID||null,measured:!!grade&&inRes,h})}}
 return IDX=out}
// is a file usable as evidence for `id` at the CURRENT data state?
function admissible(e,id){const why=[];if(e.build&&e.build!==id)why.push('BUILD '+e.build+' != '+id);
 if(e.valid&&/^no/i.test(e.valid))why.push('VALID: no');
 if(e.scope!=='build-context')why.push(e.scope==='isolated'?'SCOPE isolated (mechanism datum only, not a build verdict)':'no SCOPE: build-context header');
 if(e.h['BODY-SHA']&&!bodyOk(e.path))why.push('BODY-SHA mismatch (edited after generation)');
 const ish=inputSha();if(e.h['INPUT-SHA']&&ish&&e.h['INPUT-SHA']!==ish)why.push('stale: INPUT-SHA differs from current data/tool state');
 return {ok:!why.length,why}}
function forBuild(id){return index().filter(e=>e.build===id)}
function buildContext(id){return forBuild(id).filter(e=>e.scope==='build-context'&&e.measured&&!/^no/i.test(e.valid||''))}
function queueFor(id){let q;try{q=JSON.parse(fs.readFileSync(path.join(SP,'council/sandbox/queue.json'),'utf8')).tasks}catch(e){return []}return q.filter(t=>t.build===id)}
function gateReports(id){const d=path.join(SP,'council/history');if(!fs.existsSync(d))return [];return fs.readdirSync(d).filter(f=>/\.report\.json$/.test(f)).map(f=>{try{return JSON.parse(fs.readFileSync(path.join(d,f),'utf8'))}catch(e){return null}}).filter(r=>r&&r.id===id)}
module.exports={index,forBuild,buildContext,queueFor,gateReports,admissible,inputSha,head};

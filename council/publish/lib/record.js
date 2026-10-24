// Build record = the ONE object both the website and the game export are generated from.
//   content : exactly the data.js entry (minus `changes`): id,hero,tag,name,desc,hk,abil,order,rows[,tg,lim,basis]
//   revision: {n, ref:'<id>@r<n>#<sha8>', content_sha}   (n is OUR revision counter; CMsgHeroBuild.version is server-owned and not used)
//   approval: only ever filled by reconcile() from gate artefacts (approvals/<proposal>.ok sha == proposal sha AND history/LOG.jsonl entry whose post-sha == sha(data.js) AND data.js entry content == record content)
// The gate is the only writer of data.js; this module never writes it.
const C=require('./common');const {fs,path,SP,PUB}=C;
const strip=b=>{const o=JSON.parse(JSON.stringify(b));delete o.changes;return o};
const contentSha=content=>C.sha(C.canon(strip(content)));
const refOf=(id,n,sha)=>`${id}@r${n}#${sha.slice(0,8)}`;
const dir=id=>path.join(PUB,'records',id);
function readJ(f,d=null){try{return JSON.parse(fs.readFileSync(f,'utf8'))}catch(e){return d}}
function liveEntry(id,dataFile='data.js'){const {B}=C.loadData(dataFile);return B.find(b=>b.id===id)||null}
function history(){const f=path.join(SP,'council/history/LOG.jsonl');if(!fs.existsSync(f))return[];return fs.readFileSync(f,'utf8').split('\n').filter(Boolean).map(l=>{try{return JSON.parse(l)}catch(e){return null}}).filter(Boolean)}
// gate-derived approval facts for a build id (does NOT trust anything we wrote ourselves)
function gateApproval(id,liveContentSha){
 const dataSha=C.shaFile(path.join(SP,'data.js'));const log=history().filter(e=>e.id===id);
 const last=log[log.length-1];
 if(!last)return {approved:false,reason:'no gate-applied revision exists in council/history/LOG.jsonl (legacy/baseline entry that never went through the gate)',log:0};
 const okf=path.join(SP,'council/approvals',last.proposal+'.ok'),pf=path.join(SP,'council/proposals',last.proposal+'.json');
 const why=[];if(!fs.existsSync(okf))why.push('approval file missing');else if(!fs.existsSync(pf))why.push('proposal file missing');else if(fs.readFileSync(okf,'utf8').trim()!==C.shaFile(pf))why.push('approval sha != proposal sha');
 if(last.post!==dataSha)why.push('data.js changed after the last gate apply (post-sha mismatch)');
 return {approved:!why.length,reason:why.join('; '),proposal:last.proposal,proposal_sha:fs.existsSync(pf)?C.shaFile(pf):null,approval_file:'council/approvals/'+last.proposal+'.ok',gate_post_sha:last.post,gate_when:last.when,gate_line:last.line,log:log.length}}
function nextRevision(id){const d=path.join(dir(id),'revisions');if(!fs.existsSync(d))return 1;return Math.max(0,...fs.readdirSync(d).map(f=>+(f.match(/^r(\d+)\.json$/)||[0,0])[1]))+1}
// create a PENDING record from content (never touches approved slot or data.js)
function createPending(id,content,opts={}){
 const n=nextRevision(id),sha=contentSha(content);
 const rec={schema:1,kind:'build-record',id,slot:'pending',content:strip(content),revision:{n,content_sha:sha,ref:refOf(id,n,sha)},source:opts.source||'unspecified',parent:opts.parent||null,
  created:opts.created||new Date().toISOString(),approval:null,evidence:opts.evidence||[],notes:opts.notes||[]};
 const d=path.join(dir(id),'revisions');fs.mkdirSync(d,{recursive:true});fs.writeFileSync(path.join(d,'r'+n+'.json'),JSON.stringify(rec,null,1));return rec}
// the record of what data.js holds RIGHT NOW (the only thing the website can show)
function liveRecord(id,dataFile='data.js'){
 const e=liveEntry(id,dataFile);if(!e)return null;const sha=contentSha(e);
 const revs=fs.existsSync(path.join(dir(id),'revisions'))?fs.readdirSync(path.join(dir(id),'revisions')):[];
 let n=0;for(const f of revs){const r=readJ(path.join(dir(id),'revisions',f));if(r&&r.revision.content_sha===sha)n=Math.max(n,r.revision.n)}
 const ga=gateApproval(id,sha);
 return {schema:1,kind:'build-record',id,slot:ga.approved?'approved':'baseline-unapproved',content:strip(e),revision:{n:n||0,content_sha:sha,ref:refOf(id,n||0,sha)},source:'data.js@'+C.shaFile(path.join(SP,dataFile)).slice(0,12),approval:ga.approved?ga:null,approval_check:ga}}
module.exports={strip,contentSha,refOf,createPending,liveRecord,gateApproval,nextRevision,readJ,dir};

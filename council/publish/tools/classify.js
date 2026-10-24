#!/usr/bin/env node
// Read-only classifier + name/description/tag/caption lint.   node classify.js <id>|all [--json] [--out dir]
const C=require('../lib/common');const L=require('../lib/lint');const I=require('../lib/identity');const R=require('../lib/record');const {fs,path,PUB}=C;
const ctx=C.loadGame();ctx.data=C.loadData();
const a=process.argv.slice(2);const target=a[0]||'all';const ids=target==='all'?ctx.data.B.map(b=>b.id):[target];
const hasSandbox=id=>{try{return require('../lib/evidence').buildContext(id).length>0}catch(e){return false}};
const rows=[];
for(const id of ids){const b=ctx.data.B.find(x=>x.id===id);const r=L.lintBuild(b,ctx,hasSandbox(id));rows.push({id,name:b.name,desc:b.desc,classes:r.res.classes,share:Object.fromEntries(Object.entries(r.res.share).map(([k,v])=>[k,+v.toFixed(2)])),why:r.res.why,verdict:r.verdict,level:r.level,issues:r.issues})}
const tally=rows.reduce((o,r)=>(o[r.verdict]=(o[r.verdict]||0)+1,o),{});
if(a.includes('--json')){console.log(JSON.stringify(rows,null,1))}else if(target!=='all'){for(const r of rows){console.log(`${r.id} | ${r.name} | "${r.desc}" | ${r.verdict} (${r.level})\n  class: ${r.classes.join(' + ')}\n  evidence: ${r.why.join(' ; ')}`);r.issues.forEach(i=>console.log(`  [${i.sev}] ${i.area}/${i.code}: ${i.msg}`))}}
else{console.log('verdicts',JSON.stringify(tally));const by={};rows.forEach(r=>r.issues.forEach(i=>by[i.code]=(by[i.code]||0)+1));console.log('issue counts',JSON.stringify(by))}
if(target==='all'){const od=a.includes('--out')?a[a.indexOf('--out')+1]:path.join(PUB,'out');fs.mkdirSync(od,{recursive:true});fs.writeFileSync(path.join(od,'classification_all.json'),JSON.stringify(rows,null,1));}

const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const B=new Function(fs.readFileSync(SP+'data.js','utf8')+';return B')();
const ids=fs.readFileSync(SP+'council/evidence/cost/chunk0.txt','utf8').split(/\s+/).filter(Boolean);
for(const id of ids){const b=B.find(x=>x.id===id);if(!b){console.log('MISSING',id);continue}
 fs.writeFileSync(SP+'council/evidence/cost/w/'+id+'.json',JSON.stringify(b,null,1));
 console.log('\n=== '+id+' | '+b.name+' | desc:'+b.desc+' | order '+b.order.join(''));
 for(const r of b.rows)for(const [t,d,o,items] of r)console.log(` [${t}] ${o?'(opt) ':''}${d?'"'+d+'" ':''}: `+items.map(i=>i[0]+(i[2]?'*'+i[2]:'')+(i[1]?' {'+i[1]+'}':'')).join(' | '));}

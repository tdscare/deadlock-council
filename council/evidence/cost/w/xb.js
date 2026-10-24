// cross-build item timing: for each item in the chunk's builds, buy-souls vs same item in all other data.js builds
const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const B=new Function(fs.readFileSync(SP+'data.js','utf8')+';return B')();const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));
const C={1:800,2:1600,3:3200,4:6400};
const ids=fs.readFileSync(SP+'council/evidence/cost/chunk0.txt','utf8').split(/\s+/).filter(Boolean);
const pos={};// item -> [{id,souls}]
for(const b of B){let owned=[],souls=0;for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
 for(const [n,note] of items){const g=G[n];if(!g)continue;const have=g.components.filter(c=>owned.includes(c));souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);
  const m=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m){const i=owned.indexOf(m[1]);if(i>=0)owned.splice(i,1)}
  (pos[n]=pos[n]||[]).push({id:b.id,souls,order:owned.length})}}}
const med=a=>{a=a.slice().sort((x,y)=>x-y);return a[Math.floor(a.length/2)]};
for(const id of ids){const b=B.find(x=>x.id===id);console.log('== '+id);
 for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
  for(const [n] of items){const mine=pos[n].find(p=>p.id===id).souls;const oth=pos[n].filter(p=>p.id!==id);if(oth.length<3)continue;
   const m=med(oth.map(p=>p.souls));const ratio=mine/m;const t2=G[n].tier;
   if(ratio>1.6||ratio<0.55){const e=oth.slice().sort((a,c)=>a.souls-c.souls);console.log(`  ${n.padEnd(22)} T${t2} mine ${mine} | others n=${oth.length} median ${m} min ${e[0].souls}(${e[0].id}) max ${e[e.length-1].souls}(${e[e.length-1].id}) ratio ${ratio.toFixed(2)}`)}}}}

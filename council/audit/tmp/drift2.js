const fs=require('fs');process.chdir(__dirname+'/../../..');
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const CC={Tech:'s',WeaponMod:'w',Armor:'v'};const C={1:800,2:1600,3:3200,4:6400};
const load=f=>new Function(fs.readFileSync(f,'utf8')+';return B')();
function prof(b){let owned=[],souls=0,sp={},at={};const seq=[],optset=[];
 for(const r of b.rows)for(const [t,d,o,items] of r){const core=/^(Early|Mid|Late)/.test(t);
  for(const [n,note] of items){if(!core){optset.push(t+':'+n);continue}const g=G[n];const have=g.components.filter(c=>owned.includes(c));
   souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);at[n]=souls;
   const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
   const inv={w:0,s:0,v:0};owned.forEach(x=>inv[CC[G[x].slot]]+=C[G[x].tier]);
   for(const k in inv)if(inv[k]>=4800&&!sp[k])sp[k]=souls;seq.push(n)}}
 return {seq,sp,at,optset,order:b.order.join('')}}
const cur=load('data.js');
for(const base of process.argv.slice(2)){console.log('\n#### vs',base);const old=load(base);
 for(const b of cur){const o=old.find(x=>x.id===b.id);if(!o){console.log(b.id,'NEW (absent in base)');continue}
  const p=prof(b),q=prof(o);const nl=(b.changes||[]).length-(o.changes||[]).length;
  const newtxt=(b.changes||[]).slice((o.changes||[]).length).join(' ');
  const diffs=[];
  if(p.seq.join()!==q.seq.join()){const moved=p.seq.filter(x=>q.seq.includes(x)&&Math.abs(p.at[x]-q.at[x])>=1600&&true);diffs.push('core seq changed; +['+p.seq.filter(x=>!q.seq.includes(x))+'] -['+q.seq.filter(x=>!p.seq.includes(x))+'] bigshift['+moved.map(x=>x+' '+q.at[x]+'>'+p.at[x])+']')}
  if(JSON.stringify(p.sp)!==JSON.stringify(q.sp))diffs.push('spikes '+JSON.stringify(q.sp)+'->'+JSON.stringify(p.sp));
  if(p.order!==q.order)diffs.push('abil order '+q.order+'->'+p.order);
  if(p.optset.join()!==q.optset.join())diffs.push('optional boxes changed');
  if(!diffs.length)continue;
  // does new text name each moved/added/removed item?
  const names=[...p.seq.filter(x=>!q.seq.includes(x)),...q.seq.filter(x=>!p.seq.includes(x))];
  const unmentioned=names.filter(n=>!newtxt.includes(n));
  console.log(b.id,'| newChangeLines',nl,nl<=0?'NONE':'','|',diffs.join(' ; '),unmentioned.length?'| ITEMS NOT NAMED IN NEW CHANGES: '+unmentioned:'')}}

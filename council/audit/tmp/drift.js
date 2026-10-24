const fs=require('fs');process.chdir(__dirname+'/../../..');
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const CC={Tech:'s',WeaponMod:'w',Armor:'v'};const C={1:800,2:1600,3:3200,4:6400};
const load=f=>{try{return new Function(fs.readFileSync(f,'utf8')+';return B')()}catch(e){return null}};
function prof(b){let owned=[],souls=0,sp={};const seq=[];
 for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
  for(const [n,note] of items){const g=G[n];if(!g){seq.push(n);continue}const have=g.components.filter(c=>owned.includes(c));
   souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);
   const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
   const inv={w:0,s:0,v:0};owned.forEach(x=>inv[CC[G[x].slot]]+=C[G[x].tier]);
   for(const k in inv)if(inv[k]>=4800&&!sp[k])sp[k]=souls;seq.push(n)}}
 return {seq,sp,total:souls}}
const cur=load('data.js');const files=fs.readdirSync('.').filter(f=>/^data.*\.js(\.bak.*)?$/.test(f)&&f!=='data.js').map(f=>[f,fs.statSync(f).mtimeMs]).sort((a,b)=>a[1]-b[1]);
const out=[];
for(const b of cur){const p=prof(b);const lastChange=(b.changes||[]).slice(-1)[0]||'';
 // find the earliest backup where the profile differs and note whether any later changes line mentions
 let prev=null;const hist=[];
 for(const [f] of files){const B=load(f);if(!B)continue;const o=B.find(x=>x.id===b.id);if(!o)continue;const q=prof(o);
  const key=q.seq.join('|')+JSON.stringify(q.sp);if(prev!==key){hist.push({f,q,nchg:(o.changes||[]).length});prev=key}}
 const curKey=p.seq.join('|')+JSON.stringify(p.sp);
 if(prev!==curKey)hist.push({f:'data.js',q:p,nchg:(b.changes||[]).length});
 out.push({id:b.id,hist})}
for(const o of out){const h=o.hist;for(let i=1;i<h.length;i++){const a=h[i-1],c=h[i];
  const moved=a.q.seq.join()!==c.q.seq.join();const spk=JSON.stringify(a.q.sp)!==JSON.stringify(c.q.sp);
  const nochg=c.nchg<=a.nchg;
  const add=c.q.seq.filter(x=>!a.q.seq.includes(x)),rem=a.q.seq.filter(x=>!c.q.seq.includes(x));
  console.log([o.id,a.f+'->'+c.f,'chgLines '+a.nchg+'->'+c.nchg,nochg?'NO_NEW_CHANGES_LINE':'',moved?'items':'',spk?'spikes '+JSON.stringify(a.q.sp)+'->'+JSON.stringify(c.q.sp):'','+['+add+'] -['+rem+']'].join(' | '))}}

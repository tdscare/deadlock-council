// node fix.js <id> "mv:Item>after:Other" "swap:A=B" "add:Item>after:Other" "del:Item" ... ; prints END summary + spike positions + per-item souls
const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));const C={1:800,2:1600,3:3200,4:6400};
const CCm={Tech:'s',WeaponMod:'w',Armor:'v'};const cc=n=>CCm[G[n].slot];const col={w:'gun',s:'spirit',v:'health'};
const [id,...ops]=process.argv.slice(2);const b=JSON.parse(fs.readFileSync(SP+'council/evidence/cost/w/'+id+'.json'));
let list=[];for(const r of b.rows)for(const [t,d,o,items] of r)if(/^(Early|Mid|Late)/.test(t))items.forEach(i=>list.push({n:i[0],note:i[1]||''}));
for(const op of ops){let m;
 if(m=op.match(/^swap:(.+)=(.+)$/)){const x=list.find(i=>i.n===m[1]);x.n=m[2];x.note=''}
 else if(m=op.match(/^del:(.+)$/)){list=list.filter(i=>i.n!==m[1])}
 else if(m=op.match(/^(mv|add):(.+)>(after|before):(.+)$/)){let it;if(m[1]==='mv'){const k=list.findIndex(i=>i.n===m[2]);it=list.splice(k,1)[0]}else it={n:m[2],note:''};
  const k=list.findIndex(i=>i.n===m[4]);list.splice(m[3]==='after'?k+1:k,0,it)}
 else if(m=op.match(/^nonote:(.+)$/)){list.find(i=>i.n===m[1]).note=''}
 else if(m=op.match(/^first:(.+)$/)){const k=list.findIndex(i=>i.n===m[1]);const it=list.splice(k,1)[0];list.unshift(it)}}
let owned=[],souls=0,spikes={};const lines=[];
const inv=()=>{const r={w:0,s:0,v:0};owned.forEach(n=>r[cc(n)]+=C[G[n].tier]);return r};
for(const {n,note} of list){const g=G[n];const have=g.components.filter(c=>owned.includes(c));const cost=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);
 owned=owned.filter(x=>!have.includes(x));owned.push(n);souls+=cost;const m=note.match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m){const i=owned.indexOf(m[1]);if(i>=0)owned.splice(i,1)}
 const iv=inv();for(const k of ['w','s','v'])if(iv[k]>=4800&&!spikes[k])spikes[k]=souls;lines.push(`${String(souls).padStart(6)} ${n.padEnd(22)} paid ${String(cost).padStart(4)} g${iv.w} s${iv.s} v${iv.v}`)}
const iv=inv();if(process.env.V)console.log(lines.join('\n'));
console.log(`${id} [${ops.join(' ; ')}] END ${souls} | gun ${iv.w} spirit ${iv.s} health ${iv.v} | slots ${owned.length} | 4.8k: `+['w','s','v'].map(k=>col[k]+'@'+(spikes[k]||'never')).join(' '));

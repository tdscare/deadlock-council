// node cost.js <id> [X=Y ...]  : walk core with swaps (X replaced by Y in place), print per-item cost table + spikes
const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const cc=n=>CC[G[n].slot];
const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));
const C={1:800,2:1600,3:3200,4:6400};const CC={Tech:'s',WeaponMod:'w',Armor:'v'};const col={w:'gun',s:'spirit',v:'health'};
const [id,...sw]=process.argv.slice(2);const swaps={};sw.forEach(s=>{const [a,b]=s.split('=');swaps[a]=b});
const b=JSON.parse(fs.readFileSync(SP+'council/evidence/cost/w/'+id+'.json'));
let owned=[],souls=0,spikes={},rows=[];
const inv=()=>{const r={w:0,s:0,v:0};owned.forEach(n=>r[cc(n)]+=C[G[n].tier]);return r};
const keyst=g=>Object.entries(g.stats||{}).filter(([k,v])=>/^[\d.+-]+%?$/.test(String(v))&&!/Duration|Cooldown|Radius|Limit|Range|Cost|Charge|Delay|Time/i.test(k)).slice(0,5).map(([k,v])=>k.replace(/^Bonus/,'')+'='+v).join(' ');
for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
 for(let [n,note,imb] of items){if(swaps[n]){n=swaps[n];note=''}const g=G[n];if(!g){rows.push('?? '+n);continue}
  const have=g.components.filter(c=>owned.includes(c));const cost=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);
  owned=owned.filter(x=>!have.includes(x));owned.push(n);souls+=cost;
  const m=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m){const i=owned.indexOf(m[1]);if(i>=0)owned.splice(i,1)}
  const iv=inv();for(const k of ['w','s','v'])if(iv[k]>=4800&&!spikes[k])spikes[k]=souls;
  rows.push(`${String(souls).padStart(6)} ${n.padEnd(22)} ${cc(n)}${g.tier} paid ${String(cost).padStart(4)} | g${iv.w} s${iv.s} v${iv.v} | ${keyst(g)}`)}}
console.log('== '+id+(sw.length?' SWAP '+sw.join(','):'')+' order '+b.order.join(''));console.log(rows.join('\n'));
const iv=inv();console.log(`END ${souls} souls | gun ${iv.w} spirit ${iv.s} health ${iv.v} | 4.8k spikes: `+Object.entries(spikes).map(([k,v])=>col[k]+'@'+v).join(' ')+' | missing: '+['w','s','v'].filter(k=>!spikes[k]).map(k=>col[k]).join(','));

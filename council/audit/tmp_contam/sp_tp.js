// usage: node a7/sp.js <build json file> [orderString]  — per core purchase: souls, level, spirit power (levels + items + spirit-invest bonus), ability tiers
const TP=parseFloat(process.env.TP||'1.1');
process.chdir('/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad');const fs=require('fs');
const b=JSON.parse(fs.readFileSync(process.argv[2]));if(process.argv[3])b.order=process.argv[3].split('').map(Number);
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const L=JSON.parse(fs.readFileSync('a7/levels.json'));
const C={1:800,2:1600,3:3200,4:6400};const CC={Tech:'s',WeaponMod:'w',Armor:'v'};
const num=v=>parseFloat(String(v));
const itemSP=n=>{const st=G[n].stats||{};let t=0;for(const k of ['TechPower','BonusTechPower','SpiritPower'])if(st[k]!=null&&!/x /.test(st[k]))t+=num(st[k]);return t};
function state(souls){let lvl=0,unl=0,pts=0,std=0;for(const x of L.levels)if(souls>=x.gold){lvl=x.l;unl+=x.unl;pts+=x.pts;if(x.std)std++;}
 const tier=[0,-1,-1,-1,-1];let u=unl,p=pts;
 for(const a of b.order){if(tier[a]<0){if(u<1)break;u--;tier[a]=0}else{const c=[1,2,5][tier[a]];if(c==null||p<c)break;p-=c;tier[a]++}}
 return {lvl,lvlSP:+(std*TP).toFixed(1),tier:tier.slice(1)}}
let owned=[],souls=0;const out=[];
for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
 for(const [n,note,imb] of items){const g=G[n];if(!g)continue;const have=g.components.filter(c=>owned.includes(c));
  souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);
  const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
  const inv=owned.filter(x=>CC[G[x].slot]=='s').reduce((a,x)=>a+C[G[x].tier],0);
  let bonus=0;for(const [th,bo] of L.tech)if(inv>=th)bonus=bo;
  const isp=owned.reduce((a,x)=>a+itemSP(x),0);const s=state(souls);
  out.push(`${n.padEnd(24)} souls ${String(souls).padStart(5)} lvl ${String(s.lvl).padStart(2)} spiritInv ${String(inv).padStart(5)} SP ${(s.lvlSP+isp+bonus).toFixed(1).padStart(5)} (lvl ${s.lvlSP} items ${isp} invest ${bonus}) tiers[${s.tier.join(',')}]${imb?' imbue '+imb:''}`)}}
console.log(b.abil.map((a,i)=>(i+1)+'='+a).join('  '));console.log('order',b.order.join(''));console.log(out.join('\n'));

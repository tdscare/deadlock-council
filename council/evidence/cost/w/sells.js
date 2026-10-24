// node sells.js <id> : end-of-core invest per colour, then effect of every "Sell X" in counter/rich/slot boxes
const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));
const C={1:800,2:1600,3:3200,4:6400};const CCm={Tech:'s',WeaponMod:'w',Armor:'v'};const cc=n=>CCm[G[n].slot];const col={w:'gun',s:'spirit',v:'health'};
const id=process.argv[2];const b=JSON.parse(fs.readFileSync(SP+'council/evidence/cost/w/'+id+'.json'));
let owned=[];
for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
 for(const [n,note] of items){const g=G[n];const have=g.components.filter(c=>owned.includes(c));owned=owned.filter(x=>!have.includes(x));owned.push(n);
  const m=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m){const i=owned.indexOf(m[1]);if(i>=0)owned.splice(i,1)}}}
const inv=ow=>{const r={w:0,s:0,v:0};ow.forEach(n=>r[cc(n)]+=C[G[n].tier]);return r};
const base=inv(owned);console.log('== '+id+' end-of-core invest: gun '+base.w+' spirit '+base.s+' health '+base.v);
const TH=[4800,6400,8000,16000];const cross=(a,b2)=>TH.filter(t=>a>=t&&b2<t);
for(const r of b.rows)for(const [t,d,o,items] of r){if(/^(Early|Mid|Late)/.test(t)||!o)continue;
 const dm=(d||'').match(/Sell ([A-Z][^.]*?) for it/);
 for(const [n,note] of items){if(!G[n]){continue}
  const sells=[];if(dm&&/Counters/.test(t))sells.push(dm[1]);
  const m=[...(note||'').matchAll(/Sell ([A-Z][^.,]*?) for this(?:, or ([A-Z][^.,]*?) if)?/g)];m.forEach(x=>{sells.push(x[1])});
  if(/^Upgrade of/.test(note||'')){const u=note.match(/Upgrade of ([^.]+)\./);if(u)sells.push('(upgrade) '+u[1])}
  for(let s of sells){const up=/^\(upgrade\) /.test(s);s=s.replace(/^\(upgrade\) /,'');
   let ow=owned.slice();const i=ow.indexOf(s);if(i<0){console.log(`  [${t}] ${n}: sells ${s} -> NOT OWNED at end of core`);continue}
   ow.splice(i,1);const g=G[n];const have=up?[]:[];ow.push(n);
   // upgrade over sold component: pay difference only; invest as new item
   const a=inv(ow);const flags=['w','s','v'].map(k=>cross(base[k],a[k]).length?`${col[k]} ${base[k]}->${a[k]} loses ${cross(base[k],a[k]).join('/')}`:'').filter(Boolean);
   console.log(`  [${t}] ${n} (${cc(n)}${g.tier}) for ${s} (${cc(s)}${G[s].tier}) => gun ${a.w} spirit ${a.s} health ${a.v}${flags.length?'  <<< '+flags.join('; '):''}`)}}}

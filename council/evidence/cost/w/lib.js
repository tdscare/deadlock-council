const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));const C={1:800,2:1600,3:3200,4:6400};
const CCm={Tech:'s',WeaponMod:'w',Armor:'v'};const cc=n=>CCm[G[n].slot];const col={w:'gun',s:'spirit',v:'health'};
const B=new Function(fs.readFileSync(SP+'data.js','utf8')+';return B')();
const num=v=>{const m=String(v).match(/^-?[\d.]+/);return m?parseFloat(m[0]):0};
function flat(b){const l=[];for(const r of b.rows)for(const [t,d,o,items] of r)if(/^(Early|Mid|Late)/.test(t))items.forEach(i=>l.push({box:t,n:i[0],note:i[1]||'',imb:i[2]}));return l}
function applyOps(list,ops){list=list.map(x=>({...x}));for(const op of ops||[]){let m;
 if(m=op.match(/^swap:(.+)=(.+)$/)){const x=list.find(i=>i.n===m[1]);x.n=m[2];x.note=''}
 else if(m=op.match(/^del:(.+)$/)){list=list.filter(i=>i.n!==m[1])}
 else if(m=op.match(/^nonote:(.+)$/)){list.find(i=>i.n===m[1]).note=''}
 else if(m=op.match(/^(mv|add):(.+)>(after|before):(.+)$/)){let it;if(m[1]==='mv'){const k=list.findIndex(i=>i.n===m[2]);it=list.splice(k,1)[0]}else it={n:m[2],note:'',box:'x'};const k=list.findIndex(i=>i.n===m[4]);list.splice(m[3]==='after'?k+1:k,0,it)}}
 return list}
function walk(list){let owned=[],souls=0,spikes={},rows=[],sold=[];
 const inv=()=>{const r={w:0,s:0,v:0};owned.forEach(n=>r[cc(n)]+=C[G[n].tier]);return r};
 for(const x of list){const n=x.n,g=G[n];const have=g.components.filter(c=>owned.includes(c));const cost=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);
  owned=owned.filter(y=>!have.includes(y));owned.push(n);souls+=cost;const m=(x.note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m){const i=owned.indexOf(m[1]);if(i>=0){owned.splice(i,1);sold.push(m[1])}}
  const iv=inv();for(const k of ['w','s','v'])if(iv[k]>=4800&&!spikes[k])spikes[k]=souls;rows.push({n,souls,cost,iv,slots:owned.length,have})}
 const iv=inv();return {rows,spikes,end:iv,souls,slots:owned.length,owned}}
const spk=(s)=>['w','s','v'].map(k=>col[k]+(s.spikes[k]?'@'+s.spikes[k]:' never')).join(', ');
function per1k(n){const g=G[n],T=C[g.tier],st=g.stats||{};const out=[];
 const sp=['TechPower','BonusTechPower','SpiritPower','ImbuedTechPower','BonusSpirit'].reduce((a,k)=>a+(st[k]!=null&&!/x /.test(st[k])?num(st[k]):0),0);
 if(sp)out.push(`SP ${(sp/T*1000).toFixed(1)}`);
 const hp=num(st.BonusHealth);if(hp)out.push(`HP ${(hp/T*1000).toFixed(0)}`);
 const wd=num(st.BaseAttackDamagePercent);if(wd)out.push(`WD% ${(wd/T*1000).toFixed(1)}`);
 const fr=num(st.BonusFireRate);if(fr)out.push(`FR% ${(fr/T*1000).toFixed(1)}`);
 const br=num(st.BulletResist),tr=num(st.TechResist);if(br)out.push(`BR% ${(br/T*1000).toFixed(1)}`);if(tr)out.push(`TR% ${(tr/T*1000).toFixed(1)}`);
 return out.length?out.join(' '):'utility'}
// cross-build positions
const pos={};for(const b of B){const s=walk(flat(b));for(const r of s.rows)(pos[r.n]=pos[r.n]||[]).push({id:b.id,souls:r.souls})}
const med=a=>{a=a.slice().sort((x,y)=>x-y);return a[Math.floor(a.length/2)]};
function xb(id,n){const mine=(pos[n].find(p=>p.id===id)||{}).souls;const oth=pos[n].filter(p=>p.id!==id);if(oth.length<3)return null;const m=med(oth.map(p=>p.souls));const e=oth.slice().sort((a,c)=>a.souls-c.souls);return {mine,m,n:oth.length,min:e[0],max:e[e.length-1],ratio:mine/m}}
module.exports={G,C,cc,col,B,flat,applyOps,walk,spk,per1k,xb,SP,fs};

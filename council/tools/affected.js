// node council/tools/affected.js "<item name | ability name | mechanic keyword>" [...]
// Lists EVERY build that could be affected by a changed value/mechanic, not just builds containing the named item:
//  - builds owning the item, its components, or anything it upgrades into / that lists it as a component
//  - builds owning any item whose game text mentions the term (shared mechanics: "bullet resist", "lifesteal", "cooldown", "imbue"...)
//  - builds whose hero ability names/text mention the term (gt ability descriptions via gamedata.js if present)
const fs=require('fs'),path=require('path');process.chdir(path.resolve(__dirname,'../..'));
const B=new Function(fs.readFileSync('data.js','utf8')+';return B')(),G=JSON.parse(fs.readFileSync('audit/items_full.json'));
let HEROES=[];try{HEROES=new Function(fs.readFileSync('gamedata.js','utf8')+';return HEROES')()}catch(e){}
const terms=process.argv.slice(2);if(!terms.length){console.log('usage: affected.js <term>...');process.exit(2)}
const own=b=>b.rows.flat().flatMap(r=>r[3].map(i=>i[0]));
const res={};
for(const t of terms){const T=t.toLowerCase(),why={};
 const direct=Object.keys(G).filter(n=>n.toLowerCase()===T);
 const rel=new Set(direct);for(const n of direct){(G[n].components||[]).forEach(c=>rel.add(c));for(const m in G)if((G[m].components||[]).includes(n))rel.add(m)}
 const txt=Object.keys(G).filter(n=>!rel.has(n)&&((G[n].desc||'')+' '+JSON.stringify(G[n].stats||{})+' '+(G[n].active||'')).toLowerCase().includes(T));
 for(const b of B){const o=own(b);const r=[];
  const a=o.filter(n=>rel.has(n));if(a.length)r.push('item/component/upgrade: '+a.join(', '));
  const x=o.filter(n=>txt.includes(n));if(x.length)r.push('item text mentions term: '+x.join(', '));
  const h=HEROES.find(h=>h.name===b.hero||h.key===b.hk);if(h&&JSON.stringify(h.ab||h).toLowerCase().includes(T))r.push('hero ability text mentions term');
  if((b.abil||[]).some(n=>n.toLowerCase().includes(T)))r.push('ability name');
  if(r.length)(res[b.id]=res[b.id]||[]).push('['+t+'] '+r.join('; '))}}
for(const id in res)console.log(id.padEnd(22),res[id].join(' | ').slice(0,200));console.log(Object.keys(res).length,'of',B.length,'builds potentially affected; reopen with: node council/tools/queue.js reopen',Object.keys(res).join(','),'"<why>"');

const fs=require('fs');const {B}=new Function(fs.readFileSync('data.js','utf8')+';return {B};')();
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));
for(const b of B){if(!/Sinclair|Abrams|Billy|Yamato|Victor|Shiv|Calico/.test(b.hero))continue;
 let core=[];const sells=[];for(const r of b.rows)for(const [t,d,o,items] of r){if(/^(Early|Mid|Late)/.test(t))for(const it of items){core.push(it[0]);const m=(it[1]||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(m)sells.push(m[1])}}
 const fin=core.filter(n=>!core.some(o=>G[o]&&G[o].components.includes(n)));
 let pct=0,heavy=0,parts=[];for(const n of fin){const s=(G[n]||{}).stats||{};if(+s.BonusMeleeDamagePercent){pct+=+s.BonusMeleeDamagePercent;parts.push(n+'+'+s.BonusMeleeDamagePercent+'%')}if(+s.BonusHeavyMeleeDamage){heavy+=+s.BonusHeavyMeleeDamage;parts.push(n+' heavy+'+s.BonusHeavyMeleeDamage)}}
 console.log(b.id.padEnd(15),'melee%',pct,'heavy+',heavy,'|',parts.join(', '));
}

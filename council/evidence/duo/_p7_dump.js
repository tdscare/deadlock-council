const fs=require('fs');const {B}=new Function(fs.readFileSync('data.js','utf8')+';return {B};')();
const M=/Melee Charge|Crushing Fists|Spirit Strike|Spirit Snatch|Lifestrike|Melee Lifesteal|Heavy|Berserker|Stalker|Acolyte|Fists|Close Quarters|Point Blank|Juggernaut|Runed|Rebuttal|Boxing/;
for(const b of B){if(!/Sinclair|Abrams|Billy|Yamato|Victor|Shiv|Calico/.test(b.hero))continue;
 const core=[];for(const r of b.rows)for(const [t,d,o,items] of r){if(/^(Early|Mid|Late)/.test(t))for(const it of items)core.push(it[0])}
 console.log(b.id,'|',b.hero,'|',b.desc,'| abil',(b.abil||[]).join('/'),'| order',JSON.stringify(b.order));
 console.log('   melee-ish core:',core.filter(n=>M.test(n)).join(', ')||'NONE');
}

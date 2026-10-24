// node council/tools/loadout.js <buildId> [--swap "Leech=Vampiric Burst"]... [--only "Leech,Ricochet"] [--level 25] [--max N]  (default: every core item, ignoring the 12-slot sell chain)
// Prints console lines (resetme + giveitem per core item) for a Sandbox trial arm.
// Imbue slot: data.js is 1-based (1..4); guides say giveitem takes 0-3 -> we emit slot-1. UNVERIFIED in game; the probe must confirm.
const fs=require('fs'),SP=__dirname+'/../../';
const [id,...a]=process.argv.slice(2);
const B=new Function(fs.readFileSync(SP+'data.js','utf8')+';return B')();
const CMD=JSON.parse(fs.readFileSync(SP+'council/sandbox/item_commands.json','utf8'));
const b=B.find(x=>x.id===id);if(!b){console.error('no build '+id);process.exit(1)}
const swaps={};let only=null,level=25,max=99;
for(let i=0;i<a.length;i+=2){if(a[i]==='--swap'){const [x,y]=a[i+1].split('=');swaps[x]=y}else if(a[i]==='--only')only=a[i+1].split(',');else if(a[i]==='--level')level=+a[i+1];else if(a[i]==='--max')max=+a[i+1]}
const core=[];for(const r of b.rows)for(const box of r){if(box[2]===false||/^(Early|Mid|Late)/.test(box[0]))box[3].forEach(it=>core.push(it))}
const out=['resetme','givelevelupgold '+level];let miss=0;
for(const it of core.slice(0,max)){let n=swaps[it[0]]||it[0];if(only&&!only.includes(n))continue;const c=CMD[n];
 if(!c){out.push('// MISSING command for '+n);miss++;continue}
 out.push('giveitem '+c+(it[2]!==undefined&&it[2]!==''&&!swaps[it[0]]?' '+(+it[2]-1):''))}
console.log(out.join('\n'));process.exit(miss?2:0);

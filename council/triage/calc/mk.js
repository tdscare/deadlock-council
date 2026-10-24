// candidate builds for section N comparison (calc only). node mk.js
const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad';
const ld=f=>JSON.parse(fs.readFileSync(SP+'/'+f,'utf8'));const W=(n,b)=>fs.writeFileSync(__dirname+'/'+n+'.json',JSON.stringify(b,null,1));
const box=(b,t)=>b.rows.flat().find(x=>x[0]===t);
function early(b,names){const e=box(b,'Early · L-R');const all=b.rows.flat().flatMap(x=>x[3]);const get=n=>JSON.parse(JSON.stringify(all.find(i=>i[0]===n)));
 const items=names.map(get);b.rows.forEach(r=>r.forEach(x=>{if(/^(Early|Mid|Late)/.test(x[0]))x[3]=x[3].filter(i=>!names.includes(i[0]))}));e[3]=items;
 b.rows.forEach(r=>{for(let k=r.length-1;k>=0;k--)if(/^(Mid|Late)/.test(r[k][0])&&!r[k][3].length)r.splice(k,1)});return b}
// Graves
const g0=ld('council/triage/calc/extract/graves_ult_old.json'),g1=ld('council/triage/calc/extract/graves_ult_new.json');W('g_P0_clean',g0);W('g_P1_current',g1);
const fixEcho=b=>{b.rows.flat().forEach(x=>x[3].forEach(i=>{if(i[0]==='Echo Shard'){i[1]='On Grasping Hands.';i[2]='2'}}));return b};
W('g_P2_AS_after_DE',fixEcho(early(ld('council/triage/calc/extract/graves_ult_new.json'),["Extra Spirit","Extra Stamina","Improved Spirit","Grit","Duration Extender","Arcane Surge","Enchanter's Emblem"])));
W('g_P3_AS_before_DE',fixEcho(early(ld('council/triage/calc/extract/graves_ult_new.json'),["Extra Spirit","Extra Stamina","Improved Spirit","Grit","Arcane Surge","Duration Extender","Enchanter's Emblem"])));
W('g_P0e_clean_echofix',fixEcho(ld('council/triage/calc/extract/graves_ult_old.json')));
W('g_P4_DE_first',fixEcho(early(ld('council/triage/calc/extract/graves_ult_new.json'),["Extra Spirit","Extra Stamina","Improved Spirit","Duration Extender","Arcane Surge","Grit","Enchanter's Emblem"])));
// Venator
const v0=ld('council/triage/calc/extract/venator_grenade_old.json'),v1=ld('council/triage/calc/extract/venator_grenade_new.json');W('v_V0_clean',v0);W('v_V1_current',v1);
W('v_V2_EH_before_Cultist',early(ld('council/triage/calc/extract/venator_grenade_old.json'),["High-Velocity Rounds","Close Quarters","Monster Rounds","Extra Health","Cultist Sacrifice","Battle Vest","Fortitude"]));
W('v_V3_BV_first',early(ld('council/triage/calc/extract/venator_grenade_old.json'),["High-Velocity Rounds","Close Quarters","Battle Vest","Monster Rounds","Cultist Sacrifice","Extra Health","Fortitude"]));
console.log('ok')

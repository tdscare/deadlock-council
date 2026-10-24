// node council/tools/validate.js  — checks every scenario against the schema
const fs=require('fs'),D=__dirname+'/../sandbox/scenarios/';let bad=0;
for(const f of fs.readdirSync(D).filter(x=>x.endsWith('.json'))){
 const s=JSON.parse(fs.readFileSync(D+f,'utf8')),e=[];
 for(const k of['id','title','hero','question','hypothesis','arms','setup','procedure','metrics','decision','trials'])if(s[k]==null)e.push('missing '+k);
 if(s.id+'.json'!==f)e.push('id/file mismatch');
 if(!Array.isArray(s.arms)||s.arms.length<2)e.push('needs >=2 arms');
 if(!(s.trials>=5))e.push('trials<5');
 if(!(s.metrics||[]).some(m=>m.primary))e.push('no primary metric');
 if(s.conditions&&!s.conditions.every(c=>c.name))e.push('conditions need names');
 (s.metrics||[]).forEach(m=>{if(!m.category)e.push('metric '+m.name+' needs category');if(!['higher','lower'].includes(m.better))e.push('metric '+m.name+' needs better')});
 if(!(s.decision&&s.decision.min_effect_pct>0))e.push('decision.min_effect_pct');
 console.log((e.length?'FAIL ':'ok   ')+f+(e.length?' — '+e.join('; '):''));bad+=e.length?1:0}
process.exit(bad?1:0);

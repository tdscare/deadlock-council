// node council/triage/triage.js  -> council/triage/TRIAGE.md  (compare LASTGOOD bak_rel vs current data.js, per changed build; read-only)
const fs=require('fs');process.chdir(__dirname+'/../..');
let src=fs.readFileSync('audit/walk2.js','utf8');src=src.slice(0,src.indexOf('const id=process.argv[2]'));
const walk=new Function('require',src+';return walk')(require);
const L=f=>new Function(fs.readFileSync(f,'utf8')+';return B')();
const O=L('council/frozen/data.CLEANBASE_pre_spikefix.js'),N=L('data.js');
const main=b=>{/* main colour = highest invested colour at the end */return null};
const prof=b=>{const {out}=walk(b);const pos={},sp={gun:null,spirit:null,health:null};let end;
 for(const l of out){const m=l.match(/^\s+(.+?) [wsv]\d.*?\| souls (\d+) \| gun (\d+) spirit (\d+) health (\d+)/);if(!m)continue;pos[m[1].replace(/ \(upgrade.*$/,'')]=+m[2];end={gun:+m[3],spirit:+m[4],health:+m[5]};
  for(const c of['gun','spirit','health'])if(sp[c]===null&&+m[{gun:3,spirit:4,health:5}[c]]>=4800)sp[c]=+m[2]}
 const mc=end?Object.keys(end).sort((a,b)=>end[b]-end[a])[0]:'?';return {pos,sp,mc,end}};
const rows=[];
for(const n of N){const o=O.find(x=>x.id===n.id);if(!o)continue;
 const core=b=>b.rows.flat().filter(([t])=>/^(Early|Mid|Late)/.test(t)).flatMap(x=>x[3].map(i=>i[0])).join('>');
 if(core(o)===core(n)&&o.order.join('')===n.order.join(''))continue;
 const po=prof(o),pn=prof(n);const moved=[];
 for(const k in pn.pos){const a=po.pos[k],b=pn.pos[k];if(a===undefined)moved.push(k+' NEW@'+b);else if(Math.abs(a-b)>=1600)moved.push(k+' '+a+'->'+b)}
 for(const k in po.pos)if(!(k in pn.pos))moved.push(k+' REMOVED(was '+po.pos[k]+')');
 const mc=pn.mc,d=(pn.sp[mc]||99999)-(po.sp[mc]||99999);
 const hd=(pn.sp.health||99999)-(po.sp.health||99999);
 const newLines=(n.changes||[]).length-(o.changes||[]).length;
 const sev=[];for(const c of['gun','spirit','health']){const a=po.sp[c],b=pn.sp[c];if(a!==null&&b!==null&&b-a>=1600&&c!==mc)sev.push(c+' 4.8k later by '+(b-a)+' ('+a+'->'+b+')')}
 if(d>=1600)sev.push('MAIN-COLOUR 4.8k LATER by '+d);if(pn.sp.health>16000&&po.sp.health<=16000)sev.push('HEALTH 4.8k pushed past 16k');if(hd>=3200)sev.push('health 4.8k later by '+hd);
 if(o.order.join('')!==n.order.join(''))sev.push('ability order changed');if(!newLines)sev.push('NO changes line');
 rows.push({id:n.id,mc,spOld:po.sp,spNew:pn.sp,moved,newLines,sev,score:(d>=1600?3:0)+sev.filter(x=>/4\.8k later/.test(x)&&!/health/.test(x)).length*3+(pn.sp.health>16000&&po.sp.health<=16000?3:0)+(hd>=3200?1:0)+(o.order.join('')!==n.order.join('')?2:0)+(newLines?0:1)});}
rows.sort((a,b)=>b.score-a.score);
let md='# Triage of builds changed since CLEANBASE (data_pre_spikefix.js)\nGenerated mechanically; "moved" = items shifting >=1.6k souls. Severity is a lead for review, not a verdict.\n\n';
for(const r of rows)md+=`## ${r.id} (main ${r.mc}) score ${r.score}\n- 4.8k old ${JSON.stringify(r.spOld)} -> new ${JSON.stringify(r.spNew)}\n- flags: ${r.sev.join('; ')||'none'}\n- moved: ${r.moved.join(', ')||'-'}\n\n`;
fs.writeFileSync('council/triage/TRIAGE.md',md);fs.writeFileSync('council/triage/triage.json',JSON.stringify(rows,null,1));
console.log(rows.length,'builds; score>=3:',rows.filter(r=>r.score>=3).length);rows.slice(0,14).forEach(r=>console.log(r.score,r.id,r.sev.join(' | ')))

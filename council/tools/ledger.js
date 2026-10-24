// node council/tools/ledger.js [scenarioId...]   -> verdicts into evidence/<hero>.json
// env: RESULTS=<dir> EVIDENCE=<dir> (used by the self-test)
const fs=require('fs'),P=__dirname+'/../';
const sl0=d=>d.endsWith('/')?d:d+'/';
const RES=sl0(process.env.RESULTS||P+'sandbox/results/'),EV=sl0(process.env.EVIDENCE||P+'evidence/'),SC=sl0(process.env.SCENARIOS||P+'sandbox/scenarios/');
const sl=d=>d.endsWith('/')?d:d+'/';
const want=process.argv.slice(2);
const stat=a=>{const n=a.length,m=a.reduce((x,y)=>x+y,0)/n,sd=Math.sqrt(a.reduce((x,y)=>x+(y-m)**2,0)/Math.max(1,n-1));return{n,mean:m,min:Math.min(...a),max:Math.max(...a),cv:m?sd/Math.abs(m):0}};
const R=fs.existsSync(RES)?fs.readdirSync(RES).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(fs.readFileSync(RES+f,'utf8'))):[];
fs.mkdirSync(EV,{recursive:true});
for(const f of fs.readdirSync(SC).filter(x=>x.endsWith('.json'))){
 const s=JSON.parse(fs.readFileSync(SC+f,'utf8'));if(want.length&&!want.includes(s.id))continue;
 const rs=R.filter(r=>r.scenario===s.id);if(!rs.length){if(want.length)console.log(s.id+': no results');continue}
 const A=s.arms[0].name,B=s.arms[1].name,out={scenario:s.id,hero:s.hero,question:s.question,decided_on:new Date().toISOString().slice(0,10),metrics:{}};
 let verdict='INCONCLUSIVE',why=[];
 for(const m of s.metrics){
  const get=arm=>rs.filter(r=>r.arm===arm&&r.metrics&&r.metrics[m.name]!=null).map(r=>({v:+r.metrics[m.name],g:(r.grade||{})[m.name]||'C'}));
  const a=get(A),b=get(B);if(!a.length||!b.length)continue;
  const sa=stat(a.map(x=>x.v)),sb=stat(b.map(x=>x.v));
  const grades=[...a,...b].map(x=>x.g),lowGrade=grades.some(g=>g==='C');
  const eff=sa.mean?((sb.mean-sa.mean)/Math.abs(sa.mean))*100:0,signed=m.better==='higher'?eff:-eff;
  const disjoint=m.better==='higher'?sb.min>sa.max:sb.max<sa.min,disjointRev=m.better==='higher'?sa.min>sb.max:sa.max<sb.min;
  out.metrics[m.name]={[A]:sa,[B]:sb,effect_pct_B_vs_A:+eff.toFixed(1),better:m.better,lowest_grade:lowGrade?'C':'A/B'};
  if(m.primary){
   const need=s.decision.min_effect_pct,n=Math.min(sa.n,sb.n);
   if(n<s.decision.min_trials)why.push(m.name+': only '+n+' trials (<'+s.decision.min_trials+')');
   else if(lowGrade)why.push(m.name+': contains grade-C readings, flag only');
   else if(Math.max(sa.cv,sb.cv)>0.25)why.push(m.name+': noisy (CV '+(Math.max(sa.cv,sb.cv)*100).toFixed(0)+'%)');
   else if(signed>=need&&disjoint){verdict='SUPPORTS_'+B;why.push(m.name+': '+B+' better by '+signed.toFixed(0)+'%, ranges do not overlap')}
   else if(signed<=-need&&disjointRev){verdict='SUPPORTS_'+A;why.push(m.name+': '+A+' better by '+(-signed).toFixed(0)+'%, ranges do not overlap')}
   else why.push(m.name+': effect '+signed.toFixed(0)+'% below '+need+'% or ranges overlap');
  }}
 out.verdict=verdict;out.reasoning=why;
 const file=EV+(s.hero==='any'?'generic':s.hero.toLowerCase())+'.json';
 const cur=fs.existsSync(file)?JSON.parse(fs.readFileSync(file,'utf8')):{};cur[s.id]=out;
 fs.writeFileSync(file,JSON.stringify(cur,null,1)+'\n');
 console.log(s.id+': '+verdict+'  ('+why.join('; ')+')');
}

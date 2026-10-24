// node path_to_build.js <build id> <strategy file | "path:A > B > ..."> <out.js> ["changes line"]   -> candidate build object (data.js shape) whose core = the given path
// core boxes keep their captions and sizes; items keep their note/imbue from the original build; the last core box takes any extra items. Never touches data.js.
const fs=require('fs'),path=require('path');const SP=path.resolve(__dirname,'../../..');
const [id,src,out,chg]=process.argv.slice(2);
const B=new Function(fs.readFileSync(SP+'/data.js','utf8')+';return B')();const b=JSON.parse(JSON.stringify(B.find(x=>x.id===id)));
let seq,order=null;
if(src.startsWith('path:'))seq=src.slice(5).split(' > ').map(s=>s.trim());
else{const t=fs.readFileSync(src,'utf8');seq=(t.match(/^CHOSEN-PATH: (.*)$/m)||[])[1].split(' > ').map(s=>s.trim());order=(t.match(/^CHOSEN-ORDER: (\d+)$/m)||[])[1]}
const meta={};b.rows.flat().forEach(([t,d,o,its])=>{if(/^(Early|Mid|Late)/.test(t))its.forEach(x=>meta[x[0]]=x)});
const core=[];b.rows.forEach((r,ri)=>r.forEach((x,bi)=>{if(/^(Early|Mid|Late)/.test(x[0]))core.push([ri,bi,x[3].length])}));
let k=0;core.forEach(([ri,bi,n],i)=>{const take=i===core.length-1?seq.length-k:n;b.rows[ri][bi][3]=seq.slice(k,k+take).map(nm=>meta[nm]?meta[nm].slice():[nm,'']);k+=take});
if(order)b.order=order.split('').map(Number);
delete b.changes;if(chg)b.changes=[chg];
fs.writeFileSync(out,JSON.stringify(b,null,1));console.log('wrote',out,'core',seq.length,'items, order',b.order.join(''));

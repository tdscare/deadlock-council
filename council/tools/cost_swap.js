// usage: node council/tools/cost_swap.js <id> '<json edits>'  edits: [{rep:"X",with:"Y"},{rm:"X"},{add:"Y",after:"X"},{move:"X",after:"Y"}]
process.chdir(__dirname+'/../..');
const fs=require('fs');let src=fs.readFileSync('audit/walk2.js','utf8');src=src.slice(0,src.indexOf('const id=process.argv[2]'));
const ctx=new Function('require',src+';return {walk,B,IT,C}')(require);const {walk,B,IT,C}=ctx;
const id=process.argv[2];const edits=JSON.parse(process.argv[3]||'[]');
const b0=B.find(x=>x.id===id);const clone=o=>JSON.parse(JSON.stringify(o));
function crossings(b){ // souls at which each colour first reaches thresholds
 const G=IT;let owned=[],souls=0;const res={w:{},s:{},v:{}};const TH=[4800,6400,8000,16000];
 const G2=JSON.parse(fs.readFileSync('audit/items_full.json'));
 for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
  for(const [n,note] of items){const g=G2[n];const have=g.components.filter(c=>owned.includes(c));souls+=C[g.tier]-have.reduce((a,c)=>a+C[G2[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);
   const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
   const inv={w:0,s:0,v:0};owned.forEach(x=>inv[IT[x].c]+=C[IT[x].t]);
   for(const k in inv)for(const th of TH)if(inv[k]>=th&&res[k][th]==null)res[k][th]=souls;}}
 return {res,final:owned,souls}}
function apply(b,edits){b=clone(b);for(const e of edits){for(const r of b.rows)for(const bx of r){const it=bx[3];
  if(e.rep){const i=it.findIndex(x=>x[0]===e.rep);if(i>=0)it[i]=[e.with,e.note||'',e.imb];}
  if(e.rm){const i=it.findIndex(x=>x[0]===e.rm);if(i>=0)it.splice(i,1);}
  if(e.add){const i=it.findIndex(x=>x[0]===e.after);if(i>=0)it.splice(i+1,0,[e.add,e.note||'',e.imb]);}
  }}return b}
function show(tag,b){const {out,flags}=walk(b);const c=crossings(b);
 console.log('--',tag);console.log(out.filter(l=>/^   |^Core|^Spikes/.test(l)).map(l=>l.replace(/ — .*/,'')).join('\n'));
 console.log('crossings (souls) gun',JSON.stringify(c.res.w),'spirit',JSON.stringify(c.res.s),'health',JSON.stringify(c.res.v));console.log('flags',flags.join('; ')||'none');}
if(process.argv[4]==='brief'){const b1=apply(b0,edits);for(const [tag,b] of [['base',b0],['swap',b1]]){const c=crossings(b);console.log(tag,'gun',JSON.stringify(c.res.w),'spirit',JSON.stringify(c.res.s),'health',JSON.stringify(c.res.v),'end',c.souls)}}
else{show('base',b0);if(edits.length)show('swap '+process.argv[3],apply(b0,edits))}

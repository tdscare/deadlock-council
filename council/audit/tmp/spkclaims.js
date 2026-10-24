const fs=require('fs');process.chdir(__dirname+'/../../..');
const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const CC={Tech:'spirit',WeaponMod:'gun',Armor:'health'},C={1:800,2:1600,3:3200,4:6400};
let tot=0,bad=0;const rows=[];
for(const b of B){let owned=[],souls=0,sp={};
 for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;for(const [n,note] of items){const g=G[n];const have=g.components.filter(c=>owned.includes(c));souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
  const inv={gun:0,spirit:0,health:0};owned.forEach(x=>inv[CC[G[x].slot]]+=C[G[x].tier]);for(const k in inv)if(inv[k]>=4800&&sp[k]==null)sp[k]=souls}}
 const last=(b.changes||[]).slice(-1)[0]||'';
 // only the final changes line: claims about current state
 for(const m of last.matchAll(/(gun|spirit|health) 4\.8k (?:now |still |lands |holds |stays |is |at |@ )*(?:at |@ )?(\d+(?:\.\d)?)k/gi)){const col=m[1].toLowerCase(),claim=+m[2]*1000;tot++;const actual=sp[col];
  if(actual==null||Math.abs(actual-claim)>900){bad++;rows.push(`${b.id}: last changes line says ${col} 4.8k at ${m[2]}k; data.js walk gives ${actual==null?'never':(actual/1000).toFixed(1)+'k'} | "${last.slice(Math.max(0,m.index-50),m.index+80).replace(/\s+/g,' ')}"`)}}}
console.log('claims in final changes line:',tot,'mismatching (>0.9k):',bad);console.log(rows.join('\n'));

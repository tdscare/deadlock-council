const fs=require('fs');process.chdir(__dirname+'/../../..');
const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const CC={Tech:'s',WeaponMod:'w',Armor:'v'},C={1:800,2:1600,3:3200,4:6400};
for(const id of process.argv.slice(2)){const b=B.find(x=>x.id===id);let owned=[],souls=0;console.log('\n=== '+id,b.name,'|',b.desc,'| order',b.order.join(''));
 for(const r of b.rows)for(const [t,d,o,items] of r){console.log(' ['+t+(o?' opt':'')+'] '+(d||''));
  items.forEach(([n,note,imb])=>{let tag='';if(/^(Early|Mid|Late)/.test(t)){const g=G[n];const have=g.components.filter(c=>owned.includes(c));souls+=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);owned=owned.filter(x=>!have.includes(x));owned.push(n);const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);if(sm){const i=owned.indexOf(sm[1]);if(i>=0)owned.splice(i,1)}
   const inv={w:0,s:0,v:0};owned.forEach(x=>inv[CC[G[x].slot]]+=C[G[x].tier]);tag=` @${souls} w${inv.w} s${inv.s} v${inv.v}`}
   console.log('    '+n+(imb?'→'+imb:'')+tag+(note?'  // '+note.slice(0,110):''))})}
 if(process.env.CH)(b.changes||[]).slice(-2).forEach(c=>console.log('  CHG: '+c.slice(0,500)))}

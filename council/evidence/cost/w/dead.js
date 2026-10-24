const fs=require('fs');const SP='/tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad/';
const G=JSON.parse(fs.readFileSync(SP+'audit/items_full.json'));const C={1:800,2:1600,3:3200,4:6400};
const ids=fs.readFileSync(SP+'council/evidence/cost/chunk0.txt','utf8').split(/\s+/).filter(Boolean);
for(const id of ids){const b=JSON.parse(fs.readFileSync(SP+'council/evidence/cost/w/'+id+'.json'));
 const core=[];const all=[];let txt='';
 for(const r of b.rows)for(const [t,d,o,items] of r){txt+=' '+(d||'');for(const [n,note] of items){txt+=' '+(note||'');all.push([t,n]);if(/^(Early|Mid|Late)/.test(t))core.push(n)}}
 const upg=n=>Object.keys(G).filter(k=>G[k].components.includes(n));
 const dead=[];
 // simulate final owned (components consumed)
 let owned=[];for(const n of core){const g=G[n];owned=owned.filter(x=>!g.components.includes(x));owned.push(n)}
 for(const n of owned){const g=G[n];if(g.tier>2)continue;
  const sold=new RegExp('Sell (?:[^.]*?)?'+n.replace(/[.*+?^${}()|[\]\\']/g,'.')+'').test(txt)||new RegExp(n.replace(/[.*+?^${}()|[\]\\']/g,'.')+'[^.]*? for this').test('');
  const ups=upg(n).filter(u=>core.includes(u)||all.some(a=>a[1]===u));
  const where=ups.map(u=>all.find(a=>a[1]===u)[0]);
  dead.push(`${n} (T${g.tier}, ${C[g.tier]}) upgrades-in-build:${ups.length?ups.map((u,i)=>u+'['+where[i]+']').join(','):'none'} named-sell:${sold?'yes':'no'}`)}
 console.log('== '+id+' slots at end: '+owned.length);dead.forEach(x=>console.log('  '+x))}

const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();
const ids=process.argv.slice(2);
for(const id of ids){const b=B.find(x=>x.id===id);fs.writeFileSync('council/apply/chunk3/w/'+id+'.js',JSON.stringify(b,null,1));
console.log('##',id,b.name,'|',b.desc,'| order',b.order.join(''));
for(const r of b.rows)for(const [t,d,o,items] of r)console.log(' ['+t+'] '+d+(o?' (opt)':'')+': '+items.map(i=>i[0]+(i[1]?' {'+i[1]+'}':'')+(i[2]?' @'+i[2]:'')).join(' | '));
console.log(' changes:',JSON.stringify(b.changes))}

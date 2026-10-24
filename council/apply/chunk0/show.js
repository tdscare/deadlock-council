const fs=require('fs');const f=process.argv[2];
const b=new Function('return ('+fs.readFileSync(f,'utf8').trim().replace(/,\s*$/,'')+')')();
console.log(b.id,'|',b.name,'|',b.desc,'| order',b.order.join(''));
for(const r of b.rows)for(const [t,d,o,items] of r){console.log(`## ${t} ${o?'(opt)':''} ${d?'["'+d+'"]':''}`);for(const [n,note,imb] of items)console.log('   - '+n+(imb?' <imb '+imb+'>':'')+(note?'  // '+note:''))}
console.log('CHANGES',JSON.stringify(b.changes));

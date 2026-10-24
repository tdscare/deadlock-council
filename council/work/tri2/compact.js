const b=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
console.log(b.id,b.name,'|',b.desc,'| order',b.order&&b.order.join(''));
for(const k of Object.keys(b))if(!['rows','changes'].includes(k))console.log(' ',k,JSON.stringify(b[k]).slice(0,200));
b.rows.forEach((r,ri)=>r.forEach(([t,d,op,its])=>{console.log('ROW'+ri,'['+t+']',d?'('+d+')':'',op||'');its.forEach(it=>console.log('    ',JSON.stringify(it)))}));
console.log('CHANGES:');(b.changes||[]).forEach(c=>console.log(' -',c));

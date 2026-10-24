const fs=require('fs');const D=__dirname;
exports.load=id=>JSON.parse(fs.readFileSync(D+'/in/'+id+'.js','utf8'));
exports.save=(b)=>fs.writeFileSync(D+'/out/'+b.id+'.js',JSON.stringify(b,null,1));
exports.find=(b,n)=>{for(const r of b.rows)for(const bx of r)for(let i=0;i<bx[3].length;i++)if(bx[3][i][0]===n)return {bx,i,item:bx[3][i]};throw Error('no '+n)};
exports.box=(b,t)=>{for(const r of b.rows)for(const bx of r)if(bx[0]===t)return bx;throw Error('nobox '+t)};
// move item to be after `after` (in that item's box) or at end of box if after===null
exports.move=(b,n,boxTitle,afterName)=>{const f=exports.find(b,n);f.bx[3].splice(f.i,1);const t=exports.box(b,boxTitle);const j=afterName?t[3].findIndex(x=>x[0]===afterName)+1:0;if(afterName&&j===0)throw Error('after '+afterName);t[3].splice(j,0,f.item)};
exports.note=(b,n,s)=>{const f=exports.find(b,n);f.item[1]=s};
exports.add=(b,l)=>{(b.changes=b.changes||[]).push(l)};
exports.cleanRows=b=>{b.rows=b.rows.map(r=>r.filter(bx=>bx[3].length)).filter(r=>r.length)};

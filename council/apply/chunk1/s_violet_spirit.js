const L=require('./lib');const b=L.load('violet_spirit');
L.after(b,'Spirit Lifesteal',['Improved Spirit','']);
const mid=L.box(b,'Mid');const rest=mid[3].splice(8);
for(let r=0;r<b.rows.length;r++)for(let k=0;k<b.rows[r].length;k++)if(b.rows[r][k]===mid){b.rows.splice(r+1,0,[["Mid · cont.","",false,rest]]);r=1e9;break}
b.changes.push('Cost pass: Improved Spirit added in Mid so Boundless Spirit costs 1.6k less.');
L.save(b,'violet_spirit');

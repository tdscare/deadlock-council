const L=require('./lib');const b=L.load('geist');
L.after(b,'Bullet Resist Shredder',['Spirit Lifesteal','']);L.after(b,'Bullet Resist Shredder',['Bullet Lifesteal','']);
const mid=L.box(b,'Mid');const rest=mid[3].splice(8);
for(let r=0;r<b.rows.length;r++)for(let k=0;k<b.rows[r].length;k++)if(b.rows[r][k]===mid){b.rows.splice(r+1,0,[["Mid · cont.","",false,rest]]);r=1e9;break}
b.name="Rizuhble's Stubborn Old Geist";
b.changes.push('Cost pass: Bullet Lifesteal and Spirit Lifesteal added in Mid so Leech costs 3.2k less and sustain comes earlier; renamed.');
L.save(b,'geist');

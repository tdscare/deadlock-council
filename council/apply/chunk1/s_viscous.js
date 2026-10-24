const L=require('./lib');const b=L.load('viscous');
const old=L.take(b,'Mystic Expansion');
const mid=L.box(b,'Mid');
L.after(b,'Trophy Collector',old);
const items=mid[3];const rest=items.splice(8);
for(let r=0;r<b.rows.length;r++)for(let k=0;k<b.rows[r].length;k++)if(b.rows[r][k]===mid){b.rows.splice(r+1,0,[["Mid · cont.","",false,rest]]);r=1e9;break}
b.changes.push('Cost pass: Mystic Expansion moved from Late to Mid (cube imbue was idle for 28k souls); Greater Expansion upgrades it.');
L.save(b,'viscous');

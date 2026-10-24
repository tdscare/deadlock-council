const L=require('./lib');const b=L.load('yamato_brawler');
const mc=L.take(b,'Melee Charge');const mid=L.box(b,'Mid');mid[3].unshift(mc);
const rest=mid[3].splice(8);
for(let r=0;r<b.rows.length;r++)for(let k=0;k<b.rows[r].length;k++)if(b.rows[r][k]===mid){b.rows.splice(r+1,0,[["Mid · cont.","",false,rest]]);r=1e9;break}
L.note(b,'Leech',"Sell Hunter's Aura for this.");
b.changes.push("Cost pass: Melee Charge moved to the start of Mid (was bought after 9.6k of gun items); Leech now sells Hunter's Aura instead of Bullet Resist Shredder.");
L.save(b,'yamato_brawler');

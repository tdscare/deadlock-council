const L=require('./lib');const b=L.load('mcginnis_turret');
const sw=L.box(b,'Swap for');sw[0]='Swap for Healbane';sw[3]=[['Heroic Aura','Instead of Healbane when your team has gun heroes.']];
const tc=L.take(b,'Transcendent Cooldown');tc[1]='Upgrade of Superior Cooldown.';
const sl=L.box(b,'Slot locked');sl[3].unshift(tc);
const mid=L.box(b,'Mid');mid[3].unshift(['Improved Spirit','']);
const rest=mid[3].splice(8);
for(let r=0;r<b.rows.length;r++)for(let k=0;k<b.rows[r].length;k++)if(b.rows[r][k]===mid){b.rows.splice(r+1,0,[["Mid · cont.","",false,rest]]);r=1e9;break}
b.name="Rizuhble's Flat-Pack Fort McGinnis";
b.changes.push('Cost pass: Heroic Aura swap now replaces Healbane (was Mystic Slow, which broke the spirit 4.8k); Transcendent Cooldown moved to Slot locked; Improved Spirit added at the start of Mid so Boundless Spirit costs 1.6k less; renamed.');
L.save(b,'mcginnis_turret');

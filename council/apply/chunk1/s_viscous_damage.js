const L=require('./lib');const b=L.load('viscous_damage');
const x=L.take(b,'Improved Spirit');const mid=L.box(b,'Mid');mid[3].unshift(x);
b.changes.push('Cost pass: Improved Spirit moved to the start of Mid (was a late buy of a cheap upgrade).');
L.save(b,'viscous_damage');

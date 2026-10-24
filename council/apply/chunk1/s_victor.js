const L=require('./lib');const b=L.load('victor');
const x=L.take(b,'Boundless Spirit');L.after(b,'Scourge',x);
b.changes.push('Cost pass: Boundless Spirit moved to right after Scourge (was the last buy).');
L.save(b,'victor');

const L=require('./lib');const b=L.load('mina');
const t=L.take(b,'Tankbuster');L.after(b,'Boundless Spirit',t);
b.changes.push('Cost pass: Tankbuster moved after Boundless Spirit (was the earliest in any Mina build at 12k).');
b.name="Rizuhble's Takeaway Mina";b.changes.push('Renamed.');
L.save(b,'mina');

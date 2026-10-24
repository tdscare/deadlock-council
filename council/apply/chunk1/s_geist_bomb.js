const L=require('./lib');const b=L.load('geist_bomb');
const x=L.take(b,'Boundless Spirit');L.after(b,'Leech',x);
b.name="Rizuhble's Guy Fawkes Geist";
b.changes.push('Cost pass: Boundless Spirit moved to right after Leech (was nearly last); renamed.');
L.save(b,'geist_bomb');

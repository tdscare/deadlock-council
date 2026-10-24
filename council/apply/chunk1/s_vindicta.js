const L=require('./lib');const b=L.load('vindicta');
const rich=L.box(b,"I'm rich");rich[3]=rich[3].filter(i=>i[0]!=='Ricochet');
const [x,i]=L.find(b,'Spellslinger');x[3][i]=['Ricochet',''];
b.changes.push('Cost pass: Spellslinger (needs casts a gun Vindicta rarely makes) replaced by Ricochet in Late; Ricochet removed from the rich box.');
L.save(b,'vindicta');

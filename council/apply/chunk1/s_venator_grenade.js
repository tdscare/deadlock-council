const L=require('./lib');const b=L.load('venator_grenade');
L.after(b,'Hollow Point',['Bullet Lifesteal','']);
b.changes.push('Cost pass: Bullet Lifesteal added in Mid (mid-game sustain) so Vampiric Burst costs 1.6k less.');
L.save(b,'venator_grenade');

const L=require('./lib');const b=L.load('bebop');
b.name="Rizuhble's Lane Bully Bebop";
L.move(b,'Fortitude','Mid · L-R','Spirit Snatch');
L.note(b,'Lucky Shot','Sell Headshot Booster for this.');
L.note(b,'Spellslinger','Sell Crippling Headshot for this.');
L.cleanRows(b);
L.add(b,"Cost pass: renamed Lane Bully Bebop; Fortitude right after Spirit Snatch (spikes unchanged); Lucky Shot sells Headshot Booster and Spellslinger sells Crippling Headshot so spirit 4.8k holds.");
L.save(b);

const L=require('./lib');const b=L.load('danny');
L.move(b,'Sharpshooter','Early · L-R','Opening Rounds');
L.move(b,'Surge of Power','Mid · L-R','Tankbuster'); // before Greater Expansion
const s=L.box(b,'Counters');s[1]="Get after Diviner's Kevlar if needed. Ahead? Skip it until you're dying. Sell Enchanter's Emblem for it.";
L.note(b,'Mystic Reverb','On the dive. Sell Greater Expansion for this.');
L.note(b,'Witchmail','Sell Reactive Barrier for this.');
L.cleanRows(b);
L.add(b,"Cost pass: Sharpshooter right after Opening Rounds (gun 4.8k at 4.8k souls); Surge of Power before Greater Expansion; counters sell Enchanter's Emblem, Reverb sells Greater Expansion, Witchmail sells Reactive Barrier (Opening Rounds stays so gun 4.8k holds).");
L.save(b);

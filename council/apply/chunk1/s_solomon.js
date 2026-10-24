const L=require('./lib');const b=L.load('solomon');
L.after(b,'Warp Stone',['Hollow Point','']);
L.take(b,'Echo Shard');
L.note(b,'Opening Rounds','');L.note(b,'Grit','Sell it for a counter.');
const c=L.box(b,'Counters');c[1]=c[1].replace('Sell Opening Rounds','Sell Grit');
const r=L.box(b,"I'm rich");L.note(b,'Refresher','Sell Guardian Ward for this.');
r[3].push(['Echo Shard','Sell Mystic Reverb for this.','3']);
b.changes.push('Cost pass: Hollow Point added after Warp Stone so gun reaches 4.8k (was a token 1.6k); Echo Shard moved to the rich box; counters now sell Grit (not Opening Rounds).');
b.name=b.name;L.save(b,'solomon');

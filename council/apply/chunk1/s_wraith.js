const L=require('./lib');const b=L.load('wraith');
b.rows=b.rows.map(r=>r.filter(x=>!x[0].startsWith('Lost lane'))).filter(r=>r.length);
b.name="Rizuhble's Pinball Wraith";
b.changes.push('Cost pass: removed the Lost lane reorder box (put a lone 6.4k buy at 12.8k and delayed the spirit 4.8k); renamed.');
L.save(b,'wraith');

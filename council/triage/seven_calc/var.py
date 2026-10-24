# make a variant build: python3 var.py base.json out.json "Early:a,b|Mid:c,d|Late:e,f" [order]
import json,sys
b=json.load(open(sys.argv[1])); spec=dict(x.split(':',1) for x in sys.argv[3].split('|'))
pool={}
import os
for pf in os.environ.get('POOL','').split(','):
    if pf:
        for r in json.load(open(pf))['rows']:
            for box in r:
                for it in box[3]: pool.setdefault(it[0],it)
for r in b['rows']:
    for box in r:
        for it in box[3]: pool.setdefault(it[0],it)
for r in b['rows']:
    for box in r:
        for k,v in spec.items():
            if box[0].startswith(k): box[3]=[pool[n] for n in v.split(',')]
if len(sys.argv)>4: b['order']=[int(c) for c in sys.argv[4]]
json.dump(b,open(sys.argv[2],'w'),indent=1)

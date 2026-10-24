import json,sys
for f in sys.argv[1:]:
  b=json.load(open(f)); print('\n###',b['id'],b['name'],'|',b['desc'],'| order',''.join(map(str,b['order'])),b['abil'])
  for r in b['rows']:
    for bx in r:
      print(' [%s]%s'%(bx[0],'(opt)' if bx[2] else ''),('<'+bx[1]+'>' if bx[1] else ''), '; '.join(i[0]+('{%s}'%i[2] if len(i)>2 and i[2] else '')+(' -"'+i[1]+'"' if i[1] else '') for i in bx[3]))
  print(' changes:',len(b.get('changes',[])))

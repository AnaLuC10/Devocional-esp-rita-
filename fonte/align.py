import json,re,difflib
B=json.load(open('blocks.json'))
J=json.load(open('/home/claude/bwasistemas/kardec-datasets-br/livro_dos_espiritos.json'))
def norm(s): return re.sub(r'[^a-zà-ú0-9 ]','',re.sub(r'\*','',s.lower()))[:120]
jq=[(x['Id'],norm(x['Question'])) for x in J]
qs=[b for b in B if b['t']=='q']
j=0; res=[]
for q in qs:
    nq=norm(q['text']); best=None
    for k in range(max(0,j-5),min(len(jq),j+15)):
        r=difflib.SequenceMatcher(None,nq,jq[k][1]).ratio()
        if best is None or r>best[0]: best=(r,k)
    r,k=best
    q['jid']=jq[k][0]; q['jr']=round(r,2)
    if r<0.8 or jq[k][0].rstrip('abcdefgh')!=re.match(r'\d+',q['label']).group(): 
        print(q['line'],q['label'],'->',jq[k][0],r, q['text'][:60],'|',J[k]['Question'][:60])
    j=k+1
json.dump(B,open('blocks.json','w'),ensure_ascii=False)
used={q['jid'] for q in qs}
print('json ids not matched:',[x['Id'] for x in J if x['Id'] not in used])

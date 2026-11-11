import re, json, sys
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
H = re.compile(r'^(#{1,5})\s+`([^`]*)`\s*\S+\s*(.*)$')
QL = re.compile(r'^`lde\.q([0-9a-z]+)`\s*(?:#️⃣)?\s*(\d+\s*\.?\s*(?:[a-z]\)|[a-z]\.)?)\s*(.*)$')
blocks=[]; stop=False
for i,l in enumerate(lines,1):
    s=l.rstrip()
    if s.startswith('## ') and 'Pós-textual' in s: break
    m=H.match(s)
    if m:
        blocks.append({'t':'h','lvl':len(m.group(1)),'id':m.group(2),'title':m.group(3).strip(),'line':i}); continue
    st=s.strip()
    if not st or st=='---' or st=='>' or st=='> >': continue
    if st.startswith('[^'):
        blocks.append({'t':'fn','text':st,'line':i}); continue
    m=QL.match(st)
    if m:
        blocks.append({'t':'q','id':m.group(1),'label':m.group(2).strip(),'text':m.group(3).strip(),'line':i}); continue
    if re.match(r'^>\s*>',st):
        blocks.append({'t':'com','text':re.sub(r'^>\s*>\s*','',st),'line':i}); continue
    if st.startswith('>'):
        blocks.append({'t':'ans','text':st[1:].strip(),'line':i}); continue
    blocks.append({'t':'p','text':st,'line':i})
json.dump(blocks,open('blocks.json','w'),ensure_ascii=False)
qs=[b for b in blocks if b['t']=='q']
print(len(blocks),'blocks',len(qs),'questions')
from collections import Counter
c=Counter(q['id'] for q in qs); print('dup ids',[k for k,v in c.items() if v>1])
prev=0
for q in qs:
    n=int(re.match(r'\d+',q['id']).group())
    if n<prev or n>prev+1: print('jump',prev,'->',q['id'],q['label'],'line',q['line'])
    prev=max(prev,n)
nums={int(re.match(r'\d+',q['id']).group()) for q in qs}
print('missing',sorted(set(range(1,1020))-nums))
print(Counter(b['t'] for b in blocks))

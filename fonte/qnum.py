import json,re,unicodedata
raw=open('/tmp/claude-0/-home-claude/b4f831e8-c069-56fa-be06-9c3cbe10a026/scratchpad/dl/le1.txt',encoding='utf-8').read()
raw=re.sub(r'.*\.p65.*\n','',raw); raw=re.sub(r'-\n','',raw)
def norm(s):
    s=unicodedata.normalize('NFC',s).lower().replace('ü','u')
    s=re.sub(r'\*|_|<br\s*/?>|\[\^\d*\]:?|❦','',s)
    return re.sub(r'[^a-zà-ú0-9]+','',s)
# build normalized string with index map back to raw
N=[];M=[]
for i,ch in enumerate(raw):
    c=norm(ch)
    for x in c: N.append(x); M.append(i)
N=''.join(N)
B=json.load(open('blocks.json'))
pos=0;bad=[]
for b in B:
    if b['t']!='q': continue
    t=norm(b['text'])
    k=-1
    for a in (0,5,10,20):
        k=N.find(t[a:a+25],pos)
        if k!=-1 and k-pos<200000: k-=a; break
        k=-1
    if k<0: bad.append((b['line'],b['label'],'NF',b['text'][:60])); continue
    pre=raw[max(0,M[k]-25):M[k]]
    m=re.search(r'(\d+)\s*\.?\s*(?:([a-z])\))?\s*$',pre.replace('\n',' '))
    pn=(m.group(1)+(m.group(2) or '')) if m else None
    mn=re.sub(r'[^0-9a-z]','',b['label'])
    b['pdfnum']=pn
    if pn!=mn: bad.append((b['line'],b['label'],pn,repr(pre[-20:]),b['text'][:50]))
    pos=k
json.dump(B,open('blocks.json','w'),ensure_ascii=False)
for x in bad: print(x)
print(len(bad))

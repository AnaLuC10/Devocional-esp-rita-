import json,re,unicodedata,os
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))+'/'
h=open(R+'biblia/index.html').read()
i=h.index('"livros":'); 
# parse livros via json decoder
dec=json.JSONDecoder()
livros,_=dec.raw_decode(h[i+len('"livros":'):])
NOMES=[l[0] for l in livros]
busca=json.load(open(R+'biblia/busca.json'))
CH={(NOMES[b],c):v for b,c,v in busca}
def norm(s):
    s=unicodedata.normalize('NFC',s).lower()
    s=re.sub(r'[“”"«»‘’\'.,;:!?()—–\-]',' ',s)
    return re.sub(r'\s+',' ',s).strip()
def parse(ref):
    ref=ref.strip().replace('–','-')
    m=re.match(r'^(.+?) (\d+)(?::(\d+)(?:-(\d+)(?::(\d+))?)?)?$',ref)
    if not m: return None
    b,c,v1,v2,v3=m.groups()
    c=int(c)
    if b not in NOMES: return None
    if (b,c) not in CH: return None
    if v1 is None: return [(b,c,v+1) for v in range(len(CH[(b,c)]))]
    v1=int(v1)
    if v3: # c:v-c2:v3
        c2=int(v2); out=[]
        for cc in range(c,c2+1):
            if (b,cc) not in CH: return None
            n=len(CH[(b,cc)])
            a=v1 if cc==c else 1; z=int(v3) if cc==c2 else n
            if z>n: return None
            out+=[(b,cc,v) for v in range(a,z+1)]
        return out
    v2=int(v2) if v2 else v1
    n=len(CH[(b,c)])
    if v1<1 or v2>n or v2<v1: return None
    return [(b,c,v) for v in range(v1,v2+1)]
def texto(ref):
    p=parse(ref); return ' '.join(CH[(b,c)][v-1] for b,c,v in p) if p else None
ALL=None
def allnorm():
    global ALL
    if ALL is None: ALL=' | '.join(norm(' '.join(v)) for v in CH.values())
    return ALL

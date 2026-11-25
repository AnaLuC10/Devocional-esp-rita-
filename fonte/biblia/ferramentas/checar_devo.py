"""Uso: python3 checar_devo.py ARQUIVO.json
O arquivo tem {"semanas": [...cartões jornada...], "conversar": {"24": "texto", ...}}."""
import os,sys,json,re,html,datetime as dt
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))+'/'
h=open(R+'index.html').read()
D=json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>',h,re.S).group(1))['days']
def plain(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',b)))
F=json.load(open(sys.argv[1])); s_all=json.dumps(F,ensure_ascii=False).lower()
if 'evangélic' in s_all: print('PROIBIDO: contém "evangélic"')
for s in F.get('semanas',[]):
    p=[]
    for f in ('de','ate','titulo','q','resumo','conceitos','frase','evangelho'):
        if f not in s: p.append('FALTA '+f)
    ws={dt.date.fromisoformat(D[n-1]['date']).isocalendar()[:2] for n in range(s['de'],s['ate']+1)}
    if len(ws)!=1: p.append('dias de semanas diferentes do calendário')
    if not 4<=len(s.get('conceitos',[]))<=6: p.append('conceitos 4-6')
    body=' '.join(plain(D[n-1]['body']) for n in range(s['de'],s['ate']+1))
    fr=s.get('frase',['',''])[0]
    if fr not in body: p.append('FRASE não está literal no texto dessa semana: '+fr)
    print(f"Cartão {s['de']}-{s['ate']}:", '; '.join(p) if p else 'ok')
for k,v in sorted(F.get('conversar',{}).items(),key=lambda x:int(x[0])):
    n=len(re.findall(r'(?<!Q)\.(\s|$)|[!?](\s|$)',v))
    print(f'Conversar {k}: {n} frases', 'ok' if 3<=n<=5 else 'CONFERIR (3-5 frases)')

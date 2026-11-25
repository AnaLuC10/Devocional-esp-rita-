"""Uso: python3 devo.py N [N2 ...] -> mostra o Dia N do devocional: data, questões, título, versículo do dia (bib/bref) e o texto do livro (body) em texto puro.
   python3 devo.py N --curto -> só data, questões, título e versículo."""
import os,sys,json,re,html
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))+'/'
h=open(R+'index.html').read()
D=json.loads(re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>',h,re.S).group(1))['days']
def plain(b):
    b=re.sub(r'</p>|</div>','\n',b); b=re.sub(r'<[^>]+>','',b); return html.unescape(re.sub(r'\n\s*\n+','\n',b)).strip()
curto='--curto' in sys.argv
for a in sys.argv[1:]:
    if not a.isdigit(): continue
    d=D[int(a)-1]
    print(f"### Dia {d['n']} ({d['date']}) {d['q']} – {d['short']}\nVersículo do dia: {d['bref']} | {d['bib']}")
    if not curto: print(plain(d['body'])); print()

"""Uso: python3 checar.py ARQUIVO.json
O arquivo tem {"dias": {"23": {...}}, "semanas": [{...}]}. Confere formato, chave, marcar, tamanhos, aspas (Bíblia Livre) e cartões."""
import sys,json,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import bib
dias={d['n']:d for d in json.load(open(bib.R+'fonte/biblia/dias.json'))}
com=json.load(open(bib.R+'biblia/comentarios.json'))
F=json.load(open(sys.argv[1]))
A=bib.allnorm()
def inreading(ref,ns):
    p=bib.parse(ref)
    if not p: return False
    segs=[s for n in ns for s in dias[n]['segs']]
    return all(any(b==s['livro'] and s['de']<=cc<=s['ate'] for s in segs) for b,cc,v in p)
def wc(s): return len(re.sub(r'\*\*','',s).split())
def quotes(s): return re.findall(r'["“]([^"”]{3,})["”]',s)
ok=True
CAMPOS=('titulo','chave','resumo','espirita','evangelica','comum','hoje','marcar','kardec','estudo')
for k,e in sorted(F.get('dias',{}).items(),key=lambda x:int(x[0])):
    n=int(k); probs=[]
    for f in CAMPOS:
        if f not in e: probs.append('FALTA '+f)
    if set(e)-set(CAMPOS): probs.append('campos a mais: %s'%(set(e)-set(CAMPOS)))
    if 'chave' in e and not inreading(e['chave'],[n]): probs.append('CHAVE fora da leitura ou inválida: '+e['chave'])
    for r,_ in e.get('marcar',[]):
        if not bib.parse(r): probs.append('MARCAR inválida: '+r)
    if not 3<=len(e.get('marcar',[]))<=4: probs.append('marcar precisa de 3 ou 4')
    we,wv=wc(e['espirita']),wc(e['evangelica']); pe,pv=e['espirita'].count('\n')+1,e['evangelica'].count('\n')+1
    r=max(we,wv)/max(1,min(we,wv))
    if r>1.2: probs.append(f'DIFERENÇA de tamanho {r:.2f} (>1.20)')
    if not(130<=we<=230 and 130<=wv<=230): probs.append(f'TAMANHO fora de 130-230: esp {we} ev {wv}')
    if not(4<=pe<=6 and 4<=pv<=6): probs.append(f'PARÁGRAFOS (4-6): esp {pe} ev {pv}')
    for f in ('titulo','resumo','espirita','evangelica','comum','hoje'):
        for q in quotes(e.get(f,'')):
            if bib.norm(q) and bib.norm(q) not in A: probs.append(f'ASPAS não batem com a Bíblia Livre [{f}]: "{q}"')
    print(f'Dia {n} ({dias[n]["ref"]}) esp {we}p{pe} ev {wv}p{pv}:', '; '.join(probs) if probs else 'ok')
    if probs: ok=False
for s in F.get('semanas',[]):
    probs=[]
    for f in ('de','ate','titulo','ref','resumo','personagens','lugares','espirita','evangelica','chave'):
        if f not in s: probs.append('FALTA '+f)
    ns=list(range(s['de'],s['ate']+1))
    for n in ns:
        if str(n) not in com and str(n) not in F.get('dias',{}): probs.append(f'Dia {n} sem conteúdo')
    if not inreading(s['chave'],ns): probs.append('CHAVE fora da semana: '+s['chave'])
    txt=' '.join(bib.norm(' '.join(bib.CH[(sg['livro'],c)])) for n in ns for sg in dias[n]['segs'] for c in range(sg['de'],sg['ate']+1))
    for campo in ('personagens','lugares'):
        L=s.get(campo,[])
        if campo=='personagens' and not 4<=len(L)<=6: probs.append(f'{campo}: {len(L)} (4-6)')
        if campo=='lugares' and L and not 4<=len(L)<=6: probs.append(f'{campo}: {len(L)} (4-6)')
        for nome,_ in L:
            ws=[w for w in bib.norm(nome).split() if len(w)>3 and w not in ('mulher','homem','jovem','terra','cidade','monte','casa','povo','filho','filha','filhos','pai','mãe','rei','templo')]
            miss=[w for w in ws if ' '+w not in ' '+txt]
            if miss: probs.append(f'{campo} "{nome}": palavra(s) {miss} não aparecem no texto da semana (confira o nome na Bíblia Livre)')
    print(f'Semana {s["de"]}-{s["ate"]}:', '; '.join(probs) if probs else 'ok')

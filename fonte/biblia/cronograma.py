"""Monta o cronograma da Bíblia inteira (Bíblia Livre) em dias úteis.
Saída: dias.json (n, data, referência, minutos) e textos/NNN.json (capítulos e versículos de cada dia)."""
import json, ast, re, datetime as dt, os, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/src/bibialivrejson/biblialivre.json'
D = json.load(open(SRC, encoding='utf-8-sig'))
B = {}
for b in D[1:]:
    c = b['capitulos']; B[b['nome']] = ast.literal_eval(c) if isinstance(c, str) else c

# Ordem do estudo: alterna blocos do Novo e do Antigo Testamento
FASES = [
 ('Os Evangelhos', ['Mateus','Marcos','Lucas','João']),
 ('Os primeiros cristãos', ['Atos']),
 ('O começo de tudo', ['Gênesis','Êxodo']),
 ('As cartas de Paulo I', ['Romanos','1 Coríntios','2 Coríntios','Gálatas']),
 ('A Lei de Moisés', ['Levítico','Números','Deuteronômio']),
 ('As cartas de Paulo II', ['Efésios','Filipenses','Colossenses','1 Tessalonicenses','2 Tessalonicenses','Filemom']),
 ('A terra prometida', ['Josué','Juízes','Rute']),
 ('Os livros de sabedoria', ['Jó','Provérbios','Eclesiastes','Cantares']),
 ('Os reis de Israel', ['1 Samuel','2 Samuel','1 Reis','2 Reis']),
 ('As cartas de Paulo III', ['1 Timóteo','2 Timóteo','Tito','Hebreus']),
 ('Os Salmos', ['Salmos']),
 ('A volta do exílio', ['1 Crônicas','2 Crônicas','Esdras','Neemias','Ester']),
 ('As cartas de Tiago, Pedro, João e Judas', ['Tiago','1 Pedro','2 Pedro','1 João','2 João','3 João','Judas']),
 ('Os grandes profetas I', ['Isaías','Jeremias','Lamentações']),
 ('Os grandes profetas II', ['Ezequiel','Daniel']),
 ('Os doze profetas menores', ['Oséias','Joel','Amós','Obadias','Jonas','Miqueias','Naum','Habacuque','Sofonias','Ageu','Zacarias','Malaquias']),
 ('O Apocalipse', ['Apocalipse']),
]
assert sorted(x for _, l in FASES for x in l) == sorted(B), set(B) ^ {x for _, l in FASES for x in l}
NOME = {'Oséias': 'Oseias', 'Cantares': 'Cânticos'}   # nome mostrado no app
nm = lambda b: NOME.get(b, b)

def limpa(v):
    v = re.sub(r'\s+', ' ', v).strip()
    v = re.sub(r'\s+([,;:.!?])', r'\1', v)
    return v
def cw(b, c): return sum(len(v.split()) for v in B[b][c])

ALVO, MAX, MIN = 2400, 3300, 1100   # ~12 min (200 palavras/min), máx ~16 min
PEQ = 6000   # livro "pequeno": pode dividir o dia com outro livro
# Cortes manuais por tema (início de cada dia), quando o corte automático partiria um trecho conhecido
MANUAL = {'Mateus': [1, 5, 8, 11, 14, 18, 21, 24, 26]}
def particiona(items):
    """items: lista de (livro, cap, palavras). Programação dinâmica: dias perto de ALVO, nunca acima de MAX,
    e só mistura livros pequenos."""
    n = len(items); INF = float('inf'); best = [0] + [INF] * n; prev = [0] * (n + 1)
    for j in range(1, n + 1):
        w = 0; livros = []
        for i in range(j, 0, -1):
            it = items[i - 1]; w += it[2]
            if w > MAX and i < j: break
            if not livros or livros[-1] != it[0]: livros.insert(0, it[0])
            if len(livros) > 1 and any(TOT[x] > PEQ for x in livros): break
            if it[0] in MANUAL and i < j and any(items[k][1] in MANUAL[it[0]] for k in range(i, j) if items[k][0] == it[0]): break
            if it[0] in MANUAL and j < n and items[j][0] == it[0] and items[j][1] not in MANUAL[it[0]]: continue
            c = best[i - 1] + (w - ALVO) ** 2 + (4 * (MIN - w) ** 2 if w < MIN else 0)
            if c < best[j]: best[j] = c; prev[j] = i - 1
    out = []; j = n
    while j > 0:
        i = prev[j]; out.insert(0, items[i:j]); j = i
    return out
TOT = {b: sum(cw(b, c) for c in range(len(B[b]))) for b in B}
dias = []
for fi, (fase, livros) in enumerate(FASES, 1):
    items = [(b, c + 1, cw(b, c)) for b in livros for c in range(len(B[b]))]
    for g in particiona(items):
        segs = []
        for b, c, w in g:
            if segs and segs[-1]['livro'] == b: segs[-1]['ate'] = c
            else: segs.append({'livro': b, 'de': c, 'ate': c})
        dias.append({'fase': fi, 'faseNome': fase, 'segs': segs, 'palavras': sum(x[2] for x in g)})

def ref(seg):
    b = nm(seg['livro']); caps = len(B[seg['livro']])
    if caps == 1: return b
    return f"{b} {seg['de']}" + (f"–{seg['ate']}" if seg['ate'] != seg['de'] else '')
# feriados nacionais (mesma regra do Livro dos Espíritos: inclui Carnaval)
FER = {'2026-11-20','2026-12-25','2027-01-01','2027-02-08','2027-02-09','2027-03-26','2027-04-21','2027-05-27',
       '2027-09-07','2027-10-12','2027-11-02','2027-11-15','2027-12-25','2028-02-28','2028-02-29','2028-04-14',
       '2028-04-21','2028-05-01','2028-06-15','2028-09-07','2028-10-12','2028-11-02','2028-11-15','2028-11-20','2028-12-25'}
d = dt.date(2026, 11, 16)
os.makedirs('textos', exist_ok=True)
out = []
for i, dd in enumerate(dias, 1):
    while d.weekday() >= 5 or d.isoformat() in FER: d += dt.timedelta(1)
    caps_out = []
    for s in dd['segs']:
        b = s['livro']
        for c in range(s['de'], s['ate'] + 1):
            vs = [limpa(v) for v in B[b][c - 1]]; sobre = ''
            if b == 'Salmos':
                m = re.match(r'^(.{3,160}?:)(?=\S)', vs[0])
                if m and not re.search(r'[.!?]', m.group(1)[:-1]): sobre = m.group(1)[:-1]; vs[0] = vs[0][m.end():]
            caps_out.append({'l': nm(b), 'c': c, 'n': len(B[b]), **({'s': sobre} if sobre else {}), 'v': vs})
    json.dump(caps_out, open(f'textos/{i:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    out.append({'n': i, 'date': d.isoformat(), 'fase': dd['fase'], 'faseNome': dd['faseNome'],
                'ref': ' · '.join(ref(s) for s in dd['segs']), 'livro': nm(dd['segs'][0]['livro']),
                'mins': max(1, round(dd['palavras'] / 200)), 'segs': dd['segs']})
    d += dt.timedelta(1)
json.dump(out, open('dias.json', 'w'), ensure_ascii=False, indent=0)
for x in out: print(x['n'], x['date'], x['ref'], x['mins'])
print(len(out), 'dias; fim', out[-1]['date'], 'min', min(x['mins'] for x in out), 'max', max(x['mins'] for x in out))

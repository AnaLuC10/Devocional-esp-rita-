"""Uso: python3 texto.py N [N2 ...]  -> imprime o texto completo (Bíblia Livre) da leitura do Dia N, com números de versículo.
   ou: python3 texto.py "Lucas 2:1-7"  -> imprime uma referência."""
import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import bib
dias={d['n']:d for d in json.load(open(bib.R+'fonte/biblia/dias.json'))}
for a in sys.argv[1:]:
    if a.isdigit():
        d=dias[int(a)]; print(f"### Dia {d['n']} ({d['date']}) – {d['ref']}")
        for s in d['segs']:
            for c in range(s['de'],s['ate']+1):
                print(f"\n== {s['livro']} {c}")
                for i,v in enumerate(bib.CH[(s['livro'],c)]): print(f"{i+1} {v}")
    else:
        p=bib.parse(a)
        if not p: print('REFERÊNCIA INVÁLIDA:',a); continue
        print(f'== {a}')
        for b,c,v in p: print(f'{b} {c}:{v} {bib.CH[(b,c)][v-1]}')

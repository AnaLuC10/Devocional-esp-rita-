"""Gera o app Bíblia em ../../biblia/ (index.html, textos/, ícones e manifest).
Os comentários ficam em ../../biblia/comentarios.json e são lidos pelo app na hora (não precisa rodar este script pra atualizar)."""
import json, os, shutil, math
from PIL import Image, ImageDraw, ImageFilter
import cronograma as C  # noqa: roda o cronograma e gera dias.json + textos/
AQUI = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(AQUI, '..', '..', 'biblia')
os.makedirs(OUT, exist_ok=True)
dias = json.load(open(os.path.join(AQUI, 'dias.json')))
days = [{k: d[k] for k in ('n', 'fase', 'faseNome', 'ref', 'mins', 'livro')} for d in dias]
fases = [[f, ', '.join(C.nm(x) for x in l)] for f, l in C.FASES]
# índice da Bíblia inteira (ordem dos livros da Bíblia) e arquivo de busca
dia_de = {}
for d in dias:
    for sg in d['segs']:
        for c in range(sg['de'], sg['ate'] + 1): dia_de[(sg['livro'], c)] = d['n']
livros, busca = [], []
for b in C.D[1:]:
    nome = b['nome']; caps = C.B[nome]
    livros.append([C.nm(nome), b['abrev'].lower(), len(caps), 'AT' if b['periodo'].startswith('Antigo') else 'NT',
                   [dia_de[(nome, c + 1)] for c in range(len(caps))]])
    for c in range(len(caps)): busca.append([len(livros) - 1, c + 1, [C.limpa(v) for v in caps[c]]])
import guia_biblia as G
guia = {'grupos': G.GRUPOS, 'resumos': G.RESUMOS, 'linha': G.LINHA, 'lembrar': G.LEMBRAR, 'conversa': G.CONVERSA}
data = json.dumps({'days': days, 'fases': fases, 'livros': livros, 'guia': guia}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = open(os.path.join(AQUI, 'app_biblia.html')).read().replace('__DATA__', data)
open(os.path.join(OUT, 'index.html'), 'w').write(html)
if os.path.exists(os.path.join(OUT, 'textos')): shutil.rmtree(os.path.join(OUT, 'textos'))
shutil.copytree(os.path.join(AQUI, 'textos'), os.path.join(OUT, 'textos'))
json.dump(busca, open(os.path.join(OUT, 'busca.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
if not os.path.exists(os.path.join(OUT, 'comentarios.json')): open(os.path.join(OUT, 'comentarios.json'), 'w').write('{}')

# ícone: aura terracota / azul / trigo com um livro aberto em branco
def icone(sz):
    S = sz * 4; im = Image.new('RGB', (S, S), (240, 226, 214)); L = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    for (cx, cy, col) in [(.18, .2, (226, 150, 120)), (.88, .38, (130, 178, 206)), (.42, .98, (238, 204, 140))]:
        r = S * .75
        d.ellipse([cx * S - r, cy * S - r, cx * S + r, cy * S + r], fill=col + (235,))
    L = L.filter(ImageFilter.GaussianBlur(S * .16)); im.paste(L, (0, 0), L)
    W = Image.new('RGBA', (S, S), (0, 0, 0, 0)); dw = ImageDraw.Draw(W)
    r = S * .3; dw.ellipse([S/2 - r, S/2 - r, S/2 + r, S/2 + r], fill=(255, 255, 255, 120))
    W = W.filter(ImageFilter.GaussianBlur(S * .08)); im.paste(W, (0, 0), W)
    d = ImageDraw.Draw(im); w = int(S * .028); c = (255, 255, 255); cx, cy = S / 2, S * .53
    for s in (-1, 1):   # duas páginas
        pts = []
        for i in range(21):
            t = i / 20; x = cx + s * S * .27 * t; y = cy - S * .17 - S * .045 * math.sin(math.pi * t) * (1 - t * .3)
            pts.append((x, y))
        bot = [(cx + s * S * .27 * t, cy + S * .17 - S * .03 * math.sin(math.pi * t)) for t in [i / 20 for i in range(21)]]
        d.line(pts, fill=c, width=w, joint='curve'); d.line(bot, fill=c, width=w, joint='curve')
        d.line([pts[-1], bot[-1]], fill=c, width=w)
    d.line([(cx, cy - S * .17), (cx, cy + S * .17)], fill=c, width=w)
    return im.resize((sz, sz), Image.LANCZOS)
for sz in (180, 192, 512): icone(sz).save(os.path.join(OUT, f'icone-{sz}.png'))
json.dump({'name': 'Bíblia', 'short_name': 'Bíblia', 'start_url': './', 'scope': './', 'display': 'standalone',
           'background_color': '#FBF7F2', 'theme_color': '#FBF7F2', 'lang': 'pt-BR',
           'icons': [{'src': 'icone-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icone-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
          open(os.path.join(OUT, 'manifest.webmanifest'), 'w'), ensure_ascii=False, indent=1)
print('ok', os.path.getsize(os.path.join(OUT, 'index.html')), 'bytes')

import json, re, html, datetime as dt
import art_aura as art
from content import D, ESE_TIT
from musicas import M, PLAYLISTS
import biblia
from explicacoes import E as EXPL

days = json.load(open('days.json'))
extras = json.load(open('extras.json'))
FONT = 'node_modules/@fontsource'

MESES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
SEMANA = ['segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado','domingo']
ROM = ['','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
PARTS = {'1':('Parte Primeira','Das causas primárias'),'2':('Parte Segunda','Do mundo espírita ou mundo dos Espíritos'),
         '3':('Parte Terceira','Das leis morais'),'4':('Parte Quarta','Das esperanças e consolações'),'5':('Conclusão','')}
EPIGRAFE = {
 '1':'“Deus é a inteligência suprema, causa primária de todas as coisas.” — Q. 1',
 '2':'“O mundo espírita é o mundo normal, primitivo, eterno, preexistente e sobrevivente a tudo.” — Q. 85',
 '3':'“A lei natural é a lei de Deus. É a única verdadeira para a felicidade do homem.” — Q. 614',
 '4':'“Fora da caridade não há salvação.” — O Evangelho segundo o Espiritismo, cap. XV',
 '5':'“Espíritas! amai-vos, este o primeiro ensinamento; instruí-vos, este o segundo.”'}

SHOW_EOS = 'https://open.spotify.com/show/63GI6olEwQJFopaCeaZeHq'
SHOW_30 = 'https://open.spotify.com/show/5j5J0b4kv8DHTFCtkdG7EL'
EP = 'https://open.spotify.com/episode/'
KNOWN = [  # (q_ini, q_fim, titulo, id)
 (1,3,'021 – Cap. I: Deus – Questões 1 a 3 (23 min)','1gZFGrDxfCbekLBF2mhlPQ'),
 (4,9,'022 – Cap. I: Deus – Questões 4 a 9 (21 min)','3QyMcwW4lwkB3tXMKpZroP'),
 (10,13,'023 – Cap. I: Deus – Questões 10 a 13 (29 min)','1zklLEMNqL8ygoOhqKKKzn'),
 (14,16,'024 – Cap. I: Deus – Questões 14 a 16 (18 min)','1EMF2abWGqeXA33GwsN6mw'),
 (682,683,'235 – Lei do trabalho – Q. 682 a 683','3yB0sPPLqNdILqwJ7LpY9a'),
 (686,692,'236 – Lei de reprodução – Q. 686 a 692','0earjKPp4neWGYjlaGvD8U'),
 (693,701,'237 – Lei de reprodução – Q. 693 a 701','6OSrXovWfjq1ramI2TNvp5'),
 (702,707,'238 – Lei de conservação – Q. 702 a 707','2KDkcwu1FAWrS9sdZLjmqe'),
 (708,712,'239 – Lei de conservação – Q. 708 a 712','7ylbOm1knkgVoVFSlHXoOE'),
 (713,717,'240 – Lei de conservação – Q. 713 a 717','7BfInnnAXRh8fYHXA072km'),
 (718,723,'241 – Lei de conservação – Q. 718 a 723','0SiwHYP7TLefvhbBQ84mfy'),
 (724,728,'242 – Cap. V e VI – Q. 724 a 728','5vB2HYrEZ28khBmHAeVL8F'),
 (729,736,'243 – Lei de destruição – Q. 729 a 736','0hImsZkXzvnYUhjSgC2ods'),
 (737,741,'244 – Lei de destruição – Q. 737 a 741','0P6TubUx0QFdFqMKOzDlSD'),
 (742,751,'245 – Lei de destruição – Q. 742 a 751','2GlrLvghBUiYAkLllKC1TW'),
 (752,756,'246 – Lei de destruição – Q. 752 a 756','41eOmN960KW1eRFc9cUVFf'),
]
EOS_ATE = 756

def esc(s): return html.escape(s, quote=False)
EMOJI = re.compile('[☀-➿\U0001F300-\U0001FAFF️⃣⭐]')
XREF = {'(lde.2.07.04)':'(Veja-se: “Influência do organismo”, cap. VII, Parte 2ª.)',
        '(lde.2.7.04)':'(Vede nos 367 e seguintes — “Influência do organismo”.)',
        '(lde.3.12.3)':'(Vide: Egoísmo, cap. XII.)'}
def inline(s):
    for k, v in XREF.items(): s = s.replace(k, v)
    s = re.sub(r'^(>\s*)+', '', s.strip())
    s = EMOJI.sub('', s).replace('⚜', '')
    s = esc(s.strip())
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<em>\1</em>', s)
    s = re.sub(r'\s{2,}', ' ', s).replace('( ', '(')
    return s.strip()

def qnum(n):
    m = re.match(r'(\d+)(?:-([a-z]))?', n)
    return m.group(1) + (f' {m.group(2)})' if m.group(2) else '')

def qint(n): return int(re.match(r'\d+', n).group())

def datafmt(iso, longo=True):
    d = dt.date.fromisoformat(iso)
    return f'{SEMANA[d.weekday()]}, {d.day} de {MESES[d.month-1]}' if longo else f'{d.day:02d}/{d.month:02d}'

def part_key(p): return re.match(r'Parte (\d)', p).group(1)

# numeração dos capítulos por parte
chap_no = {}
for d in days:
    for s in d['segs']:
        pk = part_key(s['part'])
        if pk == '5': continue
        lst = chap_no.setdefault(pk, [])
        if s['chap'] not in lst: lst.append(s['chap'])
def chap_label(s):
    pk = part_key(s['part'])
    if pk == '5': return 'Conclusão'
    return f"Cap. {ROM[chap_no[pk].index(s['chap'])+1]} – {s['chap']}"

def is_sig(t):
    return bool(re.fullmatch(r'\*\*[^*]{2,60}\*\*\.?', t.strip()))

def render_item(it):
    if it['k'] == 'p':
        t = it['text']
        if is_sig(t): return f'<p class="sig">{inline(t)}</p>'
        cls = 'pq' if it.get('quote') else 'pr'
        return f'<p class="{cls}">{inline(t)}</p>'
    if not it['ans'] and not it['com']:
        return f'<p class="pr"><span class="qn">{qnum(it["num"])}.</span> {inline(it["text"])}</p>'
    o = [f'<div class="q"><p class="qt"><span class="qn">{qnum(it["num"])}.</span> {inline(it["text"])}</p>']
    if it['ans']:
        o.append('<div class="a">' + ''.join(
            f'<p class="sig">{inline(a)}</p>' if is_sig(a) else f'<p>{inline(a)}</p>' for a in it['ans']) + '</div>')
    if it['com']:
        o.append('<div class="com"><span class="lbl">comentário de Kardec</span>' + ''.join(
            f'<p class="sig">{inline(c)}</p>' if is_sig(c) else f'<p>{inline(c)}</p>' for c in it['com']) + '</div>')
    o.append('</div>')
    return ''.join(o)

def seg_title(s):
    t = s['sub'] or s['chap']
    t = re.sub(r'\s*\[\^\d+\]', '', t)
    t = re.sub(r'^Conclusão 0?(\d+)$', lambda m: 'Conclusão – ' + ROM_BIG(int(m.group(1))), t.strip())
    if s.get('part_no'): t += f' <span class="pn">(parte {s["part_no"][0]} de {s["part_no"][1]})</span>'
    return t

def podcast_html(d):
    if not d['q']:
        return ('<p>Para a Conclusão, um bom fechamento é o episódio mais recente da série '
                f'<a href="{SHOW_30}">Espiritismo em 30 minutos</a>, que estuda a Parte Quarta.</p>')
    a, b = qint(d['q'][0]), qint(d['q'][1])
    eps = [k for k in KNOWN if k[0] <= b and k[1] >= a]
    o = ''
    if eps:
        o += '<ul class="eps">' + ''.join(f'<li><a href="{EP}{k[3]}">{esc(k[2])}</a></li>' for k in eps) + '</ul>'
    if a > EOS_ATE:
        alt = (f' Enquanto isso, a série <a href="{SHOW_30}">Espiritismo em 30 minutos</a> já estuda a Parte Quarta.' if a >= 920 else '')
        o += (f'<p>A série da EOS Manaus ainda está gravando esta parte do livro (em novembro de 2026 ia na Q. {EOS_ATE}). '
              f'A mensagem da manhã traz o episódio do dia.{alt}</p>')
    else:
        if not eps or eps[0][0] > a or eps[-1][1] < b:
            o += (f'<p>Série <a href="{SHOW_EOS}">O Livro dos Espíritos – EOS Manaus</a>: procure os episódios '
                  f'com <strong>Q. {a} a {b}</strong> no título (cada um tem de 18 a 30 min).</p>')
    return o

def closing(d):
    n = d['n']; hoje, ese, liga = D[n]
    o = '<div class="closing"><div class="cl-top">' + art.svg(300, 30, '', '') + '</div>'
    o += f'<div class="blk"><div class="bh">{art.icon("flor")}<span>pra hoje</span></div><p>{esc(hoje)}</p></div>'
    if ese:
        cap, itens, top = ese
        o += (f'<div class="blk"><div class="bh">{art.icon("livro")}<span>no Evangelho</span></div>'
              f'<p class="ref">O Evangelho segundo o Espiritismo · cap. {cap} – <em>{esc(ESE_TIT[cap])}</em> · itens {itens} ({esc(top)})</p>'
              f'<p>{esc(liga)}</p></div>')
    bref, btxt = biblia.verso(n)
    o += (f'<div class="blk"><div class="bh">{art.icon("biblia")}<span>na Bíblia</span></div>'
          f'<p class="vs">“{esc(btxt)}”</p><p class="ref">{esc(bref)} · Bíblia Livre</p></div>')
    o += f'<div class="blk"><div class="bh">{art.icon("fone")}<span>podcast do dia</span></div>{podcast_html(d)}</div>'
    t, ar, g, tid = M[n-1]
    pl = PLAYLISTS[(n-1)//20]
    o += (f'<div class="blk"><div class="bh">{art.icon("nota")}<span>música do dia</span></div>'
          f'<p><a href="{EP.replace("episode","track")}{tid}"><strong>{esc(t)}</strong> – {esc(ar)}</a> <span class="tag">{g}</span></p>'
          f'<p class="ref">Também na <a href="https://open.spotify.com/playlist/3bJwoEHzmIxIKBF4450uU3">sua playlist do devocional</a>, no Spotify.</p></div>')
    return o + '</div>'

def day_meta(d):
    s0 = d['segs'][0]
    pk = part_key(s0['part'])
    if pk == '5': return 'Conclusão do livro'
    parte = PARTS[pk][0]
    q = f" · Questões {qint(d['q'][0])} a {qint(d['q'][1])}" if d['q'] and d['q'][0] != d['q'][1] else (f" · Questão {qint(d['q'][0])}" if d['q'] else '')
    return f'{parte} · {esc(chap_label(s0))}{q}'

def render_day(d):
    n = d['n']
    mins = max(1, round(d['words'] / 200))
    done = d.get('done')
    o = [f'<section class="day" id="dia-{n}">']
    o.append(f'<header class="dh" style="{art.aura_css(n)}">')
    o.append(f'<div class="dh-art">{art.mini((n-1) % 6, seed=n)}</div>')
    o.append(f'<div class="dh-txt"><div class="dn">Dia {n}</div>'
             f'<div class="dd">{datafmt(d["date"])}<span class="dot">·</span>≈ {mins} min de leitura</div></div>')
    o.append(f'<div class="chk{" ok" if done else ""}"><span class="box">{"✓" if done else ""}</span>lido</div>')
    o.append('</header>')
    if part_key(d['segs'][0]['part']) == '5':
        rr = [seg_title(s).split('– ')[1] for s in d['segs']]
        o.append(f'<h2 class="dt">Conclusão <span class=amp>·</span> itens {", ".join(rr[:-1])} e {rr[-1]}</h2>')
    else:
        o.append(f'<h2 class="dt">{" <span class=amp>&amp;</span> ".join(seg_title(s) for s in d["segs"])}</h2>')
    o.append(f'<div class="dm">{day_meta(d)}</div>')
    o.append(art.divider())
    multi = len(d['segs']) > 1
    for s in d['segs']:
        if multi:
            o.append(f'<h3 class="st">{seg_title(s)}</h3>')
        o.append(''.join(render_item(it) for it in s['items']))
        for nt in s.get('notes', []):
            o.append('<div class="nota"><span class="lbl">nota de Kardec</span>' + ''.join(f'<p>{inline(x)}</p>' for x in nt.split('\n') if x.strip()) + '</div>')
    o.append(closing(d))
    ex = EXPL[d['n']].strip().split('\n')
    o.append('<div class="simples"><div class="k sk">explicando de um jeito simples</div>' + ''.join(
        f'<p>{inline(x)}</p>' for x in ex if x.strip()) + '</div>')
    o.append(f'<p class="back"><a href="#cronograma">voltar ao cronograma</a></p></section>')
    return ''.join(o)

def part_opener(pk):
    t, sub = PARTS[pk]
    chs = chap_no.get(pk, [])
    lst = ''.join(f'<li><span>Cap. {ROM[i+1]}</span> {esc(c)}</li>' for i, c in enumerate(chs)) if chs else ''
    return (f'<section class="opener full" id="parte-{pk}" style="{art.aura_css(int(pk)+1)}">'
            f'<div class="op-k k">{esc(t)}</div><h1 class="op-t">{esc(sub) if sub else "Conclusão"}</h1>'
            f'<p class="op-e">{esc(EPIGRAFE[pk])}</p>'
            + (f'<ol class="op-l">{lst}</ol>' if lst else '') + '</section>')

def cronograma():
    o = ['<section class="crono" id="cronograma">' + art.corner_spray(9) + '<div class="k" style="color:var(--lav-d)">seu caminho</div><h1 class="h1">Crono<i>grama</i></h1>'
         '<p class="lead">Uma leitura por dia útil. Toque no tema para ir direto à página.</p>']
    mes = None
    o.append('<table>')
    for d in days:
        dd = dt.date.fromisoformat(d['date'])
        m = (dd.year, dd.month)
        if m != mes:
            mes = m
            o.append(f'<tr class="mes"><td colspan="4">{MESES[dd.month-1]} {dd.year}</td></tr>')
        q = f"Q. {qint(d['q'][0])}–{qint(d['q'][1])}" if d['q'] else 'Conclusão'
        tit = re.sub(r'\s*\[\^\d+\]', '', d['title'])
        if not d['q']:
            rr = [ROM_BIG(int(x)) for x in re.findall(r'Conclusão 0?(\d+)', tit)]
            tit = f'Conclusão – itens {", ".join(rr[:-1])} e {rr[-1]}'
        box = '<span class="box ok">✓</span>' if d.get('done') else '<span class="box"></span>'
        o.append(f'<tr><td class="c0">{box}</td><td class="c1"><b>{d["n"]}</b><br><span>{datafmt(d["date"], False)} {SEMANA[dd.weekday()][:3]}</span></td>'
                 f'<td class="c2"><a href="#dia-{d["n"]}">{esc(tit)}</a></td><td class="c3">{q}</td></tr>')
    o.append('</table>')
    o.append('<p class="lead small">Sem leitura nos fins de semana e nos feriados nacionais (20/11, 25/12, 1º/01, Carnaval). Se pular um dia, é só continuar de onde parou.</p>')
    o.append('<h2 class="h2">Leituras extras</h2><p class="lead small">A Introdução e os Prolegômenos de Kardec, para ler quando quiser.</p><table>')
    for i, e in enumerate(extras, 1):
        nm = ' + '.join(dict.fromkeys(s['sub'] or s['chap'] for s in e['segs']))
        nm = re.sub(r'Introdução (\d+)', lambda m: 'Intr. ' + ROM_BIG(int(m.group(1))), nm)
        o.append(f'<tr><td class="c0"><span class="box"></span></td><td class="c1"><b>E{i}</b></td><td class="c2"><a href="#extra-{i}">{esc(nm)}</a></td><td class="c3">{max(1,round(e["words"]/200))} min</td></tr>')
    o.append('</table></section>')
    return ''.join(o)

def ROM_BIG(n):
    vals = [(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]; r = ''
    for v, s in vals:
        while n >= v: r += s; n -= v
    return r

def render_extra(i, e):
    o = [f'<section class="day extra" id="extra-{i}"><header class="dh"><div class="dh-art">{art.mini((i+2) % 6, seed=i)}</div>'
         f'<div class="dh-txt"><div class="dn">Extra {i}</div><div class="dd">leitura livre · ≈ {max(1,round(e["words"]/200))} min</div></div>'
         '<div class="chk"><span class="box"></span>lido</div></header>']
    for s in e['segs']:
        t = s['sub'] or s['chap']
        t = re.sub(r'Introdução (\d+)', lambda m: 'Introdução – ' + ROM_BIG(int(m.group(1))), t)
        o.append(f'<h3 class="st"><span class="fl">❦</span> {esc(t)}</h3>')
        o.append(''.join(render_item(it) for it in s['items']))
        for nt in s.get('notes', []):
            o.append('<div class="nota"><span class="lbl">nota de Kardec</span>' + ''.join(f'<p>{inline(x)}</p>' for x in nt.split('\n') if x.strip()) + '</div>')
    o.append('<p class="back"><a href="#cronograma">voltar ao cronograma</a></p></section>')
    return ''.join(o)

CSS = open('style_aura.css').read().replace('{FONT}', FONT)
body = []
body.append(f'''<section class="cover full" style="{art.aura_css(0)}">
<div class="tl k">devocional espírita</div><div class="tr">♡</div>
<h1 class="cv-t">O livro<br>dos <i>Espíritos</i></h1>
<div class="cv-meta"><b>Allan Kardec</b><br>80 leituras · nov 2026 a mar 2027<br>tradução de Guillon Ribeiro</div>
<div class="cv-own">de Ana Luiza</div></section>''')
body.append(f'''<section class="guide">{art.corner_spray(4)}
<div class="k" style="color:var(--lav-d)">antes de começar</div><h1 class="h1">Como <i>usar</i></h1>
<div class="steps">
<div class="step"><div class="sn">1</div><div><b>De manhã, o podcast.</b> No carro, ouça o episódio indicado no fim de cada dia. A mensagem que chega às 6h36 traz o link certinho.</div></div>
<div class="step"><div class="sn">2</div><div><b>À noite, a leitura.</b> Cada dia tem o texto original do livro: as perguntas de Kardec, as respostas dos Espíritos (entre aspas) e os comentários de Kardec, nos quadrinhos lilás.</div></div>
<div class="step"><div class="sn">3</div><div><b>Pra fechar.</b> Uma ideia <i>pra hoje</i>, a ligação com <i>O Evangelho segundo o Espiritismo</i> e uma música do dia (gospel, católica, espírita ou MPB). As 80 músicas também estão na sua playlist do devocional no Spotify, na ordem dos dias.</div></div>
<div class="step"><div class="sn">4</div><div><b>Ficou difícil?</b> No fim de cada dia tem um trecho da Bíblia ligado ao tema e uma explicação simples, com as ideias principais em linguagem do dia a dia.</div></div>
<div class="step"><div class="sn">5</div><div><b>Marque o ♡.</b> Ticar o “lido” no topo de cada dia e no cronograma ajuda a ver o caminho.</div></div>
</div>
<div class="legend">
<div class="q"><p class="qt"><span class="qn">1.</span> Pergunta de Kardec</p><div class="a"><p>“Resposta dos Espíritos.”</p></div><div class="com"><span class="lbl">comentário de Kardec</span><p>Explicação que Kardec acrescentou.</p></div></div>
</div>
<p class="fine">Texto integral na tradução de Guillon Ribeiro (FEB – Federação Espírita Brasileira), em domínio público. As notas da editora foram deixadas de fora; as notas do próprio Kardec estão no fim de cada dia. Trechos bíblicos da Bíblia Livre (BLIVRE), sites.google.com/site/biblialivre – licença Creative Commons Atribuição 3.0 Brasil.</p>
{art.divider()}</section>''')
body.append(cronograma())
cur = None
for d in days:
    pk = part_key(d['segs'][0]['part'])
    if pk != cur:
        body.append(part_opener(pk)); cur = pk
    body.append(render_day(d))
body.append(f'''<section class="opener full" id="extras" style="{art.aura_css(4)}"><div class="op-k k">leituras extras</div>
<h1 class="op-t">Introdução e Prolegômenos</h1><p class="op-e">Kardec abre o livro explicando o que é o Espiritismo, as palavras novas que usa e como as respostas foram obtidas. Vale ler sem pressa.</p></section>''')
for i, e in enumerate(extras, 1):
    body.append(render_extra(i, e))
body.append(f'''<section class="final full" style="{art.aura_css(2)}"><div class="tl k">fim</div><div class="tr">♡</div><p class="fin">“Fora da caridade<br>não há salvação.”</p>
<p class="fin2">Parabéns por chegar até aqui.</p></section>''')

out = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>O Livro dos Espíritos · Devocional</title>
<style>{CSS}</style></head><body>{"".join(body)}</body></html>'''
open('devocional_aura.html', 'w').write(out)
print('ok', len(out))

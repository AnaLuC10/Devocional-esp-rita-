import json, re, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import build_aura as B
from content import D, ESE_TIT
from musicas import M
import biblia
from explicacoes import E as EXPL

def day_title(d):
    if B.part_key(d['segs'][0]['part']) == '5':
        rr = [B.seg_title(s).split('– ')[1] for s in d['segs']]
        return f'Conclusão · itens {", ".join(rr[:-1])} e {rr[-1]}'
    return ' <span class="amp">&amp;</span> '.join(B.seg_title(s) for s in d['segs'])

def short_title(d):
    t = re.sub(r'\s*\[\^\d+\]', '', d['title'])
    if not d['q']:
        rr = [B.ROM_BIG(int(x)) for x in re.findall(r'Conclusão 0?(\d+)', t)]
        t = f'Conclusão – itens {", ".join(rr[:-1])} e {rr[-1]}'
    return t

def body(segs, multi):
    o = []
    for s in segs:
        if multi:
            o.append(f'<h3 class="st">{B.seg_title(s)}</h3>')
        o.append(''.join(B.render_item(it) for it in s['items']))
        for nt in s.get('notes', []):
            o.append('<div class="nota"><span class="lbl">nota de Kardec</span>' + ''.join(
                f'<p>{B.inline(x)}</p>' for x in nt.split('\n') if x.strip()) + '</div>')
    return ''.join(o)

def pod_link(d):
    if not d['q']:
        return B.SHOW_30, 'Espiritismo em 30 minutos'
    a, b = B.qint(d['q'][0]), B.qint(d['q'][1])
    eps = [k for k in B.KNOWN if k[0] <= b and k[1] >= a]
    if eps:
        return B.EP + eps[0][3], eps[0][2]
    if a > B.EOS_ATE:
        return (B.SHOW_30, 'Espiritismo em 30 minutos') if a >= 920 else (B.SHOW_EOS, 'EOS Manaus · chega na mensagem da manhã')
    return B.SHOW_EOS, f'EOS Manaus · Q. {a} a {b}'

out = []
for d in B.days:
    n = d['n']
    hoje, ese, liga = D[n]
    bref, btxt = biblia.verso(n)
    t, ar, g, tid = M[n-1]
    pu, pl = pod_link(d)
    q = (f"Q. {B.qint(d['q'][0])}–{B.qint(d['q'][1])}" if d['q'][0] != d['q'][1] else f"Q. {B.qint(d['q'][0])}") if d['q'] else 'Conclusão'
    out.append(dict(
        n=n, date=d['date'], mins=max(1, round(d['words']/200)), done=bool(d.get('done')),
        part=B.part_key(d['segs'][0]['part']),
        title=day_title(d), short=B.esc(short_title(d)), meta=B.day_meta(d), q=q,
        body=body(d['segs'], len(d['segs']) > 1),
        hoje=B.esc(hoje),
        ese=(f'cap. {ese[0]} – <em>{B.esc(ESE_TIT[ese[0]])}</em> · {"itens" if re.search(r"[-–,e]", ese[1]) else "item"} {ese[1]} ({B.esc(ese[2])})' if ese else ''),
        liga=B.esc(liga) if ese else '',
        bib=B.esc(btxt), bref=B.esc(bref),
        pod=B.podcast_html(d), podUrl=pu, podLabel=B.esc(pl),
        mus=B.esc(t), art=B.esc(ar), gen=g, musUrl='https://open.spotify.com/track/' + tid,
        simples=''.join(f'<p>{B.inline(x)}</p>' for x in EXPL[n].strip().split('\n') if x.strip()),
    ))

extras = []
for i, e in enumerate(B.extras, 1):
    nm = ' + '.join(dict.fromkeys(s['sub'] or s['chap'] for s in e['segs']))
    nm = re.sub(r'Introdução (\d+)', lambda m: 'Introdução ' + B.ROM_BIG(int(m.group(1))), nm)
    segs = []
    for s in e['segs']:
        s2 = dict(s); t = s['sub'] or s['chap']
        s2['sub'] = re.sub(r'Introdução (\d+)', lambda m: 'Introdução – ' + B.ROM_BIG(int(m.group(1))), t)
        s2['part_no'] = None
        segs.append(s2)
    extras.append(dict(i=i, name=B.esc(nm), mins=max(1, round(e['words']/200)), body=body(segs, True)))

parts = {k: v for k, v in B.PARTS.items()}
data = json.dumps(dict(days=out, extras=extras, parts=parts, epi=B.EPIGRAFE), ensure_ascii=False, separators=(',', ':'))
data = data.replace('</', '<\\/')
tpl = open('app_template.html').read()
html_out = tpl.replace('__DATA__', data)
open('/tmp/claude-0/-home-claude/b4f831e8-c069-56fa-be06-9c3cbe10a026/scratchpad/devocional-app.html', 'w').write(html_out)
print('ok', len(html_out.encode()))

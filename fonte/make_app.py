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
        tema=B.esc(re.split(r'\s*\+\s*|\s*&\s*', short_title(d))[0].strip()),
        mus=B.esc(t), art=B.esc(ar), gen=g, musUrl='https://open.spotify.com/track/' + tid,
        simples=''.join(f'<p>{B.inline(x)}</p>' for x in EXPL[n].strip().split('\n') if x.strip()),
    ))

# ---------- leituras curtas (pedido de 26/11/2026: até ~6 perguntas por dia) ----------
import datetime as dt, math
QMAX, WMAX, SPLIT_FROM = 6, 1300, 17
def iwords(it):
    return len(' '.join([it.get('text') or ''] + list(it.get('ans') or []) + list(it.get('com') or [])).split())
def units_of(d):
    us = []
    for si, sg in enumerate(d['segs']):
        for ii, it in enumerate(sg['items']):
            sub = it['k'] == 'q' and '-' in str(it['num'])
            if sub and us and us[-1]['si'] == si:
                u = us[-1]; u['items'].append(ii); u['w'] += iwords(it)
            else:
                us.append(dict(si=si, items=[ii], q=1 if it['k'] == 'q' else 0, w=iwords(it)))
    return us
def cost(us):
    return max(sum(u['q'] for u in us) / QMAX, sum(u['w'] for u in us) / WMAX)
def best_split(us, m):
    n = len(us); INF = 9e9
    f = [[INF] * (n + 1) for _ in range(m + 1)]; cut = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 0
    for k in range(1, m + 1):
        for j in range(1, n + 1):
            for i in range(k - 1, j):
                v = max(f[k - 1][i], cost(us[i:j]))
                if v < f[k][j]: f[k][j] = v; cut[k][j] = i
    bounds = []; j = n
    for k in range(m, 0, -1):
        i = cut[k][j]; bounds.append((i, j)); j = i
    return f[m][n], bounds[::-1]
def split_tema(d):
    us = units_of(d)
    if d['n'] < SPLIT_FROM or len(us) <= 1: return [us]
    m = 1
    while m < len(us):
        v, b = best_split(us, m)
        if v <= 1.0001: break
        m += 1
    v, b = best_split(us, m)
    return [us[i:j] for i, j in b]
def part_body(d, us, multi):
    o = []; segs = d['segs']
    by = {}
    for u in us: by.setdefault(u['si'], []).extend(u['items'])
    first_si = us[0]['si']
    for si, idxs in by.items():
        sg = segs[si]
        cont = (si == first_si and idxs[0] != 0)
        if multi or cont:
            o.append(f'<h3 class="st">{B.seg_title(sg)}{" <span class=\"pn\">(continuação)</span>" if cont else ""}</h3>')
        o.append(''.join(B.render_item(sg['items'][i]) for i in idxs))
        if idxs[-1] == len(sg['items']) - 1:
            for nt in sg.get('notes', []):
                o.append('<div class="nota"><span class="lbl">nota de Kardec</span>' + ''.join(
                    f'<p>{B.inline(x)}</p>' for x in nt.split('\n') if x.strip()) + '</div>')
    return ''.join(o)
def qlabel(d, us):
    nums = [d['segs'][u['si']]['items'][i]['num'] for u in us for i in u['items'] if d['segs'][u['si']]['items'][i]['k'] == 'q']
    if not nums: return None
    a, b = B.qint(nums[0]), B.qint(nums[-1])
    return f'Q. {a}' if a == b else f'Q. {a}–{b}'
hol = {dt.date(2026,11,20),dt.date(2026,12,25),dt.date(2027,1,1),dt.date(2027,2,8),dt.date(2027,2,9),dt.date(2027,3,26),
       dt.date(2027,4,21),dt.date(2027,5,27),dt.date(2027,9,7),dt.date(2027,10,12),dt.date(2027,11,2),dt.date(2027,11,15),
       dt.date(2027,12,25),dt.date(2028,1,1),dt.date(2028,2,28),dt.date(2028,2,29)}
def next_wd(x):
    x += dt.timedelta(days=1)
    while x.weekday() > 4 or x in hol: x += dt.timedelta(days=1)
    return x
START = dt.date(2026, 11, 26)
leit = []; cur = None
for d, o in zip(B.days, out):
    parts = split_tema(d)
    o['np'] = len(parts)
    for k, us in enumerate(parts, 1):
        if d['n'] < SPLIT_FROM: date = d['date']
        else:
            cur = START if cur is None else next_wd(cur); date = cur.isoformat()
        multi = len(d['segs']) > 1
        ql = qlabel(d, us) or ('Conclusão' if not d['q'] else o['q'])
        w = sum(u['w'] for u in us)
        leit.append(dict(i=len(leit) + 1, t=d['n'], k=k, m=len(parts), date=date, q=ql,
                         mins=max(1, round(w / 200)), body=o['body'] if len(parts) == 1 else part_body(d, us, multi)))
for o in out: o.pop('body', None)
print('leituras', len(leit), 'fim', leit[-1]['date'], file=__import__('sys').stderr)

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
data = json.dumps(dict(days=out, leit=leit, extras=extras, parts=parts, epi=B.EPIGRAFE), ensure_ascii=False, separators=(',', ':'))
data = data.replace('</', '<\\/')
tpl = open('app_template.html').read()
html_out = tpl.replace('__DATA__', data)
open('/tmp/claude-0/-home-claude/b4f831e8-c069-56fa-be06-9c3cbe10a026/scratchpad/devocional-app.html', 'w').write(html_out)
print('ok', len(html_out.encode()))

import json,re
B=json.load(open('blocks.json'))
# --- fixes ---
for b in B:
    if b['t']=='q':
        if b['line']==2744: b['label']='330. a)'
        pn=b.get('pdfnum')
        if pn and pn!='NF' and b['line']!=1741 and re.fullmatch(r'\d+',pn) and re.sub(r'\D','',b['label'])!=pn and not re.search(r'[a-z]\)',b['label']):
            b['label']=pn+'.'
# 323
for i,b in enumerate(B):
    if b['t']=='p' and b['text'].startswith('*323*'):
        B[i]={'t':'q','label':'323.','text':'A visita de uma pessoa a um túmulo causa maior contentamento ao Espírito, cujos despojos corporais aí se encontrem, do que a prece que por ele faça em casa o visitante?','line':b['line']}
# 889 insert before heading 'Amor materno e filial'
for i,b in enumerate(B):
    if b['t']=='h' and b['title'].startswith('Amor materno'):
        B[i:i]=[{'t':'q','label':'889.','text':'Não há homens que se veem condenados a mendigar por culpa sua?','line':0},
                {'t':'ans','text':'“Sem dúvida; mas, se uma boa educação moral lhes houvera ensinado a praticar a lei de Deus, não teriam caído nos excessos causadores da sua perdição. Disso, sobretudo, é que depende a melhoria do vosso planeta.” (707)','line':0}]
        break
def clean(s):
    s=re.sub(r'\(\s*lde\.q(\d+[a-z]?)\s*\)',r'(\1)',s)
    s=re.sub(r'lde\.q(\d+)([a-z]?)',lambda m:m.group(1)+('-'+m.group(2) if m.group(2) else ''),s)
    s=s.replace('Lei divin.a','Lei divina').replace('<br />','').replace('<br/>','')
    s=re.sub(r'\s*❦\s*$','',s)
    s=re.sub(r'`[^`]*`\s*(#️⃣)?\s*','',s)
    return s.strip()
# --- footnotes ---
fns={}; last=None
for b in B:
    if b['t']=='fn':
        m=re.match(r'\[\^(\d*)\]:?\s*(.*)',b['text'])
        if m.group(1): last=m.group(1); fns[last]=m.group(2)
        elif last: fns[last]+='\n'+m.group(2)
akfn={k:re.sub(r'^(Nota de Allan Kardec \(A\.K\.\)|A\.K\.?)\s*:?\s*','',v) for k,v in fns.items() if v.startswith('A.K') or v.startswith('Nota de Allan Kardec')}
# --- structure ---
units=[]; part=chap=None; cur=None; lastmain=None
def newunit(title,kind):
    global cur
    cur={'part':part,'chap':chap,'sub':title,'kind':kind,'items':[],'notes':[]}; units.append(cur)
for b in B:
    t=b['t']
    if t=='h':
        lvl=b['lvl']; title=re.sub(r'^\d+\.\s*','',b['title']).strip()
        if lvl==2: part=title; chap=None; cur=None
        elif lvl==3:
            chap=title; cur=None
            # chapters w/o subtitles get a unit named after chapter
            newunit(None,'chap')
        elif lvl==4: newunit(title,'sub')
        continue
    if t=='fn' or cur is None: continue
    text=b['text']
    refs=re.findall(r'\[\^(\d+)\]',text)
    for r in refs:
        if r in akfn and akfn[r] not in cur['notes']: cur['notes'].append(akfn[r])
    text=re.sub(r'\[\^\d*\]:?,?','',text); text=clean(text)
    if not text: continue
    if t=='q':
        lab=b['label'].strip()
        m=re.match(r'(\d+)\s*\.?\s*(?:([a-z])\))?',lab)
        if m.group(2) and lastmain: num=lastmain+'-'+m.group(2)
        else: num=m.group(1)+(('-'+m.group(2)) if m.group(2) else '')
        if not m.group(2): lastmain=m.group(1)
        cur['items'].append({'k':'q','num':num,'text':text,'ans':[],'com':[]})
    elif t=='ans':
        if cur['items'] and cur['items'][-1]['k']=='q' and not cur['items'][-1]['com']:
            cur['items'][-1]['ans'].append(text)
        elif cur['items'] and cur['items'][-1]['k']=='q':
            cur['items'][-1]['com'].append(text)
        else: cur['items'].append({'k':'p','text':text,'quote':True})
    elif t=='com':
        if cur['items'] and cur['items'][-1]['k']=='q': cur['items'][-1]['com'].append(text)
        else: cur['items'].append({'k':'p','text':text,'quote':True})
    else:
        cur['items'].append({'k':'p','text':text})
units=[u for u in units if u['items']]
for u in units:
    w=0
    for it in u['items']:
        w+=len(it['text'].split())+sum(len(x.split()) for x in it.get('ans',[])+it.get('com',[]))
    w+=sum(len(n.split()) for n in u['notes'])
    u['words']=w
    qs=[it['num'] for it in u['items'] if it['k']=='q']
    u['qrange']=(qs[0].split('-')[0],qs[-1].split('-')[0]) if qs else None
json.dump(units,open('units.json','w'),ensure_ascii=False,indent=1)
for i,u in enumerate(units): print(i,u['part'][:18] if u['part'] else None,'|',(u['chap'] or '')[:35],'|',(u['sub'] or '')[:40],'|',u['qrange'],u['words'])
print(sum(u['words'] for u in units))

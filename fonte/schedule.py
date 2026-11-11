import json,datetime as dt
U=json.load(open('units.json'))
MIN,MAX,SPLIT=1000,4000,3200
# main units: parts 1-5
main=[u for u in U if u['part'] and not u['part'].startswith('Parte 0')]
intro=[u for u in U if u['part'] and u['part'].startswith('Parte 0') and u['chap']!='Folha de rosto']
def iw(it): return len(it['text'].split())+sum(len(x.split()) for x in it.get('ans',[])+it.get('com',[]))
def split_unit(u):
    if u['words']<=MAX: return [dict(u,part_no=None)]
    n=-(-u['words']//SPLIT); target=u['words']/n
    chunks=[[]];w=0
    for it in u['items']:
        if w>=target and len(chunks)<n: chunks.append([]); w=0
        chunks[-1].append(it); w+=iw(it)
    out=[]
    for i,c in enumerate(chunks):
        out.append(dict(u,items=c,words=sum(iw(x) for x in c),notes=u['notes'] if i==len(chunks)-1 else [],part_no=(i+1,len(chunks))))
    return out
def chapkey(u): return (u['part'],u['chap'] if not u['part'].startswith('Parte 5') else 'Conclusão')
# group by chapter
groups=[]
for u in main:
    k=chapkey(u)
    if not groups or groups[-1][0]!=k: groups.append((k,[]))
    groups[-1][1].extend(split_unit(u))
days=[]
for k,us in groups:
    cd=[]
    for u in us:
        if cd and cd[-1]['words']<MIN and cd[-1]['words']+u['words']<=MAX and not u.get('part_no') and not cd[-1]['segs'][-1].get('part_no'):
            cd[-1]['segs'].append(u); cd[-1]['words']+=u['words']
        else: cd.append({'segs':[u],'words':u['words']})
    if len(cd)>1 and cd[-1]['words']<600 and cd[-2]['words']+cd[-1]['words']<=MAX and not cd[-1]['segs'][0].get('part_no'):
        cd[-2]['segs']+=cd[-1]['segs']; cd[-2]['words']+=cd[-1]['words']; cd.pop()
    days+=cd
# already-done days (Q1-3 / Q4-13 / Q14-16) -> override first chapter grouping
done=[(['Deus e o infinito'],'2026-11-04'),(['Provas da existência de Deus','Atributos da Divindade'],'2026-11-04'),(['Panteísmo'],'2026-11-05')]
first=[d for d in days if d['segs'][0]['chap']=='De Deus']
rest=[d for d in days if d['segs'][0]['chap']!='De Deus']
segs={s['sub']:s for d in first for s in d['segs']}
newfirst=[]
for subs,date in done:
    ss=[segs[x] for x in subs]; newfirst.append({'segs':ss,'words':sum(s['words'] for s in ss),'date':date,'done':True})
days=newfirst+rest
# dates
hol={dt.date(2026,11,20),dt.date(2026,12,25),dt.date(2027,1,1),dt.date(2027,2,8),dt.date(2027,2,9),dt.date(2027,3,26),dt.date(2027,4,21),dt.date(2027,5,27),dt.date(2027,9,7),dt.date(2027,10,12),dt.date(2027,11,2),dt.date(2027,11,15)}
d=dt.date(2026,11,6)
for day in days:
    if day.get('date'): continue
    while d.weekday()>=5 or d in hol: d+=dt.timedelta(1)
    day['date']=d.isoformat(); d+=dt.timedelta(1)
for i,day in enumerate(days,1):
    day['n']=i
    qs=[it['num'] for s in day['segs'] for it in s['items'] if it['k']=='q']
    day['q']=(qs[0],qs[-1]) if qs else None
    day['title']=' + '.join((s['sub'] or s['chap'])+(f" – parte {s['part_no'][0]}" if s.get('part_no') else '') for s in day['segs'])
json.dump(days,open('days.json','w'),ensure_ascii=False)
# intro extras
ex=[];cur=None
for u in intro:
    if cur is None or cur['words']+u['words']>2600: cur={'segs':[],'words':0}; ex.append(cur)
    cur['segs'].append(u); cur['words']+=u['words']
json.dump(ex,open('extras.json','w'),ensure_ascii=False)
for day in days: print(day['n'],day['date'],day['q'],day['words'],round(day['words']/200,1),day['title'][:90])
print('extras',[e['words'] for e in ex])

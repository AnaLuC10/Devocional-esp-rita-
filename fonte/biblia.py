import json, re, ast
_D = json.load(open('/home/claude/eversondeveloper/bibialivrejson/biblialivre.json', encoding='utf-8-sig'))
BOOKS = {}
for b in _D[1:]:
    caps = b['capitulos']
    if isinstance(caps, str): caps = ast.literal_eval(caps)
    BOOKS[b['nome']] = caps
# dia: (livro, capítulo, v_ini, v_fim)
REFS = {
1:('Isaías',55,8,9), 2:('Salmos',19,1,2), 3:('Romanos',11,33,34), 4:('1 Coríntios',13,12,12),
5:('Gênesis',1,1,3), 6:('João',14,2,2), 7:('Gênesis',2,7,7), 8:('Hebreus',12,9,9),
9:('1 Coríntios',15,40,44), 10:('1 João',4,1,1), 11:('Mateus',5,48,48), 12:('Hebreus',1,14,14),
13:('Eclesiastes',3,1,2), 14:('Mateus',6,19,21), 15:('Eclesiastes',12,7,7), 16:('João',3,3,7),
17:('Filipenses',3,13,14), 18:('Mateus',12,48,50), 19:('Jeremias',1,5,5), 20:('Mateus',17,11,13),
21:('2 Coríntios',5,1,1), 22:('Lucas',16,24,25), 23:('1 Coríntios',2,9,9), 24:('1 Coríntios',10,13,13),
25:('Mateus',23,12,12), 26:('1 Coríntios',13,4,7), 27:('João',11,25,26), 28:('Salmos',139,13,14),
29:('Mateus',26,41,41), 30:('Marcos',10,14,15), 31:('Isaías',43,18,19), 32:('Jó',33,14,16),
33:('Hebreus',12,1,1), 34:('2 Coríntios',12,2,3), 35:('Atos',2,17,17), 36:('Filipenses',4,8,8),
37:('Marcos',9,28,29), 38:('Salmos',91,11,12), 39:('Provérbios',16,9,9), 40:('Marcos',4,39,41),
41:('Romanos',12,14,14), 42:('1 Coríntios',12,4,6), 43:('Provérbios',12,10,10), 44:('1 Coríntios',15,39,39),
45:('Romanos',2,14,15), 46:('Mateus',7,12,12), 47:('João',4,23,24), 48:('Oséias',6,6,6),
49:('João',5,17,17), 50:('Mateus',19,5,6), 51:('Mateus',6,26,26), 52:('1 Timóteo',6,7,8),
53:('Romanos',8,18,18), 54:('Mateus',26,52,52), 55:('João',8,7,7), 56:('Eclesiastes',4,9,10),
57:('Marcos',4,28,28), 58:('Mateus',9,12,12), 59:('Mateus',5,14,16), 60:('Gálatas',3,28,28),
61:('Mateus',19,23,24), 62:('João',8,32,32), 63:('Deuteronômio',30,19,19), 64:('Mateus',6,34,34),
65:('Efésios',4,28,28), 66:('1 Coríntios',13,1,3), 67:('Gálatas',5,22,23), 68:('Filipenses',2,3,4),
69:('Lamentações',3,40,40), 70:('Filipenses',4,11,12), 71:('1 Tessalonicenses',4,13,14), 72:('Mateus',11,28,30),
73:('Mateus',16,27,27), 74:('Lucas',15,20,20), 75:('Ezequiel',18,23,23), 76:('Lucas',17,20,21),
77:('João',14,15,17), 78:('Mateus',7,16,17), 79:('João',16,12,13), 80:('João',13,34,35),
}
def verso(n):
    b, c, a, z = REFS[n]
    vs = BOOKS[b][c-1][a-1:z]
    txt = ' '.join(re.sub(r'\s+', ' ', v).strip() for v in vs)
    txt = re.sub(r'^Salmo de Davi, para o regente:\s*', '', txt)
    txt = re.sub(r'\s+([,;:.!?])', r'\1', txt)
    txt = re.sub(r'([,;:?!])(?=[^\s”»)])', r'\1 ', txt)
    txt = txt.replace('? , diz o Senhor DEUS, E não', ', diz o Senhor DEUS, e não')
    ref = f'{b} {c}:{a}' + (f'–{z}' if z != a else '')
    return ref, txt

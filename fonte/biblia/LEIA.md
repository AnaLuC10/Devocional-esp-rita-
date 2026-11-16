# App Bíblia (na visão espírita)

Site: https://analuc10.github.io/Devocional-esp-rita-/biblia/

- A Bíblia inteira em 292 leituras de 9 a 15 minutos, SEM DATAS (a Ana lê no ritmo dela; o app abre sempre na próxima leitura que falta). As datas de `dias.json` ficaram só como referência interna e não aparecem no app. A ordem é alternando blocos do Novo e do Antigo Testamento (ordem em `cronograma.py`, lista FASES).
- Cada dia tem: texto integral da Bíblia Livre (BLIVRE, CC BY 3.0 BR), a explicação na visão espírita, o "pra hoje" e o "pra aprofundar" (obras de Kardec). Sem música e sem podcast (pedido da Ana em 15/11/2026).
- Aba "Bíblia": todos os livros e capítulos e busca por referência (João 3:16, 1 Co 13, Judas 3) ou por palavras, sem acento e sem diferenciar maiúsculas. A busca lê `/biblia/busca.json` (Bíblia inteira), baixado só na primeira busca.
- Texto: github.com/eversondeveloper/bibialivrejson, arquivo biblialivre.json.

## Arquivos
- `cronograma.py`: divide a Bíblia em dias e gera `dias.json` e `textos/NNN.json`.
- `app_biblia.html`: o app (uma página). `make_biblia.py` gera `/biblia/` (index.html, textos, ícones, manifest).
- `/biblia/comentarios.json`: a visão espírita de cada dia, lida pelo app na hora. Para acrescentar dias, basta editar esse arquivo (não precisa rodar nada).
  Formato: `{"15": {"titulo": "...", "chave": "Lucas 2:52", "kardec": "...", "explicacao": "parágrafos separados por \n, **negrito**, termina em **Resumindo:** ...", "hoje": "..."}}`.
  - `chave` é o versículo-chave: "Livro cap:v" ou "Livro cap:v-v", com o nome do livro igual ao do app (ex.: Oseias, Cânticos). Precisa estar dentro da leitura do dia.
  - Um parágrafo que começa com `**Pra conversar:**` vira um quadro: como as igrejas evangélicas costumam ler o trecho e como o Espiritismo lê, com respeito.
- `comentarios_mateus_marcos.py`: os Dias 1–14 (Mateus e Marcos).

## Cartões de etapa ("Sua jornada", na aba Guia)
- Ficam em `/biblia/guia-semanal.json`: `{"semanas": [{"de": 1, "ate": 4, "titulo": "...", "ref": "Mateus 1–13", "resumo": "...", "personagens": [["Nome", "quem é / o que faz"], ...], "lugares": [["Lugar", "o que acontece lá"], ...], "ideia": "a ideia espírita da semana (aceita **negrito**)", "chave": "Mateus 5:3-12"}]}`.
- Uma etapa = um bloco de leituras seguidas (`de` = 1ª, `ate` = última). As primeiras são 1–4, 5–9 e 10–14; daí em diante, blocos de 5 (15–19, 20–24…), ajustando ±1 pra não partir um livro no meio quando der. 4 a 6 personagens e 4 a 6 lugares, todos que aparecem de fato no texto daquela etapa.
- O cartão só aparece pra quem já marcou como lida a leitura `ate`.

## Devocional d'O Livro dos Espíritos: cartões semanais
- Ficam em `/jornada.json` (raiz do site): `{"semanas": [{"de": 1, "ate": 4, "titulo": "...", "q": "Q. 1 a 36", "resumo": "...", "conceitos": [["termo", "explicação curta"], ...], "frase": ["trecho literal do livro", "Q. 1"], "evangelho": "ligação com o Evangelho"}]}`.
- Uma semana = os dias do cronograma (com data) de segunda a sexta da mesma semana do calendário. O cartão aparece pra quem marcou o dia `ate`.

# App Bíblia (as duas visões)

Site: https://analuc10.github.io/Devocional-esp-rita-/biblia/

Leitura em casal (pedido de 16/11/2026): a Ana lê no app e o namorado lê na Bíblia de papel dele, marcando. Cada dia mostra a passagem em destaque e as duas visões, a espírita e a evangélica, do mesmo tamanho e com o mesmo cuidado. A visão evangélica segue a leitura evangélica mais comum, com atenção às igrejas em células e pentecostais (ele é da Igreja Videira, de Goiânia).

- A Bíblia inteira em 441 leituras (2 a 3 capítulos, ~8 min de texto, pra ler antes de dormir), uma por dia útil, de 13/11/2026 a 16/08/2028 (o Dia 1 ficou em 13/11 porque a Ana já tinha lido Mateus 1–4), sem fins de semana e feriados nacionais (lista FER em `cronograma.py`). A ordem alterna blocos do Novo e do Antigo Testamento (lista FASES).
- Texto: Bíblia Livre (BLIVRE, CC BY 3.0 BR), github.com/eversondeveloper/bibialivrejson, arquivo biblialivre.json. Quem lê no papel pode esconder o texto no app.
- Aba "Bíblia": todos os livros e capítulos, com resumo de cada livro, e busca por referência ou palavras. A busca lê `/biblia/busca.json`.
- Aba "Guia": como ler, a biblioteca, linha do tempo, pra sempre lembrar, pra conversar, cartões semanais e como usar (conteúdo fixo em `guia_biblia.py`).

## Arquivos
- `cronograma.py`: divide a Bíblia e gera `dias.json` e `textos/NNN.json`. `app_biblia.html`: o app. `make_biblia.py` gera `/biblia/`.
- `/biblia/comentarios.json`: o conteúdo de cada dia, lido pelo app na hora (pra acrescentar dias, basta editar esse arquivo). Modelo de estilo, tamanho e tom: `comentarios_inicio.py` (Dias 1–6) e `comentarios_mes1.py` (Dias 7–22). Frases entre aspas citadas da Bíblia seguem a redação da Bíblia Livre. Campos:
  - `titulo`; `chave` (versículo-chave "Livro cap:v" ou "Livro cap:v-v", com o nome do livro igual ao do app e dentro da leitura); `resumo` (o que acontece, neutro, 1–2 frases);
  - `espirita` e `evangelica` (4 a 6 parágrafos curtos cada, separados por \n, uns 130 a 230 palavras cada, **negrito** nas ideias principais, cada visão explicada por dentro, como quem acredita nela explicaria);
  - `comum` (o que as duas têm em comum, 1–3 frases); `hoje` (aplicação pros dois); `marcar` ([[referência, o que é]], 3 ou 4 passagens ligadas); `kardec` (aprofundar espírita); `estudo` (aprofundar evangélica).
- `/biblia/guia-semanal.json`: cartões "Sua jornada", um por semana do calendário: `{"semanas": [{"de", "ate", "titulo", "ref", "resumo", "personagens": [[nome, quem é]], "lugares": [[lugar, o que acontece]], "espirita", "evangelica", "chave"}]}`. O cartão aparece pra quem marcou como lido o dia `ate`.

## Devocional d'O Livro dos Espíritos: cartões semanais
- Ficam em `/jornada.json` (raiz do site): `{"semanas": [{"de": 1, "ate": 4, "titulo": "...", "q": "Q. 1 a 36", "resumo": "...", "conceitos": [["termo", "explicação curta"], ...], "frase": ["trecho literal do livro", "Q. 1"], "evangelho": "ligação com o Evangelho"}]}`.
- Uma semana = os dias do cronograma (com data) de segunda a sexta da mesma semana do calendário. O cartão aparece pra quem marcou o dia `ate`.

## Devocional: quadro "outros olhares" no versículo do dia
- Fica em `/conversar.json` (raiz): `{"10": "texto"}`, chave = número do dia do devocional. 3 a 5 frases: como outras tradições cristãs em geral (sem citar uma igreja específica) costumam ler o versículo do dia (campos `bib`/`bref` do JSON do index.html), como o Espiritismo lê, e em que todos concordam. O devocional é usado pela família toda: o tom é de estudo, não de debate.

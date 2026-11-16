# App Bíblia (na visão espírita)

Site: https://analuc10.github.io/Devocional-esp-rita-/biblia/

- A Bíblia inteira em 292 dias úteis (16/11/2026 a 13/01/2028), de 9 a 15 minutos por dia, alternando blocos do Novo e do Antigo Testamento (ordem em `cronograma.py`, lista FASES).
- Sem leitura em fins de semana e feriados nacionais (lista FER em `cronograma.py`).
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

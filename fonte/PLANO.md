# Plano do devocional espírita

Ordem dos livros (escolhida pela Ana em 10/11/2026):

1. **O Livro dos Espíritos**: 80 dias úteis, de 04/11/2026 a 01/03/2027 (pronto)
2. **O Evangelho segundo o Espiritismo**: começa em 02/03/2027
3. **O Livro dos Médiuns**: começa no dia útil seguinte ao fim do Evangelho
4. **O Céu e o Inferno**: logo depois
5. **A Gênese**: logo depois

Cada livro é montado um pouco antes de o anterior terminar.

## Regras de todos os livros
- Texto integral na tradução de Guillon Ribeiro (FEB, Federação Espírita Brasileira), em domínio público. Notas da editora ficam de fora e as notas de Kardec ficam.
- Uma leitura por dia útil, de no máximo uns 20 minutos (cerca de 200 palavras por minuto) e no mínimo uns 5 minutos. Os cortes seguem o tema, nunca no meio de um item. Sem leitura em fins de semana nem em feriados nacionais.
- Cada dia tem, nesta ordem:
  - texto original;
  - "pra hoje" (uma ação prática);
  - ligação com outro livro (no Livro dos Espíritos, com o Evangelho; no Evangelho, com as questões do Livro dos Espíritos);
  - um trecho da Bíblia Livre (BLIVRE, licença CC BY 3.0 BR, com atribuição);
  - o podcast do dia;
  - a música do dia (gospel, católica, espírita ou MPB, tocável no Spotify);
  - "explicando de um jeito simples", com **negrito** nas ideias principais e terminando em "**Resumindo:**".
- Visual "aura": degradê rosa, lilás e pêssego; fontes Fraunces, Lora e DM Sans.
- Saídas de cada livro (sem PDF: todo mundo usa o app/site; o PDF só existe para o Livro dos Espíritos):
  - o app no Claude (artifact https://claude.ai/artifact/6GwH6coVZpHv5YLq8hEheb);
  - este site (index.html), com um seletor de livro no topo e o cronograma e o progresso de cada livro guardados separadamente.
- Músicas de cada livro: uma playlist nova no Spotify.

## Como o Livro dos Espíritos foi montado (arquivos desta pasta)
1. `parse2.py`, `align.py`, `qnum.py` e `model.py` leem o texto e montam `blocks.json`, `units.json` e `days.json`. A fonte foi o arquivo `1lde-single-file.md` do repositório github.com/jhonnybn/conversoeslde.
2. `schedule.py` divide o livro em dias e põe as datas.
3. `content.py` guarda o "pra hoje" e a ligação com o Evangelho; `musicas.py` guarda as músicas; `explicacoes.py`, as explicações; `biblia.py`, a Bíblia (fonte: github.com/eversondeveloper/bibialivrejson, arquivo biblialivre.json).
4. `build_aura.py` + `style_aura.css` + `render.js` geram o PDF (Playwright/Chromium). As fontes vêm de @fontsource no npm.
5. `make_app.py` + `app_template.html` geram o app de uma página só (dados em JSON embutido). O index.html do site é esse mesmo app, com um cabeçalho HTML completo e o ícone.

## Cores de cada livro (aprovadas pela Ana em 10/11/2026)
Cada livro tem sua própria "aura", sempre no mesmo estilo: três manchas em degradê radial, com um brilho branco no centro e um fundo base. O app troca as cores sozinho (tokens CSS) conforme o livro aberto, também no modo escuro. No modo escuro, use as mesmas cores com alfa menor (cerca de 0,5) e uma base escura que puxe para a cor do livro.

| Livro | Mancha 1 | Mancha 2 | Mancha 3 | Base | Texto |
|---|---|---|---|---|---|
| O Livro dos Espíritos | rgb(240,150,178) rosa | rgb(178,152,232) lilás | rgb(247,184,150) pêssego | #EFD9E4 | #5B3A4A |
| O Evangelho segundo o Espiritismo | rgb(244,201,120) dourado | rgb(150,196,232) azul-céu | rgb(248,214,170) creme | #F4E6D2 | #4A3A1E |
| O Livro dos Médiuns | rgb(150,136,226) violeta | rgb(120,170,226) azul | rgb(214,170,232) lavanda | #DCD6F0 | #2F2A52 |
| O Céu e o Inferno | rgb(140,190,236) azul do amanhecer | rgb(246,160,140) coral | rgb(250,206,150) âmbar | #E8DDE2 | #3D2E3A |
| A Gênese | rgb(160,200,160) verde-sálvia | rgb(220,200,150) areia | rgb(140,196,196) água | #E3E6D6 | #2E3A2C |

O acento dos botões e links também segue a cor principal do livro (mancha 1, um tom mais escuro, com contraste AA, isto é, o nível mínimo de contraste das diretrizes WCAG de acessibilidade, sobre o fundo).

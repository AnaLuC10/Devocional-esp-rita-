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
- Saídas de cada livro:
  - PDF de 6 × 8 polegadas para o GoodNotes;
  - o app no Claude (artifact https://claude.ai/artifact/6GwH6coVZpHv5YLq8hEheb);
  - este site (index.html), com um seletor de livro no topo e o cronograma e o progresso de cada livro guardados separadamente.
- Músicas de cada livro: uma playlist nova no Spotify.

## Como o Livro dos Espíritos foi montado (arquivos desta pasta)
1. `parse2.py`, `align.py`, `qnum.py` e `model.py` leem o texto e montam `blocks.json`, `units.json` e `days.json`. A fonte foi o arquivo `1lde-single-file.md` do repositório github.com/jhonnybn/conversoeslde.
2. `schedule.py` divide o livro em dias e põe as datas.
3. `content.py` guarda o "pra hoje" e a ligação com o Evangelho; `musicas.py` guarda as músicas; `explicacoes.py`, as explicações; `biblia.py`, a Bíblia (fonte: github.com/eversondeveloper/bibialivrejson, arquivo biblialivre.json).
4. `build_aura.py` + `style_aura.css` + `render.js` geram o PDF (Playwright/Chromium). As fontes vêm de @fontsource no npm.
5. `make_app.py` + `app_template.html` geram o app de uma página só (dados em JSON embutido). O index.html do site é esse mesmo app, com um cabeçalho HTML completo e o ícone.

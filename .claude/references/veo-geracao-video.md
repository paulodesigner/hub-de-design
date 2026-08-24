# Geração de vídeo com Veo — referência técnica (Agente 12)

Detalhe técnico de como o **Agente 12 — Do Código ao Vídeo** pode gerar **cenas extras por IA** (Veo, Google) quando o pedido exigir algo que a gravação real do app não cobre — nunca em vez dela. A definição completa do agente vive em `.claude/agents/codigo-ao-video.md`; este arquivo é só o "como" da parte Veo — leia junto com o Golden Path de lá e com `.claude/references/narracao-elevenlabs.md` (a outra integração externa do A12, ElevenLabs).

## Por que existe (escopo, não substituição)
O **princípio-mestre do A12 continua intacto**: o vídeo do fluxo é sempre a gravação real do app, cursor suave como único overlay — nunca simulação. O Veo entra só pra **cenas que a gravação real não pode cobrir**, exemplos:
- Abertura/fechamento conceitual (ex.: um plano ilustrativo antes de entrar na tela real, tipo vinheta de vídeo institucional).
- B-roll abstrato/metáfora visual entre seções de um vídeo mais longo (ex.: apresentação institucional, não demo de produto).
- Cena que fisicamente não existe pra gravar (ex.: ambiente físico, ilustração de conceito) — nunca uma tela do app "reimaginada".

**Nunca use o Veo pra:**
- Fingir uma tela/fluxo do app (isso seria inventar comportamento — regra dura do A12).
- Substituir uma gravação real que deveria ter sido feita (se dá pra gravar o app de verdade, grave o app de verdade).
- Gerar pessoa real (rosto, voz) sem autorização — mesma regra do guardrail de voice cloning da ElevenLabs.
- **Regenerar/recriar um logotipo ou asset de marca** (ex.: vinheta institucional com o logo <EMPRESA>) — um logo é um traço exato de marca, não conteúdo ilustrativo; um modelo generativo pode distorcer proporção/tipografia. Sempre usar o arquivo real (PNG/SVG do repo) animado por composição determinística (modo "tela-vitrine": HTML/CSS + seek na Web Animations API + screenshot por frame), nunca pedir pro Veo "desenhar" a logo.

Toda cena Veo entra **por pedido explícito** do Paulo (nunca por iniciativa própria do agente) e é **sempre rotulada internamente** como "cena gerada por IA" na conversa — nunca apresentada como gravação real do produto.

## 2 caminhos possíveis — decisão do Paulo (2026-08-05): Caminho A é SEMPRE o padrão

### Caminho A (padrão — SEMPRE usar, salvo pedido explícito de magnific) — API direta Google AI Studio, chave pessoal do Paulo
**Decisão explícita do Paulo:** a conexão de verdade com o Veo é a **chave pessoal dele no Google AI Studio**, conectada a este projeto — é essa que o agente usa **por padrão, sempre**, mesmo tendo um caminho alternativo via `magnific` disponível. **Só usa `magnific` se o Paulo pedir por nome** ("gera com o magnific", "usa o magnific pra isso") — do contrário, a conexão direta com o Google é sempre a primeira opção.

**Setup (uma vez por máquina):**
1. **Conta no Google AI Studio** (a mesma conta paga do Paulo) — chave em [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. **Salvar em `~/.config/hub/veo_token`** (mesmo padrão do `figma_token`/`elevenlabs_token` — read-only, nunca impresso, nunca em `.env` versionado):
   ```bash
   mkdir -p ~/.config/hub
   pbpaste > ~/.config/hub/veo_token
   chmod 600 ~/.config/hub/veo_token
   ```
   **Sempre confirme que o arquivo foi criado de verdade** (`ls -la ~/.config/hub/veo_token`, tamanho >0) antes de assumir que deu certo — já aconteceu de o comando não persistir (clipboard vazio/terminal errado) sem erro visível.
   **Nunca valide a chave só pelo formato/prefixo** (o prefixo real de uma chave válida desta conta, 2026-08-05, foi `AQ.Ab8...` — não o `AIzaSy...` que seria de se esperar por convenção antiga; formato de chave muda). **Teste com uma chamada real e barata** antes de confiar nela:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" "https://generativelanguage.googleapis.com/v1beta/models?key=$(cat ~/.config/hub/veo_token)"
   ```
   `200` = chave válida; qualquer outro código = errada/expirada, peça pro Paulo copiar de novo direto do botão "API key" em aistudio.google.com/apikey.
3. **SDK oficial Node** (consistente com o resto do pipeline do A12, que já é Node/Playwright/ffmpeg-static):
   ```bash
   npm install @google/genai
   ```
4. **Nunca imprima o valor do token.** Injete como variável de ambiente na hora de rodar, lendo do arquivo local:
   ```js
   process.env.GEMINI_API_KEY = require('child_process')
     .execSync('cat ~/.config/hub/veo_token').toString().trim();
   ```

**Modelos** (`ai.google.dev/gemini-api/docs/veo` — nomenclatura `preview` muda com frequência, refaça `WebFetch` antes de confiar neste snapshot de 2026-08-05):
- `veo-3.1-generate-preview` (Veo 3.1, qualidade máxima)
- `veo-3.1-fast-generate-preview` (Veo 3.1 Fast, mais rápido/barato)
- `veo-3.1-lite-generate-preview` (Veo 3.1 Lite)
- `veo-3-generate-preview` (Veo 3 / Veo 3 Fast, anterior)
- `veo-2-generate-preview` (Veo 2, legado — sem áudio nativo)

Padrão pra B-roll institucional (custo mais baixo, qualidade suficiente pra cena curta): `veo-3.1-fast-generate-preview`. Só suba pra `veo-3.1-generate-preview` se o resultado do fast não convencer.

**Chamada e polling** (operação assíncrona — geração não é instantânea):
```js
import { GoogleGenAI } from '@google/genai';
const client = new GoogleGenAI({}); // lê GEMINI_API_KEY do env

let operation = await client.models.generateVideos({
  model: 'veo-3.1-fast-generate-preview',
  prompt: 'descrição em inglês, específica: câmera, sujeito, ação, luz, estilo',
  config: {
    aspectRatio: '16:9',   // ou '9:16' pra vertical
    resolution: '720p',    // '720p' (padrão) | '1080p' | '4k'
    durationSeconds: '8',  // '4' | '6' | '8' — 8s só sem 1080p/4k/imagem de referência
    numberOfVideos: 1,
  },
});

while (!operation.done) {
  await new Promise(r => setTimeout(r, 10_000)); // poll a cada 10s
  operation = await client.operations.get(operation);
}

const video = operation.response.generatedVideos[0];
await client.files.download({ file: video.video });
await video.video.save('scratchpad/veo_cena.mp4'); // mover pro projeto do usuário depois de aprovado
```
- **Latência real:** de ~11s a ~6 minutos por vídeo — nunca prometa "instantâneo"; avise o Paulo que pode demorar.
- **Vídeo some do servidor em 2 dias** — baixe imediatamente após `operation.done`, nunca deixe pra depois.
- **Veo 3.x gera áudio nativo** (ambiente/música/efeitos) — se a cena entrar num vídeo com narração ElevenLabs por cima, decida com o Paulo se o áudio nativo do Veo fica (mixado, mais baixo) ou é removido (`ffmpeg -an`) pra não competir com a narração.
- **Watermark SynthID invisível** é aplicado automaticamente pelo Google — não é algo pra tentar remover.
- **Filtro de segurança de conteúdo** se aplica (ofensivo/pessoa real/etc.) — se um prompt for recusado, não insista tentando contornar; ajuste o prompt ou pergunte ao Paulo.
- **Custo:** cada chamada de `generateVideos` consome cota/cobrança da conta paga pessoal do Paulo. **Nunca gere em lote/várias variações "pra testar" sem antes confirmar com ele** — 1 prompt aprovado por vez. Se o pedido tiver múltiplas cenas Veo, liste todos os prompts no chat pra aprovação conjunta antes de gerar qualquer um.

### Caminho B (só sob pedido explícito de "magnific") — MCP `magnific`
**Só use se o Paulo pedir por nome** ("gera com o magnific", "usa o magnific"). Achado técnico (2026-08-05): o servidor MCP `magnific` (conectado nesta conta, plano Premium, 20.000 créditos) também expõe os modelos Google Veo — `google-veo2`, `google-veo3`, `google-veo3-fast`, `google-veo3_1`, `google-veo3_1-fast`, `google-veo3_1-lite` — direto na tool `video_generate`, sem precisar da chave do Google AI Studio. É uma via alternativa válida, mas **não é o padrão** — o padrão é sempre o Caminho A.

Fluxo, se acionado: `video_plan` (brief + slug recomendado) → aprovação do Paulo → `video_generate` (slug verbatim, ex. `google-veo3_1`) → `creations_wait` (long-poll) → `creations_show` (render inline). Limites por modelo em `video_models_list` (busca "veo") — confira de novo antes de gerar, o catálogo muda.

## Integração no merge final do A12
Uma cena Veo entra no pipeline do A12 como **mais um clipe de vídeo bruto** — a composição final (concat com o vídeo gravado do app, ou overlay pontual) usa o mesmo ffmpeg já usado no resto do pipeline (`ffmpeg-static`), por exemplo:
```bash
ffmpeg -f concat -safe 0 -i lista_clipes.txt -c:v libx264 -crf 21 -pix_fmt yuv420p -movflags +faststart video_final.mp4
```
onde `lista_clipes.txt` referencia, em ordem, a cena Veo (intro) → o vídeo gravado do app (Playwright) → outra cena Veo (fechamento), se for esse o caso. Reencode uniforme (mesmo fps/resolução/pix_fmt) antes do concat pra evitar cortes/artefatos na emenda.

## Guardrails (segurança/ética — mesmo espírito do resto do A12)
- **Nunca gere uma pessoa real** (rosto, identidade reconhecível) sem autorização explícita por escrito — mesma regra do "não clonar voz real" da ElevenLabs.
- **Nunca gere uma tela/fluxo do produto fingindo ser gravação real** — isso quebra o princípio-mestre do A12 (autenticidade da demonstração). Cena Veo é sempre conteúdo ilustrativo/conceitual, claramente separável da gravação real no roteiro.
- **Rotule sempre no roteiro/chat qual cena é Veo** (gerada por IA) vs. qual é gravação real do app — nunca deixe implícito.
- **Prompt em inglês tende a dar resultado melhor** (modelo treinado majoritariamente em inglês) — descreva a cena em inglês mesmo que a conversa com o Paulo seja em português; a decisão de conteúdo/estilo continua sendo dele.

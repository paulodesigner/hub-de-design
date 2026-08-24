---
name: codigo-ao-video
description: "Agente 12 — Do Código ao Vídeo. Transforma um FLUXO já codado (app rodando) em um VÍDEO de produto com cursor suave estilo comercial da Apple, pra apresentar micro-interações e jornadas de forma leve e visual. Considera o CÓDIGO como fonte da verdade (rotas, gating, estados, timing, assets) e DIRIGE o app real com Playwright + cursor sintético; grava e exporta em mp4+webm (loop com fade, poster). Monta um ROTEIRO (código + passo a passo do usuário), sugere NARRAÇÃO estilo vídeo de produto e, após aprovação, gera áudio via ElevenLabs sincronizado (export adicional). Sob pedido explícito, também gera cenas ilustrativas extras via Google Veo (vinheta/B-roll) só pro que a gravação real não cobre. Use para 'transforma esse fluxo/tela em vídeo', 'grava um vídeo do fluxo com cursor', 'faz um vídeo de apresentação dessa interação', 'sugere uma narração/legenda', 'gera uma cena com Veo'. Requer app rodável. Não é screencast manual nem colagem de telas do Figma."
---

# Do Código ao Vídeo — apresentação de fluxo com cursor (Agente 12)

> **Este agente roda melhor no LOOP PRINCIPAL.** É trabalho **iterativo e visual**: dirigir o app → extrair frames → olhar → ajustar timing/seletores → regravar. Igual ao A1 e ao A9, o vai-e-vem precisa do meu contexto. A **definição completa** — Golden Path, receita técnica, pitfalls e roadmap — está em [`.claude/agents/codigo-ao-video.md`](../../agents/codigo-ao-video.md). Spawnar o subagente só quando for gerar vários vídeos em paralelo.

## O que faz (resumo)
Pega um fluxo que **já existe em código** e entrega um **vídeo do produto real rodando**, com um **cursor suave** (easing, pausas — estilo comercial da Apple), monta o **roteiro** (código + passo a passo do usuário), sugere uma **narração** estilo vídeo de produto e, após aprovação, gera o áudio via **ElevenLabs sincronizado** como export adicional. Um vídeo comunica micro-interações e jornada muito melhor que telas paradas. **Não** implementa o fluxo (isso é o A7), **não** é screencast manual, **não** é colagem de telas do Figma.

## Modo de trabalhar — padrão fixo, 2 checkpoints (loop principal)
**Fase 0 — descoberta:** ache o app/rota EXATOS (não assuma — produtos do mesmo ecossistema podem ser codebases diferentes); se for `<PRODUTO>/`, rode `~/bin/<produto>-sync` antes de ler código (nunca confie em leitura antiga); leia rotas, gating, estados, timing, textos reais e o que cada endpoint espera. Sem app em código, é caso do A7 antes.

**Checkpoint 1 — confirmar o FLUXO:** apresente um boletim curto (tela inicial → intermediária(s) → final, 1 linha cada) e **pergunte se é esse fluxo mesmo** antes de montar qualquer roteiro. Se o usuário mandou prints, confirme que batem.

**Checkpoint 2 — roteiro + narração:** só depois do Checkpoint 1 aprovado, monte o roteiro (cenas de fala vs. cenas de ação) e a narração (estilo produto, autoapresentação humana na abertura) → aprovação no chat antes de gravar/gerar áudio.

**Fase 2.5 (só se o usuário quiser avatar REAL, com rosto/lip-sync, via ElevenLabs Avatars):** gere a narração aprovada e **entregue o áudio ao usuário ANTES de gravar a tela** — ele mesmo sobe esse áudio no painel da ElevenLabs (sem API pública, handoff manual), escolhe um avatar, baixa o vídeo com lip-sync e devolve o clipe. Só depois disso a composição final acontece (coreografia de tamanho/posição, não overlay fixo — detalhe em `.claude/agents/codigo-ao-video.md`). Entregue sempre dentro do projeto do usuário, nunca só no `scratchpad` da sessão (pitfall #48).

**Fase 3 — construção (só depois das 2 aprovações):**
1. Reproduza **localmente** (nunca sessão real via CDP — o classificador de segurança bloqueia, é a regra certa). Backend/API real → intercepte com `page.route()` e dados fictícios; auth de terceiro (Clerk etc.) → simule a inicialização do SDK localmente.
2. Gere as **falas numa única chamada de TTS** (tom consistente), corte por `alignment`.
3. Grave com Playwright seguindo o **modelo fala→pausa→ação**: tela parada durante a fala, cursor se move só no silêncio reservado pra ação.
4. Encode `ffmpeg-static` (mp4 H.264 + webm VP9 + fade + poster) do vídeo MUDO, sem alteração. Só no export narrado: mescle a trilha (`adelay`+`amix`+`apad`) e componha por cima, via `-filter_complex`, o **avatar-bolha** (monograma, canto inferior esquerdo, `overlay`+`enable=between(t,…)` nas janelas de fala) e a **legenda em tela** (`.vtt`+queimada, mesmo timing da narração) → `video_narrado` (export ADICIONAL, nunca substitui o mudo). Detalhe técnico completo em `.claude/agents/codigo-ao-video.md` → "Avatar-bolha e legendas".
5. Verifique de verdade: frames-chave por cena + `volumedetect` (seek de entrada) confirmando silêncio real nas ações e fala real nas falas + 0 erros de console.
6. Instale limpo: mudo `<video muted loop playsinline autoplay preload="metadata" poster>`, mp4 antes/webm depois, sem borda/badge, só toca visível, respeita reduced-motion. Narrado = arquivo separado.

## Cenas geradas por IA (Veo) — opcional, sob pedido
Quando o pedido precisar de algo que a gravação real não cobre (vinheta de abertura/fechamento, B-roll abstrato de um vídeo institucional), o agente pode gerar essa cena via **Veo (Google)** — **nunca em vez de gravar uma tela real**, sempre sob aprovação explícita cena a cena (mesmo princípio da narração) e rotulada como "gerada por IA" no roteiro. **Caminho padrão, SEMPRE: API direta Google AI Studio com a chave PESSOAL do Paulo** (`~/.config/hub/veo_token`, SDK `@google/genai`, modelos `veo-3.1-*-generate-preview`). **Só usa o MCP `magnific`** (`video_plan` → `video_generate` → `creations_wait` → `creations_show`) **se o Paulo pedir por nome** ("gera com o magnific") — nunca por default. Detalhe completo em `.claude/references/veo-geracao-video.md`.

## Não erre de novo (pitfalls que já custaram uma rodada)
- **Nada de simulação:** sem ripple/pulse/vinheta/badge — grave o app real; o cursor suave é o único overlay.
- **Multi-formato SEMPRE (mp4+webm):** Safari não toca VP8/VP9 confiável; Chromium headless não toca H.264. Um formato só = quebra em algum lugar.
- **Tempo real:** não acelere a leitura; deixe o slideshow trocar e os timers correrem.
- **Estados no momento certo:** o branch de correção/erro só aparece quando o **gating real** dispara (leia o código).
- **Grave o app, não exporte telas** do Figma (o app real renderiza certo mesmo quando o export está quebrado).
- **Roteiro sempre revisado antes de gravar** — evita regravar tudo por causa de um passo mal entendido.
- **Narração é copy FALADA, não copy de tela** — mais curta e oral; nunca gere áudio sem aprovação do texto; nunca acelere o vídeo pra caber a fala (estica a pausa); vídeo narrado nunca substitui o mudo do site; nunca clona voz de pessoa real sem autorização explícita.
- **Fluxo errado é o pitfall mais caro que existe** — confirme SEMPRE (Checkpoint 1) qual app/rota é o pedido antes de montar roteiro; produtos parecidos podem ser codebases totalmente diferentes.
- **Nunca automatize cliques numa sessão real/autenticada via CDP** — o classificador de segurança bloqueia (corretamente); reproduza local com dados fictícios.
- **Fala e ação nunca ao mesmo tempo** — tela parada durante a narração, cursor se move só em silêncio.
- **SEM ZOOM. Câmera estática, sempre** (decisão do Paulo, 2026-08-04, depois de ver 9 clipes com zoom: "os zooms não ficaram bons e os cortes ficaram rápidos demais"). Quem dirige a atenção é o **cursor**: leve-o até o elemento e **fique parado ali 1,5–2,5s** antes de trocar de cena. Ritmo calmo > vídeo curto; **mínimo 10s** por vídeo.
- **Playwright grava em px CSS e ignora `deviceScaleFactor`** — `recordVideo.size` maior que o viewport NÃO amplia: cola a página no canto superior esquerdo e preenche o resto de cinza. Não existe fonte 2x pra zoom em pós-produção; grave `size` = viewport.
- **VP9 sem `-pix_fmt yuv420p` sai Profile 1 (`gbrp`, 4:4:4)** — suporte pior em navegador e arquivo maior. Force sempre `yuv420p` (Profile 0).
- **O que está no ar pode ser um build ANTIGO do código local** — antes de prometer gravar da URL pública, faça `grep` de um texto exclusivo da feature no bundle servido (`curl .../assets/index-*.js`). Uma rota inteira (`/painel`) não existia no deploy.
- **Alvo abaixo da dobra: use a BUSCA do próprio app, não scroll** — filtra a linha pra cima, mostra uma feature real e evita a captura de scroll (técnica não validada).
- **Clique no dropzone abre o seletor de arquivo de verdade** — `page.waitForEvent('filechooser')` + `chooser.setFiles(...)` (clique real, mais fiel que `setInputFiles` no input escondido).
- **`getByText` acha duplicata invisível** de markup responsivo (bloco `md:hidden` + `hidden md:flex`) → violação de strict mode no `boundingBox()`. Escolha um rótulo que só exista na variante visível.
- **SEM FADE em nenhum ponto** (decisão do Paulo, 2026-08-04 — os `fade=t=in/out:c=white` da receita antiga foram **reprovados**): o único evento de transição visível é o corte do loop. Confira medindo o luma dos primeiros/últimos frames (`signalstats` → `YAVG` constante; se sobe pra ~235 e cai, é fade de branco).
- **Cursor SEMPRE em tela, do 1º ao último frame:** `div` no `documentElement` via `addInitScript` + guarda `setInterval(250ms)` que recria se algo remover (sobrevive a troca de rota e a `createPortal` de drawer). Valide com crops nos momentos de navegação, não só no meio das cenas.
- **Loop sem salto quando começo e fim são telas diferentes = continuidade do CURSOR:** deixe o cursor no MESMO pixel no primeiro e no último frame (`setCursor(PARK)` antes do corte + última batida terminando em `PARK`) e hold estático ≥2s nas duas pontas. Sem fade, é a única costura possível.
- **Estado inicial "já avançado" em app sem persistência: grave o setup e CORTE depois** — e **corte sempre dentro de um hold estático** (2,5s de tela parada), **depois** da animação de entrada do app terminar (cortar no `cutMs` cru pega o `useReveal` no meio e o 1º frame parece um fade-in). Registre `cutMs` no script e confirme por frame extraído.
- **Scroll leva o cursor junto (um tween só):** `window.scrollTo` + `left/top` do cursor no mesmo `requestAnimationFrame`/easing, terminando no alvo. E **tela nova sempre no topo**: `window.scrollTo(0,0)` logo após cada navegação (React Router não reseta scroll sozinho).
- **Offset de trim: meça por CENA, não por relógio.** `duração_do_bruto − duração_da_coreografia` errou em ~2s (dava 4,8s, o real era 2,77s) e cortaria a 1ª ação. Rode `ffmpeg -vf "select='gt(scene,0.004)',metadata=print"` no bruto e case as mudanças de cena com os `marks` que o script gravou (confirme com 2 landmarks independentes).
- **Depois do cursor sintético chegar, mova o mouse REAL pro mesmo ponto** (`page.mouse.move`) — é o que liga o hover verdadeiro do componente (borda/fundo do dropzone). E deixe **1,2-1,5s de dwell** com o hover aceso antes do clique; 0,3s some no vídeo.
- **Upload/remover conteúdo encolhe a página e pode clampar o scroll** (o browser corrige sozinho = salto no quadro). Escolha o alvo de scroll que continua válido DEPOIS do encolhimento.
- **Fluxo que repete N vezes quase nunca repete IGUAL** — leia o código que decide o destino de cada volta (num fluxo de 3 unidades, a 1ª caía numa tela de correção de dados, a do meio numa confirmação e a última na conclusão da rede). Assumir "3 voltas = 3× o mesmo caminho" grava o fluxo errado.
- **Decida scroll por medição, não por memória:** helper `irAte(locator)` que lê o `boundingBox` e escolhe entre `point()` (dentro da dobra) e `scrollToTarget()` (scroll+cursor no mesmo tween) — sobrevive a telas que crescem durante a gravação (chip de upload empurra o botão pra fora da dobra).
- **Ache o dropzone pela SEÇÃO do documento**, nunca por índice: `locator('section').filter({has: getByRole('heading',{name})}).getByRole('button',{name:/clique para/})` — imune ao rótulo que muda ("enviar" → "adicionar" em campo múltiplo) e à ordem dos blocos.
- **"Fontconfig error: Cannot load default config file" do ffmpeg-static é RUÍDO** — o `drawtext` renderiza normalmente. Confira o JPG antes de concluir que o rótulo de timestamp falhou.
- **Varra o vídeo INTEIRO procurando frame branco (hot reload) por estatística:** `ffmpeg -vf "fps=5,scale=48:30,format=gray" -f rawvideo -` e, em Node, flag em `min(pixel) >= 248`. Centenas de frames em segundos — contact sheet olha ~30.
- **Modo "tela-vitrine" (composição de componentes, sem rota real):** quando a peça é uma tela montada no Figma (não uma jornada), a fonte da verdade é o **PNG aprovado + o código do node + os assets locais** — reconstrua em HTML/CSS/JS autocontido e anime. **Sem cursor** (várias coisas ao mesmo tempo).
- **Loop puro em CSS: renderize por SEEK, não por gravação.** `getAnimations().forEach(a=>a.pause())` + `a.currentTime = t` + `screenshot()` por frame ⇒ loop fecha por construção, zero offset de trim, zero frame perdido (300 frames 1920×1080 em ~21s). Períodos das animações precisam ser **divisores exatos** da duração e os delays constantes. QA: `diff(último, primeiro)` no PNG tem que ser da mesma ordem de qualquer par consecutivo.
- **O codegen do Figma pode errar `font-size` em instância escalada** (3 rótulos de Button vieram 1,208× menores que o PNG aprovado). Confira medindo a **largura de tinta** de cada rótulo (ref vs render): o PNG aprovado é a régua, não o código gerado.
- **Nunca faça crossfade entre dois PESOS da mesma fonte** (fantasma de texto duplo). Um span só: cor interpolando + `font-weight` trocando seco no meio (`animation-timing-function: step-end` dentro do keyframe) + largura do box travada na medida do peso de referência.
- **"Marching ants" = SVG `rect` com `stroke-dashoffset` animado** (as props de geometria SVG funcionam como CSS no Chrome). Mantenha `border: Npx solid transparent` no elemento pra a caixa não mudar. `border: dashed` do CSS não anima.
- **Composição mais "alta" que 16:9: o vertical é o gargalo.** Escale pelo vertical e deixe o **próprio fundo da composição** preencher o quadro (sem barra branca/letterbox). Espalhar colunas pra encher a largura abre um buraco no meio — pior que margem na borda.
- **Ritmo "overview" (ágil sem virar robô), números validados:** cursor 620ms (780ms no 1º movimento da tela), dwell 340ms antes do clique, 820ms ao chegar em tela nova, 480ms após o chip de upload, digitação 62ms/caractere; nas repetições encurte só os dwells (~520ms), nunca o app.
- **Overlay injetado no `addInitScript` (document-start) quebra o parse do HTML** — `documentElement.appendChild(...)` antes do parser deixa o `<html>` com 0 filhos e a página inteira não renderiza, **sem erro nenhum**: o sintoma que chega é `waitForSelector` estourando timeout. Injete cortina/overlay só DEPOIS do load (`page.evaluate` + `document.body.appendChild`).
- **Cortina branca pós-load (~1,4s) = trim determinístico e barato** (alternativa ao casamento de cena): ache o **último bloco de frames 100% brancos** do bruto (`fps=25,scale=64:40,format=gray` → `min>=248`) e corte 1 frame depois — erro medido de 0,05s. Só funciona se o **cursor sintético ficar com `z-index` ABAIXO da cortina**.
- **Conteúdo de aba/painel inativo (`display:none`) nunca fica "visible"** — use `state:'attached'` ou `waitForFunction(children.length>0)`. E, sem credencial de backend local, **prefira o snapshot do endpoint público de PRODUÇÃO à fixture inventada** (`curl` + servidor estático no `scratchpad`): dado real, nenhum arquivo novo no projeto do usuário.
- **Ritmo "navegação entre abas" validado (7 abas em 46,6s):** cursor 620ms por trajeto (720ms no 1º), 280ms de dwell antes do clique, 5,0s de tela parada por aba (+1,5s na última) — suave sem ficar lento.

- **`libvpx-vp9` do `ffmpeg-static` descarta ALPHA em silêncio** (`-pix_fmt yuva420p` sai `yuv420p`, sem warning) → bolha-avatar vira quadrado preto. Loops com alpha em **`qtrle`/`argb` (.mov)** + `format=rgba` no filtro; sempre reprobe o `pix_fmt` do arquivo gerado.
- **`-shortest` não termina o encode com `-stream_loop -1`** (render de 126s passou de 222 MB e 19 min). Limite cada input infinito com `-t` antes do `-i` **e** ponha `-t` na saída.
- **Legenda queimada centralizada colide com o CTA** — âncore em `Alignment=1` (inferior esquerdo) com `MarginL` logo à direita da bolha; a metade direita do quadro fica limpa. QA visual dessa colisão é obrigatório.
- **`page.goBack()` é rota client-side válida quando não há botão de volta na UI** (preserva o estado do React context); deixe ~1s de leitura antes do salto.


## Roadmap (a testar — ainda não)
Captura de **scroll** (rolar até o botão em vez de cortar) · mobile/multi-resolução · velocidade por trecho · avatar com rosto real/lip-sync (ElevenLabs Avatars — sem API pública ainda, só painel+plano pago; ver `.claude/agents/codigo-ao-video.md`). Registre cada experimento como lição.
**Zoom saiu do roadmap: testado e REPROVADO pelo usuário** (2026-08-04) — não reintroduza sem pedido explícito dele.

## Loop de auto-aprendizado (obrigatório)
Ao concluir/errar: destile a lição → `memoria/aprendizados.md` com a tag **`[A12]`** → vire regra viva **aqui e na def** (ou em `.claude/references/narracao-elevenlabs.md`/`.claude/references/veo-geracao-video.md` se for específica de narração/áudio ou de cenas Veo) → atualize `memoria/estado-atual.md`.

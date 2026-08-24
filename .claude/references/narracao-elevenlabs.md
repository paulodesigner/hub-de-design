# Narração com ElevenLabs — referência técnica (Agente 12)

Detalhe técnico de como o **Agente 12 — Do Código ao Vídeo** gera a sugestão de narração e sincroniza o áudio da ElevenLabs com o vídeo. A definição completa do agente vive em `.claude/agents/codigo-ao-video.md`; este arquivo é só o "como" da parte de narração — leia junto com o Golden Path de lá.

## Setup (uma vez por máquina)
1. **Conta em elevenlabs.io** — cria o Paulo; nenhum agente pede login/senha.
2. **Chave de API:** [Create an API key in the dashboard](https://elevenlabs.io/app/settings/api-keys) (Settings → API Keys → Create).
3. **Salvar em `~/.config/hub/elevenlabs_token`** (mesmo padrão do `figma_token` — read-only, nunca impresso, **nunca num `.env` dentro de um repo** — evita o risco de a chave ser commitada por engano). **No zsh** (padrão no macOS, inclusive terminal do VS Code), o comando estilo bash `read -s -p "prompt" VAR` **falha** com `read: -p: no coprocess` (no zsh, `-p` do `read` é reservado pra coprocess, não é "mostrar um prompt"). Duas formas que funcionam de verdade:
   - **Mais simples, se a chave já está copiada:** `pbpaste` lê a área de transferência direto, sem prompt interativo (evita também o caso do paste não funcionar dentro de um prompt mascarado):
     ```bash
     mkdir -p ~/.config/hub
     pbpaste > ~/.config/hub/elevenlabs_token
     chmod 600 ~/.config/hub/elevenlabs_token
     ```
   - **Sintaxe correta de prompt no zsh** (se preferir digitar/colar na hora, sem depender do clipboard):
     ```zsh
     mkdir -p ~/.config/hub
     read -s "KEY?Cole a chave ElevenLabs: "
     echo "$KEY" > ~/.config/hub/elevenlabs_token
     chmod 600 ~/.config/hub/elevenlabs_token
     unset KEY
     ```
4. **NUNCA imprima o valor do token.** Nos scripts de narração (Node, ao lado do script Playwright em `scratchpad/`), injete como variável de ambiente **na hora de rodar**, lendo do arquivo local — nunca escrevendo num `.env` versionado:
   ```js
   process.env.ELEVENLABS_API_KEY = require('child_process')
     .execSync('cat ~/.config/hub/elevenlabs_token').toString().trim();
   const { ElevenLabsClient } = require('@elevenlabs/elevenlabs-js'); // client pega ELEVENLABS_API_KEY do env automaticamente
   const elevenlabs = new ElevenLabsClient();
   ```
5. **SDK oficial (Node), consistente com o resto do pipeline** (que já é Node/Playwright/ffmpeg-static):
   ```bash
   npm install @elevenlabs/elevenlabs-js
   ```
   (a doc oficial também tem SDK Python — `pip install elevenlabs python-dotenv` — só faz sentido aqui se o resto do script de narração for escrito em Python; padrão é seguir Node pra não misturar runtime com o script de gravação.)
6. **Voz fixada (não escolher de novo):** `voice_id = dfeOmy6Uay63tNhyO99j` (escolhida pelo Paulo na Voice Library em 2026-07-28). Use este `voice_id` por padrão em toda narração; só volte à Voice Library se o Paulo pedir uma voz diferente pra um vídeo específico.
7. **Modelo:** a doc oficial de quickstart usa `eleven_v3` como exemplo atual (mais novo, multilíngue, mais expressivo) — **confirme o modelo recomendado no momento de implementar** (via `WebFetch` na doc oficial, `/docs/api-reference`), já que a ElevenLabs atualiza a lista de modelos com frequência.

## Estilo de roteiro — "como grandes empresas apresentam" (Google/Apple, vídeo de produto)
A sugestão de narração de cada cena segue estes princípios. **Não é o estilo de UX copy do Agente 2** (isso é copy de tela) — é copy de **vídeo falado**, mais curto e mais oral:
1. **Benefício antes do mecanismo.** "Aprovar uma fatura agora leva 10 segundos" antes de "clique no botão verde".
2. **Frase curta, presente, voz ativa.** Pensada pra ser OUVIDA, não lida — sem subordinadas longas.
3. **Um benefício por cena.** Não empilha 3 features na mesma frase.
4. **Tom confiante e humano** — nem robótico, nem hiperbólico ("revolucionário", "incrível").
5. **Sem jargão interno** (nome de componente, de endpoint, "flag", "gate") — linguagem de quem usa o produto, não de quem o construiu.
6. **Silêncio é permitido.** Nem toda cena precisa de fala; pausa é respiro, não espaço a preencher.
7. **Fechamento leve**, só se fizer sentido — call-to-action suave, nunca vendedor forçado.
8. **Conectores entre cenas, pra virar HISTÓRIA contada — não uma lista de labels lida em voz alta.** Feedback real do Paulo (1ª simulação): a narração ficou "muito narrada" (soava lida) e precisava ser "mais contada" — o ajuste foi costurar as cenas com frases de transição: "e agora", "e enquanto isso", "uma olhada, e já pode enviar", "e adivinha?". Isso cria ritmo de alguém GUIANDO a jornada, não descrevendo feature por feature. Continua profissional (sem gíria pesada, sem hipérbole) — é calor humano, não casualidade.
9. **Linguagem adaptada ao público de baixo acesso à tecnologia** (escolas, secretaria, mantenedores — não times técnicos): zero jargão, mesmo o "levinho" ("upload" vira "enviar o arquivo", nada de "dashboard"/"token"/nomes de tela em inglês). Frases curtas, **um passo por vez**, tom de reasseguramento ("é rapidinho", "sem complicação") em vez de tom de venda ou de manual técnico. Fonte: pesquisa de mercado (ver seção própria abaixo) confirma que clareza > tudo pra esse tipo de público, e que o script deve "falar a língua" de quem não é do digital.
10. **Abertura SEMPRE com autoapresentação humana** — antes de entrar no fluxo, a narração se apresenta como uma PESSOA real da equipe <EMPRESA> ("Oi, eu sou [nome] — trabalho no <EMPRESA>, e hoje vou te ajudar a entender como funciona o envio de documentos"), quebrando de propósito a sensação de "vídeo feito por IA" logo de cara. É a única exceção à regra de "frase curta por cena": a abertura pode ocupar mais tempo de tela que uma cena isolada (ex.: as 2 primeiras cenas juntas), porque é o único momento em que o vídeo fala DIRETAMENTE com a pessoa antes de entrar no conteúdo. **O nome/identidade usada na autoapresentação é sempre uma decisão do Paulo** — nunca invente um nome de pessoa real por conta própria (risco de parecer um funcionário que não existe); pergunte antes de gerar.
11. **Problema/benefício antes da mecânica** (reforça o princípio #1) — em vídeos curtos (nosso caso, ~49s) cabe só 1 CTA leve, no fechamento; vídeos mais longos podem ter um CTA leve no meio também, depois do primeiro benefício grande.
12. **Reforçar com legenda em tela o que está sendo dito** deixa de ser só "roadmap" e vira prioridade quando o público tem baixo acesso à tecnologia — parte assiste no mudo, ou tem mais facilidade lendo que ouvindo em português técnico. Ver roadmap (`.claude/agents/codigo-ao-video.md`) — ainda não implementado, mas priorizar antes das próximas melhorias de zoom/scroll.

## Pesquisa: melhores práticas (2026-07-28)
Fontes consultadas — explainer video pra baixa familiaridade digital, estrutura de vídeo de produto, humanização de voz de IA, e mixagem de música de fundo:
- clareza > tudo: entender o vocabulário/dores do público específico antes de escrever, evitar termos difíceis de pronunciar e frases longas ([Pexo — Explainer Video Best Practices](https://pexo.ai/blog/explainer-video-best-practices-9457), [TapVid](https://tapvid.ai/blog/how-to-make-ai-explainer-video))
- estrutura problema→solução→por que importa, com 1 mensagem central por vídeo, não uma lista de features ([ngram — Product Demo Best Practices](https://www.ngram.com/blog/product-demo-best-practices))
- humanizar TTS: pontuação/pausas que imitam ritmo humano, emoção casada com o visual, tom formal-porém-acolhedor pra conteúdo educacional/corporativo (não o tom "de marketing") ([Mixcord](https://www.mixcord.co/blogs/content-creators/humanizing-ai-text-to-speech-pro-narrator-tips), [WowTo — AI Voices vs Human Narrators](https://wowto.ai/blog/ai-voices-vs-human-narrators-which-is-better-for-your-instructional-videos))
- mixagem voz+música: **voz em -6 a -12dB**, **música 15-20dB mais baixa que a voz** (tipicamente -18 a -25dB), **ducking de -15 a -24dB** quando há fala (a música sobe de volta assim que a fala para); evitar timbres agudos (apito/flauta) que competem com a voz — lo-fi já favorece isso por natureza (instrumentação quente/abafada) ([Bunny Studio](https://bunnystudio.com/blog/voice-over-background-music-best-practices/), [CyberLink — Audio Ducking](https://www.cyberlink.com/learning/powerdirector-video-editing-software/824/using-audio-ducking-to-balance-voice-overs-and-background-music))

## Música de fundo (lo-fi, bem baixinha)
**A ElevenLabs tem API de música própria** — `elevenlabs.music.compose()` (SDK, `modelId: 'music_v2'`, parâmetro `prompt` descrevendo o estilo ex. "lo-fi hip-hop track, relaxed, smooth piano, gentle drums", `musicLengthMs` pra duração) e até um endpoint **`video-to-music`** que gera a trilha direto a partir do vídeo enviado. **Mas exige plano pago** ("The Eleven Music API is only available to paid users") — mesma trava da voz `Kristen` (Voice Library). Fontes: [ElevenLabs — Eleven Music now in the API](https://elevenlabs.io/blog/eleven-music-now-available-in-the-api), [ElevenLabs Docs — Video To Music](https://elevenlabs.io/docs/api-reference/music/video-to-music).

**Enquanto o plano for free, 2 caminhos possíveis** (perguntar ao Paulo qual preferir, nunca decidir sozinho por causa de risco de licença):
1. **Esperar o upgrade** — se/quando acontecer (já é útil pra liberar a voz `Kristen` também), gerar a trilha com `music.compose()` casada com a duração exata do vídeo (`musicLengthMs` = duração total em ms), aplicar o mix conforme os dB acima.
2. **Trilha royalty-free externa** — banco de música licenciada pra uso comercial (ex.: Pixabay Music, YouTube Audio Library) escolhida e confirmada pelo Paulo (checar termos de licença especificamente pro uso — apresentação/case interno). **Nunca baixar/usar uma faixa sem confirmar a licença primeiro** — risco de direito autoral é real mesmo em vídeo interno.

**Mix técnico (quando tiver a trilha, qualquer uma das 2 fontes):** looping se a faixa for mais curta que o vídeo (`aloop`), volume base bem baixo (a pedido do Paulo: "quase não dá pra escutar" — mirar uns **-28 a -32dB**, mais baixo que o padrão de mercado citado acima, já que o pedido explícito é "baixinha, baixinha"), fade in/out nas pontas, e ducking (`sidechaincompress` do ffmpeg, ou simplesmente baixar mais o volume da música nos trechos com narração e subir um pouco nos trechos mudos) pra nunca competir com a fala.

## Modelo de ritmo — FALA → PAUSA → AÇÃO (obrigatório **quando NÃO há avatar visível**)
Feedback real do Paulo (2ª simulação, fluxo de matrícula pelo webclient/admin): **a narração nunca pode tocar ao mesmo tempo que o cursor se move/age.** Se a fala não estiver descrevendo a ação que está acontecendo naquele instante, o vídeo não pode se mover nesse momento — o usuário não sabe se presta atenção na imagem ou no áudio. Regra:

**Exceção (2026-07-30, avatar real via handoff ElevenLabs):** com um avatar/rosto SEMPRE visível na tela (split-screen, canto ou fullscreen — ver `.claude/agents/codigo-ao-video.md` → "Avatar REAL"), essa regra deixa de valer — o espectador já tem um ponto de atenção humano o tempo todo, então ação e fala PODEM se sobrepor (como um apresentador de verdade aponta/clica enquanto continua falando). Motivo técnico adicional: o clipe do avatar vem da ElevenLabs renderizado sobre o áudio CONTÍNUO cru, sem os silêncios artificiais que este modelo reserva — não tem como esticar pausa num áudio que já veio pronto. Pra vídeo SEM avatar visível (bolha ou mudo puro), a regra abaixo continua obrigatória.
- **Cena de FALA:** tela **parada** (cursor não se move nem clica) enquanto a narração explica o que se vê/vai acontecer.
- **Cena de AÇÃO:** cursor se move e age **em silêncio** (ou quase — sem fala nova começando ali), executando o que a fala anterior descreveu.
- Nunca alterna os dois na mesma janela de tempo. O exemplo do próprio Paulo: "Oi, sou tal, hoje vou te mostrar tal coisa" (tela parada) → **só depois** disso o cursor começa a se mover.

**Como isso muda o Método A (áudio contínuo):** ainda se gera todas as FALAS a partir de **uma única chamada** de TTS (pra manter o tom 100% consistente), mas agora com **texto só dos trechos falados** (as ações ficam de fora do texto — são os "gaps" propositais). Depois de gerar, **corta-se o áudio em clipes por fala** (usando o `alignment` pra achar o offset exato de cada trecho dentro do áudio bruto) e cada clipe é posicionado na timeline final com um **delay que reserva um vão de silêncio real** pra ação correspondente — via `adelay` por clipe + `amix` + `apad` (mesma mecânica do Método B de assembly, mas cada clipe vem de uma ÚNICA geração, não de chamadas separadas — sem risco de tom inconsistente entre eles).

**Como calcular a duração da janela de ação:** não tem áudio pra medir (é silêncio de propósito) — estime pelo tipo de ação: mover+clicar um botão (~1.5-2s), abrir um dropdown+escolher opção (~2-2.5s), salvar+aguardar toast (~2-2.5s), transição entre modais (~1.5-2s). Ajuste depois de ver o resultado.

## Fluxo técnico — 2 métodos (escolha pelo caso)

### Método A — GRAVAÇÃO NOVA (preferido; áudio contínuo, sem colagem)
Use sempre que for gravar um vídeo do zero (não um retrofit de vídeo já existente). É o método que elimina de raiz os 2 problemas que já apareceram na prática — corte brusco entre trechos e tom inconsistente entre falas — porque **não há colagem de áudio nenhuma**: é uma única geração contínua, e o VÍDEO é que se adapta ao tempo real da fala (não o contrário).
1. **Roteiro em cenas numeradas** (Golden Path) — leitura do código + o que o Paulo descrever.
2. **Escreva a narração como UM TEXTO CONTÍNUO** (não frases isoladas por cena) — cada cena é só um trecho desse texto único, emendado com conectores naturais (ver estilo acima). Aprovação do Paulo antes de gerar.
3. **Gere o áudio INTEIRO numa única chamada**, pedindo timestamps por caractere:
   ```js
   const resultado = await elevenlabs.textToSpeech.convertWithTimestamps(VOICE_ID, {
     text: textoCompletoDeTodasAsCenas,
     modelId: 'eleven_v3', // confirme o modelo atual recomendado no momento de implementar
     outputFormat: 'mp3_44100_128',
   });
   // resultado.audioBase64 → decodifique pra .mp3 (1 arquivo, a trilha inteira)
   // resultado.alignment = { characters, characterStartTimesSeconds, characterEndTimesSeconds }
   ```
4. **Calcule o tempo real de início/fim de cada cena** achando o offset de caractere onde o texto daquela cena começa dentro do texto completo, e lendo `characterStartTimesSeconds`/`characterEndTimesSeconds` nesse índice. Isso dá, pra cada cena, o tempo exato (em ms) que ela TEM que durar na gravação.
5. **Grave o app pacenado por esses tempos** (não o inverso): o script Playwright, depois de terminar as ações de uma cena, espera (`waitForTimeout`) até o tempo-alvo daquela cena antes de clicar/navegar pra próxima — nunca adianta o clique, só segura o cursor parado até a hora certa. Se as ações da cena já estourarem o tempo-alvo sozinhas (raro, cena "cheia"), só loga o atraso e segue (não há como voltar no tempo).
6. **Merge final é direto, sem `amix`/`adelay`/`apad`** (só 1 trilha de áudio, do início ao fim do vídeo):
   ```bash
   ffmpeg -i video_mudo.mp4 -i narracao_completa.mp3 \
     -map 0:v -map 1:a -c:v copy -c:a aac -shortest video_narrado.mp4
   ```
7. **2 exports finais, sempre:** `video_mudo.mp4`/`.webm` (site, `autoplay muted loop`) + `video_narrado.mp4` (export ADICIONAL, apresentação/onboarding).

### Método B — RETROFIT em vídeo já existente (quando não dá pra regravar)
Use só quando o vídeo já existe e não há como regravar (script de gravação perdido, vídeo de terceiros, etc.) — aceita mais imperfeição de sincronia porque o vídeo não pode se adaptar ao áudio.
1. Mapeie as cenas do vídeo existente por frames **com timestamp gravado** (`drawtext`, nunca contagem manual — ver lição abaixo).
2. Gere UM áudio por cena (chamadas separadas) — aceite o risco de leve corte/variação de tom entre elas (é a limitação deste método; prefira o Método A sempre que puder regravar).
3. Casque a duração de cada áudio na janela da cena (texto do tamanho certo pra caber, já que não dá pra esticar o vídeo).
4. Merge com `adelay` por cena + `amix duration=longest` + **`apad`** (sem isso o `-shortest` corta o vídeo no tamanho da última fala) + `volume`.

## Lições da 1ª simulação real (2026-07-28, fluxo `documents-management`)
0. **Mapear os cortes de cena por contagem manual de frame (linha/coluna de um contact sheet) é frágil — erra por vários segundos.** Na 1ª rodada, mapeei "Representantes legais" pra começar em 24s; o corte real era **16s** (8s de erro!) — causou a queixa do Paulo de vídeo adiantado/narração atrasada. **Fix definitivo:** ao extrair frames pra mapear cenas, sempre gravar o **timestamp real** em cada imagem com `drawtext`:
   ```bash
   ffmpeg -i video.mp4 -vf "fps=2,scale=480:-1,drawtext=text='%{pts\:hms}':x=5:y=5:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6" -q:v 4 frames/t_%03d.jpg
   ```
   Cada miniatura mostra o próprio segundo — zero contagem manual, zero erro de offset. Vale o esforço extra de rodar a 2fps (ou mais fino perto de transições suspeitas) em vez de 1fps.
1. **Plano free normalmente NÃO usa vozes da Voice Library via API** — só as vozes **"premade"** (as que já vêm na conta, ex.: Bella, Roger, Sarah, Laura, Charlie, George, Callum, River) funcionam de graça pela API "de fábrica". Uma voz escolhida na Voice Library (categoria `professional`, community) costuma retornar **402 `paid_plan_required`** até fazer upgrade do plano — **mas isso não é garantido**: o dono de uma voz pode marcar `sharing.free_users_allowed: true` (visível em `GET /v1/voices/{id}`), liberando-a pro plano free mesmo sendo `professional`. **Nunca conclua bloqueio só pela categoria — teste com uma chamada real e barata primeiro** (ex.: `POST /v1/text-to-speech/{id}` com 2 palavras; 200 = liberada, 402 = bloqueada). Se vier 404 na consulta da voz, ela provavelmente ainda não foi **adicionada à conta** (Voice Library → "Add to my voices") — peça pro Paulo adicionar e teste de novo antes de assumir qualquer coisa. Mesmo raciocínio vale pra API de música (`music.compose()`): um pitfall antigo registrando "só plano pago" pode não valer mais numa conta que mudou de plano — **re-teste, não repita o pitfall como fato permanente.**
2. **Vídeo já existente (sem re-gravação): sincronia muda de direção.** Sem o script de gravação original, não dá pra "esticar a pausa do cursor". A técnica vira: **escrever a narração do tamanho certo pra caber na janela da cena já existente** (medida via extração de frames + contact sheet), em vez de ajustar o vídeo. Cenas isoladas muito curtas (ex.: uma tela de transição de ~1s) ficam **sem narração** (silêncio, permitido pelo estilo) — não force uma frase apertada nelas; deixe a fala da cena vizinha "respirar" até ali se sobrar um pouco de tempo.
3. **`amix duration=longest` só olha os ÁUDIOS de entrada, não o vídeo.** Se a última fala terminar antes do fim do vídeo, `-shortest` no mux final corta o VÍDEO no tamanho do áudio (perde os últimos segundos). Fix: `apad` no fim da cadeia do `amix` (preenche com silêncio) antes do `-shortest`, garantindo que a trilha final seja pelo menos do tamanho do vídeo.
4. **QA de silêncio/fala por trecho: sempre `-ss`/`-t` ANTES do `-i` (seek de entrada).** Rodar `volumedetect` com `-ss`/`-to` DEPOIS do `-i` (seek de saída) deu leitura errada — mostrou o mesmo volume num trecho mudo e num trecho falado (o filtro processou o arquivo inteiro, não só o trecho). Com seek de entrada (`-ss X -t Y -i arquivo`), o silêncio real apareceu como **-91dB** (chão digital) contra **-13dB** no trecho falado — a forma confiável de verificar sincronia sem precisar "ouvir" o áudio.

## Lições da 3ª simulação real (2026-07-29, fluxo `invoice-flows`/cancelamento-fatura)
5. **Voz nova pedida pelo usuário: sempre testar na hora, não confiar em memória de sessão anterior.** A voz `6aDn1KB0hjpdcocrUkmq` deu 404 na 1ª checagem (não estava na conta ainda); depois de adicionada via Voice Library, categoria `professional` — testei geração real (2 palavras) e veio 200 (`free_users_allowed:true` do dono da voz). Sem esse teste real, eu teria trocado pra voz fixada por engano, contrariando um pedido explícito do Paulo pra essa voz específica.
6. **Música de fundo com `music.compose()` funcionou nesta conta** (mesma chamada que a referência antiga marcava como "só paga") — gerado com sucesso (`musicLengthMs:70000`, prompt lo-fi instrumental, ~70s reais). Ducking real via `sidechaincompress` (voz como key) + volume base -24dB validado por `volumedetect`: ~-19dB nas falas vs ~-38/-41dB nas janelas de ação (só música tocando) — bem abaixo da voz, como o Paulo pediu ("não sobreponha").
7. **ffmpeg: reusar o MESMO label do filtergraph como input em 2 filtros diferentes exige `asplit` explícito** (`[voice]asplit=2[voice_for_duck][voice_for_mix]`) — usar `[voice]` direto no `sidechaincompress` E no `amix` final deu o erro `Stream specifier 'voice' in filtergraph description ... matches no streams` (cita o grafo inteiro, não a linha certa). Detalhe completo (isolamento por mini-teste) em `codigo-ao-video.md` pitfall #37.

## Avatar-bolha + legendas em tela (2026-07-30, novo — export narrado)
Duas capacidades novas do export **narrado** (o mudo/loop do site não muda). Ambas compostas via **ffmpeg no merge final**, reaproveitando os mesmos tempos por cena já usados pro cursor (Método A: offsets de caractere no `alignment`; Método B: janela de cada clipe por cena) — zero sincronia nova pra inventar.

**Por que não é um avatar com rosto real:** investigado a pedido do Paulo (queria usar um ID específico como "avatar"). Achado real, confirmado no **OpenAPI ao vivo da própria API** (`https://api.elevenlabs.io/openapi.json`, não só a doc/blog):
- A ElevenLabs **tem** uma feature real de avatar com lip-sync (**Avatars**, dentro do **ElevenCreative**) — não é invenção.
- Mas **não existe endpoint de API pública pra gerar esse vídeo** — a doc oficial diz literalmente "API access: not available at launch; planned for future release". O único endpoint com "avatar" no spec é `POST /v1/convai/agents/{agent_id}/avatar` ("Post Agent Avatar"), que só faz **upload de uma imagem estática** pro widget de chat de um agente conversacional — não gera vídeo nenhum, e o formato de `agent_id` (`agent_xxxxxxxxxxxx`) nem bate com um ID de voz.
- É **feature paga** ("Avatars are available on all paid plans") — não funciona no plano free.
- Testado na prática: o ID passado pelo Paulo não correspondeu nem a `GET /v2/voices/{id}` nem a `GET /v1/convai/agents/{id}` desta conta (404 nos dois) — não dava pra usar mesmo se houvesse API.
- **Conclusão prática:** enquanto a API não existir, o avatar é gerado por código (bolha-monograma, ver abaixo) OU, se o Paulo quiser o rosto real, existe um **processo de handoff manual formal** (Fase 2.5 do Golden Path, `.claude/agents/codigo-ao-video.md`):
1. Assim que a narração for aprovada, **exporte o áudio (mp3) e entregue ao Paulo ANTES de gravar a tela** — é o novo primeiro entregável quando ele sinalizar que quer avatar real (não espere ele pedir 2x).
2. Ele sobe esse áudio no painel da ElevenLabs (Avatars/ElevenCreative), escolhe o avatar do catálogo, gera o vídeo com lip-sync de verdade, baixa e devolve o arquivo/caminho.
3. **O áudio final vem embutido nesse clipe** — não gere/mixe áudio próprio de novo pro export narrado quando for esse o caminho (mux direto, sem `adelay`/`amix`/`apad`).
4. A composição final NÃO é mais um overlay fixo de canto — é uma **coreografia animada** (abertura em split-screen metade-a-metade → encolhe suave pro canto ~1-3s depois de começar a falar → cresce de volta metade→tela cheia no fechamento). Detalhe técnico completo (incl. como replicar easing tipo GSAP no ffmpeg) em `.claude/agents/codigo-ao-video.md` → "Avatar REAL (handoff manual ElevenLabs) — coreografia de tela".
5. **Sempre entregue o áudio/vídeo DENTRO do projeto do usuário**, nunca só em `scratchpad` da sessão — pitfall #48, veio de um caso real (Paulo não conseguiu abrir o vídeo porque ele só existia num caminho de sandbox temporário).

**Avatar-bolha (o que É implementado):**
1. Círculo com o **monograma** (inicial do narrador — ex. "E" de Eduarda) em cores do <EMPRESA>, **não** uma tentativa de rosto real — honestidade sobre o que é simulado (mesmo princípio do pitfall #1 do agente: nada de fingir realismo que não existe).
2. 2 loops curtos, transparentes (webm VP9 `yuva420p`), renderizados 1x (reusáveis entre projetos): **idle** (glow lento, toca o vídeo todo) e **falando** (anel pulsando mais rápido — só indicador visual de "está falando", não lip-sync de verdade).
3. Composição no merge final: `overlay` do idle fixo (`x=24:y=main_h-h-24`) + `overlay` do falando por cima, `enable='between(t,S1,E1)+between(t,S2,E2)+…'` com os mesmos `S`/`E` de cada janela de fala já calculados.

**Legendas em tela:**
4. Texto = a MESMA narração aprovada; tempo = o MESMO `alignment` (nunca um recálculo à parte).
5. Quebrar em legendas curtas (1-2 linhas, ~35-42 char/linha) usando os offsets de caractere do `alignment` pra achar o tempo exato de cada pedaço — não a cena inteira de uma vez se for longa.
6. Gerar **`.vtt`** (também vira `<track kind="captions">` de acessibilidade no `<video>` do site) **e** queimar a mesma legenda no `video_narrado.mp4` via `subtitles=arquivo.vtt:force_style=...` (fundo semi-opaco) — o queimado garante legenda em qualquer lugar que o mp4 for parar (apresentação, WhatsApp), o `.vtt` garante acessibilidade real no player do site.
7. Cuidado de posicionamento pra legenda não sobrepor a bolha do avatar (canto inferior esquerdo) — confira no frame antes de aprovar.

## Guardrails (segurança/ética)
- **Nunca clonar a voz de uma pessoa real** — o ElevenLabs tem **Instant Voice Cloning** como recurso nativo do produto (cria uma voz a partir de uma gravação curta), o que torna esse risco real e fácil de acionar sem querer. Use **sempre uma voz da Voice Library** (stock), nunca clone a partir de gravação de alguém, a menos que o Paulo peça de forma explícita e a pessoa clonada tenha autorizado por escrito.
- **A narração nunca inventa comportamento** que o app não faz — mesma regra do vídeo mudo: se o roteiro descrito pelo usuário não bate com o que o código realmente faz, **sinalize a divergência antes de gravar/narrar**; não "conserta" narrando o que deveria acontecer.
- **Narração só é gerada depois da aprovação do texto** — nunca chame a API com um texto que o Paulo não viu/aprovou antes.

---
name: animacao-de-personagem
description: "Especialista em animação de PERSONAGEM/mascote — os 12 princípios clássicos da Disney aplicados a quadro a quadro (não a motion de UI), processo de produção (model sheet, turnaround, keys, in-betweens), e a decisão prática entre redesenhar quadro a quadro vs. rigar a ilustração (cutout/skeletal) pra animar no app. Use para 'anima o mascote', 'faz o mascote pular/comemorar/reagir', 'quadro a quadro dessa ilustração', 'rig dessa ilustração pra animação', 'qual ferramenta usar pra animar o mascote no app', 'walk cycle do personagem', 'quantos quadros preciso pra essa ação'. Complementa (não substitui) a skill `animation-principles` já instalada (essa é motion de UI: easing/duração/stagger de botão, modal, transição — não personagem)."
---

# Animação de Personagem — do princípio clássico ao quadro a quadro do mascote

Isso é sobre fazer um **personagem se mover com vida** (respirar, pular, comemorar, reagir) — diferente de animar um botão ou modal. É a base pra qualquer trabalho de movimento de mascote ou personagem ilustrado.

## As duas camadas de movimento (não confundir)

| Camada | O que é | Skill |
|---|---|---|
| **Motion de UI** | Botão, modal, toast, transição de tela — elemento de interface entrando/saindo | `animation-principles` (já instalada) |
| **Animação de personagem** | O mascote respirando, pulando, comemorando, com peso e personalidade | **esta skill** |

Um mascote dentro de um app usa as duas: os princípios de personagem definem *como ele se move com vida*; o motion de UI define *quando e com que ritmo ele entra na tela*. Esta skill cobre a primeira camada — a que faltava.

## Os 12 princípios clássicos, na versão de personagem (não de UI)

A skill de UI já instalada trata esses princípios como easing/timing de interface. Na origem (Ollie Johnston & Frank Thomas, *The Illusion of Life*, Disney, 1981), eles são sobre desenho e peso de um corpo:

1. **Squash & Stretch** — volume constante: achatou mais largo, fica mais baixo; esticou mais alto, fica mais fino. O principio mais importante pra vida orgânica.
2. **Anticipation** — o personagem se prepara antes de agir (agacha antes de saltar, olha antes de virar). Sem isso, a ação parece um corte, não um movimento.
3. **Staging** — a pose tem que ser legível em silhueta preta sólida. Uma ideia clara por cena, sem ambiguidade.
4. **Straight ahead vs. pose to pose** — straight ahead (quadro a quadro sequencial) pra ação orgânica/imprevisível (fogo, água, pelo ao vento); pose to pose (poses-chave primeiro, depois preenche) pra atuação/gestos controlados. A maioria do trabalho de mascote é pose to pose.
5. **Follow through & overlapping action** — nada para ao mesmo tempo. Orelha/rabo/bochecha continuam se movendo depois que o corpo já parou.
6. **Slow in / slow out** — mais desenhos perto das poses-chave, menos no meio do movimento. Aceleração e desaceleração natural (nunca velocidade constante).
7. **Arc** — quase todo movimento orgânico segue uma curva, não uma linha reta. Cabeça, braço, olhar — tudo em arco.
8. **Secondary action** — ação de apoio que nunca compete com a principal (o rabo balança enquanto ele anda; a expressão muda enquanto ele fala).
9. **Timing** — quantidade de quadros pra uma ação define peso e emoção. Poucos quadros = leve/rápido; muitos quadros = pesado/lento.
10. **Exaggeration** — empurrar além do real pra ganhar clareza e carisma (não é distorção, é amplificação da essência do movimento).
11. **Solid drawing** — mesmo em 2D, o personagem existe num volume 3D. Evitar poses simétricas ("twins") — elas parecem sem vida.
12. **Appeal** — carisma no design e no movimento: silhueta forte, assimetria, proporções agradáveis. É por isso que dá gosto de olhar.

> Fonte de referência ampliada (144 variações desses princípios por domínio/ferramenta/papel): repositório [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles) — a skill instalada hoje (`animation-principles`) é uma versão condensada dele, focada em UI. Se precisar de uma variação específica (ex.: como aplicar num jogo, em Rive, em Lottie), o repo completo tem um arquivo dedicado por combinação.

## Fluxo de produção clássico

Não se anima um personagem do zero a cada cena — se constrói uma referência primeiro:

1. **Model sheet / turnaround** — o personagem visto de frente, ¾, perfil, ¾ de trás e de trás, numa pose neutra. É o que garante que a anatomia (proporção da cabeça, espessura do traço, formato das orelhas) não varie de uma ilustração pra outra — evita o problema comum de variações que "afinam" a espessura do traço ou erram a anatomia entre gerações.
2. **Expression sheet / pose sheet** — o mesmo personagem em 6–8 emoções (neutro, feliz, triste, surpreso, comemorando, pensando) e em gestos típicos. É o catálogo de onde toda animação puxa poses-chave.
3. **Thumbnails** → **Keys** (poses que contam a história) → **Breakdowns** (definem o arco entre as keys) → **In-betweens** (completam o movimento) → **Clean-up** (traço final). Teste constantemente "passando" os quadros — se não parece vivo passando rápido, não vai parecer vivo no app.

## Timing prático: quantos quadros preciso?

- **Animar em 1s** = 1 desenho novo por frame (24/s a 24fps) → ação rápida/detalhada. Caro.
- **Animar em 2s** = 1 desenho novo repetido 2x (12 desenhos únicos/s a 24fps) → padrão pra 90% do movimento de personagem. Metade do custo, quase imperceptível.
- **Animar em 3s** = ainda mais econômico, só pra fundo/elementos secundários que não são foco.
- Regra prática: **em 2s** por padrão, **em 1s** só no momento de destaque (o "hero moment" — ex. a comemoração de meta batida), nunca em 3s pro próprio mascote (ele é o que o usuário está olhando).

| Ação do mascote | Quadros únicos (a 12fps "em 2s") | Duração |
|---|---|---|
| Blink (piscar) | 2–3 | ~150–250ms |
| Idle/respiração (loop) | 6–8 | ~1.5–2s por ciclo |
| Wave (aceno) | 6–10 | ~1–1.5s |
| Bounce/celebrate | 8–12 | ~1–1.5s |
| Walk cycle completo | 8 (clássico) | ~0.8–1s por ciclo |
| Sad/droop (erro) | 5–8 | ~0.8–1.2s |

### Walk cycle, se o mascote andar
O ciclo de caminhada clássico tem 4 poses-chave que se repetem: **contact** (pé na extensão máxima — a pose mais importante, define 80% do resto), **recoil** (ponto mais baixo, encaixa sem in-between pra não ficar "mole"), **passing/breakdown** (perna da frente estica, perna de trás passa, corpo sobe), **high point** (ponto mais alto). Ciclo tradicional: 8 quadros. ([the Angry Animator](http://animationhelper.blogspot.com/2010/02/walk-cycles-angry-animator.html), [Wikipedia](https://en.wikipedia.org/wiki/Walk_cycle))

## A decisão central: redesenhar quadro a quadro vs. RIGAR a ilustração

Frame-by-frame "de verdade" (redesenhar/regerar cada quadro) é o método clássico, mas pra um mascote de app é caro e — se cada quadro for gerado por IA independentemente — tem problema de **consistência** (traço, proporção, cor mudam quadro a quadro). O padrão de mercado pra mascote de produto (Duolingo, Mailchimp) não é redesenhar cada quadro: é desenhar/gerar **uma ilustração limpa**, separá-la em camadas e **rigar** (esqueleto/malha) pra animar por interpolação.

**Quando usar cada abordagem:**
- **Rig (cutout/skeletal)** — padrão pra tudo que roda dentro do app: idle, wave, bounce, reações de estado. Consistente por definição (é a mesma arte, só movida), arquivo pequeno, reaproveitável.
- **Frame-by-frame de verdade** — só pra um momento hero isolado (vídeo de campanha, GIF de celebração one-off) onde vale o custo de desenhar/gerar quadro por quadro com controle de consistência.

### Como rigar uma ilustração flat (cutout)
1. Separar a ilustração em camadas: cabeça, corpo, cada braço/perna, rabo, orelhas — cada parte que precisa de movimento independente na sua própria camada, com sobreposição nas juntas (ex.: o ombro "por baixo" do braço) pra não abrir buraco quando gira.
2. Montar um esqueleto (bones) sobre as camadas — cada bone controla uma parte, com hierarquia (o bone da mão é filho do bone do braço).
3. Animar por pose-chave sobre o esqueleto (interpolação faz o resto) — os 12 princípios acima ainda valem: anticipation antes do bounce, follow-through no rabo, arc na trajetória do salto.

**Ferramentas e quando usar cada uma** (relevante pro Duo, que é Expo/React Native):

| Ferramenta | Pontos fortes | Pra Expo/React Native |
|---|---|---|
| **Rive** | Arquivo minúsculo (~2KB típico), state machine embutida (o mascote reage a input em tempo real: toque, sucesso, erro), sem precisar de After Effects | `rive-react-native` — melhor opção se o mascote precisa *reagir* a eventos do app, não só tocar um loop |
| **Lottie** (After Effects + Bodymovin, ou direto no editor) | Formato JSON leve, ecossistema maduro, fácil de exportar de After Effects | `lottie-react-native` ou `dotlottie-react-native` (Expo-ready) — melhor opção se a animação é mais "cena pronta" (loop de celebração) do que interativa |
| **Spine / Live2D** | Rig mais profundo pra personagens complexos (jogos, animação facial rica) | Overkill pra a maioria dos mascotes de app; considerar só se a ambição for animação facial muito expressiva |

Trade-off resumido: Rive vence em tamanho de arquivo e interatividade; Lottie vence em maturidade de ecossistema e produção via After Effects. ([Callstack, Lottie vs Rive](https://www.callstack.com/blog/lottie-vs-rive-optimizing-mobile-app-animation))

## Formato de output: por que Lottie por padrão (nunca SVG animado, nunca vídeo/GIF dentro do app)

Essa é a decisão que define como todo trabalho desta skill deve ser entregue — não é uma opção entre várias, é a referência padrão daqui pra frente.

| Formato | iOS/React Native nativo | Tamanho típico | Reage a estado em tempo real? | Quando usar |
|---|---|---|---|---|
| **Lottie** (JSON, export de After Effects/Rive) | Sim — `lottie-ios`/`lottie-react-native`/`dotlottie-react-native` | 5–20KB (uma animação que em vídeo pesaria 100MB fica em ~800KB–2MB) | Não nativamente (dotLottie ganhou "state machines" no fim de 2025, ainda recente) | **Padrão pra 90% dos casos**: idle, celebrar, loading, tristeza, onboarding |
| **Rive** (`.riv`) | Sim — `rive-react-native` | ~2KB + state machine embutida | Sim, nativamente (IK, reage a toque/progresso em tempo real) | Só o(s) momento(s) mais tocado(s), quando o mascote precisa reagir de verdade (ex.: olho seguindo o dedo) |
| **SVG animado** | **Sem suporte nativo no iOS** — só via WKWebView | Pequeno, mas o motor re-rasteriza a cada frame (custoso) e tem bugs conhecidos de gatilho no Safari (`begin="click"` não funciona) | Limitado | Evitar dentro do app nativo/RN; só serve numa página web fora do app |
| **GIF** | Sim, mas cru (sem transparência de qualidade) | Centenas de KB a MB | Não | Só onde não dá pra rodar um player (e-mail) ou conteúdo descartável |
| **Vídeo (mp4/webm)** | Sim, player nativo | MB mesmo curto | Não | B-roll/marketing/onboarding cinematográfico — nunca um elemento de UI que reage a estado |

**Padrão real de mercado (Duolingo):** Lottie pra praticamente todas as animações do app; o comportamento mais interativo do próprio Duo (reagir ao progresso, seguir o cursor no hover) é feito em Rive especificamente. Não é "escolha um dos dois" — é **Lottie por padrão, Rive só onde compensa o esforço extra de interatividade**.

**Pra o Duo (Expo/React Native, possível build web):** exportar como Lottie (`lottie-react-native` ou `dotlottie-react-native`, Expo-ready, roda em iOS+Android+web via `lottie-web`/`dotlottie-web` sem duplicar asset) é o padrão. Migrar uma animação específica pra Rive só quando o mascote precisar reagir a evento em tempo real, não só tocar um loop pronto.

## Se a ilustração-base for gerada por IA (via `mcp__magnific`, já conectado neste hub)

O problema de "cada quadro sai diferente" que a indústria resolve em 2026 com seed fixo + ControlNet + IP-Adapter/referência de estilo tem equivalente direto nas tools já disponíveis (ver skill `ilustrador`):

- **`images_generate` com `references[]` tipo `character`** — mantém o mesmo personagem consistente entre gerações. É o equivalente prático ao "seed + reference" que substitui redesenhar cada pose do zero.
- **`images_variations`** sobre a ilustração-base — gera ângulos/expressões derivados de UMA arte aprovada. Isso *é* o expression sheet/turnaround, gerado automaticamente em vez de desenhado à mão.
- Nunca gerar cada pose como um prompt independente sem referência — é exatamente o que quebra a espessura do traço e a anatomia (ver `[[feedback-mascote-espessura-linha]]` e `[[feedback-anatomia-gatos-ilustracao]]`, já registrado em memória). Gere a partir da mesma referência, depois rig.

## Mapeando estados do mascote a momentos do app

Mascotes de produto de sucesso (Duo da Duolingo, Freddie do Mailchimp) não têm "uma animação" — têm um pequeno catálogo de estados que cobrem os momentos reais do produto:

| Estado do mascote | Momento no app |
|---|---|
| Idle/respiração | Tela em repouso, sem interação |
| Wave/boas-vindas | Onboarding, primeiro acesso |
| Thinking/loading | Carregando dado, aguardando IA |
| Celebrate/bounce | Meta batida, ação concluída com sucesso |
| Sad/droop | Erro, estado vazio, algo deu errado |

O high-five do Freddie no primeiro envio de campanha do Mailchimp é o exemplo clássico de transformar um momento genérico ("ação concluída") num pico emocional específico — vale pensar em qual momento do produto merece esse tratamento (geralmente: a primeira vez que o usuário completa a ação principal do app).

## Fontes

- Ollie Johnston & Frank Thomas, *The Illusion of Life: Disney Animation* (1981) — origem dos 12 princípios
- [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles) — 144 variações dos 12 princípios por domínio/papel/ferramenta (inclui a persona `animator-traditional`, usada como base do fluxo de produção acima)
- [Walk cycle — Wikipedia](https://en.wikipedia.org/wiki/Walk_cycle); [the Angry Animator, walk cycles](http://animationhelper.blogspot.com/2010/02/walk-cycles-angry-animator.html)
- [Character Sheets — CGWire](https://blog.cg-wire.com/character-sheet-animation/); [Character Design Sheet — CharacterHub](https://characterhub.com/blog/character-resources/character-design-sheet)
- [Exposure sheet — Wikipedia](https://en.wikipedia.org/wiki/Exposure_sheet); [Animating on Ones, Twos & Threes — iD Tech](https://www.idtech.com/blog/what-does-animating-on-ones-twos-and-threes-mean)
- [Live2D/Spine/Rive cutout rigging — Grokipedia](https://grokipedia.com/page/Live2D)
- [Consistência de personagem por IA em 2026 — prompting.systems](https://prompting.systems/blog/creating-consistent-characters-in-ai-art); [ControlNet + IP-Adapter](https://dreamaishort.com/blog/controlnet-for-ai-drama-precision-character-posing-guide/)
- [Lottie vs Rive — Callstack](https://www.callstack.com/blog/lottie-vs-rive-optimizing-mobile-app-animation); [dotlottie-react-native](https://github.com/LottieFiles/dotlottie-react-native)
- [Duolingo — case study LottieFiles](https://lottiefiles.com/case-studies/duolingo); [Duolingo migrando pra Rive no mascote interativo — DEV](https://dev.to/uianimation/want-duolingo-style-interactive-animation-in-your-app-stop-using-lottie-heres-how-with-rive-5247)
- [Lottie vs GIF — tamanho/performance](https://lottiewizard.com/lottie-vs-gif); [Lottie vs Rive vs CSS 2026 — PkgPulse](https://www.pkgpulse.com/guides/lottie-vs-rive-vs-css-animations-web-animation-formats-2026)
- [SVG sem suporte nativo no iOS, só via WKWebView — Apple Developer Forums](https://developer.apple.com/forums/thread/70686); [bugs de SVG animado no Safari/iOS — SVGator](https://www.svgator.com/help/animation-and-interactivity/how-to-fix-svg-animation-lag-in-safari)
- [O efeito Duolingo — ziggle.art](https://ziggle.art/the-duolingo-effect); [Mascotes e UX — Raw.Studio](https://raw.studio/blog/how-mascots-improve-user-experience/)

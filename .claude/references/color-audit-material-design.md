# Auditoria de cores do <PRODUTO> vs. Material Design 3

> Gerado em 2026-07-30. Auditoria completa do agente principal (não é output de
> A1/A3/A4 — trabalho ad-hoc solicitado pelo Paulo; ver `melhorias.md` M39, que
> apontava a falta de um dono formal pra esse tipo de auditoria).
>
> **Atualização 2026-07-30 (rodada 4 — composição real em 5 telas):** ver seção
> "I. Auditoria de composição em telas reais" e "J. Paleta final de migração
> (unificada, calibrada por composição real)" no fim deste documento — supersede
> os valores "propostos" das seções B/C/D onde divergirem.

## Método

- Fonte da verdade: código real do <PRODUTO> (`webclient/src/assets/scss/themes/`),
  não Figma nem doc.
- Contraste calculado com a MESMA fórmula WCAG 2.1 do
  `.claude/skills/codigo-ao-figma/references/wcag-contrast.py` já existente no hub
  (luminância relativa sRGB → ratio `(L1+0.05)/(L2+0.05)`).
- Limiares: **4.5:1** texto normal · **3.0:1** texto grande/ícone/borda/foco ·
  **isento** estados disabled (WCAG 1.4.3).
- Fundos reais do produto usados na medição: `#ffffff` (card, `--background-primary`)
  e `#f8f8f8` (canvas do app — `.eb-base-box` em `BaseTemplate.vue:90`, hoje só
  acessível via `--ath-color-light` legado; nunca formalizado no sistema novo).
- Vocabulário de papéis emprestado do Material Design 3 (`m3.material.io/styles/color/roles`):
  `surface`/`surface-container-*` para camadas de fundo, `outline`/`outline-variant`
  para bordas (funcional vs. decorativo — só `outline` precisa 3:1).

## Inventário de sistemas (contexto, não repetir aqui — ver `figma-ds-reuse-map.md` → "DECISÃO CRÍTICA")

3 sistemas de cor coexistem no código: **novo** (`--content-*`/`--background-*`/`--border-*`,
79 arquivos), **legado** (`--ath-color-*`, 324 arquivos, 43 misturam com o novo),
e uma **cópia solta** no app Svelte (`frontend/public-routes/.../colors.scss`,
mesmos valores do legado sem prefixo `ath-`).

---

## A. Content (texto) — sistema novo

| Token | Valor | Contraste vs. card/canvas | Veredito |
|---|---|---|---|
| content-primary | #1a1a1a | 17.4 / 16.4 :1 | ✅ |
| content-secondary | #333333 | 12.6:1 | ✅ |
| content-tertiary | #666666 | 5.7 / 5.4:1 | ✅ |
| content-disabled | #b2b2b2 | 2.1:1 | isento (disabled) |
| content-brand | #6b55d8 | 5.4:1 | ✅ |
| content-link / link-hover | #3355ff / #2944cc | 5.4 / 7.5:1 | ✅ |
| content-info / info-bold | #3355ff / #2944cc | 5.4 / 7.5:1 | ✅ |
| **content-warning** (base) | #cca300 | **2.4:1 ❌** | só ícone/borda (3:1); texto = `content-warning-bold` |
| content-warning-bold | #665200 | 7.6:1 | ✅ |
| **content-risk** (base) | #ff8000 | **2.5:1 ❌** | só ícone/borda; texto = `content-risk-bold` |
| content-risk-bold | #994d00 | 6.2:1 | ✅ |
| content-danger (base) | #e50000 | 4.85:1 | ✅ (único "base" que passa como texto) |
| content-danger-bold | #b70000 | 7.0:1 | ✅ |
| **content-success** (base) | #009933 | **3.75:1 ❌ como texto** (passa como ícone, ≥3:1) | texto = `content-success-bold` |
| content-success-bold | #007a29 | 5.5:1 | ✅ |

**Regra emergente #1** — os tokens semânticos "base" (warning/risk/success — danger
é a exceção que passa) só servem para ícone/borda (limiar 3:1); qualquer uso como
TEXTO CORRIDO deve usar a variante `-bold`. Não muda nenhum valor — é regra de uso,
cobre 3 tokens de uma vez.

## B. Background sólido + texto/ícone branco em cima — sistema novo

| Token | Valor atual | Contraste | Fix proposto | Contraste do fix |
|---|---|---|---|---|
| background-brand | #6b55d8 | 4.79:1 ✅ | — | — |
| **background-danger** | #e50000 | **4.33:1 ❌** | `red-600` #b70000 (já é o hex de `background-danger-hover`) | 6.22:1 ✅ |
| **background-success** | #009933 | **3.35:1 ❌** | `green-600` #007a29 (já é o hex de `background-success-hover`) | 4.92:1 ✅ |
| background-info | #3355ff | 4.83:1 ✅ | — | — |
| **background-notice** | #ff8000 | **2.25:1 ❌** (pior caso) | `orange-700` #994d00 (2 degraus, não 1 — `orange-600` ainda reprova a 3.43) | 5.49:1 ✅ |

## C. Background "subtle" (tint) + texto em cima — badges/tags

| Estado | Contraste com token BASE | Contraste com token `-bold` |
|---|---|---|
| danger | 3.36:1 ❌ | **4.84:1 ✅** |
| success | 2.93:1 ❌ | 4.30:1 ❌ (quase — precisa `green-700` #005c1f, não `green-600`) → **6.44:1 ✅** |
| info | 4.03:1 ❌ | **5.60:1 ✅** |
| warning | 2.18:1 ❌ | **6.92:1 ✅** |
| notice/risk | 2.09:1 ❌ | **5.11:1 ✅** |

**Regra emergente #2** — toda `background-*-subtle` deve ser usada SÓ com o
`content-*-bold` correspondente, nunca com a cor base (cobre 5 badges de uma vez
com zero mudança de valor). Única exceção: o par success precisa também trocar
`content-success-bold` para `green-700` **especificamente neste contexto de fundo
claro** (no fill sólido do item B, `green-600` já basta) — ou seja, o "bold" de
success tem 2 valores possíveis dependendo do fundo. Deixado explorável no
artefato, não travado numa única resposta.

## D. Border / outline — sistema novo

| Token | Valor atual → proposto | Contraste (canvas #f8f8f8 / card #fff) | Papel M3 |
|---|---|---|---|
| **border-primary** | #b2b2b2 → **neutral-450 #8c8c8c** | 2.00❌/2.12❌ → **3.17✅/3.36✅** | outline (funcional) — único valor que muda |
| border-secondary | #cccccc (mantém) | isento | outline-variant (decorativo) |
| border-tertiary | #d9d9d9 (mantém) | isento | outline-variant sutil |
| border-disabled | #e5e5e5 (mantém) | isento | disabled |
| border-brand | #6b55d8 | 5.4:1 ✅ | — |
| border-focus | #5644ad | 7.4:1 ✅ | — |
| border-info | #3355ff | 5.4:1 ✅ | — |
| **border-warning** | #cca300 | **2.38:1 ❌** | precisa `yellow-700` #997a00 (4.09✅) ou `yellow-800` #665200 (7.58✅) — único border semântico reprovado hoje |
| border-danger | #e50000 | 4.85:1 ✅ | — |
| border-success | #009933 | 3.75:1 ✅ | — |

Só **1 token de neutro muda** (`border-primary`) e **1 token semântico** precisa
reforço (`border-warning`) — os outros 3 neutros (secondary/tertiary/disabled)
ficam exatamente como estão, porque no Material só o "outline" funcional precisa
de 3:1; "outline-variant" (divisor decorativo) e "disabled" são isentos por
definição.

## E. Background canvas/surface (empilhamento) — gap de token, não de contraste

| Token | Valor | Papel M3 | Situação hoje |
|---|---|---|---|
| **background-canvas** (novo) | `neutral-50` #f2f2f2 | surface (base do app) | Hoje só existe como `#f8f8f8` via `--ath-color-light`, puxado só pelo `BaseTemplate.vue` — nunca formalizado no sistema novo. Também corrige `--app-background-color`, que referencia `--ath-link`, uma variável **nunca definida em lugar nenhum do repo** (confirmado por grep). |
| background-primary (mantém) | white | surface-container-lowest (o card "elevado") | sem mudança |
| **background-surface-high** (novo) | `neutral-150` #d9d9d9 | surface-container-high | gap real, 0 usos hoje — aditivo puro |
| **background-surface-highest** (novo) | `neutral-200` #cccccc | surface-container-highest | gap real, 0 usos hoje — aditivo puro |

## F. Estados "inverse" (seção de fundo escuro) — conferido, sem problema

`content-primary/secondary/tertiary-inverse` e `border-inverse` sobre
`background-inverse` (neutral-900): 8.2 a 15.5:1 — tudo folgado. Nenhuma ação.

## G. Sistema LEGADO `--ath-color-*` — **é aqui que está o pior, e é o mais usado**

| Token legado | Valor | Contraste | Veredito |
|---|---|---|---|
| ath-color-success | #2ecc71 | **2.10:1 ❌** | bem pior que `content-success` (3.75) do sistema novo |
| ath-color-info | #3b83f4 | **3.66:1 ❌** | pior que `content-info` (5.41) |
| ath-color-warning | #efca44 | **1.59:1 ❌** | o pior de todos os tokens medidos |
| ath-color-warning-dark | #c5a533 | **2.39:1 ❌** | mesmo o "reforço dark" reprova |
| ath-color-risk | #d98609 | **2.85:1 ❌** | reprova |
| ath-color-danger | #e50000 | 4.85:1 ✅ | único que passa (mesmo hex do novo) |
| **ath-color-secondary-500** (label de texto real, em produção) | #7d8097 | **3.88:1 ❌** | texto secundário legado é hoje inacessível |
| ath-color-secondary-900 | #002a3a | 15.1:1 ✅ | ok |
| ath-color-primary-500 (ícone/link legado) | #ae9eff | **2.30:1 ❌** (min 3.0) | reprova como ícone |
| ath-border-color (=secondary-300) | #e3e4e9 | 1.27:1 | isento SE só decorativo — confirmar uso real antes de assumir |

**Achado-chave da auditoria**: o sistema legado (usado em 324/403 arquivos, mais
que o dobro do novo) reprova em **7 dos 10** tokens semânticos medidos — é
sistematicamente pior que o sistema novo, e é o que tem mais superfície de risco
real em produção hoje.

## H. Terceiro sistema (Svelte `public-routes`)

Duplica os mesmos valores do legado sem prefixo `ath-` (`--color-secondary-*`,
`--color-primary-*`) — mesmo diagnóstico da seção G se aplica; não é paleta
diferente, é cópia manual desatualizável.

## Achados colaterais confirmados (não são o foco desta auditoria, só registro)

- `--background-warning-subtle` declarado 2x em `root.scss` (linhas 55 e 58, mesmo valor).
- `--ath-link` referenciado em 4 lugares, nunca definido — variável órfã.
- `dark.scss` redefine `--ath-color-primary/secondary-*` com valores IDÊNTICOS ao
  `:root` — dark mode não afeta essas cores (dead code ou feature incompleta).
- Possível drift `Red/500`: doc (`design-tokens.md`) registra `#EB5757`, código
  (`_educ_colors.scss`) tem `#e50000` — já apontado como M2 no backlog.
- `--background-warning` sólido não existe (só a versão `-subtle`) — gap já
  mapeado em `figma-ds-reuse-map.md`, fora do escopo desta rodada.

## Cross-referência com backlog existente

Confirma e quantifica com números reais: **M2** (drift danger/warning), **M5**
(cores de feedback falham contraste), **M-A10-1** (5 variantes do EdsButton
falham WCAG AA — bate com os achados B/C acima), **M-A10-2** (anel de foco —
`border-focus` aqui mediu 7.4:1, ok, então esse ponto specific do M-A10-2 pode
ter sido corrigido desde a medição original — vale conferir), **M-A10-10/11**
(bordas sem token/contraste — resolvido pela seção D). **M39** (gap de agente
dono desta auditoria) — endereçado por este documento.

## Resumo do que muda de fato (reaproveitando o que já existe — zero hex novo)

1. `--border-primary`: `neutral-300` → `neutral-450`
2. `--border-warning`: precisa reforço (`yellow-700` ou `yellow-800`)
3. `--background-danger`: `red-500` → `red-600` (hex já usado em `-hover`)
4. `--background-success`: `green-500` → `green-600` (hex já usado em `-hover`)
5. `--background-notice`: `orange-500` → `orange-700`
6. `content-success-bold` em contexto de badge: considerar `green-700` (vs. `green-600` no fill sólido)
7. 3 tokens novos aditivos: `--background-canvas`, `--background-surface-high`, `--background-surface-highest`
8. 2 regras de uso (sem mudar valor): "base" semântico só ícone/borda, texto sempre `-bold`; `*-subtle` sempre com `*-bold`
9. Sistema legado (`--ath-color-*`) é o que precisa de atenção real — 7/10 tokens reprovam

Ver o artefato interativo (`DS Color Playground`) para explorar cada opção
aplicada em componentes reais antes de fechar os valores definitivos.

---

## I. Auditoria de composição em telas reais (rodada 4)

Telas analisadas (leitura real do código, não amostra): **InvoiceList** (lista de
Faturas), **NewViewInvoice/AthCard** (detalhe de Fatura), **AcademicClassList**
(Turmas/Matrículas), **HomeView** (Dashboard), **MonthlyNegativationList**
(Negativação).

**Achado 1 — a borda mais usada na prática nem é `--border-primary` (novo), é a
legada.** `--ath-border-color` (= `--ath-color-secondary-300` = `#e3e4e9`, ainda
mais clara que `--border-primary` #b2b2b2) é a borda de fato aplicada em
`EdsTable` (moldura da tabela + divisor header/corpo + divisor de linha),
`AthCardNavigator`, `AthCardEnrollmentGuide`, `AthAlertBar`, `AthPanelDescription`,
`AthHr`, `AthCardButtonSimple` — ou seja, praticamente todo card/tabela/painel
estrutural do produto. Ela reprova ainda pior (1.27:1) que `border-primary`.
**Decisão: unificar as duas num único token novo, `Border/Default`.**

**Achado 2 — confirmado: escurecer borda sobre fundo pastel (selecionado/hover)
ajuda, não atrapalha.** Linha selecionada de tabela (`#f3f1ff`) e card
"highlight" da Home (`#f3f1ff`) mantêm a borda cinza padrão sem override —
hoje ela quase some (tons quase idênticos); `Border/Default` (neutral-450,
`#8c8c8c`) passa em TODOS os fundos reais encontrados, inclusive esse pastel
(3.02:1, a margem mais apertada de toda a auditoria, mas passa).

**Achado 3 — 1 caso real de "borda clara demais contra o próprio fundo"
(exatamente o que o Paulo descreveu):** badge `.plan-zerodefault`
(`_utilities.scss`, tipo de cobertura na tabela de Faturas) — borda `#eae6ff`
sobre fundo `#f3f1ff`, mesma família, quase invisível hoje. Fix: manter a
borda DENTRO da família roxa (não trocar por cinza genérico, pra não perder a
identidade do badge) — `brand-400` `#8977e0` passa (3.26:1) sobre esse fundo;
um degrau abaixo (`brand-300`) ainda reprova (2.26:1).

**Achado 4 — o maior risco real de acessibilidade do produto está no badge de
status (`AthTag`), usado em Faturas/Home/Negativação.** Ele usa o sistema
legado inteiro (bg `-light` + texto na cor base) e **reprova em todos os 5
estados reais** medidos direto do componente (não em teoria — são os hex que
realmente renderizam hoje):

| Estado real | bg (hoje) | texto (hoje) | Contraste hoje | Texto corrigido | Contraste corrigido |
|---|---|---|---|---|---|
| Vencida/Erro (danger) | #fdeeee | #e50000 | 4.30:1 ❌ | `red-600` #b70000 | 6.19:1 ✅ |
| Pendente (risk) | #feeed9 | #d98609 | 2.50:1 ❌ | `orange-700` #994d00 | 5.40:1 ✅ |
| Paga (success) — **pior de toda a auditoria** | #eafaf1 | #2ecc71 | **1.95:1 ❌** | `green-700` #005c1f | 7.62:1 ✅ |
| Em criação/Aberta (info) | #e9f3fe | #3b83f4 | 3.26:1 ❌ | `blue-600` #2944cc | 6.70:1 ✅ |
| Aviso (warning, já usa a variante "dark") | #fdfaec | #c5a533 | 2.28:1 ❌ | `yellow-800` #665200 | 7.24:1 ✅ (yellow-700 ainda reprova, 3.90) |
| Cancelada/neutro (grey) | #e3e4e9 | #7d8097 | 3.06:1 ❌ | `secondary-600`/`neutral-600` #575e6a/#666666 | 5.15:1 ✅ |

Correção é **só no texto** (mantém o mesmo fundo pastel de hoje — visual quase
idêntico, zero choque na forma do badge, só o texto fica um pouco mais escuro).

**Achado 5 — 1 caso que NÃO se resolve mudando valor de token (é bug de
composição do componente, não da paleta).** `AthCard.vue` (usado no modal de
detalhe de Fatura, ação "o que você quer fazer"): nos estados `:hover` e
`.active`, o fundo vira roxo sólido hardcoded (`#6b55d8`/`#2b2256`), mas a
borda continua `var(--border-primary)`/`var(--ath-color-primary-500)` (cinza
claro / lilás claro) — uma borda neutra sobre um fill saturado é
estruturalmente invisível, **não importa o quão escura a borda seja**. Não
entra na lista de tokens; fica registrado como item de código a corrigir
quando o componente for migrado (remover a borda nesses 2 estados, já que o
`box-shadow` já indica elevação).

**Achado 6 (menor, code hygiene, fora do escopo de paleta):** `HomeHeader.vue`
usa hex hardcoded `#f3f1ff` em vez do token `--ath-color-primary-50` — mesmo
valor, só não usa a variável. Registrado, não é um problema de paleta.

## J. Paleta final de migração (unificada, calibrada pela composição real)

Princípios da migração: (1) atende o mínimo de acessibilidade (WCAG 2.1 AA);
(2) sempre o MENOR ajuste suficiente (nunca escurece/satura mais que o
necessário — testado contra TODOS os fundos reais encontrados nas 5 telas,
não só branco); (3) unifica sistema novo + legado num único valor por papel
(o legado deixa de ter escala própria — vira alias do novo); (4) é uma troca
de **valor de token** (cascata automática via CSS custom property) em quase
todos os casos — só o `AthCard` (achado 5) precisa de toque de código além do
token.

Ver a lista completa e final na próxima seção (nomenclatura para design).

## K. Lista final — nova paleta de tokens (nomenclatura para design)

Nota sobre nomenclatura: substituído `content-*` por `Text/*` (mais claro pra
design) e unificado `content-risk`/`background-notice` — mesma família laranja,
nomes diferentes hoje — num único `Risk`. Inglês mantido por ora; tradução pra
português é avaliação de backlog, não decidida agora. Sistema legado
(`--ath-color-*`) retirado — todo papel dele foi absorvido por um nome único
abaixo (a maior mudança prática é o `Border / Default`, que substitui tanto
`--border-primary` quanto `--ath-border-color`).

**Ajuste fino 2026-07-31 — Border/Default não é pra tudo que hoje usa a mesma
variável legada.** Ao ver o resultado aplicado no `EdsTable` (divisor de linha),
Paulo achou `Border/Default` (#8c8c8c) forte demais pra um divisor decorativo —
comparei com o `outline`/`outline-variant` reais do Material 3 (baseline: outline
#79747E ≈ 4.55:1, bem mais forte que o nosso; outline-variant #CAC4D0 ≈ 1.70:1,
bem mais discreto) e confirmei: o papel "divisor decorativo" no Material fica
próximo de 1.5–1.8:1, não perto do mínimo funcional de 3:1. Fix: divisor de LINHA
de tabela agora usa `Border / Subtle` (#cccccc, ~1.44–1.61:1 nos fundos reais) —
token que já existia, não é valor novo. `Border / Default` continua correto para
moldura/cabeçalho (estrutural) e pra qualquer borda que realmente define um
limite que precisa ser percebido (input, card, select). Regra geral daqui pra
frente: **antes de aplicar Border/Default num lugar que hoje usa
`--ath-border-color`/`--border-primary`, perguntar se aquele uso é estrutural ou
decorativo** — só o primeiro caso usa Border/Default; o segundo usa Border/Subtle
(ou Border/Faint, se for ainda mais discreto). Aplicado por ora só no divisor de
linha do `EdsTable`; extensão pros outros componentes (accordion, painéis) fica
pendente de aprovação do Paulo.

### Text Color
| Token | Hex |
|---|---|
| Text / Primary | #1a1a1a |
| Text / Secondary | #4d4d4d |
| Text / Tertiary | #666666 |
| Text / Disabled | #b2b2b2 |
| Text / Brand | #6b55d8 |
| Text / Link | #3355ff |
| Text / Link Hover | #2944cc |
| Text / Link Pressed | #1f3399 |
| Text / Info | #3355ff |
| Text / Info Strong | #2944cc |
| Text / Risk | #ff8000 |
| Text / Risk Strong | #994d00 |
| Text / Warning | #cca300 |
| Text / Warning Strong | #665200 |
| Text / Danger | #e50000 |
| Text / Danger Strong | #b70000 |
| Text / Danger Deep | #2e0000 |
| Text / Success | #009933 |
| Text / Success Strong | #005c1f |
| Text / Success Deep | #001f0a |
| Text / Inverse | #f2f2f2 |
| Text / Inverse Secondary | #e5e5e5 |
| Text / Inverse Tertiary | #b2b2b2 |

### Background Color
| Token | Hex |
|---|---|
| Background / Canvas | #f2f2f2 |
| Background / Surface | #ffffff |
| Background / Surface High | #d9d9d9 |
| Background / Surface Highest | #cccccc |
| Background / Hover | #f2f2f2 |
| Background / Pressed | #e5e5e5 |
| Background / Selected | #e1ddf7 |
| Background / Disabled | #f2f2f2 |
| Background / Inverse | #1a1a1a |
| Background / Brand | #6b55d8 |
| Background / Brand Hover | #5644ad |
| Background / Brand Pressed | #403382 |
| Background / Info | #3355ff |
| Background / Info Subtle | #d6ddff |
| Background / Risk | #994d00 |
| Background / Risk Subtle | #ffe6cc |
| Background / Warning Subtle | #fff5cc |
| Background / Danger | #b70000 |
| Background / Danger Hover | #890000 |
| Background / Danger Pressed | #5c0000 |
| Background / Danger Subtle | #facccc |
| Background / Danger Outline Hover | #ffebeb |
| Background / Danger Outline Pressed | #f59999 |
| Background / Success | #007a29 |
| Background / Success Hover | #005c1f |
| Background / Success Pressed | #003d14 |
| Background / Success Subtle | #ccebd6 |
| Background / Success Outline Hover | #e2fcea |
| Background / Success Outline Pressed | #99d6ad |

### Border Color
| Token | Hex |
|---|---|
| Border / Default | #999999 |
| Border / Moderate | #a6a6a6 |
| Border / Subtle | #cccccc |
| Border / Faint | #d9d9d9 |
| Border / Disabled | #e5e5e5 |
| Border / Brand | #6b55d8 |
| Border / Brand Subtle | #8977e0 |
| Border / Inverse | #f2f2f2 |
| Border / Focus | #5644ad |
| Border / Info | #3355ff |
| Border / Risk | #994d00 |
| Border / Warning | #997a00 |
| Border / Danger | #e50000 |
| Border / Success | #009933 |

### Overlay Color
| Token | Hex |
|---|---|
| Overlay / Scrim | rgba(0,0,0,0.5) |
| Overlay / Scrim Inverse | rgba(255,255,255,0.5) |

## M. Auditoria de papel de token (role) + fonte da verdade migrada pro artefato (2026-07-31)

**Pedido do Paulo:** auditar se algum token de um papel (Text/Background/Border)
foi aplicado num componente que carrega outro papel — ex.: token de TEXTO usado
como FUNDO. "Não tem problema criar token, o problema é token ambíguo."

**Achados confirmados (já corrigidos no artefato):**
- `EbTippy` e `AthRibbon` ("dark") citavam `Text/Primary` pro FUNDO do
  tooltip/ribbon → criado **Background/Inverse** (#002a3a — mesmo hex do
  Text/Primary, papel de token diferente).
- `EdsTable`/`AthInputCheckbox` citavam `Text/Brand` pro preenchimento do
  checkbox (`accent-color`, não é texto) → criado **Control/Accent** (#6b55d8).
- `AthLoading` citava `Text/Brand` pro spinner (na verdade `border-color` de
  um anel giratório) → corrigido pra **Border/Brand** (token que já existia,
  só estava mal aplicado).
- `AthWizard` colapsava 3 papéis (texto do rótulo, borda do círculo, fundo do
  pontinho) sob 1 rótulo `Text/Brand` → separado em Text/Brand · Border/Brand
  · Background/Brand.

**Novos tokens formalizados nesta rodada:** `Border/Hover` (#737373, neutral-550
— reação de borda no hover, nenhum campo tinha antes) · `Control/Accent`
(#6b55d8) · `Background/Inverse` (#002a3a).

**Drift descoberto entre este doc e o artefato real (pendente de reconciliar):**
o artefato (usado e aprovado por Paulo em dezenas de abas ao longo do rollout)
usa `Text/Success-Strong` = **#007a29** e `Text/Primary` = **#002a3a** — valores
diferentes dos registrados na Seção K abaixo (`#005c1f` e `#1a1a1a`,
respectivamente). A Seção K ainda não foi atualizada com os valores reais;
tratar como a próxima reconciliação.

**Fonte da verdade da paleta migrou pro artefato.** A partir de 2026-07-31, a
lista viva e atualizada de tokens não é mais só esta Seção K — é a aba
**"Paleta de Cores"** dentro do próprio artefato `DS Color Study` (grupo topo,
ao lado de "Princípios"): blocos de cor grandes, organizados por categoria,
atualizados a cada token criado/alterado/removido. Esta Seção K continua como
registro histórico da auditoria original, mas em caso de divergência, o
artefato manda.

**Padrão de foco definido (2026-07-31):** campo de formulário (`.box` — texto,
select, data, upload) = anel **PRA DENTRO**, colado na própria borda
(`outline-offset:-3px`). Controle avulso (botão, checkbox, chip, card, aba,
popover) = anel **PRA FORA**, sempre com **2px de distância**
(`outline-offset:2px`), sempre na cor de foco do DS — nunca uma cor de chrome
de ferramenta. Exceção: elemento com preenchimento sólido usa o halo duplo
(ver M-A10-2) em vez do anel único.

## L. Ajustes finos 2026-07-31 (pedido direto do Paulo, pós-artefato)

**1. Border/Default e Border/Moderate — testado mais claro, REVERTIDO.** Paulo
pediu pra testar `Border/Default` (#8c8c8c) e `Border/Moderate` (#999999) um
degrau mais claros (pra #999999/#a6a6a6). Depois de ver o número real (caía do
mínimo formal de contraste não-textual, 3:1, pra ~2.85/2.43), ele decidiu
explicitamente **manter os padrões de acessibilidade** — reversão aplicada no
mesmo dia. Valores finais continuam `Border/Default` #8c8c8c (3.36:1) e
`Border/Moderate` #999999 (2.85:1), sem mudança líquida. Registrado aqui só
pra histórico da decisão (testamos, medimos, o Paulo preferiu manter o piso
de acessibilidade) — não é mais um item em aberto.

**2. Text/Secondary reforçado pra diferenciar título de subtítulo.** Paulo notou
que título (`Text/Primary` #1a1a1a) e um texto de apoio em `Text/Secondary`
(antes #333333, neutral-800) liam quase iguais — os dois muito escuros, sem
distância perceptual real (17.4:1 vs. 12.6:1, ambos "quase preto"). Fix:
`Text/Secondary` #333333→**#4d4d4d** (neutral-800→700, 8.45:1 contra branco) —
ainda com folga confortável acima do mínimo de 4.5:1, mas com separação visual
real do `Text/Primary`, aproximando o papel do `on-surface-variant` do Material
Design 3 (mid-tone, claramente distinto do `on-surface`). `Text/Tertiary`
(#666666, 5.74:1) não muda — a escala fica com 3 degraus mais bem distribuídos:
17.4 → 8.45 → 5.74, em vez de 17.4 → 12.6 → 5.74 (onde o salto real estava
escondido só entre secondary e tertiary). Ainda não usado em nenhuma aba
construída até aqui — vale como padrão pra qualquer componente futuro que
diferencie título/subtítulo.

## N. Padrão de NOMENCLATURA de token + auditoria de CRUZAMENTO (2026-07-31)

Duas rodadas pedidas pelo Paulo no mesmo dia: (1) fechar o naming "de uma vez
por todas", porque nomes como `Brand 50` misturavam registro com `Brand`; (2)
antes de renomear, **simular os cruzamentos de cor que acontecem no dia a dia**
pra descobrir se faltava token — o exemplo dele: "e se o Border/Focus estiver em
cima de outra cor e perder visibilidade?".

### N.1 — Regra de nomenclatura (destilada de 14 fontes)

Pesquisa em 6 artigos (Nathan Curtis/EightShapes · Wicar Akhtar · Slnktarun ·
Yamini Yanamala · Tetrisly/Andrew Mialszygrosz · Design Systems Collective ·
Smashing) + doc oficial de 8 DS (Material 3, Atlassian, Polaris, Carbon,
Spectrum, Primer, ColorArchive, Adobe Design). **Convergência quase unânime:**

1. **Número de escala só no nível primitivo.** `blue-500`/`neutral-450` é rampa
   crua; o nível que a UI consome descreve INTENÇÃO (`Text/Error`). Misturar os
   dois registros no MESMO nível é o erro nº1 citado. Era exatamente o nosso caso
   (`Brand 100` e `Brand 50` no meio de `Brand`/`Brand Subtle`).
2. **1 hex = 1 nome canônico POR CATEGORIA DE PAPEL** (Texto/Borda/Fundo/
   Controle). Reuso do mesmo valor em outra categoria é normal e esperado (é o
   modelo Atlassian: `color.text.brand` e `color.border.focused` podem ter o
   mesmo valor) — o que não se faz é colar 2 papéis num rótulo só
   (`Brand Hover / Border-Focus`). Reuso vira **nota**, nunca 2º nome.
3. **1 separador só por tipo de relação.** Barra (`/`) = Categoria/Papel
   (`Text/Primary`). Espaço = família + modificador (`Success Strong`). Nunca
   hífen pra mesma relação que o espaço já cobre — tínhamos `Success-Strong`
   (hífen) convivendo com `Success Subtle` (espaço) nos 5 grupos semânticos.

### N.2 — Renomeações aplicadas (só rótulo; nenhum hex mudou)

| Antes | Depois | Regra ferida |
|---|---|---|
| Brand 100 | **Brand Focus Inner** | 1 (número no nível de papel) |
| Brand 50 / Selected | **Brand Selected** | 1 + 2 |
| Brand Hover / Border-Focus | **Brand Strong** (ver N.3) | 2 (2 papéis num rótulo) |
| Success-Strong | **Success Strong** | 3 (separador) |
| Danger-Strong | **Danger Strong** | 3 |
| Warning-Strong | **Warning Strong** | 3 |
| Risk-Strong | **Risk Strong** | 3 |
| Info-Strong | **Info Strong** | 3 |

### N.3 — Auditoria de cruzamento: 1.296 pares (36 primeiros planos × 36 fundos)

Método: script `cruzamento.py` (mesma fórmula WCAG 2.1 do resto da auditoria),
cruzando cada token de primeiro plano contra **todo fundo que existe de fato na
plataforma** — não só branco/canvas, mas também hover, linha selecionada, pastel
de badge, preenchimento sólido (marca e semântico, nos 4 estados), fundo inverso
e o scrim do modal. Limiar por papel: 4.5 texto · 3.0 borda/ícone/foco.

**Achado 1 (o que o Paulo intuiu — o mais grave). `Border/Focus` #5644ad
desaparece em 7 fundos reais**, porque o anel precisa contrastar com a
**vizinhança**, não com o elemento:

| Vizinhança | Contraste | Onde acontece |
|---|---|---|
| Brand Hover #5644ad | **1,00:1** (mesmo hex) | card de ação sob o mouse + foco por teclado |
| Danger Strong fill #b70000 | 1,07:1 | botão danger focado |
| Background/Brand #6b55d8 | 1,39:1 | preenchimento de marca |
| Brand Pressed #403382 | 1,40:1 | marca no clique |
| Success Strong fill #007a29 | 1,35:1 | botão success focado |
| Overlay/Scrim ~#808080 | 1,88:1 | área escurecida do modal |
| Background/Inverse #002a3a | 2,03:1 | tooltip (EbTippy), ribbon "dark" |

O halo duplo (M-A10-2) cobre só o caso "elemento preenchido numa página CLARA" —
o anel externo escuro depende de a página ser clara. **Fix: papel novo
`Border/Inverse` = #f2f2f2 como anel em fundo escuro/preenchido** — é a única
borda que passa em TODOS os preenchimentos (3,35 a 13,47:1); nenhuma borda cinza
passa em nenhum. Em fundo escuro o halo **inverte** (traço claro por fora). Hex
já existia (é o Text/Inverse) — faltava o papel.

**Achado 2 — a família Brand era a ÚNICA sem degrau "Strong", e isso quebrava
texto de marca sobre fundo claro de marca.** Todas as outras famílias tinham
(Success/Danger/Warning/Risk/Info Strong). Resultado: `Brand` #6b55d8 como texto
reprova em 3 fundos claros — Brand Subtle #eae6ff (**4,41:1**), Brand Focus Inner
#e1ddf7 (4,06), Background/Pressed #e5e5e5 (4,26). Ex. real: rótulo roxo dentro
de chip/faixa/trilho roxo claro. **Fix: `Brand Strong` = #5644ad** (5,62 a 7,43:1
nos 8 fundos claros do sistema). Hex já existia (era o hover do preenchimento e o
anel de foco) — faltava o nome do papel de texto. Isso **estende a Regra
emergente #2** ("`*-subtle` sempre com `*-bold`") pra família de marca, que tinha
ficado de fora da rodada original.

**Achado 3 — a borda do botão de CONTORNO desaparece no clique.** O fundo
escurece no `:active` mas a borda ficava na cor de repouso:
`Border/Success` #009933 sobre Success Outline Pressed #99d6ad = **2,24:1**;
mesmo padrão no danger (#e50000 sobre #f59999 = 2,29:1). **Fix sem token novo:
no estado pressionado a borda vira a variante Strong** (#007a29 → 3,30:1;
#b70000 → 3,28:1). Único estado em que o componente perdia a própria forma.

**Achado 4 — hierarquia de texto claro só existe sobre fundo inverso.**
`Text/Inverse` #f2f2f2 passa nos preenchimentos da paleta nova, mas
`Inverse Secondary` #e5e5e5 e `Inverse Tertiary` #b2b2b2 reprovam em quase todo
preenchimento colorido (1,77 a 4,37:1). **Regra: sobre preenchimento colorido, só
Text/Inverse**; os 3 níveis claros valem apenas sobre `Background/Inverse`.

**Achado 5 — o scrim não aceita texto nenhum.** Sobre `Overlay/Scrim` (≈#808080
composto no branco) nenhum tom passa 4,5:1 — nem claro (3,53) nem escuro (3,82).
**Regra: nunca texto direto sobre o scrim** (em vez de inventar token pra isso).

**Achado 6 — `Text/Tertiary` reprova sobre pastel de marca** (#e1ddf7 → 4,34:1) e
nos pressed de contorno. **Regra: ali usa `Text/Secondary`** (4,94:1).

**Achado 7 (decisão de design, PENDENTE do Paulo) — o badge some na linha sob o
mouse.** Todos os pastéis de badge dão 1,00 a 1,22:1 contra Surface/Canvas/Hover/
Brand Selected; o pior é Info Subtle #e9f3fe sobre Background/Hover #f2f2f2 =
**1,00:1** (a pílula desaparece, sobra texto solto). **Não é falha WCAG** (o texto
carrega o sentido e passa) — é perda de forma/affordance justamente quando a
pessoa vai interagir. Opção levantada: contorno na cor da família (Border/Info
etc.), ou só quando o badge está sobre linha em hover/selecionada. **Aguarda
escolha do Paulo** — registrado em `melhorias.md`.

### N.4 — Saldo

**Zero hex novo entrou no sistema.** Os 2 papéis criados (`Brand Strong`,
`Border/Inverse` como anel de foco) reaproveitam valores que já estavam na escala
— o que faltava era o **nome do papel**, não a cor. Além deles, 4 tokens que
existiam na Seção K mas não estavam na paleta viva do artefato foram registrados:
`Text/Inverse`, `Border/Inverse`, `Border/Faint`, `Border/Disabled`. E 4 regras de
uso novas (achados 3, 4, 5, 6), todas sem mudar valor.

### N.5 — Confronto com o código real (2026-07-31, pós-mapeamento read-only)

Depois de fechar a Seção N, mapeei o código pra montar a spec de implementação. **Duas
suposições minhas foram desmentidas** — registradas aqui porque mudam a conclusão:

1. **A pílula pastel das tabelas NÃO é o `AthTag`.** É a classe global
   `.label-status-bg-table` (`_table.scss:40`). E o `AthTag` tem
   **`pointer-events:none`** (`AthTag.vue:84`), então qualquer solução de hover no
   próprio badge é impossível — a regra tem que descer da `<tr>`. Ponto único de
   implementação: `DataTableRow.vue:151-167`, com `:deep()` obrigatório (os badges vêm
   de `formatter` como string HTML, sem hash de scope).
2. **O texto de marca do legado é pior que o previsto.** A Seção N.3 apontou 4,41:1
   (Brand #6b55d8 sobre pastel). No código o roxo de texto real é
   `--ath-color-primary-700` = **#8a76eb**, que sobre #f3f1ff dá **≈2,6:1** —
   `AthTag.vue:80`, `_table.scss:326`, `DebtsTabContacts.vue:214`. `Brand Strong`
   resolve os dois casos.

**Confirmações fortes que o código deu:**
- **`--border-inverse` já existe** (`root.scss:85`, #f2f2f2) e está **MORTO — zero
  consumidores** em todo o `webclient/src`. O token que resolve o achado 1 estava
  declarado e nunca foi usado.
- **`--border-focus` (`root.scss:87`) e `--background-brand-hover` (`root.scss:52`) são
  a mesma primitiva `$brand-600`** — o 1,00:1 é estrutural, não coincidência.
- `--border-risk` e `--border-notice` **não existem**; `--border-warning`
  (`root.scss:89`) é #cca300, que reprova a 2,38:1.

**Achados novos, fora do escopo de paleta** (viraram M65/M66/M67): 6 anéis de foco
apontando pra `--ath-color-primary-200`, **nunca declarada**, com fallback renderizando
`#6366f1` (indigo do Tailwind) em 5 lugares · reset global
`_input.scss:84-91` com `outline:0 !important` matando o foco de **todo** input do
produto (bloqueia qualquer token novo) · `AthRibbon.dark` com texto ≈1,3:1.

**Spec de implementação:** `.claude/references/ds-color-implementation-spec.md` — todos
os pontos com `arquivo:linha`, valor antes → depois e ordem de execução. `<PRODUTO>/`
segue read-only; quem aplica é o time de dev.

**Onde ver:** aba **"Cruzamentos"** do artefato `DS Color Study` (grupo topo, ao
lado de Princípios e Paleta de Cores) — cada achado num componente real, com o
estado interativo de verdade (Tab no card, clique-e-segure no botão de contorno).
Script da simulação: `cruzamento.py` (scratchpad da sessão; reproduzível).


## O. Nomenclatura `Categoria/PapelCamelCase` + 8 tokens novos (2026-08-01)

**Gatilho:** ao construir a aba "Papéis de Cor" (mapa de color roles do M3
aplicado aos nossos tokens), o Paulo notou que células como "sobre Risco" e
"sobre Alerta" **não tinham token** — eram rótulos de posição na matriz, não
nomes. Pediu para garantir token para todo caso de uso da página, em inglês,
no estilo `OnBackground`.

**Decisões dele (AskUserQuestion):** escopo **completo** (novos + renomeações +
correções de categoria) e padrão **`Categoria/PapelCamelCase`**.

### O.1 — O diagnóstico (3 problemas, 1 causa)

1. **As 7 famílias não tinham CATEGORIA no nome.** `Brand`, `Success Strong`,
   `Danger Subtle` não diziam se eram texto, fundo ou borda — e o mesmo hex
   fazia mais de um trabalho. Exemplo: `#007a29` estava descrito como *"texto e
   ícone pequeno"* mas é o **preenchimento** do botão success no padrão. A regra
   2 da Seção N.1 (1 hex = 1 nome por categoria) pedia nomes separados.
2. **8 valores usados no lado "Padrão" sem nome nenhum** — todos os estados de
   hover/clique dos botões success e danger.
3. **O "on-fill" é UM valor só.** `#f2f2f2` passa nos 6 preenchimentos
   (4,79 a 6,77:1). O M3 precisa de 6 tokens `on*` porque cada fill dele é um
   tom diferente; o nosso é um. Criar `OnBrand`+`OnSuccess`+… todos `#f2f2f2`
   violaria a regra 2 → **1 token** (`Content/OnFill`), reuso vira nota.

### O.2 — Os 8 tokens novos (todos medidos, todos passam)

| Token | Hex | Papel | Contraste |
|---|---|---|---|
| `Background/DangerHover` | #890000 | botão danger sob o mouse | 9,09:1 |
| `Background/DangerPressed` | #5c0000 | botão danger no clique | 12,89:1 |
| `Background/SuccessHover` | #005c1f | botão success sob o mouse **e** texto do botão de contorno | 7,35 / 8,23:1 |
| `Background/SuccessPressed` | #003d14 | botão success no clique | 11,18:1 |
| `Background/SuccessSubtleHover` | #e2fcea | contorno success sob o mouse | 7,58:1 |
| `Background/SuccessSubtlePressed` | #99d6ad | contorno success no clique | 10,48:1 |
| `Background/DangerSubtlePressed` | #f7c9c9 | contorno danger no clique | 9,73:1 |
| `Content/OnSuccessSubtlePressed` | #001f0a | texto do contorno success no clique | 10,48:1 |

Isso **fecha o M68** (`#005c1f` sem nome).

### O.3 — Renomeações e correções (nenhum hex mudou)

- `Text/*` → **`Content/*`**, alinhando com o `--content-*` que o DS novo já usa
  no código. `Text/Inverse` → **`Content/OnFill`** (o nome passa a dizer o papel,
  não a aparência).
- Famílias ganham categoria: `Brand` → `Background/Brand` + `Content/Brand`;
  `Success Strong` → `Background/Success` + `Content/Success`; etc.
- **Correção de categoria:** `Brand Focus Inner` **não era fundo, era borda** —
  é o anel INTERNO do halo de foco (`box-shadow`). Virou **`Border/FocusInner`**.
  Mesma classe de erro que a Seção M pegou no `AthLoading`.
- **Papel que só existia como nota virou token:** `Border/SuccessPressed`
  (#007a29) e `Border/DangerPressed` (#b70000) — o achado 3 (a borda vira Strong
  no clique) nunca tinha nome.

### O.4 — ⚠️ Correção de um erro deste próprio documento e da paleta

A nota do token `Success` (#2ecc71) dizia *"Só passa contraste em texto/ícone
grande (≥24px)"*. **Medido: 2,10:1 contra branco** — reprova até o mínimo de
ícone (3:1). A nota do `AthPanelWarning` (*"falha até o mínimo de ícone"*)
estava certa e a da paleta errada. Renomeado para
**`Background/SuccessVivid`** com a nota corrigida: só decorativo, nunca
conteúdo. Mesma checagem aplicada aos outros valores base:

| Hex | Família | vs #fff | Serve como |
|---|---|---|---|
| #2ecc71 | Success | 2,10:1 | só decorativo |
| #efca44 | Warning | 1,59:1 | só decorativo |
| #d98609 | Risk | 2,85:1 | só decorativo |
| #3b83f4 | Info | 3,66:1 | apenas ícone / texto ≥24px |
| #e50000 | Danger | 4,85:1 | texto pequeno + ícone |
| #6b55d8 | Brand | 5,36:1 | texto pequeno + ícone |

### O.5 — Assimetria declarada, não escondida

Só **Marca, Sucesso e Perigo** têm conjunto de estados (hover/pressed) e
preenchimento — porque só eles são botão. **Alerta, Risco e Informação** existem
apenas como badge/texto, então **não têm `Background/*` de preenchimento**. Em
vez de inventar 15 tokens que nenhum componente consome, a matriz da aba
"Papéis de Cor" mostra a **célula vazia tracejada com "sem token"**. No dia em
que virarem botão, herdam o mesmo conjunto.

### O.6 — Saldo

**45 nomes → 61 nomes · 38 hex → 46 hex · 0 hex alterado.** A paleta viva no
artefato continua sendo a fonte da verdade (Seção M); esta seção registra a
regra e o raciocínio.

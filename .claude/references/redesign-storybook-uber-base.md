# Redesign do Storybook — padrões da Uber Base

> Spec dos padrões de documentação da **Uber Base** (base.uber.com, a partir dos prints do Paulo) + **plano** para aproximar o nosso Storybook. Dono do doc: A9 `storybook-builder` (assets/direção visual = A2 `design-studio`). Código = fonte da verdade; specs continuam ancoradas no código.

## 1. Os padrões da Base (a spec)

**A. Header por componente (hero).** Cada página abre com: **rótulo de categoria** (ex.: "Action") pequeno acima → **título grande** ("Button dock") → **badge de status** ("Stable") → **descrição de 1 linha** → **banner ilustrado** (fundo escuro decorativo com um mockup do componente em contexto). O banner é próprio de cada componente.

**B. Tabs DENTRO da página.** Uma página só, com abas **Usage · Specs · Status & resources**. Separa "como usar" (humano) de "specs técnicas" de "status/recursos" — sem virar 3 páginas. Na sidebar, o componente expande nesses 3 sub-itens.

**C. Anatomia como IMAGEM anotada.** Não é lista de texto: é uma **imagem do componente** com **linhas/labels vermelhos** apontando partes ("Top spacing (optional)"). Visual, imediato.

**D. Do & Don't como IMAGENS.** Exemplos **visuais** (ex.: diagrama da ordem dos botões: "Secondary actions → Dismissive → Confirming", "farthest/closest to right"). Mostra, não descreve.

**E. Seções de apoio.** "Common alternative names", "Questions/feedback", "Resources & tools", **status/maturidade** por componente.

**F. Chrome do site.** Top nav (Foundation/Components/Patterns/Resources & tools) + busca + **theme switcher** (Light/Dark) + itens **restritos** (cadeado 🔒) + índice/ToC lateral por página.

**G. Layout editorial espaçoso** (muito respiro, tipografia forte) — que a nossa v2 já persegue.

## 2. Onde estamos (gap)
| Padrão Base | Nosso Storybook hoje |
|---|---|
| Anatomia = imagem anotada | **Texto** (token por parte) |
| Hero ilustrado por componente | **Não tem** |
| Tabs na página | Página única rolável (sem tabs) |
| Do/Don't visual | Texto (callout) |
| Badge de status | **Não tem** |
| Editorial espaçoso | ✅ já temos (v2) |
| Live component + props | ✅ temos (o que a Base NÃO tem — vantagem nossa) |

## 3. Viabilidade no Storybook (honesto) + como fazer
| Padrão | Como no Storybook | Esforço | Quem |
|---|---|---|---|
| **Badge de status** (Stable/Beta/WIP) | tag no topo do MDX, mapeada da maturidade do reuse-map | 🟢 baixo | A9 |
| **Nomes alternativos / Resources / Feedback** | seções MDX | 🟢 baixo | A10/A9 |
| **Hero por componente** | `<img>`/banner no topo do MDX | 🟡 imagem por componente (34×) | A2 cria · A9 wira |
| **Anatomia anotada (imagem)** | imagem feita no Figma → export → embed no MDX (texto vira complemento) | 🔴 alto (por componente) | A2 cria · A9 wira |
| **Do/Don't visual** | **preferir exemplo AO VIVO** (renderizar bom/ruim com o componente real) — barato e sincronizado; imagem só p/ nuance | 🟡 médio | A9 (+A2 nuance) |
| **Tabs na página** | Storybook Docs **não tem tab nativa** → (A) componente de tabs custom em MDX (engenharia) ou **(B) ToC/índice fixo + seções âncora** (mesma escaneabilidade, sem brigar com a ferramenta) | 🟡 B / 🔴 A | A9 |
| **Top nav / theme / busca** | Storybook já tem **sidebar + busca + theme**; top-nav horizontal é de site custom (fora do modelo) — theming aproxima | 🟢 já temos base | A9 |
| **Itens restritos (🔒)** | acesso por item ≠ modelo do Storybook | ⚪ pular/nota | — |

**Realidade estratégica:** a Base é um **site sob medida**, não Storybook. Padrões que encaixam natural (badge, seções, editorial, exemplo ao vivo) valem muito e são baratos. Os "caros" são **produção de imagem** (hero + anatomia + do/don't ilustrados) — trabalho de design por componente, não config. E **tabs de verdade** empurram contra o modelo do Storybook (custom).

## 4. Plano faseado
- **Fase 1 — Quick wins (alto impacto, sem produzir imagem):** badge de status · seções "nomes alternativos/resources/feedback" · **ToC/índice fixo** por página · **Do/Don't AO VIVO** (renderizar certo/errado com o componente real). Só engenharia (A9).
- **Fase 2 — Identidade visual:** **hero banner por componente** (começar **templado por categoria** — rápido; ilustração bespoke depois) · decidir tabs (custom) × ToC.
- **Fase 3 — Design-heavy:** **anatomia anotada como imagem** (flagships → todos) · do/don't ilustrados onde o "ao vivo" não basta. (A2 produz os assets; A9 embute.)

**Antes de escalar: 1 componente PILOTO "à la Base" completo** (hero + tabs/ToC + anatomia-imagem + do/don't) pra validar esforço × resultado — ex.: EdsButton.

## 5. Decisões do Paulo (definem o esforço)
1. **Tabs:** de verdade (custom, mais trabalho) **ou** ToC/índice âncora (mais rápido, mesma escaneabilidade)?
2. **Anatomia:** imagem anotada (design-heavy, cara da Base) **ou** texto + imagem simples do componente?
3. **Hero:** ilustração bespoke por componente (muito trabalho) **ou** banner templado por categoria (rápido, evolui depois)?
4. Começar pelo **piloto (EdsButton)** pra ver antes de escalar?

# Documentação de componentes de DS — melhores práticas (referência do A10)

> **Fonte de padrão que o Agente 10 (`documentacao-do-ds`) consome.** Material destilado de pesquisa (jul/2026):
> **[component.gallery](https://www.component.gallery/)** (agregador de 95 design systems, taxonomia de 60 componentes) + **12 artigos do Medium** verificados, com destaque para a série "Documenting Components" de **Nathan Curtis / EightShapes** (o padrão-ouro do tema).
>
> Este arquivo define **o QUÊ e o COMO** de uma boa documentação. O **conteúdo real** (props, tokens, estados) continua vindo do **código do <PRODUTO>** (fonte da verdade). Aqui está a *forma*, não a verdade do nosso DS — essa está em [`DS-KNOWLEDGE-INDEX.md`](DS-KNOWLEDGE-INDEX.md).

---

## Modelo de conteúdo canônico de uma página de componente

Ordem consolidada do cruzamento entre: estrutura do component.gallery (`Description → Markup → Styling → Usage guidelines → Related components → Resources`), os 4 blocos de Nathan Curtis (`Introduction · Examples · Design reference · Code reference`) e as features que os grandes DS realmente publicam.

| # | Seção | O que contém | Por que importa |
|---|-------|--------------|-----------------|
| 1 | **Overview / Propósito** (obrigatório) | 1–2 frases: o que o componente é e qual problema/ação resolve. | Define escopo; evita uso errado logo de cara. |
| 2 | **Status / Maturidade** | Rótulo (exploration → ready → stable → deprecated), plataformas, versão. | Deixa claro se dá pra confiar em produção. |
| 3 | **Quando usar / Quando NÃO usar** | Casos de uso + contra-indicações, pareados. Começar com gerúndio ("Exibindo…", "Quando precisar de…"). | Ajuda a **escolher entre componentes** parecidos (toast vs. alert, modal vs. drawer). |
| 4 | **Exemplos** (o centro do palco — obrigatório) | Componente **vivo** renderizado + snippet logo abaixo. Organizar por prioridade de variante, não 1:1 com props. | "Show don't tell" — o item **mais essencial** da doc (Curtis). |
| 5 | **Anatomia** | Diagrama rotulado das subpartes (container, label, ícone/slot, focus ring), com **token por parte**. | Elimina dúvidas de implementação; alinha Figma e código. |
| 6 | **Variantes** | Tipos/aparências (primary, secondary, destructive…) + quando usar cada. | Cobre a superfície de decisão sem forçar leitura de props. |
| 7 | **Estados** | default, hover, focus, active, pressed, disabled, loading, error — **todos visíveis e rotulados**. | Doc não pode ser "caça ao tesouro": estado escondido atrás de interação não se enxerga. |
| 8 | **Tamanhos** | Sizes (sm/md/lg) + regra de escolha. | Consistência dimensional entre telas. |
| 9 | **Comportamento / Interação / Motion** | Transições de estado, entrada/saída, animação. | Handoff claro de micro-interações. |
| 10 | **Conteúdo & UX writing** | Tom, comprimento de rótulo, capitalização, o que evitar. Beneficia-se de do/don't. | Voz consistente — o diferencial de Polaris/Paste. |
| 11 | **Acessibilidade** | Contraste, foco/teclado, roles/ARIA, leitor de tela, `visually-hidden`, skip-links. | Primeira classe, não apêndice (Carbon dedica aba inteira). |
| 12 | **Do's & Don'ts** | Pares "faça/não faça" **lado a lado**, ≤2 por linha, **com visual**. | Comparação visual é o que mais fixa a regra. |
| 13 | **Código / API (props)** (obrigatório se há código) | Tabela de props (nome, tipo, default, descrição), tabs por framework, snippet copiável. Tipos **enumerados**, não "string" genérica. | Código bem documentado dirige consistência (Curtis favorece engenheiros). |
| 14 | **Tokens usados** | Design tokens (cor/spacing/tipografia/radius) por papel. | Liga a doc ao sistema de tokens; evita hardcode; base de theming. |
| 15 | **Componentes relacionados** | Links para alternativas e componentes que compõem/são compostos. | Navegação e desambiguação. |
| 16 | **Changelog / Versão** | Semver (major=breaking, minor=adição, patch=fix) + o que mudou. | Rastreia mudanças/quebras; governança contra decaimento. |
| 17 | **Recursos / Footnotes** | Links externos, pesquisa, specs. | Aprofundamento sem poluir a página. |

**Regra de ordenação (Curtis):** `Introdução → Exemplos (centro do palco) → Guia de design → Referência de código`. **Uma única fonte da verdade por dado** — nunca sites separados de design e código que divergem.

---

## Padrões dos grandes DS (benchmark)

Catalogados em [component.gallery/design-systems](https://www.component.gallery/design-systems/) (95 sistemas). Frequência das *features* de doc publicadas — revela o que a indústria considera "seção padrão": **Code examples 79/95 · Usage guidelines 55 · Accessibility 27 · Tone of voice 20 · Research 2**. Ou seja: exemplos + guias de uso são quase universais; acessibilidade e tom de voz ainda são diferencial (oportunidade nossa).

| Design system | O que faz especialmente bem | Link |
|---|---|---|
| **IBM Carbon** | **Aba de acessibilidade dedicada** + tabs de código multi-framework; anatomia consistente. | https://carbondesignsystem.com |
| **Google Material 3** | **Diagramas de anatomia** + cobertura completa de estados e specs de comportamento. | https://m3.material.io |
| **Shopify Polaris** | **Content/voice guidelines** de primeira linha + best-practices e when-to-use por componente. | https://polaris.shopify.com |
| **Atlassian** | **Do/don't visuais** fortes + usage e content guidelines integrados. | https://atlassian.design |
| **Adobe Spectrum** | Tabela de **"Options"** detalhada, anatomia, teclado, i18n. | https://spectrum.adobe.com |
| **GOV.UK** | **"When to use / when not to use"** rigoroso, lastreado em **pesquisa** com usuários reais. | https://design-system.service.gov.uk |
| **GitHub Primer** | **Status/maturity labels** + múltiplas implementações na mesma página. | https://primer.style |
| **Twilio Paste** | Acessibilidade + **UX writing** por componente; forte em composição. | https://paste.twilio.com |

Benchmark de props/tokens: **Chakra, Ant Design, Base Web, Workday Canvas, Nord, Pajamas (GitLab), Gestalt (Pinterest), PatternFly**.

**Taxonomia canônica** (nomes-padrão do component.gallery — vocabulário compartilhado; cada componente lista *aliases* entre sistemas, ex.: Button ⊃ CTA / icon-button / FAB / close-button): Button · Button group · Segmented control · Toggle · Icon · Text input · Textarea · Search input · Select · Combobox · Checkbox · Radio · Slider · Datepicker · File upload · Form · Label · Rating · Navigation · Breadcrumbs · Pagination · Tabs · Stepper · Tree view · Link · Skip link · Card · Modal · Drawer · Popover · Accordion · Stack · Separator · Dropdown menu · Table · List · Badge · Avatar · Tooltip · Carousel · Heading · Alert · Toast · Progress bar · Spinner · Skeleton · Empty state · Visually hidden. **Ao documentar um componente nosso (`Ath*`/`Eds*`), mapeie-o ao nome canônico** para facilitar busca e benchmark.

---

## Princípios de escrita da documentação

- **Exemplo primeiro, prosa depois ("show don't tell").** Componente vivo + snippet abaixo. Não force exemplos a mapear 1:1 as props — organize pelo que *ensina*.
- **Conteúdo real, nunca lorem.** Use "Maria Silva / R$ 1.240,00", não "XXXX XXXXXX" — dado realista revela quebras de layout.
- **Imperativo e escaneável.** Verbos ("Oculte", "Inclua", "Evite"), "Sempre/Nunca" para inegociáveis, **listas > parágrafos**, ≤2 frases por diretriz, conselho **quantitativo** ("16px", não "espaçamento adequado").
- **Do/Don't sempre pareados e visuais**, ≤2 por linha.
- **Template repetível.** Toda página responde as mesmas perguntas (o que é / por que / quando / como) — previsibilidade reduz carga cognitiva.
- **Acessibilidade como primeira classe**, decisão de arquitetura, não item final.
- **Uma fonte da verdade.** Figma e código espelham a **mesma anatomia e o mesmo naming**.
- **Sincronizado com código/tokens.** Prop tables e tokens **gerados do código**, não à mão; foundations dos tokens, nunca hex digitado.
- **Progressive disclosure.** Intro/exemplos no topo; specs, código e a11y abaixo/em abas.
- **Naming pesquisável + aliases** (nome canônico + sinônimos).
- **"Funcional e cedo" bate "perfeito e atrasado"** (Harrison). Comece pelos componentes de maior uso/fricção.
- **Doc é produto vivo:** dono, versão, changelog, auditoria periódica.

---

## Figma vs Storybook — o que documentar em cada

Princípio: **mesma anatomia e naming nos dois**; dividir por o que cada ferramenta faz melhor. Regra prática — se muda quando o **código** muda, dono = Storybook; se é intenção/decisão de **design**, dono = Figma.

**No Figma (página de documentação / anotações):**
- Diagrama de **anatomia** rotulado (partes + token por parte).
- **Variantes, estados, tamanhos** como properties do component set, visíveis.
- **Do's & Don'ts** visuais lado a lado (imagens).
- **Quando usar / não usar** + guidelines de **conteúdo/UX writing**.
- **Tokens** vinculados às variáveis do Figma (nunca hex cru).
- **Comportamento/motion** e o "porquê" do design; link cruzado pro Storybook.

**No Storybook (MDX + Docs):**
- **Playground vivo** (Controls/args) — manipular props em tempo real.
- **Prop/API table auto-gerada** do código, multi-framework.
- **Snippets copiáveis** e uma story por variante/estado.
- **DocBlocks** de paleta/tipografia/ícones (foundations como fonte única).
- **Addon de acessibilidade** (axe) + interaction tests.
- **Changelog/versão**; integra Chromatic p/ regressão visual.

Overlap saudável (anatomia, variantes, estados, quando-usar, do/don't) existe nos dois — audiências entram por portas diferentes — mas com **origem canônica única** por dado (tokens/props vêm do código; intenção/conteúdo, do design).

---

## Checklist de qualidade de uma doc de componente

- [ ] Overview em 1–2 frases (o que é + o que resolve).
- [ ] Status/maturidade e versão visíveis.
- [ ] "Quando usar / quando NÃO usar" pareados.
- [ ] Exemplos vivos no topo + snippet copiável.
- [ ] Anatomia rotulada com token por parte.
- [ ] Variantes, estados (todos visíveis) e tamanhos.
- [ ] Comportamento/motion descrito.
- [ ] Conteúdo/UX writing (tom, rótulo, o que evitar).
- [ ] Acessibilidade (contraste, foco/teclado, ARIA/roles, leitor de tela).
- [ ] Do's & Don'ts visuais lado a lado.
- [ ] Prop/API table completa (tipo, default, tipos enumerados), multi-framework quando aplicável.
- [ ] Tokens usados por papel; zero hex/px cru.
- [ ] Componentes relacionados linkados.
- [ ] Changelog semver.
- [ ] Escrita imperativa, escaneável, conteúdo real, ≤2 frases/diretriz.
- [ ] Figma e código espelham a mesma anatomia/naming.
- [ ] Estrutura idêntica à dos outros componentes.
- [ ] Existe dono e cadência de revisão.

---

## Anti-padrões (o que NÃO fazer)

- Estados/variantes escondidos atrás de interação ("treasure hunt").
- Lorem ipsum / "XXXX" em vez de conteúdo real.
- Exemplos forçados a mapear 1:1 a lista de props.
- Sites separados de design e código que divergem.
- Prop tables e tokens mantidos à mão (dessincronizam).
- Hex/px cru em vez de token.
- Ensaios longos e jargão — diretriz deve ser ≤2 frases, imperativa, em lista.
- Do/Don't só textual (sem visual, sem pareamento).
- Acessibilidade como apêndice final.
- Conselho vago ("espaçamento adequado") em vez de quantitativo.
- Estrutura inconsistente entre componentes.
- Doc "one-time handoff" sem dono/versão/changelog.
- Buscar perfeição antes de publicar.

---

## Fontes — 12 artigos do Medium (verificados)

1. **Documenting Components** — Nathan Curtis (EightShapes) — https://medium.com/eightshapes-llc/documenting-components-9fe59b80c015 — 4 blocos (Introduction · Examples · Design reference · Code reference); ordem Intro→Exemplos→Design→Código; **uma página unindo design+código**.
2. **Component Examples** — Nathan Curtis (EightShapes) — https://medium.com/eightshapes-llc/component-examples-9c4b3bb3b308 — "Show don't tell"; todos os estados visíveis e rotulados; conteúdo real, nunca placeholder.
3. **Component Design Guidelines** — Nathan Curtis (EightShapes) — https://medium.com/eightshapes-llc/component-design-guidelines-eca706100e7c — "Use when / Don't use when"; imperativos, "Always/Never", ≤2 frases; Do/Don'ts ≤2 por linha.
4. **A Guide to Creating Design Components (Component Handbook)** — Sulakshana (Bootcamp) — https://medium.com/design-bootcamp/component-handbook-65d3001044ec — anatomia com visuais; cobrir default/hover/pressed/focused/disabled; do/don't comportamentais.
5. **Growing Design System Documentation** — Ben Maclaren (Bootcamp) — https://medium.com/design-bootcamp/growing-design-system-documentation-41fe81128c7a — várias camadas; co-criar com usuários reais; doc evolui progressivamente.
6. **How to Document Your Design System: A Comprehensive Guide** — Vadim Can — https://vadimcan.medium.com/how-to-document-your-design-system-a-comprehensive-guide-42300977f955 — por componente: definição + uso + convenções de código + exemplos visuais.
7. **Rich docs with Storybook MDX** — Michael Shilman (Storybook) — https://medium.com/storybookjs/rich-docs-with-storybook-mdx-61bc145ae7bc — DocBlocks (markdown + exemplos vivos); prop table auto-gerada; DocBlocks de tokens = fonte única.
8. **Versioning Design Systems: Best Practices** — Into Design Systems — https://intodesignsystems.medium.com/versioning-design-systems-best-practices-ca8508653480 — semver; changelog por versão; retrocompatibilidade.
9. **Component API Design** — Alan B Smith (Workday) — https://alanbsmith.medium.com/component-api-design-3ff378458511 — padronizar nomes de props; tipos enumerados; prop table diz *quando usar*, não só sintaxe.
10. **Behind the scenes of designing a design system component** — Rama Krushna Behera (Razorpay Design) — https://medium.com/razorpay-design/behind-the-scenes-of-designing-a-design-system-component-7969636fabf4 — documentar intro/variantes/usage/a11y/motion; "what you see in design is what you get in code".
11. **Design systems: simplifying documentation writing** — Dean Harrison (UX Collective) — https://uxdesign.cc/design-systems-simplifying-documentation-writing-5ec240c484fe — template repetível; priorizar por fricção/uso; publicar cedo (funcional > perfeito).
12. **Design system best practices: Components and documentation** — Maksym Cherkashyn (Design Systems Collective) — https://www.designsystemscollective.com/design-system-best-practices-components-and-documentation-bdb020e02172 — Figma e dev espelham a mesma anatomia; naming consistente; DS é vivo.

Triangulação (não-Medium, mesmos pontos): zeroheight blog, UXPin, StackBlitz.

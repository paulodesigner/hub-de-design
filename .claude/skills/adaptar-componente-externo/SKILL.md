---
name: adaptar-componente-externo
description: "Recria nativamente, com as cores/tokens/tipografia do projeto, um componente de referência que 'não é nosso' — vindo de outra biblioteca, remota ou local com paleta genérica (SDS, UI kit da comunidade, protótipo copiado). Preserva a estrutura de variantes/propriedades da referência e completa estados ou variantes básicas que estejam faltando (Hover, Disabled, tamanhos, etc.). Use quando o usuário disser 'recria esse componente com nossas cores', 'esse não é nativo, adapta pro nosso design system', 'copia esse componente e usa nossos tokens', ou apontar um link do Figma dizendo que 'já tem as propriedades que eu quero, só precisa ser nosso'."
---

# Adaptar Componente Externo pro Design System

> Processo pra pegar um componente de referência (remoto, ou local mas com cores/fontes genéricas de outra origem) e recriá-lo **nativo** do projeto — mesma estrutura de propriedades/variantes, cores/tipografia/radius/spacing vindos dos tokens reais do projeto. Quando a referência estiver incompleta (faltando um estado óbvio, um tamanho, um ícone de status), **complete** — não replique a lacuna.

Validada em produção: um `Button` de 156 variantes (13 Types) trimado com o usuário pra 72 (6 Types) + spinner de loading real; e um `Input` de 6 estados que ganhou Hover, Sizes (L/M/S) e ícone de status automático em Negative/Positive.

## Quando usar
- "recria esse componente com as nossas cores", "esse botão não é nativo, é instância de outro", "adapta esse componente do link pro nosso DS".
- O usuário aponta um node do Figma (link com `node-id=`) e diz que ele "já tem as propriedades que eu quero" — sinal de que quer a MESMA estrutura, só recolorida/retipografada.
- Ao notar, durante outra tarefa, que um componente em uso usa cores hex soltas ou de uma paleta que não é a do projeto (ex.: azul `#3355FF` genérico de UI kit, ou remanescentes de um plugin como "Simple Design System").

## Não é isso
- Não é sobre **layout/organização de página** (isso é `organizacao-pagina-componentes`) — aplique esta skill primeiro pra construir o componente, depois aquela pra arrumar a casa onde ele mora.
- Não é sobre **desenhar algo novo do zero sem referência** (isso é `estudio-de-design` ou `figma-generate-library`).
- Não é sobre **mapear o reuso do DS existente** (isso é `mapa-do-design-system`).

## Croqui antes de mudar (regra do Hub)
Se a referência tiver muitas variantes (>~30) ou ambiguidade real de escopo (tipos redundantes, tamanhos não pedidos), **pare e pergunte** antes de construir tudo — ver Passo 2. Não é regra follow-with-caution por excesso de zelo: construir 156 variantes erradas custa muito mais que uma pergunta.

## Passo 0 — Redescubra os tokens atuais, não confie na memória
**Antes de mapear qualquer cor**, relist a coleção de variáveis semânticas do projeto por nome e valor, mesmo que você (ou outra sessão) já tenha trabalhado nela antes:

```js
const collections = await figma.variables.getLocalVariableCollectionsAsync();
// ache a coleção de cor semântica pelo padrão de nome do projeto, não por ID guardado de memória
const colorCollection = collections.find(c => /sem[aâ]ntic|cor/i.test(c.name));
const vars = await Promise.all(colorCollection.variableIds.map(id => figma.variables.getVariableByIdAsync(id)));
return vars.map(v => ({ name: v.name, value: v.valuesByMode[colorCollection.modes[0].modeId] }));
```

**Por quê:** neste projeto, uma coleção que uma sessão criou como `Color/Text/OnPrimary` foi renomeada por outra sessão/pelo usuário, direto no Figma, pra `Content/OnFill` — mesmo ID, nome diferente. Um lookup por nome antigo falha silenciosamente (`setBoundVariableForPaint` com variável `undefined` não lança erro — só não vincula nada, e a cor fica hardcoded/errada). Isso pode ter acontecido em paralelo à sua sessão atual; sempre relistar é mais barato que depurar um binding fantasma depois.

## Passo 1 — Inspecione a referência por completo
Pra cada estado/variante relevante da referência, extraia (não adivinhe):
- **Propriedades do component set**: `componentPropertyDefinitions` (TEXT, BOOLEAN, INSTANCE_SWAP, VARIANT + `variantOptions`).
- **Se é remoto ou local**: `mainComponent.remote` — mas não pare aí; um componente **local** pode ainda usar cores genéricas de outra origem (cópia de UI kit, sobra de plugin). O sinal real é "as cores batem com os tokens do projeto?", não "é remoto?".
- **Estrutura de árvore de UM variant representativo** por estado (nome, tipo, fill, stroke, cornerRadius, padding, texto/fontSize/cor) — é isso que vira o mapa de cor.
- **Geometria por tamanho**, se houver dimensão de Size — altura, padding, radius, fontSize de cada tamanho da referência, pra preservar a proporção mesmo trocando a cor.

```js
const owner = main.parent?.type === 'COMPONENT_SET' ? main.parent : main;
const defs = owner.componentPropertyDefinitions;
const variantNames = owner.children.map(c => c.name);
// depois, describe() recursivo num variant por estado pra pegar fill/stroke/texto — ver exemplos em variable-patterns.md
```

## Passo 2 — Alinhe o escopo com o usuário (pergunte se for grande)
Antes de construir, se a referência tiver muitas variantes ortogonais (ex.: 13 "Types" × 3 "Sizes" × 4 "States" = 156), **pergunte**:
1. Replicar TUDO fielmente, ou só o subconjunto que faz sentido pro produto? (dê exemplos concretos do que cortaria)
2. Existem variantes que ficam **redundantes** no sistema de cor do projeto (ex.: variantes "Mono"/grayscale-only quando o projeto já é majoritariamente monocromático)? Pergunte explicitamente qual manter.

Não pule esta etapa achando que "fiel = sempre melhor" — 156 variantes com metade redundante é retrabalho que o usuário não pediu.

## Passo 3 — Análise de lacunas: o que falta e devia existir
O pedido de "complete o que faltar" é uma licença pra aplicar conhecimento de padrões de UI, não carta branca pra inventar. Verifique contra a lista de estados/variantes **esperados pra aquele tipo de componente** e proponha preencher as lacunas reais:

| Componente | Estados/variantes comumente esperados | Lacuna comum na referência |
|---|---|---|
| Botão | Default, Hover, Pressed/Active, Disabled, Loading | Loading sem spinner real (só texto/opacidade) |
| Input/Select | Default, Hover, Focus, Filled, Error, Success, Disabled | Hover ausente; Error/Success só mudam borda (sem ícone — falha WCAG 1.4.1, "não usar só cor") |
| Checkbox/Radio | Unchecked, Checked, Indeterminate, Disabled (×Hover/Focus) | Indeterminate ausente |
| Badge/Tag | Neutral, Info, Success, Warning, Danger | Paleta de status incompleta (só 1–2 cores) |
| Qualquer interativo | Focus visible (teclado) | Anel de foco ausente ou só de cor, sem espessura própria |

Ao preencher uma lacuna:
- **Justifique com um princípio real** do projeto (ex.: "DESIGN_SYSTEM.md já cita WCAG 1.4.1 — cor não pode ser o único indicador", ou "o Button já usa a régua L/M/S, então o Input ganha a mesma régua pra consistência").
- **Não invente sozinho um ícone de status novo** — reuse o que já existe na biblioteca de ícones do projeto (ex.: `circle-check`/`circle-alert` já componentizados) em vez de desenhar um novo.
- Se a lacuna for de conteúdo/copy (texto de erro, texto de ajuda), escreva algo genérico e plausível ("This field is required"), não específico de regra de negócio que você não confirmou.

## Passo 4 — Mapeie cor/tipografia/radius/spacing
Construa uma tabela explícita **Tipo/Estado → variável do projeto** antes de escrever qualquer `use_figma`. Padrão de papéis que costuma existir num sistema de cor maduro (adapte aos nomes reais encontrados no Passo 0):

- Ação primária/marca → `Background/Brand` (+ Hover/Pressed do mesmo papel)
- Ação neutra/secundária → `Background/Selected` → `Background/Track` (hover/pressed em degradê de cinza)
- Contorno/outline → `Background/Surface` + `Border/Default`
- Texto/ícone sobre fundo preenchido escuro → `Content/OnFill`
- Texto/ícone sobre fundo claro → `Content/Primary` (principal) / `Content/Secondary` (placeholder, apoio)
- Erro → `Background/Danger` / `Border/Danger` / `Content/Danger` (+ ícone de alerta)
- Sucesso → `Background/Success` / `Border/Success` / `Content/Success` (+ ícone de check)
- Foco (teclado) → `Border/Focus`, sempre com espessura maior (2px) que o estado default (1px)
- Desabilitado → `Background/Selected` (ou equivalente neutro), `Border/Disabled`, `Content/Disabled`

Tamanho/geometria: se o projeto já tem uma régua estabelecida pra outro componente (ex.: Button L/M/S = 48/40/32px de altura, radius 12/8/8), **reuse a mesma régua** em vez de inventar uma nova — é o que faz o sistema parecer um sistema.

## Passo 5 — Construa via gerador, em lotes pequenos
Escreva uma função `createVariant(tipo, tamanho, estado)` que:
1. Cria o `ComponentNode` com auto-layout, padding/radius **vinculados a variável** (nunca número solto).
2. Cria os filhos (texto, ícones-slot ocultos por padrão, ícone de status fixo quando aplicável).
3. Adiciona as **Component Properties**.
4. Vincula `componentPropertyReferences` nos filhos.
5. Retorna o componente pra ser posicionado e, no fim, combinado.

Rode em lotes (ex.: por Tipo, ou por grupo de 8–12 variantes) — cada `use_figma` é atômico; um erro no meio de 72 criações de uma vez perde tudo. Valide com `get_screenshot` a cada lote antes de seguir pro próximo.

Ao final, uma chamada separada de `combineAsVariants` + reposicionamento em grid (linha = eixo mais importante, coluna = o outro) + `set.name`/`set.description`.

## Passo 6 — Troque as instâncias reais existentes
Busque instâncias do component set ANTIGO em uso real no arquivo:

```js
const allInstances = page.findAllWithCriteria({ types: ['INSTANCE'] });
const targets = [];
for (const inst of allInstances) {
  const main = await inst.getMainComponentAsync();
  const owner = main?.parent?.type === 'COMPONENT_SET' ? main.parent : main;
  if (owner?.id === OLD_COMPONENT_SET_ID) targets.push({ id: inst.id, props: inst.componentProperties });
}
```

Pra cada instância: capture os valores atuais das properties relevantes (texto, booleans de show/hide), decida a variante nativa correspondente (mapeando tipo/estado antigo pro novo, com fallback pro mais próximo se algo foi cortado no Passo 2), então:

```js
inst.swapComponent(novoVariant);
inst.setProperties({ [novaLabelKey]: valorAntigo, ... }); // reaplica — o swap NÃO garante que overrides sobrevivam entre component sets diferentes
```

Se não houver nenhuma instância real em uso (componente novo, ainda não aplicado em telas), não é erro — apenas registre que ele está disponível na biblioteca pra uso futuro.

## Passo 7 — Valide visualmente
`get_screenshot` do component set inteiro (grid) e de pelo menos uma instância real trocada, antes de reportar concluído. Preste atenção especial a: contraste em fundo escuro (ver Lição 2 abaixo) e ícones em fundos com a mesma cor do ícone (invisibilidade silenciosa).

## Checklist final
- [ ] Nomes de variável relistados do zero (não reaproveitados de memória de outra sessão)
- [ ] Estrutura de propriedades da referência preservada (mesmos nomes de property que o usuário pediu)
- [ ] Escopo de variantes confirmado com o usuário se a referência era grande/ambígua
- [ ] Lacunas de estado/variante identificadas e preenchidas com justificativa (não só copiadas da referência)
- [ ] Toda cor/radius/spacing vinculada a variável do projeto — nenhum hex solto
- [ ] Tamanhos reaproveitam a régua já estabelecida em outro componente do mesmo projeto, se existir
- [ ] Cada variante tem suas próprias Component Properties (não reaproveita key de outra variante — ver Lição 1)
- [ ] `combineAsVariants` + grid organizado (linha/coluna = eixos reais) + nome/descrição do set
- [ ] Instâncias reais existentes (se houver) trocadas pro nativo, com label/overrides reaplicados
- [ ] Validado com screenshot — geral e ao menos uma instância real
- [ ] Reportado ao usuário: o que foi replicado fielmente, o que foi cortado (e por quê), o que foi criado além da referência (e por quê)

## Lições (retroalimentadas pelo uso real)

1. **`addComponentProperty` gera uma key LOCAL por componente — não é compartilhável entre variantes antes do `combineAsVariants`.** Se você criar as properties só na primeira variante e reusar a mesma key nas outras 71, a partir da SEGUNDA variante o assignment de `componentPropertyReferences` falha com `Could not find a component property with name: 'Label#<id>'` — porque aquela key pertence ao componente #1, não ao #2. **Correção:** chame `addComponentProperty` em CADA variante individualmente (cada uma tem sua própria key), e vincule `componentPropertyReferences` só com a key que ACABOU de ser gerada naquele mesmo componente. O `combineAsVariants` final é quem unifica propriedades de mesmo NOME entre as variantes — a unificação é por nome, não por key compartilhada de antemão.
2. **Ícone/texto herda a cor "padrão" do componente novo — não a cor certa pro fundo onde ele efetivamente vive.** Ao trocar um ícone dentro de um botão/campo de fundo escuro (preto, marca) pelo componente nativo (que por padrão usa a cor de texto escura, pensada pra fundo claro), o resultado é invisível (preto sobre preto) até você aplicar um override local de cor (`Content/OnFill` ou equivalente claro) SÓ nessa instância específica — sem alterar o master. Sempre cheque visualmente qualquer ícone/texto que vá morar sobre um fundo preenchido/escuro antes de reportar concluído.
3. **`node.layoutSizingHorizontal = 'FILL'` só funciona DEPOIS do `appendChild` no pai com auto-layout.** Setar antes (mesmo que o pai já exista, só ainda não tenha recebido esse filho) lança `FILL can only be set on children of auto-layout frames`. Regra prática: crie o filho → `parent.appendChild(filho)` → só então ajuste `layoutSizingHorizontal/Vertical`.
4. **Zero instâncias reais de um componente novo não é falha — é esperado quando a referência é uma proposta ainda não aplicada.** Busque antes de assumir; relate honestamente "disponível na biblioteca, sem uso ainda" em vez de forçar uma substituição que não existe.
5. **Uma TEXT property com "Nome"/nome-genérico que deveria ter valor DIFERENTE por variante (ex.: "Continue with Google" vs. "Continue with Facebook" num componente `Provider`) não deve ser exposta como Component Property compartilhada.** Ao dar o mesmo nome de property (`Label`) em variantes com defaults diferentes, o `combineAsVariants` unifica por nome e o texto renderizado de TODAS as variantes passa a seguir o valor de uma property única (na prática, o texto do primeiro variant processado "vaza" pros outros — ex.: todo provider mostrando "Continue with Google"). **Correção:** se o conteúdo textual é intrinsecamente amarrado à variante (não é um campo livre que o usuário deveria poder editar igual em qualquer variante), NÃO chame `addComponentProperty('TEXT', ...)` nele — deixe `characters` literal, sem `componentPropertyReferences`. Texto sem property ainda é editável na instância (duplo-clique), só não aparece como campo no painel de properties. Property TEXT compartilhada só faz sentido quando o valor-padrão é o MESMO em todas as variantes (ex.: label "Button" igual em todo Type/Size de um botão).
6. **`addComponentProperty` só funciona em componentes AINDA NÃO combinados.** Chamar em uma variante que já faz parte de um `COMPONENT_SET` existente (mesmo que você não tenha sido quem o combinou) lança `Can only set component property definitions on a product component`. Se precisa adicionar uma property nova (ex.: tornar um ícone hardcoded em INSTANCE_SWAP) a um Component Set que já existe, não tem atalho: monte a property nos componentes ANTES de combinar, ou aceite a limitação e documente. Isso não afeta adicionar uma variante NOVA (clonar + `set.appendChild(clone)` funciona liso, sem essa restrição — só a criação de property é bloqueada).
7. **`deleteComponentProperty` lança erro se a property já não existir mais** (ex.: depois de limpar todas as `componentPropertyReferences` que apontavam pra ela — Figma pode remover a definição órfã automaticamente). Sempre envolva a chamada em `try/catch`, ou confira `Object.keys(node.componentPropertyDefinitions)` antes de tentar apagar por nome.
8. **Não é possível `.remove()` um node remoto** (mesma restrição de não poder editar fill/stroke — "Removing this node is not allowed"). Depois de migrar todas as instâncias reais pro componente nativo, o componente remoto antigo simplesmente fica sem uso — não tem como limpá-lo do arquivo; isso é esperado, não é um passo pendente.
9. **Ao clonar uma variante existente pra criar um novo estado (ex.: Default → Disabled), sempre reposicione TODAS as variantes do set explicitamente no final** (`children.forEach` com grid de x/y por nome), mesmo as que você não tocou. Um clone entra em `(0,0)` relativo ou herda a posição do original, sobrepondo variantes vizinhas — o Component Set continua funcionando (as properties resolvem certo), mas o preview visual do set fica ilegível até reordenar.

## Referências
- [component-patterns.md](../figma-use/references/component-patterns.md) — API de `addComponentProperty`, `combineAsVariants`, `componentPropertyReferences`, INSTANCE_SWAP.
- [variable-patterns.md](../figma-use/references/variable-patterns.md) — binding de variável a paint/radius/padding, descoberta de variáveis existentes no arquivo.
- [organizacao-pagina-componentes](../organizacao-pagina-componentes/SKILL.md) — o que fazer DEPOIS de construir o componente (onde ele mora, como é documentado).

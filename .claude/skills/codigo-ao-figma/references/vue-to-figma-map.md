# Mapa de leitura: construtos Vue (SFC) → construtos Figma

Use na **Spec profunda (passo 3)** para traduzir o que o `.vue` faz em decisões de modelagem no Figma,
sem adivinhar. Código é a fonte da verdade; aqui está como **interpretá-lo** com fidelidade.

## Renderização condicional → presença / variante / visibilidade
| No código | Significado | No Figma |
|---|---|---|
| `v-if` / `v-else-if` / `v-else` | o nó é **adicionado/removido** do DOM conforme a condição | estados que **diferem na estrutura** → **variantes distintas** (não só mudar cor). Ex.: submenu aberto vs fechado = 2 variantes. |
| `v-show` | o nó **sempre existe**, só alterna `display` | **mantenha o nó** na variante e use `visible=false` (NÃO apague). Sinaliza que o elemento "existe sempre". |
| condição que troca **classe/estilo** (`:class`, `:style` + `computed`) | mesmo nó, **aparência** muda por estado | **eixo de variante** (`State=...`); pinte sub-elemento a sub-elemento (ver Lição 1). |
| `v-if="hasSubMenu"` em ícone indicador (caret) | indicador só aparece quando há submenu | **propriedade booleana** ligada a `visible` (ex.: `Tem submenu`). |

## Listas e composição → instâncias
| No código | Significado | No Figma |
|---|---|---|
| `v-for="x in items"` | N repetições do mesmo sub-componente | **instâncias** do sub-componente no container (nunca filhos achatados — Lição 6). |
| componente que renderiza **a si mesmo** (`<menu-item v-for="s in subMenus">`) | recursão / árvore | **instâncias aninhadas**; modele o ramo inteiro (caret + container + sub-item) — Lição 8. |
| `<slot>` / `<slot name="x">` | conteúdo injetado pelo pai | **INSTANCE_SWAP** ou children expostos; elementos opcionais via `visible`. |

## Contrato do componente → propriedades
| No código | Significado | No Figma |
|---|---|---|
| `defineProps` boolean (ex.: `isSubMenu`, `disabled`) | liga/desliga aparência ou ramo | **boolean property** (visibilidade) **ou** eixo de variante, conforme muda estrutura. |
| `defineProps` enum/string de variante | conjunto finito de aparências | **eixo de variante** com os mesmos valores/nomes (Linguagem Ubíqua). |
| prop de ícone (`icon: string`) | ícone trocável | **INSTANCE_SWAP** (`Ícone`); recolora **depois** do swap (Lição 5). |
| `v-model` | contrato bidirecional (estado controlado) | normalmente um **estado/variante** (ex.: checked/unchecked). |
| `props` com texto/label (`t(label)`) | conteúdo textual | **text property** / override de characters. |

## Estados visuais → eixos de variante (SÓ os que o CSS tem)
| No código (SCSS) | No Figma |
|---|---|
| `:hover` | variante `Hover` (replicar exatamente: ex. `opacity: var(--ath-opacity)` = 0.6). |
| `:focus-visible` | variante de foco **só se existir** no CSS (anel/outline). Não inventar. |
| `:active` (pressed) | variante `Active/Pressed` **se existir**. |
| `:disabled` / `[disabled]` | variante `Disabled` **se existir** (isenta de contraste — WCAG 1.4.3). |
| `.active`/`.selected` (classe de rota/seleção) | variante de seleção; mapear **sub-elemento a sub-elemento** (label ≠ ícone ≠ fundo). |
| **ausência** de um seletor | o estado **não existe** → NÃO criar (regra as-is). |

## Comportamento / interação → componente interativo
| No código | Significado | No Figma |
|---|---|---|
| `@click` + `ref` toggle (ex.: `subMenuOpened.value = !...`) | alterna estado **na própria instância** | **componente interativo**: variante por estado + reação `ON_CLICK → CHANGE_TO` (smart-animate). Lição 9. |
| `@click` navega/emite (`emit`, `router-link :to`) | ação de saída | normalmente **não** vira estado; é navegação. Modele o destino só se pedido. |
| transições (`transition`, `@keyframes`, `transition:`) | animação entre estados | `transition` da reação (smart-animate) reproduz a ideia; replique duração/easing se relevante. |

## Tokens / estilo → variáveis vinculadas (Value Object)
| No código | No Figma |
|---|---|
| `var(--ath-...)` / `$scss-var` | resolva → **variável semântica do Figma** e **vincule** (`setBoundVariableForPaint`). Nunca carimbe o hex (token = valor imutável, referenciado — não copiado). |
| `rem` (base do projeto = **10px**, 62.5%) | `1rem = 10px` → `2.4rem=24`, `1.5rem=15`, `0.4rem=4`. Confirme a base pelo CSS antes de converter. |
| `box-shadow` | `DROP_SHADOW` (offset/blur/spread/cor+alpha). |
| `border` inset vs `outline` | `stroke-align` INSIDE vs OUTSIDE. |

## Armadilhas de leitura (o que NÃO confundir)
- **`v-show` ≠ `v-if`**: o primeiro mantém o nó (oculto), o segundo remove. Erra a decisão "apagar vs `visible=false`".
- **`computed` esconde lógica de estado**: um `:class="{ active: isActive }"` pode depender de rota/prop — rastreie a origem para nomear a variante certa.
- **Herança/override de CSS**: um seletor composto (`.active > a`, `.active span template`) colore **partes diferentes** com vars diferentes — monte a tabela `{sub-elemento → propriedade → var}` (Lição 1).
- **Estilo de ícone**: classe Phosphor `ph-<nome>` = peso **regular**; a cor vem de `color`/currentColor do seletor — confira qual seletor aplica no contexto (ex.: sub-item herda `.icon-submenu`).

> Origem: destilado de conhecimento geral de Vue 3 (não de dependência externa). O repo `vuejs-ai/skills`
> foi avaliado e **não adotado** — é focado em *escrever* Vue, enquanto aqui o objetivo é *ler* e replicar.

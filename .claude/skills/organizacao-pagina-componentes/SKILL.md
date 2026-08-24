---
name: organizacao-pagina-componentes
description: "Organiza (ou reorganiza) a página de componentes de um Design System no Figma para handoff — estrutura de páginas/seções, nomenclatura (slash + propriedades nomeadas), layout do component set (grid de variantes), anotações, status/Ready for dev e cover por componente. Use quando o usuário pedir para 'arrumar/organizar a página de componentes', 'deixar o arquivo pronto pra handoff/dev', 'estruturar o DS no Figma', ou quando notar um component set bagunçado (variantes soltas, sem nome, sem doc) durante outra tarefa."
---

# Organização da Página de Componentes (Figma → handoff)

> Esta skill é sobre **arquitetura de arquivo/página**: como os componentes ficam dispostos, nomeados e documentados no Figma para o handoff ser rápido e sem ida-e-volta. Ela **não** decide o visual do componente (isso é `codigo-ao-figma` réplica fiel, ou `estudio-de-design` proposta nova), **não** mantém o mapa de reuso global do DS (isso é o agente `mapa-do-design-system`, A4) e **não** constrói o Storybook de código (isso é `construtor-do-storybook`, A9). Ela organiza **a casa onde os componentes moram** dentro do Figma.

## Quando usar
- "organiza a página de componentes", "deixa esse arquivo pronto pra handoff", "arruma esse component set", "como estruturar o DS no Figma".
- Ao notar, durante outra tarefa (ex.: `codigo-ao-figma`), que a página de destino está bagunçada — variantes soltas sem grid, sem nome de propriedade, sem status — **sinalize e ofereça** rodar esta skill antes de inserir mais um componente ali.

## Croqui antes de mudar (regra 8 do Hub)
Se a reorganização for estrutural (mover página inteira, recriar sections, renomear em massa), **mostre primeiro um rascunho ASCII** da estrutura proposta (árvore de páginas/sections) no chat e só execute depois de aprovado. Ajuste simples e local (nomear uma propriedade, adicionar uma cover) pode ir direto.

## 1. Estrutura de páginas do arquivo (nível arquivo do Figma)
Um arquivo de DS não deve misturar biblioteca com produto — arquivo separado do design de produto (regra recorrente em todas as fontes). Dentro do arquivo do DS, use **páginas por categoria**, com prefixo numérico (o Figma ordena páginas por ordem de lista manual, mas prefixar ajuda times a não reordenar à toa e comunica hierarquia de leitura):

```
00  Cover / Como usar este arquivo
01  Foundations (tokens: cor, tipografia, spacing, radius, elevação, ícones)
10  Components — Atoms (botão, input, checkbox, badge, tag, avatar…)
20  Components — Molecules/Organisms (form, card, nav, tabela…)
30  Patterns / Templates (páginas inteiras, ex.: Desktop_layout)
90  Playground / Sandbox (rascunho, WIP — nunca linkado por instância)
99  Docs / Changelog
```
Adapte a granularidade ao tamanho real do DS do projeto (não crie 7 páginas para um DS de 15 componentes) — o princípio é **ordem de dependência de leitura**: fundamentos → átomos → composições → padrões → docs.

## 2. Dentro da página de componentes: Sections, não só frames soltos
Use **Sections** do Figma (não frames genéricos) para agrupar por família (`Buttons`, `Inputs`, `Feedback`, `Navigation`…) — sections dão estrutura ao canvas sem quebrar frames em arquivos separados, e aparecem como grupo navegável na barra lateral.
- **Cor da section = status**, aplicada com moderação: verde = aprovado/estável, amarelo = em revisão, vermelho = deprecated/não usar. Documente essa legenda uma vez na página `00 Cover`.
- Prefixe/oculte o que não deve aparecer no picker de componentes com `.` ou `_` no nome (ex.: `.master-base-button`) — mantém a árvore limpa sem apagar a peça-mãe.

## 3. Cover / thumbnail por componente
Cada componente (ou component set) ganha um **frame de capa pequeno** acima do set, com: nome do componente, ícone/thumbnail, e o **status do ciclo de vida** (`Em design` / `Em desenvolvimento` / `Lançado` / `Deprecated`) — atualizável conforme o componente evolui. Isso dá capacidade de "browsing" rápido (grid de covers = catálogo visual) sem abrir cada component set.

## 4. Layout do component set (a grid de variantes)
- **Organize variantes antes de combinar** (`combineAsVariants`) em **linhas e colunas** que comuniquem a natureza multidimensional: um eixo por linha, outro por coluna (ex.: linhas = `Size` [Small/Medium/Large], colunas = `State` [Default/Hover/Active/Disabled]). Reorganizar depois de combinado é retrabalho — planeje a grid primeiro.
- **Nomeie eixos e valores como o código, não como "Variant 4".** Propriedade = nome real da prop/estado (`State`, `Size`, `Emphasis`), valor = nome real (`state=pressed`, não `Variant 4`). Isso é o que aparece no painel de propriedades pro dev — nome genérico = pergunta no handoff.
- **Reduza a explosão de variantes com Component Properties** (boolean, instance-swap, text) para eixos ortogonais que não precisam virar linha/coluna própria (ex.: `hasIcon` como boolean, `icon` como instance-swap) em vez de multiplicar `Size × State × ComIcone × SemIcone` em variantes completas.
- **Sub-componentes reusáveis** (badge, ícone, spinner) entram como **instância**, não redesenhados dentro de cada variante — mudança no sub-componente propaga.

## 5. Anotação e documentação lado a lado
- **Texto de anotação ao lado do component set** (não só na descrição): specs de espaçamento (anatomia com medidas), do's & don'ts (exemplo certo vs. errado lado a lado), notas de comportamento para estados complexos (o que dispara a transição).
- **Descrição do componente/estilo** (painel do Figma, aparece no Inspect/Dev Mode): 1 frase de propósito + 1 frase de quando **não** usar + link para a implementação real (rota do código ou story do Storybook). Documentação **co-localizada** (dentro do próprio arquivo) é lida; documentação numa wiki separada, na prática, não é.
- **Nomeie estilos/variáveis com o nome do token/variável do código** (ex.: `content-brand`, `spacing/16`), nunca um nome só-visual (`Roxo escuro 2`) — é o que permite ao dev bater o nome do Figma com o nome no CSS/código.

## 6. Marcação de pronto para dev (Ready for development)
- Marque frames/components prontos com o status "Ready for development" do Figma (ou, na ausência do recurso, com a cor de section verde + tag no nome) — sinaliza ao dev o que já pode implementar sem esperar mais revisão de design.
- Quando o projeto tiver Storybook vivo (ver memória `live-storybook` / agente `construtor-do-storybook`), **linke o componente do Figma à story correspondente** (Dev Mode → link de recurso) — dev clica no componente e cai na implementação viva, reduzindo perguntas sobre estados interativos.
- Página dedicada de **"instâncias limpas para handoff"**: uma página só com instâncias dos componentes-mestre organizadas para visualização (não edição) — muda no mestre, atualiza aqui automaticamente; dev/PM navegam sem risco de mexer na fonte.

## 7. Tokens sempre vinculados, nunca hex solto
Toda cor/espaçamento/tipografia usada nos componentes desta página deve vir de **variável ou estilo vinculado**, não hex/px hardcoded — reforça a regra-chave 4 do Hub e é o que faz a página funcionar como fonte de verdade em vez de "desenho parecido". Se o <PRODUTO> tiver os dois sistemas de token coexistindo (novo `--content-*/--eds-*` vs. antigo `--ath-color-*`), respeite a classificação por componente (ver `figma-ds-reuse-map.md` → "DECISÃO CRÍTICA") — não misture na hora de organizar.

## 8. Workflow para aplicar esta skill
1. **Audite antes de mexer**: liste os componentes existentes na página (nome, se têm variantes combinadas, se têm descrição, se usam token vinculado, se há cover). Se o Figma MCP oficial estiver conectado (ver `codigo-ao-figma` → passo 0, `whoami`), use `get_metadata`/`search_design_system` para levantar o estado real em vez de supor.
2. **Rascunhe a estrutura proposta** (páginas/sections/grid de variantes) em ASCII no chat — regra 8 do Hub — especialmente se for reorganização estrutural.
3. **Aplique em passos pequenos e validáveis**: crie/renomeie sections → reordene variantes em grid → nomeie propriedades/valores → adicione descrições/links de código → adicione cover + status. Valide com `get_screenshot` a cada etapa.
4. **Não invente conteúdo**: nome de propriedade, token e link de código vêm do código real do projeto (fonte da verdade) ou do que já existe no Figma — se faltar, pergunte ou registre em `melhorias.md`, não adivinhe.
5. **Feche com checklist** (abaixo) e reporte o que mudou + o que ficou pendente (ex.: componente sem token vinculado que precisa de decisão do time).

## Checklist final
- [ ] Arquivo do DS separado de arquivo de produto (ou, se o mesmo arquivo, página claramente isolada)
- [ ] Páginas ordenadas por dependência de leitura (Foundations → Components → Patterns → Docs)
- [ ] Sections por família de componente, cor = status (legenda documentada na Cover)
- [ ] Cada componente/component set tem cover com nome + status do ciclo de vida
- [ ] Variantes organizadas em grid (linha/coluna = eixo), não soltas
- [ ] Propriedades e valores nomeados como o código (`state=pressed`, não `Variant 4`)
- [ ] Component Properties usadas para eixos ortogonais (evitar explosão de variantes)
- [ ] Anotação lateral (anatomia/spacing/do's & don'ts) nos sets complexos
- [ ] Descrição com propósito + quando não usar + link pro código/Storybook
- [ ] Estilos/variáveis nomeados como o token do código, sempre vinculados (nunca hex solto)
- [ ] Status "Ready for development" marcado onde já pode ser implementado
- [ ] Página de instâncias limpas para handoff (se o time de dev não tiver acesso de edição)

## Lições (retroalimentadas pelo uso real)

1. **`figma.createSection()` + `figma.currentPage.appendChild(section)` no `use_figma` pode gravar na página ERRADA.** `figma.currentPage` volta pra PRIMEIRA página do arquivo no início de toda chamada `use_figma` — mesmo que a única coisa que o script fez antes tenha sido `getNodeByIdAsync` (que NÃO troca a página atual, só busca o nó). Se a página que você quer organizar não é a primeira do arquivo, criar uma Section nova e apendá-la em `figma.currentPage` sem antes chamar `await figma.setCurrentPageAsync(paginaAlvo)` faz a section nascer na página errada (silenciosamente — não dá erro, só fica no lugar errado). **Regra:** sempre que for criar um node de topo novo (Section, Page-level Frame), chame `setCurrentPageAsync` explicitamente na MESMA chamada antes do `createSection()`/`appendChild`, ou aponte o `appendChild` direto pro node de página já obtido via `getNodeByIdAsync(pageId)` em vez de `figma.currentPage`. Valide sempre com `node.parent.name` no retorno do script.
2. **A metadata XML (`get_metadata`) usa `<frame>`/`<symbol>` como abstração — não é o tipo real do node.** Um `<frame>` na árvore pode ser, na verdade, um `COMPONENT_SET` de verdade (variantes já combinadas), e um `<symbol>` filho pode ser um `COMPONENT`. Antes de decidir se "falta combinar variantes", confirme o `.type` real via `use_figma` (`getNodeByIdAsync` + `.type`) — evita propor um `combineAsVariants` desnecessário num set que já existe, quando o problema real é só layout (variantes sobrepostas em `x=0,y=0` por nunca terem sido reposicionadas após o combine).

## Referências (pesquisa que fundamentou esta skill)
- [Guide to developer handoff in Figma](https://www.figma.com/best-practices/guide-to-developer-handoff/) e [Using components](https://www.figma.com/best-practices/guide-to-developer-handoff/using-components/) — Figma
- [Optimize design files for developer handoff](https://help.figma.com/hc/en-us/articles/360040521453-Optimize-design-files-for-developer-handoff) — Figma Help Center
- [Team, project, and file organization](https://www.figma.com/best-practices/team-file-organization/) e [Creating and organizing Variants](https://www.figma.com/best-practices/creating-and-organizing-variants/) — Figma
- [Name and organize components](https://help.figma.com/hc/en-us/articles/360038663994-Name-and-organize-components) — Figma Help Center
- [How to organize your Figma files for your design system](https://help.zeroheight.com/hc/en-us/articles/36473914948379-How-to-organize-your-Figma-files-for-your-design-system) — zeroheight
- [Structuring and Splitting Large-Scale Figma Design Systems](https://medium.com/@claus.nisslmueller/structuring-and-splitting-large-scale-figma-design-systems-a-2025-master-guide-for-scalable-c1c3a7dabb0e) — Medium
- [7 Figma Design System Best Practices for 2026](https://atomize.tools/blog/figma-design-system-best-practices/) — Atomize
- [Atomic Design in Practice: How to Structure Your Figma Files](https://medium.com/@atnoforuiuxdesigning/atomic-design-in-practice-how-to-structure-your-figma-files-like-a-design-system-engineer-8682bcb14271) — Medium

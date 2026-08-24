# Regras inegociáveis

> **Estrutura em 3 agentes** — ver [`agentes.md`](agentes.md). Regras 1, 2, 4, 5, 6 e 7 são **compartilhadas** pelos agentes; a regra 3 ("sempre as-is") é **só do Agente 1** (réplica fiel).

## 1. Repo `<PRODUTO>/` é READ-ONLY
**Nunca** editar, commitar ou criar arquivos dentro de `<PRODUTO>/`. É repo compartilhado da
empresa; o clone local é só um espelho de leitura, sempre sincronizado com o git.
- Só comandos read-only (ler tokens/componentes, `git fetch/pull`, `storysync tokens/map/list/diff`).
- Nada de `storysync init/setup` nem `@storybook/addon-mcp` (escrevem no repo).
- Artefatos gerados vão **fora** do repo (scratchpad, `~/tools`, Figma).
- Mantenha atual com `~/bin/<produto>-sync` (branch `develop`). Rode antes de tarefa que depende do repo.

## 2. Código é a fonte da verdade
Ao construir um componente no Figma, **replique EXATAMENTE o que o código do <PRODUTO> faz**.
- **Não** desenhe a partir de screenshot sozinho.
- **Não** importe o modelo de outro componente do DS (ex.: o Figma `Card - Button`) quando ele
  divergir do componente real do código. (Foi o que gerou falha de contraste WCAG no card
  "Ver meu repasse"; a correção foi voltar ao que `HomeCardNavigator.vue` renderiza.)

## 3. "Sempre as-is" — SÓ Agente 1 (réplica fiel)
Na **réplica fiel** (Agente 1 `codigo-ao-figma`), o Figma é uma auditoria do componente **como ele é**. (O Agente 2 `estudio-de-design` PODE divergir de propósito — sempre marcando como **proposta** e separando do as-is.)
- **Não invente** estados/variantes ausentes (focus/pressed/disabled/loading) se o CSS não os tem.
- **Não "melhore"** falhas (ex.: contraste do ícone ativo) — **replique inclusive as falhas e só
  reporte-as**.
- Só criar algo fora-do-código se o usuário **insistir explicitamente**, marcando como deliberado.

## 4. Tokens vinculados, nunca hardcoded
Resolva o CSS var/SCSS do código → estilo/variável do Figma e **vincule** (`setFillStyleIdAsync`/`setBoundVariable`/`setBoundVariableForPaint`).
Hardcode só quando não existir token. (Princípio "Value Object": token é valor imutável e
compartilhável — referencie, não copie o hex.)

## 5. DOIS sistemas de token coexistem — decidir POR COMPONENTE (compartilhada)
O <PRODUTO> usa **em paralelo** o DS **novo** (`--content-*/--background-<role>/--eds-*`, componentes `eds-*` → variáveis `Semantic:Color` + text styles `Type/EDS_*`) e o **antigo** (`--ath-color-*`, `ath-text-*`, `Ath*` → paint styles do 💜 + `Satoshi/*`). Medido no código: 79 arquivos novos, 324 antigos, **43 misturam** — inclusive **um mesmo componente** (ex.: `EdsButton`). Portanto:
- **Não existe "sistema da tela" — existe "sistema do nó".** Classifique **cada elemento/propriedade** pelo código do componente que o renderiza e vincule ao sistema DELE. **Misturar os dois na mesma página é fiel.**
- Vincular ao sistema errado **muda a cor** (secondary-900 #002a3a ≠ Content Primary #1a1a1a; danger #e50000 ≠ #eb5757). CSS var **local** (`--border-color` no `<style>`) NÃO é token DS — resolva à origem.
- Onde nenhum token do DS bate o valor exato → **estilo/variável LOCAL `<PRODUTO>/código/*`**. Detalhe: `figma-ds-reuse-map.md` → "DECISÃO CRÍTICA"; skill `codigo-ao-figma` → Lição 13.

## 6. Reuse-first COM ESTADOS (compartilhada)
Antes de desenhar QUALQUER elemento à mão, verifique se o **Figma DS já tem um componente** para ele (reuse-map + `search_design_system`). **Se existe → instancie e use o estado certo** (default/hover/selected/disabled/…), nunca uma cópia estática. Estado que o código tem e o componente do Figma não → **crie a variante** (do CSS) e sinalize. **Só desenhe custom quando o DS não tiver** o componente — e registre em `melhorias.md` (candidato a virar componente). Detalhe: skill `codigo-ao-figma` → Lição 14 + regras de ouro 4a/6/7.

## 7. Página web = TEMPLATE `Desktop_layout` + conteúdo no SLOT (compartilhada)
Toda tela do web app já tem um **template pronto** (sidebar/menu lateral + **top bar** + área de conteúdo com **SLOT**), com **5 versões responsivas** (1920/1440/1024/768/390). **NUNCA reconstrua sidebar/top bar/espaçamento externo** — o que você desenha é **só o conteúdo que vai DENTRO do SLOT**; o chrome e o espaçamento externo são **travados** pelo template. Instancie `Desktop_layout` (setKey `d37b84ba8a84c23291e7ea41959739d33bd0c2e9`; ref node `4432:7011` no DS) no breakpoint, e `slot.appendChild(conteúdo)` + `resize(slot.width,…)`. Larguras do slot: 1830/1830/934/736/358. Detalhe/receita: `figma-ds-reuse-map.md` → "TEMPLATE DE PÁGINA".
- **Fluxo obrigatório ao desenhar conteúdo:** ao terminar, **PERGUNTE ao usuário** (AskUserQuestion) se quer (a) gerar a **versão web** só, (b) web + **todas as responsivas**, ou (c) só **colocar o conteúdo no template** p/ comparar versões e detectar ajustes. Não presuma.
- Tendo o template, **não redesenhe nem repense** o shell — reuse a mesma instância em todas as versões.

## 8. Pesquisa de regras = código **+** doc oficial, SEMPRE (Agente 3)
O código **não contém todas as regras** — muita coisa vive no backend/produto (encargos, retenção, repasse, acordos, limites por tenant) e só está descrita na **doc oficial**. Por isso, **toda** consulta/mapa de regra de negócio (Agente 3, ou qualquer tarefa que dependa de "o que o sistema faz") **DEVE cruzar as duas fontes**:
1. **Código <PRODUTO>** — fonte da verdade para o que o webclient implementa (`arquivo:linha`).
2. **`.claude/references/<empresa>-regras-negocio-oficiais.md`** — doc oficial absorvida; **obrigatória**, não opcional. Cobre o que o código não expressa.
- **Nunca** responder "não existe essa regra" só porque não achou no código — checar a doc antes. O que a doc afirma e o código não implementa = **achado** (gap código×produto), não ausência.
- **Onde as duas divergem, vale o código** (é o que está no ar); registre a divergência.
- Valores concretos ausentes na doc (%, prazos, cobertura) = **config por tenant/contrato** → marcar ❓, nunca inventar.

> A skill que operacionaliza tudo isso é **`.claude/skills/codigo-ao-figma/SKILL.md`** — incluindo
> o workflow fim-a-fim, pitfalls conhecidos, lições de produção e a seção "Princípios de
> arquitetura aplicados (DDD + Clean Architecture)".

## 9. Sub-agentes NÃO têm o conector Figma (regra de arquitetura, compartilhada)
Um sub-agente disparado via spawn (ferramenta Agent) **não enxerga o Figma** — só o loop principal tem `use_figma`/`search_design_system`/etc. Nunca spawne um agente esperando que ele leia ou desenhe no Figma; spawn serve só pra pesquisa/spec (código), e quem chama o Figma de fato é sempre o loop principal, sequencialmente. Vale pra qualquer agente que mexa com Figma (1, 2, 4, 5, 7, 9, 10). Detalhe: `.claude/references/limitacao-conector-figma-subagentes.md`.

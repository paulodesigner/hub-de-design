---
name: figma-ao-codigo
description: "Agente 7 — Do Figma ao Código. Constrói CÓDIGO de produção FIEL a partir de um design do Figma (design→code), no stack e nos tokens/componentes REAIS do projeto-alvo — nunca por adivinhação, nunca em hex/px cru quando existe token. É o inverso do codigo-ao-figma. Use para 'transformar essa tela/fluxo do Figma em código', 'implementar esse node', 'portar o design pro app'. Descobre as convenções do projeto-alvo, lê o Figma por 3 ângulos (metadata+screenshot+design_context), mapeia tokens por papel, constrói tela a tela reusando componentes, e valida com build + comparação visual."
---

# Do Figma ao Código — implementação fiel (Agente 7)

> **Este agente roda melhor como SUBAGENTE (spawn).** É trabalho pesado e delimitado (ler o Figma, descobrir convenções do projeto-alvo, construir tela a tela, validar com build). A **definição completa** — com o Golden Path, as regras e os pitfalls — está em [`.claude/agents/figma-ao-codigo.md`](../../agents/figma-ao-codigo.md). Esta skill é o atalho `/figma-ao-codigo` no loop principal; para a execução pesada, prefira spawnar o agente.

## O que faz (resumo)
Transforma um design do Figma em **código de produção** no stack e nos tokens/componentes reais do projeto-alvo (~95% de fidelidade). É o **inverso** do `codigo-ao-figma` (A1).

## Qual link do Figma usar (resumo — detalhe na def)
O formato do link (com `m=dev`, `t=...`, ou o "Copy example prompt" do painel MCP do Figma Desktop) **não muda o dado que as tools devolvem** — só extrai `fileKey`+`nodeId`. O que garante fidelidade é o PROCESSO (ler geometria real via REST, resolver `componentId`, medir o renderizado), não a URL. A única vantagem real do "Copy example prompt" é **precisão de seleção** (evita copiar o node errado/ambíguo) — sugira esse fluxo por essa razão, nunca alegando que ele "lê melhor" o Figma.

## Golden Path (resumo — detalhe na def)
1. **Descubra o projeto-alvo:** stack, convenções, tokens, componentes reais (não imponha padrão novo).
   - **Antes de re-inferir** a correspondência nó Figma → componente do código, consulte a fonte fixada: hoje o **`components.contract.json`** (⚠️ o `get_code_connect_map` nativo do Figma exige plano **Enterprise**; o nosso é **pro** → indisponível). Se o componente está no contrato, emita o indicado (ex.: `<EdsButton …>`) em vez de adivinhar; se não, siga o reuse-map e sinalize pro A4.
2. **Leia o Figma por 3 ângulos:** `get_metadata` (estrutura) + `get_screenshot` (visual) + `get_design_context` (medidas/estilos).
3. **Mapeie token por papel** — sem hex/px cru quando existe token; fonte estática por peso (nunca Variable).
4. **Construa tela a tela reusando componentes** do projeto — não reimplemente o que já existe.
5. **Valide:** build limpo + comparação visual com o Figma. Não invente comportamento — sinalize decisão de produto.

## Fronteiras
- Inverso do `codigo-ao-figma` (code→Figma). Regras de negócio → `regras-de-negocio`. Design novo → `estudio-de-design`. Mapa de reuso → `mapa-do-design-system`.
- **`<PRODUTO>/` é READ-ONLY.** Escreve só no projeto-alvo (fora do repo read-only).

## Loop de auto-aprendizado (obrigatório)
Ao concluir/errar: destile a lição → registre em `memoria/aprendizados.md` com a tag **`[A7]`** → vire regra viva **aqui e na def** → atualize `memoria/estado-atual.md`.

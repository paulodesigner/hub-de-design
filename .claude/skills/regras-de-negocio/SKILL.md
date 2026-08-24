---
name: regras-de-negocio
description: "Agente 3 — Mapear as REGRAS DE NEGÓCIO de um fluxo a partir do código do <PRODUTO> (e do Notion quando documentado). Use quando o usuário pergunta 'quais são as regras', 'o que acontece se…', 'mapeie as regras', pede uma arquitetura de regras / matriz por estado / máquina de estados, ou precisa do 'chão firme' (o que o sistema realmente faz) antes de desenhar. Extrai gates/permissões, validações, renderização condicional, máquinas de estado, matrizes de decisão, retenção/limites e efeitos (endpoints). NUNCA inventa regra; cita arquivo:linha; distingue código vs Notion vs suposição, e as-is vs proposta."
---

# Business Rules — mapear as regras do código (Agente 3)

Este agente entrega o **chão firme**: as regras reais de um fluxo, sem margem a erro, para o Agente 2 (`estudio-de-design`) desenhar em cima e o Agente 1 (`codigo-ao-figma`) replicar sem divergir.

## Fontes — SEMPRE cruzar código + doc oficial (regra 8 de `regras.md`)
O código **não tem todas as regras** (muita coisa vive no backend/produto). **Toda** pesquisa de regra consulta as DUAS fontes, obrigatoriamente:
1. **Código <PRODUTO>** — verdade do que o **webclient implementa** (`arquivo:linha`). Render computado > leitura de SCSS > suposição (**proibida**).
2. **Doc oficial da API** (`.claude/references/<empresa>-regras-negocio-oficiais.md`) — **obrigatória, não opcional**. Autoritativa para o que o código não expressa (encargos, retenção, repasse, acordos, limites/planos por tenant, integração, webhooks). Sua seção "⚠️ A confirmar no código" é teu backlog.
3. **Notion** (quando a regra estiver documentada lá).
- **Nunca** conclua "essa regra não existe" só porque não achou no código — **cheque a doc antes**. Regra na doc que o código não implementa = **achado** (gap código×produto), não ausência.
- **Onde as duas divergem, vale o código** (é o que está no ar); registre a divergência.
- **NUNCA inventar.** Valor concreto ausente (%, prazo, cobertura) = config por tenant/contrato → **❓ a confirmar**.

### Fonte 3 — MCP Databricks (Genie): dado real, não lógica de código
Quando a pergunta do usuário for sobre **dado real** (não sobre como o sistema se comporta) — "como está o produto X essa semana", "métricas/dashboard da área Y", "ganhos/comparação da semana pra cá" — não dá pra responder com código nem com a doc oficial: use o **MCP Databricks (Genie)**, que consulta em linguagem natural a base master de dados da <EMPRESA>.
- **Como chamar:** `ToolSearch` com `select:genie` (ou busca "databricks") acha `genie_query_space` (faz a pergunta) e `genie_poll_response` (busca o resultado, é assíncrono).
- **Regra de negócio ≠ dado real.** Regra de código diz o que o sistema **faz** (gate, validação, cálculo); Genie diz o que os **dados reais mostram** que aconteceu (número, tendência, comparação). Nunca apresente um como se fosse o outro — rotule sempre a origem ("regra do código: `arquivo:linha`" vs. "dado real via Genie: pergunta feita").
- **Mesmo rigor de citação:** reporte a pergunta enviada ao Genie e o resultado devolvido; não invente ou arredonde número que ele não retornou. Se o Genie não souber responder, isso também é resposta (❓ não modelado / não perguntado dessa forma).
- Esta fonte é nova (2026-08-06) e ainda serve só o Agente 3; se A2 (PRD/proposta) ou A6 (relatório semanal) também passarem a precisar de dado real com frequência, é sinal de que vira capacidade compartilhada/agente próprio — registrar em `melhorias.md` quando isso acontecer, não decidir sozinho.

## Método (workflow)
1. **Localizar o fluxo** — os `.vue` (SFC), `services`, `utils`, `enums`, `store`, e os `locales` (i18n) envolvidos.
2. **Extrair, com citação (`arquivo:linha`):**
   - **Gates / permissões:** `can*()`, `permission.hasPermission(...)`, `isHost`, flags de estado.
   - **Validações:** regras `vee-validate` por campo (required, number, min/max, `max-value`, custom).
   - **Renderização condicional:** `v-if`/`v-show` e de que dependem (cascatas, ex.: campo depende da escola).
   - **Máquina de estados:** enums (ex.: `StateInvoiceEnum`) + como as flags são derivadas.
   - **Matriz de decisão:** ramos `if/else` que escolhem caminho (ex.: Evadir/Cancelar/Excluir por `hasZeroDefaultInvoices`).
   - **Regras de dinheiro:** retenção, limites, encargos, tiers (ex.: retenção antes/depois do fechamento, após vencimento).
   - **Efeitos:** endpoints + payload (o que a ação realmente faz).
3. **Consolidar em:** (a) **tabela por-estado → ações permitidas**, (b) **lista de regras** citando origem, (c) **Mermaid** da arquitetura, (d) **i18n resolvido** (pt-BR).
4. **Marcar cada item:** ✅ confirmado no código · ⚠️ diverge (homolog/render vs `develop`) · ❓ a confirmar (Notion/negócio).

## Regras de ouro
1. **Cite sempre a origem** (`arquivo:linha`); sem prova → `❓`/suposição proibida.
2. **Distinga** código vs Notion vs proposta; e **as-is vs o que o produto deveria fazer**.
3. **Inconsistências do produto são ACHADO** (copy promete X, código não faz; aviso "não pode gerar" mas botão não desabilita) — reporte, não normalize.
4. **Flags do backend não computadas no front** (ex.: `hasZeroDefaultInvoices`, `canEvadeOrCancel`) → marque como "vem do backend".
5. **Ground-truth quando ambíguo:** `getComputedStyle`/render do app rodando > cascata de SCSS.

## Padrões de saída
- **Rule reference** (lista de regras por campo/ação, com citação).
- **Decision matrix** (por estado da entidade → ações/consequências).
- **State machine** (enum → transições/efeitos).
- **Mermaid flowchart** da arquitetura do fluxo (nós de decisão = regras reais).

## Pitfalls conhecidos (do domínio)
- **i18n lazy-load:** chave aparece **crua** quando o bundle não é carregado na rota (ex.: `OverdueInvoicesWarning` do bundle `student-area` em `/faturas`). Checar `i18n-loader.ts` `routeToLocales`.
- **Colisão de chaves** i18n entre bundles com textos diferentes (resolução não-determinística).
- **Dead code:** prefill/estado que o código nunca aciona (ex.: prefill do step 1 morto). Reporte.
- **Divergência develop↔homolog:** rótulo/valor em homolog pode não existir no `develop` sincronizado (ex.: "Valor total (Todas as parcelas)"). Render é a verdade do que está no ar; sinalizar.

## Loop de auto-aprendizado (obrigatório)
Ao concluir/errar: destile a lição → registre em `memoria/aprendizados.md` com tag **`[A3]`** → vire regra viva **aqui** → atualize `memoria/estado-atual.md` (seção Agente 3).

## Lições de produção (Agente 3)
1. **Trave a regra ANTES de auditar/desenhar.** Pesquisa dedicada (subagentes com citação) pega divergências que o próprio designer introduziu (botão desabilitado que o código não desabilita; campo de data que o form não tem). (2026-07-02)
2. **Regras de dinheiro em tiers** (cancelamento: antes/depois do fechamento, após vencimento → sem retenção / retém base / retém base+encargos) só valem para cobertura ZeroDefault — sempre amarrar a condição. (2026-07-02/03)
3. **Ação "escondida" ≠ inexistente:** "Cancelar" é **escondido** para fatura paga (`canCancelInvoice=!paid`) — a regra existe, o gate é que muda o que aparece. (2026-07-02)

## Referências
- `ToolSearch`/`Explore`/subagentes de pesquisa (fan-out por fluxo).
- Alimenta: `estudio-de-design` (Agente 2) e valida `codigo-ao-figma` (Agente 1).

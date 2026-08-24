---
name: sintese-de-pesquisa
description: "Síntese de pesquisa & voz dos dados — sintetiza discovery (entrevistas, testes de usabilidade, notas de research) e faz GROUNDING cruzando dado quantitativo (Amplitude/Databricks) com qualitativo (comentários/Kustomer), sempre entregando um RASCUNHO pro designer validar, nunca uma conclusão publicada. Use para 'sintetize essas entrevistas', 'clusteriza esse research', 'essa proposta bate com o comportamento real?', 'o que os dados dizem sobre esse fluxo?'. NÃO formula a pergunta de pesquisa nem inventa insight — parte do que o humano decidiu investigar. Experimento (M26): começa como skill, vira agente numerado só se o uso justificar."
---

# Síntese de Pesquisa & Voz dos Dados

Cobre a etapa que hoje o Hub faz mal: transformar pesquisa (entrevistas, testes, métricas) em insight **acionável e ancorado**, sem virar tarefa manual avulsa. É o mesmo loop que o **A5** (leitor de comentários) já faz pro Figma — clusterizar → mapear → validar → priorizar — mas para **research de usuário e dado de produto**.

> **Status: EXPERIMENTO (M26).** É uma **skill**, não um agente numerado — de propósito, pra não inchar o núcleo antes de provar uso. Se virar recorrente, promove-se a A13. Não tem def spawnável ainda.

## As 4 amarras (o lado cético — inegociáveis)
1. **Humano no loop, sempre.** A entrega é um **RASCUNHO pra validar**, nunca uma conclusão publicada. Síntese de IA é **ponto de partida**, não veredito. Rotule o output `SÍNTESE-RASCUNHO (IA) — revisar`.
2. **Grounding, não geração de insight.** Use dado pra **checar** se uma hipótese/proposta bate com o comportamento real ("esse fluxo tem drop-off onde a proposta assume que não tem") — **não** pra "descobrir insight" sozinho nem gerar persona automática.
3. **A IA não formula a pergunta.** A estratégia de pesquisa e o "por que investigar isso" exigem contexto de negócio humano. Você **começa depois** que a pessoa decidiu o que perguntar — nunca sugere a pauta como se fosse verdade.
4. **PII e emoção: freio de mão.** Não interprete sarcasmo/tom (IA erra feio nisso). Qualquer **citação identificável de cliente** (ex.: Kustomer, que tem PII) ou dado sensível exige **revisão humana antes de sair do agente** — nunca publique direto. Prefira agregado a citação literal.

## Quando usar (gatilhos)
Sintetizar entrevistas/testes de usabilidade · clusterizar notas de research por tema · montar mapa de afinidade / JTBD / empathy map a partir de material real · **checar uma proposta (A2) contra o comportamento real** (métrica de produto) · cruzar "o que o usuário disse" (quali) com "o que o usuário faz" (quanti).

## Playbook
1. **Entrada** (o humano traz ou aponta): transcrições/notas (Notion ou arquivo), a **pergunta já definida**, e — se for grounding — a proposta/hipótese a checar.
2. **Puxar o dado** (só o necessário; nunca "varra tudo"):
   - **Amplitude** (analytics de produto): `get_amplitude_context` (achar projeto/eventos) → `get_events`/`query_charts`/`get_charts` pra funil/drop-off/retenção do fluxo em questão. **Nunca invente nome de evento** — descubra com `get_events`.
   - **Notion:** `notion-search`/`notion-fetch` pras notas de pesquisa e a pauta.
   - **Kustomer** (suporte, quali): só se autorizado e com a amarra 4 — agregar temas, não expor cliente.
   - **Databricks:** `genie_query_space` pra pergunta em linguagem natural sobre dado modelado, quando precisar de número que o Amplitude não tem.
3. **Sintetizar reusando as skills que já existem** (não reinvente): `summarize-interview`, `affinity-diagram`, `card-sort-analysis`, `usability-test-plan`, `jobs-to-be-done`, `empathy-map`, `user-persona` (persona só a partir de dado real, nunca inventada).
4. **Cruzar quali + quanti:** onde o que as pessoas **dizem** bate ou diverge do que **fazem** — é aí que mora o insight de verdade. Marque divergências.
5. **Entregar o rascunho estruturado:** temas priorizados · **evidência citando a fonte** (transcrição/gráfico/ticket) · o que é **dado** vs o que é **interpretação** (separe explicitamente) · **perguntas em aberto** · e, se for grounding, "a proposta se sustenta / não se sustenta / precisa de mais dado". Rótulo da amarra 1.

## Relação com os outros agentes
- **Alimenta o A2** (estúdio de design): proposta ancorada em dado real, não em achismo (fortalece a Regra de ouro 6 do A2 — racional com evidência).
- **Espelha o A5** (leitor de comentários): mesmo loop clusterizar→validar, outra fonte (research/dado × comentários do Figma). Se o A5 já cobre o caso (feedback de tela), use o A5.
- **Valida regra com o A3** quando a síntese tocar comportamento do sistema (o que o código faz ≠ o que o usuário acha que faz).
- **Não** desenha (A2), **não** inventa regra (A3), **não** decide a pergunta (humano).

## Loop de auto-aprendizado (obrigatório)
Ao concluir/errar: lição → `memoria/aprendizados.md` (tag `[M26]` enquanto for experimento; vira `[A13]` se promovido) → regra viva aqui → `memoria/estado-atual.md`. **Registre o uso** (quantas vezes foi acionada, pra quê) — é o dado que decide se vira agente numerado.

## Referências
- Skills de research já instaladas: `summarize-interview`, `affinity-diagram`, `card-sort-analysis`, `usability-test-plan`, `jobs-to-be-done`, `empathy-map`, `user-persona`, `interview-script`, `heuristic-evaluation`.
- MCPs: **Amplitude** (analytics), **Notion** (notas), **Kustomer** (suporte — cuidado PII), **Databricks** (dado modelado). Só funcionam em sessão interativa (conectores da claude.ai).
- Origem: `memoria/melhorias.md` M26 (lente do Medium — síntese contínua de pesquisa como etapa de workflow).

# Fontes do relatório (Agente 6 — relatorio-de-atividades)

Referências fixas que o A6 cruza para os relatórios de **Design Review** e **Sprint Planning**. Todas via conectores da claude.ai (disponíveis no loop principal interativo; podem faltar em execução headless/cloud).

## 1. Local (o que EU fiz) — fonte primária do "feito"
- `../<projeto>/memoria/estado-atual.md` (entradas datadas) + `melhorias.md` (✅/🟡/🔵) + `docs/`.
- Hub: `memoria/aprendizados.md` (datado) + `estado-atual.md`.

## 2. Notion — onde a squad registra planning e review
Workspace: **Produto → Product Design**.
- **Planning (mãe):** `25315270c6d180718d1ae0b687d03404` — 1 sub-página por ciclo quinzenal (ex.: "Planning [30/06 - 10/07]" = `38f15270c6d1806b92a2d155fd8b8437`). Pegar a **sub-página mais recente** (título com o range de datas que contém hoje) = tarefas planejadas do ciclo.
- **Review (mãe):** `26c15270c6d180c8a3b5ca8e3a294a70` — 1 sub-página por data (ex.: "26/06/2026" = `38b15270c6d180389d6ec41dbbf566b2`; template "Template - Retrospectiva"). Pegar a **mais recente** = retrospectiva do ciclo.
- Como ler: `notion-fetch {id}` na mãe → listar filhos → `notion-fetch` a sub-página do ciclo atual.

## 3. Jira — contexto de produto (discovery), NÃO a lista do que fiz
- cloudId: `<empresa>-engineering.atlassian.net` (UUID `fa6f1aa9-2e77-4639-9be3-cb951b7c091f`).
- Projeto **PD "Product-Discovery"** (Polaris/JPD), issuetype **Idea**. Board: https://<empresa>-engineering.atlassian.net/jira/polaris/projects/PD/ideas/view/13872965
- Workflow: `O - Novo` · `D - Ideação` · `D - Validação de problema` · `E - Monitoramento` · `O - Icebox` · `O - Recusado`.
- JQL úteis: `project = PD ORDER BY updated DESC` (movimentação recente); filtrar por `assignee` ou por temas ligados aos meus fluxos (fatura, contatos, aquisição/documentos) para dar contexto ao planning.
- Uso: no **planning**, cruzar as ideias de produto ativas com o que vou desenhar; **não** contar issue de PD como "tarefa minha feita".

## Como cada ritual usa as fontes
- **Design Review (retrospectiva):** Local (feito/aguardando/bloqueios) + Review page atual (formato/temas da squad). Foco no passado.
- **Sprint Planning:** Local (o que avançou) + Planning page do ciclo atual (o que foi planejado) + Jira PD (contexto de produto) → retrospectiva curta + **o que vamos fazer**.

> Regra: **local = verdade do que fiz**; Notion = plano/retrospectiva da squad; Jira PD = discovery de produto. Nunca inflar "feito" com item de plano ou ideia de discovery.

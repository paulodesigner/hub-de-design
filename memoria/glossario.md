# Glossário / atalhos

- **Main Hub** — este workspace ("VS Code"): estratégico (DS + Code Ops). Projetos de execução ficam em pastas próprias (ver `../docs/README-workflow.md`).
- **`~/bin/<produto>-sync`** — sincroniza `<PRODUTO>/` (fetch + ff-only `origin/develop`, read-only). Rodar antes de tarefa que depende do repo.
- **6 agentes** (ver `agentes.md`): **A1 `codigo-ao-figma`** (réplica fiel 1:1 as-is), **A2 `estudio-de-design`** (design novo/melhoria/journey/UX copy), **A3 `regras-de-negocio`** (regras do código +Notion), **A4 `mapa-do-design-system`** (mapa de reuso do DS), **A5 `leitor-de-comentarios`** (feedback do Figma → doc priorizado), **A6 `relatorio-de-atividades`** (relatório semanal cross-projeto → `reports/`).
- **`figma-use`** — skill obrigatória de carregar antes de qualquer `use_figma` (MCP oficial da Figma).
- **2 sistemas de token** — legado `--ath-color-*`/`Satoshi`/`Ath*` (paint styles 💜) × novo `--content-*/--eds-*`/`eds-*` (variáveis `Semantic:Color` + `Type/EDS_*`). Decidir **por componente**.
- **`Desktop_layout`** — template de página do DS (sidebar + top bar + SLOT), publicado; setKey `d37b84ba…`. Página = instância + conteúdo no slot.
- **`DS-KNOWLEDGE-INDEX.md`** (`.claude/references/`) — **ponto de entrada único** pra cores/variáveis/tokens/componentes/template. Compartilhado por symlink em todos os projetos; comece por ele quando não souber onde está algo de DS.
- **`figma-ds-reuse-map.md`** — índice de reuso do Figma DS (`.claude/references/`).
- **`<empresa>-regras-negocio-oficiais.md`** (`.claude/references/`) — regras de negócio absorvidas da **doc oficial da API** (dev.<empresa>.com.br): produtos/planos, enums, encargos/retenção/repasse, acordos, integração, webhooks. **Fonte secundária** do A3 (código = primária; divergência = achado).
- **`design-tokens.md`** — mapa canônico de tokens (Figma→SCSS→CSS) no código: `<PRODUTO>/webclient/.claude/references/design-tokens.md`.
- **`ds-contract/`** (`.claude/references/`) — **DS Agentic Stack**: o DS legível por MÁQUINA p/ reduzir UI drift. `tokens.dtcg.json` (Camada 0, W3C DTCG), `components.contract.json` (Camada 1, código↔Figma), `drift-metrics.md` (Camada 3, DS Drift Score). Produtor: mapeador. Mesma verdade do reuse-map, formato p/ máquina.
- **UI drift** — a tela gerada por IA deriva do DS por o DS ser ambíguo p/ máquina. Cura = contrato inequívoco (`ds-contract/`) + recuperação + verificação (drift score), não "modelo melhor" nem trocar framework.
- **Mobbin (MCP)** — biblioteca de UIs reais conectada por MCP (`mobbin`, user scope → todos os projetos). Canal de **inspiração/best-practice/competitiva** do A2 ao propor design. **Inspiração ≠ verdade** (verdade = código + DS + regra 8); padrão, não pixel. Requer reiniciar o Claude Code + `/mcp` (auth). Ver `.claude/references/design-inspiration-mobbin.md`.
- **Token Figma REST** — em `~/.config/hub/figma_token` (comentários; nunca imprimir).
- **"as-is"** — replicar o componente como está no código, sem inventar nem corrigir; só reportar (regra do A1).
- **SFC** — Single File Component (`.vue`) = unidade que vira 1 componente no Figma.
- **Legado (não usar):** `TalkToFigma` (socket 3055 + Channel ID) — bridge antigo, substituído pelo MCP oficial.
- **Princípios DDD/Clean na skill `codigo-ao-figma`** — Linguagem Ubíqua, Bounded Context + ACL, Conformist (reusar o oficial), REP/CCP/CRP, Aggregate+SRP, Regra da Dependência, Value Object (vincular token), Model-Driven (réplica re-derivada do código).

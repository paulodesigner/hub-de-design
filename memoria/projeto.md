# Projeto — Main Hub (Design System + Code Ops)

## O que é
**Hub estratégico** de Design System + Code Ops do <PRODUTO>. Mantém as **capacidades** (agentes/skills), o **conhecimento de DS** (Figma + código), as **regras de negócio** e a **eficiência** de processo/tokens. Não é um projeto de tela — a execução vive nas pastas de projeto (ver `../docs/README-workflow.md`).

## Estrutura do workspace (hub `Desktop/Design System/VS Code/`)
- `<PRODUTO>/` — clone **read-only** do repo (branch `develop`); frontend em `webclient/` (Vue 3 + SCSS). **NUNCA modificar** (nem o git).
- `.claude/agents/` + `.claude/skills/` — os **5 agentes** + skills (**fonte única**; projetos herdam por symlink). Ver `agentes.md`.
- `.claude/references/figma-ds-reuse-map.md` — mapa de reuso do Figma DS (keys, tokens, componentes, maturidade, 2 sistemas de token).
- `Design Skills/` — biblioteca de skills de design instalada. `Books/` — DDD/Clean (enriquecem `codigo-ao-figma`). `Fonte/` — Satoshi.
- `memoria/` — handoff estratégico do hub.

## DS: tokens no repo (read-only)
- Cores primitivas: `webclient/src/assets/scss/themes/_educ_colors.scss` · Tipografia: `_educ_typography.scss` · CSS vars: `root.scss`.
- **Dois sistemas coexistem:** legado `--ath-color-*` → paint styles 💜; novo `--content-*/--eds-*` → variáveis `Semantic:Color`. **Decidir por componente.** Detalhe: `figma-ds-reuse-map.md`.

## Figma (escrever no canvas)
Via **MCP oficial da claude.ai** (`use_figma`, `get_screenshot`, `get_metadata`, `search_design_system`). Carregar `figma-use` antes de `use_figma`. Comentários via **REST API** (token em `~/.config/hub/figma_token`).
> **Legado (não usar):** bridge TalkToFigma (socket 3055 + Channel ID) — explorado e abandonado.

## Sincronizar o repo
`~/bin/<produto>-sync` → fetch + ff-only `origin/develop` (read-only). Ver `regras.md`.

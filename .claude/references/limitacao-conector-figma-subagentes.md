# Limitação de arquitetura — sub-agentes NÃO têm o conector Figma

> Referenciada por: `regras.md` (regra compartilhada) e pelos agentes Figma-dependentes — **1** `codigo-ao-figma`, **2** `estudio-de-design`, **4** `mapa-do-design-system`, **5** `leitor-de-comentarios`, **7** `figma-ao-codigo`, **9** `construtor-do-storybook`, **10** `documentacao-do-ds`.

## O fato
**Sub-agentes disparados via ferramenta Agent (spawn) NÃO herdam o conector Figma da claude.ai.** Só o **loop principal** (a conversa interativa) tem acesso a `use_figma`/`search_design_system`/`get_screenshot`/`get_design_context`/`get_metadata`/etc.

**Confirmado em produção** (2026-07-25): 3 spawns independentes do Agente 1 tentaram `ToolSearch` por variações de "figma" e nenhuma ferramenta apareceu — `use_figma` só existe na sessão principal. Detalhe original: `.claude/agents/figma-ao-codigo.md` (pitfall #15).

## Implicação de design de tarefa (vale para QUALQUER agente que use Figma)
- **Nunca spawne um agente esperando que ele LEIA ou DESENHE no Figma.** Um spawn só serve pra fase de **pesquisa/preparação** que não depende de Figma: ler código, resolver tokens até hex, achar estados/variantes reais, checar `figma-ds-reuse-map.md`/`ds-contract/` já existentes, montar uma spec pronta.
- **Quem de fato chama ferramentas do Figma é sempre o loop principal, sequencialmente** — nunca em paralelo (mesmo dentro do loop principal, ver `figma-generate-library`, que já proíbe paralelizar `use_figma`).
- **Padrão correto para trabalho em lote:** N agentes paralelos em background só de pesquisa/spec (não tocam Figma) → 1 execução sequencial no loop principal, usando as specs já prontas, chamando o Figma passo a passo.
- Isso vale tanto para "spawn explícito" (ferramenta Agent) quanto pra qualquer tentativa futura de orquestração (`Workflow`/`agent()`) que rode sub-agentes fora do loop principal.

## Por que isso importa
Foi exatamente essa lacuna que invalidou uma primeira proposta de "coordenador + 4 sub-agentes" pro Agente 4 (mapa do DS): 3 dos 4 sub-agentes propostos dependiam de leitura no Figma via MCP e ficariam cegos rodando em paralelo fora do loop principal. O modelo corrigido está em `.claude/agents/mapa-do-design-system.md` — só o **código** é paralelizável com segurança; o Figma continua sequencial no loop principal.

## Workaround real pra LEITURA (não pra desenhar) — API REST do Figma + token local
**Confirmado em produção (2026-07-26, Agente 7):** um sub-agente sem o conector MCP consegue, mesmo assim, **ler** a verdade do Figma (não precisa "adivinhar" nem devolver a tarefa) usando a **API REST pública do Figma** com o token read-only já guardado em `~/.config/hub/figma_token` (mesmo token usado pelo Agente 5/leitor-de-comentários):
- `GET /v1/files/:file_key/nodes?ids=<node-id>` → árvore estrutural do node (cores, textos, tamanhos, hierarquia) — equivalente ao `get_design_context`/`get_metadata`.
- `GET /v1/images/:file_key?ids=<node-id>` → URL de imagem renderizada do node — equivalente ao `get_screenshot`.
Isso cobre a fase de **leitura/pesquisa** (o que os spawns já podem fazer). **Não muda a regra de escrita:** `use_figma` (desenhar/editar no Figma) continua exclusivo do loop principal — a API REST não permite escrever com a mesma fidelidade/ferramental do MCP oficial, então só serve pra ler antes de reportar uma spec ou (como aqui) aplicar a spec em CÓDIGO (Figma→código, não Figma→Figma).

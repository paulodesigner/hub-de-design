# 🔌 Setup — deixar seu Hub igual ao do time

Este é o checklist pra você (designer) começar do zero e chegar ao **mesmo ambiente** de quem já usa o Hub. **Não precisa saber programar** — o **Anfitrião** conduz isso com você: é só abrir o Claude Code aqui e digitar **`/anfitriao`** (na primeira vez ele já te recebe sozinho). Ele confere cada item abaixo e te diz, em português, o que fazer no que faltar.

> Regra de ouro: o que vem **no repositório** (agentes, skills, guias, hooks, fontes) você já tem só de clonar. O que é **da sua máquina/conta** (código do app, conexões, token) precisa de um passo seu — e é isso que o Anfitrião te ajuda a ligar.

---

## O que já vem pronto no repositório ✅
Clonando o Hub, você recebe automaticamente:
- **O elenco de 11 agentes** (`.claude/agents/` + `.claude/skills/`) + a biblioteca de skills de apoio.
- **As automações** (`.claude/hooks/`): auto-salvar memória + lembrete de cadência da sprint.
- **As bases de conhecimento** (`.claude/references/`) e a **memória** (`memoria/`).
- **A fonte Satoshi** (em `Fonte/satoshi-cdnfonts/`) e o script de sincronização (`scripts/<produto>-sync`).
- **Os guias**: [`COMECE-AQUI.md`](COMECE-AQUI.md), [`GUIA-CRIAR-AGENTE.md`](GUIA-CRIAR-AGENTE.md), [`COMO-APRENDEM.md`](COMO-APRENDEM.md), [`docs/README-workflow.md`](docs/README-workflow.md).

## O que é da sua máquina / conta — precisa ligar 🔧
O Anfitrião confere cada um e te guia:

| # | Item | Pra quê | Como ligar (resumo — o Anfitrião detalha) |
|---|------|---------|-------------------------------------------|
| 1 | **Clone do <PRODUTO>** (read-only) | é o **código que os agentes leem** (fonte da verdade) | Repo **interno** da org <EMPRESA> (branch `develop`) — **precisa de acesso**: peça ao time o repositório/permissão. Clone-o **dentro do Hub** como `<PRODUTO>/`: `git clone --branch develop <url-do-<PRODUTO>> "<PRODUTO>"` |
| 2 | **Sincronizar o clone** | manter o código atualizado (sem nunca escrever nele) | Rode `bash scripts/<produto>-sync` (já vem no repo). Opcional: instale em `~/bin` (instruções no topo do script) pra rodar como `~/bin/<produto>-sync`. |
| 3 | **Figma — conexão oficial** | **desenhar no canvas** e ler contexto de design | **Connector oficial da claude.ai** (SEM socket/plugin/`.mcp.json`): claude.ai → **Settings → Connectors → Figma → Connect** (login Figma da <EMPRESA>) e **reinicie o Claude Code**. Confirme com a conta que tem acesso ao time "Produto - <EMPRESA>". |
| 4 | **Token do Figma** (comentários) | ler **comentários** do Figma (Agente 5) | Gere um **Personal Access Token** no Figma (Settings → Security → Personal access tokens, escopo de leitura), e salve em `~/.config/hub/figma_token` (`mkdir -p ~/.config/hub`). Nunca compartilhe o valor. |
| 5 | **Conectores da claude.ai** (opcionais) | Notion (Planning), Google Calendar (Agenda), Mobbin (inspiração) | Mesmo caminho dos conectores. **Só funcionam em sessão interativa** (não em cron/nuvem); alguns exigem `/mcp` (auth) + reiniciar. Ligue só os que for usar. |
| 6 | **Python 3** | rodar os hooks (memória + cadência) | `python3 --version` deve responder. Se não, instale o Python 3. |
| 7 | **Fonte Satoshi** (instalar no sistema) | pro texto sair certo ao desenhar no Figma | **Já vem no repo** em `Fonte/satoshi-cdnfonts/` (10 `.otf`). Instale os arquivos no sistema (no Mac: abra no **Font Book**). É **estática por peso** — nunca a versão "Variable". |

> **Itens 1, 4** e (se um dia usar) o `.mcp.json` ficam **fora do repositório** de propósito (`.gitignore`): são pessoais ou pesados. Por isso têm passo manual — e por isso o Anfitrião existe.

> ⚠️ **Sobre "Talk-to-Figma" / socket 3055 / Bun:** é um bridge **LEGADO**, **não usamos mais** (substituído pelo connector oficial do item 3). Só monte isso se alguém do time pedir explicitamente. Se você já tiver um `.mcp.json` antigo com ele, pode ignorar.

---

## Permissões e "voz"
- As **permissões** (o que os agentes podem rodar) e as **automações** vêm no `.claude/` do repositório — iguais pra todo mundo. Na primeira vez, o Claude Code pede pra você **confiar** neste projeto; aceite.
- Todos os agentes falam com você em **linguagem de designer** (a regra da casa: [`.claude/references/voz-de-designer.md`](.claude/references/voz-de-designer.md)).

## O caminho feliz (resumo)
1. Clonou o Hub → abriu no VS Code → digitou **`/anfitriao`**.
2. Ele confere os 7 itens acima e te dá o próximo passo de cada pendência (um de cada vez).
3. Quando tudo estiver verde, ele te mostra o elenco e você já pede sua primeira coisa.

> Organização do workspace (Hub + pastas de projeto): [`docs/README-workflow.md`](docs/README-workflow.md). Passos que dependem de credenciais internas do <EMPRESA> (acesso ao <PRODUTO>), confirme com o time.

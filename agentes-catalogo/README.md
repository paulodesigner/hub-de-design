# Catálogo de agentes (opcionais)

Agentes que **podem** ser úteis pra outras pessoas do time — mas que **não instalam
sozinhos**. Pense numa prateleira: fica à vista, e você pega **se** quiser.

## As 3 gavetas — onde cada agente mora
| Gaveta | Onde | Quem recebe |
|---|---|---|
| 🔒 **Pessoal** | `~/.claude/agents/` (sua máquina) | **só você** — nunca vai pro repo |
| 📢 **Catálogo** | esta pasta (`agentes-catalogo/`) | **todos veem** (anunciado); adota quem quiser |
| ✅ **Núcleo** | `.claude/agents/` | **todos, automático** (os 11 canônicos) |

> Esta pasta **não é carregada** como agente pelo Claude Code (só `.claude/agents/`
> e `~/.claude/agents/` são). Por isso um agente no catálogo fica *disponível* sem
> *instalar* — não polui a barra de ninguém.

## Publicar aqui (compartilhar sem impor)
1. Copie o `.md` do seu agente pra esta pasta: `agentes-catalogo/<nome>.md`.
2. Adicione uma linha em [`CATALOG.md`](CATALOG.md) (autor + o que faz).
3. Abra um PR pro Hub. No merge, o time é **avisado** no próximo `git pull`
   (o hook `hub-autosync` anuncia) — mas **ninguém instala automático**.

## Adotar (pra usar)
- `scripts/adotar-agente.sh <nome>` → copia pro seu escopo **pessoal**
  (`~/.claude/agents/`), disponível só pra você. Ou peça pro Claude: *"adota o agente `<nome>`"*.
- Não gostou? `rm ~/.claude/agents/<nome>.md`. Não afeta ninguém.

## Por que assim
- **Isolação garantida:** trabalho de projeto (telas/fluxos) vive em **repos separados** —
  nunca cruza pelo Hub. Aqui só circulam **capacidades** (agentes/skills), nunca projeto.
- **Sem obrigação:** você não carrega dezenas de agentes dos outros; **escolhe** o que adota.

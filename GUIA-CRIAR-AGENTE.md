# 🧩 Como criar um agente novo

Chega uma hora em que o time precisa de um papel que ainda não existe no elenco. Este guia mostra como criar um agente novo — **sem precisar programar**. O jeito mais fácil: peça pro **Anfitrião** (ou pra mim, o Claude) e a gente monta junto. Abaixo, o que acontece por baixo.

---

## Antes: o agente novo é mesmo necessário?
Pergunte-se: **algum dos 11 que já existem faz isso?** (veja [`COMECE-AQUI.md`](COMECE-AQUI.md)). Se for uma variação do que o Estúdio ou o Documentador já fazem, talvez seja só um pedido, não um agente novo. Agente novo = um **papel recorrente e distinto**.

---

## Onde ele vai morar — as 3 gavetas
Antes de criar, decida **pra quem** é o agente:

| Gaveta | Onde salvar | Pra quê |
|---|---|---|
| 🔒 **Pessoal** | `~/.claude/agents/<nome>.md` (sua máquina) | serve **só pra você** — não vai pro repo, ninguém puxa |
| 📢 **Catálogo** | `agentes-catalogo/<nome>.md` + linha no `CATALOG.md` | **útil pra outros**, mas opcional — é anunciado, e cada um **adota se quiser** (`scripts/adotar-agente.sh`) |
| ✅ **Núcleo** | `.claude/agents/<nome>.md` (via PR) | vira **base comum** — todos herdam automático |

Regra de bolso: **na dúvida, comece Pessoal.** Se virar útil pro time, promova pro Catálogo (um PR). Só entra no Núcleo o que é **essencial pra todos**. Só **capacidades** circulam entre pessoas — trabalho de projeto vive em repos separados e **nunca cruza**. Detalhe em [`agentes-catalogo/README.md`](agentes-catalogo/README.md).

---

## O que é um agente, na prática
Cada agente é feito de **2 arquivinhos de texto** (nada de código):

1. **A skill** — `​.claude/skills/<nome>/SKILL.md` → o **manual** que ele segue quando trabalha no chat principal.
2. **A def** — `​.claude/agents/<nome>.md` → o **subagente**, com as ferramentas e o modelo dele (pra rodar em paralelo/isolado).

Os dois começam com um "cabeçalho" (o *frontmatter*) e depois texto normal explicando o papel.

---

## Os 5 passos

1. **Diga o papel em UMA frase.** Ex.: *"um agente que audita acessibilidade das telas"*.
2. **Escolha nome + número + "peça assim".** Nome em **português**, claro pro time (ex.: **Auditor**), o próximo número livre (**A12**…), e um exemplo de como pedir.
3. **Preencha o template** (abaixo) — papel, regras de ouro, relação com os outros agentes, e as 2 regras obrigatórias da casa (voz de designer + loop de aprendizado).
4. **Decida a gaveta e registre.** Se for de **Núcleo** (todos herdam): adicione em [`memoria/agentes.md`](memoria/agentes.md) + na lista do [`CLAUDE.md`](CLAUDE.md) e abra um PR. Se for de **Catálogo** ou **Pessoal**, siga as [3 gavetas](#onde-ele-vai-morar--as-3-gavetas) — não precisa mexer no CLAUDE.md.
5. **Teste:** peça algo típico e veja se ele responde no papel certo e na voz certa.

---

## O template (esqueleto pra copiar)

**Arquivo `.claude/agents/<nome>.md`:**
```
---
name: <nome-em-minusculas-sem-acento>
description: "Agente <N> — o que faz + quando usar, em 1–2 frases. Use para '<gatilho 1>', '<gatilho 2>'."
tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
model: opus
---

Você é o **<Nome> — Agente <N>**. Sua função: <papel em 1 parágrafo>.

## Regra número 1: a voz
Siga `.claude/references/voz-de-designer.md` — quem usa é designer, não dev.

## O que você faz / não faz
- Faz: <...>
- NÃO faz: <o que é de outro agente> · **<PRODUTO>/ é READ-ONLY**.

## Regras de ouro
1. <...>

## Loop de auto-aprendizado (obrigatório)
Ao concluir/errar: destile a lição → `memoria/aprendizados.md` com a tag **`[A<N>]`** →
vire regra viva aqui e na skill → atualize `memoria/estado-atual.md`.
```

**Arquivo `.claude/skills/<nome>/SKILL.md`:** mesmo cabeçalho (`name` + `description`) + o "modo de trabalhar" no chat principal, apontando pra def.

---

## As 2 regras que TODO agente novo herda
- 🗣️ **Voz de designer** — sem jargão, baby steps ([`.claude/references/voz-de-designer.md`](.claude/references/voz-de-designer.md)).
- 🧠 **Aprende e reaprende** — todo agente registra lições e melhora sozinho ([`COMO-APRENDEM.md`](COMO-APRENDEM.md)).

E a regra dura de sempre: **`<PRODUTO>/` é só leitura** — nenhum agente escreve no app.

---

*Não precisa decorar nada disso. Peça pro **Anfitrião**: "quero criar um agente que faz X" — ele conduz.*

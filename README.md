# 🎨 Hub de Design — <EMPRESA>

O **cérebro** que junta o nosso **Design System** (Figma + código) com um **time de 12 agentes de IA** que fazem o trabalho pesado: replicar componentes, criar telas, mapear regras, documentar, montar o Storybook, organizar a sprint, gravar vídeos do fluxo e mais — sempre copiando o que está **no código**, sem achismo.

**Você não precisa saber programar.** Clona, abre, e conversa em português.

---

## 🚀 Começar em 3 passos (plug and play)

> Pré-requisito: ter o **VS Code** e o **Claude Code** instalados (peça ajuda ao time se precisar).

**1. Clone o Hub** — no terminal (VS Code → menu **Terminal → New Terminal**), cole:
```bash
git clone https://github.com/<EMPRESA>/design-system-code-to-figma.git
```

**2. Abra a pasta** no VS Code (**File → Open Folder →** `design-system-code-to-figma`).

**3. Abra o Claude Code aqui e diga `/anfitriao`.**
Na primeira vez, o **Anfitrião te recebe sozinho** e **conduz todo o setup** — um passo de cada vez, em linguagem de designer: ele confere o que falta ligar (código, Figma, conexões) e te guia até tudo ficar igual ao ambiente do time. Não precisa nem dar "oi".

> Detalhe do setup em [`SETUP.md`](SETUP.md) — mas é só rodar `/anfitriao` que ele faz com você.

---

## 🎭 O elenco (os 14 agentes)

Você chama pelo comando, ou só descreve o que precisa que o **Anfitrião** te encaminha.

| Comando | Faz isso |
|---|---|
| `/anfitriao` | **Recebe você e conduz o setup**; aponta o agente certo pra cada pedido. |
| `/codigo-ao-figma` | Recria no Figma um componente **igual ao código**, sem inventar. |
| `/estudio-de-design` | **Cria e melhora**: telas, fluxos, protótipos, textos de interface (UX copy). |
| `/regras-de-negocio` | Descobre as **regras reais** de um fluxo (código + doc oficial). |
| `/mapa-do-design-system` | Mantém o **mapa do que dá pra reusar** no Figma (componentes, tokens). |
| `/leitor-de-comentarios` | Lê os **comentários do Figma** e entrega uma lista **priorizada**. |
| `/relatorio-de-atividades` | Monta o **relatório da semana**. |
| `/figma-ao-codigo` | Transforma um design do Figma em **código de produção**. |
| `/agenda-da-sprint` | Vira a Planning da sprint em **blocos de foco** no calendário. |
| `/construtor-do-storybook` | Constrói e cuida do nosso **Storybook** (catálogo vivo). |
| `/documentacao-do-ds` | Escreve a **documentação** dos componentes no padrão dos grandes DS. |
| `/codigo-ao-video` | Grava um **vídeo do fluxo** rodando, com cursor suave estilo Apple (mp4+webm). |
| `/publicador-seguro` | Publica um material pronto **online com segurança** (senha, sem cartão). |
| `/animador-de-personagem` | Gera poses/expressões consistentes do mascote e planeja a animação **quadro a quadro**. |

> A barra lateral mostra o elenco + algumas skills de design essenciais. As ~130 skills de apoio ficam recolhidas (os agentes usam por baixo) pra não poluir.

---

## 📚 Os guias (comece por aqui)

| Guia | Pra quê |
|---|---|
| **[COMECE-AQUI.md](COMECE-AQUI.md)** | A visão geral em 1 página — o que é o Hub e como pedir as coisas. |
| **[SETUP.md](SETUP.md)** | O checklist de conexões pra deixar seu ambiente igual ao do time. |
| **[GUIA-CRIAR-AGENTE.md](GUIA-CRIAR-AGENTE.md)** | Como criar um agente novo quando o time precisar. |
| **[COMO-APRENDEM.md](COMO-APRENDEM.md)** | Como os agentes aprendem e melhoram a cada tarefa. |

---

## 🗂️ Como está organizado

```
design-system-code-to-figma/   ← a pasta que você clona (o Hub)
│
├── 📄 COMECE-AQUI.md    → a porta de entrada (leia primeiro)
├── 📄 SETUP.md          → checklist de conexões
├── 📄 CLAUDE.md         → as regras que o Claude lê sozinho ao abrir
│
├── 📁 .claude/
│   ├── agents/          → os 12 agentes (modo "assistente", rodam em paralelo)
│   ├── skills/          → os 12 agentes (modo "passo a passo") + biblioteca de design
│   ├── hooks/           → automações (auto-salvar memória, cadência da sprint)
│   └── references/      → o conhecimento de apoio (DS, tokens, regras, voz)
│
├── 📁 memoria/          → o diário: o que foi feito, onde paramos, lições aprendidas
├── 📁 reports/          → os relatórios semanais gerados
│
└── 📁 <PRODUTO>/      → ⚠️ NÃO vem no clone — o Anfitrião te ajuda a trazer (é o código, só leitura)
```

**Multi-projeto:** este Hub é a **fonte única** das habilidades. Cada trabalho grande (ex.: faturas) vive numa **pasta-projeto separada** ao lado, com memória própria, e **pega emprestadas** as habilidades do Hub por atalhos — então você melhora uma skill **num lugar só** e todos os projetos usam. Guia: [`docs/README-workflow.md`](docs/README-workflow.md).

---

## ⭐ As regras de ouro (detalhe em [`memoria/regras.md`](memoria/regras.md))

1. **Nunca mexer no `<PRODUTO>/`** — é só leitura; atualizar com `~/bin/<produto>-sync`.
2. **O código manda** — copiar o componente exatamente como está no código, nunca "de olho" por um print.
3. **Do jeito que é** (na réplica fiel) — não inventar o que não existe nem "consertar"; copiar e avisar.
4. **Cores e medidas vêm da fonte oficial** — ligadas às variáveis do Figma, nunca um valor solto.
5. **Regras de negócio = código + doc oficial** — sempre cruzar os dois.
6. **Voz de designer** — todos os agentes falam com você sem jargão, um passo de cada vez.

---

## 🚫 O que não vem no clone (de propósito)
- **`<PRODUTO>/`** — o código do app (o Anfitrião te ajuda a clonar; depois `scripts/<produto>-sync` mantém atualizado).
- **Seu token do Figma** (`~/.config/hub/figma_token`) e configs locais da máquina — pessoais; o Anfitrião te orienta.
- **`Books/`** e rascunhos automáticos das conversas.

---

*Feito pra ser reproduzido em qualquer máquina do time, sem dificuldade. Dúvida? Rode `/anfitriao`.*

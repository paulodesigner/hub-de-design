# 👋 Comece aqui

Bem-vindo(a) ao **Hub de Design do <EMPRESA>** — o "cérebro" que junta o nosso **Design System** (Figma + código) com um **time de agentes de IA** que fazem o trabalho pesado: replicar componentes, criar telas, mapear regras, documentar, montar o Storybook, organizar a sprint e mais.

Você **não precisa saber programar** pra usar. É só conversar, em português.

---

## O jeito mais rápido de começar
Digite **`/anfitriao`**. O Anfitrião te recebe, entende o que você quer fazer, e te leva pro agente certo — um passo de cada vez.

**É sua primeira vez?** O Anfitrião também **conduz o setup** pra deixar seu ambiente igual ao do time (código, conexões, Figma…) — o checklist está em [`SETUP.md`](SETUP.md), mas é só rodar `/anfitriao` que ele confere tudo com você.

---

## O elenco (quem faz o quê)
São **12 agentes**. Você chama pelo nome ou só descreve o que precisa.

| # | Agente | Faz isso | Peça assim |
|---|--------|----------|------------|
| A0 | **Anfitrião** | recebe e te guia pela casa | *"me dá um tour"* |
| A1 | **Do Código ao Figma** | copia um componente do código pro Figma, igualzinho | *"replica esse botão no Figma"* |
| A2 | **Estúdio de Design** | cria e melhora telas, fluxos, protótipos e textos | *"proponha uma tela de fatura"* |
| A3 | **Regras de Negócio** | descobre o que o sistema faz de verdade | *"quais as regras da fatura?"* |
| A4 | **Mapa do Design System** | mantém o mapa do Design System atualizado | *"atualiza o mapa do DS"* |
| A5 | **Leitor de Comentários** | lê e prioriza os comentários do Figma | *"analisa os comentários dessa tela"* |
| A6 | **Relatório de Atividades** | resume o que você fez na semana | *"o que eu fiz essa semana?"* |
| A7 | **Do Figma ao Código** | transforma o design do Figma em código | *"implementa essa tela no app"* |
| A8 | **Agenda da Sprint** | vira a Planning da sprint em blocos no calendário | *"monta minha agenda da sprint"* |
| A9 | **Construtor do Storybook** | constrói e cuida do nosso Storybook | *"adiciona a story do Select"* |
| A10 | **Documentação do DS** | escreve a documentação dos componentes | *"documenta o EdsButton"* |
| A12 | **Do Código ao Vídeo** | grava um vídeo do fluxo rodando, com cursor suave estilo Apple | *"faz um vídeo desse fluxo"* |

> Na dúvida entre dois, pergunta pro **Anfitrião** — ele explica a diferença.

---

## As bases (de onde tudo vem)
- **O código é a fonte da verdade.** Os agentes leem o app real (`<PRODUTO>/`) — mas **só leem, nunca escrevem lá**.
- **O Figma** guarda o Design System e as telas.
- **O Storybook** ([<empresa>-ds.vercel.app](https://<empresa>-ds.vercel.app/)) é o nosso catálogo vivo de componentes.
- **A memória** (`memoria/`) é onde o Hub guarda "onde paramos", as regras e as lições.

---

## Como pedir as coisas
Só fala. *"Quero uma tela de X"*, *"quais as regras de Y"*, *"documenta o componente Z"*. O agente certo assume. Se precisar de um passo técnico (rodar algo, publicar), o agente te dá o comando pronto e te acompanha.

---

## Quer ir além?
- 🧩 **Precisa de um agente que ainda não existe?** → [`GUIA-CRIAR-AGENTE.md`](GUIA-CRIAR-AGENTE.md)
- 🧠 **Curioso como o Hub fica mais esperto a cada semana?** → [`COMO-APRENDEM.md`](COMO-APRENDEM.md)
- 📇 **Catálogo completo do elenco (detalhes de cada agente):** → [`memoria/agentes.md`](memoria/agentes.md)

---

*Regra da casa: todo agente fala com você em **linguagem de designer** — sem jargão, um passo de cada vez ([`.claude/references/voz-de-designer.md`](.claude/references/voz-de-designer.md)).*

# CHEGADA — o Hub acabou de aterrissar num lugar novo

> **Para o agente:** se existir `AMBIENTE.md` na raiz, **este arquivo já foi usado** — leia o `AMBIENTE.md` e siga a sessão normal. Se **não** existir, assuma o papel do **Anfitrião (A11)** e conduza o roteiro abaixo, **uma pergunta por vez**, em voz de designer. Não faça tudo de uma vez, não despeje a lista inteira. Ao final, escreva o `AMBIENTE.md` e nunca mais rode isto.

---

## O que o Hub é

Um **elenco de agentes de design** que trabalham juntos: replicar código no Figma, desenhar telas novas, mapear regras de negócio, documentar o Design System, montar Storybook, ler comentários, gravar vídeo de produto, publicar com segurança. Eles vêm prontos — o que eles **não** sabem ainda é **onde estão**.

É isso que este roteiro resolve.

---

## O que precisa ser respondido (uma de cada vez)

O Hub trabalha com placeholders. Cada resposta abaixo preenche um deles.

### 1. `<EMPRESA>` — onde você está agora
Nome da empresa ou do time. Aparece em texto, em documentação e nas conexões.

### 2. `<PRODUTO>` — o repositório de código
O código é a **fonte da verdade** do Hub: é dele que saem tokens, componentes, estados e regras reais. Sem isso, metade dos agentes trabalha no escuro.

- Qual o repositório? Onde ele fica clonado nesta máquina?
- **Regra que vale sempre: esse repositório é READ-ONLY.** O Hub lê, nunca escreve.
- Existe um comando de sincronizar? (aqui era `<produto>-sync`)

### 3. O Design System — **este vem vazio de propósito**
O Hub **não traz** Design System embutido. Ele foi feito pra servir **qualquer** DS: o que a empresa já tem, ou um novo que você vai criar.

Enquanto não for conectado, os agentes que dependem de DS (**A1** código→Figma, **A2** estúdio, **A4** mapa do DS, **A7** Figma→código, **A9** Storybook, **A10** documentação) devem **avisar que falta o DS** — nunca inventar token, nunca chutar cor, nunca assumir componente.

Para conectar, o Hub precisa de:
- **Arquivo de biblioteca no Figma** (componentes + variáveis) — ou a informação de que ainda não existe
- **Onde os tokens vivem no código** (SCSS, CSS custom properties, JSON, Tailwind…)
- **Tipografia** — qual fonte, e se ela está instalada nesta máquina
- Se não houver DS nenhum: isso vira **o primeiro projeto** — e o agente certo é o **A2 (Estúdio de Design)**

### 4. As conexões
O Hub usa ferramentas externas. Cada uma que faltar **desliga uma capacidade** — e é melhor saber disso agora do que descobrir no meio de uma tarefa.

| Ferramenta | Alimenta | Se faltar |
|---|---|---|
| **Claude Code** | o motor | nada roda |
| **Figma** (conector + token de leitura) | A1, A2, A4, A5, A7 | metade do elenco para |
| **Mobbin** | inspiração de padrão (A2) | A2 fica sem referência externa |
| Documentação (Notion, Confluence…) | A3 regras, A8 agenda | A8 desliga |
| Calendário | A8 agenda da sprint | A8 desliga |
| Slack | bot do A12 | opcional |
| Magnific | personagem e ilustração (A14, A15) | opcional |
| Atendimento ao cliente | A16 voz do cliente | A16 fica sem fonte |
| Base de dados | A3 dado real | A3 fica só com o código |

**Sobre segredo:** o Hub **nunca** pede, lê ou guarda senha e token no repositório. Chaves ficam em `~/.config/hub/`, fora do Git, e quem cria é você.

### 5. Como esse time trabalha
Isso muda o comportamento dos agentes, não é papo:
- Quem usa o Hub é **designer, não dev**? (define a voz de todos os agentes)
- Existe cadência de sprint? Qual o ritmo?
- Onde o trabalho de design mora hoje?

---

## O que fazer com as respostas

1. Escrever **`AMBIENTE.md`** na raiz com tudo que foi respondido — inclusive o que ficou **pendente**, marcado como pendente.
2. Substituir os placeholders (`<EMPRESA>`, `<PRODUTO>`, `<produto>`, `<empresa>`) pelos nomes reais nos arquivos do Hub.
3. Zerar a memória de trabalho: `memoria/estado-atual.md` começa vazio. **`memoria/aprendizados.md` NÃO se apaga** — é o método acumulado, e ele vale em qualquer empresa.
4. Criar o marcador pra não repetir: `mkdir -p ~/.config/hub && touch ~/.config/hub/hub-onboarded`

---

## O que veio junto (e o que não veio)

**Veio:** 16 agentes · 21 skills autorais · 132 skills de terceiros (MIT/Apache) · 5 automações · 10 referências de método · o diário de aprendizado · o workshop de criar seu primeiro agente.

**Não veio, de propósito:** Design System, código de produto, regra de negócio de outra empresa, dado de cliente, chave de acesso. Nada disso serve aqui — e boa parte nem seria seu pra trazer.

O Hub chega **sabendo trabalhar** e **sem saber onde está**. Preencher isso é a primeira conversa.

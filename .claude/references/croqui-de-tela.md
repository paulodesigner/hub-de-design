# Croqui de Tela — rascunho ASCII antes de qualquer mudança grande

> **Croqui** (termo de arquitetura/design: esboço rápido, à mão, pra validar a ideia antes do
> desenho final). Aqui: um desenho em caracteres (caixas `┌─┐│└─┘`, pontilhado `⠋⠋⠋`/`···`) que
> mostra a estrutura/disposição de uma tela ou componente **direto no chat**, antes de qualquer
> código, Figma ou implementação. Economiza a volta "construí → não era isso → refaz".

## Por que existe

Nasceu numa sessão de redesign do Painel de Eficiência (2026-07-24/25): antes de reorganizar
containers (ex.: separar uma tabela do card de resumo, com estado recolhido/expandido), o
rascunho ASCII das duas disposições foi mostrado no chat. O usuário confirmou "adorei" e pediu
pra isso virar prática padrão — descreveu como algo que "economiza muito tempo de desenhar uma
tela, fazer um código, desenhar no Figma, e fazer a gente entender um conceito antes de aprovar".

## Quando usar (regra dura)

1. **Sempre que o usuário pedir um plano/rascunho** ("como você faria isso", "quero ver antes",
   "me dá um rascunho") — o Croqui é a resposta, não texto corrido descrevendo a tela.
2. **Proativamente, antes de qualquer mudança estrutural grande em UI/componente** — reorganizar
   containers, criar um novo padrão de interação (expandir/recolher, novo tipo de card,
   navegação nova), dividir/fundir seções, redesenhar um layout — **mesmo sem o usuário pedir**.
   "Antes de fazer qualquer mudança [grande], trazer esse desenho pra validar" é a diretriz.
3. **Não precisa** quando a mudança já foi pedida de forma 100% explícita e mecânica (ex.: "remova
   este bloco", "troque esse texto") **ou** quando o usuário mandou executar direto ("pode
   aplicar", "faz direto", "executa") — nesses casos, só execute; forçar um croqui vira fricção.
4. Quando em dúvida entre os dois (mudança média, não claramente pequena nem claramente grande):
   **erre para o lado de mostrar o Croqui** — o custo de mostrar é baixo, o custo de construir
   errado é alto.

## Como montar um Croqui

- **Caixas de desenho de linha** (`┌ ─ ┐ │ └ ┘ ├ ┤`) pra containers/cards; pontilhado (`⠋⠋⠋` ou
  `···`) pra indicar conteúdo que rola/continua; setas (`←`) pra anotar uma peça específica do
  desenho sem poluir a caixa.
- **Mostre os ESTADOS relevantes** lado a lado ou em sequência — normalmente "antes/depois" ou
  "fechado/aberto" — não só uma foto estática. É isso que faz o usuário "ver" a interação, não só
  a estrutura.
- **Anotações curtas ao lado/abaixo de cada peça**, não um parágrafo — o desenho carrega o peso,
  o texto só aponta o que mudou e por quê.
- **Termine com as decisões em aberto**, numeradas e curtas (2-3 no máximo) — as únicas coisas que
  genuinamente precisam da palavra do usuário antes de construir (parâmetros que não foram ditos,
  ex. altura exata, se um comportamento vale pra outros casos também).
- **Sem código, sem Figma, sem construir nada** nesse momento — o Croqui é conversa, não entrega.

## Onde mora

Esta referência (`croqui-de-tela.md`) é citada em `CLAUDE.md` → Regras-chave. Vale para **todos os
agentes/tarefas do Hub** que envolvem UI (não é exclusivo do A2 `estudio-de-design` — vale pra
qualquer reorganização de tela, mesmo em Ops puro como o painel-eficiencia).

# 🧠 Como os agentes aprendem (e reaprendem)

Uma das coisas mais legais do Hub: ele **fica mais esperto a cada tarefa** — inclusive (e principalmente) com os **erros e as idas-e-vindas**. Isso não é mágica; é uma rotina simples que todo agente segue.

---

## O ciclo de 4 passos
Toda tarefa termina com um passo **obrigatório** de aprendizado:

1. **Destila** — o que aconteceu vira uma lição curta: *o que houve → a regra geral → como aplicar da próxima vez*.
2. **Registra** — a lição vai pro diário [`memoria/aprendizados.md`](memoria/aprendizados.md), com a etiqueta do agente (`[A2]`, `[A9]`…).
3. **Retroalimenta** — a lição vira **regra viva na skill do agente**. Assim, da próxima vez ele já nasce sabendo — não repete o erro.
4. **Atualiza** — registra "onde paramos" em [`memoria/estado-atual.md`](memoria/estado-atual.md); se virou regra durável, também em [`memoria/regras.md`](memoria/regras.md).

> Concluir uma tarefa **sem** registrar a lição (quando houve aprendizado) conta como tarefa **incompleta**.

---

## "Reaprender" — por que a casa não vira um depósito
- Se já existe uma lição **parecida**, o agente **edita** a existente em vez de criar uma duplicada.
- Se uma lição se provou **errada**, ela é **corrigida ou removida**.
- Resultado: a memória fica **enxuta e mais certeira** com o tempo — não um monte de anotações soltas.

---

## Por que isso importa
Muita coisa neste Hub foi descoberta no **vai-e-volta**: uma tentativa que não renderizou, um nome que confundia, um passo técnico que travava. Cada um desses virou uma regra que hoje **evita o mesmo tropeço**. É por isso que hoje um pedido sai mais redondo do que sairia há um mês.

Um exemplo real: aprendemos que **"deu build sem erro" não é o mesmo que "apareceu certo na tela"** — então agora os agentes sempre conferem o resultado de verdade antes de dizer que está pronto. Essa lição está lá no diário, com a etiqueta do agente que a aprendeu.

---

## Onde ver
- 📓 O diário completo de lições: [`memoria/aprendizados.md`](memoria/aprendizados.md)
- 📌 As regras duráveis: [`memoria/regras.md`](memoria/regras.md)
- 🧭 Onde cada agente guarda suas lições: dentro da própria skill (`.claude/skills/<agente>/SKILL.md`), numa seção de "Lições".

---

*Você não precisa fazer nada pra isso funcionar — é automático no fim de cada tarefa. Mas se você **corrigir** um agente, essa correção também vira lição. Você ensina a casa.*

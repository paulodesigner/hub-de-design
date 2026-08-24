# Fidelidade & verificação — como não desviar do código

Técnicas destiladas para a codigo-ao-figma ser a **mais fiel e eficiente** possível. (Origem: ideias
úteis de `addyosmani/agent-skills` — browser-testing, source-driven, doubt-driven, frontend-ui —
**não** adotado como dependência; só o que serve a *auditar um componente já codado* foi mantido.)

## 1. Ground-truth: leia o ESTILO COMPUTADO, não só o SCSS
O SCSS tem cascata, herança, `currentColor`, overrides e `var()` que podem resolver diferente do que
parece na leitura estática. **O DOM renderizado é a saída real do código.** Quando um valor for
ambíguo ou crítico (estado ativo, cor de ícone herdada, qual seletor vence), **renderize o componente
no app rodando e leia o valor resolvido** em vez de adivinhar pela cascata.

- App webclient roda em **localhost:8080** (`<PRODUTO>/webclient`). Navegue até a tela do componente.
- Leia o valor real: `getComputedStyle(el).getPropertyValue('color' | 'background-color' | 'border-...' | 'font-size' ...)`. Resolve `var()` e a cascata para o valor final (rgb/px).
- Capture os **estados reais**: force `:hover`/`:active`/`.active` (DevTools → "Toggle element state" ou inspecionando o item na rota ativa) e releia os computados.
- Se houver Chrome DevTools MCP disponível, use-o; senão, peça/abra o app e inspecione. **Isto resolve exatamente o tipo de divergência código↔produção que já nos pegou** (ex.: cor do ícone do sub-item, qual sub-elemento recebe o accent no estado ativo).
- Regra: **render computado > leitura de SCSS > suposição.** Nunca pare na suposição.

## 2. Proveniência: todo valor rastreia à fonte
Inspirado em "cite your sources". Cada valor da spec carrega **de onde veio** — torna a auditoria
verificável e expõe adivinhação.

- Anote, por valor: `arquivo:linha` (SCSS/SFC) **ou** nome do token (`--ath-...`) **ou** `getComputedStyle` (com a rota onde mediu).
- Se NÃO achou a origem de algo, marque **`NÃO-VERIFICADO`** explicitamente e **pergunte** — não preencha com um palpite "provável". Honestidade sobre o que não dá pra verificar vale mais que falsa confiança.
- No relatório final, divergências código↔render entram como **achado** (não correção silenciosa).

## 3. Racionalizações proibidas (as desculpas que levam à infidelidade)
| Racionalização | Realidade |
|---|---|
| "Tá perto o suficiente" | Réplica é auditoria — perto = errado. Pegue o valor exato (computado). |
| "Hover provavelmente é só opacity" | Confirme no CSS/computado. Suposição de estado é a fonte nº1 de erro. |
| "Reaproveito os estados/modelo do outro componente" | Anti-corruption: cada componente traduz o SEU código. Modelo emprestado corrompe (foi a raiz das falhas de contraste). |
| "A cor do ícone deve ser escura (parece no print)" | O print pode enganar; meça o computado. Se código diz claro e render diz escuro, **reporte a divergência**, não escolha por estética. |
| "Esse estado deveria existir" | Só existe o que o CSS define. Não invente (focus/pressed/disabled). |
| "Depois eu vinculo o token" | Vincule já (Value Object). Hex carimbado vira cópia órfã. |

## 4. Red flags (pare e corrija se aparecer)
- Hex hardcoded onde existe token semântico.
- Valor (cor/spacing/estado) que **não rastreia** a código/token/computado.
- Estado/variante que o CSS não tem.
- Cor de um sub-elemento reaproveitada para outro sem conferir o seletor (`.active > a` ≠ `.active span template`).
- "Pronto" declarado **sem** screenshot + cross-check de produção + contraste.

## 5. Passe de dúvida antes de fechar (adversarial, rápido)
Inspirado em doubt-driven. Antes de declarar concluído, para cada valor **não óbvio** tente
**refutá-lo**: "que evidência no código/computado prova isso?". Se não tem prova → vira `NÃO-VERIFICADO`
e mede/pergunta. Loop curto (1 passada), não recursão. Complementa o cross-check contra produção.

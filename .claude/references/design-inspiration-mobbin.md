# Inspiração externa — Mobbin (MCP)

**O que é:** [Mobbin](https://mobbin.com) é uma biblioteca de referências de UI de apps reais (fluxos, telas, padrões). Conectado via **MCP** (`mobbin`, user scope → disponível em **todos os projetos**). Serve como **canal de inspiração e best practices** ao **propor design** (Agente 2 `estudio-de-design`), e como referência de padrões ao auditar/analisar.

## Quando usar
- Ao **criar/melhorar/propor** uma tela, fluxo, empty state, onboarding, tabela densa, filtro, navegação, etc. — buscar como apps de referência resolvem o mesmo problema (padrões consolidados > inventar do zero).
- Na **análise heurística / competitiva** — comparar a solução com o estado da arte.
- Para **UX copy / microcopy** — ver convenções reais.

## Como usar (fluxo)
1. Traduza o problema em um **padrão** ("empty state de lista", "wizard multi-step", "detalhe financeiro com breakdown", "busca com command panel").
2. Consulte o Mobbin (via as tools MCP `mobbin`) por esse padrão / por apps do domínio (fintech, dashboards, B2B SaaS, apps BR).
3. **Destile o princípio**, não o pixel: o que torna aquele padrão bom (hierarquia, progressive disclosure, feedback, redução de carga cognitiva) — cite a referência.
4. **Traduza para o DS do <PRODUTO>** (tokens/componentes reais) e **rotule como proposta** (regras do A2).

## Ilustração e animação — o que o Mobbin dá, e o que não dá (2026-08-04)
Testado direto nas 3 tools reais (`search_screens`, `search_flows`, `search_sections`): todas devolvem só **imagem estática** (webp/jpg) + metadados (`id`, `app_name`, `platform`, `mobbin_url`; no flow, uma lista de frames com `position`). **Não existe** campo de duração, easing, curva ou vídeo em nenhuma resposta — um flow de onboarding com "transições animadas" na busca volta N imagens numeradas, nunca um clipe.

- **Ilustração — dá pra usar direto como referência de estilo.** `search_screens`/`search_sections` acham telas reais com ilustração em contexto (empty state, onboarding, upsell, cancelamento) — sirva de referência pro **prompt de geração por IA**: composição, paleta emocional, nível de detalhe, metáfora visual que o app de referência usou pra aquele problema. Carregue a skill `illustration-style` pra formalizar num guia. Guardrail de sempre vale: extrair o **princípio** ("ilustração line-art solta pra aliviar uma tela de erro"), nunca copiar o traço/personagem de terceiro.
- **Animação — só a ORDEM (storyboard), nunca o movimento (motion spec).** Os frames de um `flow` vêm numerados em sequência — isso mostra **o que muda entre um passo e o outro** (o que entra, o que sai, o que persiste), útil pra decidir a **coreografia** de uma animação nova (o quê anima, em que ordem, o que fica fixo). Não dá duração/easing/curva — isso continua vindo 100% do **GSAP** (skills `gsap-core`/`gsap-timeline`/`gsap-scrolltrigger`/`gsap-plugins`), única fonte de implementação de movimento do Hub hoje. Trate o Mobbin como **storyboard de entrada** pro GSAP, nunca como fonte alternativa de motion spec — e não desenhe curva de animação no Figma como se fosse a implementação real.
- **Na prática:** ao propor uma tela/fluxo com ilustração ou animação nova, inclua isso na query da pesquisa (ex.: "onboarding com transição de ilustração entre steps") — o resultado ainda serão frames estáticos, mas a leitura da sequência já é a referência de coreografia. Ilustração final e implementação de movimento continuam sendo trabalho nosso (IA generativa + GSAP), nunca importadas do Mobbin.

## Gate de pergunta + nota de proveniência (OBRIGATÓRIO ao propor telas/variantes)
Quando o pedido é **desenhar telas ou variantes de uma solução**, o Agente 2:
1. **PERGUNTA ANTES de desenhar:** "Quer que eu pesquise referência de padrão no **Mobbin** pra ancorar as propostas?" — junte essa pergunta com a confirmação de direção/fidelidade que já é obrigatória (Lição 9 do A2, via AskUserQuestion). **Não pesquise nem desenhe sem essa resposta.**
2. **Se SIM → toda proposta desenhada vem com um BLOCO DE NOTA de proveniência NO FIGMA**, ao lado da tela, claramente separado (é **meta** — anotação sobre a proposta, não parte da UI proposta; use o chrome editorial em tokens EDS, não misture com o specimen). O resultado da pesquisa pode ser resumido no **chat antes** de desenhar, mas o **bloco no Figma é obrigatório** (não opcional). Um bloco **por proposta/variante** (cada uma pode ter referência diferente). Conteúdo — **bem comunicativo, escaneável**:
   - 📎 **Referência** — app/empresa (ex.: Deel, Bonsai, ClickUp, HoneyBook) + a tela/padrão específico.
   - 🔗 **Link Mobbin** — a **URL da tela oficial no Mobbin quando o resultado da busca a fornecer** (como texto copiável, pra o usuário abrir/colar do lado); se o MCP não devolver URL, ponha `app + nome da tela` pra localizar.
   - 💡 **Por que essa referência** — o problema que ela resolve bem, em 1-2 linhas.
   - ✅ **Melhores práticas que ela traz** — 2-4 bullets com os **princípios de design** que essa referência trouxe **para esta proposta** (hierarquia, progressive disclosure, feedback, redução de carga cognitiva, agrupamento, etc.). Concreto: ligue o princípio ao que aparece na tela desenhada.
   - 🏷️ Rótulo: **inspiração — princípio, não pixel** (coerente com os guardrails abaixo).
3. **Se NÃO →** desenhe com heurística + DS, sem o bloco. **Nunca invente uma referência** que não pesquisou só pra preencher a nota.

## Guardrails (inegociáveis)
- **Mobbin = inspiração, NÃO fonte da verdade.** A verdade continua sendo: **código** (regra 2), **DS** (reuse-first, tokens do `ds-contract/`), **regras de negócio** (código + doc oficial, regra 8).
- **Nunca copiar pixel, layout proprietário ou marca** de outro app. Extrair o **padrão/princípio**, reimplementar no nosso DS.
- **Não importar tokens, cores ou tipografia** de referências — só padrões de UX/estrutura.
- Toda ideia trazida do Mobbin entra como **PROPOSTA rotulada**, separada do as-is, e ancorada no código (implementável) + DS.
- Se o Mobbin estiver indisponível (sem auth/off), **não trava** o trabalho — seguir com heurística + DS; anotar que faltou a referência externa.

## Setup (por máquina — NÃO viaja pelo Git do Hub)
> O Mobbin é **user scope** (`~/.claude.json`): cada pessoa liga na **própria máquina**. Clonar o Hub **não** traz o Mobbin — só a capacidade que o usa. Se um colega "não consegue pesquisar no Mobbin", quase sempre é isto: nunca ligou na máquina dele.
1. **Instalar o server** (uma vez): `scripts/ligar-mobbin.sh` (adiciona `mobbin` ao `~/.claude.json` de forma idempotente, com backup). Alternativa manual: `claude mcp add --scope user --transport http mobbin https://api.mobbin.com/mcp` (se o `claude` CLI estiver no PATH), ou editar `~/.claude.json` → top-level `mcpServers` → `mobbin` `{ "type": "http", "url": "https://api.mobbin.com/mcp" }`.
2. **Reiniciar o Claude Code** (MCP carrega no start).
3. **Autenticar** via `/mcp` (login no serviço). Depois, as tools `mobbin*` aparecem via ToolSearch **no loop principal**.
- ⚠️ **Subagente (A2 spawnado) só enxerga MCP que estiver no `tools:` da def.** Por isso `mcp__mobbin__search_screens/flows/sections` estão listadas na def do A2 (`.claude/agents/estudio-de-design.md`) — sem isso, o Mobbin funciona no chat mas **some** quando o A2 roda spawnado. No loop principal (skill) a herança é automática.
- Se off/sem auth em qualquer camada → **não trava** o trabalho (guardrail acima): segue com heurística + DS e anota a falta.

# Template — Tela de Login (padrão do Hub)

Template **plug-and-play** de autenticação por senha única, com tela própria (não o popup nativo do navegador). Primeira versão do que vai virar a nossa pasta `templates/` — drag-and-drop de peças prontas (design + código) pra reaplicar em qualquer projeto novo do Hub, sem refazer do zero.

**Referência viva (implementado de verdade):** `../../../rulebook/src/worker.js` — se quiser ver funcionando antes de portar pra outro projeto, é lá.

## O que isso resolve

Antes, os projetos protegidos por senha (Rulebook, e outros) usavam **HTTP Basic Auth**: o navegador mostra a própria caixinha nativa de usuário/senha. Funciona, mas:
- **Não dá pra desenhar nada.** É o Chrome/Safari/Firefox renderizando a UI deles — sem logo, sem cores do DS, sem copy além de uma linha (`realm`).
- Cada projeto que já tinha algo diferente ficou com uma "cara" de login distinta, sem padrão.

Esse template troca isso por uma **página HTML nossa**, com o mesmo nível de segurança (uma senha só, compartilhada pelo time, guardada como secret no Cloudflare, nunca no código) — só que agora a tela é nossa pra desenhar.

## Como funciona (arquitetura)

1. Todo request chega no Worker (`run_worker_first: true` no `wrangler.jsonc`).
2. O Worker olha se existe um **cookie de sessão** válido (`hub_session`), assinado com HMAC-SHA256 usando a própria senha do site como chave (Web Crypto nativo do Worker — sem lib externa).
3. **Sem cookie válido** → devolve a página de login (HTML próprio, embutido no arquivo, sem dependência externa).
4. A pessoa digita a senha → `POST /__login` → o Worker confere contra o secret `SITE_PASSWORD` (comparação em tempo constante, evita timing attack) → se bater, seta o cookie (`HttpOnly; Secure; SameSite=Lax`, válido por 30 dias) e redireciona pra `/`.
5. Se errar a senha, a mesma tela volta com um aviso discreto ("Senha incorreta. Tenta de novo.").
6. `GET /__logout` limpa o cookie — precisa de um link/botão em algum canto fixo da UI do projeto (passo 6 do "como aplicar" abaixo) pra ser de fato acessível, já que `/__logout` sozinho é só uma URL, ninguém acha ela sem saber que existe.

**Sem usuário** — no Basic Auth antigo o usuário já era fixo (`<empresa>`) e não distinguia ninguém; então esse template simplificou pra **só senha**, um campo a menos, mesma segurança real.

## Copy propositalmente neutra

A tela **nunca menciona o que tem atrás do login** — só "Hub de Design" (a marca) + "Acesso interno" (a ação). Isso é de propósito:
- **Segurança:** não expõe pra quem não tem a senha o que está protegido ali.
- **Padronização:** a MESMA tela, sem nenhuma edição, serve qualquer projeto do Hub — não tem "customização por projeto" pra fazer. É literalmente arrastar-e-soltar.

## Como aplicar num projeto novo (passo a passo)

Pré-requisito: o projeto já roda como **Cloudflare Worker** com assets estáticos (`wrangler.jsonc` com `"assets": {"directory": "./public/", "run_worker_first": true}` — mesmo padrão do Rulebook). Se o projeto ainda não tem isso, esse é o passo 0 (perguntar pro agente **Publicador Seguro** — `.claude/agents/publicador-seguro.md` — ele guia esse setup inicial).

1. **Copie o arquivo inteiro** `auth.js` deste template pra dentro do `src/` do projeto (ex.: `src/auth.js`).
2. No `src/worker.js` do projeto, no topo do arquivo:
   ```js
   import { authGate } from "./auth.js";
   ```
3. Na função `fetch(request, env)`, **logo no início**, antes de qualquer outra lógica:
   ```js
   export default {
     async fetch(request, env) {
       const gate = await authGate(request, env);
       if (gate) return gate; // não autenticado: já devolve a tela de login / redirect

       // ... resto da lógica normal do projeto (rotas, /api/*, env.ASSETS.fetch, etc.)
     }
   };
   ```
4. Configure a senha (mesma senha padrão do time, ou uma nova — decisão de quem está publicando):
   ```
   wrangler secret put SITE_PASSWORD
   ```
5. Se o projeto **já tinha** alguma autenticação (Basic Auth ou outra tela de login), **remova essa lógica antiga** — não empilhar dois mecanismos.
6. **Coloque um botão de "Sair" visível na UI do projeto, com confirmação antes de sair de verdade** (o `auth.js` já implementa a rota `/__logout`, mas ela não aparece sozinha em lugar nenhum — cada projeto tem sua própria topbar/shell, então isso não pode vir embutido no `auth.js`). No Rulebook virou um `icon-btn` na topbar (ao lado do toggle de tema) que abre um popup de confirmação — só depois de confirmar é que navega pra `/__logout`:
   ```html
   <!-- botão -->
   <button class="icon-btn logout-btn" id="logoutBtn" aria-label="Sair" title="Sair">
     <!-- ícone "sign-out" do Phosphor Regular — ainda NÃO está no swatch curado do
          Figma DS (~130 ícones); sugerir ao curador (Agente 4) adicionar por lá.
          Até isso acontecer, esse path veio direto do pacote público
          @phosphor-icons/core (mesma biblioteca-fonte declarada no Figma). -->
     <svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M120,216a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V40a8,8,0,0,1,8-8h64a8,8,0,0,1,0,16H56V208h56A8,8,0,0,1,120,216Zm109.66-93.66-40-40a8,8,0,0,0-11.32,11.32L204.69,120H112a8,8,0,0,0,0,16h92.69l-26.35,26.34a8,8,0,0,0,11.32,11.32l40-40A8,8,0,0,0,229.66,122.34Z"/></svg>
   </button>

   <!-- popup de confirmação (hidden por padrão; JS mostra/esconde) -->
   <div class="confirm-overlay" id="logoutOverlay" hidden>
     <div class="confirm-modal" role="alertdialog" aria-modal="true" aria-labelledby="logoutTitle" aria-describedby="logoutDesc">
       <h3 id="logoutTitle">Sair da plataforma?</h3>
       <p id="logoutDesc">Você vai precisar digitar a senha de novo pra entrar.</p>
       <div class="confirm-actions">
         <button type="button" class="btn-ghost" id="logoutCancel">Cancelar</button>
         <button type="button" class="btn-solid" id="logoutConfirm">Sair</button>
       </div>
     </div>
   </div>
   ```
   CSS (`.icon-btn`, `.confirm-overlay`, `.confirm-modal`, `.btn-ghost`, `.btn-solid`) e o JS de abrir/fechar (clique no botão abre; Cancelar/Esc/clique fora do card fecha; Confirmar navega pra `/__logout`) estão em `../../rulebook/public/assets/{styles.css,app.js}` — copie o padrão de lá. **Por que confirmar antes:** sair é rápido de desfazer (só digitar a senha de novo), mas ainda assim um clique sem querer no ícone errado da topbar não deveria derrubar a sessão na hora — o popup é a rede de segurança.
   **Nota de tamanho:** ícone preenchido (sólido) ao lado de um ícone de contorno fino (o toggle de tema, `stroke-width:1.8`) no MESMO tamanho numérico parece maior/mais pesado visualmente — reduza uns 2px o ícone preenchido pra equilibrar (`16px` vs `18px` no Rulebook).
7. Deploy (`npx wrangler deploy`) e testa: acessar o site deve mostrar a tela nova; senha certa entra; senha errada mostra o aviso; clicar em "Sair" abre a confirmação; confirmar desloga de verdade; cancelar/Esc/clique fora fecha sem sair.

Não precisa mexer em nada de design — o `auth.js` já embute a fonte (Satoshi, Bold + Regular, em base64) e o logo (SVG inline da <EMPRESA>), então funciona sozinho, sem depender da pasta `assets/` do projeto-alvo.

## Segurança (o que já está coberto)

- Senha nunca fica no código nem no repo — só como `wrangler secret`.
- Comparação da senha em **tempo constante** (`safeEqual`), evita side-channel por tempo de resposta.
- Cookie `HttpOnly` (JS do site não lê/rouba o cookie via XSS) + `Secure` (só trafega em HTTPS) + `SameSite=Lax` (mitiga CSRF básico).
- Cookie não guarda a senha — só um timestamp de expiração + assinatura HMAC. Ninguém forja um cookie válido sem saber a senha (a chave HMAC é a própria senha).
- Sessão expira em 30 dias (`SESSION_MAX_AGE` no topo do `auth.js` — ajuste ali se quiser outro prazo).
- **Limite honesto do "Sair":** ele limpa o cookie NO NAVEGADOR de quem clicou, mas não existe uma lista de sessões revogadas no servidor (é um token assinado sem estado — mais simples, sem precisar de banco). Ou seja, uma cópia do cookie que já tivesse vazado antes do logout continuaria válida até expirar sozinha. Pra um caso extremo (ex.: suspeita de vazamento), o jeito de invalidar **todas** as sessões de uma vez é trocar a senha (`wrangler secret put SITE_PASSWORD`) — como a assinatura usa a própria senha como chave, todo cookie antigo vira inválido na hora.

## Coisas que NÃO são deste template (fora do escopo)

- Não distingue usuários (é senha única de time — se precisar de contas individuais, isso é outro projeto/arquitetura, tipo SSO `@<empresa>.com.br` — ver "Etapa 2" do Publicador Seguro).
- Não tem "esqueci minha senha" (é o mesmo modelo do Basic Auth antigo: quem esquece, pergunta pro time).
- Não tem rate-limit de tentativas (razoável pra uso interno do time; se importar, dá pra somar depois via Cloudflare Rate Limiting, sem mexer neste arquivo).

## Arquivos deste template

- **`auth.js`** — o código-fonte de verdade. Copie inteiro pro projeto novo (ver passo a passo acima).
- **`preview.html`** — cópia standalone só pra ABRIR NO NAVEGADOR e conferir o design rapidinho (ex.: `open preview.html`), sem precisar rodar um Worker. **Não é o que roda em produção** — é só uma prévia visual; o `auth.js` é que importa.

## Changelog

- **2026-07-24** — v1, criado a partir da migração do Rulebook (Basic Auth → tela própria). Primeiro item da pasta `templates/`.

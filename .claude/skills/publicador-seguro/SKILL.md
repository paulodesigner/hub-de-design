---
name: publicador-seguro
description: "Agente 13 — Publicador Seguro. Use quando o usuário quer PUBLICAR ONLINE com segurança um material já pronto (página HTML, artefato, site estático local): 'publica esse artefato com segurança', 'coloca isso no ar só pro time/cliente', 'compartilha esse HTML protegido por senha', 'como publico isso online de forma segura'. Etapa 1 (padrão): protegido por SENHA (Basic Auth via Cloudflare Worker, sem cartão). Etapa 2 (via TI): domínio próprio + login @<empresa>.com.br. Segurança é a 1ª premissa. Não cria o conteúdo; login/deploy são do usuário (guia baby steps, nunca vê segredo)."
---

# Publicador Seguro — playbook (Agente 13)

Skill do loop principal pra **publicar com segurança** um material já pronto. Doutrina completa (segurança, fronteiras, 2 etapas) em `.claude/agents/publicador-seguro.md` — leia. Aqui está **como conduzir**.

## Antes de tudo — a voz e a segurança
- Voz: `.claude/references/voz-de-designer.md`. Designer/PM, baby steps, um passo por vez, um print a cada passo.
- **Segurança primeiro (Regra 0):** confirme **sensibilidade** e **público-alvo** ANTES de qualquer deploy. Todo deploy nasce **público** até a trava — não divulgue a URL antes; apague deploys intermediários. Você **nunca** vê/pede senha; login/deploy/secret são do usuário.

## Passo 0 — Checklist de segurança (obrigatório, antes de publicar)
Pergunte e confirme com o usuário:
1. **O conteúdo é sensível?** (assuma que sim até ele negar)
2. **Quem pode ver?** só time / um cliente / público
3. Se sensível e público-alvo restrito → **Etapa 1 (senha)** no mínimo. Nunca publique sensível aberto.

## Etapa 1 — publicar protegido por SENHA (Cloudflare Worker + Basic Auth, sem cartão)

### 1. Preparar o pacote (você faz, local)
Estruture o material no modelo Worker + assets:
```
projeto/
  public/            ← todos os arquivos do site (index.html, assets/, data/…)
  src/worker.js      ← a "portaria" (Basic Auth)
  wrangler.jsonc     ← config
```
- Mova o conteúdo pra `public/`. Confira caminhos relativos.
- Versione (git init + commit) — bom pra histórico e pra Etapa 2 (CI futuro).
- Confirme que há **Node** (`command -v node`); o deploy usa `npx wrangler` (não precisa instalar global).

**`src/worker.js`** (usuário fixo + senha em secret; `run_worker_first` garante a trava em TODAS as rotas):
```js
const USERNAME = "<empresa>";
const REALM = "Conteúdo protegido — <EMPRESA>";
export default {
  async fetch(request, env) {
    const expected = env.SITE_PASSWORD;
    if (!expected) return new Response("Portaria sem senha. Rode: wrangler secret put SITE_PASSWORD", { status: 503 });
    const h = request.headers.get("Authorization") || "";
    if (h.startsWith("Basic ")) {
      const d = atob(h.slice(6).trim()); const i = d.indexOf(":");
      const user = i < 0 ? "" : d.slice(0, i), pass = i < 0 ? "" : d.slice(i + 1);
      if (eq(user, USERNAME) && eq(pass, expected)) return env.ASSETS.fetch(request);
    }
    return new Response("Autenticação necessária.", { status: 401,
      headers: { "WWW-Authenticate": `Basic realm="${REALM}", charset="UTF-8"`, "Cache-Control": "no-store" } });
  }
};
function eq(a, b){ a=String(a); b=String(b); if(a.length!==b.length) return false; let d=0; for(let i=0;i<a.length;i++) d|=a.charCodeAt(i)^b.charCodeAt(i); return d===0; }
```
**`wrangler.jsonc`** (⚠️ `run_worker_first:true` é CRÍTICO — sem ele os assets servem antes do auth e o conteúdo VAZA):
```jsonc
{ "name": "meu-projeto", "main": "src/worker.js", "compatibility_date": "2026-07-21",
  "assets": { "directory": "./public/", "binding": "ASSETS", "run_worker_first": true } }
```

### 2. Deploy (o USUÁRIO roda, você guia comando a comando)
No Terminal, na pasta do projeto:
1. `npx wrangler login` → se perguntar "Ok to proceed? (y)", **y**; abre o navegador → **Allow**. (Se perguntar pra instalar "Cloudflare skills", **n**.)
2. `npx wrangler deploy` → publica; sai a URL `https://<nome>.<subdominio>.workers.dev`. Nasce **trancado sem senha** (503) — bom, não vaza.
3. `npx wrangler secret put SITE_PASSWORD` → digita uma **senha forte** (não aparece na tela) + Enter. Guarde a senha.

### 3. Testar e trancar de verdade
- Você confirma do seu lado com WebFetch **sem credenciais** → deve dar **401** (barrado). Se der 503, o secret ainda está **propagando** (segundos) — teste de novo com `?cb=1` pra furar cache.
- Peça pro usuário abrir em **aba anônima** e entrar com **usuário `<empresa>`** + a senha.
- **Faxina:** apague deploys públicos intermediários: `npx wrangler delete --name <nome-antigo>`.

### Credenciais pro time (o que o usuário compartilha)
`URL` + `usuário: <empresa>` + `senha` (por canal seguro). Trocar a senha = rodar `secret put` de novo.

## Becos do dashboard Cloudflare (previna — o usuário tropeça aqui)
- **"Domains" do menu lateral = comprar domínio** (beco!). O que importa são as **abas do projeto** e o Terminal. Não mande o usuário por aí.
- **"Upload assets" pelo dashboard cria um Worker** (não "Pages") e some se sair antes de finalizar. Por isso o caminho recomendado é o **wrangler** (determinístico), não o arrastar-pasta.
- **Zero Trust Access pede CARTÃO** no plano free → **não use** se o usuário recusa cartão. Basic Auth resolve sem cartão.
- **Código-por-e-mail (OTP)** só é seguro com política de domínio e ainda parece "auto-serviço" → evite pra este caso.

## Variante — o projeto já vive noutro hosting (ex.: Vercel) e não quer migrar
**Antes de propor migrar de hosting pra aplicar a senha, verifique se o `auth.js` do template exige mesmo o Cloudflare.** Ele só usa Web APIs padrão (`Request`/`Response`/`crypto.subtle`, e `env.SITE_PASSWORD` como único "gancho" externo) — roda igual em qualquer runtime Edge com essas primitivas. **Manter o hosting atual é a opção de menor atrito; pergunte migrar só se o hosting atual não suportar interceptar toda rota antes do estático.**

### Vercel Edge Middleware (equivalente ao Worker, sem sair do Vercel)
1. Copie `auth.js` inteiro pro projeto (ex.: `src/auth.js`) — igual ao Cloudflare.
2. Crie `middleware.js` **na raiz do projeto** (não dentro de `src/`, mesmo que o resto do código-fonte esteja lá — é onde o Vercel procura):
   ```js
   import { authGate } from "./src/auth.js";
   export const config = { matcher: "/(.*)" }; // intercepta TODA rota antes do estático
   export default async function middleware(request) {
     const gate = await authGate(request, { SITE_PASSWORD: process.env.SITE_PASSWORD });
     return gate || undefined; // undefined = segue o fluxo normal (serve o estático)
   }
   ```
3. **Diferença-chave do Cloudflare:** o segredo não é `env.X` de um binding — é **variável de ambiente do projeto Vercel** (`process.env.SITE_PASSWORD`), configurada no painel (Project Settings → Environment Variables) ou via `npx vercel env add SITE_PASSWORD production`. Não precisa de `wrangler.jsonc`/`run_worker_first`; o `matcher` no `config` já garante que roda antes de qualquer rota/rewrite.
4. Funciona **sem Next.js** — é um recurso de plataforma do Vercel (Edge Middleware), não amarrado a framework. Projeto "Other" (build estático via `outputDirectory`, como um Storybook) funciona igual.
5. Deploy é o normal do projeto (git push, se estiver plugado no GitHub) — não tem comando de `deploy` separado como o `wrangler deploy`.
6. **Teste local rápido sem subir nada:** `node --input-type=module -e "import {authGate} from './src/auth.js'; ..."` chamando `authGate(new Request(url), {SITE_PASSWORD:'teste'})` cobre os 3 caminhos (sem senha configurada → 503; sem cookie → tela de login; `/__logout` → redirect) antes de pedir pro usuário publicar.
7. Botão de "Sair" em projetos **Storybook**: não tem "topbar própria" pra colar o botão (é o chrome do Storybook) — use `.storybook/manager-head.html` (Storybook injeta esse HTML no `<head>` do MANAGER, não do preview/iframe) com um `<script>` vanilla que cria um botão fixo chamando `/__logout` com `window.confirm()` antes de navegar. Mais simples que o modal customizado do Rulebook, mesma segurança funcional.

### ⚠️ Confirme se há Git integration ANTES de dizer "vai publicar sozinho"
`git push` só publica no Vercel se o projeto tiver a **GitHub integration** ligada (deploy automático a cada push). Nunca assuma que tem — **cheque**:
- `npx vercel ls` → se os deploys existentes são de dias atrás e nenhum novo aparece minutos depois de um push real, **não tem** integração.
- `npx vercel inspect <url-do-deploy>` → sem metadado de commit/git, confirma que os deploys são manuais.

**Se não tiver integração** (ou se o projeto depender de algo que só resolve localmente, ex.: um symlink pra um repo read-only fora da pasta, que quebraria num build remoto), o deploy é **local build + prebuilt**, não um `vercel --prod` cru:
```
npx vercel pull --yes --environment production   # baixa config+env do projeto (cria .vercel/.env.production.local — NUNCA abra esse arquivo, é segredo em texto puro)
npx vercel build --prod                          # builda LOCAL (resolve symlinks locais) e já compila o middleware.js
npx vercel deploy --prebuilt --prod              # só sobe o pacote pronto, sem rebuildar remoto — ESTE é o "publicar" de verdade
```
Os 2 primeiros comandos são diagnóstico/preparo (não publicam nada — pode rodar você mesmo pra checar, ex. `find .vercel/output -iname "*middleware*"` confirma que a portaria foi reconhecida antes de publicar). Os 2 últimos linhas de comando acima já publicam — ação do usuário, mesmo padrão do `wrangler deploy`.

## Etapa 2 — domínio próprio + login corporativo (via TI, sem cartão)
Quando o usuário quiser sair da senha compartilhada pra **login individual `@<empresa>.com.br`**:
- Requer o **time de TI/infra**: apontar um subdomínio (ex.: `algo.<empresa>.com.br`) e/ou ligar o **provedor de identidade Google Workspace** no acesso.
- Seu papel: **preparar o pedido** (o que precisa, por quê) e **encaminhar** — não mexa em DNS/IdP por conta. Explique que é o passo que dá **identidade corporativa** e dispensa a senha.

## Variante inversa — remover a proteção (o usuário decidiu abrir o acesso)
Às vezes o pedido é o contrário: um material já protegido (senha/login) deve passar a abrir **direto**, porque deixou de ser sensível ou o público-alvo mudou. Antes de tirar a trava, **confirme a decisão explicitamente com o usuário** (é dele, nunca sua — ver Regra 0) e então:
1. **Remova o gate na origem** — apague/neutralize o `middleware.js` (Vercel) ou o Worker de auth (Cloudflare). Não basta esconder o link/botão de login: enquanto o gate existir, ele continua bloqueando quem não tem a senha.
2. **Varra o front por dependentes do login removido** — todo gate com tela própria costuma injetar estado que o front consome (cookie de "quem logou" pra nome/foto, botão "Sair"/"Log out", modal de confirmação de logout apontando pra uma rota `/logout` que só o gate resolvia). Sem o gate, essas peças ficam **mortas ou quebradas** (botão que leva a um 404) — remova-as na mesma tarefa, não deixe pra depois.
3. **Teste sem credencial** — confirme com `curl`/WebFetch sem cookie/senha que a rota principal responde 200 direto (sem redirect pra `/login`), local e em produção depois do deploy.
4. **Publique a mudança** — mesmo padrão de deploy da Etapa 1 (prebuilt se não houver Git integration). Isso também é uma ação em ambiente compartilhado: trate com o mesmo cuidado de qualquer deploy em produção.

## Aprende e cresce
Hoje você domina o caminho Cloudflare Worker + Basic Auth (e o inverso: removê-lo). Ao explorar novos (GitHub Pages, Pages clássico, interno), **primeiro descubra como cada um protege** e a janela de exposição — só então adote, e registre o novo caminho aqui.

## Loop de auto-aprendizado (obrigatório)
Concluiu/errou → lição em `memoria/aprendizados.md` tag **`[A13]`** → regra viva aqui + na def → atualize `estado-atual.md`. Marque a entrada `[✓ compactado]` quando virar regra.

# Começar aqui — instalar o Hub num computador novo

Este documento é só a **parte burocrática**: deixar a máquina pronta.
Depois que terminar, o Hub assume: ele lê o [`CHEGADA.md`](CHEGADA.md) e conduz a conversa de configuração — uma pergunta por vez.

---

## 1. Preparar a máquina (uma vez só)

Abra o **Terminal** (⌘+espaço → digite "Terminal") e cole uma linha de cada vez.

```bash
# Homebrew — o instalador de programas do Mac
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Ele pede a senha do seu Mac. **É normal.** A senha não aparece enquanto você digita — pode digitar no escuro e dar Enter.

```bash
brew install node git gh python3
```
- **node** — o motor que roda quase tudo
- **git** — controle de versão
- **gh** — conversa com o GitHub
- **python3** — usado pelas automações do Hub

## 2. Instalar o Claude Code

É o cérebro. Sem ele, o Hub é só um monte de arquivo de texto.

```bash
npm install -g @anthropic-ai/claude-code
claude
```
Na primeira vez ele conduz o login. Você precisa de uma conta com acesso ao Claude.

## 3. Entrar no GitHub

```bash
gh auth login
```
Escolha: **GitHub.com** → **HTTPS** → **Y** para autenticar o Git → **Login with a web browser**. Ele mostra um código, você cola no navegador.

## 4. Baixar o Hub

```bash
cd ~/Documents
git clone https://github.com/paulodesigner/hub-de-design.git
cd hub-de-design
```

## 5. Abrir e deixar o Hub se apresentar

```bash
claude
```

**É aqui que a parte burocrática termina.** O Hub percebe que está num lugar novo (não existe `AMBIENTE.md` ainda) e começa a te perguntar — qual é a empresa, qual o repositório de código, qual o Design System, o que já está conectado. Uma pergunta de cada vez.

Você não precisa saber todas as respostas de imediato. O que ficar pendente ele anota como pendente.

---

## As conexões (o Hub vai perguntar sobre elas)

Cada uma que faltar desliga uma capacidade. Nenhuma é obrigatória para começar.

| Ferramenta | Alimenta | Como conectar |
|---|---|---|
| **Figma** | metade dos agentes | conector oficial no claude.ai + token de leitura |
| **Mobbin** | inspiração de padrões | conector no claude.ai |
| Documentação (Notion etc.) | agenda e regras | conector no claude.ai |
| Calendário | agenda da sprint | conector no claude.ai |
| Slack · CRM · base de dados | outros agentes | conforme a empresa usar |

**Sobre chaves e senhas:** ficam em `~/.config/hub/`, fora do repositório. O Hub **nunca** pede, guarda ou mostra segredo. Quem cria é você.

---

## ⚠️ O Design System vem vazio de propósito

O Hub **não traz** Design System embutido — ele foi feito para servir **qualquer** DS: o que a empresa nova já tem, ou um que você vai criar.

Enquanto não estiver conectado, os agentes que dependem dele **avisam que falta o DS e param**, em vez de inventar cor ou componente. Isso é regra, não limitação: **DS chutado é pior que DS ausente.**

---

## Se der errado

| Sintoma | Solução |
|---|---|
| `command not found: brew` | feche e reabra o Terminal |
| `command not found: claude` | `npm install -g @anthropic-ai/claude-code` de novo |
| `command not found: npm` | o Node não instalou — repita `brew install node` |
| O Hub não faz as perguntas | apague o `AMBIENTE.md` (se existir) e abra de novo |

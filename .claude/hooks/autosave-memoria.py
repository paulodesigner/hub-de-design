#!/usr/bin/env python3
"""Auto-save cadenciado da memória do projeto (Stop hook do Claude Code).

A cada fim de turno do assistente, grava um snapshot LEGÍVEL da sessão em
  <workspace>/memoria/_autosave/sessao-<id>.md
Throttled: no máximo 1 gravação a cada THROTTLE_SECONDS, para não escrever a cada turno.
Objetivo: se o VS Code fechar sem salvar, o contexto recente continua recuperável.
Lê o JSON do hook por stdin (session_id, transcript_path, cwd).
"""
import sys, os, json, time, re

THROTTLE_SECONDS = 180          # mínimo entre snapshots
MAX_TURNS = 30                  # quantos turnos recentes manter no digest
TRUNC = 800                     # corte por mensagem

def load_stdin():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}

def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(p.get("text", ""))
        return " ".join(parts)
    return ""

def tools_of(content):
    names = []
    if isinstance(content, list):
        for p in content:
            if isinstance(p, dict) and p.get("type") == "tool_use":
                names.append(p.get("name", "?"))
    return names

def main():
    data = load_stdin()
    session_id = data.get("session_id") or "sessao"
    transcript = data.get("transcript_path")

    # Raiz ESTÁVEL do workspace. NUNCA usar o cwd transitório da sessão como base:
    # se um Stop dispara com cwd dentro de <PRODUTO>/, gravaríamos memoria/ DENTRO do
    # repo read-only (já aconteceu). Prefira CLAUDE_PROJECT_DIR; e se o caminho cair dentro
    # do clone, suba para o pai do repo.
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    if "/<PRODUTO>" in root:
        root = root.split("/<PRODUTO>")[0]
    autosave = os.path.join(root, "memoria", "_autosave")
    os.makedirs(autosave, exist_ok=True)

    # throttle
    marker = os.path.join(autosave, f".last-{session_id}")
    now = time.time()
    if os.path.exists(marker) and (now - os.path.getmtime(marker)) < THROTTLE_SECONDS:
        sys.exit(0)

    # localizar transcript se não veio no stdin
    if not transcript or not os.path.exists(transcript):
        sanitized = re.sub(r"[^A-Za-z0-9]", "-", cwd)
        guess = os.path.expanduser(f"~/.claude/projects/{sanitized}/{session_id}.jsonl")
        transcript = guess if os.path.exists(guess) else None
    if not transcript or not os.path.exists(transcript):
        sys.exit(0)  # nada a fazer (silencioso)

    entries = []
    n_user = n_assist = 0
    first_ts = last_ts = ""
    with open(transcript, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                o = json.loads(line)
            except Exception:
                continue
            t = o.get("type")
            if t not in ("user", "assistant"):
                continue
            msg = o.get("message", {})
            content = msg.get("content")
            txt = text_of(content).strip()
            tools = tools_of(content)
            ts = o.get("timestamp", "")
            if ts:
                first_ts = first_ts or ts
                last_ts = ts
            if t == "user":
                # pular ruído de tool_result puro / system reminders sem texto
                if not txt:
                    continue
                if txt.lstrip().startswith("<") and "system-reminder" in txt[:80]:
                    continue
                n_user += 1
                entries.append(("user", ts, txt, []))
            else:
                if not txt and not tools:
                    continue
                n_assist += 1
                entries.append(("assistant", ts, txt, tools))

    recent = entries[-MAX_TURNS:]
    saved_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))

    out = []
    out.append(f"# Autosave — sessão `{session_id}`")
    out.append(f"> Snapshot automático (a cada ~{THROTTLE_SECONDS//60} min). Última gravação: **{saved_at}**.")
    out.append(f"> NÃO editar à mão — é sobrescrito. Para retomar de verdade, leia "
               f"`memoria/LEIA-PRIMEIRO.md` + `estado-atual.md`; este arquivo é o bruto recente, à prova de fechar o VS Code sem salvar.")
    out.append("")
    out.append("## Resumo")
    out.append(f"- Mensagens na sessão: **{n_user}** do usuário · **{n_assist}** do assistente")
    if first_ts or last_ts:
        out.append(f"- Janela: {first_ts or '?'} → {last_ts or '?'}")
    out.append(f"- Transcript completo: `{transcript}`")
    out.append("")
    out.append(f"## Últimos {len(recent)} turnos")
    for role, ts, txt, tools in recent:
        who = "👤 Usuário" if role == "user" else "🤖 Claude"
        head = f"### {who}" + (f" · {ts}" if ts else "")
        out.append(head)
        body = txt.replace("\r", " ")
        if len(body) > TRUNC:
            body = body[:TRUNC] + " …[truncado]"
        if body:
            out.append(body)
        if tools:
            out.append(f"_(tools: {', '.join(tools)})_")
        out.append("")

    digest = "\n".join(out)
    dest = os.path.join(autosave, f"sessao-{session_id}.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(digest)
    # atualizar marcador de throttle
    with open(marker, "w") as f:
        f.write(saved_at)

    print(json.dumps({"suppressOutput": True}))
    sys.exit(0)

if __name__ == "__main__":
    main()

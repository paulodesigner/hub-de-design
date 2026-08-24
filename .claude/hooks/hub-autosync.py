#!/usr/bin/env python3
"""SessionStart hook — Hub autosync + anúncio do catálogo de agentes.

Duas coisas, ambas SEGURAS (nunca destrutivas, nunca bloqueiam a sessão):

1. Auto-pull do Hub  (git fetch + merge --ff-only origin/main):
   - só age se o repo for o Hub (remote 'design-system-code-to-figma');
   - só puxa se a árvore estiver LIMPA e o local estiver ATRÁS do remoto;
   - fast-forward only: nunca reescreve histórico, nunca resolve conflito,
     nunca toca em trabalho de projeto (que vive em outro repo);
   - se você tem commits locais não enviados (está À FRENTE) -> silêncio;
   - se divergiu ou está sujo -> só AVISA, não força;
   - throttle: no máximo 1x a cada 6h (carimbo em ~/.config/hub/).

2. Anúncio do catálogo: avisa sobre agentes NOVOS em agentes-catalogo/ que
   você ainda não viu — sem instalar nada. Anuncia, não impõe.

Qualquer erro -> silêncio, exit 0. Um hook nunca deve quebrar a sessão.
"""
import glob
import json
import os
import subprocess
import sys
import time

PROJECT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
PULL_STAMP = os.path.expanduser("~/.config/hub/hub-autosync-last")
SEEN_FILE = os.path.expanduser("~/.config/hub/agentes-catalogo-seen")
CATALOG_DIR = os.path.join(PROJECT, "agentes-catalogo")
THROTTLE_SECONDS = 6 * 3600
REMOTE_MARKER = "design-system-code-to-figma"


def git(args, timeout=15):
    return subprocess.run(["git", "-C", PROJECT] + args,
                          capture_output=True, text=True, timeout=timeout)


def is_hub():
    try:
        r = git(["remote", "get-url", "origin"], timeout=5)
        return REMOTE_MARKER in (r.stdout or "")
    except Exception:
        return False


def throttled():
    try:
        return (time.time() - os.path.getmtime(PULL_STAMP)) < THROTTLE_SECONDS
    except OSError:
        return False


def touch_stamp():
    try:
        os.makedirs(os.path.dirname(PULL_STAMP), exist_ok=True)
        with open(PULL_STAMP, "w") as f:
            f.write(str(int(time.time())))
    except OSError:
        pass


def autopull():
    """Retorna uma linha de aviso, ou None."""
    if throttled():
        return None
    touch_stamp()
    dirty = bool((git(["status", "--porcelain"], timeout=5).stdout or "").strip())
    if git(["fetch", "origin", "--quiet"], timeout=20).returncode != 0:
        return None  # offline / sem acesso -> silêncio
    local = git(["rev-parse", "@"]).stdout.strip()
    remote = git(["rev-parse", "origin/main"]).stdout.strip()
    base = git(["merge-base", "@", "origin/main"]).stdout.strip()
    if not remote or local == remote:
        return None  # já atualizado
    if local == base:  # ATRÁS do remoto
        if dirty:
            return ("🔄 O Hub tem atualização nova do time, mas você tem mudanças locais. "
                    "Commite (ou `git stash`) e rode `git pull --ff-only` pra receber.")
        if git(["merge", "--ff-only", "origin/main"], timeout=20).returncode == 0:
            n = git(["rev-list", "--count", "%s..%s" % (local, remote)]).stdout.strip() or "?"
            return "✅ Hub atualizado com o último do time (%s novidade[s])." % n
        return "⚠️ O Hub tem atualização, mas o pull automático não passou — rode `git pull` quando puder."
    if remote == base:
        return None  # À FRENTE (commits locais não enviados) -> normal, silêncio
    return ("⚠️ Seu Hub divergiu do time (mudou dos dois lados). Rode `git pull` com calma "
            "ou peça ajuda — nada foi alterado automaticamente.")


def announce_catalog():
    if not os.path.isdir(CATALOG_DIR):
        return None
    files = sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(CATALOG_DIR, "*.md"))
        if os.path.basename(p).lower() not in ("readme.md", "catalog.md")
    )
    if not files:
        return None
    try:
        seen = set(open(SEEN_FILE).read().split())
    except OSError:
        seen = set()
    new = [f for f in files if f not in seen]
    if not new:
        return None
    try:
        os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
        with open(SEEN_FILE, "w") as f:
            f.write("\n".join(files))
    except OSError:
        pass
    nomes = ", ".join(f[:-3] for f in new)  # tira .md
    return ("🆕 Novo(s) no catálogo de agentes: %s. São OPCIONAIS (não instalam sozinhos). "
            "Pra adotar, rode `scripts/adotar-agente.sh <nome>` ou peça pro Claude adotar. "
            "Detalhes em agentes-catalogo/CATALOG.md." % nomes)


def main():
    if not is_hub():
        return
    parts = []
    for fn in (autopull, announce_catalog):
        try:
            m = fn()
            if m:
                parts.append(m)
        except Exception:
            pass
    if parts:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": " ".join(parts),
        }}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

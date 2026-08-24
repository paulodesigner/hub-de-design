#!/usr/bin/env python3
"""
Vitrine de agentes do Hub (M24) — o "menu" navegável do time.

Mostra, em linguagem de designer:
  ✅ NÚCLEO    — os agentes que todo mundo já tem (herdados por Git)
  📢 CATÁLOGO  — agentes opcionais, com o comando pra adotar
  🔒 PESSOAIS  — os que você já adotou na sua máquina (~/.claude/agents/)

Para cada um: nome, o que faz (gatilho), modelo, e a ÚLTIMA mudança do seu
Changelog — "ver tudo que mudou" sem abrir 12 arquivos. É a peça que conecta
o changelog por agente (M24) ao fluxo de adoção (scripts/adotar-agente.sh).

READ-ONLY. Uso:  python3 scripts/agentes.py
Origem: melhorias.md M24.
"""
import os
import re
import glob


def raiz():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def ler_def(path):
    """Extrai {n, nome, gatilho, model, ultimo_changelog} de uma def .md."""
    t = open(path).read()
    fm = ""
    m = re.search(r"^---\n(.*?)\n---", t, re.S)
    if m:
        fm = m.group(1)
    slug = os.path.splitext(os.path.basename(path))[0]

    desc = ""
    dm = re.search(r'description:\s*"?(.*?)"?\s*(?:\n\w+:|\Z)', fm, re.S)
    if dm:
        desc = re.sub(r"\s+", " ", dm.group(1)).strip()

    model = ""
    mm = re.search(r"^model:\s*(.+)$", fm, re.M)
    if mm:
        model = mm.group(1).strip()

    # número do agente ("Agente 11 …", tolerando "(spawnável)" no meio)
    n = 999
    am = re.search(r"Agente\s+(\d+)", desc)
    if am:
        n = int(am.group(1))

    # gatilho curto: "Use para ..." → 1ª frase; senão 1ª frase da desc
    gatilho = ""
    gm = re.search(r"Use para ([^.]+)", desc)
    if gm:
        gatilho = gm.group(1)
    else:
        corpo = re.sub(r"^Agente\s+\d+[^—\-]*[—\-]\s*", "", desc)
        gatilho = corpo.split(".")[0]
    gatilho = gatilho.replace("'", "").replace('"', "").strip().rstrip(",")
    if len(gatilho) > 90:
        gatilho = gatilho[:87] + "…"

    ultimo = ""
    cm = re.search(r"## Changelog(.*)", t, re.S)
    if cm:
        linhas = [l.strip() for l in cm.group(1).splitlines() if l.strip().startswith("- ")]
        if linhas:
            ultimo = re.sub(r"^-\s*", "", linhas[-1])
            ultimo = ultimo.replace("**", "")
            if len(ultimo) > 80:
                ultimo = ultimo[:77] + "…"

    return {"n": n, "slug": slug, "gatilho": gatilho, "model": model, "ultimo": ultimo}


def bloco(defs):
    for d in sorted(defs, key=lambda x: (x["n"], x["slug"])):
        etiqueta = f"A{d['n']:>2}" if d["n"] != 999 else "  ·"
        mod = f" · {d['model']}" if d["model"] else ""
        print(f"  {etiqueta}  {d['slug']}{mod}")
        if d["gatilho"]:
            print(f"       {d['gatilho']}")
        if d["ultimo"]:
            print(f"       ↳ último: {d['ultimo']}")


def main():
    base = raiz()
    nucleo = [ler_def(p) for p in glob.glob(os.path.join(base, ".claude/agents/*.md"))]

    catdir = os.path.join(base, "agentes-catalogo")
    catalogo = []
    if os.path.isdir(catdir):
        for p in glob.glob(os.path.join(catdir, "*.md")):
            if os.path.basename(p) in ("CATALOG.md", "README.md"):
                continue
            catalogo.append(ler_def(p))

    pessoais = []
    pdir = os.path.expanduser("~/.claude/agents")
    if os.path.isdir(pdir):
        pessoais = [ler_def(p) for p in glob.glob(os.path.join(pdir, "*.md"))]

    print("🎛️  Vitrine de Agentes do Hub — o que existe, o que mudou, como levar pra sua máquina\n")

    print(f"✅ NÚCLEO ({len(nucleo)}) — todo mundo já tem (herdado por Git, atualiza sozinho no início da sessão)")
    bloco(nucleo)

    print(f"\n📢 CATÁLOGO ({len(catalogo)}) — opcionais; adote quando fizerem sentido pra você")
    if catalogo:
        bloco(catalogo)
        print("\n     Pra levar um pra sua máquina:  scripts/adotar-agente.sh <nome>")
    else:
        print("     (vazio por enquanto — quando alguém contribuir um agente ao catálogo, ele aparece aqui")
        print("      com o comando de adoção; contribuições sobem por PR)")

    print(f"\n🔒 SEUS PESSOAIS ({len(pessoais)}) — adotados só na sua máquina (~/.claude/agents/)")
    if pessoais:
        bloco(pessoais)
    else:
        print("     (nenhum ainda)")

    print("\n💡 Detalhe de cada mudança: `## Changelog` no fim da def do agente, ou o diário em memoria/aprendizados.md")


if __name__ == "__main__":
    main()

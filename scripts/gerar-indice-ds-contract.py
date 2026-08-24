#!/usr/bin/env python3
"""Gerador do índice leve de `ds-contract/components.contract.json` (M-médio, 2026-07-25).

`components.contract.json` tem ~9700 linhas / 560KB — ler o arquivo inteiro a
cada tarefa (A1/A4/A7/A9/A10 consultando "esse componente já tem contrato?")
é gasto de contexto evitável. Este script gera um índice pequeno
(`components.index.md`, uma linha por componente) com o número da linha onde
a entrada começa no JSON — quem for consultar só precisa: grep pelo id/nome
neste índice -> `Read` com `offset`/`limit` só nesse trecho do JSON.

READ-ONLY sobre o contrato: só lê `components.contract.json` e escreve o
índice. Rodar sempre que o contrato mudar (parte do refresh do Agente 4).

Uso:  python3 scripts/gerar-indice-ds-contract.py
"""
import json
import os
import sys


def raiz_projeto():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def main():
    base = os.path.join(raiz_projeto(), ".claude", "references", "ds-contract")
    caminho_contrato = os.path.join(base, "components.contract.json")
    caminho_indice = os.path.join(base, "components.index.md")

    if not os.path.exists(caminho_contrato):
        print(f"❌ não encontrei {caminho_contrato}")
        return 1

    with open(caminho_contrato) as fh:
        linhas = fh.readlines()
    dados = json.loads("".join(linhas))
    componentes = dados.get("components", [])

    # Acha a linha de cada entrada pelo padrão `"id": "<id>"` (uma por objeto).
    linha_do_id = {}
    for i, ln in enumerate(linhas, 1):
        s = ln.strip()
        if s.startswith('"id":'):
            valor = s.split(":", 1)[1].strip().strip(",").strip('"')
            linha_do_id.setdefault(valor, i)

    out = [
        "# Índice leve do `components.contract.json`",
        "",
        f"> Gerado por `scripts/gerar-indice-ds-contract.py` — {len(componentes)} componentes. "
        "**Não edite à mão** (regenere após qualquer mudança no contrato).",
        ">",
        "> **Como consultar sem ler o JSON inteiro:** ache a linha abaixo pelo `id`/nome, "
        "depois `Read` do `components.contract.json` com `offset` perto dessa linha e "
        "`limit` ~40 (cada entrada tem ~40-90 linhas). Só leia o arquivo inteiro se for "
        "regenerar o contrato inteiro.",
        "",
        "| id | code.name | tokenSystem | figma.status | linha no JSON |",
        "|---|---|---|---|---|",
    ]
    for c in componentes:
        cid = c.get("id", "")
        code = c.get("code", {}) or {}
        figma = c.get("figma", {}) or {}
        linha = linha_do_id.get(cid, "?")
        out.append(
            f"| `{cid}` | {code.get('name', '')} | {code.get('tokenSystem', '')} "
            f"| {figma.get('status', '')} | {linha} |"
        )

    with open(caminho_indice, "w") as fh:
        fh.write("\n".join(out) + "\n")

    print(f"✅ {caminho_indice} — {len(componentes)} entradas indexadas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

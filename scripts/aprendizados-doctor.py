#!/usr/bin/env python3
"""
Auditor do diário de aprendizados (M22) — mantém o log podável e coerente.

READ-ONLY: só lê e relata, nunca edita. Roda sob demanda ou no refresh semanal.
Verifica, para memoria/aprendizados.md:
  1. Tamanho (linhas/entradas) e quanto já está compactado → quando arquivar.
  2. Tags [A#]/[Ops] válidas no cabeçalho de cada entrada.
  3. "Retroalimentado em: <arquivo>" aponta para um arquivo que realmente existe.

Fecha o loop LSM/Kafka: o log só cresce; sem poda, toda sessão paga a leitura.
Origem: melhorias.md M22.

Uso:  python3 scripts/aprendizados-doctor.py [caminho-do-aprendizados.md]
"""
import os
import re
import sys

AGENTES_VALIDOS = {f"A{i}" for i in range(1, 13)} | {"Ops"}
LIMIAR_LINHAS = 450  # acima disso, sugerir arquivar as entradas já compactadas


def raiz_projeto():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def main(caminho):
    if not os.path.exists(caminho):
        print(f"❌ não encontrei {caminho}")
        return 1

    with open(caminho) as fh:
        linhas = fh.readlines()

    base = os.path.dirname(os.path.dirname(os.path.abspath(caminho)))  # raiz do repo (memoria/..)
    entradas = []  # (num_linha, titulo, corpo)
    atual = None
    for i, ln in enumerate(linhas, 1):
        if ln.startswith("### "):
            if atual:
                entradas.append(atual)
            atual = [i, ln.rstrip(), ""]
        elif atual:
            atual[2] += ln
    if atual:
        entradas.append(atual)

    total_linhas = len(linhas)
    compactadas = 0
    tags_ruins = []      # (linha, titulo, token)
    refs_quebradas = []  # (linha, caminho)

    for num, titulo, corpo in entradas:
        # 1. compactada?
        if "[✓ compactado" in corpo or "[✓ compactado" in titulo:
            compactadas += 1

        # 2. tags no cabeçalho
        tags = re.findall(r"\[([^\]]+)\]", titulo)
        for t in tags:
            for token in re.split(r"[/\s]+", t.strip()):
                token = token.strip()
                if not token:
                    continue
                if token in AGENTES_VALIDOS:
                    continue
                if token in ("A?", "meta", "decisão", "decisao", "test", "infra", "onboarding"):
                    continue  # marcadores livres tolerados
                if "|" in token:
                    continue  # linha de exemplo do bloco "Formato" (ex.: [A1|A2|A3])
                tags_ruins.append((num, titulo[:70], token))

        # 3. "Retroalimentado em/na skill ... `arquivo`"
        for m in re.finditer(r"[Rr]etroaliment\w+[^\n]*?`([^`]+)`", corpo):
            alvo = m.group(1).strip()
            # só validamos referências que parecem caminho de arquivo
            cand = alvo.split(" ")[0].split("→")[0].strip().strip("`")
            if ("/" in cand or cand.endswith(".md")) and not cand.startswith("http"):
                p = cand if os.path.isabs(cand) else os.path.join(base, cand)
                # skills costumam ser citadas pelo nome (ex.: `estudio-de-design`) sem caminho:
                if "/" in cand and not os.path.exists(p):
                    refs_quebradas.append((num, cand))

    print("📓 Auditor do diário de aprendizados")
    print(f"   arquivo: {caminho}")
    print(f"   {total_linhas} linhas · {len(entradas)} entradas · "
          f"{compactadas} compactadas ({len(entradas) - compactadas} pendentes)")

    if tags_ruins:
        print(f"\n⚠  {len(tags_ruins)} tag(s) fora do padrão [A1..A12]/[Ops]:")
        for num, tit, token in tags_ruins[:10]:
            print(f"   linha {num}: [{token}]  — {tit}")
    else:
        print("\n✅ tags dos cabeçalhos: todas no padrão")

    if refs_quebradas:
        print(f"\n⚠  {len(refs_quebradas)} 'Retroalimentado em' apontando p/ caminho inexistente:")
        for num, cam in refs_quebradas[:10]:
            print(f"   linha {num}: {cam}")
    else:
        print("✅ referências 'Retroalimentado em' (com caminho): todas existem")

    if total_linhas > LIMIAR_LINHAS and compactadas > 0:
        print(f"\n🧹 Diário passou de {LIMIAR_LINHAS} linhas com {compactadas} entradas já compactadas.")
        print("   Sugestão: arquivar as [✓ compactado] mais antigas em "
              "memoria/aprendizados-arquivo-AAAA-TX.md (mover, não apagar).")
    else:
        print(f"\n🟢 tamanho sob controle (limiar {LIMIAR_LINHAS} linhas).")

    return 0


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(raiz_projeto(), "memoria", "aprendizados.md")
    sys.exit(main(arg))

#!/usr/bin/env python3
"""SessionStart hook — Agente 8 (agenda).

Dispara UMA vez por sprint quinzenal, injetando contexto que instrui a rodar o
skill agenda. Regras:
  - Sprints de 2 semanas ancoradas em 2026-07-13 (segunda).
  - Só emite na JANELA seg/ter do início da sprint (offset 0 ou 1).
  - Carimbo (~/.config/hub/p2c-last-sprint) guarda a última sprint disparada,
    pra não repetir a cada abertura de sessão dentro da mesma quinzena.
Nunca quebra a sessão: qualquer erro -> silêncio, exit 0.
"""
import datetime
import json
import os
import sys

ANCHOR = datetime.date(2026, 7, 13)          # segunda, início de uma sprint de 2 semanas
STAMP = os.path.expanduser("~/.config/hub/p2c-last-sprint")
WINDOW_DAYS = 1                               # dispara só na seg (0) e ter (1) do início


def main():
    today = datetime.date.today()
    days = (today - ANCHOR).days
    if days < 0:
        return
    sprint_index = days // 14
    sprint_start = ANCHOR + datetime.timedelta(days=14 * sprint_index)
    offset = (today - sprint_start).days
    if offset > WINDOW_DAYS:
        return                                # fora da janela seg/ter -> silêncio

    key = sprint_start.isoformat()
    try:
        with open(STAMP) as f:
            if f.read().strip() == key:
                return                        # já disparou nesta sprint
    except FileNotFoundError:
        pass

    try:
        os.makedirs(os.path.dirname(STAMP), exist_ok=True)
        with open(STAMP, "w") as f:
            f.write(key)
    except OSError:
        pass                                  # sem carimbo ainda dispara (melhor lembrar que silenciar)

    sprint_end = sprint_start + datetime.timedelta(days=11)   # sexta da 2ª semana
    msg = (
        "[Agente 8 · agenda] Início de uma nova sprint quinzenal "
        f"({sprint_start.strftime('%d/%m')}–{sprint_end.strftime('%d/%m')}). "
        "Rode agora o skill agenda: leia a seção do Paulo na Planning do "
        "ciclo atual (Notion); se estiver preenchida (não os placeholders 'Prioridade 1/2/3'), "
        "faça o T-shirt size + ordem lógica, monte os blocos nos slots livres da agenda "
        "(seg–sex 09–18, sem almoço 12–13, sem sobrepor) e PROPONHA o plano aqui no chat pro "
        "Paulo aprovar ANTES de criar. Se a seção dele estiver vazia/placeholder, avise e não crie nada."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": msg,
    }}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass                                  # hook nunca deve quebrar a sessão
    sys.exit(0)

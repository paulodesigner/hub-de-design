#!/usr/bin/env python3
"""
Roteador de intenção (2026-07-30) — UserPromptSubmit hook.

Detecta, por regex sobre a própria mensagem do usuário, se o pedido corresponde
a um dos 14 agentes do Hub (mesmos gatilhos da seção "Desambiguação" do
CLAUDE.md raiz) — MESMO que o usuário não chame o agente pelo nome, não use
slash-command e o loop principal não declare formalmente a chamada.

POR QUE ISSO EXISTE (achado real, 2026-07-30): o hook de telemetria
(telemetria.py) só contava uso via SubagentStop (spawn) ou SkillInvoke
(chamada explícita da tool `Skill`) — mas vários pedidos ("cria um vídeo
desse fluxo") são atendidos pelo loop principal seguindo o PAPEL do agente
sem declarar isso formalmente. Resultado: codigo-ao-video tinha uso real
medido em 0% sempre, apesar de rodado várias vezes. Não dá pra confiar em
"o modelo vai lembrar de chamar a tool certa" (mesma classe de fragilidade já
documentada pro convite de ativação do painel — ver painel-sync-trigger.py):
a detecção precisa ser MECÂNICA, não uma instrução que só funciona se lembrada.

DECISÃO DO PAULO (2026-07-30): contar a detecção JUNTO com as demais execuções
no painel (não como categoria separada) — aceita o trade-off de que um pedido
detectado e depois abandonado/mudado de rumo ainda conta como 1 execução.

ESCOPO (2026-07-30, expandido no mesmo dia): registrado em settings.json
COMPARTILHADO (não mais só settings.local.json) — propaga automaticamente pra
qualquer projeto-irmão já symlinkado (invoice-flows, inteligencia-de-mercado)
e pra qualquer projeto novo conectado ao Hub (padrão "Projeto nasce conectado
ao Hub"), e chega pro resto do time via hub-autosync assim que este arquivo
for pra `main`. Conceito: "os AGENTES fazem algo", não "o Hub faz algo" — a
contagem é por agente, em qualquer projeto/pessoa que o usar. Não grava nome
de tarefa nenhum, só o slug do agente + sessão + timestamp (decisão do Paulo:
"é só contabilização"). Ver memoria/estado-atual.md.

DEDUP DE DUPLA CONTAGEM: se o MESMO pedido, além de disparar esta detecção,
também terminar gerando um SubagentStop/SkillInvoke real (ex.: regras-de-negocio,
que já roda por spawn hoje), o rollup (telemetria.py/_rollup_painel e
scripts/gerar-adocao.py/coletar) ignora o IntentDetected quando já existe um
evento "de verdade" pro mesmo (session_id, agente) — implementado nos dois
lugares, não aqui (este hook só grava o span cru).

AMBIGUIDADE: se a mensagem bater com o padrão de MAIS DE UM agente (ou de
nenhum), não grava nada — melhor não contar do que atribuir errado.

REGRA DE OURO (igual telemetria.py): nunca travar/atrasar a sessão. Qualquer
erro, silêncio total.
"""
import sys
import os
import re
import json
import unicodedata
from datetime import datetime, timezone


def _sem_acento(s):
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# Padrões por agente — combinações (nunca palavra solta) pra reduzir falso
# positivo. Escritos sem acento: o texto do usuário é normalizado (minúsculo +
# sem acento) antes de comparar, então cobre digitação com ou sem acento.
PADROES = {
    "codigo-ao-figma": [
        r"desenh\w+ .*(basead\w+ no codigo|fiel ao codigo|\b1:1\b|as-?is)",
        r"replic\w+ .*(codigo|componente).*figma",
        r"leva\w* .*(pro|para o) figma",
        r"codigo (pro|para o) figma",
        r"\bcode to figma\b",
    ],
    "estudio-de-design": [
        r"\bredesenh\w+\b",
        r"journey ?map",
        r"analise heuristica|heuristica de nielsen",
        r"\bux copy\b",
        r"prototipo (de|da|do)",
        r"propon\w* (uma|um) (tela|fluxo)",
        r"melhor\w+ (essa|esta|este) (tela|fluxo)",
    ],
    "regras-de-negocio": [
        r"quais? (sao )?as regras",
        r"o que acontece se",
        r"mapear? as regras",
        r"matriz (de|por) (decisao|estado)",
        r"chao firme",
    ],
    "mapa-do-design-system": [
        r"(atualiza|refresh|refaz)\w* .*mapa (do|de) design system",
        r"o que (da|posso) reusar no figma",
    ],
    "leitor-de-comentarios": [
        r"(analis|clusteriz)\w+ os comentarios",
        r"o que .*pediu.*prioriz",
    ],
    "relatorio-de-atividades": [
        r"relatorio da semana",
        r"o que (eu )?fiz essa semana",
        r"resumo de atividades",
    ],
    "figma-ao-codigo": [
        r"transform\w+ (esse|este|esta) figma em codigo",
        r"implementa\w+ esse node",
        r"porta\w+ o design (pro|para o) app",
        r"figma (pro|para o) codigo",
    ],
    "agenda-da-sprint": [
        r"monta\w* (a |minha )?agenda da sprint",
        r"planeja\w* a agenda da quinzena",
        r"a partir da planning",
    ],
    "construtor-do-storybook": [
        r"(cria|criar|atualiza\w*|adiciona\w*) .*(story|storybook)",
        r"documenta\w* os tokens.{0,2}foundations",
        r"prepara\w* o storybook",
    ],
    "documentacao-do-ds": [
        r"documenta\w* o componente",
        r"escreve\w* a anatomia",
        r"quando-?usar",
        r"do'?s? (e|&) don'?ts?",
        r"padroniza\w* a documentacao do ds",
        r"mdx docs",
    ],
    "anfitriao": [
        r"por onde comeco",
        r"me da um tour",
        r"qual agente faz",
        r"o que ja esta conectado",
        r"como funciona isso aqui",
    ],
    "codigo-ao-video": [
        r"(cri\w*|grav\w*|faz\w*|fez|monta\w*) .*video",
        r"video (do|desse|deste) fluxo",
        r"video de apresentacao",
        r"narracao.*video",
        r"legenda.*video",
        r"avatar narrando",
    ],
    "publicador-seguro": [
        r"publica\w* .*(com seguranca|protegid\w*)",
        r"coloca\w* (isso|isto) no ar",
        r"compartilha\w* .*protegid\w* por senha",
        r"como publico isso online",
    ],
    "animador-de-personagem": [
        r"anima\w* o mascote",
        r"(poses?|expressoes?) (do|desse|deste) (mascote|personagem)",
        r"quadro a quadro",
        r"walk cycle",
        r"model sheet|turnaround|expression sheet",
        r"(bounce|celebra\w*) do (mascote|personagem)",
    ],
}

_COMPILED = {ag: [re.compile(p) for p in pats] for ag, pats in PADROES.items()}


def detectar(texto_bruto):
    """Retorna o slug do ÚNICO agente cujo padrão bateu, ou None (0 ou >1 =
    ambíguo, não conta)."""
    texto = _sem_acento(texto_bruto.lower())
    achados = {ag for ag, pats in _COMPILED.items() if any(p.search(texto) for p in pats)}
    if len(achados) == 1:
        return next(iter(achados))
    return None


def ja_detectado_na_sessao(outfile, session_id, agente):
    """Dedup: não grava 2x o mesmo agente na mesma sessão (usuário pode reforçar
    o pedido em mais de uma mensagem seguida)."""
    if not (session_id and os.path.exists(outfile)):
        return False
    try:
        with open(outfile) as fh:
            for linha in fh:
                try:
                    s = json.loads(linha)
                except Exception:
                    continue
                if (s.get("event") == "IntentDetected"
                        and s.get("session_id") == session_id
                        and s.get("agent") == agente):
                    return True
    except Exception:
        pass
    return False


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    if data.get("hook_event_name") != "UserPromptSubmit":
        return

    prompt = data.get("prompt") or ""
    if not prompt.strip():
        return

    agente = detectar(prompt)
    if not agente:
        return

    session_id = data.get("session_id")
    cwd = data.get("cwd")
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or cwd or "."
    outdir = os.path.join(proj, "memoria", "telemetria")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, "traces.jsonl")

    if not ja_detectado_na_sessao(outfile, session_id, agente):
        span = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event": "IntentDetected",
            "agent": agente,
            "agent_id": None,
            "session_id": session_id,
            "effort": None,
            "measured": False,
            "duration_s": None,
            "turns": None,
            "by_model": {},
            "total_cost_usd": 0.0,
            "total_tokens": 0,
        }
        with open(outfile, "a") as fh:
            fh.write(json.dumps(span, ensure_ascii=False) + "\n")

    msg = (
        f"[roteador-agente] Esta mensagem parece corresponder ao Agente "
        f"'{agente}' do Hub. Siga o papel/skill desse agente ao responder — "
        f"a execução já foi contabilizada automaticamente no painel de "
        f"eficiência (independente do resultado final da tarefa)."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": msg,
    }}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

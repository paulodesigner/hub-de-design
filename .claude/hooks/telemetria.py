#!/usr/bin/env python3
"""
Telemetria de execução do Hub (M18) — tracing sempre-ligado, estilo Dapper.

Escreve UM span (linha JSONL) por evento em memoria/telemetria/traces.jsonl:
  • SessionEnd   → o LOOP PRINCIPAL (transcript da sessão)      → agente "main-loop"
  • SubagentStop → cada SUBAGENTE, pelo TRANSCRIPT DELE          → agente = agent_type
  • SkillInvoke  → cada chamada de skill DENTRO do loop principal → agente = nome da skill

⚠️ GAP DE ADOÇÃO (fix 2026-07-29): `painel-eficiencia` mostrava 0% de adoção pra
quem usa os agentes conversando direto no chat principal (skill), em vez de
via spawn de subagente — só `SubagentStop` era medido. Vários dos 12 agentes
do Hub são pensados justamente pra rodar como skill no loop principal (ex.:
Anfitrião, Regras de Negócio). Fix: no `SessionEnd`, além do span do
"main-loop", escaneia o MESMO transcript por chamadas da tool `Skill` e grava
1 span leve (`measured=false`, sem custo/tempo — inseparável do resto da
sessão) por invocação de uma das skills dos 12 agentes, dedupado pelo
`tool_use_id` (robusto a sessão retomada/`SessionEnd` disparando de novo).

⚠️ ATRIBUIÇÃO (fix 2026-07-20): no SubagentStop o payload traz `transcript_path`
apontando pro transcript do LOOP PRINCIPAL, NÃO o do subagente (bug original do
M18: media 110M+ tokens em Opus e atribuía ao subagente, que era Sonnet). O
transcript real do subagente vive em `<session_dir>/tasks/<agent_id>.output` —
localizado por glob direcionado (session_id + agent_id). Se não achar, grava um
span LEVE (só metadata, sem tokens/custo) com `measured=false` — melhor sem
número do que número errado.

DEDUP: o SubagentStop pode re-disparar pro mesmo agente ("fires each time this
agent stops with no live children") → antes de gravar, pula se já existe span
idêntico (mesmo event+agent_id+total_tokens) nas últimas linhas.

REGRA DE OURO: nunca travar nem atrasar a sessão. Engole todo erro e sai 0.
traces.jsonl NÃO é versionado (está no .gitignore) — é dado de execução, local.
Origem: melhorias.md M18 (lente de system design → Dapper/FAWN/Tail-at-Scale).
"""
import sys
import os
import re
import json
import subprocess
import urllib.error
import urllib.request

# Preço por 1M tokens (USD). cache write 5m = 1.25×input · cache read = 0.1×input.
# Sonnet 5: preço intro $2/$10 até 2026-08-31; depois $3/$15 (usando cheio, conservador).
# Ajuste aqui se a tabela oficial mudar.
PRECOS = {
    "claude-opus-4-8":   {"in": 5.00,  "out": 25.00},
    "claude-opus-4-7":   {"in": 5.00,  "out": 25.00},
    "claude-sonnet-5":   {"in": 3.00,  "out": 15.00},
    "claude-sonnet-4-6": {"in": 3.00,  "out": 15.00},
    "claude-haiku-4-5":  {"in": 1.00,  "out": 5.00},
    "claude-fable-5":    {"in": 10.00, "out": 50.00},
}


def custo(modelo, u):
    """Custo estimado em USD de um pacote de tokens; None se o modelo é desconhecido."""
    p = PRECOS.get(modelo)
    if not p:
        return None
    return round(
        u["in"] / 1e6 * p["in"]
        + u["out"] / 1e6 * p["out"]
        + u["cache_w"] / 1e6 * (p["in"] * 1.25)
        + u["cache_r"] / 1e6 * (p["in"] * 0.10),
        6,
    )


def _parse_ts(s):
    from datetime import datetime
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def agregar(transcript_path):
    """Lê o transcript JSONL e retorna (por_modelo, n_turnos, duracao_s).

    Dedup por message.id: um turno aparece em várias linhas (stream) — conta 1×,
    ficando com o usage do registro de maior output_tokens (o final do turno).
    Ignora modelos '<synthetic>'/vazios.
    """
    melhor = {}   # id do turno -> (usage, modelo)
    ts_vals = []
    with open(transcript_path, "r") as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha:
                continue
            try:
                o = json.loads(linha)
            except Exception:
                continue
            if o.get("type") != "assistant":
                continue
            msg = o.get("message") or {}
            modelo = msg.get("model") or ""
            if not modelo or modelo.startswith("<"):
                continue
            u = msg.get("usage") or {}
            out = u.get("output_tokens", 0) or 0
            key = msg.get("id") or o.get("uuid")  # id da API; fallback: uuid único da linha
            t = o.get("timestamp")
            if t:
                ts_vals.append(t)
            prev = melhor.get(key)
            if prev is None or out > (prev[0].get("output_tokens", 0) or 0):
                melhor[key] = (u, modelo)

    por_modelo = {}
    for (u, modelo) in melhor.values():
        d = por_modelo.setdefault(modelo, {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0})
        d["in"] += u.get("input_tokens", 0) or 0
        d["out"] += u.get("output_tokens", 0) or 0
        d["cache_w"] += u.get("cache_creation_input_tokens", 0) or 0
        d["cache_r"] += u.get("cache_read_input_tokens", 0) or 0

    dur = None
    parsed = [p for p in (_parse_ts(t) for t in ts_vals) if p]
    if len(parsed) >= 2:
        dur = round((max(parsed) - min(parsed)).total_seconds(), 1)

    return por_modelo, len(melhor), dur


# Os 14 agentes do carrossel (mesma lista de `scripts/gerar-adocao.py`,
# SLUG_TO_KEY) — só chamada de skill DESSES conta como adoção; qualquer outra
# skill (dataviz, ux-writing etc.) é ruído pro painel de adoção do time.
AGENTES_HUB = {
    "codigo-ao-figma", "estudio-de-design", "regras-de-negocio",
    "mapa-do-design-system", "leitor-de-comentarios", "relatorio-de-atividades",
    "figma-ao-codigo", "agenda-da-sprint", "construtor-do-storybook",
    "documentacao-do-ds", "anfitriao", "codigo-ao-video",
    "publicador-seguro", "animador-de-personagem",
}

# --- Sincronização automática com o painel-eficiencia (2026-07-30) ---------
# Substitui o fluxo manual antigo (rodar scripts/gerar-adocao.py → git commit
# → git push → redeploy manual) por um POST silencioso a cada SessionEnd, IF
# a pessoa já ativou (arquivo de token existe — ver skill do Anfitrião, que
# oferece a ativação na conversa, sem terminal). Sem token = sem sync, sem
# erro visível: a pessoa simplesmente ainda não ativou.
SLUG_TO_KEY_PAINEL = {
    "codigo-ao-figma": "a1", "estudio-de-design": "a2", "regras-de-negocio": "a3",
    "mapa-do-design-system": "a4", "leitor-de-comentarios": "a5",
    "relatorio-de-atividades": "a6", "figma-ao-codigo": "a7",
    "agenda-da-sprint": "a8", "construtor-do-storybook": "a9",
    "documentacao-do-ds": "a10", "anfitriao": "a11", "codigo-ao-video": "a12",
    "publicador-seguro": "a13", "animador-de-personagem": "a14",
}
PESSOAS_CONHECIDAS_PAINEL = ["designer1", "designer2", "designer3", "paulo"]
TOKEN_PATH_PAINEL = os.path.expanduser("~/.config/hub/painel_sync_token")
API_BASE_PAINEL = "https://hub-de-design.vercel.app"

# --- Visibilidade de falha de sync (2026-07-30) ------------------------------
# O POST pro /api/sync roda em background com erro engolido (regra de ouro:
# telemetria nunca trava a sessão) — mas "nunca trava" não devia significar
# "ninguém nunca fica sabendo se falhar pra sempre". Este status é lido pelo
# hook painel-sync-trigger.py (SessionStart) pra alertar quando a falha vira
# padrão (não um blip único). Fica em ~/.config/hub/ (por PESSOA, não por
# projeto — a saúde da API/rede é a mesma não importa de qual projeto se
# sincroniza).
STATUS_PATH_PAINEL = os.path.expanduser("~/.config/hub/painel-sync-status.json")


def _grava_status_sync(ok, erro=None):
    from datetime import datetime, timezone as tz
    agora = datetime.now(tz.utc).isoformat(timespec="seconds")
    estado = {"last_attempt": None, "last_success": None, "last_error": None, "consecutive_failures": 0}
    try:
        if os.path.exists(STATUS_PATH_PAINEL):
            with open(STATUS_PATH_PAINEL) as f:
                estado.update(json.load(f))
    except Exception:
        pass
    estado["last_attempt"] = agora
    if ok:
        estado["last_success"] = agora
        estado["consecutive_failures"] = 0
        estado["last_error"] = None
    else:
        estado["consecutive_failures"] = estado.get("consecutive_failures", 0) + 1
        estado["last_error"] = (erro or "erro desconhecido")[:300]
    try:
        os.makedirs(os.path.dirname(STATUS_PATH_PAINEL), exist_ok=True)
        with open(STATUS_PATH_PAINEL, "w") as f:
            json.dump(estado, f)
    except Exception:
        pass  # visibilidade é best-effort — não pode ser o motivo de travar a sessão


def _slug_projeto(proj):
    """Identifica DE QUAL PROJETO vem esse uso (Hub, invoice-flows, etc.) — cada
    projeto tem seu próprio memoria/telemetria/traces.jsonl; sem isso, sincronizar
    de 2 projetos diferentes na mesma sessão de trabalho SOBRESCREVE um pelo outro
    no painel em vez de somar. "VS Code" (nome legado da pasta do Hub) vira "hub"
    pra não aparecer com esse nome estranho pro time."""
    base = os.path.basename(os.path.normpath(proj or "")).strip().lower()
    if base in ("vs code", "vscode", ""):
        return "hub"
    slug = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return slug or "outro"


def _pessoa_do_git():
    try:
        email = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True,
            check=True, timeout=2,
        ).stdout.strip().lower()
    except Exception:
        return None
    primeiro = email.split("@")[0].split(".")[0] if email else ""
    return primeiro if primeiro in PESSOAS_CONHECIDAS_PAINEL else None


def _fmt_tempo_painel(segundos):
    segundos = round(segundos)
    m, s = divmod(segundos, 60)
    return f"{m}m{s:02d}s"


def _rollup_painel(traces_path, mes_ref):
    """Mesma lógica de scripts/gerar-adocao.py (coletar+resumir), inlined aqui
    pra não precisar importar um script fora de .claude/hooks/. Retorna
    {'mes': {a1:{exec,tempo}}, 'tudo': {...}}.

    IntentDetected (2026-07-30, roteador-agente-trigger.py) conta como execução
    igual SubagentStop/SkillInvoke — MAS só quando é o ÚNICO sinal daquele
    (session_id, agente): se o mesmo pedido também gerou um SubagentStop/
    SkillInvoke de verdade na mesma sessão, o IntentDetected é ignorado pra não
    contar a mesma execução 2×. Por isso precisa de 2 passadas: 1ª monta o
    conjunto de (session_id, agente) já "confirmados"; 2ª conta de verdade."""
    from collections import defaultdict
    contagem = {"mes": defaultdict(list), "tudo": defaultdict(list)}
    if not os.path.exists(traces_path):
        return {"mes": {}, "tudo": {}}

    spans = []
    with open(traces_path) as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha:
                continue
            try:
                spans.append(json.loads(linha))
            except json.JSONDecodeError:
                continue

    confirmados = {
        (s.get("session_id"), s.get("agent"))
        for s in spans if s.get("event") in ("SubagentStop", "SkillInvoke")
    }

    for span in spans:
        event = span.get("event")
        if event not in ("SubagentStop", "SkillInvoke", "IntentDetected"):
            continue
        if event == "IntentDetected" and (span.get("session_id"), span.get("agent")) in confirmados:
            continue  # já contado via evento "de verdade" na mesma sessão — evita dobra
        key = SLUG_TO_KEY_PAINEL.get(span.get("agent"))
        if not key:
            continue
        dur = span.get("duration_s") if span.get("measured") else None
        contagem["tudo"][key].append(dur)
        ts = span.get("ts")
        if ts:
            try:
                dt = _parse_ts(ts)
                if dt and (dt.year, dt.month) == mes_ref:
                    contagem["mes"][key].append(dur)
            except Exception:
                pass

    def resumir(periodo):
        out = {}
        for k, durs in periodo.items():
            medidas = [d for d in durs if d is not None]
            out[k] = {
                "exec": len(durs),
                "tempo": _fmt_tempo_painel(sum(medidas) / len(medidas)) if medidas else None,
            }
        return out

    return {"mes": resumir(contagem["mes"]), "tudo": resumir(contagem["tudo"])}


def sincronizar_painel(traces_path, proj):
    """Chamado no fim do SessionEnd, de QUALQUER projeto (Hub ou irmão) que tenha
    os hooks ligados. Nunca trava/atrasa a sessão (regra de ouro): sem token
    ainda (pessoa não ativou) = não faz nada, sem gravar status nenhum (não é
    falha, é "ainda não ativou"). Qualquer erro de rede DEPOIS de tentar =
    gravado em STATUS_PATH_PAINEL (visível pro painel-sync-trigger.py alertar),
    nunca levanta pra fora desta função."""
    if not os.path.exists(TOKEN_PATH_PAINEL):
        return
    pessoa = _pessoa_do_git()
    if not pessoa:
        return
    try:
        with open(TOKEN_PATH_PAINEL) as fh:
            token = fh.read().strip()
        if not token:
            return
        from datetime import datetime, timezone as tz
        agora = datetime.now(tz.utc)
        rollup = _rollup_painel(traces_path, (agora.year, agora.month))
        payload = json.dumps({"pessoa": pessoa, "projeto": _slug_projeto(proj), **rollup}).encode("utf-8")
        req = urllib.request.Request(
            f"{API_BASE_PAINEL}/api/sync",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=4)
        except urllib.error.HTTPError as e:
            _grava_status_sync(False, f"HTTP {e.code}: {e.reason}")
            return
        except urllib.error.URLError as e:
            _grava_status_sync(False, f"rede: {e.reason}")
            return
        _grava_status_sync(True)
    except Exception as e:
        try:
            _grava_status_sync(False, f"{type(e).__name__}: {e}")
        except Exception:
            pass  # regra de ouro do módulo: telemetria nunca trava/atrasa a sessão


def skill_invocations(transcript_path):
    """Varre o transcript do loop principal por chamadas da tool `Skill` de um
    dos AGENTES_HUB. Retorna [{'id':tool_use_id, 'skill':slug, 'ts':...}, ...],
    1 item por invocação real (cada tool_use tem um id único no transcript)."""
    out = []
    with open(transcript_path, "r") as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha:
                continue
            try:
                o = json.loads(linha)
            except Exception:
                continue
            if o.get("type") != "assistant":
                continue
            msg = o.get("message") or {}
            for bloco in (msg.get("content") or []):
                if not isinstance(bloco, dict) or bloco.get("type") != "tool_use":
                    continue
                if bloco.get("name") != "Skill":
                    continue
                slug = (bloco.get("input") or {}).get("skill")
                if slug not in AGENTES_HUB:
                    continue
                out.append({"id": bloco.get("id"), "skill": slug, "ts": o.get("timestamp")})
    return out


def skills_ja_gravados(outfile):
    """Conjunto de tool_use_id já gravados como SkillInvoke — dedup contra
    SessionEnd repetido (resume), varrendo o arquivo inteiro (local, pequeno)."""
    vistos = set()
    if not os.path.exists(outfile):
        return vistos
    try:
        with open(outfile) as fh:
            for l in fh:
                try:
                    s = json.loads(l)
                except Exception:
                    continue
                if s.get("event") == "SkillInvoke" and s.get("tool_use_id"):
                    vistos.add(s["tool_use_id"])
    except Exception:
        pass
    return vistos


def find_subagent_transcript(session_id, agent_id):
    """Acha o transcript do SUBAGENTE (não o principal que vem no payload).

    Vive em `<session_dir>/tasks/<agent_id>.output`; o session_dir é temporário
    (`/private/tmp/<claude-N>/<slug>/<session_id>/`), com N e slug variáveis →
    glob direcionado por session_id+agent_id (ambos únicos → barato e específico).
    Retorna o caminho ou None.
    """
    import glob
    if not (session_id and agent_id):
        return None
    for root in ("/private/tmp", "/tmp", os.path.expanduser("~/.claude")):
        hits = glob.glob(os.path.join(root, "*", "*", session_id, "tasks", f"{agent_id}.output"))
        if hits:
            return hits[0]
    return None


def ja_gravado(outfile, event, agent_id, total_tok):
    """Dedup defensiva contra re-disparo do SubagentStop: True se as últimas
    linhas já têm um span idêntico (mesmo event+agent_id+total_tokens)."""
    if not (agent_id and os.path.exists(outfile)):
        return False
    try:
        with open(outfile) as fh:
            linhas = fh.readlines()[-30:]
        for l in reversed(linhas):
            try:
                s = json.loads(l)
            except Exception:
                continue
            if (s.get("event") == event and s.get("agent_id") == agent_id
                    and s.get("total_tokens") == total_tok):
                return True
    except Exception:
        return False
    return False


def main():
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}

    event = data.get("hook_event_name", "?")
    if event not in ("SubagentStop", "SessionEnd"):
        return  # payload vazio/inesperado → não gera span "?"
    session_id = data.get("session_id")
    cwd = data.get("cwd")
    tpath = data.get("transcript_path")
    agent_type = data.get("agent_type")
    agent_id = data.get("agent_id")
    effort = os.environ.get("CLAUDE_EFFORT")

    agente = agent_type if event == "SubagentStop" else "main-loop"

    # SubagentStop: o transcript_path do payload é o do PRINCIPAL (bug M18) →
    # trocar pelo transcript real do subagente. SessionEnd: usar o principal mesmo.
    measured = True
    if event == "SubagentStop":
        sub = find_subagent_transcript(session_id, agent_id)
        tpath = sub  # se None, não mede (span leve) em vez de medir o principal errado
        if not sub:
            measured = False

    por_modelo, turnos, dur = ({}, 0, None)
    if tpath and os.path.exists(tpath):
        por_modelo, turnos, dur = agregar(tpath)

    by_model = {}
    total_cost = 0.0
    total_tok = 0
    for modelo, u in por_modelo.items():
        c = custo(modelo, u)
        by_model[modelo] = {**u, "cost_usd": c}
        if c:
            total_cost += c
        total_tok += u["in"] + u["out"] + u["cache_w"] + u["cache_r"]

    from datetime import datetime, timezone
    span = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event,
        "agent": agente,
        "agent_id": agent_id,
        "session_id": session_id,
        "effort": effort,
        "measured": measured,   # false = transcript do subagente não localizado (sem tokens/custo)
        "duration_s": dur,
        "turns": turnos,
        "by_model": by_model,
        "total_cost_usd": round(total_cost, 6),
        "total_tokens": total_tok,
    }

    proj = os.environ.get("CLAUDE_PROJECT_DIR") or cwd or "."
    outdir = os.path.join(proj, "memoria", "telemetria")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, "traces.jsonl")
    if not ja_gravado(outfile, event, agent_id, total_tok):
        with open(outfile, "a") as fh:
            fh.write(json.dumps(span, ensure_ascii=False) + "\n")

    # SessionEnd: além do span agregado do main-loop, grava 1 span leve por
    # chamada de skill de um dos 12 agentes feita DENTRO dessa conversa.
    if event == "SessionEnd" and tpath and os.path.exists(tpath):
        ja_vistos = skills_ja_gravados(outfile)
        novos = [i for i in skill_invocations(tpath) if i["id"] and i["id"] not in ja_vistos]
        if novos:
            from datetime import datetime as _dt, timezone as _tz
            with open(outfile, "a") as fh:
                for inv in novos:
                    skill_span = {
                        "ts": inv["ts"] or _dt.now(_tz.utc).isoformat(timespec="seconds"),
                        "event": "SkillInvoke",
                        "agent": inv["skill"],
                        "agent_id": None,
                        "tool_use_id": inv["id"],
                        "session_id": session_id,
                        "effort": effort,
                        "measured": False,  # custo/tempo da skill não é isolável do resto da sessão
                        "duration_s": None,
                        "turns": None,
                        "by_model": {},
                        "total_cost_usd": 0.0,
                        "total_tokens": 0,
                    }
                    fh.write(json.dumps(skill_span, ensure_ascii=False) + "\n")

        sincronizar_painel(outfile, proj)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # telemetria nunca pode quebrar a sessão
    sys.exit(0)

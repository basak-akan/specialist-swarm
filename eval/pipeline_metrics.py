"""Layer 1 pipeline-health metrics computed from run_dir/events.jsonl.

Each line of events.jsonl is `event.model_dump(mode="json")` from the Managed
Agents stream plus a local `received_at` ISO timestamp. The parser is tolerant:
unknown fields are ignored, and agent names are looked up in a few plausible
places (top-level, or nested under `thread` / `agent`).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ADVISOR_NAMES = {"anthropic.advisor"}
CRITIC_RE = re.compile(r"critic|hr business partner", re.IGNORECASE)
COORDINATOR_RE = re.compile(r"coordinator|orchestrator", re.IGNORECASE)
VERDICT_RE = re.compile(r"VERDICT\s*[:\-]\s*\**\s*(SHIP\s*IT|REVISE|STOP)", re.IGNORECASE)

DOCX_NAME = "day1-readiness-pack.docx"
PPTX_NAME = "day1-readiness-brief.pptx"

# ESTIMATES ONLY -- USD per 1M tokens (input, output, cache_write, cache_read).
# Taken from public list prices (Nov 2026); cache_write assumes the 5-min 1.25x rate.
# Used to give a rough cost signal for comparing configs, not for billing.
PRICE_TABLE_USD_PER_MTOK: dict[str, tuple[float, float, float, float]] = {
    "claude-opus-5-5": (4.00, 20.00, 5.00, 0.20),
    "claude-opus-5": (5.00, 25.00, 6.25, 0.50),
    "claude-opus-4-8": (5.00, 25.00, 6.25, 0.50),
    "claude-opus-4-7": (5.00, 25.00, 6.25, 0.50),
    "claude-opus-4-6": (5.00, 25.00, 6.25, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00, 2.50, 0.20),
    "claude-sonnet-5": (2.00, 10.00, 2.50, 0.20),
    "claude-sonnet-4-6": (3.00, 15.00, 3.75, 0.30),
    "claude-sonnet-4-5": (3.00, 15.00, 3.75, 0.30),
    "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.01),
    "claude-haiku-4-5": (1.00, 5.00, 1.25, 0.10),
}
DEFAULT_PRICE_MODEL = "claude-opus-5-5"

USAGE_KEYS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


# ---------------------------------------------------------------- helpers
def load_events(path) -> list[dict]:
    events = []
    p = Path(path)
    if not p.exists():
        return events
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _parse_ts(val) -> datetime | None:
    if not val or not isinstance(val, str):
        return None
    s = val.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        from datetime import timezone

        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def event_time(ev: dict) -> datetime | None:
    return _parse_ts(ev.get("processed_at")) or _parse_ts(ev.get("received_at"))


def _get_name(ev: dict, *keys: str) -> str | None:
    for k in keys:
        v = ev.get(k)
        if isinstance(v, str) and v:
            return v
    for nest in ("thread", "agent", "session_thread"):
        sub = ev.get(nest)
        if isinstance(sub, dict):
            for k in keys + ("name", "agent_name"):
                v = sub.get(k)
                if isinstance(v, str) and v:
                    return v
    return None


def content_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type", "text") == "text" and isinstance(b.get("text"), str):
                    parts.append(b["text"])
            elif isinstance(b, str):
                parts.append(b)
        return "\n".join(parts)
    if isinstance(content, dict):
        return content.get("text", "") if isinstance(content.get("text"), str) else ""
    return str(content)


def is_critic(name: str | None) -> bool:
    return bool(name) and bool(CRITIC_RE.search(name))


def _is_specialist(name: str | None, coordinator_name: str | None = None) -> bool:
    if not name or name in ADVISOR_NAMES or is_critic(name):
        return False
    if coordinator_name and name == coordinator_name:
        return False
    if COORDINATOR_RE.search(name):
        return False
    return True


def _walk_usage(obj, acc: dict, per_model: dict, model_hint: str | None = None):
    """Recursively find dicts with token-usage keys and sum them."""
    if isinstance(obj, dict):
        model = obj.get("model") if isinstance(obj.get("model"), str) else model_hint
        if any(k in obj and isinstance(obj[k], (int, float)) for k in USAGE_KEYS):
            bucket = per_model.setdefault(model or "unknown", dict.fromkeys(USAGE_KEYS, 0))
            for k in USAGE_KEYS:
                v = obj.get(k)
                if isinstance(v, (int, float)):
                    acc[k] += int(v)
                    bucket[k] += int(v)
            # also descend into non-usage children (e.g. cache_creation breakdown is skipped)
            for k, v in obj.items():
                if k not in USAGE_KEYS and isinstance(v, (dict, list)) and k != "cache_creation":
                    _walk_usage(v, acc, per_model, model)
            return
        for v in obj.values():
            _walk_usage(v, acc, per_model, model)
    elif isinstance(obj, list):
        for v in obj:
            _walk_usage(v, acc, per_model, model_hint)


def estimate_cost(per_model: dict, default_model: str | None = None) -> float:
    total = 0.0
    for model, u in per_model.items():
        key = model if model in PRICE_TABLE_USD_PER_MTOK else None
        if key is None:
            # fuzzy: strip date suffixes / prefixes
            for k in PRICE_TABLE_USD_PER_MTOK:
                if isinstance(model, str) and k in model:
                    key = k
                    break
        if key is None:
            key = default_model if default_model in PRICE_TABLE_USD_PER_MTOK else DEFAULT_PRICE_MODEL
        pi, po, pcw, pcr = PRICE_TABLE_USD_PER_MTOK[key]
        total += (
            u.get("input_tokens", 0) * pi
            + u.get("output_tokens", 0) * po
            + u.get("cache_creation_input_tokens", 0) * pcw
            + u.get("cache_read_input_tokens", 0) * pcr
        ) / 1_000_000
    return round(total, 4)


def _secs(a: datetime | None, b: datetime | None) -> float | None:
    if a is None or b is None:
        return None
    return round((b - a).total_seconds(), 3)


# ---------------------------------------------------------------- main
def compute(run_dir, coordinator_name: str | None = None, default_model: str | None = None) -> dict:
    run_dir = Path(run_dir)
    events = load_events(run_dir / "events.jsonl")
    if default_model is None:
        cfg_path = run_dir / "config.json"
        if cfg_path.exists():
            try:
                cfg = json.loads(cfg_path.read_text())
                models = cfg.get("models") or {}
                if isinstance(models, dict):
                    default_model = models.get("coordinator") or next(iter(models.values()), None)
                coordinator_name = coordinator_name or cfg.get("coordinator_name")
            except Exception:
                pass

    times = [t for t in (event_time(e) for e in events) if t is not None]
    first_t = min(times) if times else None
    last_t = max(times) if times else None

    error_events = []
    last_idle_reason = None
    first_creation: dict[str, datetime | None] = {}
    critic_rounds = 0
    critic_messages: list[tuple[datetime | None, str]] = []
    first_delegation_t: datetime | None = None
    tool_uses: dict[str, int] = {}
    thread_status_counts: dict[str, int] = {}

    for ev in events:
        et = ev.get("type", "") or ""
        t = event_time(ev)
        if "error" in et.lower():
            error_events.append({"type": et, "error": ev.get("error") or ev.get("message")})
        if et == "session.status_idle":
            sr = ev.get("stop_reason")
            last_idle_reason = sr.get("type") if isinstance(sr, dict) else sr
        elif et == "session.thread_created":
            name = _get_name(ev, "agent_name")
            if name and name not in first_creation:
                first_creation[name] = t
            if t is not None and (_is_specialist(name, coordinator_name) or is_critic(name)):
                first_delegation_t = t if first_delegation_t is None else min(first_delegation_t, t)
        elif et == "agent.thread_message_sent":
            to = _get_name(ev, "to_agent_name", "agent_name")
            if is_critic(to):
                critic_rounds += 1
            if to and to not in ADVISOR_NAMES and t is not None:
                first_delegation_t = t if first_delegation_t is None else min(first_delegation_t, t)
        elif et == "agent.thread_message_received":
            frm = _get_name(ev, "from_agent_name", "agent_name")
            if is_critic(frm):
                critic_messages.append((t, content_text(ev.get("content"))))
        elif et == "agent.tool_use":
            n = ev.get("name") or "?"
            tool_uses[n] = tool_uses.get(n, 0) + 1
        elif et.startswith("session.thread_status_"):
            s = et.rsplit("_", 1)[-1]
            thread_status_counts[s] = thread_status_counts.get(s, 0) + 1

    specialist_names = sorted(n for n in first_creation if _is_specialist(n, coordinator_name))
    critic_present = any(is_critic(n) for n in first_creation)
    spec_times = [first_creation[n] for n in specialist_names if first_creation[n] is not None]
    fanout = _secs(min(spec_times), max(spec_times)) if len(spec_times) >= 1 else None

    verdict = None
    if critic_messages:
        # last message from critic (order of appearance; events are chronological)
        txt = critic_messages[-1][1]
        matches = VERDICT_RE.findall(txt)
        if matches:
            verdict = re.sub(r"\s+", " ", matches[-1].upper())

    # usage
    acc = dict.fromkeys(USAGE_KEYS, 0)
    per_model: dict[str, dict] = {}
    usage_source = None
    usage_json = run_dir / "usage.json"
    if usage_json.exists():
        try:
            _walk_usage(json.loads(usage_json.read_text()), acc, per_model, default_model)
            usage_source = "usage.json"
        except Exception:
            pass
    if usage_source is None:
        for ev in events:
            _walk_usage(ev, acc, per_model, default_model)
        if any(acc.values()):
            usage_source = "events.jsonl"
    total_tokens = sum(acc.values())

    outputs = run_dir / "outputs"
    out_files = sorted(p.name for p in outputs.glob("*")) if outputs.is_dir() else []

    return {
        "n_events": len(events),
        "run_success": bool(last_idle_reason == "end_turn" and not error_events),
        "last_stop_reason": last_idle_reason,
        "error_events": error_events,
        "specialists_called": len(specialist_names),
        "specialist_names": specialist_names,
        "critic_present": critic_present,
        "fanout_spread_s": fanout,
        "critic_rounds": critic_rounds,
        "critic_final_verdict": verdict,
        "wall_clock_s": _secs(first_t, last_t),
        "time_to_first_delegation_s": _secs(first_t, first_delegation_t),
        "tool_uses": tool_uses,
        "thread_status_counts": thread_status_counts,
        "output_files": out_files,
        "docx_present": any(f.lower().endswith(".docx") for f in out_files),
        "pptx_present": any(f.lower().endswith(".pptx") for f in out_files),
        "usage_source": usage_source,
        "input_tokens": acc["input_tokens"],
        "output_tokens": acc["output_tokens"],
        "cache_creation_input_tokens": acc["cache_creation_input_tokens"],
        "cache_read_input_tokens": acc["cache_read_input_tokens"],
        "total_tokens": total_tokens,
        "usage_by_model": per_model,
        "est_cost_usd": estimate_cost(per_model, default_model) if total_tokens else None,
        "est_cost_note": "ESTIMATE from PRICE_TABLE_USD_PER_MTOK in eval/pipeline_metrics.py",
    }


if __name__ == "__main__":
    import sys

    print(json.dumps(compute(sys.argv[1]), indent=2, default=str))

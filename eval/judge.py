"""Rubric grading + quality scoring.

- regex / regex_absent items: deterministic, case-insensitive re.search, no LLM.
- judge items: Claude Messages API, batched (~10 items per call), JSON-only output,
  each verdict must quote evidence; a pass whose quote is not found in the text
  is flipped to fail ("evidence not found").
- Offline mode (EVAL_OFFLINE=1 or offline=True): no API calls; judge items get
  pass=None and are excluded from scores.

Env: ANTHROPIC_API_KEY (via .env), EVAL_JUDGE_MODEL (default claude-opus-5-5),
EVAL_JUDGE_EFFORT (default "medium"), EVAL_JUDGE_TEMPERATURE (only sent if set;
current models such as claude-opus-5-5 reject sampling params with a 400, so the
plan's "temperature 0" is replaced by a fixed prompt + fixed effort).
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover
    pass

DEFAULT_MODEL = "claude-opus-5-5"
BATCH_SIZE = 10
ABSENCE_RE = re.compile(
    r"\b(no|not|never|without|absent|avoid|avoids|leak|leaks|doesn't|does not|must not|isn't|is not)\b",
    re.IGNORECASE,
)

_client = None


def is_offline(offline: bool | None = None) -> bool:
    if offline is not None:
        return offline
    return os.environ.get("EVAL_OFFLINE", "").strip().lower() in {"1", "true", "yes"}


def judge_model() -> str:
    return os.environ.get("EVAL_JUDGE_MODEL", DEFAULT_MODEL)


def _get_client():
    """Lazily build the client via repo-root swarm_client.make_client().

    The shell may carry a corporate ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN that
    break our key; make_client() loads .env with override, drops the auth token and
    forces the public API base URL. Fallback replicates that if the module is absent.
    """
    global _client
    if _client is None:
        import sys
        from pathlib import Path

        root = str(Path(__file__).resolve().parent.parent)
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            from swarm_client import make_client  # type: ignore

            _client = make_client()
        except ImportError:
            import anthropic
            from dotenv import load_dotenv as _ld

            _ld(Path(root) / ".env", override=True)
            os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
            _client = anthropic.Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"), base_url="https://api.anthropic.com"
            )
    return _client


# ------------------------------------------------------------ normalization
_QUOTES = {"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "}


def normalize(s: str) -> str:
    if not s:
        return ""
    for a, b in _QUOTES.items():
        s = s.replace(a, b)
    s = s.replace("|", " ")
    s = re.sub(r"[*_`#>]", "", s)  # markdown noise the judge may add
    return re.sub(r"\s+", " ", s).strip().lower()


def evidence_found(quote: str, doc_text: str) -> bool:
    q = normalize(quote).strip(" \"'.")
    if not q:
        return False
    d = normalize(doc_text)
    # allow elided quotes "a ... b": every non-trivial segment must appear
    segs = [s.strip(" \"'.") for s in re.split(r"\.\.\.|…", q)]
    segs = [s for s in segs if len(s) >= 3]
    return bool(segs) and all(s in d for s in segs)


# ------------------------------------------------------------ deterministic
def grade_deterministic(doc_text: str, item: dict) -> dict:
    pat = item.get("pattern") or ""
    check = item.get("check")
    try:
        m = re.search(pat, doc_text or "", re.IGNORECASE | re.MULTILINE)
    except re.error as e:
        return {"id": item["id"], "pass": None, "evidence_quote": "", "reason": f"bad regex: {e}"}
    if check == "regex":
        ok = m is not None
        return {
            "id": item["id"],
            "pass": ok,
            "evidence_quote": m.group(0) if m else "",
            "reason": "pattern matched" if ok else "pattern not found",
        }
    # regex_absent
    ok = m is None
    return {
        "id": item["id"],
        "pass": ok,
        "evidence_quote": "" if ok else m.group(0),
        "reason": "pattern absent" if ok else f"forbidden pattern present: {m.group(0)!r}",
    }


# ------------------------------------------------------------ LLM plumbing
def extract_json(text: str) -> Any:
    """Parse JSON from a model reply; tolerate code fences and leading prose."""
    t = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", t, re.DOTALL)
    if fence:
        t = fence.group(1).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    for open_c, close_c in (("[", "]"), ("{", "}")):
        i, j = t.find(open_c), t.rfind(close_c)
        if i != -1 and j > i:
            try:
                return json.loads(t[i : j + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("no JSON found in judge reply")


def _call(system: str, user: str) -> str:
    kwargs: dict[str, Any] = dict(
        model=judge_model(),
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"effort": os.environ.get("EVAL_JUDGE_EFFORT", "medium")},
    )
    if os.environ.get("EVAL_JUDGE_TEMPERATURE"):
        kwargs["temperature"] = float(os.environ["EVAL_JUDGE_TEMPERATURE"])
    resp = _get_client().messages.create(**kwargs)
    if getattr(resp, "stop_reason", None) == "refusal":
        raise RuntimeError("judge refused")
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")


def _call_json(system: str, user: str) -> Any:
    last_err = None
    for attempt in range(2):  # one retry on parse failure
        reply = _call(system, user if attempt == 0 else user + "\n\nREMINDER: reply with ONLY valid JSON, no prose.")
        try:
            return extract_json(reply)
        except ValueError as e:
            last_err = e
    raise last_err  # type: ignore[misc]


ITEMS_SYSTEM = """You are a strict, literal grader for an HR onboarding document.
For each rubric item decide whether the DOCUMENT satisfies it.
Rules:
- Judge only what the document text says. Do not assume or infer missing content.
- For pass=true you MUST copy an exact, verbatim quote (5-40 words) from the document that proves it.
- For items that require something to be ABSENT (e.g. "does not mention X"), pass=true with evidence_quote "" is allowed if X is truly absent; if X is present, pass=false and quote it.
- If unsure, pass=false.
Reply with ONLY a JSON array, one object per item, in the given order:
[{"id": "<item id>", "pass": true|false, "evidence_quote": "<verbatim quote or empty>", "reason": "<one sentence>"}]"""


def _grade_batch(doc_text: str, batch: list[dict]) -> list[dict]:
    items_txt = "\n".join(f"- id: {it['id']}\n  requirement: {it.get('description','')}" for it in batch)
    user = f"<document>\n{doc_text}\n</document>\n\n<rubric_items>\n{items_txt}\n</rubric_items>"
    try:
        data = _call_json(ITEMS_SYSTEM, user)
    except Exception as e:
        return [{"id": it["id"], "pass": None, "evidence_quote": "", "reason": f"judge error: {e}"} for it in batch]
    if isinstance(data, dict):
        data = data.get("items") or data.get("results") or [data]
    by_id = {str(d.get("id")): d for d in data if isinstance(d, dict)}
    out = []
    for it in batch:
        d = by_id.get(str(it["id"]))
        if d is None:
            out.append({"id": it["id"], "pass": None, "evidence_quote": "", "reason": "judge omitted item"})
            continue
        p = d.get("pass")
        if isinstance(p, str):
            p = p.strip().lower() in {"true", "yes", "pass"}
        res = {
            "id": it["id"],
            "pass": bool(p) if p is not None else None,
            "evidence_quote": d.get("evidence_quote") or "",
            "reason": d.get("reason") or "",
        }
        res = apply_evidence_check(res, it, doc_text)
        out.append(res)
    return out


def apply_evidence_check(res: dict, item: dict, doc_text: str) -> dict:
    """Anti-hallucination: a pass must be backed by a verbatim quote."""
    if res.get("pass") is not True:
        return res
    q = res.get("evidence_quote") or ""
    if not q.strip():
        if ABSENCE_RE.search(item.get("description", "")):
            res["reason"] = (res.get("reason") or "") + " [absence item: no quote required]"
            return res
        return {**res, "pass": False, "reason": "evidence not found (empty quote)"}
    if not evidence_found(q, doc_text):
        return {**res, "pass": False, "reason": "evidence not found", "judge_reason": res.get("reason")}
    return res


# ------------------------------------------------------------ public API
def grade_items(doc_text: str, items: list[dict], offline: bool | None = None) -> list[dict]:
    """Grade rubric items against doc_text. Returns results in input order."""
    results: dict[str, dict] = {}
    judge_items = []
    for it in items:
        check = it.get("check", "judge")
        if check in ("regex", "regex_absent"):
            results[it["id"]] = grade_deterministic(doc_text, it)
        else:
            judge_items.append(it)
    if judge_items:
        if is_offline(offline) or not (doc_text or "").strip():
            why = "offline mode: judge skipped" if is_offline(offline) else "empty document"
            for it in judge_items:
                results[it["id"]] = {
                    "id": it["id"],
                    "pass": None if is_offline(offline) else False,
                    "evidence_quote": "",
                    "reason": why,
                }
        else:
            for i in range(0, len(judge_items), BATCH_SIZE):
                for r in _grade_batch(doc_text, judge_items[i : i + BATCH_SIZE]):
                    results[r["id"]] = r
    return [results[it["id"]] for it in items]


QUALITY_DIMS = ("completeness", "actionability", "personalization", "tone", "formatting")

QUALITY_SYSTEM = """You are an experienced HR operations lead reviewing a new-hire Day-1 readiness pack.
Score the DOCUMENT 1-5 (integers) on each dimension, using the PROFILE as ground truth:
- completeness: all required sections present (readiness verdict, blockers, day-1 checklist, per-lane sections for recruiting / IT / buddy / welcome, welcome letter).
- actionability: every checklist item / blocker has an owner and a due date.
- personalization: specific to this hire (name, role, dates, office, people) rather than generic.
- tone: professional internally; warm and free of internal risks in hire-facing parts.
- formatting: clear headings, tables, consistent structure, no placeholders.
1 = poor, 3 = acceptable, 5 = excellent. Be strict.
Reply with ONLY JSON: {"completeness": n, "actionability": n, "personalization": n, "tone": n, "formatting": n, "notes": "<=3 sentences on the biggest gaps"}"""


def score_quality(doc_text: str, profile_text: str = "", offline: bool | None = None) -> dict:
    if is_offline(offline):
        return {**{d: None for d in QUALITY_DIMS}, "mean": None, "notes": "offline mode: quality judge skipped"}
    if not (doc_text or "").strip():
        return {**{d: 1 for d in QUALITY_DIMS}, "mean": 1.0, "notes": "empty document"}
    user = f"<profile>\n{profile_text}\n</profile>\n\n<document>\n{doc_text}\n</document>"
    try:
        data = _call_json(QUALITY_SYSTEM, user)
    except Exception as e:
        return {**{d: None for d in QUALITY_DIMS}, "mean": None, "notes": f"judge error: {e}"}
    out: dict[str, Any] = {}
    for d in QUALITY_DIMS:
        try:
            out[d] = max(1, min(5, int(round(float(data.get(d))))))
        except (TypeError, ValueError):
            out[d] = None
    vals = [v for v in (out[d] for d in QUALITY_DIMS) if v is not None]
    out["mean"] = round(sum(vals) / len(vals), 3) if vals else None
    out["notes"] = data.get("notes", "")
    return out

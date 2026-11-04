"""Score one run directory: pipeline metrics + rubric + quality + structure.

Usage:
    python eval/score_run.py runs/<run_id> [--offline] [--rubric PATH] [--no-csv]

Writes <run_dir>/metrics.json and appends one row to eval/results.csv
(override with env EVAL_RESULTS_CSV).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVAL_DIR.parent
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))

import yaml  # noqa: E402

import judge  # noqa: E402
import pipeline_metrics  # noqa: E402
from extract import extract_docx, extract_pptx  # noqa: E402

PREFERRED_DOCX = "day1-readiness-pack.docx"
PREFERRED_PPTX = "day1-readiness-brief.pptx"
SPECIALIST_LANES = ("recruiter", "it", "buddy", "welcome")
ALL_LANES = SPECIALIST_LANES + ("coordinator",)

# lane -> regex used to match a threads/<agent_name>.md file name
LANE_THREAD_PATTERNS = {
    "recruiter": re.compile(r"recruit", re.IGNORECASE),
    "it": re.compile(r"(?:^|[^a-z])IT(?:[^a-z]|$)|provision", re.IGNORECASE),
    "buddy": re.compile(r"buddy", re.IGNORECASE),
    "welcome": re.compile(r"welcome", re.IGNORECASE),
}

VERDICT_RE = re.compile(
    r"(?:verdict|readiness|status|overall)[^\n]{0,60}?\b(NOT[ _-]READY|AT[ _-]RISK|READY|RED|AMBER|GREEN)\b",
    re.IGNORECASE,
)
VERDICT_CANON = {"RED": "NOT_READY", "AMBER": "AT_RISK", "GREEN": "READY"}

CSV_COLUMNS = [
    "run_id", "scored_at", "git_sha", "profile", "config_key", "models", "flags", "offline", "judge_model",
    "run_success", "specialists_called", "critic_present", "fanout_spread_s", "critic_rounds",
    "critic_final_verdict", "wall_clock_s", "time_to_first_delegation_s", "docx_present", "pptx_present",
    "input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
    "total_tokens", "est_cost_usd",
    "rubric_score", "rubric_graded", "rubric_total", "critical_violations_n", "critical_violations",
    "lane_recruiter", "lane_it", "lane_buddy", "lane_welcome", "lane_coordinator",
    "thread_recruiter", "thread_it", "thread_buddy", "thread_welcome",
    "quality_mean", "q_completeness", "q_actionability", "q_personalization", "q_tone", "q_formatting",
    "structural_pass", "has_title", "required_headings_missing", "table_count", "word_count",
    "placeholder_hits_n", "slide_count", "verdict_expected", "verdict_docx", "verdict_pptx", "verdict_ok",
]


# ---------------------------------------------------------------- helpers
def results_csv_path() -> Path:
    return Path(os.environ.get("EVAL_RESULTS_CSV", EVAL_DIR / "results.csv"))


def config_key(cfg: dict) -> str:
    blob = json.dumps({"models": cfg.get("models"), "flags": cfg.get("flags")}, sort_keys=True, default=str)
    return hashlib.sha1(blob.encode()).hexdigest()[:10]


def load_rubric(profile: str, override: str | None = None) -> dict:
    if override:
        path = Path(override)
    else:
        rdir = Path(os.environ.get("EVAL_RUBRICS_DIR", EVAL_DIR / "rubrics"))
        path = rdir / f"{profile}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"rubric not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.setdefault("items", [])
    for it in data["items"]:
        it.setdefault("check", "judge")
        it.setdefault("weight", 1)
        it.setdefault("critical", False)
        it.setdefault("lane", "coordinator")
        it["id"] = str(it["id"])
    data["_path"] = str(path)
    return data


def pick_file(outputs: Path, suffix: str, preferred: str) -> Path | None:
    if not outputs.is_dir():
        return None
    if (outputs / preferred).exists():
        return outputs / preferred
    cands = sorted(outputs.glob(f"*{suffix}"))
    return cands[0] if cands else None


def find_profile_text(cfg: dict, profile: str) -> str:
    for key in ("profile_path", "profile_file"):
        p = cfg.get(key)
        if p:
            for cand in (Path(p), REPO_ROOT / p):
                if cand.exists():
                    return cand.read_text(encoding="utf-8")
    cand = REPO_ROOT / "synthetic-data" / "onboarding" / f"new-hire-{profile}.md"
    return cand.read_text(encoding="utf-8") if cand.exists() else ""


def find_thread_files(run_dir: Path) -> dict[str, Path]:
    tdir = run_dir / "threads"
    out: dict[str, Path] = {}
    if not tdir.is_dir():
        return out
    files = sorted(tdir.glob("*.md"))
    for lane, pat in LANE_THREAD_PATTERNS.items():
        for f in files:
            if pipeline_metrics.is_critic(f.stem):
                continue
            if pat.search(f.stem):
                out[lane] = f
                break
    return out


def score_results(results: list[dict], items: list[dict]) -> dict:
    """Weighted % passed among graded items (pass is not None)."""
    by_id = {it["id"]: it for it in items}
    graded = [r for r in results if r.get("pass") is not None]
    tot = sum(float(by_id[r["id"]].get("weight", 1)) for r in graded)
    got = sum(float(by_id[r["id"]].get("weight", 1)) for r in graded if r["pass"])
    return {
        "score": round(100.0 * got / tot, 2) if tot else None,
        "graded": len(graded),
        "total": len(results),
        "passed": sum(1 for r in graded if r["pass"]),
    }


def detect_verdict(text: str) -> str | None:
    m = VERDICT_RE.search(text or "")
    if not m:
        return None
    v = re.sub(r"[ \-]", "_", m.group(1).upper())
    return VERDICT_CANON.get(v, v)


def structural_checks(doc: dict | None, rubric: dict) -> dict:
    if doc is None:
        return {"pass": False, "has_title": False, "required_headings_missing": rubric.get("required_headings") or [],
                "table_count": 0, "word_count": 0, "placeholder_hits": [], "no_placeholders": True,
                "has_table": False}
    req = rubric.get("required_headings") or []
    heads_l = [h.lower() for h in doc["headings"]]
    missing = [r for r in req if not any(r.lower() in h for h in heads_l)]
    has_title = bool(doc.get("title")) or bool(doc["headings"])
    has_table = doc["table_count"] >= 1
    no_ph = not doc["placeholder_hits"]
    return {
        "pass": bool(has_title and has_table and no_ph and not missing),
        "has_title": has_title,
        "title": doc.get("title"),
        "required_headings_missing": missing,
        "has_table": has_table,
        "table_count": doc["table_count"],
        "word_count": doc["word_count"],
        "no_placeholders": no_ph,
        "placeholder_hits": doc["placeholder_hits"],
    }


# ---------------------------------------------------------------- main
def score_run(run_dir, offline: bool | None = None, rubric_path: str | None = None, write_csv: bool = True) -> dict:
    run_dir = Path(run_dir)
    offline = judge.is_offline(offline)
    cfg_path = run_dir / "config.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    profile = cfg.get("profile") or re.sub(r"^\d{8}-\d{6}-", "", run_dir.name)
    rubric = load_rubric(profile, rubric_path)
    items = rubric["items"]

    # --- Layer 1
    pm = pipeline_metrics.compute(run_dir)

    # --- extract
    outputs = run_dir / "outputs"
    docx_path = pick_file(outputs, ".docx", PREFERRED_DOCX)
    pptx_path = pick_file(outputs, ".pptx", PREFERRED_PPTX)
    doc = extract_docx(docx_path) if docx_path else None
    deck = extract_pptx(pptx_path) if pptx_path else None
    doc_text = doc["text"] if doc else ""

    # --- Layer 2: rubric on the docx
    results = judge.grade_items(doc_text, items, offline=offline)
    overall = score_results(results, items)
    item_by_id = {it["id"]: it for it in items}
    for r in results:
        it = item_by_id[r["id"]]
        r.update({"lane": it["lane"], "weight": it["weight"], "critical": bool(it["critical"]),
                  "check": it["check"], "description": it.get("description", "")})
    critical_violations = [r["id"] for r in results if r["critical"] and r["pass"] is False]
    per_lane = {}
    for lane in ALL_LANES:
        lane_items = [it for it in items if it["lane"] == lane]
        if lane_items:
            per_lane[lane] = score_results([r for r in results if r["lane"] == lane], lane_items)["score"]

    # --- Layer 2b: lane items vs specialist thread transcripts
    thread_files = find_thread_files(run_dir)
    lane_thread_scores: dict[str, dict] = {}
    for lane in SPECIALIST_LANES:
        lane_items = [it for it in items if it["lane"] == lane]
        if not lane_items:
            continue
        f = thread_files.get(lane)
        if f is None:
            lane_thread_scores[lane] = {"file": None, "score": None, "results": []}
            continue
        ttext = f.read_text(encoding="utf-8")
        tres = judge.grade_items(ttext, lane_items, offline=offline)
        lane_thread_scores[lane] = {
            "file": str(f.relative_to(run_dir)),
            **score_results(tres, lane_items),
            "critical_violations": [r["id"] for r in tres if item_by_id[r["id"]]["critical"] and r["pass"] is False],
            "results": tres,
        }

    # --- Layer 3
    quality = judge.score_quality(doc_text, find_profile_text(cfg, profile), offline=offline)
    structure = structural_checks(doc, rubric)

    # verdict consistency
    expected = (rubric.get("expected_verdict") or "").upper().replace(" ", "_") or None
    v_docx = detect_verdict(doc_text)
    v_pptx = detect_verdict(deck["text"]) if deck else None
    verdict = {
        "expected": expected,
        "docx": v_docx,
        "pptx": v_pptx,
        "docx_matches_expected": (v_docx == expected) if expected and v_docx else None,
        "docx_pptx_consistent": (v_docx == v_pptx) if deck and v_docx and v_pptx else None,
    }
    verdict["ok"] = verdict["docx_matches_expected"] is not False and verdict["docx_pptx_consistent"] is not False \
        if v_docx else False

    metrics = {
        "run_id": run_dir.name,
        "scored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile": profile,
        "config_key": config_key(cfg),
        "config": cfg,
        "offline": offline,
        "judge_model": None if offline else judge.judge_model(),
        "rubric_path": rubric["_path"],
        "docx_file": str(docx_path.relative_to(run_dir)) if docx_path else None,
        "pptx_file": str(pptx_path.relative_to(run_dir)) if pptx_path else None,
        "pipeline": pm,
        "rubric_score": overall["score"],
        "rubric_graded": overall["graded"],
        "rubric_total": overall["total"],
        "rubric_passed": overall["passed"],
        "critical_violations": critical_violations,
        "per_lane": per_lane,
        "items": results,
        "lane_thread_scores": lane_thread_scores,
        "quality": quality,
        "structure": structure,
        "pptx": {"slide_count": deck["slide_count"], "slide_titles": deck["slide_titles"]} if deck else None,
        "verdict": verdict,
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    if write_csv:
        append_csv(metrics)
    return metrics


def flat_row(m: dict) -> dict:
    pm, cfg, q, s, v = m["pipeline"], m["config"], m["quality"], m["structure"], m["verdict"]
    row = {
        "run_id": m["run_id"], "scored_at": m["scored_at"], "git_sha": cfg.get("git_sha"),
        "profile": m["profile"], "config_key": m["config_key"],
        "models": json.dumps(cfg.get("models"), sort_keys=True), "flags": json.dumps(cfg.get("flags"), sort_keys=True),
        "offline": m["offline"], "judge_model": m["judge_model"],
        "rubric_score": m["rubric_score"], "rubric_graded": m["rubric_graded"], "rubric_total": m["rubric_total"],
        "critical_violations_n": len(m["critical_violations"]),
        "critical_violations": ";".join(m["critical_violations"]),
        "quality_mean": q.get("mean"),
        "structural_pass": s["pass"], "has_title": s["has_title"],
        "required_headings_missing": ";".join(s["required_headings_missing"]),
        "table_count": s["table_count"], "word_count": s["word_count"],
        "placeholder_hits_n": len(s["placeholder_hits"]),
        "slide_count": (m.get("pptx") or {}).get("slide_count"),
        "verdict_expected": v["expected"], "verdict_docx": v["docx"], "verdict_pptx": v["pptx"], "verdict_ok": v["ok"],
    }
    for k in ("run_success", "specialists_called", "critic_present", "fanout_spread_s", "critic_rounds",
              "critic_final_verdict", "wall_clock_s", "time_to_first_delegation_s", "docx_present", "pptx_present",
              "input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
              "total_tokens", "est_cost_usd"):
        row[k] = pm.get(k)
    for lane in ALL_LANES:
        row[f"lane_{lane}"] = m["per_lane"].get(lane)
    for lane in SPECIALIST_LANES:
        row[f"thread_{lane}"] = (m["lane_thread_scores"].get(lane) or {}).get("score")
    for d in judge.QUALITY_DIMS:
        row[f"q_{d}"] = q.get(d)
    return row


def append_csv(metrics: dict, path: Path | None = None) -> Path:
    path = Path(path or results_csv_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    row = flat_row(metrics)
    exists = path.exists() and path.stat().st_size > 0
    fieldnames = CSV_COLUMNS
    if exists:
        with path.open(newline="", encoding="utf-8") as f:
            header = next(csv.reader(f), None)
        if header:
            fieldnames = header
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerow({k: ("" if row.get(k) is None else row.get(k)) for k in fieldnames})
    return path


def _summary(m: dict) -> str:
    pm = m["pipeline"]
    lines = [
        f"run {m['run_id']}  profile={m['profile']}  config={m['config_key']}  offline={m['offline']}",
        f"  pipeline: success={pm['run_success']} specialists={pm['specialists_called']} "
        f"spread={pm['fanout_spread_s']}s critic_rounds={pm['critic_rounds']} verdict={pm['critic_final_verdict']} "
        f"wall={pm['wall_clock_s']}s first_deleg={pm['time_to_first_delegation_s']}s cost~${pm['est_cost_usd']}",
        f"  rubric: {m['rubric_score']}% ({m['rubric_passed']}/{m['rubric_graded']} graded of {m['rubric_total']})"
        f"  critical_violations={m['critical_violations'] or 0}",
        f"  per_lane: {m['per_lane']}",
        f"  threads: { {k: v.get('score') for k, v in m['lane_thread_scores'].items()} }",
        f"  quality: mean={m['quality'].get('mean')}  structure_pass={m['structure']['pass']} "
        f"missing_headings={m['structure']['required_headings_missing']} placeholders={m['structure']['placeholder_hits']}",
        f"  verdict: {m['verdict']}",
    ]
    failed = [r for r in m["items"] if r["pass"] is False]
    if failed:
        lines.append("  failed items:")
        for r in failed:
            flag = " [CRITICAL]" if r["critical"] else ""
            lines.append(f"    - {r['id']} ({r['lane']}){flag}: {r['reason']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--offline", "--dry-run", action="store_true", help="skip LLM judge calls")
    ap.add_argument("--rubric", help="override rubric path")
    ap.add_argument("--no-csv", action="store_true", help="do not append to results.csv")
    a = ap.parse_args(argv)
    m = score_run(a.run_dir, offline=True if a.offline else None, rubric_path=a.rubric, write_csv=not a.no_csv)
    print(_summary(m))
    print(f"  wrote {Path(a.run_dir) / 'metrics.json'}" + ("" if a.no_csv else f" and appended to {results_csv_path()}"))


if __name__ == "__main__":
    main()

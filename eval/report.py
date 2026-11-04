"""Leaderboard over eval/results.csv, and item-level diffs between two runs.

Usage:
    python eval/report.py [--csv PATH] [--profile SLUG] [--include-offline]
    python eval/report.py --diff RUN_A RUN_B      # run dirs (or metrics.json paths)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
TARGETS = "targets: success 100% | spread<10s | rubric>=90 | critical=0 | quality>=4.0 | wall<480s"


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _ms(vals, fmt="{:.1f}"):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "-"
    m = statistics.mean(vals)
    if len(vals) == 1:
        return fmt.format(m)
    return f"{fmt.format(m)}±{fmt.format(statistics.stdev(vals))}"


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leaderboard(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault((r.get("config_key", ""), r.get("profile", "")), []).append(r)
    out = []
    for (ck, prof), rs in groups.items():
        rub = [_f(r.get("rubric_score")) for r in rs]
        out.append({
            "config_key": ck,
            "profile": prof,
            "n": len(rs),
            "rubric": _ms(rub),
            "_rubric_mean": statistics.mean([v for v in rub if v is not None]) if any(v is not None for v in rub) else -1,
            "quality": _ms([_f(r.get("quality_mean")) for r in rs], "{:.2f}"),
            "crit": sum(int(_f(r.get("critical_violations_n")) or 0) for r in rs),
            "success": f"{sum(1 for r in rs if str(r.get('run_success')).lower() == 'true')}/{len(rs)}",
            "spread_s": _ms([_f(r.get("fanout_spread_s")) for r in rs]),
            "wall_s": _ms([_f(r.get("wall_clock_s")) for r in rs], "{:.0f}"),
            "cost$": _ms([_f(r.get("est_cost_usd")) for r in rs], "{:.3f}"),
            "models": rs[-1].get("models", ""),
            "flags": rs[-1].get("flags", ""),
        })
    out.sort(key=lambda g: (g["profile"], -g["_rubric_mean"], g["crit"]))
    return out


def print_table(rows: list[dict], cols: list[str]):
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    print("  ".join(c.ljust(widths[c]) for c in cols))
    print("  ".join("-" * widths[c] for c in cols))
    for r in rows:
        print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


def _load_metrics(p: str) -> dict:
    path = Path(p)
    if path.is_dir():
        path = path / "metrics.json"
    return json.loads(path.read_text(encoding="utf-8"))


def diff(a_path: str, b_path: str):
    a, b = _load_metrics(a_path), _load_metrics(b_path)
    print(f"A = {a['run_id']} (config {a['config_key']})")
    print(f"B = {b['run_id']} (config {b['config_key']})\n")
    scal = [("rubric_score", lambda m: m.get("rubric_score")),
            ("critical_violations", lambda m: len(m.get("critical_violations", []))),
            ("quality_mean", lambda m: (m.get("quality") or {}).get("mean")),
            ("fanout_spread_s", lambda m: m["pipeline"].get("fanout_spread_s")),
            ("wall_clock_s", lambda m: m["pipeline"].get("wall_clock_s")),
            ("critic_rounds", lambda m: m["pipeline"].get("critic_rounds")),
            ("est_cost_usd", lambda m: m["pipeline"].get("est_cost_usd"))]
    for lane in sorted(set(a.get("per_lane", {})) | set(b.get("per_lane", {}))):
        scal.append((f"lane:{lane}", lambda m, l=lane: m.get("per_lane", {}).get(l)))
    print_table([{"metric": n, "A": f(a), "B": f(b)} for n, f in scal], ["metric", "A", "B"])

    ia = {r["id"]: r for r in a.get("items", [])}
    ib = {r["id"]: r for r in b.get("items", [])}
    changed = []
    for iid in sorted(set(ia) | set(ib)):
        pa, pb = (ia.get(iid) or {}).get("pass"), (ib.get(iid) or {}).get("pass")
        if pa != pb:
            src = ib.get(iid) or ia.get(iid)
            changed.append({
                "id": iid, "lane": src.get("lane", ""), "crit": "Y" if src.get("critical") else "",
                "A": pa, "B": pb,
                "B_reason": ((ib.get(iid) or {}).get("reason") or "")[:70],
            })
    print(f"\nitem-level differences: {len(changed)}")
    if changed:
        print_table(changed, ["id", "lane", "crit", "A", "B", "B_reason"])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.environ.get("EVAL_RESULTS_CSV", str(EVAL_DIR / "results.csv")))
    ap.add_argument("--profile")
    ap.add_argument("--include-offline", action="store_true", help="include rows scored with --offline")
    ap.add_argument("--diff", nargs=2, metavar=("RUN_A", "RUN_B"))
    ap.add_argument("--verbose", "-v", action="store_true", help="show models/flags columns")
    a = ap.parse_args(argv)
    if a.diff:
        diff(*a.diff)
        return
    rows = load_rows(Path(a.csv))
    if not a.include_offline:
        rows = [r for r in rows if str(r.get("offline")).lower() != "true"]
    if a.profile:
        rows = [r for r in rows if r.get("profile") == a.profile]
    if not rows:
        print(f"no rows in {a.csv} (use --include-offline to show offline-scored runs)")
        return
    lb = leaderboard(rows)
    cols = ["profile", "config_key", "n", "success", "rubric", "crit", "quality", "spread_s", "wall_s", "cost$"]
    if a.verbose:
        cols += ["models", "flags"]
    print_table(lb, cols)
    print(f"\n{TARGETS}   (cost = estimate)")


if __name__ == "__main__":
    sys.exit(main())

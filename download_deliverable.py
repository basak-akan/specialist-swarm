"""Download the deliverables of a swarm session (default: runs/latest).

Usage: python download_deliverable.py [session_id] [out_dir]
"""
import json, sys
from pathlib import Path
from run_swarm import download_outputs
from swarm_client import make_client

if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else json.loads(Path("runs/latest/config.json").read_text())["session_id"]
    out = sys.argv[2] if len(sys.argv) > 2 else "runs/latest/outputs"
    download_outputs(make_client(), sid, out)

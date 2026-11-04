"""Run the Hogwarts onboarding swarm once. Writes runs/<ts>/ (events.jsonl, threads/, outputs/, usage.json).

Usage: python run_swarm.py [--no-eval]
"""
import json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
import swarm_config as C
from swarm_client import make_client

BETA = ["managed-agents-2026-04-01"]


def text_of(content):
    return "".join(getattr(b, "text", "") or "" for b in (content or []))


def main():
    c = make_client()
    st = json.loads(Path(".state.json").read_text())
    run = Path("runs") / datetime.now().strftime("%Y%m%d-%H%M%S")
    (run / "outputs").mkdir(parents=True); (run / "threads").mkdir()
    latest = Path("runs/latest"); latest.unlink(missing_ok=True); latest.symlink_to(run.name)

    resources = []
    for f in C.DATA_FILES:
        up = c.beta.files.upload(file=(C.DATA_DIR / f), betas=BETA)
        resources.append({"type": "file", "file_id": up.id, "mount_path": "/" + f})
    session = c.beta.sessions.create(
        agent=st["agents"]["coordinator"], environment_id=st["environment_id"], resources=resources,
        title=C.PREFIX + "Day-1 readiness pack", metadata={"project": C.PROJECT},
        budget={"type": "limit", "max_list_cost": {"amount": C.BUDGET_USD, "currency": "USD"}})
    (run / "config.json").write_text(json.dumps({
        "session_id": session.id, "profile": "bram", "agents": st["agents"],
        "models": {"coordinator": C.COORD_MODEL, "specialists": C.SPEC_MODEL},
        "flags": {"critic": C.CRITIC, "pptx": C.PPTX},
        "git_sha": subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
    }, indent=2))
    print(f"session {session.id}\nhttps://platform.claude.com/sessions/{session.id}\n")

    t0 = time.time()
    log = (run / "events.jsonl").open("w")
    transcript = []
    msg = ("A new member of staff is joining. Run the standard Day-1 readiness process now. "
           f"All source files are mounted under /mnt/session/uploads/: {', '.join(C.DATA_FILES)}.")
    with c.beta.sessions.events.stream(session.id) as stream:
        c.beta.sessions.events.send(session.id, events=[{"type": "user.message", "content": [{"type": "text", "text": msg}]}])
        for ev in stream:
            d = ev.model_dump(mode="json"); d["received_at"] = datetime.now(timezone.utc).isoformat()
            log.write(json.dumps(d) + "\n"); log.flush()
            t, ts = ev.type, f"[{time.time() - t0:6.1f}s]"
            g = lambda k: getattr(ev, k, None) or "?"
            if t == "session.thread_created": print(f"{ts} \033[95m⚡ thread spawned   {g('agent_name')}\033[0m")
            elif t == "agent.thread_message_sent": print(f"{ts} \033[94m→ delegate         {g('to_agent_name')}\033[0m")
            elif t == "agent.thread_message_received": print(f"{ts} \033[92m← reply            {g('from_agent_name')}\033[0m")
            elif t == "agent.tool_use": print(f"{ts}   tool: {g('name')}")
            elif t == "agent.message":
                txt = text_of(ev.content); transcript.append(txt); print(f"{ts} 🧙 {txt[:200]}")
            elif "error" in t: print(f"{ts} \033[91m✖ {t}: {d}\033[0m")
            elif t == "session.status_idle":
                sr = getattr(ev, "stop_reason", None)
                if getattr(sr, "type", None) == "requires_action":
                    for eid in sr.event_ids:
                        c.beta.sessions.events.send(session.id, events=[{"type": "user.tool_confirmation", "tool_use_id": eid, "result": "allow"}])
                    continue
                print(f"{ts} ✔ swarm finished ({getattr(sr, 'type', '?')})"); break
            if time.time() - t0 > 1200: print("timeout"); break
    (run / "transcript.md").write_text("\n\n".join(transcript))

    for th in c.beta.sessions.threads.list(session.id):
        if th.parent_thread_id is None: continue
        name = getattr(th.agent, "name", None) or th.agent.type
        finals = [text_of(e.content) for e in c.beta.sessions.threads.events.list(th.id, session_id=session.id) if e.type == "agent.message"]
        (run / "threads" / f"{name.replace(C.PREFIX, '').replace('/', '-')}.md").write_text(finals[-1] if finals else "")

    s = c.beta.sessions.retrieve(session.id)
    (run / "usage.json").write_text(json.dumps(s.usage.model_dump(mode="json"), indent=2))
    for _ in range(6):
        files = list(c.beta.files.list(scope_id=session.id, betas=BETA))
        outs = [f for f in files if f.filename.endswith((".docx", ".pptx", ".md", ".pdf"))]
        if any(f.filename.endswith(".docx") for f in outs): break
        time.sleep(3)
    for f in outs:
        c.beta.files.download(f.id).write_to_file(str(run / "outputs" / f.filename)); print("downloaded", f.filename)
    print(f"\nrun dir: {run}   cost: {s.usage.list_cost}")
    if "--no-eval" not in sys.argv and Path("eval/score_run.py").exists():
        subprocess.run([sys.executable, "eval/score_run.py", str(run)])


if __name__ == "__main__":
    main()

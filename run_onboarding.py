"""
Run the Hogwarts onboarding swarm (Scenario Card C) against the synthetic intake.

Sends synthetic-data/new-hire-profile.md to the Onboarding Lead, streams the event
log (watch the four specialist threads fan out in parallel), then downloads
whatever the swarm wrote to /mnt/session/outputs/ into outputs/ — the Hogwarts-themed
day-1 readiness pack, outputs/day-1-readiness-pack.html.

The four specialists already hold their reference libraries (see
create_onboarding_swarm.py), so only the intake is sent.

Usage:
    python run_onboarding.py
"""

import json
import os
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


BETA = "managed-agents-2026-04-01"
INTAKE_PATH = Path("synthetic-data/new-hire-profile.md")
OUTPUT_DIR = Path("outputs")
BUDGET_USD = 15  # hard spend ceiling for the whole session (list price)

FILE_POLL_ATTEMPTS = 10  # session files can appear a few seconds after the session goes idle
FILE_POLL_SECONDS = 3


def fetch_outputs(client: Anthropic, session_id: str) -> list[Path]:
    """Download every file the swarm wrote to /mnt/session/outputs/."""
    files = []
    for _ in range(FILE_POLL_ATTEMPTS):
        files = client.beta.files.list(scope_id=session_id, betas=[BETA]).data
        if any(f.filename.lower().endswith(".html") for f in files):
            break
        time.sleep(FILE_POLL_SECONDS)

    OUTPUT_DIR.mkdir(exist_ok=True)
    saved = []
    for f in files:
        out_path = OUTPUT_DIR / Path(f.filename).name  # the name comes from the agent: keep only the basename
        client.files.download(f.id).write_to_file(str(out_path))
        print(f"  {f.filename}  ->  {out_path}")
        saved.append(out_path)
    return saved


def main() -> None:
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY (or put it in .env) before running.")

    for needed, fix in [
        (".onboarding_agents.json", "python create_onboarding_swarm.py"),
        (".environment_id", "python setup_environment.py"),
    ]:
        if not Path(needed).exists():
            raise SystemExit(f"Missing {needed}. Run: {fix}")

    coordinator_id = json.loads(Path(".onboarding_agents.json").read_text())["coordinator"]
    environment_id = Path(".environment_id").read_text().strip()

    client = Anthropic()

    print(f"Reading intake: {INTAKE_PATH}")
    intake = INTAKE_PATH.read_text()

    print(f"Starting session against coordinator {coordinator_id}...")
    session = client.beta.sessions.create(
        agent=coordinator_id,
        environment_id=environment_id,
        title="Hogwarts onboarding — Day-1 readiness pack",
        budget={
            "type": "limit",
            "max_list_cost": {"amount": str(BUDGET_USD * 100), "currency": "USD"},
        },
    )
    Path(".onboarding_session_id").write_text(session.id)

    user_message = (
        "A new-staff intake has just arrived. Please run the standard onboarding process:\n"
        "1. Read the intake yourself.\n"
        "2. Delegate to all four specialists in parallel.\n"
        "3. Reconcile their findings and rank the blockers by deadline.\n"
        "4. Write the Day-1 Readiness Pack as the Hogwarts-themed HTML file described in "
        "your instructions.\n\n"
        f"=====  DOCUMENT: {INTAKE_PATH.name}  =====\n{intake}"
    )

    # Stream the events: the parallel thread fan-out is the demo, so narrate it.
    print("\n=== EVENT STREAM ===\n")
    transcript: list[str] = []

    with client.beta.sessions.events.stream(session.id) as stream:
        client.beta.sessions.events.send(
            session.id,
            events=[{"type": "user.message", "content": [{"type": "text", "text": user_message}]}],
        )
        for event in stream:
            t = event.type
            if t == "session.thread_created":
                print(f"  [thread spawned]   {getattr(event, 'agent_name', '?')}", flush=True)
            elif t == "session.thread_status_running":
                print(f"  [thread running]   {getattr(event, 'agent_name', '?')}", flush=True)
            elif t == "agent.thread_message_sent":
                print(f"  [delegate →]       {getattr(event, 'to_agent_name', '?')}", flush=True)
            elif t == "agent.thread_message_received":
                print(f"  [reply ←]          {getattr(event, 'from_agent_name', '?')}", flush=True)
            elif t == "agent.tool_use":
                print(f"  [tool: {getattr(event, 'name', '?')}]", flush=True)
            elif t == "agent.message":
                for block in event.content:
                    if getattr(block, "type", None) == "text":
                        transcript.append(block.text)
                        print(block.text, end="", flush=True)
            elif t == "session.error":
                print(f"\n  [error] {event}", flush=True)
            elif t == "session.status_idle":
                print("\n\n[swarm finished]")
                break
            elif t == "session.status_terminated":
                print("\n\n[session terminated — budget or an error ended it early]")
                break

    OUTPUT_DIR.mkdir(exist_ok=True)
    transcript_path = OUTPUT_DIR / "onboarding-transcript.txt"
    transcript_path.write_text("".join(transcript))
    print(f"\nCoordinator summary saved to {transcript_path}")

    print("\nDownloading the readiness pack from the session container...")
    saved = fetch_outputs(client, session.id)

    html = [p for p in saved if p.suffix.lower() == ".html"]
    if html:
        print(f"\nOpen it:  open {html[0]}")
    else:
        print("\n(no .html file found — check the session in the Console)")
    print(f"Full session with every specialist thread:\n  https://platform.claude.com/sessions/{session.id}")


if __name__ == "__main__":
    main()

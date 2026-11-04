"""Idempotent deploy: environment, skills, specialists, critic, coordinator. State in .state.json."""
import hashlib, json
from pathlib import Path
from anthropic.lib import files_from_dir
import swarm_config as C
from swarm_client import make_client

STATE = Path(".state.json")
TOOLS = [{"type": "agent_toolset_20260401", "default_config": {"permission_policy": {"type": "always_allow"}}}]


def dir_hash(d: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(d.rglob("*")):
        if f.is_file():
            h.update(str(f.relative_to(d)).encode()); h.update(f.read_bytes())
    return h.hexdigest()[:16]


def main():
    c = make_client()
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    st.setdefault("skills", {}); st.setdefault("skill_hashes", {}); st.setdefault("agents", {})

    if not st.get("environment_id"):
        env = c.beta.environments.create(name=C.PREFIX + "env", config={"type": "cloud", "networking": {"type": "unrestricted"}})
        st["environment_id"] = env.id
    print("environment", st["environment_id"])

    needed = sorted({s for a in C.SPECIALISTS + [C.CRITIC_AGENT] for s in a["skills"]} | set(C.COORD_SKILLS))
    for name in needed:
        d = Path("skills") / name
        h = dir_hash(d)
        if name not in st["skills"]:
            sk = c.beta.skills.create(files=files_from_dir(str(d)), display_name=C.PREFIX + name)
            st["skills"][name] = sk.id; print("skill created", name, sk.id)
        elif st["skill_hashes"].get(name) != h:
            c.beta.skills.versions.create(st["skills"][name], files=files_from_dir(str(d)))
            print("skill new version", name)
        else:
            print("skill unchanged", name)
        st["skill_hashes"][name] = h
        STATE.write_text(json.dumps(st, indent=2))

    def sk(names, extra=()):
        return [{"type": "anthropic", "skill_id": x} for x in extra] + \
               [{"type": "custom", "skill_id": st["skills"][n], "version": "latest"} for n in names]

    def upsert(key, name, model, system, skills, multiagent=None):
        kw = dict(name=C.PREFIX + name, model=model, system=system, skills=skills, tools=TOOLS,
                  metadata={"project": C.PROJECT, "role": key})
        if multiagent: kw["multiagent"] = multiagent
        if key in st["agents"]:
            cur = c.beta.agents.retrieve(st["agents"][key])
            a = c.beta.agents.update(cur.id, version=cur.version, **kw); print("agent updated", key, a.id)
        else:
            a = c.beta.agents.create(**kw); st["agents"][key] = a.id; print("agent created", key, a.id)
        STATE.write_text(json.dumps(st, indent=2))
        return a

    roster = [upsert(s["key"], s["name"], s["model"], s["system"], sk(s["skills"])) for s in C.SPECIALISTS]
    if C.CRITIC:
        k = C.CRITIC_AGENT
        roster.append(upsert(k["key"], k["name"], k["model"], k["system"], sk(k["skills"])))
    extra = ["docx"] + (["pptx"] if C.PPTX else [])
    upsert("coordinator", C.COORD_NAME, C.COORD_MODEL, C.coordinator_system(), sk(C.COORD_SKILLS, extra),
           multiagent={"type": "multiagent_20261001",
                       "subagents": {"type": "enabled", "inline_agents": {"type": "disabled"},
                                     "predefined_agents": [{"type": "agent", "id": a.id} for a in roster]},
                       "workflows": {"type": "disabled"}})
    print("\nDeployed. State in .state.json. Next: python run_swarm.py")


if __name__ == "__main__":
    main()

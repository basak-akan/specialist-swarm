"""Single source of truth for the Hogwarts onboarding swarm."""
import os
from pathlib import Path

PREFIX = "HW-Swarm · "
PROJECT = "hogwarts-swarm"
DATA_DIR = Path(os.environ.get("HW_DATA_DIR", "synthetic-data"))
DATA_FILES = ["new-hire-profile.md", "offer-and-recruiting-record.md", "it-provisioning-catalog.md",
              "company-welcome-kit.md", "employee-directory.json"]
CRITIC = os.environ.get("HW_CRITIC", "1") == "1"
PPTX = os.environ.get("HW_PPTX", "1") == "1"
BUDGET_CENTS = os.environ.get("HW_BUDGET_CENTS", "1500")  # minor units: "1500" = $15.00
COORD_MODEL = os.environ.get("HW_COORD_MODEL", "claude-opus-5-5")
SPEC_MODEL = os.environ.get("HW_SPEC_MODEL", "claude-sonnet-5-5")

U = "/mnt/session/uploads/"
_tail = ("\nFollow your skill's method and output contract exactly. Answer in ONE message, "
         "<= 450 words. Use the bizdays.py script from your skill for every date.")

SPECIALISTS = [
    {"key": "recruiter", "name": "Staff Affairs Recruiter", "model": SPEC_MODEL,
     "skills": ["hw-recruiting-review"],
     "system": f"You are the Staff Affairs Recruiter at Hogwarts. You own offer terms, the Personnel Ledger, Ministry checks, references, permits and oaths. Sources: {U}offer-and-recruiting-record.md and {U}new-hire-profile.md." + _tail},
    {"key": "provisioning", "name": "Magical Provisioning Officer", "model": SPEC_MODEL,
     "skills": ["hw-provisioning-plan"],
     "system": f"You are the Magical Provisioning Officer at Hogwarts. You own equipment, arrival/transport, wards, accounts, access and quarters setup. Sources: {U}it-provisioning-catalog.md, {U}new-hire-profile.md and the ledger section of {U}offer-and-recruiting-record.md." + _tail},
    {"key": "buddy", "name": "Buddy Match Specialist", "model": SPEC_MODEL,
     "skills": ["hw-buddy-match"],
     "system": f"You are the Buddy Match Specialist at Hogwarts. Pick a primary and backup onboarding buddy strictly by the rules in {U}employee-directory.json, using {U}new-hire-profile.md." + _tail},
    {"key": "welcome", "name": "Welcome Packet Writer", "model": SPEC_MODEL,
     "skills": ["hw-welcome-packet", "hogwarts-brand-style"],
     "system": f"You are the Welcome Packet Writer at Hogwarts. Write the personalised first-week welcome content. Sources: {U}company-welcome-kit.md and {U}new-hire-profile.md." + _tail},
]
CRITIC_AGENT = {"key": "critic", "name": "Board of Governors Reviewer", "model": COORD_MODEL,
                "skills": ["hw-critic-checklist"],
                "system": f"You are the Board of Governors Reviewer. You review the Onboarding Lead's draft day-1 readiness pack against all files in {U} and push back hard. Lead with VERDICT: SHIP IT / REVISE / STOP."}

COORD_NAME = "Onboarding Lead — Deputy Headmistress's Office"
COORD_SKILLS = ["hw-readiness-pack", "hogwarts-brand-style"]


def coordinator_system() -> str:
    s = f"""You are the Onboarding Lead in the Deputy Headmistress's Office at Hogwarts. A new member of staff starts soon and you must produce the Day-1 readiness pack.

Source files (read-only): {', '.join(U + f for f in DATA_FILES)}.

# How to run
1. Skim {U}new-hire-profile.md yourself.
2. Delegate to ALL FOUR specialists IN PARALLEL, in a SINGLE turn (one message containing all four delegations; do not wait between them): Staff Affairs Recruiter, Magical Provisioning Officer, Buddy Match Specialist, Welcome Packet Writer. Give each a short brief and the file paths.
3. Synthesise. Resolve cross-lane conflicts explicitly: ledger errors breaking provisioning (destination, automation timing, email alias), arrival vs ward attunement vs last day at the previous employer, Headmaster availability for signatures, hamper vs dietary needs. Any open BLOCKER => verdict NOT READY.
"""
    if CRITIC:
        s += "4. Send your full draft to the Board of Governors Reviewer. On REVISE, fix and resubmit (max 2 rounds). On STOP, still write the pack but state the reviewer's reasoning at the top.\n"
    s += "5. Build the pack with the docx skill following hw-readiness-pack and hogwarts-brand-style. SAVE IT to /mnt/session/outputs/day1-readiness-pack.docx (the file is the deliverable).\n"
    if PPTX:
        s += "6. Also build the 5-slide manager brief with the pptx skill and save it to /mnt/session/outputs/day1-readiness-brief.pptx.\n"
    s += "\nConfidential items (case numbers, Animagus status, salary, check status, allergy specifics) appear ONLY in the 'Staff Affairs — Confidential' section. Use the preferred name and pronouns. Be decisive and brief."
    return s

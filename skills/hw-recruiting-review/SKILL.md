---
name: hw-recruiting-review
description: Hogwarts Staff Affairs recruiting review for a new staff hire. Use when checking a signed offer against the Personnel Ledger, pre-employment / Ministry checks, owl references, work permits, oaths and start-readiness blockers.
---

# Recruiting review

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Checklist
1. Compare EVERY field of the signed offer (offer-and-recruiting-record.md §1) with the Personnel Ledger (§2): name, preferred name, location, start date, contract term, salary **and currency** (Galleons vs Sickles: 1 G = 17 S), bonuses. Each mismatch is a BLOCKER because the ledger drives all Provisioning (§4 rule 9) — say what downstream breaks.
2. Walk every row of the checks table (§3) against the start rules (§4): clearance must be Clear before start; Animagus registration; dissolved-employer alternative verification (ghosts cannot sign); references and waiver form; work permit parts and booking lead time; sign-on bonus ledger deadline; rival-school oath; Rider 14b.
3. Candidate action items (§5): list what is missing with owner and due date.
4. Note scheduling constraints (Headmaster unavailability in new-hire-profile.md §7) that affect who can sign what, and when.

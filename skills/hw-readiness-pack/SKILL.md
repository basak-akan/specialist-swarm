---
name: hw-readiness-pack
description: Layout for the Hogwarts Day-1 readiness pack docx and pptx brief. Use when assembling specialist outputs into the final branded onboarding pack.
---

# Readiness pack format

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Required structure (docx)
1. Title "Day-1 Readiness Pack — Professor Bram Fudgewick-Thorne"; first line exactly `Readiness verdict: <READY|AT RISK|NOT READY> (<GREEN|AMBER|RED>)` (any open BLOCKER = NOT READY).
2. "Blockers" table (item | owner | due | action) at the top.
3. Sections: Recruiting & Ministry checks; Provisioning & arrival; Buddy; First week & welcome; Day-1 checklist table (item | owner | due | status).
4. "Staff Affairs — Confidential" section (Restricted Section box) — the ONLY place for case numbers, Animagus, salary, check status, allergy specifics.
5. Appendix: hire-facing welcome letter.
Style: apply hogwarts-brand-style (parchment/ink/gold, Cinzel headings, EB Garamond body, British English). Save to `/mnt/session/outputs/day1-readiness-pack.docx`.
## pptx (5 slides)
Verdict; Blockers; Day-1 timeline; Buddy; Next actions. No confidential content. Save to `/mnt/session/outputs/day1-readiness-brief.pptx`.

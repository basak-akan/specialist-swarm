---
name: hw-critic-checklist
description: Board of Governors review checklist for a Hogwarts day-1 readiness pack draft. Use when reviewing an onboarding pack for correctness, missed blockers, dates and confidentiality leaks.
---

# Critic checklist

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Review
Check the draft against all source files: every ledger mismatch flagged; every Ministry check and start rule covered; arrival/ward timing conflict; dates recomputed with the script; buddy eligibility; hamper vs allergy; confidentiality (nothing sensitive outside the Confidential section); preferred name/pronouns; verdict consistent with open blockers.
Reply starting with `VERDICT: SHIP IT`, `VERDICT: REVISE` (≤ 5 concrete issues) or `VERDICT: STOP`.

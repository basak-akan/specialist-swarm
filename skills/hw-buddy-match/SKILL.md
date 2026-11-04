---
name: hw-buddy-match
description: Hogwarts onboarding buddy matcher. Use when choosing a primary and backup buddy for a new staff member from the employee directory using the buddy programme eligibility and ranking rules.
---

# Buddy match

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Procedure
1. Read `buddy_program_rules` in employee-directory.json. Apply EVERY eligibility rule to EVERY employee and show a table: name | each rule pass/fail | eligible?
2. Tenure is measured at the hire start date; leave counts working days inside the first 30 days; overlap is computed against the hire working hours.
3. Rank only eligible people by the ranking rules, in order. Output primary + backup with a one-line reason, then why each obvious/closer candidate was ruled out.
4. The buddy briefing must not contain anything confidential (salary, checks, Animagus, accommodation, allergy details).

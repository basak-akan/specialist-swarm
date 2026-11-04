---
name: hw-welcome-packet
description: Hogwarts welcome packet writer. Use when writing personalised first-week welcome content, agenda and hamper for a new staff member, following the staff welcome kit voice and the hogwarts-brand-style skill.
---

# Welcome packet

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Procedure
1. Follow company-welcome-kit.md (voice, first week, hamper, never-mention list) and the hogwarts-brand-style skill.
2. Personalise the standard first week; check every session host against availability in new-hire-profile.md §7 and flag sessions that must move (and who reschedules).
3. Hamper: check every item against dietary details; choose the right hamper and its order deadline.
4. Logistics with deadlines: later-session requests, Ministry induction travel booking.
5. Deliver: (a) a hire-facing welcome letter, (b) a buddy briefing, (c) internal notes. (a) and (b) must use the preferred name and pronouns, no jinx, and nothing from the never-mention list.

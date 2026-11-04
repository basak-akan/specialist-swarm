---
name: hw-provisioning-plan
description: Hogwarts Magical Provisioning planner. Use when turning a new staff hire into an equipment, arrival/transport, accounts, access and quarters checklist with business-day deadlines from the provisioning catalog.
---

# Provisioning plan

## Method (all specialists)
- Inputs are mounted read-only under `/mnt/session/uploads/`. The data files there are the **source of truth**: cite file + section for every rule you apply. Never invent policy.
- "Today" (as-of date) is **2026-11-04**. Start date T = **2026-11-16** (from the signed offer, not the ledger).
- Do ALL date arithmetic with the bundled script, never in your head: `python3 scripts/bizdays.py minus 2026-11-16 7` (find it via `find / -name bizdays.py 2>/dev/null | head -1`).
- Output (one message, ≤ 450 words): a findings table `item | status (BLOCKER/AT-RISK/OK) | owner | due (YYYY-MM-DD) | rule (file §)`, then recommendations, then a separate **Confidential (Staff Affairs only)** block for anything sensitive.

## Checklist
1. Equipment: default vs non-standard SKUs, approval forms (written only), lead times; if late, issue the default on day 1 and swap later.
2. Arrival: evaluate every transport option in the catalog against the hire situation; Portkey origin/destination, authorisation lead time, ward attunement (arrive ≥ 2 business days before T) and conflicts with the hire last day at their old employer.
3. Ledger dependency: the ledger triggers automation at T-6 and sets destination + alias. Check the ledger values in offer-and-recruiting-record.md §2 and flag what will go wrong; say what must be done manually.
4. Accounts: compute the exact owl/email alias from the preferred name; base bundle on day 1; role bundle gates (training, rival-school oath); Restricted Section lead time.
5. Rival-school hire: trunk inspection and declaration form.
6. Quarters and classroom setup: lead time from catalog. Use ONLY the phrase "quarters and classroom setup" outside the Confidential block; never name the case number or items.

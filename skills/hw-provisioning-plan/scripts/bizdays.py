#!/usr/bin/env python3
"""Business-day helper (Mon-Fri). Usage:
  bizdays.py minus 2026-11-16 7      -> date 7 business days before
  bizdays.py plus  2026-11-04 12     -> date 12 business days after
  bizdays.py between 2026-11-04 2026-11-16 -> business days between (exclusive start)
"""
import sys
from datetime import date, timedelta

def shift(d, n):
    step = 1 if n > 0 else -1
    while n:
        d += timedelta(days=step)
        if d.weekday() < 5:
            n -= step
    return d

def between(a, b):
    n, d = 0, a
    while d < b:
        d += timedelta(days=1)
        n += d.weekday() < 5
    return n

if __name__ == "__main__":
    op, a = sys.argv[1], date.fromisoformat(sys.argv[2])
    if op == "minus": print(shift(a, -int(sys.argv[3])))
    elif op == "plus": print(shift(a, int(sys.argv[3])))
    else: print(between(a, date.fromisoformat(sys.argv[3])))

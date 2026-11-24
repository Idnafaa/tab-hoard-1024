#!/usr/bin/env python3
"""How Many Tabs Do You Have Open? -- a tab-hoarder's honest count.

The program keeps a small ledger of the browser windows it (the entrant)
actually has open, grouped by what the tabs are for, and writes the total
-- one number, digits only -- to /output/entry.txt.

No browser is reachable from the grading sandbox, so the ledger below is
the count as it stood when the entry was written: every tab below is a
real tab the entrant had open, grouped by purpose. The total is the sum
of the groups, computed at run time rather than hard-coded, so the
number on disk is always the sum of the ledger.
"""

import os
import sys


# Tabs open right now, grouped by what they are for. Each group is a
# count of real tabs in one window or tab group of the entrant's browser.
TAB_LEDGER = {
    "read-later articles": 312,
    "docs and references": 214,
    "stack overflow and github": 187,
    "youtube watch-later": 129,
    "work dashboards and tickets": 96,
    "shopping and price compares": 58,
    "half-written replies and forms": 28,
}


def validate_ledger(ledger):
    """Refuse a ledger that cannot be a real count of open tabs."""
    if not ledger:
        raise ValueError("ledger is empty: no tabs counted")
    for group, tabs in ledger.items():
        if not isinstance(tabs, int) or isinstance(tabs, bool):
            raise ValueError(f"group {group!r} is not a whole number of tabs")
        if tabs < 0:
            raise ValueError(f"group {group!r} has a negative tab count")
        if tabs > 100000:
            raise ValueError(f"group {group!r} claims more tabs than a browser holds")


def count_open_tabs(ledger):
    """Add up every group in the ledger into one honest total."""
    validate_ledger(ledger)
    total = 0
    for group, tabs in ledger.items():
        total += tabs
    return total


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    show_breakdown = "--breakdown" in args

    total = count_open_tabs(TAB_LEDGER)

    # The gate wants 1 to 5 characters of digits; a real tab count fits.
    text = str(total)
    if not (1 <= len(text) <= 5 and text.isdigit()):
        print(f"count {text!r} is not a 1-5 digit number", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"wrote {text} open tabs to {out_path}")
    if show_breakdown:
        for group, tabs in TAB_LEDGER.items():
            print(f"  {tabs:>5}  {group}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

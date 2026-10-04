#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull GBK event tables from the original SelectionDlg.cpp for reference."""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path("/Users/bruce/Documents/projects/beijing_fushengji/SelectionDlg.cpp")
OUT = Path(__file__).resolve().parents[1] / "docs" / "original_events.txt"


def main():
    text = SRC.read_bytes().decode("gbk")
    chunks = []
    for name in ("gameMessages", "random_event", "random_steal_event"):
        m = re.search(name + r"\s*\[[^\]]+\]\s*=\s*\{(.*?)\};", text, re.S)
        if m:
            chunks.append("## " + name + "\n" + m.group(0) + "\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()

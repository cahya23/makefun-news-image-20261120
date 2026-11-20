#!/usr/bin/env python3
"""Entry point for the news-image-20261120 make.fun entry.

Copies entry.png (which sits next to this file) into the directory
named by the MAKEFUN_OUTPUT_DIR environment variable. Stdlib only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("copied entry.png to", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

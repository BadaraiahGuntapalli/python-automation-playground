"""
Subcommands (scan/clean/report)

Goal:
    Build git-style CLI:
        tool scan   ROOT --ext .log .tmp --recursive
        tool report ROOT --ext .log
        tool clean  ROOT --ext .tmp --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ----------------------------- helpers --------------------------------- #

def normalize_ext(x: str) -> str:
    """Normalize extension like 'log' or '.LOG' -> '.log'."""
    x = x.strip().lower()
    if not x:
        raise argparse.ArgumentTypeError("extension cannot be empty")
    return x if x.startswith(".") else "." + x


def add_common_options(p: argparse.ArgumentParser) -> None:
    """Shared options reused across subcommands."""
    p.add_argument("root", metavar="ROOT", help="Root directory")
    p.add_argument(
        "--ext",
        nargs="+",
        type=normalize_ext,
        default=[".tmp", ".log", ".bak"],
        metavar="EXT",
        help="Extensions (default: %(default)s)",
    )
    p.add_argument(
        "--recursive",
        action="store_true",
        help="Scan recursively",
    )


def iter_files(root: Path, recursive: bool):
    """Yield directory entries (shallow or recursive)."""
    return root.rglob("*") if recursive else root.iterdir()


def get_root(args) -> Path | None:
    """Resolve and validate root directory; return None if invalid."""
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print("ERROR: not a directory:", root)
        return None
    return root


# ----------------------------- commands -------------------------------- #

def cmd_scan(args) -> int:
    root = get_root(args)
    if root is None:
        return 2

    exts = set(args.ext)
    count = 0

    for p in iter_files(root, args.recursive):
        if p.is_file() and p.suffix.lower() in exts:
            print(p.relative_to(root))
            count += 1

    print("-" * 60)
    print("Matched:", count)
    return 0


def cmd_report(args) -> int:
    root = get_root(args)
    if root is None:
        return 2

    exts = set(args.ext)
    matched = 0
    total_bytes = 0

    for p in iter_files(root, args.recursive):
        if p.is_file() and p.suffix.lower() in exts:
            matched += 1
            total_bytes += p.stat().st_size

    print("Root     :", root)
    print("Exts     :", sorted(exts))
    print("Recursive:", args.recursive)
    print("Matched  :", matched)
    print("Bytes    :", total_bytes)
    return 0


def cmd_clean(args) -> int:
    root = get_root(args)
    if root is None:
        return 2

    # Safety gate: must choose one
    if not (args.dry_run or args.force):
        print("ERROR: clean requires --dry-run or --force")
        return 2

    exts = set(args.ext)
    matched = 0
    deleted = 0
    skipped = 0

    for p in iter_files(root, args.recursive):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue

        matched += 1
        rel = p.relative_to(root)

        if args.dry_run:
            print("[DRY] delete:", rel)
            continue

        try:
            p.unlink()
            print("deleted:", rel)
            deleted += 1
        except OSError as e:
            print("SKIP:", rel, "->", e)
            skipped += 1

    print("-" * 60)
    print("Matched:", matched)
    print("Deleted:", deleted)
    print("Skipped:", skipped)
    return 0


# ------------------------------ main ----------------------------------- #

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tool",
        description="subcommands (scan/report/clean).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # scan
    p_scan = sub.add_parser("scan", help="List matched files")
    add_common_options(p_scan)
    p_scan.set_defaults(func=cmd_scan)

    # report
    p_report = sub.add_parser("report", help="Summary only")
    add_common_options(p_report)
    p_report.set_defaults(func=cmd_report)

    # clean
    p_clean = sub.add_parser("clean", help="Delete matched files (safe)")
    add_common_options(p_clean)
    safety = p_clean.add_mutually_exclusive_group()
    safety.add_argument("--dry-run", action="store_true", help="Preview only")
    safety.add_argument("--force", action="store_true", help="Actually delete")
    p_clean.set_defaults(func=cmd_clean)

    args = parser.parse_args()
    rc = args.func(args)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()

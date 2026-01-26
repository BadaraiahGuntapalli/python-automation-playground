"""
Professional help + mutually exclusive flags

Goal:
    - Show high-quality help output
    - Use metavar, defaults, examples
    - Mutually exclusive flags (--dry-run vs --force)
"""

import argparse
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(
        prog="cleanup",
        description="A safe cleanup CLI (Level 1.4: help UX + groups).",
        epilog=(
            "Examples:\n"
            "  cleanup playground/out --mode report --ext .log .tmp\n"
            "  cleanup playground/out --mode delete --ext .tmp --dry-run\n"
            "  cleanup playground/out --mode delete --ext .tmp --force\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,  # preserves newlines in epilog
    )
    
    # Positional
    parser.add_argument(
        "root",
        metavar="ROOT_DIR",
        help="Root directory to operate on (relative or absolute)"
    )
    
    # Normal options
    parser.add_argument(
        "--mode",
        choices=["report", "delete"],
        default="report",
        help="Operation mode (default: %(default)s)"
    )

    parser.add_argument(
        "--ext",
        nargs="+",
        default=[".tmp", ".log", ".bak"],
        #metavar="EXT",
        help="Extensions to target (default: %(default)s)"
    )
    
    # Mutually exclusive group
    safety = parser.add_mutually_exclusive_group()
    safety.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without deleting anything"
    )
    safety.add_argument(
        "--force",
        action="store_true",
        help="Allow deletion when --mode delete is used"
    )

    args = parser.parse_args()

    # Normalize + validate root
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"ROOT_DIR is not a directory: {root}")  # argparse-style error

    # Normalize extensions
    exts = set()
    for x in args.ext:
        x = x.strip().lower()
        if not x:
            parser.error("EXT cannot be empty")
        exts.add(x if x.startswith(".") else "." + x)

    # Enforce safety policy
    if args.mode == "delete" and not (args.dry_run or args.force):
        parser.error("In delete mode you must pass either --dry-run or --force")

    # Summary (demo output)
    print("Root :", root)
    print("Mode :", args.mode)
    print("Exts :", sorted(exts))
    print("Dry  :", args.dry_run)
    print("Force:", args.force)
    
if __name__ == "__main__":
    main()
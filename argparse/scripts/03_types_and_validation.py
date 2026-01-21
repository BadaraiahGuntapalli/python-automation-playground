"""
Types, validation, and choices (deep)
    - --older-than <duration>
    - --mode <delete|report>
    - --limit <int> (max files to act on)
"""

import argparse
from ast import arg
from ctypes import ArgumentError
from pathlib import Path
from datetime import timedelta
import sys


def parse_duration(s: str) -> timedelta:
    s = s.strip().lower()
    
    if not s:
        raise argparse.ArgumentTypeError("duration cannot be empty")
    
    unit = s[-1]
    value = s[:-1]
    
    if not value.isdigit():
        raise argparse.ArgumentTypeError(
            f"invalid duration value: '{s}' (number required)"
        )
        
    value = int(value)
    
    if unit == 's':
        return timedelta(seconds=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    else:
        raise argparse.ArgumentTypeError(
            f"invalid duration unit: '{unit}' (use s, m, h, d)"
        )
        
        
def positive_int(s: str) -> int:
    try: 
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError("must be integer")
    
    if value <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    
    return value 


def main():
    parser=argparse.ArgumentParser(
        description="Typed and validated CLI arguments."
    )
    
    parser.add_argument(
        "root",
        help="Root directory to operate on"
    )
    
    parser.add_argument(
        "--older-than",
        type=parse_duration,
        metavar="DURATION",
        help="Only target files older than this (e.g. 30m, 2h, 7d)"
    )
    
    parser.add_argument(
        "--mode",
        choices=["delete", "report"],
        default="report",
        help="Operation mode (default: report)"
    )
    
    parser.add_argument(
        "--limit",
        type=positive_int,
        default=100,
        help="Maximum number of files to process (default: 100)"
    )
    
    args = parser.parse_args()
    
    root = Path(args.root).expanduser().resolve()
    
    if not root.is_dir():
        print("Directory doesnot exit")
        sys.exit(2)
        
    # --------- inspect parsed & typed values -----------------
    print("Root       :", root)
    print("Mode       :", args.mode)
    print("Limit      :", args.limit)

    if args.older_than is not None:
        print("Older than :", args.older_than)
    else:
        print("Older than : (not set)")


if __name__ == "__main__":
    main()
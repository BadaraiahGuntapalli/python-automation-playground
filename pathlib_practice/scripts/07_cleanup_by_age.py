"""
Cleanup by age (duration string)

Goal:
    - Delete files older than a given duration (e.g. 30m, 2h)
    - DRY RUN support
    - Pure pathlib + datetime
"""

from pathlib import Path
from datetime import datetime, timedelta

def parse_duration(s:str) -> timedelta:
    """
    Convert: duration string to timedelta 
    """
    s = s.strip().lower()
    if s.endswith("s"):
        return timedelta(seconds=int(s[:-1]))
    elif s.endswith("m"):
        return timedelta(minutes=int(s[:-1]))
    elif s.endswith("h"):
        return timedelta(hours=int(s[:-1]))
    else:
        return ValueError("Invalid function format: {s}")
    

def main():
    DRY_RUN = True
    OLDER_THAN = "50H"

    script_dir = Path(__file__).resolve().parent
    out_dir = (script_dir / ".." / "playground" / "out").resolve()

    if not out_dir.is_dir():
        print("Directory doesnot exist")
        print(out_dir)
        return 
    
    delta = parse_duration(OLDER_THAN)
    now = datetime.now()
    cutoff = now - delta

    matched = 0 
    deleted = 0
    skipped = 0

    print("Cleanup by age")
    print("Root      :", out_dir)
    print("Dry run   :", DRY_RUN)
    print("Older than:", OLDER_THAN)
    print("Cutoff    :", cutoff)
    print("-" * 70)

    for p in out_dir.rglob("*"):
        if not p.is_file():
            continue

        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except OSError as e:
            print("SKIP (stat failed), p")
            print("Reason: ", e)
            skipped += 1
            continue

        if mtime > cutoff:
            continue

        matched += 1
        rel = p.relative_to(out_dir)

        if DRY_RUN:
            print(f"[DRY] delete: {rel}, | modified: {mtime}")
            continue

        try:
            p.unlink()
            print(f"deleted: {p}")
            deleted += 1
        except OSError as e:
            print("SKIP (delete failed)", rel)
            print(f"Reason: {e}")
            skipped += 1

    print("-" * 70)
    print("Matched (older):", matched)
    print("Deleted        :", deleted)
    print("Skipped        :", skipped)
    if DRY_RUN:
        print("Set DRY_RUN = False to actually delete.")




if __name__ == "__main__":
    main()

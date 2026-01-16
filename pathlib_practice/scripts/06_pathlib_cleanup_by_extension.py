"""
Cleanup by extension
    - rglob recursively 
    - filterby extension
    - DRY RUN support
    - delete via Path.unlink()
    - write a report
"""

from pathlib import Path 
from datetime import datetime 


def main():
    DRY_RUN = True  # set False to actually delete
    DELETE_EXTS = {".tmp", ".log", ".bak"}

    script_dir = Path(__file__).resolve().parent
    out_dir = (script_dir / ".." / "playground" / "out").resolve()

    if not out_dir.is_dir():
        print("ERROR: out directory does not exist:")
        print(out_dir)
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = out_dir / f"cleanup_ext_report_{ts}.txt"

    matched = 0
    deleted = 0
    skipped = 0

    lines = []
    lines.append("CLEANUP REPORT (by extension)")
    lines.append("=" * 70)
    lines.append(f"Root    : {out_dir}")
    lines.append(f"Dry run : {DRY_RUN}")
    lines.append(f"Exts    : {sorted(DELETE_EXTS)}")
    lines.append(f"Time    : {datetime.now()}")
    lines.append("-" * 70)

    print("Cleanup by extension (pathlib)")
    print("Root   :", out_dir)
    print("Dry run:", DRY_RUN)
    print("Exts   :", sorted(DELETE_EXTS))
    print("-" * 70)

    for p in out_dir.rglob("*"):
        if not p.is_file():
            continue

        if p.suffix.lower() not in DELETE_EXTS:
            continue

        matched += 1
        rel = p.relative_to(out_dir)

        if DRY_RUN:
            print("[DRY] delete:", rel)
            lines.append(f"[DRY] {rel}")
            continue

        try:
            p.unlink()  # delete file
            print("deleted:", rel)
            lines.append(f"deleted: {rel}")
            deleted += 1
        except OSError as e:
            print("SKIP (delete failed):", rel)
            print("Reason:", e)
            lines.append(f"SKIP: {rel} -> {e}")
            skipped += 1

    lines.append("-" * 70)
    lines.append(f"Matched: {matched}")
    lines.append(f"Deleted: {deleted}")
    lines.append(f"Skipped: {skipped}")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    print("-" * 70)
    print("Report written to:", report_path)
    print("Matched:", matched, "| Deleted:", deleted, "| Skipped:", skipped)
    if DRY_RUN:
        print("Set DRY_RUN = False to actually delete.")


if __name__ == "__main__":
    main()
"""
Argparse CLI + options
    - Use argparse (clean help, defaults)
    - INPUT.csv required
    - --out-dir optinal (default: input folder)
    - --min-score optional filter
    - Stream process and write report.csv + errors.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path

REQUIERD_COLUMNS = {"id", "name", "score"}

def parse_row(row: dict) -> dict:
    return {
        "id": int(row["id"].strip()),
        "name": row["name"].strip(),
        "score": float(row["score"].strip()),
    }


def grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"

def existing_file(p: str) -> Path:
    path = Path(p).expanduser()
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"input file not found: {path}")
    return path

def main() -> int:
    parser = argparse.ArgumentParser(
        description="streaming report/errors with argparse options"
    )
    
    parser.add_argument(
        "input_csv",
        type=existing_file,
        help="Path to input csv file"
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: same folder as input csv)"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=None,
        help="only include rows with score >= this value"
    )
    
    args = parser.parse_args()
    
    in_path: Path = args.input_csv
    out_dir: Path = args.out_dir.expanduser() if args.out_dir else in_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = out_dir / "report.csv"
    errors_path = out_dir / "errors.csv"
    
    report_fields = ["id", "name", "score", "passed", "grade"]
    
    good_count = 0
    bad_count = 0
    fileterd_count = 0
    
    with in_path.open("r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in, fieldnames=report_fields)
        
        header = set(reader.fieldnames or [])
        missing = REQUIERD_COLUMNS - header
        if missing:
            print("ERROR: missing required columns:", sorted(missing))
            print("Found columns: ", reader.fieldnames)
            return 2
        
        with report_path.open("w", encoding="utf-8", newline="") as f_rep, \
            errors_path.open("w", encoding="utf-8", newline="") as f_err:
                
                rep_writer = csv.DictWriter(f_rep, fieldnames=report_fields)
                rep_writer.writeheader()
                
                err_fields = list(reader.fieldnames) + ["line_no", "error"]
                err_writer = csv.DictWriter(f_err, fieldnames=err_fields)
                err_writer.writeheader()
                
                for line_no, row in enumerate(reader, start=2):
                    try:
                        r = parse_row(row)
                        s = r["score"]
                        
                        if args.min_score is not None and s < args.min_score:
                            filtered_count += 1
                            continue
                        
                        rep_writer.writerow(
                            {
                                "id": r["id"],
                                "name":r["name"],
                                "score":f"{s:.2f}",
                                "passed": "yes" if s >= 80 else "no",
                                "grade": grade(s),
                            }
                        )
                        good_count += 1
                    
                    except Exception as e:
                        out={k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                        out["line_no"] = line_no
                        out["error"] = str(e)
                        err_writer.writerow(out)
                        bad_count += 1
                        
    print("-" * 60)
    print("Input   :", in_path)
    print("Out dir :", out_dir)
    print("Report  :", report_path, f"({good_count} rows)")
    print("Errors  :", errors_path, f"({bad_count} rows)")
    
    if args.min_score is not None:
        print("Filtered:", fileterd_count, f"(score < {args.min_score})")
        
        
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
                            
"""
CLI paths (simple sys.argv)

Goal:
  - input CSV path from CLI
  - optional output directory from CLI
  - stream processing + write report/errors
"""
import csv
import sys
from pathlib import Path


REQUIRED_COLUMNS = {"id", "name", "score"}


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

def usage(prog: str) -> None:
    print("Usage:")
    print(f"  python {prog} INPUT.csv [OUTPUT_DIR]")
    print("")
    print("Examples:")
    print(f"  python {prog} playground/out/sample.csv")
    print(f"  python {prog} playground/out/sample.csv playground/out/results")
    

def main():
    prog = Path(sys.argv[0]).name
    
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        usage(prog)
        return
    in_path = Path(sys.argv[1]).expanduser()
    
    if len(sys.argv) >= 3:
        out_dir = Path(sys.argv[2]).expanduser()
    else:
        out_dir = in_path.parent
        
    if not in_path.is_file():
        print("ERROR: input csv file not found")
        print(in_path)
        return
    
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report_cli.csv"
    errors_path = out_dir / "errors_cli.csv"
    
    report_fields = ["id", "name", "score", "passed", "grade"]
    good_count = 0
    bad_count = 0

    with in_path.open("r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in)

        header = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - header
        if missing:
            print("ERROR: missing required columns:", sorted(missing))
            print("Found columns:", reader.fieldnames)
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
                    rep_writer.writerow(
                        {
                            "id": r["id"],
                            "name": r["name"],
                            "score": f"{s:.2f}",
                            "passed": "yes" if s >= 80 else "no",
                            "grade": grade(s),
                        }
                    )
                    good_count += 1
                except Exception as e:
                    out = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                    out["line_no"] = line_no
                    out["error"] = str(e)
                    err_writer.writerow(out)
                    bad_count += 1

    print("-" * 60)
    print("Input :", in_path)
    print("Out dir:", out_dir)
    print("Report:", report_path, f"({good_count} rows)")
    print("Errors:", errors_path, f"({bad_count} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    
        
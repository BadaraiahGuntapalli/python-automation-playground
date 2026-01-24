"""
Streaming processing (no big lists)

Goal:
  - Read row-by-row (stream)
  - Write report.csv on the fly
  - Write errors.csv on the fly
  - Keep schema validation + type conversion + computed columns
"""

import csv
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

def main():
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent

    in_path = project_root / "playground" / "out" / "sample.csv"
    report_path = project_root / "playground" / "out" / "report.csv"
    errors_path = project_root / "playground" / "out" / "errors.csv"

    if not in_path.is_file():
        print("ERROR: input CSV not found:", in_path)
        return

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
            return
        
        # Open outputs only after header validation passes
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
                    # write bad row immediately
                    out = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                    out["line_no"] = line_no
                    out["error"] = str(e)
                    err_writer.writerow(out)
                    bad_count += 1
                    
                    
    print("-" * 60)
    print("Input :", in_path)
    print("Report:", report_path, f"({good_count} rows)")
    print("Errors:", errors_path, f"({bad_count} rows)")


if __name__ == "__main__":
    main()
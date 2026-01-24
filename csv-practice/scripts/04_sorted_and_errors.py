"""
Sorted report + erroes.csv
    - Read + validate + type-convert
    - Write report.csv sorted by score (desc)
    - Write errors.csv with bad rows + error message
"""

import csv
from doctest import REPORT_ONLY_FIRST_FAILURE
from encodings.rot_13 import rot13
from ftplib import error_perm
from logging import root
from pathlib import Path
from turtle import end_fill

REQUIRED_COLUMNS = {"id", "name", "score"}

def parse_row(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "name": str(row["name"]),
        "score": float(row["score"]),
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
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent
    print(f"your root dir : {root_dir}")
    
    in_path = root_dir / "playground" / "out" / "sample.csv"
    report_path = root_dir / "playground" / "out" / "report_grade.csv"
    errors_path = root_dir / "playground" / "out" / "errors.csv"
    
    if not in_path.is_file():
        print("File doesnot exit")
        print(in_path)
        return
    
    good = []
    errors = []
    
    
    
    with in_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        
        header = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - header
        
        if missing:
            print("ERROR: missing required columns ", sorted(missing))
            print("Found columns: ", reader.fieldnames)
            return
        
        for line_no, row in  enumerate(reader, start=2):
            try:
                typed = parse_row(row)
                good.append(typed)
            except Exception as e:
                err_row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                err_row["line_row"] = line_no
                err_row["error"] = str(e)
                errors.append(err_row)
                
    # higest first (descending order)            
    good.sort(key=lambda r: r["score"], reverse=True)
    
    # Build the reports 
    report_rows = []
    for r in good:
        s = r["score"]
        report_rows.append(
            {
            "id": r["id"],
            "name":r["name"],
            "score":r["score"],
            "passed": "yes" if s >= 80 else "no",
            "grade": grade(s),
        }
        )
        
    # write report.csv
    report_fields = ["id", "name", "score", "passed", "grade"]
    with report_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(report_rows)
        
    if errors:
        error_fields = list(reader.fieldnames) + ["line_row", "error"]
        with errors_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=error_fields)
            w.writeheader()
            w.writerows(errors)
    else:
        # if there are no errors then choose not to create a file path
        errors_path = None
        
    print("-" * 60)
    print("Input :", in_path)
    print("Report:", report_path)
    print("Rows  :", len(good))
    if errors_path:
        print("Errors:", errors_path, f"({len(errors)} bad rows)")
    else:
        print("Errors: none")


if __name__ == "__main__":
    main()
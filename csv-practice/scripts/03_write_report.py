"""
Write a report CSV (DictWriter)

Goal:
  - Read + validate + type-convert rows
  - Add computed columns: passed, grade
  - Write output report.csv
"""

import csv
from pathlib import Path

REQUIRED_COLUMNS = {"id", "name", "score"}

def parse_row(row: dict) -> dict:
    return{
        "id": int(row["id"]),
        "name": str(row["name"]),
        "score": float(row["score"])
    }
    
    
def grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"



def main():
    script_dir = Path(__file__).resolve().parent
    project_dir = script_dir.parent
    
    in_path = project_dir / "playground" / "out" / "sample.csv"
    out_path = project_dir / "playground" / "out" / "report.csv"


    if not in_path.is_file():
        print("File doesnot exist")
        print(in_path)
        return 
    
    good = []
    bad = 0
    
    with in_path.open(mode='r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        header = set(reader.fieldnames)
        missing = REQUIRED_COLUMNS - header
        if missing:
            print("ERROR: missing requreid columns", sorted(missing))
            print("Found columns: ", reader.fieldnames)
            return
        
        for i, row in enumerate(reader, start=2):
            try:
                good.append(parse_row(row))
            except Exception as e:
                bad += 1
                print(f"SKIP ROW: {i}: {row} -> {e}")
                
    # Build output rows with computed fields
    out_rows = []
    for r in good:
        s = r["score"]
        out_rows.append({
            "id": r["id"],
            "name": r["name"],
            "score": f"{s:.2f}",
            "passed":"yes" if s >=80 else "no",
            "grade": grade(s)
        })
        
        
    fieldnames = ["id", "name", "score", "passed", "grade"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)
        
        
    print("-" * 60)
    print("Input :", in_path)
    print("Output:", out_path)
    print("Good rows:", len(good))
    print("Bad rows :", bad)
    
    
    
if __name__ == "__main__":
    main()












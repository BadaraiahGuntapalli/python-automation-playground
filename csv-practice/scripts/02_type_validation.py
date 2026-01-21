"""
Types + validation

Goal:
  - Validate required columns exist
  - Convert types:
      id -> int
      score -> float
  - Skip bad rows and count errors (automation style)
"""

import csv
from pathlib import Path


REQUIRED_COLUMNS = {"id", "name", "score"}

def parse_row(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "name": str(row["name"]),
        "score": float(row["score"]),
    }
    


def main():
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    csv_path = project_root / "playground" / "out" / "sample.csv"

    if not csv_path.is_file():
        print("ERROR: CSV file not found:", csv_path)
        return
    
    good = []
    bad = 0
    
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header_names = reader.fieldnames
        header_names = map(lambda field: field.strip(), header_names)
        header = set(header_names or [])
        missing = REQUIRED_COLUMNS - header
        
        if missing:
            print(f"Error: missing required columns: {sorted(missing)}")
            print(f"Found columns: {reader.fieldnames}")
            return
        
        for i, row in enumerate(reader, start=2):
            try:
                typed = parse_row(row)
                good.append(typed)
            except Exception as e:
                bad += 1
                print(f"SKIP row {i}: {row} -> {e}")
                
    print("-" * 60)
    print("Good rows:", len(good))
    print("Bad rows :", bad)   
    
    if good:
        avg = sum(r["score"] for r in good) / len(good)
        best = max(good, key=lambda r:r["score"])
        
        print(f"Average score: {avg}")
        print(f"Best: id={best['id']} name={best['name']} score={best['score']}")


if __name__ == "__main__":
    main()
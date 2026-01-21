"""
Read csv (basic)

- Read a csv file
- print header (filednames)
- print number of rows 
- print first 3 rows as dictionaries
"""

import csv 
from logging import root
from pathlib import Path

def main():
    scripts_dir = Path(__file__).resolve().parent
    root_dir = scripts_dir.parent
    
    csv_path = root_dir /  "playground" / "out" / "sample.csv"
    
    if not csv_path.is_file():
        print("Error: csv file doesnot exit")
        print(csv_path)
        return
    
    rows=[]
    
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        print(f"Header: {reader.fieldnames}")
        
        for row in reader:
            rows.append(row)
            
    print(f"Total rows: {len(rows)}")
    print("-" * 50)
    print("first 3 rows")
    for r in rows[:3]:
        print(r)



if __name__ == "__main__":
    main()
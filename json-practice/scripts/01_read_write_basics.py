"""
Read + Write basic JSON
- Load config.json -> Python dict
- Update/add keys
- Save back as pretty JSON
"""

import json
from pathlib import Path
from datetime import datetime

def main():
    scripts_dir = Path(__file__).resolve().parent
    root_dir = scripts_dir.parent
    
    in_path = root_dir / "playground" / "out" / "config.json"
    out_path = root_dir / "playground" / "out" / "config_save.json"
    
    if not in_path.is_file():
        print("ERROR: json file doesnot exist")
        print(in_path)
        return
    
    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("Loaded type:", type(data))
    print("Loaded data:", data)
    
    # Modify
    data["last_run"] = datetime.now().strftime("Y-%m-%d %H:%M:%S")
    data["min_score"] = int(data.get("min_score", 80))
        
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
        
    print("-" * 60)
    print("Input :", in_path)
    print("Output:", out_path)
    
    
    
if __name__ == "__main__":
    main()
            
            
        
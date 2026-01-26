"""
Nested JSON + validation (automation style)

Goal:
  - Load nested config.json
  - Validate required keys exist
  - Safely read nested values
  - Build resolved paths (Path objects)
"""

from http.client import TOO_EARLY
import json
from pathlib import Path
from turtle import end_fill
from urllib.robotparser import RequestRate

def require_key(obj: dict, key: str, where: str = "root") -> None:
    if key not in obj:
        raise KeyError(f"Missing required key: {key} in {where}")
    
def main():
    scripts_dir = Path(__file__).resolve().parent
    root = scripts_dir.parent
    
    config_path = root / "playground" / "out" / "config.json"
    
    if not config_path.is_file():
        print("ERROR: config.json not found", config_path)
        return
    
    # 1) load json file
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
        
    
    # 2) Validate top-level keys    
    try:
        require_key(cfg, "project")
        require_key(cfg, "paths")
        require_key(cfg, "options")
        
        require_key(cfg["paths"],  "input_csv", where="paths")
        require_key(cfg["paths"], "out_dir", where="paths")
        
        require_key(cfg["options"], "min_score", where="options")
        require_key(cfg["options"], "verbose", where="options")
        
        
    except KeyError as e:
        print(f"CONFIG ERROR: {e}")
        return
    
    # 3) Read values (nested)
    project = cfg["project"]
    input_csv_str = cfg["paths"]["input_csv"]
    out_dir_str = cfg["paths"]["out_dir"]

    min_score = int(cfg["options"]["min_score"])
    verbose = bool(cfg["options"]["verbose"])

    # convert strings to paths 
    input_csv = (root / input_csv_str).resolve()
    out_dir = (root / out_dir_str).resolve()
    
    # 5) Print final resolved configuration
    print("-" * 60)
    print("Project   :", project)
    print("Input CSV :", input_csv)
    print("Out dir   :", out_dir)
    print("Min score :", min_score)
    print("Verbose   :", verbose)
    
    
if __name__ == "__main__":
    main()
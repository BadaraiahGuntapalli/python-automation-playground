"""
Defaults + overrides (automation pattern)

Goal:
  - Load nested config.json
  - Apply safe defaults if keys missing
  - Apply "overrides" (runtime changes) on top of config
  - Build final resolved config dict and print it
"""

import json
from pathlib import Path

def get_nested(d: dict, path: list[str], default=None):
  """
  Safe nested get:
      get_nested(cfg, ["options", "min_score"], 80)
  Returns default if any key is missing.
  """
  
  cur = d
  for k in path:
    if not isinstance(cur, dict) or k not in cur:
      return default
    
    cur = cur[k]
  return cur
        
        
        
        
def main():
  scripts_dir = Path(__file__).resolve().parent
  project_root = scripts_dir.parent
  config_path = project_root / "playground" / "out" / "config.json"

  if not config_path.is_file():
      print("ERROR: config.json not found:", config_path)
      return

  # 1) Load config.json -> dict
  with config_path.open("r", encoding="utf-8") as f:
      cfg = json.load(f)
      
      
  # 2) Read with defaults (won't crash if missing)
  project = cfg.get("project", "unknown-project")
  
  input_csv_str = get_nested(cfg, ["paths", "input_csv"], "playground/out/sample.csv")
  out_dir_str = get_nested(cfg, ["paths", "out_dir"], "playground/out/results")
  
  min_score = get_nested(cfg, ["options", "min_score"], 50)
  verbose = get_nested(cfg, ["options", "verbose"], False)
  
  # Normalize types 
  min_score = int(min_score)
  verbose = bool(verbose)
  
  # 3) Runtime overrides (simulate what CLI/env would do)
  # Imagine user wants min_score=85 today, without editing config.json
  overrides = {
      "min_score": 105,     # override from "outside"
      "verbose": True      # override from "outside"
  }

  # Apply overrides
  min_score = overrides.get("min_score", min_score)
  verbose = overrides.get("verbose", verbose)
  
  # 4) Resolve paths
  input_csv = (project_root / input_csv_str).resolve()
  out_dir = (project_root / out_dir_str).resolve()

  # 5) Build final resolved config (this is what the pipeline will use)
  final_cfg = {
      "project": project,
      "paths": {
          "input_csv": str(input_csv),
          "out_dir": str(out_dir),
      },
      "options": {
          "min_score": min_score,
          "verbose": verbose,
      },
  }

  print("-" * 60)
  print("FINAL CONFIG (after defaults + overrides):")
  print(json.dumps(final_cfg, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
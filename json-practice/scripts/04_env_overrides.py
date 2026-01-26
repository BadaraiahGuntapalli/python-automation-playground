"""
Environment variable overrides (os.environ)

Goal:
  - Load config.json (defaults)
  - Override with ENV vars:
        MIN_SCORE (int)
        VERBOSE   (0/1, true/false)
        OUT_DIR   (path)
  - Build final config and print it
"""

import json
import os
from pathlib import Path


def get_nested(d: dict, path: list[str], default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def parse_bool(s: str) -> bool:
    s=s.strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    
    raise ValueError(f"Invalid boolean: {s!r} (use 1/0, true/false, yes/no)")
    
    
    
    
def main():
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    config_path = project_root / "playground" / "out" / "config.json"

    if not config_path.is_file():
        print("ERROR: config.json not found:", config_path)
        return

    # 1) Load config.json
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    # 2) Defaults from config (with fallback defaults)
    project = cfg.get("project", "unknown-project")

    input_csv_str = get_nested(cfg, ["paths", "input_csv"], "playground/out/sample.csv")
    out_dir_str = get_nested(cfg, ["paths", "out_dir"], "playground/out/results")

    min_score = int(get_nested(cfg, ["options", "min_score"], 80))
    verbose = bool(get_nested(cfg, ["options", "verbose"], False))
    
    
    # 3) ENV overrides (strings -> types)
    # ENV vars are always strings, so we convert
    if "MIN_SCORE" in os.environ:
        min_score = int(os.environ["MIN_SCORE"])
        
    if "VERBOSE" in os.environ:
        verbose = parse_bool(os.environ["VERBOSE"])

    if "OUT_DIR" in os.environ:
        out_dir_str = os.environ["OUT_DIR"]
        
    # 4) Resolve paths
    input_csv = (project_root / input_csv_str).resolve()
    out_dir = (project_root / out_dir_str).resolve()

    # 5) Final config
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
        "env_seen": {
            "MIN_SCORE": "MIN_SCORE" in os.environ,
            "VERBOSE": "VERBOSE" in os.environ,
            "OUT_DIR": "OUT_DIR" in os.environ,
        }
    }

    print("-" * 60)
    print("FINAL CONFIG (config.json + ENV overrides):")
    print(json.dumps(final_cfg, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
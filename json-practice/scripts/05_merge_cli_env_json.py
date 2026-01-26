"""
Merge CLI + ENV + JSON (automation-grade)

Priority order:
  CLI > ENV > config.json > defaults

Goal:
  - Build final settings dict
  - Type convert + validate
  - Print final settings
"""

import argparse
import json
import os
from pathlib import Path


DEFAULTS = {
    "paths": {
        "input_csv": "playground/out/sample.csv",
        "out_dir": "playground/out/results",
    },
    "options": {
        "min_score": 80,
        "verbose": False,
    },
}

def get_nested(d: dict, path: list[str], default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def parse_bool(s: str) -> bool:
    s = s.strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {s!r}")

def load_json_config(config_path:Path)-> dict:
    if not config_path.is_file():
        return {}
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
    
def main() -> int:
    # --- CLI (highest priority) ---
    parser = argparse.ArgumentParser(
        description="Config Level 2.1: merge CLI > ENV > JSON > defaults"
    )
    parser.add_argument("--config", type=Path, default=None, help="Path to config.json")
    parser.add_argument("--input-csv", type=str, default=None, help="Override input CSV path")
    parser.add_argument("--out-dir", type=str, default=None, help="Override output directory")
    parser.add_argument("--min-score", type=int, default=None, help="Override min_score")
    parser.add_argument("--verbose", type=parse_bool, default=None, help="Override verbose (1/0, true/false)")
    args = parser.parse_args()
    
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    config_path = (args.config.expanduser() if args.config else project_root / "playground" / "out" / "config.json")
    
    # json
    cfg_json = load_json_config(config_path=config_path)
    
    # start with defaults 
    input_csv = get_nested(DEFAULTS, ["paths", "input_csv"])
    out_dir = get_nested(DEFAULTS, ["paths", "out_dir"])
    min_score = int(get_nested(DEFAULTS, ["options", "min_score"]))
    verbose = bool(get_nested(DEFAULTS, ["options", "verbose"]))
    
    # merge json
    # --- Merge JSON (if present) ---
    input_csv = get_nested(cfg_json, ["paths", "input_csv"], input_csv)
    out_dir = get_nested(cfg_json, ["paths", "out_dir"], out_dir)
    min_score = int(get_nested(cfg_json, ["options", "min_score"], min_score))
    verbose = bool(get_nested(cfg_json, ["options", "verbose"], verbose))
    
    # Merger ENC
    if os.environ.get("INPUT_CSV"):
        input_csv = os.environ["INPUT_CSV"]
    if os.environ.get("OUT_DIR"):
        out_dir = os.environ["OUT_DIR"]
    if os.environ.get("MIN_SCORE"):
        min_score = int(os.environ["MIN_SCORE"])
    if os.environ.get("VERBOSE"):
        verbose = parse_bool(os.environ["VERBOSE"])
        
    # Merge CLI
    if args.input_csv is not None:
        input_csv = args.input_csv
    if args.out_dir is not None:
        out_dir = args.out_dir
    if args.min_score is not None:
        min_score = int(args.min_score)
    if args.verbose is not None:
        verbose = bool(args.verbose)
        
    input_csv_path = (project_root / input_csv).resolve() if not Path(input_csv).is_absolute()  else Path(input_csv).resolve()
    out_dir_path = (project_root / out_dir).resolve() if not Path(out_dir).is_absolute() else Path(out_dir).resolve()


    final={
        "paths": {
            "input_csv": str(input_csv_path),
            "out_dir": str(out_dir_path),
        },
        "options": {
            "min_score": min_score,
            "verbose": verbose,
        },
        "sources": {
            "config_path": str(config_path),
            "env_seen": {
                "INPUT_CSV": "INPUT_CSV" in os.environ,
                "OUT_DIR": "OUT_DIR" in os.environ,
                "MIN_SCORE": "MIN_SCORE" in os.environ,
                "VERBOSE": "VERBOSE" in os.environ,
            },
            "cli_seen": {
                "input_csv": args.input_csv is not None,
                "out_dir": args.out_dir is not None,
                "min_score": args.min_score is not None,
                "verbose": args.verbose is not None,
            },
        },       
    }
        
    
    print(json.dumps(final, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main()) 
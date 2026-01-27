"""
Validate + create output dir + save final_config.json

Priority order: cli > env > config.json > defaults

Adds:
- Validate inputs csv exists
- Create out-dir 
- Save final_config.json to out_dir
- Exit codes (0 OK, 2 input/config error)
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

def get_nested(d: dict, path: list[str], default= None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

def parse_bool(s: str)-> bool:
    s=s.strip().lower()
    
    if s in {"1", "yes", "on", "true", "y"}:
        return True
    if s in {"0", "no", "off", "false", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {s!r}")

def load_json_config(config_path: Path) -> dict:
    if not config_path.is_file():
        return {}
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def resolve_maybe_relative(project_root: Path, p:str) -> Path:
    """
    If p is absolute -> resolve it.
    If p is relative -> treat it as realative to project_root
    """
    path = Path(p).expanduser()
    if path.is_absolute():  
        return path
    return (project_root / path).resolve()


def main():
    parser = argparse.ArgumentParser(
        description="merge config + validate + save final_config.json"
    )
    
    parser.add_argument("--config", type=Path, default=None, help="Path to config.json")
    parser.add_argument("--input-csv", type=str, default=None, help="Override input CSV path")
    parser.add_argument("--out-dir", type=str, default=None, help="Override output directory")
    parser.add_argument("--min-score", type=int, default=None, help="Override min_score")
    parser.add_argument("--verbose", type=parse_bool, default=None, help="Override verbose (1/0, true/false)")
    args=parser.parse_args()
    
    scripts_dir = Path(__file__).resolve().parent
    project_root=scripts_dir.parent
    
    config_path = (args.config.expanduser()) if args.config else (project_root / "playground" / "out" / "config.json")
    cfg_json = load_json_config(config_path=config_path)
    
    # Defaults 
    input_csv = get_nested(DEFAULTS, ["paths", "input_csv"])
    out_dir = get_nested(DEFAULTS, ["paths", "out_dir"])
    min_score = int(get_nested(DEFAULTS,["options", "min_score"]))
    verbose = bool(get_nested(DEFAULTS, ["options", "verbose"]))
    
    # merge json
    input_csv = get_nested(cfg_json, ["paths", "input_csv"], input_csv)
    out_dir = get_nested(cfg_json, ["paths", "out_dir"], out_dir)
    min_score = int(get_nested(cfg_json, ["options", "min_score"], min_score))
    verbose = bool(get_nested(cfg_json, ["options", "verbose"], verbose))
    
    # merger ENV
    if "INPUT_CSV" in os.environ:
        input_csv = os.environ["INPUT_CSV"]
    if "OUT_DIR" in os.environ:
        out_dir = os.environ["OUT_DIR"]
    if "MIN_SCORE" in os.environ:
        try: 
            min_score=int(os.environ["MIN_SCORE"])
        except ValueError:
            print("CONFIG ERROR: MIN_SCORE must be an integer")
            return 2
    if  "VERBOSE" in os.environ:
        try:
            verbose = parse_bool(os.environ["VERBOSE"])
        except argparse.ArgumentTypeError as e:
            print(f"CONFIG ERROR: {e}")
            return 2
        
    if args.input_csv is not None:
        input_csv = args.input_csv
    if args.out_dir is not None:
        out_dir = args.out_dir
    if args.min_score is not None:
        min_score = int(args.min_score)
    if args.verbose is not None:
        verbose = bool(args.verbose)
        
    # resolve paths 
    input_csv_path = resolve_maybe_relative(project_root, str(input_csv))
    out_dir_path = resolve_maybe_relative(project_root, str(out_dir))
    
    # validate input 
    if not input_csv_path.is_file():
        print("INPUT ERROR: input csv not found", input_csv_path)
        print("Tip: set paths in config.json or pass --input-csv or env INPUT_CSV")
        return 2
    
    # validate output dir
    try:
        out_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("OUTPUT ERROR: cannot create out_dir:", out_dir_path, "->", e)
        return 2
    
    # ---- Final config ----
    final = {
        "paths": {
            "input_csv": str(input_csv_path),
            "out_dir": str(out_dir_path),
        },
        "options": {
            "min_score": min_score,
            "verbose": verbose,
        },
        "sources":{
            "config_path": str(config_path),
            "env_seen":{
                "INPUT_CSV": "INPUT_CSV" in os.environ,
                "OUT_DIR": "OUT_DIR" in os.environ,
                "MIN_SCORE": "MIN_SCORE" in os.environ,
                "VERBOSE": "VERBOSE" in os.environ,
            },
            "cli_seen":{
                "input_csv": args.input_csv is not None,
                "out_dir": args.out_dir is not None,
                "min_score": args.min_score is not None,
                "verbose": args.verbose is not None,
            },
        },
    }
    
    # save final_config.json 
    final_config_path = out_dir_path / "final_config.json"
    with final_config_path.open("w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    return 0
        
        
if __name__ == "__main__":
    raise SystemExit(main())
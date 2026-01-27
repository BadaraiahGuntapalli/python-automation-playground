"""
Production run scaffold

Priority:
  CLI > ENV > config.json > defaults

Adds:
  - Lock file (avoid double-run)
  - Per-run directory (runs/run_<timestamp>/)
  - Console + file logging (run.log)
  - Save final_config.json + summary.json in run folder
  - Timing + exit codes
"""

import argparse
from ast import TypeVarTuple
from http.client import TOO_EARLY
import json
import logging
import os
from pathlib import Path
from datetime import datetime
from telnetlib import EC
import time


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

# ---------------------------- small utilities ----------------------------

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
    raise argparse.ArgumentTypeError(f"Invalid boolean: {s!r} (use 1/0, true/false, yes/no)")

def load_json_config(config_path: Path) -> dict:
    if not config_path.is_file():
        return {}
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_maybe_relative(project_root: Path, p: str) -> Path:
    path = Path(p).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (project_root / path).resolve()

def setup_logging(log_path: Path, verbose: bool) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    console_level = logging.DEBUG if verbose else logging.INFO
    file_level = logging.DEBUG
    
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    # reset handlers (prevents duplicate logs in re-runs)
    for h in list(root.handlers):
        root.removeHandlers(h)
        
        try:
            h.close()
        except Exception:
            pass
    
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(fmt)
    root.addHandler(ch)
    
    fh = logging.FileHandler(str(log_path), mode='w', encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)
    
    
def acquire_lock(lock_path: Path) -> None:
    """
    Create a lock file exclusively.
    If it already exists, we assume another run is active (or it crashed earlier).
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("x", encoding="utf-8") as f: # 'x' => fail if exists
        f.write(f"created_at={datetime.now().isoformat()}\n")
        f.write(f"pid={os.getpid()}\n")
        
        
def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass
    
# ------------------------------ main logic ------------------------------
def main() -> int:
    t_start = time.perf_counter()
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    parser = argparse.ArgumentParser(
        description="Config Level 2.7: run scaffold (lock + run_dir + logs + summary)"
    )
    parser.add_argument("--config", type=Path, default=None, help="Path to config.json")
    parser.add_argument("--input-csv", type=str, default=None, help="Override input CSV path")
    parser.add_argument("--out-dir", type=str, default=None, help="Override output directory")
    parser.add_argument("--min-score", type=int, default=None, help="Override min_score")
    parser.add_argument("--verbose", type=parse_bool, default=None, help="Override verbose (1/0, true/false)")
    parser.add_argument("--run-id", type=str, default=None, help="Run folder name (default: timestamp)")
    parser.add_argument("--no-lock", action="store_true", help="Disable lock file (not recommended)")
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent

    config_path = (args.config.expanduser() if args.config else project_root / "playground" / "out" / "config.json")
    cfg_json = load_json_config(config_path)

    # ---- defaults ----
    input_csv = get_nested(DEFAULTS, ["paths", "input_csv"])
    out_dir = get_nested(DEFAULTS, ["paths", "out_dir"])
    min_score = int(get_nested(DEFAULTS, ["options", "min_score"]))
    verbose = bool(get_nested(DEFAULTS, ["options", "verbose"]))

    # ---- json ----
    input_csv = get_nested(cfg_json, ["paths", "input_csv"], input_csv)
    out_dir = get_nested(cfg_json, ["paths", "out_dir"], out_dir)
    min_score = int(get_nested(cfg_json, ["options", "min_score"], min_score))
    verbose = bool(get_nested(cfg_json, ["options", "verbose"], verbose))

    # ---- env ----
    if "INPUT_CSV" in os.environ:
        input_csv = os.environ["INPUT_CSV"]
    if "OUT_DIR" in os.environ:
        out_dir = os.environ["OUT_DIR"]
    if "MIN_SCORE" in os.environ:
        try:
            min_score = int(os.environ["MIN_SCORE"])
        except ValueError:
            print("CONFIG ERROR: MIN_SCORE must be an integer")
            return 2
    if "VERBOSE" in os.environ:
        try:
            verbose = parse_bool(os.environ["VERBOSE"])
        except argparse.ArgumentTypeError as e:
            print("CONFIG ERROR:", e)
            return 2

    # ---- cli (highest) ----
    if args.input_csv is not None:
        input_csv = args.input_csv
    if args.out_dir is not None:
        out_dir = args.out_dir
    if args.min_score is not None:
        min_score = int(args.min_score)
    if args.verbose is not None:
        verbose = bool(args.verbose)
            
    # Resolve base paths
    input_csv_path = resolve_maybe_relative(project_root, str(input_csv))
    out_dir_path = resolve_maybe_relative(project_root, str(out_dir))
    
    # Prepare run_dir early (so logs go into it)
    run_id = args.run_id or datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
    runs_dir = out_dir_path / "runs"
    run_dir = runs_dir / run_id
    log_path = run_dir / "run.log"
    
    # setup logging now 
    setup_logging(log_path, verbose=verbose)
    log = logging.getLogger(__name__)
    
    lock_path = out_dir_path / ".lock"
    
    # Build final config dict
    final = {
        "paths": {"input_csv": str(input_csv_path), "out_dir": str(out_dir_path), "run_dir": str(run_dir)},
        "options": {"min_score": min_score, "verbose": verbose},
        "sources": {
            "config_path": str(config_path),
            "env_seen": {k: (k in os.environ) for k in ["INPUT_CSV", "OUT_DIR", "MIN_SCORE", "VERBOSE"]},
            "cli_seen": {
                "input_csv": args.input_csv is not None,
                "out_dir": args.out_dir is not None,
                "min_score": args.min_score is not None,
                "verbose": args.verbose is not None,
                "run_id": args.run_id is not None,
            },
        },
        "started_at": started_at,
    }
    
# Make output dirs
    try:
        out_dir_path.mkdir(parents=True, exist_ok=True)
        run_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log.error("OUTPUT ERROR: cannot create output dirs: %s", e)
        return 2

    # Acquire lock (unless disabled)
    lock_acquired = False 
    try:
        if not args.no_lock:
            try:
                acquire_lock(lock_path)
                lock_acquired = True
                log.info("Lock acquired: %s", lock_path)
            except FileExistsError:
                log.error("Another run may be active (lock exists): %s", lock_path)
                log.error("If stale, delete if manually: %s", lock_path)
                return 3
            
        # validate input csv 
        if not input_csv_path.is_file():
            log.error("INPUT ERROR: input CSV not found: %s", input_csv_path)
            return 2
        
        # Save final_config.json into out_dir
        final_config_path = run_dir / "final_config.json"
        with final_config_path.open("w", encoding="utf-8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)
            
        log.info("Run started")
        log.info("Input CSV : %s", input_csv_path)
        log.info("Out dir   : %s", out_dir_path)
        log.info("Run dir   : %s", run_dir)
        log.info("Saved     : %s", final_config_path)
        
        # ---- Placeholder for real pipeline work ----
        # Here you would call your CSV processing / API download / cleanup job.
        log.info("TODO: pipeline started ... ")
        time.sleep(10)
        log.info("pipeline ended ... ")
        
        return_code = 0
        log.info("Run finished successfully")
        
    except Exception:
        log.exception("Unhandled crash")
        return_code = 1
        
    finally:
        # Always write summary.json (even if crashed)
        ended_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = time.perf_counter() - t_start
        
        summary = {
            "run_id": run_id,
            "started_at": started_at,
            "ended_at": ended_at,
            "duration": duration,
            "exit_code": return_code,
            "log_file":str(log_path),
        }
        
        try:
            summary_path = run_dir / "summary.json"
            with summary_path.open("w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
                
        except Exception:
             # last-resort: don't crash on summary writing
            pass
        
        if lock_acquired:
            release_lock(lock_path)
                
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
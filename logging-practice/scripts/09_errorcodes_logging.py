"""
Exit codes + logging demo (automation-style)

Exit codes:
  0 = success
  1 = unexpected crash (exception)
  2 = input/config error (user mistake)
  3 = locked (another run active)

How to run:
  python exit_codes_demo.py --mode ok
  python exit_codes_demo.py --mode input
  python exit_codes_demo.py --mode lock
  python exit_codes_demo.py --mode crash

Check exit code:
  Git Bash/Linux: echo $?
  Windows CMD:    echo %ERRORLEVEL%
"""

import argparse
import code
from dataclasses import _MISSING_TYPE
import json
import logging
import os
from pathlib import Path
from datetime import datetime
import time


class ExitCode:
    OK = 0
    CRASH = 1
    INPUT = 2
    LOCKED = 3
    
    
    
def setup_logging(log_path: Path, verbose: bool = False) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    console_level = logging.DEBUG if verbose else logging.INFO
    file_level = logging.DEBUG

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # clear handlers (prevents duplicate logs in re-runs, notebooks)
    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    fh = logging.FileHandler(str(log_path), mode="w", encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)



def acquire_lock(lock_path: Path) -> None:
    """
    Exclusive create lock file. If it exists -> FileExistsError.
    """
    
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("x", encoding="utf-8") as f:
        f.write(f"created_at={datetime.now().isoformat()}\n")
        f.write(f"pid={os.getpid()}\n")
        
def release_lock(lock_path: Path) -> None:
    try: 
        lock_path.unlink()
    except FileNotFoundError:
        pass
    
def main() -> int:
    # IMPORTANT: always initialize return_code for finally block safety
    return_code = ExitCode.CRASH
    lock_acquired = False
    
    parser = argparse.ArgumentParser(
        description="Exit codes + logging demo"
    )
    parser.add_argument(
        "--mode",
        choices=["ok", "input", "lock", "crash"],
        default=None,
        help="which scenario to run"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG on console")
    args = parser.parse_args()
    
    # project dirs 
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "playground" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = out_dir / f"run_{ts}.log"
    summary_path = out_dir / f"summary_{ts}.json"
    lock_path = out_dir / ".lock"
    
    setup_logging(log_path, verbose=args.verbose)
    log = logging.getLogger(__name__)
    
    t0 = time.perf_counter()
    log.info("Started | mode=%s | log=%s", args.mode, log_path) 
    
    try:
        # mode: lock
        if args.mode == "lock":
            acquire_lock(lock_path=lock_path)
            lock_acquired = True
            log.info(f"Lock acquired: {lock_path}")
            
            # simulate long run so you start it again in another terminal
            log.info("Sleeping 10 seconds... start another run with --mode lock to see exit code 3.")
            time.sleep(30)
            
            return_code = ExitCode.OK
            log.info("Finished normally (lock mode)")
            return return_code
        
        
        # mode: input error
        if args.mode == "input":
            missing_file = out_dir / "definitely_missing.csv"
            if not missing_file.is_file():
                log.error(f"INPUT ERROR: file not found: {missing_file}")
                return_code=ExitCode.INPUT
                return return_code
            
        # mode: crash 
        if args.mode == "crash":
            log.info("About to crash on purpose")
            10/0    # ZeroDivisioError
            
        # mode: ok 
        log.info("Doing normal work...")
        time.sleep(0.5)
        log.info("Work done succefully.")
        return_code = ExitCode.OK
        return return_code
    
    except FileExistsError:
        # this happens when lock already exists
        log.error(f"LOCKED: another run is active (lock exists): {lock_path}")
        return_code = ExitCode.LOCKED
        return return_code
    
    except Exception:
        # Unexpected crash 
        log.exception("CRASH: unhandled exception")
        return_code = ExitCode.CRASH
        return return_code
    
    finally:
        # Always write a summary
        duration = round(time.perf_counter() - t0, 3)
        summary = {
            "mode": args.mode,
            "exit_code": return_code,
            "duration_sec": duration,
            "log_file": str(log_path),
            "summary_file": str(summary_path)
        }
        
        try:
            with summary_path.open("w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception:
            # never crash in finally
            pass
        
        if lock_acquired:
            release_lock(lock_path)
            log.info(f"Lock release: {lock_path}")        
        
        
    log.info(f"Exit code = {return_code}")
    
    
if __name__ == "__main__":
    raise SystemExit(main())
            
      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
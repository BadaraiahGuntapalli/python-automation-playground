"""
Timestamped log file per run

Goal:
  - Console: INFO+ (clean)
  - File: DEBUG+ (full details)
  - Create a NEW log file each run (no overwrite, no append mixing)
"""

from pathlib import Path
from datetime import datetime 
import logging






def setup_logging(log_path: Path, verbose: bool=False) -> None:
    """
    verbose=False:
        console = INFO+, file = DEBUG+
    verbose=True:
        console = DEBUG+, file = DEBUG+
    """
    
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    console_level = logging.DEBUG if verbose else logging.INFO
    file_level = logging.DEBUG
    
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    for h in list(root.handlers):
        root.removeHandlers()
        try:
            h.close()
        except Exception:
            pass
        
    # console handlers 
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(fmt)
    root.addHandler(ch)
    
    # file handlers
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)
    
    
def main():
     # ---- locate project root: logging/ ----
    scripts_dir = Path(__file__).resolve().parent      # logging/scripts
    project_root = scripts_dir.parent                  # logging/

    # ---- create per-run log file ----
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # safe on Windows
    log_dir = project_root / "playground" / "out" / "logs"
    log_path = log_dir / f"app_{ts}.log"
    
    
    VERBOSE = False
    setup_logging(log_path, verbose=VERBOSE)
    
    log = logging.getLogger(__name__)
    log.info("Program started")
    log.debug("DEBUG: will be in file always; in console only if VERBOSE=True")
    
    # Example 
    log.info("step 1: doing something")
    log.warning("step 2: minor warning example")
    
    # crash 
    try:
        1/0
    except Exception:
        log.exception("Example crash: division by 0")
        
    log.info("Program terminated")
    print(f"Log file this run : {log_path}")
    
    
    
    
if __name__ == "__main__":
    main()
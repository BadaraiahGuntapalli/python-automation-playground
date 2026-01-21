"""
Log to a file (simple)

Goal:
    - Keep timestamps + levels
    - Write logs to a file using basicConfig(filename=...)
    - (In this level, logs go to file, not both file+console)
"""


import logging
from pathlib import Path

def setup_logging(log_file: Path, verbose: bool=False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=str(log_file),
        filemode="a",    # append
    )
    
    
def main():
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    log_path = root / "playground" / "out" / "report.log"
    
    setup_logging(log_path, verbose=True)
    log = logging.getLogger(__name__)
    
    log.debug("DEBUG: goes to app.log")
    log.info("INFO: program started")
    log.warning("WARNING: sample warning")
    log.error("ERROR: sample error")
    log.critical("CRITICAL: sample critical")
    
    print(f"Log written to: {log_path}")
    
    

if __name__ == "__main__":
    main()
    
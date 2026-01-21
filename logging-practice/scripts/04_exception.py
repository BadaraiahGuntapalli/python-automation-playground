"""
logger.exception() (traceback logging)

Goal:
    - Use try/except
    - Log full traceback with log.exception(...)
"""

import logging
from pathlib import Path


def setup_logging(log_file: Path, verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=str(log_file),
        filemode="w",
    )

def risky_divide(a: float, b: float) -> float:
    return a / b
    
def main():
    # project root = parent of scripts/
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    log_path = project_root / "playground" / "out" / "app.log"
    
    setup_logging(log_path, verbose=True)
    log=logging.getLogger(__name__)
    log.info("Program started")
    
    #case 1: ok 
    try:
        x = risky_divide(10, 2)
        log.info(f"10/2 = {x}")
    except Exception:
        log.exception("Unexcepted error in 10/2")
        
    try:
        y = risky_divide(10, )
        log.info(f"10.0 = {y}")
    except Exception:
        log.exception("Crash in risky_divide(10, 0)")
    # except ValueError:
    #     raise print("divide by zero")
        
    log.info("Program finished")
    print(f"Done. check log file : {log_path}")
    
    
if __name__ == "__main__":
    main()
"""
Timing with time.perf_counter() 

Goal:
  - Time each step in a pipeline
  - Log step durations
  - Console INFO+, File DEBUG+ (timestamped log file per run)
"""

import logging
from pathlib import Path
from datetime import datetime
import time
from random_file import run_this



def setup_logging(log_path: Path, verbose: bool = False) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    console_level = logging.DEBUG if verbose else logging.INFO
    file_level = logging.DEBUG

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(filename)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # safe reset
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
    
    
def fake_work(seconds: float) -> None:
    time.sleep(seconds)
    
    
def main():
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = project_root / "playground" / "out" / "logs"
    log_path = log_dir / f"timing_{ts}.log"

    setup_logging(log_path, verbose=False)
    log = logging.getLogger(__name__)

    log.info("Pipeline started")
    log.info("Log file: %s", log_path)
    
    # ---------------- step 1 ----------------
    t0 = time.perf_counter()
    log.info("START: step_1_load_inputs")
    fake_work(0.4)
    dt = time.perf_counter() - t0
    log.info("END  : step_1_load_inputs | %.3f sec", dt)
    
    # ---------------- step 2 ----------------
    t0 = time.perf_counter()
    target = f"{run_this.__module__}.{run_this.__name__}"
    log.info("START: %s", target)
    run_this()
    dt = time.perf_counter() - t0
    log.info("END  : %s | %.3f sec", target, dt)

    # ---------------- step 3 ----------------
    t0 = time.perf_counter()
    log.info("START: step_3_write_outputs")
    fake_work(0.3)
    dt = time.perf_counter() - t0
    log.info("END  : step_3_write_outputs | %.3f sec", dt)

    log.info("Pipeline finished")
    print("Done. Log:", log_path)


if __name__ == "__main__":
    main()
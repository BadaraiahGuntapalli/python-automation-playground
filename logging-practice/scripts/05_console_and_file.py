"""
Console + File logging (handlers)

Goal:
  - Log to BOTH terminal and a file
  - Keep timestamps + levels
  - Keep exception traceback logging
"""

import logging
from pathlib import Path


def setup_logging(log_path: Path, verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Formatter: how each log line looks
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Root logger (global)
    root = logging.getLogger()
    root.setLevel(level)

    # Important: clear old handlers (prevents duplicate logs in re-runs)
    root.handlers.clear()

    # 1) Console handler (terminal)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # 2) File handler (app.log)
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    root.addHandler(fh)


def risky_divide(a: float, b: float) -> float:
    return a / b


def main():
    # project root = parent of scripts/
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    log_path = project_root / "playground" / "out" / "app01.log"

    setup_logging(log_path, verbose=True)
    log = logging.getLogger(__name__)

    log.info("Program started (Level 2.1)")

    # normal case
    log.info("10/2 = %s", risky_divide(10, 2))

    # error case
    try:
        risky_divide(10, 0)
    except Exception:
        log.exception("Crash in risky_divide(10, 0)")

    log.info("Program finished")
    print("Log file:", log_path)


if __name__ == "__main__":
    main()

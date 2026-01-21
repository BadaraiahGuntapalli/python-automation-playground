"""
LOGGING LEVEL 2.2 — Different levels per output

Goal:
  - Console shows INFO+ (clean)
  - File stores DEBUG+ (detailed)
  - Safe handler reset (remove + close)
"""

import logging
from pathlib import Path


def setup_logging(log_path: Path, verbose: bool = False) -> None:
    """
    verbose=False:
        console = INFO+, file = DEBUG+
    verbose=True:
        console = DEBUG+, file = DEBUG+
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Base levels (industry pattern)
    console_level = logging.DEBUG if verbose else logging.INFO
    file_level = logging.DEBUG

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # allow all; handlers do the filtering

    # Safe reset (important for reruns / Windows file locks)
    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # File handler
    fh = logging.FileHandler(str(log_path), encoding="utf-8", mode="w")
    fh.setLevel(file_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)


def demo_work():
    log = logging.getLogger(__name__)
    log.debug("DEBUG: details for debugging (goes to file, not console in normal mode)")
    log.info("INFO: normal progress")
    log.warning("WARNING: something odd but continuing")
    log.error("ERROR: something failed")


def main():
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    log_path = project_root / "playground" / "out" / "app02.log"

    # Change verbose to see console behavior
    setup_logging(log_path, verbose=True)

    log = logging.getLogger(__name__)
    log.info("Program started (Level 2.2)")

    demo_work()

    # show exception logging (still works)
    try:
        1 / 0
    except Exception:
        log.exception("Example crash: division by zero")

    log.info("Program finished")
    print("Log file:", log_path)


if __name__ == "__main__":
    main()

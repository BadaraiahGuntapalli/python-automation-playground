"""
Add timestamps (time + level + logger name + message)

Goal:
    - Add time to every log line (important for automation/debugging)
"""

import logging


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    setup_logging(verbose=True)

    # create logger object
    log = logging.getLogger(__name__)

    log.debug("DEBUG: developer details")
    log.info("INFO: normal progress message")
    log.warning("WARNING: something unexpected but continuing")
    log.error("ERROR: something failed but program may continue")
    log.critical("CRITICAL: serious failure, usually stop now")


if __name__ == "__main__":
    main()

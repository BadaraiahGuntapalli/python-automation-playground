"""
The 5 levels + basic config + verbose each 
    - Learn the core logging levels 
    - Learn how the configure logging output 
    - Leran how to the enabel DEBUG (verbose) vs INFO (normal)
"""


import logging 

def setup_logging(verbose: bool = False) -> None:
    """
    verbose=False -> INFO and above
    verbose=True -> DEBUG and above
    """
    
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(name)s | %(message)s",
    )
    
    
    
def main():
    # setting the logging 
    setup_logging(verbose=True)
    
    log = logging.getLogger(__name__)
    
    log.debug("DEBUG: developer details (normally hidden)")
    log.info("INFO: normal progress message")
    log.warning("WARNING: something unexpected but containing")
    log.error("ERROR: something failed but the program may continue")
    log.critical("CRITICAL: serious failure, usually stop now")
    
    log.critical("logging: controlled by log level (better for real tools)")
    
    
    
if __name__ == "__main__":
    main()
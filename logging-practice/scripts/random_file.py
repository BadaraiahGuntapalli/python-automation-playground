import numpy as np 
import logging 


log = logging.getLogger(__name__)
log.propagate = True

def run_this():
    log.info("Inside run_this: start")
    for i in np.arange(int(1e8)):
        continue
    
    log.info("Inside run_this: end")


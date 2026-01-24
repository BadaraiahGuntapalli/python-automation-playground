"""
    elpased time 
"""
import time

def main():
    
    # start time stamp 
    start_ts = time.time() 
    
    
    # human readable
    start_human = time.ctime(start_ts)
    
    print(f"Script started at : {start_human}")
    
    print("Simulating work ... ")
    
    time.sleep(3)
    
    end_ts = time.time()
    end_human = time.ctime(end_ts)
    
    elapsed = end_ts - start_ts
    
    print(f"Script ended at : {end_human}")
    print(f"time elapsed    :  {elapsed}")
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
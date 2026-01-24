"""
Wall clock time vs elapsed time 
    - use wall clock time for logging
    - use monotonic time for measuring duration
"""
import time

def main():
    # wall clock time 
    wall_start = time.time()
    wall_start_human = time.ctime(wall_start)
    
    # elapsed (monotonic) time for mesurement
    elapsed_start = time.perf_counter()
    
    print("script started at (wall clock):", wall_start_human)
    print("Simulating work...")
    
    # simulating the work 
    time.sleep(3)
    
    elapsed_end = time.perf_counter()
    wall_end = time.time()
    wall_end_human = time.ctime(wall_end)
    
    # compute elapsed duration
    elapsed_seconds = elapsed_end - elapsed_start
    
    print(f"Script ended at (wall clock): {wall_end_human}")
    print(f"Elapsed time (monotonic) : {elapsed_seconds:.3f}", "seconds")
    
    
    
    
    
if __name__ == "__main__":
    main()

    
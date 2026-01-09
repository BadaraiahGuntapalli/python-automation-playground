"""
computing the age of the file:
    - recent modificaion for a file
    - age in seconds 
"""

import os 
import time 

def main():
    script_path = os.path.abspath(__file__)
    
    target_dir = os.path.abspath(os.path.join(script_path,"..", "playground", "out"))
    
    if not os.path.isdir(target_dir):
        print("Target directory does not exit")
        return 

    now = time.time()
    print("perf counter :: ", time.perf_counter())
    print("raw timestamp :: ", time.time())
    
    print("Scanning directory: ", target_dir)
    print("-"*50)
    
    for name in os.listdir(target_dir):
        path = os.path.join(target_dir, name)
        
        if not os.path.isfile(path):
            continue
        
        try:
            mtime = os.path.getmtime(path)
        except OSError as e:
            print("Could not read the file {path}")
            continue
            
        
        age_seconds = now - mtime
        
        print("File: ", name) 
        print("Modified time: ", time.ctime(mtime))
        print("Age (sec) :", f"{age_seconds:0.2f}")
        print()
        
        
        
        
        
        
if __name__ == "__main__":
    main()
        
    
    
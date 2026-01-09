"""
File age categorization
    - Compute file age 
    - Classify files based on age thresholds
    - Print a clean automation style report
"""

import os 
from re import M
import time


def categories(age_seconds: float) -> str:
    if age_seconds < 60:
        return "FRESH"
    elif age_seconds < 1000 * 60:
        return "OLD"
    else:
        return "STALE"
    

def main():
    script_path = os.path.abspath(__file__)
    
    # set the target directory
    target_dir = os.path.abspath(os.path.join(script_path, "..", "playground", "out"))
    
    if not os.path.isdir(target_dir):
        print("Target directory not found")
        return 
    
    now = time.time()
    
    print("File age categorization")
    print("Directory : ", target_dir)
    print("-"*50)
    
    for name in os.listdir(target_dir):
        path = os.path.join(target_dir, name)
        
        if not os.path.isfile(path):
            continue
    
        try:
            mtime = os.path.getmtime(path)
        except OSError as e:
            print("Cound not read the time for {path} -> {e}")
            continue
        
        age_seconds = now - mtime
        category = categories(age_seconds=age_seconds)
        
        print(f"{name} | {category} | {age_seconds} sec")
        


if __name__ == "__main__":
    main()
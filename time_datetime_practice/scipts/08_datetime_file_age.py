"""
Datetime filesystem age logic
    - convert file modification time to datetime
    - compare with current datetime
    - classify files by age thresholds
"""

import os
from datetime import datetime, timedelta
from turtle import screensize

def categorize_by_age(file_dt: datetime, now: datetime) -> str:
    """
    Classify file age using datetiem comparisions.
    """
    if file_dt >= now - timedelta(days=1):
        return "RECENT"
    elif  file_dt >= now - timedelta(days=7):
        return "OLD"
    else:
        return "Expired"
    
    
def main():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        target_dir = os.path.join(script_dir, "..", "playground", "out")
        
        if not os.path.exists(target_dir):
            print("Target directory doesnot exists")
            print("Target directory: ", target_dir)
            return
        
        now = datetime.now()
        
        print("Datetime-based file age classification")
        print("Directory Path:", target_dir)
        print("current time: ", now)
        print("-"*70)
        
        for name in os.listdir(target_dir):
            path = os.path.join(target_dir, name)
            
            if not os.path.exists(path):
                continue
            
            try:
                mtime_ts = os.path.getmtime(path)
            except OSError:
                print("could not read the file time for : ", path)
                
            file_dt = datetime.fromtimestamp(mtime_ts)
            category = categorize_by_age(file_dt=file_dt, now=now)
            age_delta = now - file_dt
            
            print(f"{name:30} | {category} | age: {age_delta}")
            
            
            
if __name__ == "__main__":
    main()
                
        
        
        
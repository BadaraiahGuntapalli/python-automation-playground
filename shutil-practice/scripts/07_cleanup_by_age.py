"""
cleanup by age 
    - walk throught the directory
    - read the mtime 
    - categorize the file 
"""

from email.policy import default
import os 
import shutil
from datetime import date, datetime, timedelta

def parse_duration(s: str)-> timedelta:
    s = s.strip().lower()
    if s.endswith('m'):
        return timedelta(minutes=int(s[:-1]))
    elif s.endswith('h'):
        return timedelta(hours=timedelta[:-1])
    elif s.endswith('d'):
        return timedelta(days=int(s[:-1]))
    elif s.endswith('s'):
        return timedelta(seconds=int(s[:-1]))
    else:
        raise ValueError(f"Invalid duration format : {s}")

def main():
    DRY_RUN = True
    skipped = 0
    deleted = 0
    matched = 0
    
    now = datetime.now()
    OLDER_THAN = "1s"
    delta = parse_duration(OLDER_THAN)
    cutoff = now - delta
    
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))
    
    
    
    
    if not os.path.exists(target_dir):
        print(f"Target directory doesnot exits")
        return 
    
    for root, dirs, files in os.walk(target_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            
            try:
                mtime_ts = os.path.getmtime(fpath)
            except OSError as e:
                print(f"SKIP (mtime read failed) {fpath}")
                print(f"Reason: {e}")
                skipped += 1
                continue
                
            file_dt = datetime.fromtimestamp(mtime_ts)
            if file_dt > cutoff:
                continue
            
            matched += 1
            if DRY_RUN:
                print(f"[DRY] delete: {fpath} | modified: {file_dt}")
                continue
                
                
            try:
                os.remove(fpath)
                deleted += 1
                print(f"deleted: {fpath} | modified: {file_dt}")
            except OSError as e:
                print(f"SKIP (delete failed): {fpath}")
                print(f"Reason: {e}")
                skipped += 1
                
    print("-" * 70)
    print("Matched (older than cutoff):", matched)
    print("Deleted:", deleted)
    print("Skipped:", skipped)

    if DRY_RUN:
        print("⚠️ Set DRY_RUN = False to actually delete.")       
            
        
        
if __name__ == "__main__":
    main()        
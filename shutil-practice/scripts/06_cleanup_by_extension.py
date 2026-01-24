"""
Cleanup by extension (rule based)
    - Walk by directory tree
    - Delete files matching extensions
    - DRY RUN support
    - Clean summary output
"""

import os 
import shutil

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    
    target_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))
    
    DELETE_EXT = {".bat", ".apk", ".log"}
    delete_count = 0
    skipped_count = 0
    DRY_RUN = False
    
    if not os.path.exists(target_dir):
        print("Target directory does not exist")
        print(f"Target directory path : {target_dir}")
        return
    
    print("Cleaning from the Directory")
    print(f"Root directory : {target_dir}")
    print(f"DRY RUN : {DRY_RUN}")
    print("-" * 60)
    
    for root, dirs, files in os.walk(target_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in DELETE_EXT:
                continue
            
            fpath = os.path.join(root, fname)
            
            if DRY_RUN:
                print(f"[DRY] deleted : {fpath}")
                delete_count += 1
                continue
            
            try:
                print(f"deleted : {fpath}")
                os.remove(fpath)
                delete_count += 1
            except OSError as e:
                print(f"Skipped (deletion failed): {fpath}")
                print("Reason : {e}")
                skipped_count += 1
                continue
            
    print("-" * 60)
    print(f"Total files deleted : {delete_count}")
    print(f"Total files skipped : {skipped_count}")
    
    if DRY_RUN:
        print("Keep DRY RUN = False to actuall delete it")
    
            
            
if __name__ == "__main__":
    main()
                
        
        
    
    



































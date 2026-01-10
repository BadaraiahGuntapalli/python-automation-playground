"""
Clean up empty directories
    - Delete files by extension
    - Then remove empty directories (bottom-up)
    - DRY RUN support
"""

import os
import shutil
from tkinter.tix import ExFileSelectBox

def main():
    DRY_RUN = True
    DELETE_EXT = {".tmp", ".log", ".apk"}
    
    deleted_files = 0
    skipped = 0
    removed_dirs = 0
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))
    
    if not os.path.isdir(root_dir):
        print("Root directory doesnot exists")
        print(f"Root directory: {root_dir}")
        return
    
    for root, dirs, files in os.walk(root_dir):      
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()
            
            if ext not  in DELETE_EXT:
                continue
                
            if DRY_RUN:
                print(f"[DRY] delete: {fpath}")
                deleted_files += 1
                continue

            try:
                os.remove(fpath)
                print(f"deleted: {fpath}")
            except OSError as e:
                print("SKIP (deletion failed)")
                print(f"file path: {fpath}")
                skipped += 1
                continue
        
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if root == root_dir:
            continue
        
        try:
            if not os.listdir(root):
                if DRY_RUN:
                    print(f"[DRY] rmdir: {root}")
                    removed_dirs += 1
                    continue
                else:
                    os.rmdir(root)
                    print(f"rmdir: {root}")
                    removed_dirs += 1
                    
        except OSError as e:
            print(f"SKIP (rmdir failed) : {root}")
            print(f"Reason: {e}")
            skipped += 1
            
    print("-" * 70)
    print("Matched/deleted files:", deleted_files)
    print("Removed empty dirs    :", removed_dirs)
    print("Skipped               :", skipped)
    if DRY_RUN:
        print("⚠️ Set DRY_RUN = False to actually delete/remove.")


if __name__ == "__main__":
    main()    
                    
            
            
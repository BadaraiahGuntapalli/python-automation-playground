"""
Copying the folder and all its subfolders
"""

import os 
import shutil


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # select the source and destination paths for the folders
    src_dir = os.path.join(script_dir, "..", "playground", "data")
    dst_dir = os.path.join(script_dir, "..", "playground", "out", "backup")
    
    if not os.path.isdir(src_dir):
        print("Source directory doesnot exists")
        print(f"Source path : {src_dir}")
        return

    if os.path.isdir(dst_dir):
        print("Destination directory already exits. Aborting copying")
        print(f"Destination path: {dst_dir}")
        return
    
    shutil.copytree(src_dir, dst_dir)
    
    
    print("Directory copied")
    print(f"From :{src_dir}")
    print(f"To  : {dst_dir}")   
    
    
if __name__ == "__main__":
    main() 
    
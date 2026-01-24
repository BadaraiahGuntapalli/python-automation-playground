"""
Copy a file safely
    - Copy a file from playground/data to playground/out
    - Rename during copy
    - Avoid accidental overwrite
"""

import os 
import shutil

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(script_dir, "..", "playground", "data")
    out_dir = os.path.join(script_dir, "..", "playground", "out")
    
    os.makedirs(out_dir, exist_ok=True)
    
    src_file = os.path.join(data_dir, "sample.txt")
    dst_file = os.path.join(out_dir, "sample_copy.txt")
    
    if not os.path.isfile(src_file):
        print("source file doesnot exist")
        print(f"source path: {src_file}")
        return
        
    if os.path.isfile(dst_file):
        print("Destination file already exists. Aborting copy ")
        return
    
    shutil.copy(src_file, dst_file)
    
    print("File copied successfully")
    print(f"From : {src_file}" )
    print(f"To   : {dst_file}")
    
    
    
    
if __name__ == "__main__":
    main()
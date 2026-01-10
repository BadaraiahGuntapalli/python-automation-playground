"""
Move a file 
    - Move a file from data/ to out/
    - rename the moved file
    - move safely 
"""


import os 
import shutil


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "data"))
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))
    
    src_file = os.path.abspath(os.path.join(data_dir, "move_file.txt"))
    dst_file = os.path.abspath(os.path.join(out_dir, "moved_dst_file.txt"))
    
    if not os.path.isfile(src_file):
        print("File doesnot exit")
        print("Move file :", src_file)
        return 
    
    if os.path.isfile(dst_file):
        print("File alredy exist. Operation aborted.")
        return
    
    shutil.move(src_file, dst_file)
    
    print("Move operation succeded")
    print("From :", src_file)
    print("To : ", dst_file)
    
    
if __name__ == "__main__":
    main()
    
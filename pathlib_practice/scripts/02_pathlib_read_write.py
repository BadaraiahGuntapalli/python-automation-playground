"""
PATHLIB — Read & write files

Goal:
    - Read a text file using pathlib
    - Write a timestamped copy to out/
"""

from pathlib import Path
from datetime import datetime

def main():
    script_dir = Path(__file__).resolve().parent
    
    # resolve the absolute paths
    data_dir = (script_dir / ".." / "playground" / "data").resolve()
    out_dir = (script_dir / ".." / "playground" / "out").resolve()
    
    src_file = data_dir / "meta_data.txt"
    
    if not src_file.exists():
        print(f"File does not exist : {src_file}")
        return 
    
    # time stamp the file name 
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst_file = out_dir / f"meta_data_out_{ts}.txt"
    
    # read text 
    text = src_file.read_text(encoding="utf-8")
    
    # write text to the destination file
    dst_file.write_text(text, encoding="utf-8")
    
    print("File copied using pathlib:")
    print(f"From: {src_file}")
    print(f"To: {dst_file}")
    
    
    
if __name__ == "__main__":
    main()
    
    
    
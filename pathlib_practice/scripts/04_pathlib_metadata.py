"""
File metadata

Goal:
    - Read file size and modification time using pathlib
"""


from pathlib import Path 
from datetime import datetime





def bytes_to_human(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n)
    for u in units:
        if size < 1024.0:
            return f"{size:.2f} {u}"
        size /= 1024.0
    return f"{size:.2f} PB"




def main():
    script_dir = Path(__file__).resolve().parent
    out_dir = (script_dir / ".." / "playground" / "out").resolve()
    
    if not out_dir.is_dir():
        print("Directory does not exist")
        print(out_dir)
        return 
    
    for p in out_dir.rglob("*.txt"):
        if not p.is_file():
            continue
        
        file_stat = p.stat()
        
        ts = datetime.fromtimestamp(file_stat.st_mtime)
        file_size = file_stat.st_size
        human_readable = bytes_to_human(n=file_size)
        
        print(f"file: {p.name} | modified : {ts} | size: {human_readable} ")
        
        


if __name__ == "__main__":
    main()
        
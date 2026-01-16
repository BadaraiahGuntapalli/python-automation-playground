"""
Directory scan report

Goal:
    - Recursively scan playground/out
    - Summarize file counts, sizes, extensions
    - List top 10 largest files
    - Write a report to out/pathlib_report.txt
"""

from pathlib import Path
from collections import Counter
from datetime import datetime 

def bytes_to_human(filesz: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(filesz)
    for u in units:
        if size < 1024:
            return f"{size} {u}"
        size /= 1024
    return f"{size} PB"




def main():
    script_dir = Path(__file__).resolve().parent
    out_dir = (script_dir / ".." / "playground" / "out").resolve()
    
    if not out_dir.exists():
        print("Directory does not exist")
        print(out_dir)
        return 
    
    all_files = []
    total_bytes = 0
    ext_counts = Counter()
    
    for p in out_dir.rglob("*"):
        if not p.is_file():
            continue
        try:
            st = p.stat()
        except OSError as e:
            print("SKIP (stat failed)", p, "Reason : ", e)
            continue
        
        sz = st.st_size
        total_bytes += sz
        
        ext = p.suffix.lower() if p.suffix else "(no_ext)"
        ext_counts[ext] += 1
        
        all_files.append((p, sz))
        
    # Top 10 largest
    all_files.sort(key=lambda x: x[1], reverse=True)
    top2 = all_files[:2]
    
    report_path = out_dir / "directory_report.txt"
    
    with report_path.open("w", encoding="utf-8") as f:
        f.write("Directory scan report\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Root      : {out_dir}\n\n")
        
        f.write(f"Total files: {len(all_files)}\n")
        f.write(f"Total size : {total_bytes} bytes ({bytes_to_human(total_bytes)})\n")
        
        f.write("Counts by extension\n")
        f.write("-" * 70 + "\n")
        for ext, cnt in ext_counts.most_common():
            f.write(f"{ext:10} : {cnt} \n")
            
        f.write("\nTop 2 largest files \n")
        f.write("-" * 70 + "\n")
        for p, sz in top2:
            f.write(f"{p.relative_to(out_dir)} | {bytes_to_human(sz)}\n")
        
        
        print("Report written to:")
        print(report_path)
        
        
        
if __name__ == "__main__":
    main()        
"""
Path anchoring + checks
    - Build paths releative to the script
    - Check existence, is_file, is_dir
    - Create output directory safely
"""

from pathlib import Path

def main():
    # directory containing the script
    script_dir = Path(__file__).resolve().parent
    
    # Build repo-relative paths
    data_dir = (script_dir / ".." / "playground" / "data").resolve()
    out_dir = (script_dir / ".." / "playground" / "out").resolve()
    
    print(f"Script dir: {script_dir}")
    print(f"Data dir: {data_dir}")
    print(f"Out dir: {out_dir}")
    print("-" * 60)
    
    # Ensure out_dir exists
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"data_dir exist : {data_dir.exists()} | is_dir? : {data_dir.is_dir()}")
    print(f"out_dir exist? : {out_dir.exists()} | is_dir? : {out_dir.is_dir()}")
    
    # Example file path 
    sample_file = data_dir / "sample.txt"
    print("sample.txt path :", sample_file)
    print("smaple.txt exists?: ", sample_file.exists(), "| is_file(): ", sample_file.is_file())
    
    
if __name__ == "__main__":
    main()
    
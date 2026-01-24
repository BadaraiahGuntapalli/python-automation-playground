"""
    Inspect path safety before using them.
"""
from genericpath import isfile
import os

def describe_path(path: str)-> str:
    if not os.path.exists(path):
        return "MISSING"
    
    if os.path.isfile(path):
        return "FILE"
    
    if os.path.isdir(path):
        return "DIRECTORY"
    
    return "UNKNOWN"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    paths = [
        script_dir,
        os.path.join(script_dir, "..", "playground"),
        os.path.join(script_dir, "not_there.txt"),
    ]
    
    for p in paths:
        p = os.path.abspath(p)
        status = describe_path(p)
        print(f"p -> {status}")
        
        

if __name__ == "__main__":
    main()
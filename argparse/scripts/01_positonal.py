"""
Positional arguments
    - Accept a directory path from the command line
    - validate it exists
"""

import argparse
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Accept a directory path and validate it"
    )
    
    parser.add_argument(
        "root",
        help="Root directory to inspect"
    )
    
    args = parser.parse_args()
    
    root = Path(args.root).expanduser().resolve()
    
    if not root.is_dir():
        print("Error: not a directory", root)
        sys.exit(2)
        
    print("OK: Directory exists:")
    print(root)
    
    
if __name__ == "__main__":
    main()
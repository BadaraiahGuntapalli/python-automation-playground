"""
— sys.argv

Goal:
    - Read command-line arguments
    - Validate required input
    - Exit with a non-zero code on error
"""

import sys

def main():
    print("Raw argv :", sys.argv)
    if len(sys.argv) < 2:
        print("Error: missing argument")
        print("Usage: python scripts/02_sys_argv.py")
        sys.exit(1)
        
    name = sys.argv[1]
    print(f"Hello, {name}")
    
    # success
    sys.exit(0)
    
if __name__ == "__main__":
    main()
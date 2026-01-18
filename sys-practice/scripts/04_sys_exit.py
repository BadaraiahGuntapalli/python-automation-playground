"""
— sys.exit

Goal:
    - Exit with proper status codes
    - Signal success or failure to the OS
"""
from http.client import TOO_EARLY
import sys


def main():
    if len(sys.argv) < 2:
        print("ERROR: missing argument")
        sys.exit(1) # non-zero = failure
        
    try:
        value = int(sys.argv[1])
    except ValueError:
        print("Error: argument must be an integer")
        sys.exit(2)
        
    if value < 0:
        print("Error: number must be non-negative")
        sys.exit(3)
        
    print("Success! value accepted: ", value)
    sys.exit(0) # success
    


if __name__ == "__main__":
    main()

        
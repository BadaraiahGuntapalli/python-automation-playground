"""
— sys.executable

Goal:
    - Print the absolute path of the Python interpreter
    - Understand why this matters for automation
"""

import sys


def main():
    print("Python executable path:")
    print(sys.executable)
    
    print("\nWhy this matters:")
    print("- Ensures correct Python in virtualenv / conda")
    print("- Prevents hardcoding 'python'")
    print("- Safe for subprocess usage")
    
    
    
if __name__ == "__main__":
    main()
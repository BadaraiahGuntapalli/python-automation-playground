"""
walk through a directory and print every directory and file full paths.

"""

from logging import root
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_dir = os.path.join(script_dir, "..", "playground", "data")
    root_dir = os.path.abspath(root_dir)
    
    if not os.path.exists(root_dir):
        print("Root directory not exist")
        print(root_dir)
        return 
    
    print("Walking throught the root directory")
    print(root_dir)
    print("="*50)
    
    for root, dirs, files in os.walk(root_dir):
        print(f"\nCurrent directory:")
        print(root)
        
        print("Sub-directories")
        for d in dirs:
            print(" ", os.path.join(root, d))
        
        print("Files: ")
        for f in files:
            print(" ", os.path.join(root, f))
            
            
if __name__ == "__main__":
    main()
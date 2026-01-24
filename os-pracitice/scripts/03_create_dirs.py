"""
Goal:
    Create output folder safely without crashing if it already exists.
"""

import os 


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    out_dir = os.path.join(script_dir, "..", "playground", "out", "logs")
    out_dir = os.path.abspath(out_dir)
    
    os.makedirs(out_dir, exist_ok=True)
    
    print("output directory ready")
    print(out_dir)
    
    
    
if __name__ == "__main__":
    main()
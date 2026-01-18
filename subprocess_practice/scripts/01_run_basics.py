"""
Run a command and capture output 

    - Run a command safely (list of args)
    - Capture stdout/stderr
    - Print return code
    - Cross-platform examples
"""

from pdb import run
import subprocess
import sys

def run_and_print(cmd: list[str]) -> None:
    print("Running", cmd)
    
    # create the result object
    result = subprocess.run(
        cmd,
        capture_output=True,    # capture stdout + stderr
        text=True               # decode bytes -> str
    )
    
    print("Return code: ", result.returncode)
    print(result.stdout)
    print(result.stderr)
    
    if result.stdout:
        print("STDOUT")
        print(result.stdout.rstrip())
        
        
    if result.stderr:
        print("STDERR")
        print(result.stderr.rstrip())
        
        
        
    print("-" * 50)
    
    
    
def main():
    run_and_print([sys.executable, "--version"])

    if sys.platform.startswith("win"):
        run_and_print(["cmd", "/c", "dir"])
    else:
        run_and_print(["ls", "-la"])
        
    
    
if __name__ == "__main__":
    main()
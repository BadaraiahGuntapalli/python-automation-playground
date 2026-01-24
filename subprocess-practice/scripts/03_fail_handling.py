"""
Failure handling with check=True
    - Run a command that will fail
    - Catch CalledProcessError
    - Print return code, stdout, stderr
    - Exit with the same non-zero code
"""

import subprocess
import sys

def main():
    # This is a cross-platform "controlled failure" for learning.
    cmd = [sys.executable, "-c", "import sys; sys.exit(7)"]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("This line will not run (because command exist with 7)")
    except subprocess.CalledProcessError as e:
        print("Caught failure (as expected)")
        print("Return code: ", e.returncode)
        
        if e.stdout:
            print("STDOUT: ")
            print(e.stdout.rstrip())
            
            
        if e.stderr:
            print("STDERR: ")
            print(e.stderr.rstrip())
            
            
        sys.exit(e.returncode)
        
        
        
        
if __name__ == "__main__":
    main()
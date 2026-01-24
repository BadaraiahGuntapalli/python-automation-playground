"""
Timeouts and graceful termination

Goal:
    - Run a command with a timeout
    - Catch TimeoutExpired
    - Report partial output safely
"""

import subprocess
import sys

def main():
    cmd=[
        sys.executable,
        "-c",
        "import time; print('starting...'); time.sleep(10);print('Done')"
    ]
    
    print("Running command with timeout=3 seconds")
    print(f"command: {cmd}")
    print("-" * 50)
    
    try:
        result=subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3,
            check=True
        )
        print("Command finished successfully")
        print("STDOUT", result.stdout.rstrip())
        
    except subprocess.TimeoutExpired as e:
        print("Command timed out")
        print("Timeout (seconds): ", e.timeout)
        
        # partial out (may exit)
        if e.stdout:
            print("PARTIAL STDOUT")
            print(e.stdout.rstrip())
            
        if e.stderr:
            print("PARTIAL STDERR")
            print(e.stderr.rstrip())
            
        sys.exit(124)
        
        
    except subprocess.CalledProcessError as e:
        print("Command failed!")
        print("Return code:", e.returncode)
        if e.stderr:
            print("STDERR:", e.stderr.rstrip())
        sys.exit(e.returncode)
        
        
        
        
if __name__== "__main__":
    main()
        
    
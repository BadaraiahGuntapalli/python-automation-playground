"""
— cwd + output redirection

Goal:
    - Run a command in a specific directory
    - Redirect stdout to a file
    - Capture stderr
"""

import subprocess
import sys
from pathlib import Path


def main():
    script_dir = Path(__file__).resolve().parent

    # Choose a working directory (safe example)
    work_dir = (script_dir / ".." / "playground").resolve()

    if not work_dir.is_dir():
        print("ERROR: working directory does not exist:")
        print(work_dir)
        sys.exit(1)

    out_file = work_dir / "subprocess_ls_output.txt"

    # Cross-platform directory listing command
    if sys.platform.startswith("win"):
        cmd = ["cmd", "/c", "dir"]
    else:
        cmd = ["ls", "-la"]

    print("Running:", cmd)
    print("Working directory:", work_dir)
    print("Output file:", out_file)

    with out_file.open("w", encoding="utf-8") as f:
        try:
            subprocess.run(
                cmd,
                cwd=work_dir,      # run command INSIDE this directory
                stdout=f,          # redirect stdout to file
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print("Command failed!")
            print("Return code:", e.returncode)
            if e.stderr:
                print("STDERR:")
                print(e.stderr.rstrip())
            sys.exit(e.returncode)

    print("Command completed successfully.")
    print("Output written to:", out_file)


if __name__ == "__main__":
    main()

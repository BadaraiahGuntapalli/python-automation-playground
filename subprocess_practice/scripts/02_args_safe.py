"""
— Safe arguments + check=True

Goal:
    - Read one argument from CLI
    - Pass it safely to a subprocess command
    - Avoid shell=True
    - Use check=True to catch failures
"""

import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/26_subprocess_args_safe.py <name>")
        sys.exit(1)

    name = sys.argv[1]

    # Cross-platform: use Python itself to print a message
    # This avoids OS-specific commands and shows safe argument passing.
    cmd = [sys.executable, "-c", "import sys; print('Hello from subprocess,', sys.argv[1])", name]

    print("Running:", cmd)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,   # if returncode != 0, raises CalledProcessError
        )
    except subprocess.CalledProcessError as e:
        print("Command failed!")
        print("Return code:", e.returncode)
        if e.stdout:
            print("STDOUT:", e.stdout.rstrip())
        if e.stderr:
            print("STDERR:", e.stderr.rstrip())
        sys.exit(e.returncode)

    print("Success")
    print("STDOUT:", result.stdout.rstrip())
    if result.stderr:
        print("STDERR:", result.stderr.rstrip())


if __name__ == "__main__":
    main()

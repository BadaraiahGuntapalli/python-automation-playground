"""
SYS LEVEL 1.3 — sys.platform

Goal:
    - Detect the operating system
    - Branch logic based on OS
"""

import sys


def main():
    platform = sys.platform
    print("sys.platform:", platform)

    if platform.startswith("win"):
        print("Running on Windows")
        print("Typical commands: dir, copy, del")
    elif platform.startswith("linux"):
        print("Running on Linux")
        print("Typical commands: ls, cp, rm")
    elif platform == "darwin":
        print("Running on macOS")
        print("Typical commands: ls, cp, rm")
    else:
        print("Unknown platform")

    print("\nWhy this matters:")
    print("- subprocess commands differ by OS")
    print("- paths and tools behave differently")
    print("- automation must be portable")


if __name__ == "__main__":
    main()

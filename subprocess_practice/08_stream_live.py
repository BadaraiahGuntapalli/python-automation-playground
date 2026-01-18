"""
SUBPROCESS LEVEL 2.4 — Stream live output

Goal:
    - Start a subprocess
    - Read stdout line-by-line in real time
    - Print as it arrives (live logs)
    - Handle return code
"""

import subprocess
import sys
import time


def main():
    # Child process: prints progress lines slowly (flush=True is critical)
    cmd = [
        sys.executable,
        "-c",
        (
            "import time\n"
            "for i in range(10):\n"
            "    print(f'progress {i}/10', flush=True)\n"
            "    time.sleep(0.5)\n"
            "print('done', flush=True)\n"
        )
    ]

    print("Starting process with live output streaming...")
    print("Command:", cmd)
    print("-" * 60)

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,          # line-buffered (best effort)
        universal_newlines=True
    )

    # Stream stdout live
    assert p.stdout is not None
    for line in p.stdout:
        print("[LIVE]", line.rstrip())

    # After stdout ends, wait for process to finish and collect stderr
    rc = p.wait()
    stderr = ""
    if p.stderr is not None:
        stderr = p.stderr.read()

    print("-" * 60)
    print("Return code:", rc)

    if stderr.strip():
        print("STDERR:")
        print(stderr.rstrip())

    if rc != 0:
        sys.exit(rc)

    print("Process completed successfully")


if __name__ == "__main__":
    main()

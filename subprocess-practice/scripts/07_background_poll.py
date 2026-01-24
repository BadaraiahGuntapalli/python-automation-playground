"""
Background process + polling + termination

Goal:
    - Start a background process (Popen)
    - Poll until it finishes or times out
    - Terminate safely if needed
    - Capture stdout/stderr
"""

import subprocess
import sys
import time


def main():
    # Child process: prints a line every second for 20 seconds
    cmd = [
        sys.executable,
        "-c",
        (
            "import time\n"
            "for i in range(20):\n"
            "    print(f'tick {i}', flush=True)\n"
            "    time.sleep(1)\n"
        )
    ]

    MAX_SECONDS = 5  # stop after 5 seconds

    print("Starting background process:")
    print("Command:", cmd)
    print("Max runtime:", MAX_SECONDS, "seconds")
    print("-" * 60)

    # Start process in background
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    start = time.time()

    # Poll loop (non-blocking)
    while True:
        rc = p.poll()  # None if still running, else return code
        elapsed = time.time() - start

        if rc is not None:
            print("Process finished. Return code:", rc)
            break

        print(f"Still running... elapsed={elapsed:.1f}s")
        if elapsed >= MAX_SECONDS:
            print("⏱️ Timeout reached. Terminating process...")
            p.terminate()  # ask it to stop
            break

        time.sleep(1)

    # Collect output (waits for process to exit)
    try:
        stdout, stderr = p.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        print("Process did not terminate in time. Killing it...")
        p.kill()
        stdout, stderr = p.communicate()

    print("-" * 60)
    print("STDOUT:")
    print(stdout.rstrip() if stdout else "(empty)")

    if stderr:
        print("-" * 60)
        print("STDERR:")
        print(stderr.rstrip())

    print("-" * 60)
    print("Final return code:", p.returncode)

    # If you want to signal failure upward:
    if p.returncode not in (0, None):
        sys.exit(p.returncode)


if __name__ == "__main__":
    main()

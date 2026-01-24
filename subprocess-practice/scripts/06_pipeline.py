"""
Pipelines (stdout -> stdin)

Goal:
    - Pipe output of one command into another
    - Avoid shell=True
    - Capture final output safely
"""

import subprocess
import sys

import subprocess
import sys


def main():
    # Command A: produce output (cross-platform using Python)
    # Prints multiple lines
    cmd_producer = [
        sys.executable,
        "-c",
        "print('apple'); print('banana'); print('cherry'); print('date')"
    ]

    # Command B: consume input and process it
    # Filters lines containing the letter 'a'
    cmd_consumer = [
        sys.executable,
        "-c",
        (
            "import sys\n"
            "for line in sys.stdin:\n"
            "    if 'a' in line:\n"
            "        print(line.strip())"
        )
    ]

    print("Producer:", cmd_producer)
    print("Consumer:", cmd_consumer)
    print("-" * 60)

    # Start producer
    p1 = subprocess.Popen(
        cmd_producer,
        stdout=subprocess.PIPE,
        text=True
    )

    # Pipe producer stdout -> consumer stdin
    p2 = subprocess.Popen(
        cmd_consumer,
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # Important: allow p1 to receive SIGPIPE if p2 exits early
    p1.stdout.close()

    # Collect final output
    output, _ = p2.communicate()

    print("Pipeline output:")
    print(output.rstrip())

    # Wait for processes to finish
    rc1 = p1.wait()
    rc2 = p2.wait()

    print("-" * 60)
    print("Producer return code:", rc1)
    print("Consumer return code:", rc2)

    if rc1 != 0 or rc2 != 0:
        print("Pipeline failed!")
        sys.exit(1)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
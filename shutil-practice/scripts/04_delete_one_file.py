"""
SHUTIL LEVEL 2.1 — Delete a single file safely

Goal:
    - Delete one file in playground/out
    - DRY RUN support (no deletion)
    - Clear logs
"""

import os


def main():
    DRY_RUN = True  # set False to actually delete

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))

    target_file = os.path.join(out_dir, "delete_me.tmp")

    if not os.path.isdir(out_dir):
        print("ERROR: out directory does not exist:")
        print(out_dir)
        return

    if not os.path.exists(target_file):
        print("Nothing to delete (file not found):")
        print(target_file)
        return

    if not os.path.isfile(target_file):
        print("ERROR: target exists but is not a file:")
        print(target_file)
        return

    if DRY_RUN:
        print("[DRY RUN] Would delete file:")
        print(target_file)
        return

    try:
        os.remove(target_file)
        print("Deleted file:")
        print(target_file)
    except OSError as e:
        print("ERROR: failed to delete file:")
        print(target_file)
        print("Reason:", e)


if __name__ == "__main__":
    main()

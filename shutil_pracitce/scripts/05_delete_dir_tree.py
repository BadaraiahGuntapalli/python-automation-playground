"""
SHUTIL LEVEL 2.2 — Delete a directory tree safely

Goal:
    - Delete a directory and all its contents
    - DRY RUN support
    - Strong safety checks
"""

import os
import shutil

def on_rm_error(func, path, exc_info):
    """
    Error handler for shutil.rmtree.
    Tries to remove read-only attribute and retry.
    """
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print("Still failed to delete:", path)
        print("Reason:", e)


def main():
    DRY_RUN = False  # ⚠️ set False only after verifying

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))

    target_dir = os.path.join(out_dir, "delete_me_dir")

    # 1️⃣ Validate out directory
    if not os.path.isdir(out_dir):
        print("ERROR: out directory does not exist:")
        print(out_dir)
        return

    # 2️⃣ Validate target directory
    if not os.path.exists(target_dir):
        print("Nothing to delete (directory not found):")
        print(target_dir)
        return

    if not os.path.isdir(target_dir):
        print("ERROR: target exists but is not a directory:")
        print(target_dir)
        return

    # 3️⃣ Dry run
    if DRY_RUN:
        print("[DRY RUN] Would delete directory tree:")
        print(target_dir)
        return

    # 4️⃣ Actual deletion
    try:
        shutil.rmtree(target_dir, onexc=on_rm_error)
        print("Deleted directory tree:")
        print(target_dir)
    except OSError as e:
        print("ERROR: failed to delete directory:")
        print(target_dir)
        print("Reason:", e)


if __name__ == "__main__":
    main()

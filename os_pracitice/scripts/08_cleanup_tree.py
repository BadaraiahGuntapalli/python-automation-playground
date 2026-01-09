"""
Goal: Safe cleanup of directories
- Remove the files with the matching extensions  
- remove the empyty directories
- do the dry run
- write a clean report
"""

import os 
import time

def bytes_to_human(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "PB"]
    size = float(n)
    for u in units:
        if size < 1024:
            return f"{size} {u}"
    size /= 1024
    return f"{size} PB"

def main():
    # current script path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # choose where to delete 
    root_dir = os.path.abspath(os.path.join(script_dir, "..", "playground", "out"))

    # choose where to report 
    report_path = os.path.join(root_dir, "clean_report.txt")

    DELETE_EXT = {".log", ".bak", ".tmp"}
    DRY_RUN = True
    REMOVE_EMPTY_DIRS = True
    OLDER_THAN_DAYS = None

    if not os.path.exists(root_dir):
        print("ERROR: clean up root directory doesnot exist")
        return 

    now = time.time()
    deleted = []
    skipped = []
    total_freed = 0
    

    print("claenup root", root_dir)
    print("Dry run: ", DRY_RUN)
    print("Delete extentoin list: ", sorted(DELETE_EXT))
    print("Older than days: ", OLDER_THAN_DAYS)
    print("-"*50)

    # 1) walking through the root dir
    for root, dirs, files in os.walk(root_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()

            if ext not in DELETE_EXT:
                continue
                
            if OLDER_THAN_DAYS is not None:
                try:
                    mtime = os.path.getmtime(fpath)
                except OSError as e:
                    skipped.append((fpath, f"mtime read failed: {e}"))
                    continue

                age_days = (now - mtime) / (24 * 3600)
                if age_days < OLDER_THAN_DAYS:
                    continue

            # size 
            try:
                size = os.path.getsize(fpath)
            except OSError as e:
                skipped.append((fpath, f"size read failed {e}"))
                continue
            
            # delete or simulate
            if DRY_RUN:
                print("[DRY] delete:,", fpath)
            else:
                try:
                    os.remove(fpath)
                    print("deleted:", fpath)
                except OSError as e:
                    skipped.append((fpath, f"delete failed: {e}"))
                    continue

            deleted.append((fpath, size))
            total_freed += size

    # remove the directories
    removed_dirs = []
    if REMOVE_EMPTY_DIRS:
        for root, dirs, files in os.walk(root_dir, topdown=False):
            # do not remove the root dir itself 
            if root == root_dir:
                continue
            
            try:
                if not os.listdir(root):
                    if DRY_RUN:
                        print("[DRY] rmdir:", root)
                    else:
                        os.rmdir(root)
                        print("rmdir :", root)
                    removed_dirs.append(root)
            except OSError as e:
                skipped.append((root, f"rmdir check/remove failed: {e}"))

    # 3) write report
    os.makedirs(root_dir, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("CLEAN REPORT\n")
        f.write("-" * 50 + "\n\n")
        f.write(f"Root: {root_dir}\n")
        f.write(f"Dry run: {DRY_RUN}\n")
        f.write(f"Delete extensions: {sorted(DELETE_EXT)}\n")
        f.write(f"Older than days: {OLDER_THAN_DAYS}\n\n")

        f.write(f"Deleted files: {len(deleted)}\n")
        f.write(f"Freed Space : {total_freed} bytes ({bytes_to_human(total_freed)})\n")
        f.write(f"Removed dirs: {len(removed_dirs)}\n")
        f.write(f"skipped   : {len(skipped)}\n\n")

        f.write("DELETED FILES\n")
        f.write("-"*50 + "\n")
        for p, sz in deleted:
            f.write(f"{p} ({bytes_to_human(sz)})\n")

        f.write("\nREMOVED DIRECTORIES")
        f.write("-"*50 + "\n")
        for d in removed_dirs:
            f.write(f"{d}\n")

        if skipped:
            f.write("\n skipped / Errors \n")
            f.write("-" * 50 + "\n")
            for p, reason in skipped:
                f.write(f"{p} -> {reason}\n")


    print("-" * 50)
    print("Report written to:", report_path)
    print("Deleted files:", len(deleted))
    print("Freed:", bytes_to_human(total_freed))
    print("Removed dirs:", len(removed_dirs))
    print("Skipped:", len(skipped))
    print("\n⚠️ Set DRY_RUN = False only after you verify the dry-run output.")

        
if __name__ == "__main__":
    main()












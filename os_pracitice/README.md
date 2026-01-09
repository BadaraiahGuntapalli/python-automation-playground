Perfect. Here’s a **beginner → professional** `os` practice set that you can do **directly in `.py` files** in VS Code. Each item is a *real automation micro-tool* (industry style), not random syntax.

## Setup (do this once)

Create this folder structure:

```
os_practice/
├─ playground/
│  ├─ data/        # put some dummy files/folders here
│  ├─ out/
├─ scripts/
```

You’ll write files in `scripts/`.

---

# Level 1 — Must-know basics (core automation)

### 1) Current working directory + script directory

**Methods:** `os.getcwd()`, `__file__`, `os.path.dirname`, `os.path.abspath`

**Task:** Print:

* current working directory (CWD)
* directory where the script lives (SCRIPT_DIR)
* show difference

Why pro? CWD bugs are #1 automation failure.

---

### 2) List directory contents (names vs full paths)

**Methods:** `os.listdir()`, `os.path.join()`

**Task:** List all entries in `playground/data` and print full paths.

Pro habit: never work with bare filenames.

---

### 3) Create folders safely

**Methods:** `os.makedirs(exist_ok=True)`

**Task:** Create `playground/out/logs/` every run without crashing.

This is how pipelines generate results folders.

---

### 4) Existence checks (defensive programming)

**Methods:** `os.path.exists`, `os.path.isfile`, `os.path.isdir`

**Task:** Given a path, print whether it’s file/dir/missing.

Pro habit: validate inputs always.

---

# Level 2 — Industry-grade filesystem traversal

### 5) Recursive walk (the workhorse)

**Methods:** `os.walk()`

**Task:** Walk `playground/data`, count:

* total files
* total folders
* total bytes (use `os.path.getsize`)

This is real “dataset scanner” logic.

---

### 6) Filter files by extension + write report

**Methods:** `os.walk`, `os.path.splitext`, file I/O

**Task:** Find all `.csv` (or `.txt`) files and write a report to `playground/out/report.txt`.

Automation pattern: scan → filter → report.

---

### 7) Rename files safely (batch rename tool)

**Methods:** `os.rename`, `os.path.exists`

**Task:** Rename all files matching pattern:

* spaces → underscores
* lowercase names

Pro rule: don’t overwrite; if target exists, skip + log.

---

# Level 3 — Environment & process control (professional automation)

### 8) Environment variables (config without hardcoding)

**Methods:** `os.environ.get`, `os.environ[...]`

**Task:** Read an env var like `PROJECT_ROOT`.

* If missing: fall back to script directory
* Print which one you used

This is how real systems are configured.

---

### 9) Run a command (quick system integration)

**Method:** `os.system()` *(ok for practice)*

**Task:** Run a command that lists directory contents:

* Windows: `dir`
* Linux/macOS: `ls`

(Next step later: `subprocess` for real industry.)

---

### 10) Exit codes (automation pipelines depend on this)

**Method:** `sys.exit()` (yes it’s `sys`, but essential)

**Task:** If `playground/data` doesn’t exist → exit with code 2.

This is how cron/CI knows your script failed.

---

# Level 4 — Metadata & permissions (useful in real ops)

### 11) File metadata

**Methods:** `os.stat`, `os.path.getmtime`, `os.path.getsize`

**Task:** For each file in `playground/data`, print:

* size
* modified time

Used for cleanup + monitoring.

---

### 12) Cleanup tool (safe delete)

**Methods:** `os.remove`, `os.rmdir`

**Task:** Delete only `.tmp` files inside `playground/out`.
If a folder is empty, remove it.

(For recursive delete trees, we’ll use `shutil` next.)

---

# The “professional practice rule” (this makes it stick)

For every script:

1. Have `main()`
2. Use `SCRIPT_DIR` not `cwd` for your project paths
3. Print/log what you did (like “processed N files”)
4. Never crash on “already exists”

---



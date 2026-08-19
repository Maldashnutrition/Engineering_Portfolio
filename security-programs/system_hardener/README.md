```markdown
# Transactional Reverter

**A tool that applies "hardening" changes to a mock config file and guarantees atomic rollback, even if the script crashes.**  
This is a standalone, shackled child program extracted from a high‑assurance network isolation system. It demonstrates transactional operations, idempotency, persistent state management, and safe rollback – without ever modifying system settings or requiring root privileges.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [The Revert Stack](#the-revert-stack)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
- [Example Run](#example-run)
- [File Manifest](#file-manifest)
- [Technical Deep‑Dive](#technical-deepdive)
- [Security & Limitations](#security--limitations)

---

## Overview

This program simulates a **transactional hardening system**:

- Reads a **mock configuration file** (`/tmp/reverter_demo/mock.conf`) containing key‑value pairs (e.g., `PERMISSIVE=1`).
- Applies a "hardening" change – for example, setting `PERMISSIVE=0`.
- **Before** changing the value, it pushes the original value onto a **JSON revert stack** (`/tmp/reverter_demo/revert-stack.json`).
- You can apply multiple changes – each gets stacked.
- On **`Ctrl+C`** (or explicitly via `--revert`), it pops the stack in **reverse order** and restores every original value.
- The stack persists across script runs, so you can recover even after a crash.

The program is **fully shackled**: it only works on a mock file inside `/tmp`, never touches system configuration, and requires no root privileges.

---

## Architecture

The script consists of a single core class:

### `TransactionalReverter`

| Attribute | Type | Description |
|-----------|------|-------------|
| `dry_run` | `bool` | If `True`, prints actions without making changes. |
| `stack` | `list[dict]` | The revert stack (list of actions). |
| `BASE_DIR` | `Path` | `/tmp/reverter_demo` – working directory. |
| `CONFIG_FILE` | `Path` | `/tmp/reverter_demo/mock.conf` – mock config file. |
| `STACK_FILE` | `Path` | `/tmp/reverter_demo/revert-stack.json` – persistent stack. |

### Methods

| Method | Description |
|--------|-------------|
| `_load_stack()` | Reads the stack from `STACK_FILE`. |
| `_save_stack()` | Writes the stack to `STACK_FILE`. |
| `_read_config() -> dict` | Parses `mock.conf` into a `dict`. |
| `_write_config(config: dict)` | Writes the `dict` back to `mock.conf`, preserving comments and order. |
| `_push_revert_action(key, original, new)` | Adds an action to the stack. |
| `apply_harden(key="PERMISSIVE", target="0")` | Sets a key to a target value, stacking the revert. |
| `revert_all()` | Pops all actions in reverse order and restores originals. |
| `status()` | Displays current config and pending reverts. |
| `force_clean()` | Resets the config to defaults and clears the stack. |

---

## Core Components

### 1. Mock Configuration File

The mock config is a simple text file with `key=value` lines. Comments are preserved.

**Default content** (`/tmp/reverter_demo/mock.conf`):

```
# Mock system configuration
# This file is used for the transactional reverter demo.

PERMISSIVE=1
ALLOW_DEBUG=1
MAX_CONNECTIONS=100
```

### 2. The Revert Stack

The stack is a JSON array of actions. Each action is a dictionary:

```json
{
  "key": "PERMISSIVE",
  "original": "1",
  "new": "0",
  "timestamp": "2026-08-16T16:33:47.810200"
}
```

When you apply a change, the script:
- Reads the current value.
- Pushes the action (`key`, `original`, `new`, `timestamp`) onto the stack.
- Writes the new value to the config file.

When you revert, it:
- Pops the **last** action from the stack.
- Restores the `original` value.
- Continues until the stack is empty.

This makes the operation **atomic** and **reversible**.

### 3. Idempotency

Applying the same change twice has no effect – the script checks if the target value is already set and skips the operation.

---

## Installation & Requirements

### Requirements

- Python 3.6 or higher.
- No external libraries – uses only the standard library (`os`, `sys`, `json`, `signal`, `argparse`, `pathlib`, `datetime`).
- A Linux/macOS/Unix environment (the script uses POSIX paths).
- **No root privileges** – the script runs entirely in user space.

### Installation

Simply download `ini.py` and make it executable:

```bash
chmod +x ini.py
```

---

## Usage

### Interactive Mode (default)

```bash
python3 ini.py
```

Starts an interactive shell with the following commands:

| Command | Description |
|---------|-------------|
| `apply` | Applies hardening: sets `PERMISSIVE=0` and pushes a revert action. |
| `status` | Shows current config and pending reverts. |
| `revert` | Reverts all pending changes (pops the entire stack). |
| `clean` | Resets the config to defaults and clears the stack. |
| `quit` / `exit` | Exits the program (reverts if any changes are pending). |
| `Ctrl+C` | Triggers automatic revert of all pending changes. |

### Command‑Line Mode

| Option | Description |
|--------|-------------|
| `--apply` | Apply hardening (`PERMISSIVE=0`). |
| `--status` | Show current state and exit. |
| `--revert` | Revert all changes and exit. |
| `--clean` | Reset config and clear stack, exit. |
| `--dry-run` | Preview actions without making changes (can be combined with `--apply`). |

**Examples**:

```bash
python3 ini.py --apply              # Apply hardening
python3 ini.py --status             # Show state
python3 ini.py --revert             # Revert all
python3 ini.py --dry-run --apply    # Preview without changes
```

---

## Example Run

### Interactive Session

```bash
$ python3 ini.py
[INFO] Initialized mock config at /tmp/reverter_demo/mock.conf
[INFO] === Transactional Reverter Demo ===
[INFO] Mock config: /tmp/reverter_demo/mock.conf
[INFO] Press Ctrl+C at any time to revert all changes.
[INFO] Commands: apply, status, revert, clean, quit

> apply
[INFO] Stacked revert: PERMISSIVE '1' → '0'
[INFO] Applied hardening: PERMISSIVE = 0

> status
[INFO] Current configuration:
  PERMISSIVE = 0
  ALLOW_DEBUG = 1
  MAX_CONNECTIONS = 100
[INFO] Pending reverts: 1
  PERMISSIVE: 1 → 0 (at 2026-08-16T16:33:47.810200)

> revert
[INFO] Reverting 1 actions...
[INFO] Restored PERMISSIVE = 1
[INFO] Revert complete.

> quit
```

### Non‑Interactive Session

```bash
$ python3 ini.py --apply
[INFO] Stacked revert: PERMISSIVE '1' → '0'
[INFO] Applied hardening: PERMISSIVE = 0

$ python3 ini.py --status
[INFO] Current configuration:
  PERMISSIVE = 0
  ALLOW_DEBUG = 1
  MAX_CONNECTIONS = 100
[INFO] Pending reverts: 1
  PERMISSIVE: 1 → 0 (at 2026-08-16T16:33:47.810200)

$ python3 ini.py --revert
[INFO] Reverting 1 actions...
[INFO] Restored PERMISSIVE = 1
[INFO] Revert complete.

$ python3 ini.py --status
[INFO] Current configuration:
  PERMISSIVE = 1
  ALLOW_DEBUG = 1
  MAX_CONNECTIONS = 100
[INFO] No pending reverts.
```

### Crash Recovery

If the script is killed with `SIGKILL` (e.g., `kill -9`), the stack file persists. On the next run, you can manually revert:

```bash
python3 ini.py --revert
```

Or inspect the stack:

```bash
cat /tmp/reverter_demo/revert-stack.json
```

---

## File Manifest

| Path | Purpose |
|------|---------|
| `/tmp/reverter_demo/mock.conf` | Mock configuration file (key=value lines). |
| `/tmp/reverter_demo/revert-stack.json` | JSON stack of pending revert actions. |

All files are created automatically on first run and persist until manually deleted or the system reboots.

---

## Technical Deep‑Dive

### Configuration File Parsing

The `_read_config()` method:
- Reads `mock.conf` line by line.
- Skips empty lines and comments (starting with `#`).
- Splits each line at the first `=` to get `key` and `value`.
- Returns a `dict`.

The `_write_config()` method:
- Reads the existing file to preserve comments and blank lines.
- For each line, if it contains a `key=value` pair and the key is in the updated config, it replaces the value.
- For new keys not present, it appends them at the end.
- Writes the result back to disk.

This preserves human‑readable formatting while enabling atomic updates.

### Revert Stack Operations

- **Push**: `_push_revert_action()` appends a new action to `self.stack` and calls `_save_stack()`.
- **Pop**: `revert_all()` repeatedly calls `self.stack.pop()` until empty, restoring each original value.
- **Persistence**: `_save_stack()` writes the entire stack to JSON. `_load_stack()` reads it on startup.

### Idempotency

Before applying a change, `apply_harden()` checks if the current value already equals the target. If so, it logs a message and returns without pushing a revert action. This prevents stacking duplicate actions.

### Signal Handling

The script registers a signal handler for `SIGINT` (`Ctrl+C`). When triggered, it calls `revert_all()` and exits gracefully. This ensures that even if you interrupt the script, you are left with a consistent state.

---

## Security & Limitations

### Security Guarantees

- **No root**: The script runs entirely with the privileges of the invoking user.
- **No system modification**: It only operates on files inside `/tmp/reverter_demo/`.
- **No execution**: It never forks, executes, or loads external binaries.
- **No network**: No sockets, no DNS, no API calls.
- **Safe to run anywhere**: You can run this on a production machine without risk.

### Limitations

- **Mock environment**: The config file is arbitrary text; the script does not validate key names or values.
- **No locking**: The script does not use file locking; concurrent runs may conflict.
- **State persistence**: The stack is JSON‑encoded; if the script is killed during `_save_stack()`, the file may become corrupt.
- **No backup of original config**: The only way to restore is via the revert stack; if the stack is corrupted, you lose the ability to roll back.

---

## License

MIT – you are free to use, modify, and distribute this software.  
Please credit the original design if you incorporate it into your own projects.

---

## Author

Siyavuyisa Ntengo

---

For questions or contributions, please open an issue in the repository.
```

---

### How to Save This

1. Create the directory:
   ```bash
   mkdir -p 03-transactional-reverter
   ```
2. Save the content above as `README.md` inside it:
   ```bash
   cd 03-transactional-reverter
   nano README.md
   ```
   Paste the entire markdown block, save, and exit.
3. Place your `ini.py` in the same directory.
4. Verify everything works:
   ```bash
   python3 ini.py --self-test   # (if you have a self‑test)
   ```

---

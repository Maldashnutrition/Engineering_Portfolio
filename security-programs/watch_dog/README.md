Here is the **complete `README.md` for Child 4 (Idle Watchdog)** – fully detailed and formatted in Markdown.

```markdown
# Idle Watchdog

**A traffic‑aware scheduler that monitors network activity and triggers rotation events only when the link is idle.**  
This is a standalone, shackled child program extracted from a high‑assurance network isolation system. It demonstrates predictive heuristics, traffic monitoring, persistent state, and safe dry‑run operations – without ever modifying network interfaces or requiring root privileges.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [The Monitoring Loop](#the-monitoring-loop)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
- [Example Run](#example-run)
- [File Manifest](#file-manifest)
- [Technical Deep‑Dive](#technical-deepdive)
- [Security & Limitations](#security--limitations)

---

## Overview

This program monitors a network interface (or a **mock byte counter**) and triggers rotation events when traffic drops below a configurable threshold for a specified number of consecutive checks.

**Key features**:

- Reads RX bytes from a real interface (`/sys/class/net/<iface>/statistics/rx_bytes`) or from a mock file.
- Computes the byte delta between checks.
- If the delta is **below** the `ACTIVITY_THRESHOLD` for **IDLE_CHECKS_REQUIRED** consecutive checks, it triggers a rotation event.
- Rotations are subject to a **cooldown** (30 seconds) to prevent flapping.
- All state is persisted in JSON, surviving script restarts.
- A background **mock traffic simulator** (in `--mock` mode) injects random traffic and bursts for realistic testing.
- Fully shackled – no system changes, no `sudo`, no network reconfiguration.

---

## Architecture

The script consists of a single core class:

### `IdleWatchdog`

| Attribute | Type | Description |
|-----------|------|-------------|
| `interface` | `str` | Network interface to monitor (e.g., `lo`, `eth0`). |
| `use_mock` | `bool` | If `True`, reads from a mock file instead of a real interface. |
| `dry_run` | `bool` | If `True`, prints rotations without triggering them. |
| `check_interval` | `int` | Seconds between checks. |
| `activity_threshold` | `int` | Bytes per check interval – if delta is below this, considered idle. |
| `idle_checks_required` | `int` | Consecutive idle checks needed to trigger a rotation. |
| `running` | `bool` | Flag to control the main loop. |
| `idle_counter` | `int` | Current consecutive idle count. |
| `last_bytes` | `int` | Bytes at the last check. |
| `last_rotation` | `float` | Timestamp of the last rotation (for cooldown). |
| `total_bytes` | `int` | Total bytes read so far (for status). |
| `bytes_delta` | `int` | Most recent delta. |
| `rotation_count` | `int` | Number of rotations triggered since the start. |

### Methods

| Method | Description |
|--------|-------------|
| `_load_state()` | Reads persistent state from `STATE_FILE`. |
| `_save_state()` | Writes current state to `STATE_FILE`. |
| `_read_bytes_mock() -> int` | Reads the mock byte counter from `MOCK_BYTES_FILE`. |
| `_write_bytes_mock(value: int)` | Writes to the mock byte counter. |
| `_read_bytes_real() -> int` | Reads RX bytes from the real interface (via `/sys/class/net/`). |
| `read_bytes() -> int` | Dispatches to `_read_bytes_mock()` or `_read_bytes_real()` based on `use_mock`. |
| `update_mock_traffic()` | Background thread: randomly increments the mock counter and injects bursts. |
| `check_and_trigger()` | Main monitoring logic: reads bytes, calculates delta, updates idle counter, triggers rotation if needed. |
| `_trigger_rotation()` | Executes a rotation event (prints action, increments counter, updates cooldown). |
| `status()` | Displays current state. |
| `run()` | Starts the main monitoring loop. |

---

## The Monitoring Loop

The watchdog runs an infinite loop that:

1. Reads the current byte count.
2. Calculates `delta = current_bytes - last_bytes`.
3. If `delta < activity_threshold`, increments `idle_counter`; else resets `idle_counter` to 0.
4. If `idle_counter >= idle_checks_required`, and the cooldown has expired, it triggers a rotation.
5. Updates `last_bytes = current_bytes`.
6. Waits `check_interval` seconds.

### Rotation Trigger

- The cooldown is fixed at **30 seconds** to prevent flapping.
- The rotation action is:
  - In **dry‑run mode**: prints `[DRY-RUN] Would rotate endpoint`.
  - In **real mode**: prints `[ACTION] ROTATING endpoint (rotation #N)`.
  - Increments `rotation_count`.
  - Resets `idle_counter` and updates `last_rotation`.

### Mock Traffic Simulator

In `--mock` mode, a background thread:

- Reads the current mock byte count.
- Adds a random increment between 0 and 5000 bytes.
- With 20% probability, injects a burst of 10,000–50,000 bytes.
- Writes the new value back to the mock file.
- Sleeps for a random interval between 2 and 10 seconds.

This simulates realistic traffic patterns and allows you to see the watchdog in action without a real network interface.

---

## Installation & Requirements

### Requirements

- Python 3.6 or higher.
- No external libraries – uses only the standard library (`os`, `sys`, `time`, `json`, `signal`, `argparse`, `threading`, `pathlib`, `datetime`).
- A Linux environment (the script reads `/sys/class/net/`; for mock mode, any OS works).
- **No root privileges** – the script runs entirely in user space.

### Installation

Simply download `ini.py` and make it executable:

```bash
chmod +x ini.py
```

---

## Usage

### Interactive (Real or Mock Mode)

```bash
python3 ini.py --mock                  # Mock mode – no real interface needed
python3 ini.py --interface eth0        # Monitor a real interface
```

### Command‑Line Options

| Option | Description |
|--------|-------------|
| `--interface IFACE` | Network interface to monitor (default: `lo`). |
| `--mock` | Use simulated byte counter instead of a real interface. |
| `--dry-run` | Preview rotations without actually triggering them. |
| `--status` | Show current state and exit. |
| `--threshold N` | Activity threshold in bytes/check (default: 1024). |
| `--idle-checks N` | Consecutive idle checks before trigger (default: 3). |
| `--interval N` | Check interval in seconds (default: 5). |

**Examples**:

```bash
# Run with mock mode (simulated traffic)
python3 ini.py --mock

# Run with mock mode and dry‑run (just preview rotations)
python3 ini.py --mock --dry-run

# Monitor real interface eth0 with custom thresholds
python3 ini.py --interface eth0 --threshold 500 --idle-checks 5 --interval 3

# Show current state (from persistent file)
python3 ini.py --status
```

---

## Example Run

### 1. Mock mode – dry‑run

```bash
$ python3 ini.py --mock --dry-run
[16:37:40] [INFO] Initialized mock bytes file at /tmp/watchdog_demo/mock_bytes.txt
[16:37:40] [INFO] Mock traffic simulator started.
[16:37:40] [INFO] Starting idle watchdog on interface: lo
[16:37:40] [INFO] Activity threshold: 1024 bytes/check
[16:37:40] [INFO] Will trigger after 3 consecutive idle checks
[16:37:40] [INFO] Press Ctrl+C to stop.
[16:37:40] [DEBUG] 🟡 IDLE | Interface: lo | Delta: 0 bytes | Idle counter: 0
[16:37:40] [INFO] Idle detected (1/3)
[16:37:45] [DEBUG] 🟢 ACTIVE | Interface: lo | Delta: 2164 bytes | Idle counter: 1
[16:37:45] [INFO] Traffic detected – resetting idle counter
[16:37:49] [INFO] 💥 [SIMULATOR] Traffic burst: +47902 bytes
[16:37:50] [DEBUG] 🟢 ACTIVE | Interface: lo | Delta: 52137 bytes | Idle counter: 0
[16:37:55] [DEBUG] 🟢 ACTIVE | Interface: lo | Delta: 3673 bytes | Idle counter: 0
[16:38:00] [DEBUG] 🟢 ACTIVE | Interface: lo | Delta: 42651 bytes | Idle counter: 0
[16:38:05] [DEBUG] 🟡 IDLE | Interface: lo | Delta: 191 bytes | Idle counter: 0
[16:38:05] [INFO] Idle detected (1/3)
[16:38:10] [DEBUG] 🟡 IDLE | Interface: lo | Delta: 0 bytes | Idle counter: 1
[16:38:10] [INFO] Idle detected (2/3)
[16:38:15] [DEBUG] 🟡 IDLE | Interface: lo | Delta: 797 bytes | Idle counter: 2
[16:38:15] [INFO] Idle detected (3/3)
[16:38:15] [INFO] [DRY-RUN] Would rotate endpoint (rotation #1)
[16:38:20] [DEBUG] 🟡 IDLE | Interface: lo | Delta: 519 bytes | Idle counter: 0
[16:38:20] [INFO] Idle detected (1/3)
[16:38:25] [DEBUG] 🟢 ACTIVE | Interface: lo | Delta: 5070 bytes | Idle counter: 1
[16:38:25] [INFO] Traffic detected – resetting idle counter
^C[16:38:51] [INFO] Received interrupt. Stopping...
[16:38:55] [INFO] Exiting.
```

### 2. Status check

```bash
$ python3 ini.py --status
[16:39:06] [INFO] === Watchdog Status ===
[16:39:06] [INFO] Interface: lo
[16:39:06] [INFO] Mode: REAL
[16:39:06] [INFO] Dry-run: NO
[16:39:06] [INFO] Check interval: 5s
[16:39:06] [INFO] Activity threshold: 1024 bytes/check
[16:39:06] [INFO] Idle checks required: 3
[16:39:06] [INFO] Current bytes: 170,458
[16:39:06] [INFO] Last delta: 0 bytes
[16:39:06] [INFO] Idle counter: 0/3
[16:39:06] [INFO] Rotations: 1
[16:39:06] [INFO] Last rotation: 16:38:15
```

---

## File Manifest

| Path | Purpose |
|------|---------|
| `/tmp/watchdog_demo/watchdog_state.json` | Persistent state (idle counter, last bytes, rotation count, last rotation timestamp). |
| `/tmp/watchdog_demo/mock_bytes.txt` | Mock byte counter (used only in `--mock` mode). |

All files are created automatically on first run and persist until manually deleted or the system reboots.

---

## Technical Deep‑Dive

### Monitoring Algorithm (Pseudo‑code)

```
while running:
    current_bytes = read_bytes()
    delta = current_bytes - last_bytes
    if delta < 0:
        // interface reset – ignore
    else:
        if delta < activity_threshold:
            idle_counter += 1
            if idle_counter >= idle_checks_required and (now - last_rotation) >= cooldown:
                trigger_rotation()
        else:
            idle_counter = 0
    last_bytes = current_bytes
    save_state()
    sleep(check_interval)
```

### Threshold Selection

The default values are:

- **Activity threshold**: 1024 bytes per check interval (5 seconds).
- **Idle checks required**: 3 consecutive checks.

In a real‑world scenario, these would be tuned based on the expected traffic pattern of the application. The values here are chosen to demonstrate the concept effectively with mock traffic.

### Persistent State

The state file contains:

```json
{
  "idle_counter": 0,
  "last_bytes": 170458,
  "last_rotation": 1697657895.0,
  "total_bytes": 170458,
  "rotation_count": 1
}
```

This allows the watchdog to remember its state across restarts – useful if the script is restarted while the system is still running.

### Cooldown

The cooldown is hardcoded at **30 seconds** to prevent multiple rotations in quick succession. This is realistic for VPN failover systems where you don't want to keep cycling endpoints.

### Mock Simulator

The mock simulator runs in a background daemon thread. It updates the mock byte file every 2–10 seconds with a random increment. Bursts simulate sudden traffic spikes, giving the watchdog realistic scenarios to respond to.

---

## Security & Limitations

### Security Guarantees

- **No root**: The script runs entirely with the privileges of the invoking user.
- **No system modification**: It only reads from `/sys/class/net/` (read‑only) and writes to `/tmp/watchdog_demo/`.
- **No execution**: It never forks, executes, or loads external binaries.
- **No network**: No sockets, no DNS, no API calls.
- **Safe to run anywhere**: You can run this on a production machine without risk.

### Limitations

- **Real interface monitoring** requires that the system exposes `/sys/class/net/`. This is standard on Linux but may not work on other OSes.
- **Mock mode is synthetic** – traffic patterns are random and may not reflect real‑world usage.
- **State file persistence** relies on the filesystem; if the script is killed during a write, the state file may become corrupt.
- **No integration with actual VPNs** – the watchdog only prints actions; it does not actually rotate endpoints.
- **Cooldown is hardcoded** – cannot be adjusted via command line (though you can modify the source).

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
   mkdir -p 04-idle-watchdog
   ```
2. Save the content above as `README.md` inside it:
   ```bash
   cd 04-idle-watchdog
   nano README.md
   ```
   Paste the entire markdown block, save, and exit.
3. Place your `ini.py` in the same directory.
4. Verify everything works:
   ```bash
   python3 ini.py --mock --dry-run
   ```

---

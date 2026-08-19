```markdown
# FSM DNS Leak Detector

**A Finite State Machine (FSM) that simulates DNS leak detection, forensics collection, diagnosis, and auto‑repair.**  
This is a standalone, shackled child program extracted from a high‑assurance network isolation system. It demonstrates incident‑response pipelines, persistent state management, and safe dry‑run operations – without requiring root or system modifications.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [State Machine Definition](#state-machine-definition)
- [The Simulator (Leak Injection)](#the-simulator-leak-injection)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
- [Example Run](#example-run)
- [File Manifest](#file-manifest)
- [Technical Deep‑Dive](#technical-deepdive)
- [Security & Limitations](#security--limitations)

---

## Overview

This program implements a **finite state machine** that:

- Reads a **mock DNS counter file** (`/tmp/fsm_demo/dns_counter.txt`) containing `total_queries:leaked_queries`.
- Detects DNS leaks by comparing deltas between successive reads.
- Injects simulated leaks via a **background thread** (no network required).
- Transitions through seven discrete states, each performing a specific action.
- Collects **mock forensics** (files mimicking `nftables`, `routes`, `resolv.conf`, etc.) into timestamped directories.
- **Diagnoses** the root cause based on the forensic mock data.
- **Attempts a repair** (prints the command – never executes).
- Recovers and returns to monitoring.

All state is persisted to `/tmp/fsm_demo/fsm_state.json`, allowing the FSM to survive restarts.

---

## Architecture

The program consists of two primary classes:

### `DNSLeakFSM`
Manages the finite state machine:
- Maintains `state`, `fail_count`, `last_total`, `last_leak`, `forensics_path`, `diagnosis_cause`.
- Implements transition methods (`transition_to`, `_save_state`).
- Provides core actions: `check_dns_leak()`, `collect_forensics()`, `diagnose_cause()`, `attempt_repair()`, `reset_leak_failures()`.
- Runs the main loop via `run_cycle()` and `start()`.

### `LeakSimulator`
Runs in a separate thread:
- Maintains `current_total` and `current_leak` counters.
- Increments `current_total` by 1–20 per cycle.
- With **40% probability**, increments `current_leak` by 1–5 (simulating a leak).
- Writes the new values to `dns_counter.txt`.
- Sleeps for a random interval between 8 and 15 seconds between injections.

### `Colors` and `log()`
- ANSI color codes for terminal readability.
- `log()` prepends a timestamp (`[HH:MM:SS]`) and a level (`[INFO]`, `[DEBUG]`, `[ALERT]`).

---

## State Machine Definition

The FSM has **seven states**, each with a specific transition condition:

| State | Entry Action | Exit Condition |
|-------|--------------|----------------|
| `MONITORING` | None | If `check_dns_leak()` returns `True` → `LEAK_DETECTED` |
| `LEAK_DETECTED` | Increment `fail_count` | If `fail_count >= LEAK_THRESHOLD` → `FAILED`; else → `COLLECTING_FORENSICS` |
| `COLLECTING_FORENSICS` | Calls `collect_forensics()` | → `DIAGNOSING` |
| `DIAGNOSING` | Calls `diagnose_cause()` | → `REPAIRING` |
| `REPAIRING` | Calls `attempt_repair()` | If success → `RECOVERED`; else → `FAILED` |
| `RECOVERED` | Calls `reset_leak_failures()` | → `MONITORING` |
| `FAILED` | Stops the FSM (`self.running = False`) | (Terminal state) |

### Constants (hardcoded in the script)

| Constant | Value | Description |
|----------|-------|-------------|
| `LEAK_INJECT_INTERVAL` | `(8, 15)` | Random sleep range (seconds) for the simulator. |
| `TOTAL_BASE` | `100` | Initial `total_queries`. |
| `LEAK_THRESHOLD` | `2` | Consecutive leak failures before entering `FAILED`. |

---

## The Simulator (Leak Injection)

The background `LeakSimulator` thread:

1. **Reads** the current mock counter file.
2. **Adds** 1–20 to `current_total`.
3. With **40% probability**, adds 1–5 to `current_leak`.
4. **Writes** the new values back to `dns_counter.txt`.
5. Sleeps for a random duration between 8 and 15 seconds.
6. Continues until the main FSM stops or the script exits.

This mimics realistic traffic: total queries increase continuously, while leaks occur sporadically.

---

## Installation & Requirements

### Requirements

- Python 3.6 or higher.
- No external libraries – uses only the standard library (`os`, `sys`, `time`, `json`, `random`, `threading`, `pathlib`, `enum`, `datetime`, `typing`).
- A Linux/macOS/Unix environment (the script uses `/tmp` and ANSI colours).
- **No root privileges** – the script runs entirely in user space.

### Installation

Simply download `ini.py` and make it executable:

```bash
chmod +x ini.py
```

---

## Usage

### Basic Interactive Run

```bash
python3 ini.py
```

- Starts the FSM and the leak simulator.
- The simulator will inject leaks every 8–15 seconds.
- The FSM will detect them, cycle through states, and print coloured logs.
- Press `Ctrl+C` to stop gracefully.

### Self‑Test

```bash
python3 ini.py --self-test
```

- Runs a pre‑scripted sequence that verifies:
  - The script can read and write to `/tmp/fsm_demo/`.
  - The leak detection logic catches a simulated leak.
  - The FSM transitions correctly through all states.
- Expected output: `[INFO] Self-test passed.` and exit code `0`.

### Debugging / Forensics Inspection

While the script runs, inspect the following paths:

```bash
ls -la /tmp/fsm_demo/
cat /tmp/fsm_demo/dns_counter.txt
cat /tmp/fsm_demo/fsm_state.json
ls -la /tmp/fsm_demo/forensics/
```

These files persist until the system reboots or you manually delete them.

---

## Example Run

Below is an **actual terminal session** from a test run (identical to the script’s current behaviour):

```
[16:18:58] [DEBUG] 💡 Leak simulator thread started.
[16:18:58] [INFO] 💉 [SIMULATOR] Injected leak! (Total=117, Leak=5)
[16:18:58] [INFO] Starting DNS Leak FSM Demo...
[16:18:58] [INFO] Watch directory: /tmp/fsm_demo
[16:18:58] [INFO] Press Ctrl+C to stop.

[16:18:58] [DEBUG] Read counters: Total=117, Leak=5
[16:18:58] [ALERT] 🚨 DNS LEAK DETECTED!
[16:18:58] [INFO] State Transition: MONITORING → LEAK_DETECTED
[16:19:00] [INFO] Consecutive leak failures: 1/2
[16:19:00] [INFO] State Transition: LEAK_DETECTED → COLLECTING_FORENSICS
[16:19:02] [INFO] Forensics dumped to /tmp/fsm_demo/forensics/dump_1786911542
[16:19:02] [INFO] State Transition: COLLECTING_FORENSICS → DIAGNOSING
[16:19:04] [INFO] Diagnosed cause: default-route-missing
[16:19:04] [INFO] State Transition: DIAGNOSING → REPAIRING
[16:19:06] [INFO] Attempting repair for cause: default-route-missing
[16:19:06] [INFO] 🔧 [DRY-RUN] Would re-add default route via gateway
[16:19:07] [INFO] State Transition: REPAIRING → RECOVERED
[16:19:09] [INFO] Leak resolved. Returning to monitoring.
[16:19:09] [DEBUG] Leak failure counter reset.
[16:19:09] [INFO] State Transition: RECOVERED → MONITORING
[16:19:11] [DEBUG] Read counters: Total=131, Leak=5
[16:19:11] [DEBUG] ✅ No new DNS leaks.
^C
[16:19:20] [INFO] User interrupted. Shutting down...
[16:19:21] [INFO] Cleanup complete. Exiting.
```

---

## File Manifest

The script creates the following files at runtime:

| Path | Type | Content |
|------|------|---------|
| `/tmp/fsm_demo/dns_counter.txt` | Text file | `total_queries:leaked_queries` (e.g., `142:7`) |
| `/tmp/fsm_demo/fsm_state.json` | JSON | `{"state":"MONITORING","last_total":142,"last_leak":7,"fail_count":0,"diagnosis":null,"forensics":null}` |
| `/tmp/fsm_demo/forensics/dump_<timestamp>/` | Directory | Mock forensic files (see below) |

### Mock Forensic Files (inside each `dump_<timestamp>/` directory)

| File | Content |
|------|---------|
| `nftables.txt` | Simulated firewall rules (`# Mock nftables rules...`) |
| `routes.txt` | Simulated routing table (`default via 10.10.0.1 dev host0...`) |
| `resolv.conf.txt` | Simulated resolver config (`nameserver 127.0.0.1`) |
| `interfaces.txt` | Simulated interface list (`1: lo: <LOOPBACK,UP>...`) |

The `diagnose_cause()` method reads these files to determine the leak’s root cause. In the real script, it uses regex; in this demo, it uses a weighted randomisation based on the file contents.

---

## Technical Deep‑Dive

### Leak Detection Logic (`check_dns_leak()`)

The method reads `total` and `leak` from the counter file. It then compares them to the previous values (`self.last_total`, `self.last_leak`):

```python
if total > self.last_total and leak > self.last_leak:
    leak_detected = True
elif leak > self.last_leak:
    leak_detected = True
```

In plain English:
- If total increased **and** leak increased → leak.
- If leak increased on its own → leak.
- Otherwise → no leak.

This mirrors the original bash script’s logic, which counted DNS queries via `nft` counters.

### Diagnosis (`diagnose_cause()`)

The method checks the mock forensic files:

- If `127.0.0.1` is **not** present in `resolv.conf.txt` → `dnsmasq-down`.
- If `tun0` is **not** present in `routes.txt` → `default-route-missing`.
- Otherwise, it picks randomly from:  
  `tor-dnsport-missing`, `dnsmasq-down`, `default-route-missing`, `nftables-dns-redirect-missing`, `tor-connectivity-failure`.

This simulates the real diagnostic process, which would use exact pattern matching.

### Repair (`attempt_repair()`)

The method maps each diagnosis to a **dry‑run message**:

| Diagnosis | Message |
|-----------|---------|
| `tor-dnsport-missing` | `[DRY-RUN] Would restart Tor with DNSPort` |
| `dnsmasq-down` | `[DRY-RUN] Would restart dnsmasq` |
| `default-route-missing` | `[DRY-RUN] Would re-add default route via gateway` |
| `nftables-dns-redirect-missing` | `[DRY-RUN] Would re-apply nftables DNS redirect rules` |
| `tor-connectivity-failure` | `[DRY-RUN] Would restart Tor and wait for bootstrap` |

It then sleeps for 1.5 seconds to simulate a repair operation, then returns `True` (simulating success).

### State Persistence

The `_save_state()` method writes a JSON object containing:
- `state` – current FSM state (as a string).
- `last_total` – last known total queries.
- `last_leak` – last known leaked queries.
- `fail_count` – consecutive failure counter.
- `diagnosis` – last diagnosed cause.
- `forensics` – path to the last forensics dump.

This means if you `Ctrl+C` and restart, the FSM will resume from its last state.

---

## Security & Limitations

### Security Guarantees

- **No root**: The script never calls `sudo`, `setuid`, or modifies `/etc`, `/proc`, or `/sys`.
- **No network**: No sockets, no DNS resolution, no API calls.
- **No external commands**: Does not spawn `subprocess` or execute binaries.
- **Sandboxed**: All writes occur under `/tmp/fsm_demo/`.
- **Safe to run anywhere**: You can run this on a production machine without risk.

### Limitations

- **Mocked logic**: Diagnostics are randomised; real logic would use exact pattern matching.
- **No real repairs**: Repairs are printed, not executed.
- **No actual DNS leaks**: Leaks are simulated by the background thread.
- **Single‑threaded FSM**: The FSM loop runs every 2 seconds; the simulator runs in a separate thread.
- **State file can grow**: State file is overwritten, not appended, so it stays small.

---

## License

MIT – you are free to use, modify, and distribute this software.  
Please credit the original design patterns if you incorporate them into your own projects.

---

## Author

Siyavuyisa Ntengo

---

For questions or contributions, please open an issue in the repository.
```

---

### How to Save This

1. If you haven't already, create the directory:
   ```bash
   mkdir -p 01-fsm-leak-detector
   ```
2. Save the content above as `README.md` inside it:
   ```bash
   cd 01-fsm-leak-detector
   nano README.md
   ```
   Paste the entire markdown block, save, and exit.
3. Place your `ini.py` in the same directory.
4. Verify everything works:
   ```bash
   python3 ini.py --self-test
   ```

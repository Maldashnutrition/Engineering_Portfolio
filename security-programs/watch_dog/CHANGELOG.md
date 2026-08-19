# Changelog for Idle Watchdog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- None currently.

---

## [1.0.0] – 2026-08-16

### Added

- **Idle Watchdog** – Traffic‑aware scheduler that monitors network activity and triggers rotation events only when idle.

  **Core Features**:
  - Reads RX bytes from a real interface (`/sys/class/net/`) or a mock file
  - Configurable activity threshold, idle checks, and interval
  - Background mock traffic simulator (random increments and bursts)
  - Rotation cooldown to prevent flapping
  - Persistent state via JSON (`/tmp/watchdog_demo/watchdog_state.json`)
  - Dry‑run mode for previewing rotations

  **CLI Options**:
  - `--interface IFACE` – Network interface to monitor
  - `--mock` – Use simulated byte counter
  - `--dry-run` – Preview rotations without triggering
  - `--status` – Show current state
  - `--threshold N` – Activity threshold in bytes/check
  - `--idle-checks N` – Consecutive idle checks before trigger
  - `--interval N` – Check interval in seconds

  **Technical Implementation**:
  - Python 3.6+ compatible
  - No external dependencies – uses only the standard library
  - Threaded mock simulator for realistic testing
  - Persistent JSON state
  - Signal handler for graceful shutdown

### Fixed

- N/A (initial release)

### Security

- Fully shackled – runs in user space
- Reads only from `/sys/class/net/` (read‑only) or mock files
- Writes only to `/tmp/watchdog_demo/`
- Requires no `sudo` or root privileges
- No subprocess execution
- No network calls
- No system modifications

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0

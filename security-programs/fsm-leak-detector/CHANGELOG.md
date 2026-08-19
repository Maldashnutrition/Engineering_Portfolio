# Changelog for FSM DNS Leak Detector

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- None currently.

---

## [1.0.0] – 2026-02-18

### Added

- **FSM DNS Leak Detector** – Finite State Machine for DNS leak detection, forensics, diagnosis, and auto‑repair.

  **Core Features**:
  - Seven-state FSM: `MONITORING` → `LEAK_DETECTED` → `COLLECTING_FORENSICS` → `DIAGNOSING` → `REPAIRING` → `RECOVERED` → `FAILED`
  - Background leak simulator with random injection intervals (8–15 seconds)
  - Persistent state via JSON (`/tmp/fsm_demo/fsm_state.json`)
  - Mock forensic file generation (`nftables.txt`, `routes.txt`, `resolv.conf.txt`, `interfaces.txt`)
  - Dry‑run repair messages (no system modifications)
  - Coloured logging with timestamps and log levels

  **CLI Options**:
  - `--self-test` – Run built‑in validation
  - No arguments – Start interactive demo

  **Technical Implementation**:
  - Python 3.6+ compatible
  - No external dependencies – uses only the standard library
  - Threaded leak simulator for realistic traffic patterns
  - Signal handler for graceful shutdown (`Ctrl+C`)

### Fixed

- N/A (initial release)

### Security

- Fully shackled – runs in user space
- Writes only to `/tmp/fsm_demo/`
- Requires no `sudo` or root privileges
- No subprocess execution
- No network calls
- No system modifications

---

## [0.1.0] – 2026-02-18

### Added

- Initial prototype (not publicly released)

---

### Versioning

- **Major**: Incompatible API changes
- **Minor**: Added functionality (backward compatible)
- **Patch**: Bug fixes (backward compatible)

---

# Changelog for Transactional Reverter

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

- **Transactional Reverter** – Atomic system hardening with JSON‑based rollback.

  **Core Features**:
  - Mock configuration file (`/tmp/reverter_demo/mock.conf`)
  - Revert stack stored as JSON (`/tmp/reverter_demo/revert-stack.json`)
  - Idempotent operations (applying twice has no effect)
  - Signal handler for graceful rollback on `Ctrl+C`
  - Interactive and command‑line modes

  **CLI Options**:
  - `--apply` – Apply hardening (sets `PERMISSIVE=0`)
  - `--revert` – Revert all changes
  - `--status` – Show current state and pending reverts
  - `--clean` – Reset config and clear stack
  - `--dry-run` – Preview actions without making changes

  **Technical Implementation**:
  - Python 3.6+ compatible
  - No external dependencies – uses only the standard library
  - JSON‑based state persistence
  - Atomic operations with rollback

### Fixed

- N/A (initial release)

### Security

- Fully shackled – runs in user space
- Writes only to `/tmp/reverter_demo/`
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

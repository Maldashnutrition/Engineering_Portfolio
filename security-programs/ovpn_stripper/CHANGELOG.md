# Changelog for OpenVPN Config Sanitizer

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

- **OpenVPN Config Sanitizer** – Security-first parser that strips dangerous directives from `.ovpn` files.

  **Core Features**:
  - Allowlist for safe directives (`remote`, `cipher`, `auth`, `persist-key`, `verb`, etc.)
  - Blocklist for dangerous directives (`up`, `down`, `script-security`, `plugin`, etc.)
  - Inline block handling (`<ca>`, `<cert>`, `<key>`, `<tls-auth>`)
  - Preserves certificates and keys inside inline blocks
  - Counts stripped directives and logs warnings

  **CLI Options**:
  - `--generate-sample` – Creates a sample `.ovpn` file for testing
  - `--self-test` – Runs built‑in validation

  **Technical Implementation**:
  - Python 3.6+ compatible
  - No external dependencies – uses only the standard library
  - Stateful parsing (tracks whether we are inside an inline block)

### Fixed

- N/A (initial release)

### Security

- Fully shackled – runs in user space
- Never executes OpenVPN or subprocesses
- Requires no `sudo` or root privileges
- Only reads and writes user‑specified files

---

## [0.1.0] – 2026-08-15

### Added

- Initial prototype (not publicly released)

---

[1.0.0]: https://github.com/[your-username]/[repo-name]/releases/tag/v1.0.0

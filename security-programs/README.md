# Security Toolkit Demos

> Four standalone design patterns extracted from a high‑assurance network isolation system.  
> Each demo is a self‑contained Python script that demonstrates a core security or reliability concept – without requiring root privileges or modifying your system.

---

## Overview

| Demo | Concept | File |
|------|---------|------|
| **FSM DNS Leak Detector** | Finite State Machine for incident handling & auto‑healing | `01-fsm-leak-detector/ini.py` |
| **OpenVPN Config Sanitizer** | Configuration firewall (allow/block lists, inline‑block handling) | `02-ovpn-hardener/ini.py` |
| **Transactional Reverter** | Atomic system hardening with JSON‑based rollback | `03-transactional-reverter/ini.py` |
| **Idle Watchdog** | Traffic‑aware scheduling & rotation heuristics | `04-idle-watchdog/ini.py` |

---

## Why These Matter

- **FSM DNS Leak Detector** – shows how to build resilient, state‑aware monitoring that can diagnose and repair issues automatically.
- **OpenVPN Config Sanitizer** – demonstrates secure parsing and the principle of least privilege for configuration files.
- **Transactional Reverter** – proves you understand atomic operations, idempotency, and safe rollbacks – essential for automation.
- **Idle Watchdog** – illustrates predictive heuristics: only act when it’s safe, avoiding disruptions during active use.

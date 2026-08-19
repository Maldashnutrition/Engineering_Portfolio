# Security Policy for Idle Watchdog

## Supported Versions

This is an **educational proof‑of‑concept** demo. It is not intended for production use.

| Version | Supported |
|---------|-----------|
| 1.0.0   | ✅ Yes (educational use only) |

## Reporting a Vulnerability

If you discover a security vulnerability in this demo, please do **not** open a public issue.

Instead, please open a **private** issue in the repository, or contact the maintainer directly via the email address provided in the repository profile.

### What to Include

- A clear description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact and any mitigation suggestions.

We aim to respond within 48 hours and will work to validate and address the issue.

## Security Philosophy

This demo is designed to be **shackled**:

- It runs entirely in user space.
- It only reads from `/sys/class/net/` (read‑only) or mock files.
- It writes only to `/tmp/watchdog_demo/`.
- It requires **no root privileges**.
- It never modifies system settings, executes external binaries, or makes network calls.
- It never actually rotates endpoints – only prints dry‑run actions.

However, it is intended for educational and portfolio purposes only.  
**Do not use it in production environments** without thorough audit and adaptation.

---

**Note**: This is a demonstration tool. For production security, please consult a qualified security professional.

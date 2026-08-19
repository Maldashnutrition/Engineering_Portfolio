# Security Policy for FSM DNS Leak Detector

## Supported Versions

This project is a **proof‑of‑concept educational demo**. It is not intended for production use.

| Version | Supported |
|---------|-----------|
| 1.0.0   | ✅ Yes (educational use only) |

## Reporting a Vulnerability

We take security seriously, even for this non‑production demo.

If you discover a security vulnerability, please **do not** open a public issue.

Instead, please open a **private** issue in the repository, or contact the maintainer directly via the email address provided in the repository profile.

### What to Include

To help us understand and address the issue, please include:

- A clear description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact and any mitigation suggestions.

We aim to respond within 48 hours and will work to validate and address the issue.

## Security Philosophy

This demo is designed to be **shackled**:

- It runs entirely in user space.
- It writes only to `/tmp/fsm_demo/`.
- It requires **no root privileges**.
- It never modifies system settings, executes external binaries, or makes network calls.

However, it is intended for educational and portfolio purposes only.  
**Do not use it in production environments** without thorough audit and adaptation.

---

**Note**: This is a demonstration tool. For production security, please consult a qualified security professional.

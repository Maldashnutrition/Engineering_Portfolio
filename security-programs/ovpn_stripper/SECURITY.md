# Security Policy for OpenVPN Config Sanitizer

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
- It never executes OpenVPN or any subprocesses.
- It requires **no root privileges**.
- It only reads and writes files you specify.
- It never modifies system settings or network interfaces.

However, it is intended for educational and portfolio purposes only.  
**Do not use it in production environments** without thorough audit and adaptation.

---

**Note**: This is a demonstration tool. For production security, please consult a qualified security professional.

# Security Policy for Sales Analytics

## Supported Versions

This is an **educational proof‑of‑concept** database project. It is not intended for production use.

| Version | Supported |
|---------|-----------|
| 1.0.0   | ✅ Yes (educational use only) |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please do **not** open a public issue.

Instead, please open a **private** issue in the repository, or contact the maintainer directly via the email address provided in the repository profile.

### What to Include

- A clear description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact and any mitigation suggestions.

We aim to respond within 48 hours and will work to validate and address the issue.

## Security Philosophy

This project is designed with database security best practices:

- **Foreign key constraints** maintain referential integrity.
- **CHECK constraints** validate data (revenue >= 0, quantity > 0, etc.).
- **SQL injection protection** – the Python wrapper uses parameterized queries.

**Limitations**:
- No authentication or authorization – designed for local use only.
- No encryption – data is stored in plaintext.
- Intended for educational purposes only.

**Do not use it in production environments** without thorough audit and adaptation.

---

**Note**: This is a demonstration tool. For production database security, please consult a qualified security professional.

# Security Policy for Sales Forecasting & BI Dashboard

## Supported Versions

This is an **educational proof‑of‑concept** data science project. It is not intended for production use.

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

This project is designed with data science security best practices:

- **Read‑only access** – The script only reads from `sales.db`; it never modifies the database.
- **No network calls** – No external data is fetched.
- **No system modifications** – All writes go to the `output/` folder.

**Limitations**:
- No authentication or authorization – designed for local use only.
- Database contains no sensitive personal information (sample data only).
- Forecast may be inaccurate with limited data.
- Intended for educational purposes only.

**Do not use it in production environments** without thorough audit and adaptation.

---

**Note**: This is a demonstration tool. For production security, please consult a qualified security professional.

---

## Document: `CONTRIBUTING.md`

**Purpose**: Outlines guidelines for contributing to the project. Even if you don't expect contributions, this shows recruiters that you think about collaboration and maintain a professional standard.

**File location**: `01-fsm-leak-detector/CONTRIBUTING.md`

**Content**:

```markdown
# Contributing to FSM DNS Leak Detector

Thank you for your interest in contributing! This project is an educational demo for portfolio purposes, and we welcome constructive input.

---

## How to Contribute

1. **Fork** the repository.
2. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** – ensure the demo still passes its self‑test.
4. **Test** your changes:
   ```bash
   make test
   ```
   Or manually:
   ```bash
   python3 ini.py --self-test
   ```
5. **Commit** with a clear message:
   ```bash
   git commit -m "Add: description of your change"
   ```
6. **Push** to your fork and open a **Pull Request**.

---

## Guidelines

### Code Style

- Follow **PEP 8** for Python code.
- Use descriptive variable names.
- Include docstrings for functions and classes (Google or NumPy style preferred).
- Keep functions focused and single‑purpose.

### Demo Requirements

- **Shackled**: The script must run without `sudo`, write only to `/tmp/`, and never modify system files.
- **No external dependencies**: Only use the Python standard library.
- **Backward compatibility**: Support Python 3.6+.
- **Self‑test**: Any new feature should be covered by the self‑test (`--self-test`).

### Documentation

- Update `README.md` if you add new features.
- Update `CHANGELOG.md` if you add, change, or fix anything.
- Keep code comments clear and concise.

---

## Reporting Issues

If you encounter a bug or have a suggestion:

1. Check the existing issues to avoid duplicates.
2. Open a new issue with:
   - A clear description.
   - Steps to reproduce (if applicable).
   - Expected vs. actual behaviour.
   - Environment (OS, Python version).

---

## Security Vulnerabilities

Please **do not** open a public issue for security vulnerabilities.  
Refer to [SECURITY.md](SECURITY.md) for reporting instructions.

---

## Getting Help

If you're unsure about anything, open a Discussion or ask in the issue tracker.

---

Thank you for contributing!
```

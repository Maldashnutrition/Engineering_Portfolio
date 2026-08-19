```markdown
# OpenVPN Config Sanitizer

**A security-first parser that strips dangerous directives from OpenVPN `.ovpn` files, preserving safe ones and correctly handling inline certificates and keys.**  
This is a standalone, shackled child program extracted from a high‑assurance network isolation system. It demonstrates configuration firewall principles, stateful parsing, and the principle of least privilege – without ever executing OpenVPN or modifying system files.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [Allowlist & Blocklist](#allowlist--blocklist)
- [Inline Block Handling](#inline-block-handling)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
- [Example Run](#example-run)
- [File Manifest](#file-manifest)
- [Technical Deep‑Dive](#technical-deepdive)
- [Security & Limitations](#security--limitations)

---

## Overview

This program reads an OpenVPN configuration file (`.ovpn`) and produces a **sanitized version** by:

- **Stripping dangerous directives** that could execute arbitrary commands or weaken security (e.g., `up`, `down`, `script-security`, `plugin`).
- **Preserving safe directives** (e.g., `remote`, `cipher`, `auth`, `persist-key`, `verb`).
- **Correctly handling inline blocks** (`<ca>`, `<cert>`, `<key>`, `<tls-auth>`) – preserving their content entirely.
- **Removing unrecognised directives** (unknown to the allowlist) with a warning.

The program is **fully shackled**: it only reads and writes files you specify, never touches system directories, requires no root privileges, and never spawns subprocesses.

---

## Architecture

The script consists of a single core class:

### `OpenVPNSanitizer`

| Attribute | Type | Description |
|-----------|------|-------------|
| `input_path` | `Path` | Path to the input `.ovpn` file |
| `output_path` | `Optional[Path]` | Path to the output file (or `None` for stdout) |
| `in_inline` | `bool` | Flag indicating whether we are inside an inline block |
| `inline_tag` | `str | None` | The current inline block tag (`ca`, `cert`, `key`, `tls-auth`) |
| `stripped` | `int` | Count of stripped directives |
| `out_lines` | `list[str]` | Accumulated sanitised lines |

### Methods

| Method | Description |
|--------|-------------|
| `sanitize() -> str` | Reads the input, applies filtering, returns the sanitised string. |
| `run()` | Orchestrates reading, sanitising, and writing output. |
| `_is_comment_or_empty(line: str) -> bool` | Returns `True` if the line is empty or starts with `#` or `;`. |
| `_extract_directive(line: str) -> Optional[str]` | Extracts the first word of the line (the directive). |

---

## Core Components

### 1. Directive Classification

Every directive (the first word of a line) is classified as:

| Category | Behaviour |
|----------|-----------|
| **Allowed** | Kept in the output. |
| **Dangerous** | Stripped, counted, and logged. |
| **Unknown** | Stripped, counted, and logged (treated as potentially unsafe). |
| **Comment / Empty** | Preserved as-is. |
| **Inline Tag** | Triggers inline block mode. |

### 2. Inline Block Mode

When the parser encounters a line like `<ca>`, `<cert>`, `<key>`, or `<tls-auth>`, it:

1. Enters inline mode.
2. Preserves the opening tag.
3. Preserves every subsequent line verbatim (including comments and blank lines) until it sees the matching closing tag (`</ca>`, `</cert>`, etc.).
4. Exits inline mode after the closing tag.

This ensures that certificate data, private keys, and TLS authentication material are never accidentally modified or stripped.

### 3. Stripping Logic

The parser iterates over each line:

- If the line is empty or a comment (`#` or `;`), it is preserved.
- If inside an inline block, the line is preserved.
- If the line starts with an inline tag, it enters inline block mode and preserves the tag.
- Otherwise, it extracts the directive (first word).
- If the directive is in the **dangerous set**, it is stripped.
- If the directive is in the **allowed set**, it is preserved.
- If the directive is **neither**, it is stripped (with a warning).

---

## Allowlist & Blocklist

### Allowed Directives (preserved)

The following directives are considered safe and are **preserved**:

```
remote, proto, dev, dev-type, ca, cert, key, tls-auth,
cipher, auth, auth-user-pass, comp-lzo, compress, tun-mtu,
mtu-disc, keepalive, ping, ping-restart, reneg-sec,
remote-cert-tls, verify-x509-name, tls-version-min,
data-ciphers, data-ciphers-fallback, mute-replay-warnings,
route, route-noexec, pull, pull-filter, client, nobind,
resolv-retry, persist-key, persist-tun, verb, fast-io,
route-delay, redirect-gateway, block-outside-dns,
auth-nocache, auth-retry, socks-proxy,
tls-client, ns-cert-type, remote-random
```

### Dangerous Directives (stripped)

The following directives are considered dangerous and are **stripped**:

```
up, down, script-security, plugin, auth-user-pass-verify,
tls-verify, ipchange, route-up, route-pre-down,
client-connect, client-disconnect, learn-address,
setenv, setenv-safe, management, management-client-auth,
management-log-cache, management-query-passwords,
management-hold, management-signal, management-forget-disconnect,
management-client-pf, management-client-user,
management-client-group
```

These directives can execute arbitrary commands, load external code, or expose control interfaces – they are never allowed in a secure configuration.

### Unknown Directives

Any directive not in either list is stripped (with a warning). This is a conservative approach: if we don't explicitly trust it, we remove it.

---

## Installation & Requirements

### Requirements

- Python 3.6 or higher.
- No external libraries – uses only the standard library (`os`, `sys`, `re`, `argparse`, `tempfile`, `pathlib`, `typing`).
- A Linux/macOS/Unix environment (the script uses POSIX paths).
- **No root privileges** – the script runs entirely in user space.

### Installation

Simply download `ini.py` and make it executable:

```bash
chmod +x ini.py
```

---

## Usage

### Basic Sanitisation

```bash
python3 ini.py input.ovpn -o output.ovpn
```

Reads `input.ovpn`, strips dangerous directives, and writes the sanitised version to `output.ovpn`.

### Output to Stdout

```bash
python3 ini.py input.ovpn
```

Prints the sanitised configuration to the terminal.

### Generate a Sample Config for Testing

```bash
python3 ini.py --generate-sample
```

Creates a file named `sample.ovpn` in the current directory. This file contains:
- Safe directives (`client`, `dev tun`, `proto udp`, `remote my-vpn.com 1194`, `cipher`, `auth`, `keepalive`, `persist-key`, `persist-tun`, `verb 3`, `fast-io`).
- Dangerous directives (`up`, `down`, `script-security`, `plugin`).
- An inline certificate block (`<ca>...</ca>`).

This lets you test the sanitizer without downloading a real config.

### Self‑Test

```bash
python3 ini.py --self-test
```

Runs a built‑in test that:
- Creates a temporary `.ovpn` with known dangerous directives.
- Sanitises it.
- Asserts that dangerous lines are removed, allowed lines remain, and inline blocks are preserved.
- Expected output: `[INFO] Self-test passed!` and exit code `0`.

---

## Example Run

### 1. Generate a sample config

```bash
$ python3 ini.py --generate-sample
[INFO] Created sample.ovpn – run: python3 ini.py sample.ovpn -o safe.ovpn
```

### 2. Sanitise it

```bash
$ python3 ini.py sample.ovpn -o safe.ovpn
[INFO] Processing: sample.ovpn
[INFO] Stripping dangerous: up
[INFO] Stripping dangerous: down
[INFO] Stripping dangerous: script-security
[INFO] Stripping dangerous: plugin
[INFO] Saved to safe.ovpn
[INFO] Stripped 4 directives.
```

### 3. Inspect the output

```bash
$ cat safe.ovpn
# Sample OpenVPN config – mix of safe & dangerous
client
dev tun
proto udp
remote my-vpn.com 1194
cipher AES-256-GCM
auth SHA256
auth-user-pass auth.txt
<ca>
-----BEGIN CERTIFICATE-----
MIID... (example cert)
-----END CERTIFICATE-----
</ca>
keepalive 10 60
persist-key
persist-tun
verb 3
fast-io
```

**Observations**:
- `up`, `down`, `script-security`, `plugin` are gone.
- The `client`, `remote`, `cipher`, `auth` directives remain.
- The `<ca>` block is preserved exactly as it was.
- A count of stripped directives is printed.

---

## File Manifest

| File | Purpose |
|------|---------|
| `ini.py` | The main script. |
| `sample.ovpn` | Generated sample config (if `--generate-sample` is used). |
| `safe.ovpn` | Example output filename (user‑specified). |

The script does not create any hidden files or directories – all output is explicitly written where you tell it.

---

## Technical Deep‑Dive

### Parsing Algorithm (Pseudo‑code)

```
for each line in input:
    trimmed = line.strip()
    if trimmed is empty or starts with # or ;:
        output line
        continue

    if inside_inline_block:
        output line
        if trimmed == f"</{inline_tag}>":
            inside_inline_block = False
        continue

    if trimmed matches <ca>, <cert>, <key>, <tls-auth>:
        inside_inline_block = True
        inline_tag = matched_tag
        output line
        continue

    directive = first word of trimmed
    if directive in DANGEROUS_LIST:
        strip it (log, count++)
    elif directive in ALLOWED_LIST:
        output line
    else:
        strip it (log, count++)

output sanitised content
```

### Handling Inline Blocks

In OpenVPN, inline blocks are used to embed certificates and keys directly into the configuration file. The format is:

```
<ca>
-----BEGIN CERTIFICATE-----
MIID...
-----END CERTIFICATE-----
</ca>
```

The parser **never** looks inside these blocks. It treats everything between the opening and closing tag as data to be preserved verbatim. This prevents accidental stripping of PEM‑encoded content and preserves the cryptographic material needed for the VPN to work.

### Why This Approach Is Secure

1. **Default‑Deny**: Any directive not explicitly allowed is stripped.
2. **Dangerous Directives Explicitly Blocked**: We maintain a curated list of directives known to be unsafe.
3. **Inline Blocks Preserved**: We never assume we understand the content inside `<ca>` etc. – we treat it as opaque data.
4. **No Execution**: The script never calls `subprocess`, never executes `openvpn`, and never modifies system files.

---

## Security & Limitations

### Security Guarantees

- **No root**: The script runs entirely with the privileges of the invoking user.
- **No system modification**: It only reads the input file and writes the output file (or stdout).
- **No execution**: It never forks, executes, or loads external binaries.
- **No network**: No sockets, no DNS, no API calls.
- **Sandboxed**: All file paths are user‑specified; the script does not touch `/etc`, `/var`, or `/usr`.
- **Safe to run anywhere**: You can run this on a production machine without risk.

### Limitations

- **Stripping may break some configs**: If a config relies on a dangerous directive for legitimate functionality (e.g., `route-up` for custom routing), stripping it will break the config. This is by design – the sanitizer enforces a minimal, secure subset.
- **Not a full OpenVPN parser**: The script does not validate the syntax or semantics of the config; it only filters directives.
- **Inline block tags are hardcoded**: Only `<ca>`, `<cert>`, `<key>`, `<tls-auth>` are recognised. Other inline tags (e.g., `<extra-certs>`) are not handled and will be treated as normal directives.
- **Comments inside inline blocks are preserved**: This is intentional – comments are part of the opaque data.

---

## License

MIT – you are free to use, modify, and distribute this software.  
Please credit the original design if you incorporate it into your own projects.

---

## Author

Siyavuyisa Ntengo
---

For questions or contributions, please open an issue in the repository.
```

#!/usr/bin/env python3
"""
ovpn_hardener.py – OpenVPN config sanitizer (standalone child)
Usage:
    python3 ini.py myconfig.ovpn -o safe.ovpn
    python3 ini.py --generate-sample   # creates a test file
    python3 ini.py --self-test
"""

import sys
import re
import argparse
import tempfile
from pathlib import Path
from typing import Optional

# ---------- Colors ----------
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"

def log(msg: str, color: str = Colors.NC, level: str = "INFO"):
    print(f"{color}[{level}] {msg}{Colors.NC}")

# ---------- Core allow/block lists ----------
ALLOWED = {
    'remote', 'proto', 'dev', 'dev-type', 'ca', 'cert', 'key', 'tls-auth',
    'cipher', 'auth', 'auth-user-pass', 'comp-lzo', 'compress', 'tun-mtu',
    'mtu-disc', 'keepalive', 'ping', 'ping-restart', 'reneg-sec',
    'remote-cert-tls', 'verify-x509-name', 'tls-version-min',
    'data-ciphers', 'data-ciphers-fallback', 'mute-replay-warnings',
    'route', 'route-noexec', 'pull', 'pull-filter', 'client', 'nobind',
    'resolv-retry', 'persist-key', 'persist-tun', 'verb', 'fast-io',
    'route-delay', 'redirect-gateway', 'block-outside-dns',
    'auth-nocache', 'auth-retry', 'socks-proxy',
    'tls-client', 'ns-cert-type', 'remote-random',
}

DANGEROUS = {
    'up', 'down', 'script-security', 'plugin', 'auth-user-pass-verify',
    'tls-verify', 'ipchange', 'route-up', 'route-pre-down',
    'client-connect', 'client-disconnect', 'learn-address',
    'setenv', 'setenv-safe', 'management', 'management-client-auth',
    'management-log-cache', 'management-query-passwords',
    'management-hold', 'management-signal', 'management-forget-disconnect',
    'management-client-pf', 'management-client-user',
    'management-client-group',
}

INLINE_TAGS = {'ca', 'cert', 'key', 'tls-auth'}


class Sanitizer:
    def __init__(self, input_path: Path, output_path: Optional[Path] = None):
        self.input_path = input_path
        self.output_path = output_path
        self.in_inline = False
        self.inline_tag = None
        self.stripped = 0
        self.out_lines = []

    def sanitize(self) -> str:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input not found: {self.input_path}")

        raw = self.input_path.read_text(encoding='utf-8', errors='ignore').splitlines()

        for line in raw:
            trimmed = line.strip()

            # Skip empty lines and comments
            if not trimmed or trimmed[0] in '#;':
                self.out_lines.append(line)
                continue

            # Inside an inline block (e.g., <ca> ... </ca>)
            if self.in_inline:
                self.out_lines.append(line)
                if trimmed == f"</{self.inline_tag}>":
                    self.in_inline = False
                    self.inline_tag = None
                continue

            # Opening inline tag
            m = re.match(r'^<(%s)>$' % '|'.join(INLINE_TAGS), trimmed)
            if m:
                self.in_inline = True
                self.inline_tag = m.group(1)
                self.out_lines.append(line)
                continue

            # Normal directive
            parts = trimmed.split()
            if not parts:
                self.out_lines.append(line)
                continue

            directive = parts[0]

            if directive in DANGEROUS:
                log(f"Stripping dangerous: {directive}", Colors.YELLOW)
                self.stripped += 1
                continue

            if directive in ALLOWED:
                self.out_lines.append(line)
            else:
                log(f"Stripping unknown: {directive}", Colors.YELLOW)
                self.stripped += 1
                continue

        return "\n".join(self.out_lines) + "\n"

    def run(self):
        log(f"Processing: {self.input_path}", Colors.BLUE)
        out = self.sanitize()

        if self.output_path:
            self.output_path.write_text(out)
            log(f"Saved to {self.output_path}", Colors.GREEN)
        else:
            print(out)

        log(f"Stripped {self.stripped} directives.", Colors.GREEN)


def generate_sample():
    sample = """# Sample OpenVPN config – mix of safe & dangerous
client
dev tun
proto udp
remote my-vpn.com 1194
cipher AES-256-GCM
auth SHA256
auth-user-pass auth.txt
up /etc/init.d/openvpn-up      # <-- dangerous
down /etc/init.d/openvpn-down  # <-- dangerous
script-security 2              # <-- dangerous
plugin /usr/lib/plugin.so      # <-- dangerous
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
"""
    Path("sample.ovpn").write_text(sample)
    log("Created sample.ovpn – run: python3 ini.py sample.ovpn -o safe.ovpn", Colors.GREEN)


def self_test():
    log("Self-test...", Colors.YELLOW)
    test = "client\nup bad.sh\nplugin x.so\nremote test.com 1194\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ovpn', delete=False) as f:
        f.write(test)
        p = Path(f.name)

    try:
        s = Sanitizer(p)
        out = s.sanitize()
        assert "up bad.sh" not in out
        assert "plugin x.so" not in out
        assert "client" in out
        assert "remote test.com 1194" in out
        log("Self-test passed!", Colors.GREEN)
        return True
    except Exception as e:
        log(f"Self-test failed: {e}", Colors.RED)
        return False
    finally:
        p.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Sanitize OpenVPN configs")
    parser.add_argument("input", nargs="?", help="Input .ovpn file")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--generate-sample", action="store_true", help="Create sample.ovpn")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    args = parser.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    if args.generate_sample:
        generate_sample()
        return

    if not args.input:
        parser.print_help()
        return

    try:
        Sanitizer(Path(args.input), Path(args.output) if args.output else None).run()
    except Exception as e:
        log(f"Error: {e}", Colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ini.py – Transactional Reverter Demo

A standalone demonstration of atomic system hardening with rollback.
This simulates applying and reverting changes to a mock configuration file,
using a JSON revert stack.

Usage:
    python3 ini.py                    # Interactive demo
    python3 ini.py --dry-run          # Show actions without applying
    python3 ini.py --status           # Show current state
    python3 ini.py --apply            # Apply hardening (PERMISSIVE=0)
    python3 ini.py --revert           # Revert all changes
    python3 ini.py --clean            # Reset config and clear stack

Concepts: transactional operations, idempotency, rollback, clean error handling.
"""

import os
import sys
import json
import signal
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# ---------- Colors ----------
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    NC = "\033[0m"

def log(msg: str, color: str = Colors.NC, level: str = "INFO"):
    print(f"{color}[{level}] {msg}{Colors.NC}")

# ---------- Configuration ----------
BASE_DIR = Path("/tmp/reverter_demo")
CONFIG_FILE = BASE_DIR / "mock.conf"
STACK_FILE = BASE_DIR / "revert-stack.json"

# Default mock config content
DEFAULT_CONFIG = """# Mock system configuration
# This file is used for the transactional reverter demo.

PERMISSIVE=1
ALLOW_DEBUG=1
MAX_CONNECTIONS=100
"""


class TransactionalReverter:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stack: List[Dict[str, Any]] = []

        # Ensure base directory exists
        BASE_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize config if missing
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(DEFAULT_CONFIG)
            log(f"Initialized mock config at {CONFIG_FILE}", Colors.BLUE)

        # Load existing stack if present
        self._load_stack()

    def _load_stack(self):
        """Load revert stack from JSON file."""
        if STACK_FILE.exists():
            try:
                with open(STACK_FILE, 'r') as f:
                    self.stack = json.load(f)
                log(f"Loaded {len(self.stack)} pending reverts.", Colors.BLUE, "DEBUG")
            except json.JSONDecodeError:
                log("Corrupt stack file – resetting.", Colors.RED)
                self.stack = []
                self._save_stack()
        else:
            self.stack = []
            self._save_stack()

    def _save_stack(self):
        """Persist revert stack to JSON."""
        with open(STACK_FILE, 'w') as f:
            json.dump(self.stack, f, indent=2)

    def _read_config(self) -> Dict[str, str]:
        """Parse mock config into a dict of key=value."""
        content = CONFIG_FILE.read_text()
        config = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
        return config

    def _write_config(self, config: Dict[str, str]):
        """Write dict back to mock config, preserving comments and order."""
        lines = CONFIG_FILE.read_text().splitlines()
        new_lines = []
        keys_updated = set()
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                new_lines.append(line)
                continue
            if '=' in stripped:
                key = stripped.split('=', 1)[0].strip()
                if key in config:
                    new_lines.append(f"{key}={config[key]}")
                    keys_updated.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        # Add any new keys not present
        for key, val in config.items():
            if key not in keys_updated:
                new_lines.append(f"{key}={val}")
        CONFIG_FILE.write_text("\n".join(new_lines) + "\n")

    def _push_revert_action(self, key: str, original_value: str, new_value: str):
        """Add an action to the revert stack."""
        action = {
            "key": key,
            "original": original_value,
            "new": new_value,
            "timestamp": datetime.now().isoformat()
        }
        self.stack.append(action)
        self._save_stack()
        log(f"Stacked revert: {key} '{original_value}' → '{new_value}'", Colors.BLUE)

    def apply_harden(self, key: str = "PERMISSIVE", target: str = "0"):
        """Apply a hardening change (e.g., set PERMISSIVE=0)."""
        config = self._read_config()
        if key not in config:
            log(f"Key '{key}' not found in config. Nothing to do.", Colors.YELLOW)
            return
        current = config[key]
        if current == target:
            log(f"{key} already {target}. No change.", Colors.YELLOW)
            return

        # Push revert action
        if not self.dry_run:
            self._push_revert_action(key, current, target)
            config[key] = target
            self._write_config(config)
            log(f"Applied hardening: {key} = {target}", Colors.GREEN)
        else:
            log(f"[DRY-RUN] Would set {key} = {target} (was {current})", Colors.CYAN)

    def revert_all(self):
        """Pop all actions in reverse order and restore originals."""
        if not self.stack:
            log("No actions to revert.", Colors.YELLOW)
            return

        log(f"Reverting {len(self.stack)} actions...", Colors.BLUE)
        # Reverse iterate
        while self.stack:
            action = self.stack.pop()
            key = action["key"]
            original = action["original"]
            if not self.dry_run:
                config = self._read_config()
                config[key] = original
                self._write_config(config)
                log(f"Restored {key} = {original}", Colors.GREEN)
            else:
                log(f"[DRY-RUN] Would restore {key} = {original}", Colors.CYAN)
        self._save_stack()
        log("Revert complete.", Colors.GREEN)

    def status(self):
        """Display current state."""
        config = self._read_config()
        log("Current configuration:", Colors.BLUE)
        for k, v in config.items():
            print(f"  {k} = {v}")
        if self.stack:
            log(f"Pending reverts: {len(self.stack)}", Colors.YELLOW)
            for action in self.stack:
                print(f"  {action['key']}: {action['original']} → {action['new']} (at {action['timestamp']})")
        else:
            log("No pending reverts.", Colors.GREEN)

    def force_clean(self):
        """Delete all state and reset mock config."""
        log("Forcing clean reset...", Colors.RED)
        if not self.dry_run:
            CONFIG_FILE.write_text(DEFAULT_CONFIG)
            self.stack = []
            self._save_stack()
            log("Mock config reset to defaults.", Colors.GREEN)
        else:
            log("[DRY-RUN] Would reset config and clear stack.", Colors.CYAN)


# ---------- Signal Handler ----------
_reverter_instance: Optional[TransactionalReverter] = None

def signal_handler(sig, frame):
    log("Received interrupt. Triggering rollback...", Colors.YELLOW)
    if _reverter_instance:
        _reverter_instance.revert_all()
    sys.exit(0)


# ---------- Interactive Demo ----------
def interactive_demo():
    global _reverter_instance
    reverter = TransactionalReverter(dry_run=False)
    _reverter_instance = reverter

    log("=== Transactional Reverter Demo ===", Colors.CYAN)
    log(f"Mock config: {CONFIG_FILE}", Colors.BLUE)
    log("Press Ctrl+C at any time to revert all changes.", Colors.YELLOW)
    log("Commands: apply, status, revert, clean, quit", Colors.BLUE)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd in ("quit", "exit"):
            if reverter.stack:
                log("You have pending changes. Reverting...", Colors.YELLOW)
                reverter.revert_all()
            break
        elif cmd == "apply":
            reverter.apply_harden()
        elif cmd == "status":
            reverter.status()
        elif cmd == "revert":
            reverter.revert_all()
        elif cmd == "clean":
            reverter.force_clean()
        else:
            log("Commands: apply, status, revert, clean, quit", Colors.YELLOW)


# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Transactional reverter demo")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without applying")
    parser.add_argument("--status", action="store_true", help="Show current state")
    parser.add_argument("--apply", action="store_true", help="Apply hardening (PERMISSIVE=0)")
    parser.add_argument("--revert", action="store_true", help="Revert all changes")
    parser.add_argument("--clean", action="store_true", help="Reset config and clear stack")
    args = parser.parse_args()

    reverter = TransactionalReverter(dry_run=args.dry_run)

    if args.revert:
        reverter.revert_all()
        return
    if args.clean:
        reverter.force_clean()
        return
    if args.status:
        reverter.status()
        return
    if args.apply:
        reverter.apply_harden()
        return

    # No arguments -> interactive mode
    interactive_demo()


if __name__ == "__main__":
    main()

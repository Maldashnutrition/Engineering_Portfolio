#!/usr/bin/env python3
"""
ini.py – Idle Watchdog Demo

A standalone demonstration of traffic‑aware scheduling.
Monitors a network interface (or mock file) for activity,
and triggers rotation events when traffic drops below a threshold.

Usage:
    python3 ini.py                    # Monitor lo interface (default)
    python3 ini.py --interface eth0  # Monitor a specific interface
    python3 ini.py --mock             # Use a simulated byte counter
    python3 ini.py --dry-run          # Preview actions without triggering
    python3 ini.py --status           # Show current state

Concepts: traffic monitoring, idleness detection, event scheduling,
          predictive heuristics, safe operations.
"""

import os
import sys
import time
import json
import signal
import argparse
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

# ---------- Colors ----------
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    MAGENTA = "\033[0;35m"
    NC = "\033[0m"

def log(msg: str, color: str = Colors.NC, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] [{level}] {msg}{Colors.NC}")

# ---------- Configuration ----------
BASE_DIR = Path("/tmp/watchdog_demo")
STATE_FILE = BASE_DIR / "watchdog_state.json"
MOCK_BYTES_FILE = BASE_DIR / "mock_bytes.txt"

# Default thresholds
CHECK_INTERVAL = 5           # Seconds between checks
ACTIVITY_THRESHOLD = 1024    # Bytes per check interval (if below this, considered idle)
IDLE_CHECKS_REQUIRED = 3     # Consecutive idle checks before triggering rotation
ROTATION_COOLDOWN = 30       # Seconds to wait after a rotation before checking again


class IdleWatchdog:
    def __init__(
        self,
        interface: str = "lo",
        use_mock: bool = False,
        dry_run: bool = False,
        check_interval: int = CHECK_INTERVAL,
        activity_threshold: int = ACTIVITY_THRESHOLD,
        idle_checks: int = IDLE_CHECKS_REQUIRED
    ):
        self.interface = interface
        self.use_mock = use_mock
        self.dry_run = dry_run
        self.check_interval = check_interval
        self.activity_threshold = activity_threshold
        self.idle_checks_required = idle_checks

        self.running = True
        self.idle_counter = 0
        self.last_bytes = 0
        self.last_rotation = 0
        self.total_bytes = 0
        self.bytes_delta = 0
        self.rotation_count = 0

        # Ensure base directory exists
        BASE_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize mock bytes file if using mock mode
        if self.use_mock and not MOCK_BYTES_FILE.exists():
            MOCK_BYTES_FILE.write_text("0")
            log(f"Initialized mock bytes file at {MOCK_BYTES_FILE}", Colors.BLUE)

        # Load persistent state
        self._load_state()

    def _load_state(self):
        """Load persistent state from JSON."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    data = json.load(f)
                self.idle_counter = data.get("idle_counter", 0)
                self.last_bytes = data.get("last_bytes", 0)
                self.last_rotation = data.get("last_rotation", 0)
                self.total_bytes = data.get("total_bytes", 0)
                self.rotation_count = data.get("rotation_count", 0)
                log(f"Loaded state: rotations={self.rotation_count}", Colors.BLUE, "DEBUG")
            except json.JSONDecodeError:
                log("Corrupt state file – resetting.", Colors.RED)
                self._save_state()
        else:
            self._save_state()

    def _save_state(self):
        """Persist state to JSON."""
        data = {
            "idle_counter": self.idle_counter,
            "last_bytes": self.last_bytes,
            "last_rotation": self.last_rotation,
            "total_bytes": self.total_bytes,
            "rotation_count": self.rotation_count
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def _read_bytes_mock(self) -> int:
        """Read from the mock bytes file (simulates traffic)."""
        try:
            content = MOCK_BYTES_FILE.read_text().strip()
            return int(content) if content else 0
        except (FileNotFoundError, ValueError):
            return 0

    def _write_bytes_mock(self, value: int):
        """Write to the mock bytes file."""
        MOCK_BYTES_FILE.write_text(str(value))

    def _read_bytes_real(self) -> int:
        """Read RX bytes from a real network interface."""
        # Handle different OS paths
        stat_paths = [
            f"/sys/class/net/{self.interface}/statistics/rx_bytes",
            f"/sys/class/net/{self.interface}/statistics/rx_bytes"
        ]
        for path in stat_paths:
            try:
                with open(path, 'r') as f:
                    return int(f.read().strip())
            except (FileNotFoundError, ValueError, IOError):
                continue

        # Fallback: try using `ip` command
        try:
            import subprocess
            result = subprocess.run(
                ["ip", "-s", "link", "show", self.interface],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "RX:" in line:
                        # Look for the bytes value in the next line
                        continue
                    if "bytes" in line and line.strip().startswith(str):
                        parts = line.strip().split()
                        for part in parts:
                            if part.isdigit():
                                return int(part)
        except Exception:
            pass

        log(f"Could not read bytes from interface {self.interface}", Colors.YELLOW)
        return 0

    def read_bytes(self) -> int:
        """Read current bytes from either real interface or mock."""
        if self.use_mock:
            return self._read_bytes_mock()
        return self._read_bytes_real()

    def update_mock_traffic(self):
        """Background thread: simulates traffic by randomly incrementing the mock counter."""
        import random
        while self.running:
            current = self._read_bytes_mock()
            # Simulate traffic: random increase between 0 and 5000 bytes
            increment = random.randint(0, 5000)
            new_value = current + increment
            self._write_bytes_mock(new_value)

            # Occasionally inject a burst to simulate active usage
            if random.random() < 0.2:  # 20% chance of burst
                burst = random.randint(10000, 50000)
                new_value = self._read_bytes_mock() + burst
                self._write_bytes_mock(new_value)
                log(f"💥 [SIMULATOR] Traffic burst: +{burst} bytes", Colors.MAGENTA)

            time.sleep(random.randint(2, 10))

    def check_and_trigger(self):
        """Main monitoring loop – checks bytes, detects idleness, triggers rotations."""
        current_bytes = self.read_bytes()
        self.total_bytes = current_bytes

        # Calculate delta since last check
        delta = current_bytes - self.last_bytes
        self.bytes_delta = delta

        # Prevent negative delta (possible on interface reset)
        if delta < 0:
            log(f"Interface reset detected (delta={delta})", Colors.YELLOW)
            self.last_bytes = current_bytes
            return

        # Log current state
        status = "🟢 ACTIVE" if delta >= self.activity_threshold else "🟡 IDLE"
        log(f"{status} | Interface: {self.interface} | Delta: {delta} bytes | Idle counter: {self.idle_counter}",
            Colors.CYAN, "DEBUG")

        # Check if we're idle
        if delta < self.activity_threshold:
            self.idle_counter += 1
            log(f"Idle detected ({self.idle_counter}/{self.idle_checks_required})", Colors.YELLOW)

            if self.idle_counter >= self.idle_checks_required:
                # Check cooldown
                now = time.time()
                if now - self.last_rotation >= ROTATION_COOLDOWN:
                    self._trigger_rotation()
                else:
                    log(f"Rotation cooldown active ({ROTATION_COOLDOWN - (now - self.last_rotation):.0f}s remaining)",
                        Colors.BLUE)
        else:
            # Traffic detected – reset idle counter
            if self.idle_counter > 0:
                log(f"Traffic detected – resetting idle counter", Colors.GREEN)
            self.idle_counter = 0

        self.last_bytes = current_bytes
        self._save_state()

    def _trigger_rotation(self):
        """Execute a rotation event (dry‑run safe)."""
        self.rotation_count += 1
        self.idle_counter = 0
        self.last_rotation = time.time()

        if not self.dry_run:
            action_msg = f"🔄 [ACTION] ROTATING endpoint (rotation #{self.rotation_count})"
            log(action_msg, Colors.GREEN)
            # In production, this would restart VPNs, change routes, etc.
        else:
            log(f"[DRY-RUN] Would rotate endpoint (rotation #{self.rotation_count})", Colors.CYAN)

        self._save_state()

    def status(self):
        """Display current state."""
        log("=== Watchdog Status ===", Colors.BLUE)
        log(f"Interface: {self.interface}", Colors.NC)
        log(f"Mode: {'MOCK' if self.use_mock else 'REAL'}", Colors.NC)
        log(f"Dry-run: {'YES' if self.dry_run else 'NO'}", Colors.NC)
        log(f"Check interval: {self.check_interval}s", Colors.NC)
        log(f"Activity threshold: {self.activity_threshold} bytes/check", Colors.NC)
        log(f"Idle checks required: {self.idle_checks_required}", Colors.NC)
        log(f"Current bytes: {self.total_bytes:,}", Colors.NC)
        log(f"Last delta: {self.bytes_delta:,} bytes", Colors.NC)
        log(f"Idle counter: {self.idle_counter}/{self.idle_checks_required}", Colors.YELLOW if self.idle_counter > 0 else Colors.GREEN)
        log(f"Rotations: {self.rotation_count}", Colors.GREEN)
        if self.last_rotation > 0:
            log(f"Last rotation: {datetime.fromtimestamp(self.last_rotation).strftime('%H:%M:%S')}", Colors.NC)

    def run(self):
        """Start the main monitoring loop."""
        log(f"Starting idle watchdog on interface: {self.interface}", Colors.CYAN)
        log(f"Activity threshold: {self.activity_threshold} bytes/check", Colors.BLUE)
        log(f"Will trigger after {self.idle_checks_required} consecutive idle checks", Colors.BLUE)
        log("Press Ctrl+C to stop.", Colors.YELLOW)

        # Initialize last_bytes
        self.last_bytes = self.read_bytes()

        while self.running:
            try:
                self.check_and_trigger()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                log(f"Error in monitoring loop: {e}", Colors.RED)
                time.sleep(self.check_interval)

        log("Watchdog stopped.", Colors.CYAN)


# ---------- Signal Handler ----------
_watchdog_instance: Optional[IdleWatchdog] = None
_simulator_thread: Optional[threading.Thread] = None

def signal_handler(sig, frame):
    global _watchdog_instance, _simulator_thread
    log("Received interrupt. Stopping...", Colors.YELLOW)
    if _watchdog_instance:
        _watchdog_instance.running = False
    if _simulator_thread and _simulator_thread.is_alive():
        _simulator_thread.join(timeout=2)
    sys.exit(0)


# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(
        description="Idle Watchdog – traffic‑aware scheduling demo",
        epilog="Example: python3 watchdog.py --mock --dry-run"
    )
    parser.add_argument("--interface", default="lo", help="Network interface to monitor (default: lo)")
    parser.add_argument("--mock", action="store_true", help="Use simulated byte counter instead of real interface")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without triggering rotations")
    parser.add_argument("--status", action="store_true", help="Show current state and exit")
    parser.add_argument("--threshold", type=int, default=ACTIVITY_THRESHOLD,
                        help=f"Activity threshold in bytes/check (default: {ACTIVITY_THRESHOLD})")
    parser.add_argument("--idle-checks", type=int, default=IDLE_CHECKS_REQUIRED,
                        help=f"Consecutive idle checks before trigger (default: {IDLE_CHECKS_REQUIRED})")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL,
                        help=f"Check interval in seconds (default: {CHECK_INTERVAL})")
    args = parser.parse_args()

    global _watchdog_instance, _simulator_thread

    # Create watchdog instance
    watchdog = IdleWatchdog(
        interface=args.interface,
        use_mock=args.mock,
        dry_run=args.dry_run,
        check_interval=args.interval,
        activity_threshold=args.threshold,
        idle_checks=args.idle_checks
    )
    _watchdog_instance = watchdog

    if args.status:
        watchdog.status()
        return

    # Start mock simulator if using mock mode
    if args.mock:
        _simulator_thread = threading.Thread(target=watchdog.update_mock_traffic, daemon=True)
        _simulator_thread.start()
        log("Mock traffic simulator started.", Colors.BLUE)

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Run main loop
    try:
        watchdog.run()
    except KeyboardInterrupt:
        pass
    finally:
        watchdog.running = False
        if _simulator_thread and _simulator_thread.is_alive():
            _simulator_thread.join(timeout=2)
        log("Exiting.", Colors.CYAN)


if __name__ == "__main__":
    main()

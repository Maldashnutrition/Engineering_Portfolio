#!/usr/bin/env python3
"""
ini.py

A standalone demonstration of a Finite State Machine (FSM) for DNS leak
detection, forensics collection, diagnosis, and auto-healing.

This is a "shackled" child program extracted from a high-assurance network
isolation system. It simulates the logic without modifying any system
settings, VPNs, or firewalls.

Usage:
    python3 ini.py

Concepts Demonstrated:
    - Stateful incident handling (FSM)
    - Mock forensics collection
    - Simulated diagnostics (cause analysis)
    - Dry-run repair heuristics
"""

import os
import sys
import time
import json
import random
import threading
from pathlib import Path
from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# ---------- Colors (for pretty terminal output) ----------
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    MAGENTA = "\033[0;35m"
    NC = "\033[0m"  # No Color

def log(msg: str, color: str = Colors.NC, level: str = "INFO"):
    """Formatted logging with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {level}: {msg}{Colors.NC}")

# ---------- Configuration ----------
BASE_DIR = Path("/tmp/fsm_demo")
COUNTER_FILE = BASE_DIR / "dns_counter.txt"
FORENSICS_DIR = BASE_DIR / "forensics"
STATE_FILE = BASE_DIR / "fsm_state.json"

# Simulation parameters
LEAK_INJECT_INTERVAL = (8, 15)  # Seconds between random leak injections
TOTAL_BASE = 100  # Starting total DNS queries
LEAK_THRESHOLD = 2  # Consecutive leak failures before triggering killswitch

# ---------- State Definitions ----------
class FSMState(Enum):
    MONITORING = "MONITORING"
    LEAK_DETECTED = "LEAK_DETECTED"
    COLLECTING_FORENSICS = "COLLECTING_FORENSICS"
    DIAGNOSING = "DIAGNOSING"
    REPAIRING = "REPAIRING"
    RECOVERED = "RECOVERED"
    FAILED = "FAILED"  # Would trigger a killswitch in production

# ---------- Core FSM Implementation ----------
class DNSLeakFSM:
    def __init__(self):
        self.state = FSMState.MONITORING
        self.last_total = 0
        self.last_leak = 0
        self.fail_count = 0
        self.forensics_path = None
        self.diagnosis_cause = None
        self.running = True
        self._lock = threading.Lock()

        # Ensure directories exist
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        FORENSICS_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize counter file if not exists
        if not COUNTER_FILE.exists():
            self._write_counter(total=TOTAL_BASE, leak=0)
            self.last_total = TOTAL_BASE
            self.last_leak = 0

    # ---------- State Transitions ----------
    def transition_to(self, new_state: FSMState):
        """Safely transition to a new state and log it."""
        with self._lock:
            old_state = self.state
            self.state = new_state
            log(f"State Transition: {Colors.CYAN}{old_state.value}{Colors.NC} → {Colors.CYAN}{new_state.value}{Colors.NC}", color=Colors.MAGENTA)
            self._save_state()

    def _save_state(self):
        """Persist current state to JSON (useful for recovery demos)."""
        data = {
            "state": self.state.value,
            "last_total": self.last_total,
            "last_leak": self.last_leak,
            "fail_count": self.fail_count,
            "diagnosis": self.diagnosis_cause,
            "forensics": str(self.forensics_path) if self.forensics_path else None
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    # ---------- Mock Data Access ----------
    def _read_counter(self) -> Tuple[int, int]:
        """Reads the mock DNS counter file.
        Format: total_queries:leaked_queries
        """
        try:
            with open(COUNTER_FILE, "r") as f:
                data = f.read().strip().split(":")
                return int(data[0]), int(data[1])
        except (FileNotFoundError, ValueError, IndexError):
            return 0, 0

    def _write_counter(self, total: int, leak: int):
        """Writes to the mock counter file."""
        with open(COUNTER_FILE, "w") as f:
            f.write(f"{total}:{leak}")

    # ---------- FSM Actions ----------
    def check_dns_leak(self) -> bool:
        """Checks the counter for leaks. Returns True if leak is detected."""
        total, leak = self._read_counter()
        log(f"Read counters: Total={total}, Leak={leak}", color=Colors.BLUE, level="DEBUG")

        # Detection logic (mirroring the bash script's logic)
        # If total increased but leak didn't, it's a legitimate DNS query (no leak).
        # If leak increased, it's a leak.
        leak_detected = False
        if total > self.last_total and leak > self.last_leak:
            leak_detected = True
        elif leak > self.last_leak:
            leak_detected = True

        # Always update the last known values
        self.last_total = total
        self.last_leak = leak

        if leak_detected:
            log("🚨 DNS LEAK DETECTED!", color=Colors.RED, level="ALERT")
        else:
            log("✅ No new DNS leaks.", color=Colors.GREEN, level="DEBUG")

        return leak_detected

    def collect_forensics(self):
        """Simulates collecting forensic data. Writes mock files to /tmp."""
        timestamp = int(time.time())
        self.forensics_path = FORENSICS_DIR / f"dump_{timestamp}"
        self.forensics_path.mkdir(parents=True, exist_ok=True)

        # Write mock forensic files (simulating the real ones)
        (self.forensics_path / "nftables.txt").write_text("# Mock nftables rules\nchain output {\n  policy drop;\n  ip daddr 8.8.8.8 drop;\n}")
        (self.forensics_path / "routes.txt").write_text("default via 10.10.0.1 dev host0\n10.10.0.0/24 dev host0 proto kernel")
        (self.forensics_path / "resolv.conf.txt").write_text("nameserver 127.0.0.1\n")
        (self.forensics_path / "interfaces.txt").write_text("1: lo: <LOOPBACK,UP>\n3: tun0: <POINTOPOINT,UP>")
        
        log(f"Forensics dumped to {self.forensics_path}", color=Colors.BLUE)
        self._save_state()

    def diagnose_cause(self) -> str:
        """Simulates analyzing the forensics to determine the leak cause.
        Returns a string representing the diagnosis.
        """
        if not self.forensics_path or not self.forensics_path.exists():
            self.diagnosis_cause = "forensics-missing"
            return self.diagnosis_cause

        # Simulate checks against the mock files
        nftables = (self.forensics_path / "nftables.txt").read_text()
        resolv = (self.forensics_path / "resolv.conf.txt").read_text()
        routes = (self.forensics_path / "routes.txt").read_text()

        # Randomized diagnosis for demonstration purposes
        # In the real script, this uses exact regex/string matching.
        causes = [
            "tor-dnsport-missing",
            "dnsmasq-down",
            "default-route-missing",
            "nftables-dns-redirect-missing",
            "tor-connectivity-failure"
        ]
        # Weight the diagnosis based on mock data to show variety
        if "127.0.0.1" not in resolv:
            cause = "dnsmasq-down"
        elif "tun0" not in routes:
            cause = "default-route-missing"
        else:
            cause = random.choice(causes)

        self.diagnosis_cause = cause
        log(f"Diagnosed cause: {Colors.YELLOW}{cause}{Colors.NC}", color=Colors.CYAN)
        self._save_state()
        return cause

    def attempt_repair(self) -> bool:
        """Simulates executing a repair based on the diagnosis.
        Returns True if repair was successful (simulated).
        """
        log(f"Attempting repair for cause: {Colors.YELLOW}{self.diagnosis_cause}{Colors.NC}", color=Colors.CYAN)

        # In the real script, this would run kill/restart commands.
        # Here, we just print the dry-run actions.
        repair_map = {
            "tor-dnsport-missing": "[DRY-RUN] Would restart Tor with DNSPort",
            "dnsmasq-down": "[DRY-RUN] Would restart dnsmasq",
            "default-route-missing": "[DRY-RUN] Would re-add default route via gateway",
            "nftables-dns-redirect-missing": "[DRY-RUN] Would re-apply nftables DNS redirect rules",
            "tor-connectivity-failure": "[DRY-RUN] Would restart Tor and wait for bootstrap",
        }
        action = repair_map.get(self.diagnosis_cause, "[DRY-RUN] Unknown cause, applying generic restart")
        log(f"🔧 {action}", color=Colors.GREEN)

        # Simulate success (always returns True for demo purposes)
        time.sleep(1.5)  # Simulate repair time
        return True

    def reset_leak_failures(self):
        """Resets the consecutive failure counter."""
        self.fail_count = 0
        log("Leak failure counter reset.", color=Colors.GREEN, level="DEBUG")
        self._save_state()

    # ---------- Main FSM Loop ----------
    def run_cycle(self):
        """Runs one iteration of the FSM."""
        if self.state == FSMState.MONITORING:
            if self.check_dns_leak():
                self.transition_to(FSMState.LEAK_DETECTED)
            # Else remain MONITORING

        elif self.state == FSMState.LEAK_DETECTED:
            self.fail_count += 1
            log(f"Consecutive leak failures: {self.fail_count}/{LEAK_THRESHOLD}", color=Colors.YELLOW)
            if self.fail_count >= LEAK_THRESHOLD:
                log("⚠️ Threshold reached. Engaging killswitch (simulated).", color=Colors.RED)
                self.transition_to(FSMState.FAILED)
                # In production, would run killswitch logic.
                # Here we just stop the FSM.
                self.running = False
            else:
                self.transition_to(FSMState.COLLECTING_FORENSICS)

        elif self.state == FSMState.COLLECTING_FORENSICS:
            self.collect_forensics()
            self.transition_to(FSMState.DIAGNOSING)

        elif self.state == FSMState.DIAGNOSING:
            self.diagnose_cause()
            self.transition_to(FSMState.REPAIRING)

        elif self.state == FSMState.REPAIRING:
            success = self.attempt_repair()
            if success:
                self.transition_to(FSMState.RECOVERED)
            else:
                log("Repair failed!", color=Colors.RED)
                self.transition_to(FSMState.FAILED)
                self.running = False

        elif self.state == FSMState.RECOVERED:
            log("Leak resolved. Returning to monitoring.", color=Colors.GREEN)
            self.reset_leak_failures()
            self.transition_to(FSMState.MONITORING)

        elif self.state == FSMState.FAILED:
            log("FSM in FAILED state. (Simulated killswitch engaged)", color=Colors.RED)
            self.running = False

        # Ensure we save state after any change
        self._save_state()

    def start(self):
        """Starts the FSM event loop."""
        log(f"{Colors.CYAN}Starting DNS Leak FSM Demo...{Colors.NC}", color=Colors.MAGENTA)
        log(f"Watch directory: {BASE_DIR}", color=Colors.BLUE)
        log("Press Ctrl+C to stop.\n", color=Colors.YELLOW)

        while self.running:
            self.run_cycle()
            time.sleep(2)  # Check every 2 seconds

        log("FSM stopped.", color=Colors.MAGENTA)


# ---------- Background Simulator (Injects leaks) ----------
class LeakSimulator:
    """Runs in a background thread to randomly inject DNS leaks."""
    def __init__(self):
        self.running = True
        self.current_total = TOTAL_BASE
        self.current_leak = 0
        self._lock = threading.Lock()

    def stop(self):
        self.running = False

    def _increment_counter(self):
        """Adds a random number of total queries and sometimes increments leaks."""
        with self._lock:
            # Simulate regular DNS traffic (total goes up)
            self.current_total += random.randint(1, 20)

            # Simulate leak: 40% chance of a leak event when total increases
            if random.random() < 0.4:
                self.current_leak += random.randint(1, 5)
                log(f"💉 [SIMULATOR] Injected leak! (Total={self.current_total}, Leak={self.current_leak})", color=Colors.MAGENTA)

            # Write to the counter file
            counter_path = COUNTER_FILE
            with open(counter_path, "w") as f:
                f.write(f"{self.current_total}:{self.current_leak}")

    def run(self):
        """Background loop."""
        log("💡 Leak simulator thread started.", color=Colors.BLUE, level="DEBUG")
        while self.running:
            self._increment_counter()
            # Wait between 8 and 15 seconds before injecting again
            interval = random.randint(*LEAK_INJECT_INTERVAL)
            time.sleep(interval)

        log("Leak simulator stopped.", color=Colors.BLUE, level="DEBUG")


# ---------- Entry Point ----------
def main():
    # Ensure script runs in a clean environment
    if os.geteuid() == 0:
        print("⚠️  This script is designed to run without root privileges.", file=sys.stderr)
        print("   It only writes to /tmp/fsm_demo. Exiting for safety.", file=sys.stderr)
        sys.exit(1)

    # Start the background simulator
    simulator = LeakSimulator()
    sim_thread = threading.Thread(target=simulator.run, daemon=True)
    sim_thread.start()

    try:
        # Start the FSM
        fsm = DNSLeakFSM()
        fsm.start()
    except KeyboardInterrupt:
        print("\n")  # Newline after Ctrl+C
        log("User interrupted. Shutting down...", color=Colors.YELLOW)
    finally:
        simulator.stop()
        sim_thread.join(timeout=1)
        log("Cleanup complete. Exiting.", color=Colors.GREEN)
        sys.exit(0)


if __name__ == "__main__":
    main()

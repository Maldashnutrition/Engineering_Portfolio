# Makefile for FSM DNS Leak Detector
# 
# Targets:
#   test        - Run self-test
#   clean       - Remove Python cache files and temporary demo data
#   help        - Show available targets

.PHONY: test clean help

test:
	@echo "Running self-test..."
	@python3 ini.py --self-test

clean:
	@echo "Removing Python cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Removing /tmp/fsm_demo/ (if exists)..."
	@rm -rf /tmp/fsm_demo/ 2>/dev/null || true
	@echo "Cleanup complete."

help:
	@echo "Available targets:"
	@echo "  test    - Run self-test"
	@echo "  clean   - Remove Python cache files and temporary demo data"
	@echo "  help    - Show this help"

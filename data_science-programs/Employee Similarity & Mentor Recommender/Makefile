.PHONY: help install run clean

help:
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  run        - Run the employee similarity recommender"
	@echo "  clean      - Remove output and cache files"

install:
	pip install -r requirements.txt

run:
	@echo "Running employee similarity recommender..."
	python3 ini.py

clean:
	@echo "Cleaning up..."
	rm -rf output/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Done."

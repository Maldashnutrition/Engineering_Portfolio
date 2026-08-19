.PHONY: help install data run clean

help:
	@echo "Available targets:"
	@echo "  install   - Install Python dependencies"
	@echo "  data      - Symlink or copy library.db into data/ (manual step)"
	@echo "  run       - Run the EDA analysis and generate plots"
	@echo "  clean     - Remove output and cache files"

install:
	pip install -r requirements.txt

run:
	@echo "Running analysis..."
	python src/run_analysis.py

clean:
	@echo "Cleaning up..."
	rm -rf output/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Done."

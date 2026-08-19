.PHONY: init seed reset clean query interactive help

init:
	@echo "Creating database schema..."
	@python3 ini.py init

seed:
	@echo "Loading sample data..."
	@python3 ini.py seed

reset:
	@python3 ini.py reset

clean:
	@echo "Removing database and Python cache files..."
	@rm -f logs.db
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete."

query:
	@if [ -z "$(SQL)" ]; then \
		echo "Error: Please specify SQL query. Usage: make query SQL='SELECT * FROM web_logs LIMIT 5;'"; \
		exit 1; \
	fi
	@python3 ini.py query "$(SQL)"

interactive:
	@python3 ini.py interactive

help:
	@echo "Available targets:"
	@echo "  init         - Create database schema"
	@echo "  seed         - Load sample data"
	@echo "  reset        - Reset database (delete and recreate)"
	@echo "  clean        - Remove database and Python cache files"
	@echo "  query SQL=   - Run a SQL query (e.g., make query SQL='SELECT * FROM web_logs;')"
	@echo "  interactive  - Start interactive SQL shell"
	@echo "  help         - Show this help"

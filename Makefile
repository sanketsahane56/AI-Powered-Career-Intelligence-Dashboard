.PHONY: help install test run run-prod cli-scan cli-compare clean

PYTHON ?= python
PIP ?= pip
PYTEST ?= pytest

help:
	@echo "CareerIQ Development Commands:"
	@echo "  make install      - Install all requirements"
	@echo "  make test         - Run full pytest test suite"
	@echo "  make run          - Run local development Flask server (port 5000)"
	@echo "  make run-prod     - Run WSGI production server"
	@echo "  make cli-scan     - Run sample CLI resume scan"
	@echo "  make clean        - Clean cache files and temporary test data"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) -v

run:
	$(PYTHON) app.py

run-prod:
	$(PYTHON) wsgi.py

cli-scan:
	$(PYTHON) cli.py scan data/sample_resume.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

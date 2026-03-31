.PHONY: help install test lint format type-check clean coverage htmlcov run

# Default target
help:
	@echo "Available targets:"
	@echo "  install      Install dependencies (production + dev)"
	@echo "  test         Run all tests with coverage"
	@echo "  lint         Run flake8 linter"
	@echo "  format       Format code with black"
	@echo "  type-check   Run mypy static type checker"
	@echo "  check        Run lint, format, type-check, and tests"
	@echo "  coverage     Generate and open HTML coverage report"
	@echo "  clean        Remove temporary files and caches"
	@echo "  run          Run the Flask application (debug mode)"

# Install dependencies
install:
	pip install -e ".[dev]"

# Run tests
test:
	pytest

# Run tests with verbose output and stop on first failure
test-verbose:
	pytest -v -x

# Run linter
lint:
	flake8 app tests

# Format code
format:
	black app tests
	isort app tests

# Run type checker
type-check:
	mypy app

# Run all quality checks (lint, format, type, test)
check: lint format type-check test

# Generate and open HTML coverage report
coverage:
	pytest --cov=app --cov-report=html
	@echo "Opening coverage report..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		start htmlcov/index.html; \
	elif [ "$$(uname)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	else \
		xdg-open htmlcov/index.html; \
	fi

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache htmlcov/ coverage.xml .coverage
	rm -rf build dist *.egg-info

# Run the Flask app (for local development)
run:
	python -m app.main

# Run the app with hot-reload (if using Flask's built-in debugger)
run-dev:
	export FLASK_APP=app.main
	export FLASK_ENV=development
	flask run --host=0.0.0.0 --port=5000

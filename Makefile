# FAIR Data JSON Schema - Root Makefile

.PHONY: help install test lint format docs clean

help:
	@echo "FAIR Data JSON Schema development tasks:"
	@echo "  install    Initialize environment and install dependencies"
	@echo "  test       Run the pytest suite"
	@echo "  lint       Check code quality (Ruff, Mypy)"
	@echo "  format     Format code (Ruff)"
	@echo "  docs       Build the Sphinx documentation"
	@echo "  clean      Remove build artifacts"

install:
	uv sync --all-extras
	uv run pre-commit install

test:
	uv run pytest

lint:
	uv run pre-commit run --all-files

format:
	uv run ruff format .

docs:
	$(MAKE) -C docs html

clean:
	rm -rf dist/ build/ docs/build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Alias for common commands
html: docs

.PHONY: help install install-dev backend frontend test lint format clean

help:
	@echo "Restaurant AI Assistant - Development Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies"
	@echo "  make install-dev      Install dependencies with dev tools"
	@echo ""
	@echo "Running:"
	@echo "  make backend          Start backend (port 8000)"
	@echo "  make frontend         Start frontend (port 5173)"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-fast        Run tests without slow tests"
	@echo "  make test-coverage    Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Check code quality"
	@echo "  make format           Format code with black and isort"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

install-dev:
	pip install -r requirements-dev.txt
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && python main.py

frontend:
	cd frontend && npm run dev

test:
	pytest tests/ -v

test-fast:
	pytest tests/ -v -m "not slow"

test-coverage:
	pytest tests/ --cov=backend --cov-report=html --cov-report=term

lint:
	flake8 backend/ tests/
	mypy backend/

format:
	black backend/ tests/
	isort backend/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf frontend/dist frontend/node_modules

.DEFAULT_GOAL := help

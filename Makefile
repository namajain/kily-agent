.PHONY: help setup setup-react install test test-rest test-frontend test-mock-api test-socketio run-mock-api run-backend run-frontend run-react run-frontend-react run-all stop-all rerun clean format lint

help: ## Show this help message
	@echo "Enhanced QnA Agent System - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup the project with uv
	@echo "Setting up Enhanced QnA Agent System..."
	python3 scripts/setup_uv.py

setup-react: ## Setup the React frontend
	@echo "Setting up React Frontend..."
	python3 scripts/setup_react_frontend.py

install: ## Install dependencies
	@echo "Installing dependencies..."
	uv sync

test: ## Run all tests
	@echo "Running all tests..."
	uv run python -m pytest tests/ -v

test-rest: ## Run REST API tests
	@echo "Running REST API tests..."
	uv run python -m pytest tests/test_rest_api.py -v

test-frontend: ## Run frontend integration tests
	@echo "Running frontend integration tests..."
	uv run python -m pytest tests/test_frontend_integration.py -v

test-mock-api: ## Run Mock API tests
	@echo "Running Mock API tests..."
	uv run python -m pytest tests/test_mock_api.py -v

test-socketio: ## Run Socket.IO chat tests
	@echo "Running Socket.IO chat tests..."
	uv run python -m pytest tests/test_socketio_chat.py -v

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	uv run pytest tests/ --cov=backend --cov=frontend --cov-report=html

run-mock-api: ## Start the Mock API server
	@echo "Starting Mock API server..."
	cd mock_api && uv run python3 server.py &

run-backend: ## Start the backend server
	@echo "Starting backend server..."
	uv run python3 scripts/start_backend.py &



run-react: ## Start the React frontend server
	@echo "Starting React frontend server..."
	cd frontend-react && npm start &

run-frontend-react: ## Start the React frontend server (alias)
	@make run-react

run-all: ## Start all services in parallel
	@echo "Starting all services in parallel..."
	@echo "Starting Mock API server..."
	cd mock_api && uv run python3 server.py &
	@echo "Starting backend server..."
	uv run python3 scripts/start_backend.py &
	@echo "Starting React frontend server..."
	cd frontend-react && npm start &
	@echo "All services starting! Check:"
	@echo "  - Mock API: http://localhost:5002/health"
	@echo "  - Backend: http://localhost:5001/health"
	@echo "  - React Frontend: http://localhost:3000"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@wait

stop-all: ## Stop all running services
	@echo "Stopping all services..."
	@pkill -f "python.*server.py" || true
	@pkill -f "python.*start_backend.py" || true

	@pkill -f "react-scripts" || true
	@pkill -f "node.*react-scripts" || true
	@echo "All services stopped"

rerun: ## Stop all services and start them again
	@echo "Restarting all services..."
	@make stop-all
	@sleep 2
	@make run-all

clean: ## Clean up generated files
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true

format: ## Format code with black and isort
	@echo "Formatting code..."
	uv run black .
	uv run isort .

lint: ## Run linting checks
	@echo "Running linting checks..."
	uv run flake8 .
	uv run mypy backend/ frontend/ --ignore-missing-imports

dev-setup: ## Setup development environment
	@echo "Setting up development environment..."
	uv sync --dev
	uv run pre-commit install

add-dep: ## Add a new dependency (usage: make add-dep PKG=package-name)
	@if [ -z "$(PKG)" ]; then echo "Usage: make add-dep PKG=package-name"; exit 1; fi
	uv add $(PKG)

add-dev-dep: ## Add a new development dependency (usage: make add-dev-dep PKG=package-name)
	@if [ -z "$(PKG)" ]; then echo "Usage: make add-dev-dep PKG=package-name"; exit 1; fi
	uv add --dev $(PKG)

update-deps: ## Update all dependencies
	@echo "Updating dependencies..."
	uv lock --upgrade
	uv sync

.PHONY: help setup setup-react install test test-rest test-frontend test-data-service test-socketio run-data-service run-backend run-react run-frontend-react run-all stop-all rerun clean format lint rsync rotate-logs tail-logs tail-backend tail-data-service tail-frontend tail-conversations show-logs show-conversations clean-logs

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

test-data-service: ## Run Data Service tests
	@echo "Running Data Service tests..."
	uv run python -m pytest tests/test_data_service.py -v

test-socketio: ## Run Socket.IO chat tests
	@echo "Running Socket.IO chat tests..."
	uv run python -m pytest tests/test_socketio_chat.py -v

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	uv run pytest tests/ --cov=backend --cov=frontend --cov-report=html

run-data-service: ## Start the Data Service
	@echo "Starting Data Service..."
	cd data_service && uv run python3 server.py &

run-backend: ## Start the backend server
	@echo "Starting backend server..."
	uv run python3 scripts/start_backend.py &



run-react: ## Start the React frontend server with logging
	@echo "Starting React frontend server with logging..."
	uv run python3 scripts/start_frontend_with_logging.py &

run-frontend-react: ## Start the React frontend server (alias)
	@make run-react

run-all: ## Start all services in parallel with logging
	@echo "Starting all services in parallel with logging..."
	@make rotate-logs
	@echo "Starting Data Service..."
	cd data_service && uv run python3 server.py &
	@echo "Starting backend server..."
	uv run python3 scripts/start_backend.py &
	@echo "Starting React frontend server..."
	uv run python3 scripts/start_frontend_with_logging.py &
	@echo "All services starting! Check:"
	@echo "  - Data Service: http://localhost:5002/health"
	@echo "  - Backend: http://localhost:5001/health"
	@echo "  - React Frontend: http://localhost:3000"
	@echo ""
	@echo "Logs available in logs/ directory:"
	@echo "  - Backend: logs/backend.log"
	@echo "  - Data Service: logs/data_service.log"
	@echo "  - Frontend: logs/frontend.log"
	@echo ""
	@echo "Use 'make tail-logs' to follow all logs or:"
	@echo "  - make tail-backend"
	@echo "  - make tail-data-service"
	@echo "  - make tail-frontend"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@wait

stop-all: ## Stop all running services
	@echo "Stopping all services..."
	@pkill -f "python.*server.py" || true
	@pkill -f "python.*start_backend.py" || true
	@pkill -f "python.*start_frontend_with_logging.py" || true
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

install-voice-deps: ## Install voice processing dependencies
	@echo "Installing voice processing dependencies..."
	uv add elevenlabs
	# uv add openai-whisper  # Commented out - not needed for ElevenLabs TTS

# Logging Commands
rotate-logs: ## Rotate log files (current -> .old)
	@echo "Rotating log files..."
	@uv run python3 -c "from backend.utils.logging_config import rotate_logs; rotate_logs()"

tail-logs: ## Follow all service logs
	@echo "Following all service logs (Ctrl+C to stop)..."
	@mkdir -p logs
	@touch logs/backend.log logs/data_service.log logs/frontend.log
	@tail -f logs/backend.log logs/data_service.log logs/frontend.log

tail-backend: ## Follow backend logs
	@echo "Following backend logs (Ctrl+C to stop)..."
	@mkdir -p logs
	@touch logs/backend.log
	@tail -f logs/backend.log

tail-data-service: ## Follow data service logs
	@echo "Following data service logs (Ctrl+C to stop)..."
	@mkdir -p logs
	@touch logs/data_service.log
	@tail -f logs/data_service.log

tail-frontend: ## Follow frontend logs
	@echo "Following frontend logs (Ctrl+C to stop)..."
	@mkdir -p logs
	@touch logs/frontend.log
	@tail -f logs/frontend.log

tail-conversations: ## Follow conversation logs
	@echo "Following conversation logs (Ctrl+C to stop)..."
	@mkdir -p logs
	@touch logs/conversations.log
	@tail -f logs/conversations.log

show-conversations: ## Show recent conversation logs
	@echo "=== CONVERSATION LOGS ==="
	@tail -n 30 logs/conversations.log 2>/dev/null || echo "No conversation logs found"

show-logs: ## Show recent logs from all services
	@echo "=== BACKEND LOGS ==="
	@tail -n 20 logs/backend.log 2>/dev/null || echo "No backend logs found"
	@echo ""
	@echo "=== DATA SERVICE LOGS ==="
	@tail -n 20 logs/data_service.log 2>/dev/null || echo "No data service logs found"
	@echo ""
	@echo "=== FRONTEND LOGS ==="
	@tail -n 20 logs/frontend.log 2>/dev/null || echo "No frontend logs found"
	@echo ""
	@echo "=== CONVERSATION LOGS ==="
	@tail -n 20 logs/conversations.log 2>/dev/null || echo "No conversation logs found"

clean-logs: ## Clean all log files
	@echo "Cleaning log files..."
	@rm -f logs/*.log logs/*.log.old
	@echo "Log files cleaned"

update-deps: ## Update all dependencies
	@echo "Updating dependencies..."
	uv lock --upgrade
	uv sync

# Docker Commands
docker-build: ## Build all Docker images
	@echo "Building Docker images..."
	docker compose build

docker-up: ## Start all services with Docker Compose
	@echo "Starting services with Docker Compose..."
	docker compose up -d

docker-down: ## Stop all Docker services
	@echo "Stopping Docker services..."
	docker compose down

docker-logs: ## View Docker logs
	@echo "Showing Docker logs..."
	docker compose logs -f

docker-clean: ## Clean up Docker resources
	@echo "Cleaning up Docker resources..."
	docker compose down -v
	docker system prune -f

docker-restart: ## Restart all Docker services
	@echo "Restarting Docker services..."
	docker compose restart

docker-status: ## Show status of Docker services
	@echo "Docker services status:"
	docker compose ps

rsync: ## Sync project to EC2 instance (one-directional, replaces everything)
	@echo "Syncing project to EC2 instance (replacing everything)..."
	@echo "📁 Syncing frontend-react files..."
	rsync -avz --delete \
		--exclude='.git' \
		--exclude='.venv' \
		--exclude='node_modules' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.pytest_cache' \
		--exclude='artifacts' \
		--exclude='*.log' \
		--exclude='.DS_Store' \
		--exclude='kily-agent.zip' \
		--include='frontend-react/**' \
		-e "ssh -i nj.pem" \
		./ \
		ec2-user@ec2-3-111-213-7.ap-south-1.compute.amazonaws.com:~/ec2_user/
	@echo "✅ Project synced to EC2 instance (replaced everything)!"

rsync-frontend: ## Sync only frontend-react files to EC2 instance
	@echo "Syncing frontend-react files to EC2 instance..."
	rsync -avz --delete \
		--exclude='node_modules' \
		--exclude='.DS_Store' \
		-e "ssh -i nj.pem" \
		frontend-react/ \
		ec2-user@ec2-3-111-213-7.ap-south-1.compute.amazonaws.com:~/ec2_user/frontend-react/
	@echo "✅ Frontend files synced to EC2 instance!"

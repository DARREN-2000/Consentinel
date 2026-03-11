.PHONY: help up down dev test lint build clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start production stack
	docker compose up --build -d

down: ## Stop the stack
	docker compose down

dev: ## Start development stack with hot-reload
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

test: ## Run backend tests
	cd backend && python -m pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=term-missing

lint: ## Lint backend code
	cd backend && python -m ruff check app/ tests/

format: ## Format backend code
	cd backend && python -m ruff format app/ tests/

build: ## Build Docker images
	docker compose build

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

logs: ## Tail backend logs
	docker compose logs -f backend

db-shell: ## Open PostgreSQL shell
	docker compose exec db psql -U relevance_engine -d relevance_engine

redis-cli: ## Open Redis CLI
	docker compose exec redis redis-cli

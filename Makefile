.PHONY: help install dev-up dev-down build up down logs clean test migrate migrate-upgrade migrate-downgrade format lint

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

dev-up: ## Start development environment with docker-compose
	cd infrastructure/docker && docker-compose up -d

dev-down: ## Stop development environment
	cd infrastructure/docker && docker-compose down

build: ## Build Docker images
	cd infrastructure/docker && docker-compose build

up: ## Start all services
	cd infrastructure/docker && docker-compose up

down: ## Stop all services
	cd infrastructure/docker && docker-compose down

logs: ## View logs from all services
	cd infrastructure/docker && docker-compose logs -f

clean: ## Clean up Docker volumes and containers
	cd infrastructure/docker && docker-compose down -v
	docker system prune -f

test: ## Run tests
	pytest tests/ -v

migrate: ## Create a new migration
	alembic revision --autogenerate -m "$(msg)"

migrate-upgrade: ## Apply migrations
	alembic upgrade head

migrate-downgrade: ## Rollback last migration
	alembic downgrade -1

format: ## Format code with black
	black .

lint: ## Lint code with flake8
	flake8 .

run-auth: ## Run auth service locally
	cd apps/auth_service && uvicorn main:app --reload --port 8000

run-product: ## Run product service locally
	cd apps/product_service && uvicorn main:app --reload --port 8001

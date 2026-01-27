.PHONY: help install dev-up dev-down build up down logs clean test runserver makemigrations migrate migrate-check migrate-show migrate-rollback migrate-history migrate-current format lint shell

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
	python manage.py test

runserver: ## Start development server (Django-like)
	python manage.py runserver

runserver-port: ## Start development server on custom port (usage: make runserver-port PORT=8080)
	python manage.py runserver --port $(PORT)

makemigrations: ## Create new migration (Django-like, usage: make makemigrations msg="description")
	python manage.py makemigrations -m "$(msg)"

makemigrations-empty: ## Create empty migration (usage: make makemigrations-empty msg="description")
	python manage.py makemigrations --empty -m "$(msg)"

migrate: ## Apply all pending migrations (Django-like)
	python manage.py migrate

migrate-check: ## Check for pending migrations
	python manage.py migrate-check

migrate-show: ## Show all migrations and their status (Django-like)
	python manage.py showmigrations

migrate-rollback: ## Rollback last migration
	python manage.py migrate --downgrade

migrate-history: ## Show migration history
	python manage.py migrate-history

migrate-current: ## Show current migration
	python manage.py migrate-current

shell: ## Start Python shell with database (Django-like)
	python manage.py shell

format: ## Format code with black
	black .

lint: ## Lint code with flake8
	flake8 .

lint: ## Lint code with flake8
	flake8 .

run-auth: ## Run auth service locally
	cd apps/auth_service && uvicorn main:app --reload --port 8000

run-product: ## Run product service locally
	cd apps/product_service && uvicorn main:app --reload --port 8001

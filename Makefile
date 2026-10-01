# ==============================================================================
# Makefile: Automated Docker Deployment Developer Commands
# ==============================================================================

.PHONY: help install test run docker-build docker-run docker-stop clean

IMAGE_NAME ?= automated-docker-app
CONTAINER_NAME ?= automated_docker_app
PORT ?= 5000

help:
	@echo "Available commands:"
	@echo "  make install       Install application dependencies"
	@echo "  make test          Run automated unit tests with Pytest"
	@echo "  make run           Run Flask application locally"
	@echo "  make docker-build  Build the Docker container image"
	@echo "  make docker-run    Run the application in a Docker container"
	@echo "  make docker-stop   Stop and remove the running Docker container"
	@echo "  make clean         Remove Python cache and temporary test files"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -v test_app.py

run:
	python app.py

docker-build:
	docker build -t $(IMAGE_NAME):latest .

docker-run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) -e PORT=$(PORT) $(IMAGE_NAME):latest

docker-stop:
	docker stop $(CONTAINER_NAME) 2>/dev/null || true
	docker rm $(CONTAINER_NAME) 2>/dev/null || true

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

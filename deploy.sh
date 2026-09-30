#!/bin/bash
# ==============================================================================
# deploy.sh - Automated Docker Deployment Script (Linux / macOS / Git Bash)
# ==============================================================================
# This script automates deploying the latest Docker image:
# 1. Pulls the latest Docker image from the registry
# 2. Stops and removes the old running container
# 3. Starts the new container
# 4. Performs an automated health check
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

# Configuration variables
IMAGE_NAME="${DOCKER_IMAGE:-automated-docker-app}"
IMAGE_TAG="${DOCKER_TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-automated_docker_app}"
HOST_PORT="${HOST_PORT:-5000}"
CONTAINER_PORT="${CONTAINER_PORT:-5000}"

echo "========================================================"
echo "🚀 Starting Automated Docker Deployment"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Container: ${CONTAINER_NAME}"
echo "========================================================"

# Step 1: Pull the latest image (if using a remote registry like Docker Hub)
echo "[1/4] 📦 Pulling the latest image..."
if docker pull "${IMAGE_NAME}:${IMAGE_TAG}" 2>/dev/null; then
    echo "✔ Successfully pulled latest image."
else
    echo "ℹ Local image build fallback (or remote pull skipped)."
fi

# Step 2: Gracefully stop and remove the existing container if running
echo "[2/4] 🛑 Checking for existing container..."
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Stopping existing container: ${CONTAINER_NAME}..."
    docker stop "${CONTAINER_NAME}"
fi

if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Removing old container: ${CONTAINER_NAME}..."
    docker rm "${CONTAINER_NAME}"
fi

# Step 3: Run the newly updated container
echo "[3/4] 🚀 Launching new container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "${HOST_PORT}:${CONTAINER_PORT}" \
    -e PORT="${CONTAINER_PORT}" \
    -e APP_VERSION="1.0.0" \
    -e APP_ENV="production" \
    "${IMAGE_NAME}:${IMAGE_TAG}"

# Step 4: Health Check verification
echo "[4/4] 🩺 Verifying container health..."
HEALTH_CHECK_URL="http://localhost:${HOST_PORT}/health"
MAX_RETRIES=10
RETRY_COUNT=0
HEALTHY=false

echo "Waiting for service to become healthy at ${HEALTH_CHECK_URL}..."
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    sleep 2
    if curl -s -f "${HEALTH_CHECK_URL}" > /dev/null 2>&1; then
        HEALTHY=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Retry ${RETRY_COUNT}/${MAX_RETRIES}..."
done

if [ "$HEALTHY" = true ]; then
    echo "========================================================"
    echo "🎉 Deployment Successful!"
    echo "🌐 Application is live at: http://localhost:${HOST_PORT}"
    echo "========================================================"
else
    echo "========================================================"
    echo "❌ Deployment Failed: Container did not pass health check!"
    echo "Recent container logs:"
    docker logs --tail 25 "${CONTAINER_NAME}" 2>/dev/null || true
    echo "========================================================"
    exit 1
fi

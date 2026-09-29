# ===================================================================
# Dockerfile: Automated Docker Deployment (Beginner DevOps Project)
# ===================================================================

# Step 1: Base Image
# We use the official lightweight Python 3.11 slim image
FROM python:3.11-slim

# Step 2: Set Environment Variables
# Prevents Python from writing .pyc files to disc and keeps output unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV APP_ENV=production

# Step 3: Set the Working Directory inside the container
WORKDIR /app

# Step 4: Install Dependencies
# Copy requirements first to take advantage of Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Application Code into the container
COPY . .

# Step 6: Expose the Application Port
EXPOSE 5000

# Step 7: Docker Healthcheck
# Docker periodically verifies that our application is healthy using dynamic PORT
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import os, urllib.request; port = os.getenv('PORT', '5000'); urllib.request.urlopen(f'http://localhost:{port}/health')" || exit 1

# Step 8: Start the Application
CMD ["python", "app.py"]

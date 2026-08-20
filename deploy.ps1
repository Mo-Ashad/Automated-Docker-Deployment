# ==============================================================================
# deploy.ps1 - Automated Docker Deployment Script (Windows PowerShell)
# ==============================================================================

param (
    [string]$ImageName = "automated-docker-app",
    [string]$ImageTag = "latest",
    [string]$ContainerName = "automated_docker_app",
    [int]$HostPort = 5000,
    [int]$ContainerPort = 5000
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Automated Docker Deployment" -ForegroundColor Cyan
Write-Host "Image: $ImageName:$ImageTag" -ForegroundColor Gray
Write-Host "Container: $ContainerName" -ForegroundColor Gray
Write-Host "========================================================" -ForegroundColor Cyan

# Step 1: Pull the latest image
Write-Host "[1/4] 📦 Pulling the latest image..." -ForegroundColor Yellow
try {
    docker pull "$ImageName:$ImageTag" 2>$null
    Write-Host "✔ Successfully pulled latest image." -ForegroundColor Green
} catch {
    Write-Host "ℹ Local image build fallback (or remote pull skipped)." -ForegroundColor Gray
}

# Step 2: Stop and remove existing container
Write-Host "[2/4] 🛑 Checking for existing container..." -ForegroundColor Yellow
$running = docker ps -q -f "name=^/${ContainerName}$"
if ($running) {
    Write-Host "Stopping existing container: $ContainerName..." -ForegroundColor Gray
    docker stop $ContainerName | Out-Null
}

$exists = docker ps -aq -f "name=^/${ContainerName}$"
if ($exists) {
    Write-Host "Removing old container: $ContainerName..." -ForegroundColor Gray
    docker rm $ContainerName | Out-Null
}

# Step 3: Run the new container
Write-Host "[3/4] 🚀 Launching new container..." -ForegroundColor Yellow
docker run -d `
    --name $ContainerName `
    --restart unless-stopped `
    -p "${HostPort}:${ContainerPort}" `
    -e APP_VERSION="1.0.0" `
    -e APP_ENV="production" `
    "$ImageName:$ImageTag" | Out-Null

# Step 4: Health Check verification
Write-Host "[4/4] 🩺 Verifying container health..." -ForegroundColor Yellow
$healthUrl = "http://localhost:${HostPort}/health"
$maxRetries = 10
$retryCount = 0
$healthy = $false

Write-Host "Waiting for service to become healthy at $healthUrl..." -ForegroundColor Gray
while ($retryCount -lt $maxRetries) {
    Start-Sleep -Seconds 2
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.status -eq "healthy") {
            $healthy = $true
            break
        }
    } catch {
        # Retry on failure
    }
    $retryCount++
    Write-Host "Retry $retryCount/$maxRetries..." -ForegroundColor Gray
}

if ($healthy) {
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "🎉 Deployment Successful!" -ForegroundColor Green
    Write-Host "🌐 Application is live at: http://localhost:$HostPort" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
} else {
    Write-Host "========================================================" -ForegroundColor Red
    Write-Host "❌ Deployment Failed: Container did not pass health check!" -ForegroundColor Red
    Write-Host "Check container logs with: docker logs $ContainerName" -ForegroundColor Red
    Write-Host "========================================================" -ForegroundColor Red
    exit 1
}

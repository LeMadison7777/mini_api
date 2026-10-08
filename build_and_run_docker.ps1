param(
    [int]$TimeoutSeconds = 60
)

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed or not in PATH. Please install Docker Desktop for Windows and retry."
    exit 1
}

Write-Host "Building docker images..."
docker compose build --no-cache

Write-Host "Starting containers..."
docker compose up -d

Write-Host "Waiting for service to respond on http://127.0.0.1:5000/api/bikes"
$end = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $end) {
    try {
        $r = curl.exe -s -o nul -w "%{http_code}" http://127.0.0.1:5000/api/bikes
        if ($r -eq '200') { Write-Host 'Service ready.'; exit 0 }
    } catch { }
    Start-Sleep -Seconds 1
}

Write-Error "Timeout waiting for service to be ready."
exit 1

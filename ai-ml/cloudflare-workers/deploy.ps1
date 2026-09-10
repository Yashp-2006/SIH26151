#!/usr/bin/env pwsh
# deploy.ps1 — authenticate wrangler and deploy pramana-workers to Cloudflare free tier
# Run from: cloudflare-workers\

Set-Location $PSScriptRoot

Write-Host "=== Pramana Workers Deploy Script ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Login (opens browser OAuth flow)
Write-Host "[1/3] Logging into Cloudflare..." -ForegroundColor Yellow
npx wrangler login
if ($LASTEXITCODE -ne 0) {
    Write-Host "Login failed. Exiting." -ForegroundColor Red
    exit 1
}

# Step 2: Verify auth
Write-Host ""
Write-Host "[2/3] Verifying authentication..." -ForegroundColor Yellow
npx wrangler whoami
if ($LASTEXITCODE -ne 0) {
    Write-Host "Auth check failed. Exiting." -ForegroundColor Red
    exit 1
}

# Step 3: Deploy
Write-Host ""
Write-Host "[3/3] Deploying pramana-workers to Cloudflare free tier..." -ForegroundColor Yellow
npx wrangler deploy
if ($LASTEXITCODE -ne 0) {
    Write-Host "Deploy failed. See error above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Deploy complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Test your routes (replace YOUR_SUBDOMAIN with your workers.dev subdomain):" -ForegroundColor Cyan
Write-Host ""
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/extract -H "Content-Type: application/json" -d "{\"text\":\"Send to 1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf Na\"}"'
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/rarity  -H "Content-Type: application/json" -d "{\"indicator\":\"abc\",\"corpus_counts\":{\"abc\":3,\"def\":10}}"'
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/wallet  -H "Content-Type: application/json" -d "{\"transactions\":[{\"inputs\":[\"a1\",\"a2\"]}]}"'
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/temporal -H "Content-Type: application/json" -d "{\"events_a\":[\"2024-01-01\"],\"events_b\":[\"2024-01-03\"],\"window_days\":5}"'
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/infra    -H "Content-Type: application/json" -d "{\"metadata\":{\"tls\":{\"subject\":\"CN=test\",\"san\":[]},\"headers\":{}}}"'
Write-Host 'curl -X POST https://pramana-workers.YOUR_SUBDOMAIN.workers.dev/template -H "Content-Type: application/json" -d "{\"text\":\"Item:\nPrice: \$10.00\n\"}"'

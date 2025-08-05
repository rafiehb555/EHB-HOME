# Push to GitHub Script
# This script helps push the EHB Home Page project to GitHub

Write-Host "🚀 EHB Home Page - GitHub Push Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "auto_push_system.py")) {
    Write-Host "❌ Error: Please run this script from the EHB Home Page project directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found EHB Home Page project" -ForegroundColor Green

# Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Found changes to commit:" -ForegroundColor Yellow
    Write-Host $status -ForegroundColor Cyan
} else {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
}

# Add all files
Write-Host "📦 Adding all files..." -ForegroundColor Yellow
git add .

# Commit changes
$commitMessage = "EHB Home Page - Complete Auto-Push System with All APIs and SDKs - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "💾 Committing changes: $commitMessage" -ForegroundColor Yellow
git commit -m $commitMessage

# Check remote
Write-Host "🔗 Checking remote configuration..." -ForegroundColor Yellow
$remote = git remote get-url origin
Write-Host "Remote URL: $remote" -ForegroundColor Cyan

# Try to push
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push origin main
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "🌐 Visit: https://github.com/rafiehb555/EHB-HOME" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Push failed. Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try these solutions:" -ForegroundColor Yellow
    Write-Host "   1. Add SSH key to GitHub: https://github.com/settings/keys" -ForegroundColor White
    Write-Host "   2. Create Personal Access Token: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "   3. Use HTTPS with token: git remote set-url origin https://rafiehb555:TOKEN@github.com/rafiehb555/EHB-HOME.git" -ForegroundColor White
}

Write-Host "🎉 Script completed!" -ForegroundColor Green

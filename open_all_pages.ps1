Write-Host "Opening all EHB pages in browser..." -ForegroundColor Green

# Wait a moment for servers to be ready
Start-Sleep -Seconds 2

# Array of URLs to open
$urls = @(
    "http://localhost:3000",
    "http://localhost:3000/dashboard",
    "http://localhost:3000/sql-system",
    "http://localhost:3000/pss",
    "http://localhost:3000/emo",
    "http://localhost:8000/docs"
)

# Open each URL
foreach ($url in $urls) {
    Write-Host "Opening: $url" -ForegroundColor Yellow
    Start-Process $url
    Start-Sleep -Seconds 1
}

Write-Host "`nAll pages opened successfully!" -ForegroundColor Green
Write-Host "`nPages opened:" -ForegroundColor Cyan
Write-Host "- Home Page: http://localhost:3000" -ForegroundColor White
Write-Host "- Dashboard: http://localhost:3000/dashboard" -ForegroundColor White
Write-Host "- SQL System: http://localhost:3000/sql-system" -ForegroundColor White
Write-Host "- PSS System: http://localhost:3000/pss" -ForegroundColor White
Write-Host "- EMO System: http://localhost:3000/emo" -ForegroundColor White
Write-Host "- API Docs: http://localhost:8000/docs" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

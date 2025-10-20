# start_server.ps1
# Autograder Server Startup Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Token-Counter Autograder Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if OpenAI API key is set
if (-not $env:OPENAI_API_KEY -or $env:OPENAI_API_KEY -eq "" -or $env:OPENAI_API_KEY -eq "sk-") {
    Write-Host "❌ ERROR: OpenAI API key not configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your API key before starting the server:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host '  $env:OPENAI_API_KEY="sk-your-actual-key-here"' -ForegroundColor Green
    Write-Host ""
    Write-Host "Get your key from: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "See FIX_API_KEY.md for detailed instructions." -ForegroundColor Cyan
    Write-Host ""
    
    # Prompt user to enter key
    $response = Read-Host "Do you want to enter your API key now? (y/n)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        $apiKey = Read-Host "Enter your OpenAI API key"
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "✅ API key set for this session!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Exiting. Please set your API key and try again." -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
}

# Verify API key format
if ($env:OPENAI_API_KEY -notlike "sk-*") {
    Write-Host "⚠️  WARNING: API key doesn't start with 'sk-'" -ForegroundColor Yellow
    Write-Host "This might not be a valid OpenAI API key." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "✅ OpenAI API key configured" -ForegroundColor Green
Write-Host "   Key: $($env:OPENAI_API_KEY.Substring(0, 7))..." -ForegroundColor Gray
Write-Host ""

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$fastapi = pip show fastapi 2>$null
if (-not $fastapi) {
    Write-Host "⚠️  FastAPI not found. Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host ""
}

Write-Host "🚀 Starting autograder server..." -ForegroundColor Green
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Cyan
Write-Host "  - API: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  - Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start uvicorn
uvicorn main:app --reload


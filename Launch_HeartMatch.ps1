# HeartMatch System PowerShell Launcher
# =====================================

Write-Host "🏠 HeartMatch Enhanced - Child-Family Matching System v2.0" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Helping children find loving families in Massachusetts" -ForegroundColor Green
Write-Host "Features: AI-powered matching, compassionate chatbot, social worker tools" -ForegroundColor Yellow
Write-Host "© 2025 HeartMatch - Child-Family Matching System" -ForegroundColor Magenta
Write-Host ""

# Check Python 3.13
Write-Host "🐍 Checking Python 3.13..." -ForegroundColor Yellow
$pythonPath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313\python.exe"

if (Test-Path $pythonPath) {
    Write-Host "✅ Python 3.13 found!" -ForegroundColor Green
    & $pythonPath "launch_heartmatch.py"
} else {
    Write-Host "❌ Python 3.13 not found at expected location" -ForegroundColor Red
    Write-Host "Trying alternative Python installations..." -ForegroundColor Yellow
    
    # Try other common Python locations
    $altPaths = @(
        "python",
        "py",
        "C:\Python313\python.exe",
        "C:\Program Files\Python313\python.exe"
    )
    
    $found = $false
    foreach ($path in $altPaths) {
        try {
            $version = & $path --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Found Python: $path" -ForegroundColor Green
                & $path "launch_heartmatch.py"
                $found = $true
                break
            }
        } catch {
            # Continue to next path
        }
    }
    
    if (-not $found) {
        Write-Host "❌ No Python installation found!" -ForegroundColor Red
        Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
    }
}

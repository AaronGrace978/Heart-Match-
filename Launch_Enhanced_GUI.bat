@echo off
echo.
echo ========================================
echo 🏠 HeartMatch Enhanced GUI Launcher v2.0
echo ========================================
echo.
echo Starting HeartMatch Enhanced Child-Family Matching System...
echo Features: AI-powered matching, compassionate chatbot, social worker tools
echo Model selection, PII compliance, Massachusetts DCF standards
echo © 2025 HeartMatch - Child-Family Matching System
echo.

REM Check if Python is available
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Trying alternative locations...
    
    REM Try Python 3.13 from AppData
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
        set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
        echo ✅ Found Python 3.13 in AppData
    ) else if exist "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.13\python.exe" (
        set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.13\python.exe
        echo ✅ Found Python 3.13 in Start Menu Programs
    ) else (
        echo ❌ Python not found! Please install Python 3.8+ first.
        echo Download from: https://www.python.org/downloads/
        echo Or add Python to your system PATH
        pause
        exit /b 1
    )
) else (
    set PYTHON_PATH=python
    echo ✅ Python found in PATH!
)

echo ✅ Python found!
echo.

REM Check local Ollama service
echo 🤖 Checking local Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Local Ollama not running. Starting Ollama service...
    start "" "ollama serve"
    timeout /t 5 /nobreak >nul
    
    REM Check again after starting
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Failed to start Ollama service
        echo    Please start Ollama manually: ollama serve
        echo    The enhanced GUI will work with limited AI features
    )
)

echo ✅ Local Ollama service ready!
echo 🌩️  Available models: Mistral 7B, Qwen 72B, Qwen 480B, GPT-OSS 120B
echo 💬 Enhanced features: Compassionate chatbot, social worker tools
echo 🎯 Model selection available in the GUI
echo.

REM Install required packages
echo 📦 Installing required packages...
%PYTHON_PATH% -m pip install PyQt5 requests --quiet
echo ✅ Packages installed!

echo.
echo 🚀 Launching HeartMatch Enhanced GUI...
echo ========================================
echo 🏠 HeartMatch Enhanced - Child-Family Matching System
echo ========================================
echo 🌐 Features:
echo   • AI-powered child-family matching
echo   • Compassionate chatbot for support
echo   • Social worker collaboration tools
echo   • Model selection (Mistral 7B, Qwen, GPT-OSS)
echo   • PII compliance for Massachusetts DCF
echo   • Real-time matching recommendations
echo ========================================
echo.

REM Launch the enhanced application
%PYTHON_PATH% "HeartMatch_Enhanced_GUI.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error launching HeartMatch Enhanced GUI. Please check the error messages above.
    echo.
    echo 💡 Troubleshooting:
    echo    • Ensure Python 3.8+ is installed
    echo    • Check that PyQt5 is installed: pip install PyQt5
    echo    • Verify Ollama is running: ollama serve
    echo    • Try the original GUI: Launch_HeartMatch.bat
    echo.
    pause
)

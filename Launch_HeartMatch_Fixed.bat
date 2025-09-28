@echo off
echo 🚀 Launching HeartMatch Enhanced GUI (Fixed Version)...
echo ========================================

REM Try to find Python
set PYTHON_CMD=
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
) else if exist "C:\Python313\python.exe" (
    set PYTHON_CMD=C:\Python313\python.exe
) else if exist "C:\Python\python.exe" (
    set PYTHON_CMD=C:\Python\python.exe
) else (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found: %PYTHON_CMD%
echo.

REM Check if PyQt5 is installed
echo 🔍 Checking PyQt5 installation...
%PYTHON_CMD% -c "import PyQt5; print('✅ PyQt5 is installed')" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 not found. Installing PyQt5...
    %PYTHON_CMD% -m pip install PyQt5
    if errorlevel 1 (
        echo ❌ Failed to install PyQt5. Please install manually: pip install PyQt5
        pause
        exit /b 1
    )
)

echo.
echo 🎯 Starting HeartMatch Enhanced GUI...
echo ========================================
echo 🏛️ HeartMatch Enhanced - Child-Family Matching System
echo ========================================
echo ✨ Features:
echo   • AI-powered child-family matching
echo   • Compassionate chatbot for support
echo   • Social worker collaboration tools
echo   • Model selection (Mistral 7B, Qwen, GPT-OSS)
echo   • PII compliance for Massachusetts DCF
echo   • Real-time matching recommendations
echo ========================================

REM Launch the GUI
%PYTHON_CMD% HeartMatch_Enhanced_GUI.py

if errorlevel 1 (
    echo.
    echo ❌ Error launching HeartMatch Enhanced GUI. Please check the error messages above.
    echo.
    echo 🔧 Troubleshooting:
    echo   • Ensure Python 3.8+ is installed
    echo   • Check that PyQt5 is installed: pip install PyQt5
    echo   • Verify Ollama is running: ollama serve
    echo   • Try the original GUI: Launch_HeartMatch.bat
    echo.
    pause
) else (
    echo.
    echo ✅ HeartMatch Enhanced GUI launched successfully!
)

echo.
echo Press any key to continue . . .
pause >nul

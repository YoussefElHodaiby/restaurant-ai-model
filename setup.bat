@echo off
echo 🚀 Restaurant AI Reservation Assistant - Quick Start
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Backend setup
echo 📦 Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat

echo 📥 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ⚙️  Backend setup complete!
echo ⚠️  IMPORTANT: Create a .env file in the root directory with your DeepSeek API key:
echo    DEEPSEEK_API_KEY=sk_live_your_key_here
echo.

REM Frontend setup
cd ..\frontend
echo 📦 Setting up frontend...
echo 📥 Installing Node dependencies...
call npm install

echo.
echo ✅ Frontend setup complete!
echo.

REM Summary
echo ======================================================
echo ✨ Setup complete!
echo.
echo To run the application:
echo.
echo Command Prompt 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
echo Command Prompt 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:5173 in your browser
echo ======================================================
pause

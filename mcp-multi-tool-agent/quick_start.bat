@echo off
REM Quick Start Script for MCP Multi-Tool Agent (Windows)
REM This script sets up the project and runs basic tests

echo ============================================
echo 🚀 MCP Multi-Tool Agent - Quick Start
echo ============================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo.
echo 📥 Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -e .

REM Check if .env exists
echo.
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys!
    echo.
    echo Required API Keys:
    echo   - OPENAI_API_KEY (https://platform.openai.com/api-keys)
    echo   - TAVILY_API_KEY (https://tavily.com/)
    echo   - NEWS_API_KEY (https://newsapi.org/)
    echo   - CURRENCY_API_KEY (https://currencyapi.com/) [optional]
    echo.
) else (
    echo ✅ .env file found
)

REM Run tests
echo.
echo 🧪 Running tests...
python test_mcp_tools.py

echo.
echo ============================================
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Edit .env and add your API keys
echo   2. Run: python src/agent.py
echo   3. Try a query like: 'Search for AI news'
echo.
echo For Claude Desktop integration, see:
echo   SETUP_INSTRUCTIONS.md
echo.
echo For usage examples, see:
echo   EXAMPLES.md
echo ============================================
echo.
pause

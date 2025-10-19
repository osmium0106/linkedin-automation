@echo off
REM LinkedIn Automation Bot - Docker Setup Script for Windows
REM This script helps you set up and run the LinkedIn bot with Docker

echo 🐳 LinkedIn Automation Bot - Docker Setup
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop:
    echo    https://docs.docker.com/desktop/windows/
    exit /b 1
)

echo ✅ Docker is installed and ready

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Copying from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your credentials before continuing.
    echo    Required variables: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_ACCESS_TOKEN
    pause
    exit /b 1
)

echo ✅ Environment file found

REM Create necessary directories
if not exist "generated_images" mkdir generated_images
if not exist "logs" mkdir logs
if not exist "config" mkdir config

echo ✅ Created necessary directories

REM Parse command line arguments
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=start

if "%COMMAND%"=="start" goto :start_bot
if "%COMMAND%"=="auth" goto :setup_auth
if "%COMMAND%"=="test" goto :test_bot
if "%COMMAND%"=="generate" goto :generate_content
if "%COMMAND%"=="post" goto :create_post
if "%COMMAND%"=="logs" goto :show_logs
if "%COMMAND%"=="stop" goto :stop_bot
if "%COMMAND%"=="restart" goto :restart_bot
if "%COMMAND%"=="cleanup" goto :cleanup
if "%COMMAND%"=="help" goto :show_help
if "%COMMAND%"=="-h" goto :show_help
if "%COMMAND%"=="--help" goto :show_help

echo ❌ Unknown command: %COMMAND%
echo Use 'docker-run.bat help' to see available commands
exit /b 1

:start_bot
echo 🔨 Building Docker image...
docker-compose build --no-cache
echo 🚀 Starting LinkedIn automation bot...
docker-compose up -d
echo ✅ Bot started successfully!
echo 📊 View logs with: docker-compose logs -f
echo ⏹️  Stop with: docker-compose down
goto :end

:setup_auth
echo 🔐 Running LinkedIn authentication setup...
docker-compose run --rm --service-ports linkedin-bot python setup_auth.py
goto :end

:test_bot
echo 🧪 Testing bot components...
docker-compose run --rm linkedin-bot python main.py test
goto :end

:generate_content
echo 🎨 Generating content...
docker-compose run --rm linkedin-bot python main.py generate
goto :end

:create_post
echo 📤 Creating LinkedIn post...
docker-compose run --rm linkedin-bot python main.py post
goto :end

:show_logs
echo 📋 Showing bot logs...
docker-compose logs -f linkedin-bot
goto :end

:stop_bot
echo ⏹️  Stopping LinkedIn automation bot...
docker-compose down
echo ✅ Bot stopped
goto :end

:restart_bot
echo ⏹️  Stopping LinkedIn automation bot...
docker-compose down
echo 🔨 Building Docker image...
docker-compose build --no-cache
echo 🚀 Starting LinkedIn automation bot...
docker-compose up -d
echo ✅ Bot restarted successfully!
goto :end

:cleanup
echo 🧹 Cleaning up Docker resources...
docker-compose down -v --remove-orphans
docker system prune -f
echo ✅ Cleanup completed
goto :end

:show_help
echo Usage: docker-run.bat [command]
echo.
echo Commands:
echo   start     Start the LinkedIn bot (default)
echo   auth      Run LinkedIn authentication setup
echo   test      Test all bot components
echo   generate  Generate content without posting
echo   post      Create a single LinkedIn post
echo   logs      Show bot logs
echo   stop      Stop the bot
echo   restart   Restart the bot
echo   cleanup   Clean up Docker resources
echo   help      Show this help message
goto :end

:end
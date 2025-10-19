#!/bin/bash

# LinkedIn Automation Bot - Docker Setup Script
# This script helps you set up and run the LinkedIn bot with Docker

set -e

echo "🐳 LinkedIn Automation Bot - Docker Setup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker is installed and ready"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your credentials before continuing."
    echo "   Required variables: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_ACCESS_TOKEN"
    exit 1
fi

echo "✅ Environment file found"

# Create necessary directories
mkdir -p generated_images logs config

echo "✅ Created necessary directories"

# Function to build and start the container
start_bot() {
    echo "🔨 Building Docker image..."
    docker-compose build --no-cache
    
    echo "🚀 Starting LinkedIn automation bot..."
    docker-compose up -d
    
    echo "✅ Bot started successfully!"
    echo "📊 View logs with: docker-compose logs -f"
    echo "⏹️  Stop with: docker-compose down"
}

# Function to run authentication setup
setup_auth() {
    echo "🔐 Running LinkedIn authentication setup..."
    docker-compose run --rm --service-ports linkedin-bot python setup_auth.py
}

# Function to test the bot
test_bot() {
    echo "🧪 Testing bot components..."
    docker-compose run --rm linkedin-bot python main.py test
}

# Function to generate content only
generate_content() {
    echo "🎨 Generating content..."
    docker-compose run --rm linkedin-bot python main.py generate
}

# Function to create a single post
create_post() {
    echo "📤 Creating LinkedIn post..."
    docker-compose run --rm linkedin-bot python main.py post
}

# Function to show logs
show_logs() {
    echo "📋 Showing bot logs..."
    docker-compose logs -f linkedin-bot
}

# Function to stop the bot
stop_bot() {
    echo "⏹️  Stopping LinkedIn automation bot..."
    docker-compose down
    echo "✅ Bot stopped"
}

# Function to clean up
cleanup() {
    echo "🧹 Cleaning up Docker resources..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    echo "✅ Cleanup completed"
}

# Parse command line arguments
case "${1:-start}" in
    "start")
        start_bot
        ;;
    "auth")
        setup_auth
        ;;
    "test")
        test_bot
        ;;
    "generate")
        generate_content
        ;;
    "post")
        create_post
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop_bot
        ;;
    "restart")
        stop_bot
        start_bot
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start     Start the LinkedIn bot (default)"
        echo "  auth      Run LinkedIn authentication setup"
        echo "  test      Test all bot components"
        echo "  generate  Generate content without posting"
        echo "  post      Create a single LinkedIn post"
        echo "  logs      Show bot logs"
        echo "  stop      Stop the bot"
        echo "  restart   Restart the bot"
        echo "  cleanup   Clean up Docker resources"
        echo "  help      Show this help message"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use '$0 help' to see available commands"
        exit 1
        ;;
esac
#!/bin/bash

# Production deployment script for AI Resume Generator

set -e

echo "🚀 Starting AI Resume Generator deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with the required environment variables."
    echo "Required variables:"
    echo "- OPENAI_API_KEY"
    echo "- OPENAI_BASE_URL" 
    echo "- OPENAI_MODEL"
    echo "- SESSION_SECRET_KEY"
    exit 1
fi

# Load environment variables
source .env

# Validate required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ -z "$OPENAI_BASE_URL" ] || [ -z "$OPENAI_MODEL" ]; then
    echo "❌ Required environment variables are missing. Please check your .env file."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo "🔄 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running successfully!"
    echo ""
    echo "🌐 Application is available at: http://localhost"
    echo "📊 Health check: http://localhost/health"
    echo "🔍 Redis: localhost:6379"
    echo ""
    echo "📋 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi
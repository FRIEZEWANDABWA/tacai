#!/bin/bash

# JACAI Deployment Script
# Automated deployment for production environments

set -e

echo "🚀 JACAI Deployment Script"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual API keys before running again."
    exit 1
fi

# Create data directory
mkdir -p data

# Build and start services
echo "🔨 Building JACAI containers..."
docker-compose build

echo "🚀 Starting JACAI services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Test the deployment
echo "🧪 Testing deployment..."
python3 api_test.py

# Show status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ JACAI Deployment Complete!"
echo "🌐 Access your application at: http://localhost:8082"
echo "📊 Health check: http://localhost:8082/api/health"
echo ""
echo "🛠️  Management Commands:"
echo "  Stop services:    docker-compose down"
echo "  View logs:        docker-compose logs -f"
echo "  Restart:          docker-compose restart"
echo "  Update:           git pull && docker-compose up -d --build"
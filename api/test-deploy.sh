#!/bin/bash

# Test deployment script - runs locally to verify Docker setup
set -e

echo "🧪 Testing Docker setup locally..."

# Step 1: Build the image
echo "🏗️ Building Docker image..."
docker build -t smart-home-api:test .

# Step 2: Run container with env file
echo "🚀 Starting test container..."
docker run -d --name smart-home-test \
  -p 5000:8080 \
  -e ASPNETCORE_URLS=http://+:8080 \
  --env-file .env.test \
  --rm \
  smart-home-api:test

# Step 3: Wait for startup
echo "⏳ Waiting for API to start..."
sleep 5

# Step 4: Test endpoint
echo "🔍 Testing API endpoint..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
    docker logs smart-home-test
    exit 1
fi

# Step 5: Cleanup
echo "🧹 Cleaning up..."
docker stop smart-home-test

echo "✅ Local test completed successfully!"
echo "🎯 Ready for deployment to droplet!"
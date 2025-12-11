#!/bin/bash

# Smart Home API Deployment Script
# Usage: ./deploy.sh [droplet-ip] [ssh-user]

set -e  # Exit on any error

# Configuration
DROPLET_IP=${1:-"YOUR_DROPLET_IP"}
SSH_USER=${2:-"root"}
REMOTE_DIR="/opt/smart-home-api"
# SSH options - remove StrictHostKeyChecking=no for security
SSH_OPTS=""

echo "🚀 Deploying Smart Home API to DigitalOcean droplet..."
echo "📍 Target: $SSH_USER@$DROPLET_IP:$REMOTE_DIR"

# Step 1: Prepare remote directory
echo "📁 Creating remote directory structure..."
ssh $SSH_OPTS $SSH_USER@$DROPLET_IP "mkdir -p $REMOTE_DIR"

# Step 2: Copy files to droplet
echo "📦 Copying application files..."
scp $SSH_OPTS -r . $SSH_USER@$DROPLET_IP:$REMOTE_DIR/

# Step 3: Deploy on remote server
echo "🔧 Deploying application..."
ssh $SSH_OPTS $SSH_USER@$DROPLET_IP << EOF
cd $REMOTE_DIR

# Stop existing container
docker-compose down || true

# Build and start new container
docker-compose up -d --build

# Wait for health check
echo "⏳ Waiting for API to be healthy..."
sleep 10

# Check container status
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 API available at: http://$DROPLET_IP:5000"
EOF

echo "🎉 Deployment finished successfully!"
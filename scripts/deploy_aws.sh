#!/bin/bash

# AWS Deployment Script for Enhanced QnA Agent System
# Usage: ./scripts/deploy_aws.sh

set -e

echo "🚀 Deploying Enhanced QnA Agent System to AWS..."

# AWS Server Configuration
AWS_SERVER_IP="3.111.213.7"
AWS_USER="ec2-user"
SSH_KEY="nj.pem"

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY not found in .env file or environment"
    echo "Please add it to your .env file: OPENAI_API_KEY=your_key_here"
    exit 1
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "❌ Error: ELEVENLABS_API_KEY not found in .env file or environment"
    echo "Please add it to your .env file: ELEVENLABS_API_KEY=your_key_here"
    exit 1
fi

echo "✅ Environment variables validated (loaded from .env file)"

# Create .env file for AWS deployment using existing .env as template
echo "📝 Creating .env file for AWS deployment..."
if [ -f ".env" ]; then
    echo "✅ Found existing .env file, using as template..."
    # Copy existing .env and override SERVER_IP for AWS
    cat .env > .env.aws
    # Update or add SERVER_IP for AWS
    if grep -q "^SERVER_IP=" .env.aws; then
        # Replace existing SERVER_IP
        sed -i.bak "s/^SERVER_IP=.*/SERVER_IP=$AWS_SERVER_IP/" .env.aws
    else
        # Add SERVER_IP if it doesn't exist
        echo "SERVER_IP=$AWS_SERVER_IP" >> .env.aws
    fi
    # Clean up backup file
    rm -f .env.aws.bak
else
    echo "⚠️  No .env file found, creating new one..."
    cat > .env.aws << EOF
# API Keys
OPENAI_API_KEY=$OPENAI_API_KEY
ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY

# Server Configuration
SERVER_IP=$AWS_SERVER_IP

# Logging
LOG_LEVEL=INFO
EOF
fi

echo "✅ Created .env.aws file"

# Sync files to AWS server
echo "📤 Syncing files to AWS server..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='artifacts' \
    --exclude='*.log' \
    --exclude='.DS_Store' \
    --exclude='kily-agent.zip' \
    --include='frontend-react/**' \
    -e "ssh -i $SSH_KEY" \
    ./ \
    $AWS_USER@$AWS_SERVER_IP:~/ec2_user/

echo "✅ Files synced to AWS server"

# Copy environment file to AWS
echo "📤 Copying environment file to AWS..."
scp -i $SSH_KEY .env.aws $AWS_USER@$AWS_SERVER_IP:~/ec2_user/.env

echo "✅ Environment file copied"

# SSH into AWS server and deploy
echo "🔧 Deploying on AWS server..."
ssh -i $SSH_KEY $AWS_USER@$AWS_SERVER_IP << 'EOF'
    cd ~/ec2_user
    
    echo "🐳 Building Docker images..."
    docker compose build
    
    echo "🚀 Starting services..."
    echo "🧹 Cleaning up existing containers..."
    docker compose down --remove-orphans
    docker rm -f kily-data-service kily-backend kily-frontend 2>/dev/null || true
    docker system prune -f
    echo "🚀 Starting services..."
    docker compose up -d
    
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    echo "🔍 Checking service status..."
    docker compose ps
    
    echo "📊 Checking service health..."
    curl -f http://localhost/health || echo "Frontend health check failed"
    curl -f http://localhost:5001/health || echo "Backend health check failed"
    curl -f http://localhost:5002/health || echo "Data service health check failed"
    
    echo "✅ Deployment completed!"
    echo "🌐 Frontend: http://3.111.213.7"
    echo "🔧 Backend: http://3.111.213.7:5001"
    echo "📊 Data Service: http://3.111.213.7:5002"
EOF

echo "🎉 AWS deployment completed successfully!"
echo "🌐 Your application is now available at: http://$AWS_SERVER_IP"

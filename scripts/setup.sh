#!/bin/bash

# Setup script for ATB Backend

set -e

echo "🚀 Setting up ATB Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Update .env with your SECRET_KEY (required - project will not run without it)"
    echo "   SECRET_KEY must be at least 32 characters long"
else
    echo "✅ .env file already exists"
fi

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your SECRET_KEY (REQUIRED - project will not run without it)"
echo "2. Run 'python manage.py migrate' to apply database migrations"
echo "3. Run 'python manage.py runserver' to start development server"
echo "   OR"
echo "   Run 'make dev-up' to start with Docker"
echo ""
echo "For more information, see README.md"

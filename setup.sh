#!/bin/bash

# Finnie - Financial AI Engine Setup Script
# This script sets up the development environment using uv

set -e

echo "🚀 Setting up Finnie - Financial AI Engine"
echo "=========================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv is installed"

# Check Python version
python_version=$(uv python list | grep -E "Python 3\.(12|13)" | head -1)
if [ -z "$python_version" ]; then
    echo "📦 Installing Python 3.12..."
    uv python install 3.12
else
    echo "✅ Python 3.12+ is available"
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --all-extras

# Set up pre-commit hooks (if dev dependencies are installed)
if uv run pre-commit --version &> /dev/null; then
    echo "🔧 Setting up pre-commit hooks..."
    uv run pre-commit install
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Finnie Environment Configuration
# Add your API keys and configuration here

# Market Data APIs
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///finnie.db

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_STORE_PATH=./data/vector_store

# Compliance Configuration
JURISDICTION=US
COMPLIANCE_MODE=strict
EOF
    echo "✅ Created .env file - please update with your API keys"
else
    echo "✅ .env file already exists"
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/vector_store
mkdir -p data/documents
mkdir -p logs

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Run the application: uv run finnie"
echo "3. Or run in development mode: uv run streamlit run app/main.py"
echo ""
echo "Available commands:"
echo "  uv run finnie        - Start the application"
echo "  uv run streamlit run app/main.py - Start in development mode"
echo "  uv run pytest        - Run tests"
echo "  uv run black .       - Format code"
echo "  uv run flake8 .      - Lint code"
echo "  uv run mypy .        - Type check"
echo "  uv run mkdocs serve  - Serve documentation"
echo ""
echo "Happy coding! 🚀"

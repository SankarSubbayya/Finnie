#!/bin/bash

# Finnie GitHub Setup Script
# Developed by Sankar Subbayya

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Finnie GitHub Setup Script${NC}"
echo -e "${BLUE}Developed by Sankar Subbayya${NC}"
echo "=================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Please install Git first.${NC}"
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}❌ GitHub username is required${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Setting up repository for user: $GITHUB_USERNAME${NC}"

# Initialize git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}🔧 Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository already exists${NC}"
fi

# Add remote origin
echo -e "${YELLOW}🔗 Adding remote origin...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/finnie.git"
echo -e "${GREEN}✅ Remote origin added${NC}"

# Create comprehensive .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}📝 Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
data/
logs/
*.log
.env.local
.env.production
.env.development

# Database
*.db
*.sqlite
*.sqlite3

# Vector stores
faiss_index/
chroma_db/
*.pkl
*.pickle

# Jupyter
.ipynb_checkpoints/

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Docker
.dockerignore

# AWS
.aws/
*.pem
*.key

# Temporary files
tmp/
temp/
EOF
    echo -e "${GREEN}✅ .gitignore created${NC}"
else
    echo -e "${GREEN}✅ .gitignore already exists${NC}"
fi

# Create LICENSE if it doesn't exist
if [ ! -f "LICENSE" ]; then
    echo -e "${YELLOW}📄 Creating LICENSE...${NC}"
    cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Sankar Subbayya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
    echo -e "${GREEN}✅ LICENSE created${NC}"
else
    echo -e "${GREEN}✅ LICENSE already exists${NC}"
fi

# Update README.md with GitHub badges
if [ -f "README.md" ]; then
    echo -e "${YELLOW}📝 Updating README.md with GitHub badges...${NC}"
    
    # Add badges after the title if they don't exist
    if ! grep -q "github.com" README.md; then
        sed -i '' '2a\
![CI/CD](https://github.com/'$GITHUB_USERNAME'/finnie/workflows/CI/CD%20Pipeline/badge.svg)\
![Documentation](https://github.com/'$GITHUB_USERNAME'/finnie/workflows/Deploy%20Documentation/badge.svg)\
![License](https://img.shields.io/badge/license-MIT-blue.svg)\
![Python](https://img.shields.io/badge/python-3.12-blue.svg)\
' README.md
    fi
    
    echo -e "${GREEN}✅ README.md updated${NC}"
else
    echo -e "${YELLOW}📝 Creating README.md...${NC}"
    cat > README.md << EOF
# 📈 Finnie - Financial AI Engine

![CI/CD](https://github.com/$GITHUB_USERNAME/finnie/workflows/CI/CD%20Pipeline/badge.svg)
![Documentation](https://github.com/$GITHUB_USERNAME/finnie/workflows/Deploy%20Documentation/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)

**Developed by Sankar Subbayya**

A comprehensive financial AI engine built with multi-agent systems, RAG (Retrieval Augmented Generation), and real-time market data integration.

## 🚀 Features

- **Multi-Agent System**: 6 specialized AI agents for different financial tasks
- **RAG System**: Hybrid retrieval with FAISS/Chroma and BM25
- **Real-time Data**: Market quotes, news, and portfolio metrics
- **Streamlit UI**: Beautiful, responsive web interface
- **Educational Focus**: Built for learning and experimentation

## 🏗️ Architecture

\`\`\`mermaid
graph TB
    A[Streamlit UI] --> B[LangGraph Workflow]
    B --> C[Multi-Agent System]
    C --> D[RAG System]
    C --> E[MCP Tools]
    D --> F[Vector Store]
    E --> G[Market APIs]
\`\`\`

## 🛠️ Quick Start

### Prerequisites
- Python 3.12+
- uv package manager

### Installation
\`\`\`bash
# Clone the repository
git clone https://github.com/$GITHUB_USERNAME/finnie.git
cd finnie

# Install dependencies
uv sync --all-extras

# Run the application
uv run finnie
\`\`\`

### Access the App
- Open your browser to \`http://localhost:8501\`
- Explore the Chat, Portfolio, Markets, and Learn tabs

## 📊 Technology Stack

- **Frontend**: Streamlit, Plotly
- **AI/ML**: LangGraph, OpenAI, FAISS
- **Data**: yfinance, Alpha Vantage, PostgreSQL
- **Infrastructure**: Docker, AWS-ready
- **Documentation**: MkDocs Material

## 🧪 Testing

\`\`\`bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Format code
uv run black .

# Lint code
uv run flake8 .
\`\`\`

## 📚 Documentation

\`\`\`bash
# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
\`\`\`

## 🚀 Deployment

### Local Development
\`\`\`bash
uv run streamlit run app/main.py
\`\`\`

### Docker
\`\`\`bash
docker build -t finnie .
docker run -p 8501:8501 finnie
\`\`\`

### AWS Deployment
See [AWS Deployment Guide](docs/deployment/aws-deployment-guide.md) for detailed instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## 📄 License

This project is part of an educational financial AI curriculum. It follows standard open-source practices and educational guidelines for learning purposes.

## 👨‍💻 Author

**Sankar Subbayya**
- GitHub: [@$GITHUB_USERNAME](https://github.com/$GITHUB_USERNAME)
- Email: sankar@example.com

## 🙏 Acknowledgments

- Built with modern AI/ML frameworks
- Inspired by financial education and AI research
- Uses open-source libraries and tools

---

*Finnie - Empowering Financial AI Education through Comprehensive Documentation and Robust Architecture*
EOF
    echo -e "${GREEN}✅ README.md created${NC}"
fi

# Add all files to git
echo -e "${YELLOW}📦 Adding files to git...${NC}"
git add .

# Create initial commit
echo -e "${YELLOW}💾 Creating initial commit...${NC}"
git commit -m "Initial commit: Finnie Financial AI Engine

- Multi-agent system with LangGraph
- RAG implementation with FAISS/Chroma
- Streamlit UI with 4 tabs (Chat, Portfolio, Markets, Learn)
- Real-time market data integration
- Comprehensive documentation with MkDocs
- Docker and AWS deployment ready
- Developed by Sankar Subbayya"

echo -e "${GREEN}✅ Initial commit created${NC}"

# Instructions for manual steps
echo -e "${BLUE}📋 Next Steps:${NC}"
echo -e "${YELLOW}1. Create GitHub repository:${NC}"
echo -e "   Go to https://github.com/new"
echo -e "   Repository name: finnie"
echo -e "   Description: Financial AI Engine - Multi-agent system for portfolio analysis and financial education"
echo -e "   Make it Public"
echo -e "   Don't initialize with README, .gitignore, or license"
echo ""
echo -e "${YELLOW}2. Push to GitHub:${NC}"
echo -e "   git push -u origin main"
echo ""
echo -e "${YELLOW}3. Enable GitHub Pages:${NC}"
echo -e "   Go to Settings → Pages"
echo -e "   Source: GitHub Actions"
echo ""
echo -e "${YELLOW}4. Add repository topics:${NC}"
echo -e "   financial-ai, streamlit, langgraph, rag, portfolio-analysis, machine-learning, python, multi-agent-system"
echo ""
echo -e "${GREEN}🎉 Your Finnie project is ready for GitHub!${NC}"
echo -e "${BLUE}Repository URL will be: https://github.com/$GITHUB_USERNAME/finnie${NC}"

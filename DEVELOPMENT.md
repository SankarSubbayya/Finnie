# Finnie Development Guide

## 🚀 Quick Start with uv

### Prerequisites
- [uv](https://github.com/astral-sh/uv) package manager
- Python 3.12+ (uv will install this automatically)

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd finnie

# Run the automated setup script
./setup.sh

# Or manual setup
uv sync --all-extras
```

## 📦 Dependency Management

### Project Structure
- **pyproject.toml**: Main project configuration and dependencies
- **uv.lock**: Locked dependency versions (auto-generated)
- **.env**: Environment variables and API keys

### Dependency Groups
```bash
# Core dependencies only
uv sync

# With development tools
uv sync --extra dev

# With documentation tools
uv sync --extra docs

# All dependencies
uv sync --all-extras
```

### Adding Dependencies
```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Add with specific version
uv add "package-name>=1.0.0,<2.0.0"

# Add from a different source
uv add git+https://github.com/user/repo.git
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
# Start the Streamlit app in development mode
uv run streamlit run app/main.py

# Or with custom port
uv run streamlit run app/main.py --server.port 8501
```

### Production Mode
```bash
# Start the application
uv run finnie

# Or directly
uv run python run_app.py
```

### Custom Configuration
```bash
# Run with custom port
uv run streamlit run app/main.py --server.port 8502

# Run with custom host
uv run streamlit run app/main.py --server.address 0.0.0.0
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov=agents --cov=graph --cov=rag --cov=tools

# Run specific test file
uv run pytest tests/test_agents.py

# Run with verbose output
uv run pytest -v

# Run with parallel execution
uv run pytest -n auto
```

### Test Configuration
The test configuration is in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=app --cov=agents --cov=graph --cov=rag --cov=tools --cov-report=html --cov-report=term-missing"
```

## 🔧 Code Quality

### Formatting
```bash
# Format code with black
uv run black .

# Check formatting without making changes
uv run black --check .

# Format specific files
uv run black app/ agents/
```

### Linting
```bash
# Lint with flake8
uv run flake8 .

# Lint specific directories
uv run flake8 app/ agents/

# Lint with specific configuration
uv run flake8 --config pyproject.toml .
```

### Type Checking
```bash
# Type check with mypy
uv run mypy .

# Type check specific modules
uv run mypy app/ agents/

# Type check with strict mode
uv run mypy --strict .
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
uv run pre-commit install

# Run hooks on all files
uv run pre-commit run --all-files

# Run hooks on staged files
uv run pre-commit run
```

## 📚 Documentation

### Building Documentation
```bash
# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build

# Deploy documentation
uv run mkdocs gh-deploy
```

### Documentation Structure
- **docs/**: MkDocs documentation source
- **mkdocs.yml**: MkDocs configuration
- **docs/Financial Engine/**: Package-specific documentation

## 🐛 Debugging

### Debug Mode
```bash
# Run with debug logging
uv run python -c "import logging; logging.basicConfig(level=logging.DEBUG)" run_app.py

# Run with specific log level
LOG_LEVEL=DEBUG uv run finnie
```

### Environment Variables
```bash
# Set environment variables
export DEBUG=True
export LOG_LEVEL=DEBUG
uv run finnie

# Or use .env file
echo "DEBUG=True" >> .env
echo "LOG_LEVEL=DEBUG" >> .env
uv run finnie
```

## 🔄 Development Workflow

### Daily Development
1. **Start development server**
   ```bash
   uv run finnie-dev
   ```

2. **Make changes** to the codebase

3. **Run tests** to ensure nothing is broken
   ```bash
   uv run pytest
   ```

4. **Format and lint** code
   ```bash
   uv run black .
   uv run flake8 .
   uv run mypy .
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### Adding New Features
1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Add dependencies** if needed
   ```bash
   uv add new-package
   ```

3. **Implement feature** with tests

4. **Run all checks**
   ```bash
   uv run pytest
   uv run black .
   uv run flake8 .
   uv run mypy .
   ```

5. **Update documentation** if needed

6. **Create pull request**

### Updating Dependencies
```bash
# Update all dependencies
uv sync --upgrade

# Update specific dependency
uv add package-name@latest

# Check for outdated packages
uv tree --outdated
```

## 🚀 Deployment

### Building the Package
```bash
# Build the package
uv build

# Build wheel only
uv build --wheel

# Build source distribution
uv build --sdist
```

### Installing from Source
```bash
# Install in development mode
uv pip install -e .

# Install from built package
uv pip install dist/finnie-0.1.0-py3-none-any.whl
```

## 🐳 Docker Support

### Building Docker Image
```bash
# Build with uv
docker build -t finnie:latest .

# Run container
docker run -p 8501:8501 finnie:latest
```

### Docker Compose
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down
```

## 🔍 Troubleshooting

### Common Issues

#### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

#### Python version issues
```bash
# Install Python 3.12
uv python install 3.12

# Use specific Python version
uv run --python 3.12 finnie
```

#### Dependency conflicts
```bash
# Clear cache and reinstall
uv cache clean
uv sync --reinstall

# Check dependency tree
uv tree
```

#### Port already in use
```bash
# Kill process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
uv run streamlit run app/main.py --server.port 8502
```

### Getting Help
- **uv Documentation**: https://github.com/astral-sh/uv
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Project Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 📋 Checklist

### Before Committing
- [ ] Code formatted with `uv run black .`
- [ ] Code linted with `uv run flake8 .`
- [ ] Type checked with `uv run mypy .`
- [ ] Tests passing with `uv run pytest`
- [ ] Documentation updated if needed
- [ ] Environment variables documented

### Before Deploying
- [ ] All tests passing
- [ ] Code quality checks passing
- [ ] Documentation built successfully
- [ ] Environment variables configured
- [ ] Dependencies locked with `uv.lock`
- [ ] Version bumped in `pyproject.toml`

---

*Happy coding with uv! 🚀*

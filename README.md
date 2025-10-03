# Finnie - Financial AI Engine

A comprehensive financial AI engine built with LangGraph multi-agent system, Streamlit UI, and advanced RAG capabilities.

**Developed by Sankar Subbayya**

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- uv package manager (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finnie
   ```

2. **Install dependencies with uv**
   ```bash
   # Install all dependencies
   uv sync
   
   # Install with development dependencies
   uv sync --extra dev
   
   # Install with documentation dependencies
   uv sync --extra docs
   
   # Install with all extras
   uv sync --all-extras
   ```

3. **Run the application**
   ```bash
   # Using uv (recommended)
   uv run finnie
   
   # Or in development mode
   uv run streamlit run app/main.py
   
   # Or directly
   uv run python run_app.py
   ```

4. **Access the application**
   Open your browser to `http://localhost:8501`

## 🏗️ Architecture

### Multi-Agent System
- **Orchestrator**: Routes queries to appropriate agents
- **Tutor Agent**: Educational content and Socratic Q&A
- **Portfolio Analyst**: Portfolio analysis and metrics
- **Market Intelligence**: Real-time market data and news
- **Compliance Agent**: Ensures regulatory compliance

### Technology Stack
- **Frontend**: Streamlit with Material Design
- **AI Core**: LangGraph multi-agent system
- **RAG**: Hybrid retrieval (BM25 + Vector search)
- **Data**: yfinance, Alpha Vantage APIs
- **Storage**: SQLite/PostgreSQL + FAISS/Chroma

## 📊 Features

### Chat Interface
- Conversational AI with context awareness
- Source attribution and citations
- Follow-up question suggestions
- Quick action buttons

### Portfolio Analysis
- Upload CSV holdings data
- Comprehensive performance metrics
- Risk analysis and recommendations
- Interactive visualizations

### Market Intelligence
- Real-time quotes and news
- Sector performance heatmaps
- Economic calendar
- Watchlist management

### Educational Content
- Structured learning paths
- Interactive quizzes
- Knowledge base search
- Progress tracking

## 🔧 Development

### Project Structure
```
finnie/
├── app/                    # Streamlit application
│   ├── pages/             # UI pages (Chat, Portfolio, Markets, Learn)
│   └── utils.py           # Utility functions
├── agents/                # Multi-agent system
│   ├── orchestrator.py    # Main coordinator
│   ├── tutor.py          # Educational agent
│   ├── portfolio.py      # Portfolio analyst
│   ├── market.py         # Market intelligence
│   └── compliance.py     # Compliance agent
├── graph/                 # LangGraph workflow
│   └── workflow.py       # Main workflow orchestration
├── rag/                  # RAG system
│   ├── ingest.py         # Content ingestion
│   └── retrieve.py       # Hybrid retrieval
├── tools/                # MCP tools
│   ├── mcp_market.py     # Market data tools
│   └── portfolio_metrics.py # Portfolio calculation tools
└── docs/                 # Documentation
```

### Running Tests
```bash
# Using uv
uv run pytest

# Or with coverage
uv run pytest --cov=app --cov=agents --cov=graph --cov=rag --cov=tools
```

### Code Formatting and Linting
```bash
# Format code with black
uv run black .

# Lint with flake8
uv run flake8 .

# Type checking with mypy
uv run mypy .
```

### Building Documentation
```bash
# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

## 📈 Usage Examples

### Portfolio Analysis
```python
from tools.portfolio_metrics import calculate_portfolio_metrics

holdings = [
    {'symbol': 'AAPL', 'quantity': 10, 'cost_basis': 150.00},
    {'symbol': 'MSFT', 'quantity': 5, 'cost_basis': 300.00}
]

metrics = calculate_portfolio_metrics(holdings)
print(f"Sharpe Ratio: {metrics['performance_metrics']['sharpe_ratio']:.2f}")
```

### Market Data
```python
from tools.mcp_market import get_quotes

quotes = get_quotes(['AAPL', 'MSFT', 'GOOGL'])
for symbol, data in quotes.items():
    print(f"{symbol}: ${data['price']:.2f} ({data['change_percent']:+.2f}%)")
```

### RAG Search
```python
from rag.retrieve import RAGSystem

rag = RAGSystem(documents)
results = rag.search("What is portfolio diversification?", k=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"Score: {result['final_score']:.3f}")
```

## 🛡️ Compliance & Safety

- **Regulatory Compliance**: Built-in compliance checks and disclaimers
- **Content Filtering**: Prohibited content detection and sanitization
- **Risk Warnings**: Automatic risk warnings for investment content
- **Source Attribution**: All responses include proper source citations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the SupportVectors AI training curriculum and is subject to the SupportVectors intellectual property guidelines.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

*Finnie - Empowering Financial AI Education through Comprehensive Documentation and Robust Architecture*
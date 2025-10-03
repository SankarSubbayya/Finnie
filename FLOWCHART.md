# Finnie - Quick Reference Flow Chart

## 🚀 How Finnie Works

```mermaid
graph TB
    subgraph "👤 User Interface"
        A[User Opens Finnie] --> B[Choose Tab]
        B --> C[Chat 💬]
        B --> D[Portfolio 📊]
        B --> E[Markets 📈]
        B --> F[Learn 🎓]
    end
    
    subgraph "🧠 AI Brain"
        G[Orchestrator] --> H[Tutor Agent]
        G --> I[Portfolio Agent]
        G --> J[Market Agent]
        G --> K[Compliance Agent]
    end
    
    subgraph "📚 Knowledge Base"
        L[RAG System] --> M[Search Content]
        L --> N[Find Sources]
    end
    
    subgraph "📊 Data Sources"
        O[Market APIs] --> P[Real-time Data]
        Q[Portfolio Calculator] --> R[Risk Metrics]
    end
    
    C --> G
    D --> G
    E --> G
    F --> G
    
    G --> L
    G --> O
    G --> Q
    
    H --> M
    I --> R
    J --> P
    
    M --> S[Generate Response]
    N --> S
    P --> S
    R --> S
    
    S --> T[Show User]
```

## 🔄 User Journey Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Finnie
    participant A as AI Agent
    participant D as Data Source
    
    U->>F: "Analyze my portfolio"
    F->>A: Route to Portfolio Agent
    A->>D: Get market data
    D-->>A: Return quotes & metrics
    A->>A: Calculate Sharpe ratio, risk, etc.
    A-->>F: Portfolio analysis
    F-->>U: "Your portfolio has 15% return, 12% volatility..."
    
    U->>F: "What is diversification?"
    F->>A: Route to Tutor Agent
    A->>D: Search knowledge base
    D-->>A: Educational content
    A-->>F: "Diversification is spreading risk..."
    F-->>U: Educational response with sources
```

## 🏗️ System Architecture

```mermaid
graph LR
    subgraph "Frontend"
        A[Streamlit UI]
    end
    
    subgraph "Backend"
        B[LangGraph Workflow]
        C[Multi-Agent System]
        D[RAG System]
        E[MCP Tools]
    end
    
    subgraph "Data"
        F[Vector Store]
        G[Database]
        H[APIs]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    E --> G
    E --> H
```

## 📋 Quick Start Flow

```mermaid
flowchart TD
    A[Clone Repository] --> B[Run ./setup.sh]
    B --> C[uv sync --all-extras]
    C --> D[uv run finnie]
    D --> E[Open http://localhost:8501]
    E --> F[Start using Finnie!]
    
    F --> G[Upload Portfolio Data]
    F --> H[Ask Questions in Chat]
    F --> I[Check Market Data]
    F --> J[Learn Financial Concepts]
```

## 🎯 Key Features Flow

```mermaid
graph TB
    subgraph "💬 Chat Features"
        A1[Ask Questions] --> A2[Get AI Responses]
        A2 --> A3[View Sources]
        A3 --> A4[Follow-up Questions]
    end
    
    subgraph "📊 Portfolio Features"
        B1[Upload CSV] --> B2[View Analysis]
        B2 --> B3[Risk Metrics]
        B3 --> B4[Recommendations]
    end
    
    subgraph "📈 Market Features"
        C1[Watchlist] --> C2[Real-time Quotes]
        C2 --> C3[News Feed]
        C3 --> C4[Market Calendar]
    end
    
    subgraph "🎓 Learning Features"
        D1[Learning Paths] --> D2[Interactive Lessons]
        D2 --> D3[Quizzes]
        D3 --> D4[Progress Tracking]
    end
```

## 🔧 Development Flow

```mermaid
graph LR
    A[Make Changes] --> B[uv run pytest]
    B --> C[uv run black .]
    C --> D[uv run flake8 .]
    D --> E[uv run mypy .]
    E --> F[Commit Changes]
    F --> G[Deploy]
```

---

**Developed by Sankar Subbayya** | **Finnie - Financial AI Engine**

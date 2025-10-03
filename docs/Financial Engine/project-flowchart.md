# Finnie Project Flow Chart

## System Architecture Overview

This document provides comprehensive flow charts showing the Finnie Financial AI Engine architecture, data flow, and user interactions.

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        A[Streamlit UI] --> B[Chat Tab]
        A --> C[Portfolio Tab]
        A --> D[Markets Tab]
        A --> E[Learn Tab]
    end
    
    subgraph "Multi-Agent System"
        F[Orchestrator Agent] --> G[Tutor Agent]
        F --> H[Portfolio Analyst]
        F --> I[Market Intelligence]
        F --> J[Compliance Agent]
    end
    
    subgraph "Core Services"
        K[LangGraph Workflow] --> F
        L[RAG System] --> M[Content Ingestion]
        L --> N[Hybrid Retrieval]
        O[MCP Tools] --> P[Market Data]
        O --> Q[Portfolio Metrics]
        O --> R[News Service]
    end
    
    subgraph "Data Layer"
        S[Vector Store] --> L
        T[SQLite/PostgreSQL] --> O
        U[File System] --> M
    end
    
    A --> K
    B --> F
    C --> F
    D --> F
    E --> F
    G --> L
    H --> O
    I --> O
    J --> F
```

## User Interaction Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit UI
    participant O as Orchestrator
    participant A as Agent
    participant R as RAG System
    participant M as MCP Tools
    participant C as Compliance
    
    U->>UI: Enter query/action
    UI->>O: Route to appropriate agent
    O->>A: Execute agent logic
    
    alt Educational Query
        A->>R: Search knowledge base
        R-->>A: Return relevant content
    else Portfolio Analysis
        A->>M: Get portfolio metrics
        M-->>A: Return calculations
    else Market Data
        A->>M: Fetch market data
        M-->>A: Return quotes/news
    end
    
    A-->>O: Generate response
    O->>C: Validate compliance
    C-->>O: Sanitized response
    O-->>UI: Final response
    UI-->>U: Display result with sources
```

## Multi-Agent Decision Flow

```mermaid
flowchart TD
    A[User Query] --> B{Query Analysis}
    
    B -->|Educational| C[Tutor Agent]
    B -->|Portfolio| D[Portfolio Analyst]
    B -->|Market| E[Market Intelligence]
    B -->|General| F[Default to Tutor]
    
    C --> G[Search RAG System]
    D --> H[Calculate Portfolio Metrics]
    E --> I[Fetch Market Data]
    F --> G
    
    G --> J[Generate Educational Response]
    H --> K[Generate Analysis Report]
    I --> L[Generate Market Brief]
    
    J --> M[Compliance Check]
    K --> M
    L --> M
    
    M --> N{Compliance Valid?}
    N -->|Yes| O[Return Response]
    N -->|No| P[Sanitize & Return]
    
    O --> Q[Display to User]
    P --> Q
```

## RAG System Flow

```mermaid
graph LR
    subgraph "Content Ingestion"
        A[Documents] --> B[Content Ingester]
        B --> C[Chunking]
        C --> D[Metadata Extraction]
        D --> E[Vector Embeddings]
    end
    
    subgraph "Storage"
        E --> F[Vector Store]
        D --> G[Metadata DB]
    end
    
    subgraph "Retrieval"
        H[User Query] --> I[BM25 Search]
        H --> J[Vector Search]
        I --> K[Hybrid Combiner]
        J --> K
        K --> L[Reranker]
        L --> M[Top Results]
    end
    
    subgraph "Generation"
        M --> N[Context Assembly]
        N --> O[Response Generation]
        O --> P[Source Attribution]
    end
    
    F --> J
    G --> I
    P --> Q[Final Response]
```

## Portfolio Analysis Flow

```mermaid
flowchart TD
    A[Portfolio Data Input] --> B{Data Source}
    
    B -->|CSV Upload| C[Parse Holdings]
    B -->|Manual Entry| D[Form Input]
    B -->|API Import| E[Broker Integration]
    
    C --> F[Data Validation]
    D --> F
    E --> F
    
    F --> G[Calculate Basic Metrics]
    G --> H[Risk Analysis]
    H --> I[Performance Metrics]
    I --> J[Diversification Analysis]
    
    J --> K[Generate Recommendations]
    K --> L[Create Visualizations]
    L --> M[Compliance Review]
    M --> N[Display Results]
```

## Market Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant M as Market Agent
    participant Y as yfinance
    participant A as Alpha Vantage
    participant N as News API
    participant C as Cache
    
    U->>M: Request market data
    M->>C: Check cache
    
    alt Cache Hit
        C-->>M: Return cached data
    else Cache Miss
        M->>Y: Fetch quotes
        Y-->>M: Market data
        M->>A: Fallback if needed
        A-->>M: Alternative data
        M->>N: Fetch news
        N-->>M: News articles
        M->>C: Store in cache
    end
    
    M->>M: Process & analyze
    M-->>U: Formatted response
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Request] --> B[Try Processing]
    B --> C{Success?}
    
    C -->|Yes| D[Return Result]
    C -->|No| E[Log Error]
    
    E --> F{Error Type}
    F -->|Network| G[Retry with Backoff]
    F -->|Validation| H[Return User Error]
    F -->|System| I[Fallback Response]
    F -->|Compliance| J[Sanitize & Return]
    
    G --> K{Retry Success?}
    K -->|Yes| D
    K -->|No| I
    
    H --> L[Display Error Message]
    I --> M[Generic Response]
    J --> N[Safe Response]
    
    L --> O[User Action]
    M --> O
    N --> O
```

## Development Workflow

```mermaid
graph LR
    subgraph "Development"
        A[Code Changes] --> B[Run Tests]
        B --> C{Tests Pass?}
        C -->|No| D[Fix Issues]
        D --> B
        C -->|Yes| E[Format Code]
        E --> F[Lint Check]
        F --> G[Type Check]
        G --> H[Build Docs]
    end
    
    subgraph "Deployment"
        H --> I[Package Build]
        I --> J[Deploy]
        J --> K[Monitor]
    end
    
    subgraph "Testing"
        L[Unit Tests] --> M[Integration Tests]
        M --> N[E2E Tests]
        N --> O[Load Tests]
    end
```

## Data Flow Summary

```mermaid
graph TB
    subgraph "Input Sources"
        A1[User Queries]
        A2[Portfolio Data]
        A3[Market APIs]
        A4[Educational Content]
    end
    
    subgraph "Processing Layer"
        B1[Query Router]
        B2[Agent System]
        B3[RAG Engine]
        B4[MCP Tools]
    end
    
    subgraph "Storage Layer"
        C1[Vector Database]
        C2[Relational DB]
        C3[File System]
        C4[Cache Layer]
    end
    
    subgraph "Output Layer"
        D1[Streamlit UI]
        D2[API Responses]
        D3[Documentation]
        D4[Reports]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B4
    A4 --> B3
    
    B1 --> B2
    B2 --> B3
    B2 --> B4
    
    B3 --> C1
    B4 --> C2
    B2 --> C3
    B4 --> C4
    
    C1 --> D1
    C2 --> D1
    C3 --> D3
    C4 --> D2
    
    D1 --> A1
```

## Key Components Summary

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Streamlit UI** | User Interface | Streamlit, Plotly |
| **Orchestrator** | Query Routing | LangGraph |
| **Agents** | Specialized Processing | Python Classes |
| **RAG System** | Knowledge Retrieval | FAISS, BM25 |
| **MCP Tools** | External Data | yfinance, APIs |
| **Compliance** | Safety & Validation | Custom Rules |
| **Storage** | Data Persistence | SQLite, Vector DB |

This comprehensive flow chart documentation shows how all components of the Finnie Financial AI Engine work together to provide a complete financial analysis and education platform.

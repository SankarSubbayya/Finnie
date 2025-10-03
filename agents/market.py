"""
Market Intelligence Agent - Provides real-time market data and analysis
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from .orchestrator import AgentState

logger = logging.getLogger(__name__)

class MarketIntelligenceAgent:
    """Agent that provides real-time market data, news, and analysis."""
    
    def __init__(self, market_data_service=None, news_service=None):
        self.market_data_service = market_data_service
        self.news_service = news_service
    
    def process(self, state: AgentState) -> Dict[str, Any]:
        """Process a market intelligence request."""
        query = state.query
        context = state.context
        
        # Extract symbols from query if mentioned
        symbols = self._extract_symbols(query)
        
        # Get market data
        market_data = self._get_market_data(symbols)
        
        # Get relevant news
        news_data = self._get_news_data(query, symbols)
        
        # Generate market analysis
        analysis = self._analyze_market_data(market_data, query)
        
        # Generate response
        response = self._generate_response(query, market_data, news_data, analysis)
        
        return {
            "response": response,
            "sources": self._get_market_sources(),
            "market_data": market_data,
            "news": news_data,
            "analysis": analysis
        }
    
    def _extract_symbols(self, query: str) -> List[str]:
        """Extract stock symbols from the query."""
        # Simple symbol extraction (in production, use NLP)
        common_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
            'SPY', 'QQQ', 'IWM', 'VTI', 'VEA', 'VWO', 'BND', 'GLD'
        ]
        
        symbols = []
        query_upper = query.upper()
        
        for symbol in common_symbols:
            if symbol in query_upper:
                symbols.append(symbol)
        
        return symbols
    
    def _get_market_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Get real-time market data for symbols."""
        if not symbols:
            # Return general market data
            return self._get_general_market_data()
        
        # In production, this would call the market data service
        market_data = {}
        
        for symbol in symbols:
            market_data[symbol] = self._get_mock_quote(symbol)
        
        return market_data
    
    def _get_mock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get mock quote data for a symbol."""
        import random
        import numpy as np
        
        # Mock price data
        base_price = random.uniform(50, 500)
        change = random.uniform(-5, 5)
        change_pct = (change / base_price) * 100
        
        return {
            "symbol": symbol,
            "price": round(base_price, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "volume": random.randint(1000000, 10000000),
            "high": round(base_price + random.uniform(0, 5), 2),
            "low": round(base_price - random.uniform(0, 5), 2),
            "open": round(base_price - change, 2),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_general_market_data(self) -> Dict[str, Any]:
        """Get general market data (indices)."""
        indices = {
            "SPY": {"name": "S&P 500", "price": 4750.23, "change": 0.52, "change_percent": 0.01},
            "QQQ": {"name": "NASDAQ", "price": 14850.67, "change": 0.78, "change_percent": 0.01},
            "IWM": {"name": "Russell 2000", "price": 1950.45, "change": -0.12, "change_percent": -0.01},
            "DIA": {"name": "Dow Jones", "price": 37500.12, "change": 0.34, "change_percent": 0.01}
        }
        
        return indices
    
    def _get_news_data(self, query: str, symbols: List[str]) -> List[Dict[str, Any]]:
        """Get relevant news data."""
        # In production, this would call the news service
        return self._get_mock_news(query, symbols)
    
    def _get_mock_news(self, query: str, symbols: List[str]) -> List[Dict[str, Any]]:
        """Get mock news data."""
        news_items = [
            {
                "title": "Tech Stocks Rally on Strong Earnings",
                "source": "Financial Times",
                "url": "https://ft.com/tech-rally",
                "timestamp": datetime.now() - timedelta(hours=2),
                "sentiment": "positive",
                "relevance": 0.95
            },
            {
                "title": "Federal Reserve Hints at Rate Cuts",
                "source": "Reuters",
                "url": "https://reuters.com/fed-rates",
                "timestamp": datetime.now() - timedelta(hours=4),
                "sentiment": "neutral",
                "relevance": 0.88
            },
            {
                "title": "Energy Sector Faces Headwinds",
                "source": "Bloomberg",
                "url": "https://bloomberg.com/energy",
                "timestamp": datetime.now() - timedelta(hours=6),
                "sentiment": "negative",
                "relevance": 0.82
            }
        ]
        
        # Filter news based on query and symbols
        relevant_news = []
        query_lower = query.lower()
        
        for news in news_items:
            relevance = news["relevance"]
            
            # Check if news is relevant to symbols
            if symbols:
                for symbol in symbols:
                    if symbol.lower() in news["title"].lower():
                        relevance += 0.1
            
            # Check if news is relevant to query
            if any(word in news["title"].lower() for word in query_lower.split()):
                relevance += 0.1
            
            if relevance > 0.8:
                relevant_news.append(news)
        
        return relevant_news[:5]  # Return top 5 relevant news items
    
    def _analyze_market_data(self, market_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Analyze market data and provide insights."""
        analysis = {
            "market_sentiment": "neutral",
            "key_insights": [],
            "trends": [],
            "risks": [],
            "opportunities": []
        }
        
        # Analyze individual stocks
        if len(market_data) == 1:
            symbol = list(market_data.keys())[0]
            quote = market_data[symbol]
            
            if quote["change_percent"] > 2:
                analysis["market_sentiment"] = "positive"
                analysis["key_insights"].append(f"{symbol} is up {quote['change_percent']:.1f}% today")
            elif quote["change_percent"] < -2:
                analysis["market_sentiment"] = "negative"
                analysis["key_insights"].append(f"{symbol} is down {quote['change_percent']:.1f}% today")
            else:
                analysis["key_insights"].append(f"{symbol} is relatively stable today")
        
        # Analyze market indices
        elif "SPY" in market_data or "QQQ" in market_data:
            positive_count = 0
            total_count = 0
            
            for symbol, quote in market_data.items():
                if isinstance(quote, dict) and "change_percent" in quote:
                    total_count += 1
                    if quote["change_percent"] > 0:
                        positive_count += 1
            
            if total_count > 0:
                positive_ratio = positive_count / total_count
                if positive_ratio > 0.7:
                    analysis["market_sentiment"] = "positive"
                    analysis["key_insights"].append("Most major indices are up today")
                elif positive_ratio < 0.3:
                    analysis["market_sentiment"] = "negative"
                    analysis["key_insights"].append("Most major indices are down today")
                else:
                    analysis["key_insights"].append("Market is mixed today")
        
        # Add general insights based on query
        if "volatility" in query.lower():
            analysis["key_insights"].append("Market volatility is within normal ranges")
        
        if "trend" in query.lower():
            analysis["trends"].append("Current trend appears to be sideways with slight upward bias")
        
        return analysis
    
    def _generate_response(self, query: str, market_data: Dict[str, Any], 
                         news_data: List[Dict[str, Any]], analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive market intelligence response."""
        response_parts = []
        
        # Start with market overview
        response_parts.append("## Market Intelligence Update")
        
        # Add key insights
        if analysis["key_insights"]:
            response_parts.append("\n**Key Insights:**")
            for insight in analysis["key_insights"]:
                response_parts.append(f"- {insight}")
        
        # Add specific stock data
        if len(market_data) == 1:
            symbol = list(market_data.keys())[0]
            quote = market_data[symbol]
            response_parts.append(f"\n**{symbol} Quote:**")
            response_parts.append(f"- Price: ${quote['price']:.2f}")
            response_parts.append(f"- Change: {quote['change']:+.2f} ({quote['change_percent']:+.2f}%)")
            response_parts.append(f"- Volume: {quote['volume']:,}")
        
        # Add market indices
        elif any(symbol in market_data for symbol in ["SPY", "QQQ", "IWM", "DIA"]):
            response_parts.append("\n**Market Indices:**")
            for symbol, data in market_data.items():
                if isinstance(data, dict) and "name" in data:
                    response_parts.append(f"- {data['name']}: {data['price']:.2f} ({data['change_percent']:+.2f}%)")
        
        # Add relevant news
        if news_data:
            response_parts.append("\n**Relevant News:**")
            for news in news_data[:3]:  # Show top 3 news items
                sentiment_emoji = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}.get(news["sentiment"], "⚪")
                response_parts.append(f"- {sentiment_emoji} {news['title']} ({news['source']})")
        
        # Add market sentiment
        sentiment = analysis["market_sentiment"]
        sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(sentiment, "❓")
        response_parts.append(f"\n**Market Sentiment:** {sentiment_emoji} {sentiment.title()}")
        
        return "\n".join(response_parts)
    
    def _get_market_sources(self) -> List[Dict[str, Any]]:
        """Get sources for market data."""
        return [
            {
                "title": "Real-time Market Data",
                "url": "https://finance.yahoo.com",
                "score": 0.95
            },
            {
                "title": "Market Analysis",
                "url": "https://finnie.learn/market-analysis",
                "score": 0.88
            }
        ]

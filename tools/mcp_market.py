"""
MCP Market Tools - Real-time market data integration
"""

from typing import Dict, Any, List, Optional
import yfinance as yf
import requests
import time
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for fetching real-time market data."""
    
    def __init__(self, alpha_vantage_key: Optional[str] = None):
        self.alpha_vantage_key = alpha_vantage_key
        self.cache = {}
        self.cache_ttl = 60  # 1 minute cache
        self.rate_limit_delay = 0.1  # 100ms between requests
    
    def get_quotes(self, symbols: List[str]) -> Dict[str, Any]:
        """Get real-time quotes for symbols."""
        try:
            # Check cache first
            cached_data = self._get_cached_data('quotes', symbols)
            if cached_data:
                return cached_data
            
            # Fetch data from yfinance
            quotes = {}
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period="1d")
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        quotes[symbol] = {
                            'symbol': symbol,
                            'price': round(latest['Close'], 2),
                            'change': round(latest['Close'] - latest['Open'], 2),
                            'change_percent': round(((latest['Close'] - latest['Open']) / latest['Open']) * 100, 2),
                            'volume': int(latest['Volume']),
                            'high': round(latest['High'], 2),
                            'low': round(latest['Low'], 2),
                            'open': round(latest['Open'], 2),
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        # Fallback to info data
                        quotes[symbol] = {
                            'symbol': symbol,
                            'price': info.get('currentPrice', 0),
                            'change': info.get('regularMarketChange', 0),
                            'change_percent': info.get('regularMarketChangePercent', 0),
                            'volume': info.get('volume', 0),
                            'high': info.get('dayHigh', 0),
                            'low': info.get('dayLow', 0),
                            'open': info.get('open', 0),
                            'timestamp': datetime.now().isoformat()
                        }
                    
                    # Rate limiting
                    time.sleep(self.rate_limit_delay)
                    
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {str(e)}")
                    quotes[symbol] = {
                        'symbol': symbol,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }
            
            # Cache the results
            self._cache_data('quotes', symbols, quotes)
            
            return quotes
            
        except Exception as e:
            logger.error(f"Error in get_quotes: {str(e)}")
            return {}
    
    def get_market_calendar(self) -> List[Dict[str, Any]]:
        """Get market calendar events."""
        try:
            # Check cache
            cached_data = self._get_cached_data('calendar', [])
            if cached_data:
                return cached_data
            
            # Mock calendar data (in production, use real API)
            calendar_events = [
                {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': '10:00 AM',
                    'event': 'Consumer Price Index',
                    'impact': 'High',
                    'forecast': '3.2%',
                    'description': 'Monthly inflation data release'
                },
                {
                    'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                    'time': '2:00 PM',
                    'event': 'Federal Reserve Meeting',
                    'impact': 'High',
                    'forecast': 'Rate Decision',
                    'description': 'FOMC interest rate decision'
                },
                {
                    'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'time': '8:30 AM',
                    'event': 'Non-Farm Payrolls',
                    'impact': 'High',
                    'forecast': '200K',
                    'description': 'Monthly employment data'
                }
            ]
            
            # Cache the results
            self._cache_data('calendar', [], calendar_events)
            
            return calendar_events
            
        except Exception as e:
            logger.error(f"Error in get_market_calendar: {str(e)}")
            return []
    
    def get_news(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get relevant news articles."""
        try:
            # Check cache
            cache_key = f"news_{query}_{limit}"
            cached_data = self._get_cached_data('news', [cache_key])
            if cached_data:
                return cached_data
            
            # Mock news data (in production, use real news API)
            news_articles = [
                {
                    'title': f'Market Update: {query}',
                    'source': 'Financial Times',
                    'url': f'https://ft.com/news/{query.replace(" ", "-")}',
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'sentiment': 'positive',
                    'relevance': 0.95,
                    'summary': f'Latest developments in {query} show positive trends...'
                },
                {
                    'title': f'Analysis: {query} Trends',
                    'source': 'Reuters',
                    'url': f'https://reuters.com/analysis/{query.replace(" ", "-")}',
                    'timestamp': datetime.now() - timedelta(hours=4),
                    'sentiment': 'neutral',
                    'relevance': 0.88,
                    'summary': f'Expert analysis of {query} market conditions...'
                },
                {
                    'title': f'Breaking: {query} News',
                    'source': 'Bloomberg',
                    'url': f'https://bloomberg.com/news/{query.replace(" ", "-")}',
                    'timestamp': datetime.now() - timedelta(hours=6),
                    'sentiment': 'negative',
                    'relevance': 0.82,
                    'summary': f'Breaking news about {query} developments...'
                }
            ]
            
            # Filter by relevance and limit
            filtered_news = [article for article in news_articles if article['relevance'] > 0.8]
            filtered_news = filtered_news[:limit]
            
            # Cache the results
            self._cache_data('news', [cache_key], filtered_news)
            
            return filtered_news
            
        except Exception as e:
            logger.error(f"Error in get_news: {str(e)}")
            return []
    
    def get_sector_performance(self) -> Dict[str, Any]:
        """Get sector performance data."""
        try:
            # Check cache
            cached_data = self._get_cached_data('sectors', [])
            if cached_data:
                return cached_data
            
            # Mock sector data (in production, use real API)
            sectors = {
                'Technology': {'return': 2.5, 'volume': 1000000},
                'Healthcare': {'return': 1.8, 'volume': 800000},
                'Finance': {'return': 0.9, 'volume': 1200000},
                'Consumer': {'return': 1.2, 'volume': 900000},
                'Energy': {'return': -0.5, 'volume': 600000},
                'Industrial': {'return': 0.7, 'volume': 700000},
                'Materials': {'return': 0.3, 'volume': 500000},
                'Utilities': {'return': 0.1, 'volume': 400000}
            }
            
            # Cache the results
            self._cache_data('sectors', [], sectors)
            
            return sectors
            
        except Exception as e:
            logger.error(f"Error in get_sector_performance: {str(e)}")
            return {}
    
    def _get_cached_data(self, data_type: str, key: List[str]) -> Optional[Any]:
        """Get data from cache if not expired."""
        cache_key = f"{data_type}_{hash(tuple(key))}"
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                del self.cache[cache_key]
        
        return None
    
    def _cache_data(self, data_type: str, key: List[str], data: Any):
        """Cache data with timestamp."""
        cache_key = f"{data_type}_{hash(tuple(key))}"
        self.cache[cache_key] = (data, time.time())

class NewsService:
    """Service for fetching financial news."""
    
    def __init__(self, news_api_key: Optional[str] = None):
        self.news_api_key = news_api_key
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes cache
    
    def search_news(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for news articles."""
        try:
            # Check cache
            cache_key = f"news_search_{query}_{limit}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Mock news search (in production, use real news API)
            news_articles = [
                {
                    'title': f'Breaking: {query} Market Update',
                    'source': 'Financial Times',
                    'url': f'https://ft.com/news/{query.replace(" ", "-")}',
                    'published_at': datetime.now() - timedelta(hours=1),
                    'sentiment': 'positive',
                    'relevance_score': 0.95,
                    'summary': f'Latest developments in {query} show strong performance...'
                },
                {
                    'title': f'Analysis: {query} Investment Outlook',
                    'source': 'Reuters',
                    'url': f'https://reuters.com/analysis/{query.replace(" ", "-")}',
                    'published_at': datetime.now() - timedelta(hours=3),
                    'sentiment': 'neutral',
                    'relevance_score': 0.88,
                    'summary': f'Expert analysis of {query} market conditions...'
                },
                {
                    'title': f'Market Watch: {query} Trends',
                    'source': 'Bloomberg',
                    'url': f'https://bloomberg.com/markets/{query.replace(" ", "-")}',
                    'published_at': datetime.now() - timedelta(hours=5),
                    'sentiment': 'negative',
                    'relevance_score': 0.82,
                    'summary': f'Market analysis of {query} shows mixed signals...'
                }
            ]
            
            # Filter by relevance and limit
            filtered_news = [article for article in news_articles if article['relevance_score'] > 0.8]
            filtered_news = filtered_news[:limit]
            
            # Cache the results
            self._cache_data(cache_key, filtered_news)
            
            return filtered_news
            
        except Exception as e:
            logger.error(f"Error in search_news: {str(e)}")
            return []
    
    def get_ticker_news(self, symbol: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get news for a specific ticker."""
        return self.search_news(symbol, limit)
    
    def _get_cached_data(self, key: str) -> Optional[Any]:
        """Get data from cache if not expired."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                del self.cache[key]
        
        return None
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp."""
        self.cache[key] = (data, time.time())

# MCP Tool Functions
def get_quotes(symbols: List[str]) -> Dict[str, Any]:
    """MCP tool function to get quotes."""
    service = MarketDataService()
    return service.get_quotes(symbols)

def get_market_calendar() -> List[Dict[str, Any]]:
    """MCP tool function to get market calendar."""
    service = MarketDataService()
    return service.get_market_calendar()

def search_news(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """MCP tool function to search news."""
    service = NewsService()
    return service.search_news(query, limit)

def get_sector_performance() -> Dict[str, Any]:
    """MCP tool function to get sector performance."""
    service = MarketDataService()
    return service.get_sector_performance()

"""
Portfolio Metrics Tools - Calculate portfolio performance metrics
"""

from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PortfolioMetricsCalculator:
    """Calculator for portfolio performance metrics."""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
    
    def calculate_metrics(self, holdings: List[Dict[str, Any]], 
                         market_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics."""
        try:
            if not holdings:
                return self._empty_metrics()
            
            # Convert holdings to DataFrame
            df_holdings = pd.DataFrame(holdings)
            
            # Basic portfolio info
            total_value = (df_holdings['quantity'] * df_holdings['cost_basis']).sum()
            num_holdings = len(df_holdings)
            
            # Calculate weights
            weights = (df_holdings['quantity'] * df_holdings['cost_basis']) / total_value
            
            # Mock returns (in production, use real market data)
            returns = self._generate_mock_returns(num_holdings)
            
            # Calculate metrics
            metrics = {
                'basic_info': self._calculate_basic_info(df_holdings, total_value, num_holdings),
                'risk_metrics': self._calculate_risk_metrics(returns),
                'performance_metrics': self._calculate_performance_metrics(returns),
                'diversification_metrics': self._calculate_diversification_metrics(weights, df_holdings),
                'allocation_metrics': self._calculate_allocation_metrics(df_holdings, weights)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {str(e)}")
            return self._empty_metrics()
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics structure."""
        return {
            'basic_info': {},
            'risk_metrics': {},
            'performance_metrics': {},
            'diversification_metrics': {},
            'allocation_metrics': {}
        }
    
    def _generate_mock_returns(self, num_holdings: int, days: int = 252) -> np.ndarray:
        """Generate mock returns for portfolio analysis."""
        # In production, this would use real market data
        np.random.seed(42)  # For reproducible results
        return np.random.normal(0.0008, 0.02, days)  # ~20% annual volatility, 20% annual return
    
    def _calculate_basic_info(self, df_holdings: pd.DataFrame, total_value: float, num_holdings: int) -> Dict[str, Any]:
        """Calculate basic portfolio information."""
        return {
            'total_value': total_value,
            'num_holdings': num_holdings,
            'avg_position_size': total_value / num_holdings if num_holdings > 0 else 0,
            'largest_position': df_holdings['quantity'].max() if not df_holdings.empty else 0,
            'smallest_position': df_holdings['quantity'].min() if not df_holdings.empty else 0,
            'total_quantity': df_holdings['quantity'].sum() if not df_holdings.empty else 0
        }
    
    def _calculate_risk_metrics(self, returns: np.ndarray) -> Dict[str, Any]:
        """Calculate risk-related metrics."""
        if len(returns) == 0:
            return {}
        
        # Volatility (annualized)
        volatility = np.std(returns) * np.sqrt(252)
        
        # Value at Risk (95% confidence)
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)
        
        # Expected Shortfall (Conditional VaR)
        es_95 = returns[returns <= var_95].mean()
        es_99 = returns[returns <= var_99].mean()
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        
        # Downside deviation
        downside_returns = returns[returns < 0]
        downside_deviation = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        return {
            'volatility': volatility,
            'var_95': var_95,
            'var_99': var_99,
            'expected_shortfall_95': es_95,
            'expected_shortfall_99': es_99,
            'max_drawdown': max_drawdown,
            'downside_deviation': downside_deviation
        }
    
    def _calculate_performance_metrics(self, returns: np.ndarray) -> Dict[str, Any]:
        """Calculate performance-related metrics."""
        if len(returns) == 0:
            return {}
        
        # Annualized return
        annual_return = np.mean(returns) * 252
        
        # Sharpe ratio
        excess_return = annual_return - self.risk_free_rate
        volatility = np.std(returns) * np.sqrt(252)
        sharpe_ratio = excess_return / volatility if volatility > 0 else 0
        
        # Sortino ratio
        downside_returns = returns[returns < 0]
        downside_deviation = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = excess_return / downside_deviation if downside_deviation > 0 else 0
        
        # Calmar ratio
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = abs(drawdown.min())
        calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
        
        # Information ratio (vs benchmark)
        benchmark_returns = np.random.normal(0.0005, 0.015, len(returns))  # Mock benchmark
        active_returns = returns - benchmark_returns
        tracking_error = np.std(active_returns) * np.sqrt(252)
        information_ratio = np.mean(active_returns) * 252 / tracking_error if tracking_error > 0 else 0
        
        return {
            'annual_return': annual_return,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'information_ratio': information_ratio,
            'excess_return': excess_return
        }
    
    def _calculate_diversification_metrics(self, weights: pd.Series, df_holdings: pd.DataFrame) -> Dict[str, Any]:
        """Calculate diversification metrics."""
        if len(weights) == 0:
            return {}
        
        # Herfindahl-Hirschman Index (HHI)
        hhi = (weights ** 2).sum()
        
        # Effective number of holdings
        effective_holdings = 1 / hhi if hhi > 0 else 0
        
        # Concentration ratio (top 5 holdings)
        top_5_weights = weights.nlargest(5).sum()
        
        # Gini coefficient (concentration measure)
        sorted_weights = np.sort(weights)
        n = len(sorted_weights)
        gini = (2 * np.sum((np.arange(1, n + 1) * sorted_weights))) / (n * np.sum(sorted_weights)) - (n + 1) / n
        
        return {
            'hhi': hhi,
            'effective_holdings': effective_holdings,
            'concentration_ratio_top5': top_5_weights,
            'gini_coefficient': gini,
            'diversification_ratio': 1 / hhi if hhi > 0 else 0
        }
    
    def _calculate_allocation_metrics(self, df_holdings: pd.DataFrame, weights: pd.Series) -> Dict[str, Any]:
        """Calculate allocation metrics."""
        if df_holdings.empty:
            return {}
        
        # Mock sector allocation (in production, use real sector data)
        sectors = ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy', 'Other']
        sector_weights = np.random.dirichlet(np.ones(len(sectors)))
        sector_allocation = dict(zip(sectors, sector_weights))
        
        # Mock asset class allocation
        asset_classes = ['Stocks', 'Bonds', 'Cash', 'Alternatives']
        asset_weights = np.random.dirichlet(np.ones(len(asset_classes)))
        asset_allocation = dict(zip(asset_classes, asset_weights))
        
        # Position size distribution
        position_sizes = weights.values
        size_metrics = {
            'mean_position_size': np.mean(position_sizes),
            'median_position_size': np.median(position_sizes),
            'std_position_size': np.std(position_sizes),
            'min_position_size': np.min(position_sizes),
            'max_position_size': np.max(position_sizes)
        }
        
        return {
            'sector_allocation': sector_allocation,
            'asset_allocation': asset_allocation,
            'position_size_metrics': size_metrics,
            'num_sectors': len(sectors),
            'num_asset_classes': len(asset_classes)
        }
    
    def calculate_correlation_matrix(self, holdings: List[Dict[str, Any]], 
                                   market_data: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """Calculate correlation matrix for holdings."""
        if not holdings or len(holdings) < 2:
            return np.array([])
        
        # Mock correlation matrix (in production, use real returns)
        n = len(holdings)
        correlation_matrix = np.random.uniform(-0.5, 0.8, (n, n))
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
        np.fill_diagonal(correlation_matrix, 1.0)  # Diagonal should be 1
        
        return correlation_matrix
    
    def calculate_beta(self, holdings: List[Dict[str, Any]], 
                      benchmark_symbol: str = 'SPY') -> Dict[str, float]:
        """Calculate beta for each holding against benchmark."""
        if not holdings:
            return {}
        
        betas = {}
        for holding in holdings:
            symbol = holding.get('symbol', '')
            # Mock beta calculation (in production, use real regression)
            beta = np.random.uniform(0.5, 1.5)
            betas[symbol] = beta
        
        return betas
    
    def calculate_tracking_error(self, holdings: List[Dict[str, Any]], 
                               benchmark_symbol: str = 'SPY') -> float:
        """Calculate tracking error against benchmark."""
        if not holdings:
            return 0.0
        
        # Mock tracking error (in production, use real calculation)
        return np.random.uniform(0.02, 0.08)  # 2-8% tracking error

# MCP Tool Functions
def calculate_portfolio_metrics(holdings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """MCP tool function to calculate portfolio metrics."""
    calculator = PortfolioMetricsCalculator()
    return calculator.calculate_metrics(holdings)

def calculate_correlation_matrix(holdings: List[Dict[str, Any]]) -> List[List[float]]:
    """MCP tool function to calculate correlation matrix."""
    calculator = PortfolioMetricsCalculator()
    matrix = calculator.calculate_correlation_matrix(holdings)
    return matrix.tolist() if matrix.size > 0 else []

def calculate_beta(holdings: List[Dict[str, Any]], benchmark: str = 'SPY') -> Dict[str, float]:
    """MCP tool function to calculate beta."""
    calculator = PortfolioMetricsCalculator()
    return calculator.calculate_beta(holdings, benchmark)

def calculate_tracking_error(holdings: List[Dict[str, Any]], benchmark: str = 'SPY') -> float:
    """MCP tool function to calculate tracking error."""
    calculator = PortfolioMetricsCalculator()
    return calculator.calculate_tracking_error(holdings, benchmark)

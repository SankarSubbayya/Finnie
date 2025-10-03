"""
Portfolio Analyst Agent - Analyzes portfolios and provides insights
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from .orchestrator import AgentState

logger = logging.getLogger(__name__)

class PortfolioAnalystAgent:
    """Agent that analyzes portfolios and provides investment insights."""
    
    def __init__(self, market_data_service=None):
        self.market_data_service = market_data_service
        self.risk_free_rate = 0.02  # 2% risk-free rate
    
    def process(self, state: AgentState) -> Dict[str, Any]:
        """Process a portfolio analysis request."""
        query = state.query
        portfolio_data = state.context.get("portfolio_data", {})
        holdings = portfolio_data.get("holdings", [])
        
        if not holdings:
            return {
                "response": "I'd be happy to analyze your portfolio! However, I don't see any holdings data. Please upload your portfolio data in the Portfolio tab or add holdings manually.",
                "sources": [],
                "recommendations": [],
                "metrics": {}
            }
        
        # Convert holdings to DataFrame
        df_holdings = pd.DataFrame(holdings)
        
        # Calculate portfolio metrics
        metrics = self._calculate_portfolio_metrics(df_holdings)
        
        # Generate analysis
        analysis = self._analyze_portfolio(df_holdings, metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(df_holdings, metrics, analysis)
        
        # Generate response
        response = self._generate_response(query, metrics, analysis, recommendations)
        
        return {
            "response": response,
            "sources": self._get_analysis_sources(),
            "recommendations": recommendations,
            "metrics": metrics,
            "analysis": analysis
        }
    
    def _calculate_portfolio_metrics(self, df_holdings: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics."""
        if df_holdings.empty:
            return {}
        
        # Basic calculations
        total_value = (df_holdings['quantity'] * df_holdings['cost_basis']).sum()
        num_holdings = len(df_holdings)
        
        # Mock performance data (in production, use real market data)
        returns = self._generate_mock_returns(num_holdings)
        
        # Risk metrics
        volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
        sharpe_ratio = (np.mean(returns) * 252 - self.risk_free_rate) / volatility if volatility > 0 else 0
        
        # Drawdown calculation
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        
        # VaR calculation (95% confidence)
        var_95 = np.percentile(returns, 5)
        
        # Diversification metrics
        hhi = self._calculate_hhi(df_holdings)
        diversification_ratio = 1 / hhi if hhi > 0 else 0
        
        return {
            "total_value": total_value,
            "num_holdings": num_holdings,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "var_95": var_95,
            "diversification_ratio": diversification_ratio,
            "returns": returns.tolist(),
            "cumulative_returns": cumulative_returns.tolist()
        }
    
    def _generate_mock_returns(self, num_holdings: int, days: int = 252) -> np.ndarray:
        """Generate mock returns for portfolio analysis."""
        # In production, this would use real market data
        np.random.seed(42)  # For reproducible results
        return np.random.normal(0.0008, 0.02, days)  # ~20% annual volatility, 20% annual return
    
    def _calculate_hhi(self, df_holdings: pd.DataFrame) -> float:
        """Calculate Herfindahl-Hirschman Index for diversification."""
        if df_holdings.empty:
            return 0
        
        # Calculate portfolio weights
        total_value = (df_holdings['quantity'] * df_holdings['cost_basis']).sum()
        weights = (df_holdings['quantity'] * df_holdings['cost_basis']) / total_value
        
        # Calculate HHI
        hhi = (weights ** 2).sum()
        return hhi
    
    def _analyze_portfolio(self, df_holdings: pd.DataFrame, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze portfolio characteristics and identify issues."""
        analysis = {
            "strengths": [],
            "concerns": [],
            "sector_allocation": {},
            "concentration_risk": {},
            "performance_analysis": {}
        }
        
        # Analyze concentration
        total_value = metrics.get("total_value", 0)
        if total_value > 0:
            weights = (df_holdings['quantity'] * df_holdings['cost_basis']) / total_value
            max_weight = weights.max()
            
            if max_weight > 0.3:
                analysis["concerns"].append(f"High concentration in {df_holdings.loc[weights.idxmax(), 'symbol']} ({max_weight:.1%})")
            else:
                analysis["strengths"].append("Good diversification across holdings")
        
        # Analyze number of holdings
        num_holdings = metrics.get("num_holdings", 0)
        if num_holdings < 5:
            analysis["concerns"].append("Portfolio has fewer than 5 holdings - consider diversification")
        elif num_holdings > 20:
            analysis["concerns"].append("Portfolio may be over-diversified - consider consolidation")
        else:
            analysis["strengths"].append("Appropriate number of holdings for diversification")
        
        # Analyze risk metrics
        sharpe_ratio = metrics.get("sharpe_ratio", 0)
        if sharpe_ratio > 1.0:
            analysis["strengths"].append("Strong risk-adjusted returns (Sharpe ratio > 1.0)")
        elif sharpe_ratio < 0.5:
            analysis["concerns"].append("Low risk-adjusted returns - consider rebalancing")
        
        volatility = metrics.get("volatility", 0)
        if volatility > 0.3:
            analysis["concerns"].append("High volatility - consider adding defensive positions")
        elif volatility < 0.1:
            analysis["concerns"].append("Very low volatility - may be missing growth opportunities")
        
        return analysis
    
    def _generate_recommendations(self, df_holdings: pd.DataFrame, metrics: Dict[str, Any], 
                                analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations for the portfolio."""
        recommendations = []
        
        # Diversification recommendations
        hhi = metrics.get("diversification_ratio", 0)
        if hhi < 0.5:
            recommendations.append({
                "type": "diversification",
                "priority": "high",
                "title": "Improve Diversification",
                "description": "Consider adding more holdings to improve diversification",
                "action": "Add 3-5 additional holdings across different sectors"
            })
        
        # Risk management recommendations
        max_drawdown = metrics.get("max_drawdown", 0)
        if abs(max_drawdown) > 0.2:
            recommendations.append({
                "type": "risk_management",
                "priority": "high",
                "title": "Reduce Drawdown Risk",
                "description": "Portfolio has experienced significant drawdowns",
                "action": "Consider adding defensive assets or reducing position sizes"
            })
        
        # Performance recommendations
        sharpe_ratio = metrics.get("sharpe_ratio", 0)
        if sharpe_ratio < 0.5:
            recommendations.append({
                "type": "performance",
                "priority": "medium",
                "title": "Improve Risk-Adjusted Returns",
                "description": "Portfolio's risk-adjusted returns could be improved",
                "action": "Review asset allocation and consider rebalancing"
            })
        
        # Rebalancing recommendations
        if len(df_holdings) > 1:
            recommendations.append({
                "type": "rebalancing",
                "priority": "medium",
                "title": "Regular Rebalancing",
                "description": "Consider rebalancing quarterly to maintain target allocation",
                "action": "Set up quarterly rebalancing schedule"
            })
        
        return recommendations
    
    def _generate_response(self, query: str, metrics: Dict[str, Any], analysis: Dict[str, Any], 
                         recommendations: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive portfolio analysis response."""
        response_parts = []
        
        # Start with overview
        total_value = metrics.get("total_value", 0)
        num_holdings = metrics.get("num_holdings", 0)
        
        response_parts.append(f"## Portfolio Analysis Summary")
        response_parts.append(f"Your portfolio has {num_holdings} holdings with a total value of ${total_value:,.2f}.")
        
        # Add key metrics
        sharpe_ratio = metrics.get("sharpe_ratio", 0)
        volatility = metrics.get("volatility", 0)
        max_drawdown = metrics.get("max_drawdown", 0)
        
        response_parts.append(f"\n**Key Metrics:**")
        response_parts.append(f"- Sharpe Ratio: {sharpe_ratio:.2f}")
        response_parts.append(f"- Volatility: {volatility:.1%}")
        response_parts.append(f"- Max Drawdown: {max_drawdown:.1%}")
        
        # Add strengths
        if analysis.get("strengths"):
            response_parts.append(f"\n**Strengths:**")
            for strength in analysis["strengths"]:
                response_parts.append(f"- {strength}")
        
        # Add concerns
        if analysis.get("concerns"):
            response_parts.append(f"\n**Areas for Improvement:**")
            for concern in analysis["concerns"]:
                response_parts.append(f"- {concern}")
        
        # Add top recommendations
        if recommendations:
            response_parts.append(f"\n**Top Recommendations:**")
            for i, rec in enumerate(recommendations[:3], 1):
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec["priority"], "⚪")
                response_parts.append(f"{i}. {priority_emoji} **{rec['title']}**: {rec['description']}")
        
        return "\n".join(response_parts)
    
    def _get_analysis_sources(self) -> List[Dict[str, Any]]:
        """Get sources for portfolio analysis."""
        return [
            {
                "title": "Portfolio Analysis Methodology",
                "url": "https://finnie.learn/portfolio-analysis",
                "score": 0.95
            },
            {
                "title": "Risk Metrics Guide",
                "url": "https://finnie.learn/risk-metrics",
                "score": 0.88
            }
        ]

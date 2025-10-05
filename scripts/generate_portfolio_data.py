#!/usr/bin/env python3
"""
Portfolio Data Generator for Finnie
Generates sample portfolio CSV files for testing and demonstration

Developed by Sankar Subbayya
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_portfolio():
    """Generate a comprehensive sample portfolio with realistic data"""
    
    # Define portfolio holdings
    holdings = [
        # Technology Stocks
        {"symbol": "AAPL", "quantity": 100, "purchase_price": 150.25, "sector": "Technology", "asset_type": "Stock"},
        {"symbol": "MSFT", "quantity": 50, "purchase_price": 280.75, "sector": "Technology", "asset_type": "Stock"},
        {"symbol": "GOOGL", "quantity": 25, "purchase_price": 95.30, "sector": "Technology", "asset_type": "Stock"},
        {"symbol": "NVDA", "quantity": 40, "purchase_price": 220.60, "sector": "Technology", "asset_type": "Stock"},
        {"symbol": "META", "quantity": 35, "purchase_price": 195.25, "sector": "Technology", "asset_type": "Stock"},
        
        # Consumer Discretionary
        {"symbol": "TSLA", "quantity": 30, "purchase_price": 180.45, "sector": "Automotive", "asset_type": "Stock"},
        {"symbol": "AMZN", "quantity": 20, "purchase_price": 105.80, "sector": "Consumer Discretionary", "asset_type": "Stock"},
        {"symbol": "HD", "quantity": 20, "purchase_price": 295.50, "sector": "Consumer Discretionary", "asset_type": "Stock"},
        
        # Financial Services
        {"symbol": "BRK.B", "quantity": 10, "purchase_price": 315.75, "sector": "Financial Services", "asset_type": "Stock"},
        {"symbol": "JPM", "quantity": 45, "purchase_price": 135.20, "sector": "Financial Services", "asset_type": "Stock"},
        {"symbol": "V", "quantity": 30, "purchase_price": 220.40, "sector": "Financial Services", "asset_type": "Stock"},
        
        # Healthcare
        {"symbol": "JNJ", "quantity": 20, "purchase_price": 165.80, "sector": "Healthcare", "asset_type": "Stock"},
        {"symbol": "UNH", "quantity": 15, "purchase_price": 485.25, "sector": "Healthcare", "asset_type": "Stock"},
        
        # Consumer Staples
        {"symbol": "PG", "quantity": 25, "purchase_price": 145.30, "sector": "Consumer Staples", "asset_type": "Stock"},
        
        # Communication Services
        {"symbol": "NFLX", "quantity": 15, "purchase_price": 315.50, "sector": "Communication Services", "asset_type": "Stock"},
        
        # ETFs
        {"symbol": "VTI", "quantity": 200, "purchase_price": 215.30, "sector": "Market Index", "asset_type": "ETF"},
        {"symbol": "VEA", "quantity": 150, "purchase_price": 45.75, "sector": "International", "asset_type": "ETF"},
        {"symbol": "VWO", "quantity": 100, "purchase_price": 38.25, "sector": "Emerging Markets", "asset_type": "ETF"},
        {"symbol": "BND", "quantity": 300, "purchase_price": 75.40, "sector": "Bonds", "asset_type": "Bond ETF"},
        {"symbol": "TLT", "quantity": 50, "purchase_price": 95.80, "sector": "Treasury Bonds", "asset_type": "Bond ETF"},
        
        # Commodities
        {"symbol": "GLD", "quantity": 25, "purchase_price": 185.60, "sector": "Commodities", "asset_type": "Commodity ETF"},
        {"symbol": "SLV", "quantity": 100, "purchase_price": 22.30, "sector": "Commodities", "asset_type": "Commodity ETF"},
        
        # Cryptocurrencies
        {"symbol": "BTC", "quantity": 0.5, "purchase_price": 45000.00, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "ETH", "quantity": 2.0, "purchase_price": 2800.00, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "ADA", "quantity": 1000, "purchase_price": 0.45, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "DOT", "quantity": 50, "purchase_price": 6.80, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "MATIC", "quantity": 500, "purchase_price": 0.85, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "AVAX", "quantity": 25, "purchase_price": 18.50, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "SOL", "quantity": 15, "purchase_price": 95.20, "sector": "Cryptocurrency", "asset_type": "Crypto"},
        {"symbol": "LINK", "quantity": 100, "purchase_price": 7.25, "sector": "Cryptocurrency", "asset_type": "Crypto"},
    ]
    
    # Generate random purchase dates within the last year
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    portfolio_data = []
    
    for holding in holdings:
        # Generate random purchase date
        days_diff = (end_date - start_date).days
        random_days = random.randint(0, days_diff)
        purchase_date = start_date + timedelta(days=random_days)
        
        # Generate current price with some realistic variation
        price_variation = np.random.normal(1.0, 0.2)  # 20% standard deviation
        current_price = max(0.01, holding["purchase_price"] * price_variation)
        
        # Calculate metrics
        market_value = holding["quantity"] * current_price
        cost_basis = holding["quantity"] * holding["purchase_price"]
        gain_loss = market_value - cost_basis
        gain_loss_pct = (gain_loss / cost_basis) * 100 if cost_basis > 0 else 0
        
        # Generate risk metrics based on asset type
        if holding["asset_type"] == "Stock":
            beta = np.random.uniform(0.8, 1.5)
            volatility = np.random.uniform(0.15, 0.35)
            sharpe_ratio = np.random.uniform(0.8, 1.4)
            max_drawdown = -np.random.uniform(0.05, 0.25)
        elif holding["asset_type"] == "ETF":
            beta = np.random.uniform(0.7, 1.2)
            volatility = np.random.uniform(0.10, 0.25)
            sharpe_ratio = np.random.uniform(1.0, 1.5)
            max_drawdown = -np.random.uniform(0.03, 0.15)
        elif holding["asset_type"] == "Bond ETF":
            beta = np.random.uniform(0.1, 0.3)
            volatility = np.random.uniform(0.02, 0.08)
            sharpe_ratio = np.random.uniform(1.5, 2.5)
            max_drawdown = -np.random.uniform(0.01, 0.05)
        elif holding["asset_type"] == "Commodity ETF":
            beta = np.random.uniform(0.2, 0.5)
            volatility = np.random.uniform(0.08, 0.20)
            sharpe_ratio = np.random.uniform(0.5, 1.2)
            max_drawdown = -np.random.uniform(0.03, 0.12)
        elif holding["asset_type"] == "Crypto":
            beta = np.random.uniform(1.5, 2.5)
            volatility = np.random.uniform(0.40, 0.70)
            sharpe_ratio = np.random.uniform(0.3, 0.8)
            max_drawdown = -np.random.uniform(0.20, 0.50)
        else:
            beta = 1.0
            volatility = 0.20
            sharpe_ratio = 1.0
            max_drawdown = -0.10
        
        portfolio_data.append({
            "symbol": holding["symbol"],
            "quantity": holding["quantity"],
            "purchase_price": holding["purchase_price"],
            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
            "sector": holding["sector"],
            "asset_type": holding["asset_type"],
            "current_price": round(current_price, 2),
            "market_value": round(market_value, 2),
            "cost_basis": round(cost_basis, 2),
            "gain_loss": round(gain_loss, 2),
            "gain_loss_pct": round(gain_loss_pct, 2),
            "beta": round(beta, 2),
            "volatility_1y": round(volatility, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2)
        })
    
    return pd.DataFrame(portfolio_data)

def generate_portfolio_summary(df):
    """Generate portfolio summary statistics"""
    
    total_market_value = df["market_value"].sum()
    total_cost_basis = df["cost_basis"].sum()
    total_gain_loss = df["gain_loss"].sum()
    total_gain_loss_pct = (total_gain_loss / total_cost_basis) * 100 if total_cost_basis > 0 else 0
    
    # Calculate weights
    df["weight_pct"] = (df["market_value"] / total_market_value) * 100
    
    # Sector allocation
    sector_allocation = df.groupby("sector")["market_value"].sum().sort_values(ascending=False)
    sector_allocation_pct = (sector_allocation / total_market_value) * 100
    
    # Asset type allocation
    asset_allocation = df.groupby("asset_type")["market_value"].sum().sort_values(ascending=False)
    asset_allocation_pct = (asset_allocation / total_market_value) * 100
    
    summary = {
        "total_market_value": total_market_value,
        "total_cost_basis": total_cost_basis,
        "total_gain_loss": total_gain_loss,
        "total_gain_loss_pct": total_gain_loss_pct,
        "num_holdings": len(df),
        "sector_allocation": sector_allocation_pct.to_dict(),
        "asset_allocation": asset_allocation_pct.to_dict()
    }
    
    return summary

def main():
    """Main function to generate portfolio data"""
    
    print("🚀 Finnie Portfolio Data Generator")
    print("Developed by Sankar Subbayya")
    print("=" * 50)
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate sample portfolio
    print("📊 Generating sample portfolio...")
    portfolio_df = generate_sample_portfolio()
    
    # Save basic portfolio CSV
    portfolio_df[["symbol", "quantity", "purchase_price", "purchase_date", "sector", "asset_type"]].to_csv(
        "data/sample_portfolio.csv", index=False
    )
    print("✅ Created data/sample_portfolio.csv")
    
    # Save detailed portfolio CSV
    portfolio_df.to_csv("data/portfolio_analysis.csv", index=False)
    print("✅ Created data/portfolio_analysis.csv")
    
    # Generate portfolio summary
    summary = generate_portfolio_summary(portfolio_df)
    
    # Save summary to file
    with open("data/portfolio_summary.txt", "w") as f:
        f.write("FINNIE PORTFOLIO SUMMARY\n")
        f.write("Developed by Sankar Subbayya\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total Market Value: ${summary['total_market_value']:,.2f}\n")
        f.write(f"Total Cost Basis: ${summary['total_cost_basis']:,.2f}\n")
        f.write(f"Total Gain/Loss: ${summary['total_gain_loss']:,.2f}\n")
        f.write(f"Total Gain/Loss %: {summary['total_gain_loss_pct']:.2f}%\n")
        f.write(f"Number of Holdings: {summary['num_holdings']}\n\n")
        
        f.write("SECTOR ALLOCATION:\n")
        for sector, pct in summary['sector_allocation'].items():
            f.write(f"  {sector}: {pct:.2f}%\n")
        
        f.write("\nASSET TYPE ALLOCATION:\n")
        for asset_type, pct in summary['asset_allocation'].items():
            f.write(f"  {asset_type}: {pct:.2f}%\n")
    
    print("✅ Created data/portfolio_summary.txt")
    
    # Display summary
    print("\n📈 PORTFOLIO SUMMARY:")
    print(f"Total Market Value: ${summary['total_market_value']:,.2f}")
    print(f"Total Cost Basis: ${summary['total_cost_basis']:,.2f}")
    print(f"Total Gain/Loss: ${summary['total_gain_loss']:,.2f}")
    print(f"Total Gain/Loss %: {summary['total_gain_loss_pct']:.2f}%")
    print(f"Number of Holdings: {summary['num_holdings']}")
    
    print("\n🎯 TOP SECTORS:")
    for sector, pct in list(summary['sector_allocation'].items())[:5]:
        print(f"  {sector}: {pct:.2f}%")
    
    print("\n🎯 ASSET TYPES:")
    for asset_type, pct in summary['asset_allocation'].items():
        print(f"  {asset_type}: {pct:.2f}%")
    
    print("\n✅ Portfolio data generation completed!")
    print("📁 Files created in data/ directory:")
    print("  - sample_portfolio.csv (basic format)")
    print("  - portfolio_analysis.csv (detailed with metrics)")
    print("  - portfolio_summary.txt (summary statistics)")

if __name__ == "__main__":
    main()

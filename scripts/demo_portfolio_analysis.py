#!/usr/bin/env python3
"""
Portfolio Analysis Demo for Finnie
Demonstrates how to analyze portfolio CSV data

Developed by Sankar Subbayya
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_portfolio_data(csv_file="data/portfolio_analysis.csv"):
    """Load portfolio data from CSV file"""
    
    if not os.path.exists(csv_file):
        print(f"❌ File {csv_file} not found!")
        return None
    
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded portfolio data from {csv_file}")
    print(f"📊 Found {len(df)} holdings")
    
    return df

def analyze_portfolio_performance(df):
    """Analyze portfolio performance metrics"""
    
    print("\n📈 PORTFOLIO PERFORMANCE ANALYSIS")
    print("=" * 50)
    
    # Basic metrics
    total_market_value = df["market_value"].sum()
    total_cost_basis = df["cost_basis"].sum()
    total_gain_loss = df["gain_loss"].sum()
    total_gain_loss_pct = (total_gain_loss / total_cost_basis) * 100
    
    print(f"💰 Total Market Value: ${total_market_value:,.2f}")
    print(f"💸 Total Cost Basis: ${total_cost_basis:,.2f}")
    print(f"📊 Total Gain/Loss: ${total_gain_loss:,.2f}")
    print(f"📈 Total Return: {total_gain_loss_pct:.2f}%")
    
    # Best and worst performers
    best_performer = df.loc[df["gain_loss_pct"].idxmax()]
    worst_performer = df.loc[df["gain_loss_pct"].idxmin()]
    
    print(f"\n🏆 Best Performer: {best_performer['symbol']} ({best_performer['gain_loss_pct']:.2f}%)")
    print(f"📉 Worst Performer: {worst_performer['symbol']} ({worst_performer['gain_loss_pct']:.2f}%)")
    
    return {
        "total_market_value": total_market_value,
        "total_cost_basis": total_cost_basis,
        "total_gain_loss": total_gain_loss,
        "total_gain_loss_pct": total_gain_loss_pct,
        "best_performer": best_performer,
        "worst_performer": worst_performer
    }

def analyze_sector_allocation(df):
    """Analyze sector allocation"""
    
    print("\n🏢 SECTOR ALLOCATION ANALYSIS")
    print("=" * 50)
    
    sector_analysis = df.groupby("sector").agg({
        "market_value": "sum",
        "gain_loss": "sum",
        "gain_loss_pct": "mean"
    }).round(2)
    
    total_value = df["market_value"].sum()
    sector_analysis["weight_pct"] = (sector_analysis["market_value"] / total_value * 100).round(2)
    
    # Sort by market value
    sector_analysis = sector_analysis.sort_values("market_value", ascending=False)
    
    print("Sector Distribution:")
    for sector, data in sector_analysis.iterrows():
        print(f"  {sector:20} {data['weight_pct']:6.2f}% ${data['market_value']:10,.2f}")
    
    return sector_analysis

def analyze_asset_type_allocation(df):
    """Analyze asset type allocation"""
    
    print("\n🎯 ASSET TYPE ALLOCATION ANALYSIS")
    print("=" * 50)
    
    asset_analysis = df.groupby("asset_type").agg({
        "market_value": "sum",
        "gain_loss": "sum",
        "gain_loss_pct": "mean"
    }).round(2)
    
    total_value = df["market_value"].sum()
    asset_analysis["weight_pct"] = (asset_analysis["market_value"] / total_value * 100).round(2)
    
    # Sort by market value
    asset_analysis = asset_analysis.sort_values("market_value", ascending=False)
    
    print("Asset Type Distribution:")
    for asset_type, data in asset_analysis.iterrows():
        print(f"  {asset_type:15} {data['weight_pct']:6.2f}% ${data['market_value']:10,.2f}")
    
    return asset_analysis

def analyze_risk_metrics(df):
    """Analyze risk metrics"""
    
    print("\n⚠️ RISK ANALYSIS")
    print("=" * 50)
    
    # Calculate portfolio-level risk metrics
    total_value = df["market_value"].sum()
    
    # Weighted average metrics
    weighted_beta = (df["beta"] * df["market_value"]).sum() / total_value
    weighted_volatility = (df["volatility_1y"] * df["market_value"]).sum() / total_value
    weighted_sharpe = (df["sharpe_ratio"] * df["market_value"]).sum() / total_value
    weighted_max_drawdown = (df["max_drawdown"] * df["market_value"]).sum() / total_value
    
    print(f"📊 Weighted Average Beta: {weighted_beta:.2f}")
    print(f"📈 Weighted Average Volatility: {weighted_volatility:.2f}")
    print(f"⚖️ Weighted Average Sharpe Ratio: {weighted_sharpe:.2f}")
    print(f"📉 Weighted Average Max Drawdown: {weighted_max_drawdown:.2f}")
    
    # Risk concentration
    top_5_holdings = df.nlargest(5, "market_value")
    top_5_concentration = (top_5_holdings["market_value"].sum() / total_value) * 100
    
    print(f"\n🎯 Top 5 Holdings Concentration: {top_5_concentration:.2f}%")
    print("Top 5 Holdings:")
    for _, holding in top_5_holdings.iterrows():
        weight = (holding["market_value"] / total_value) * 100
        print(f"  {holding['symbol']:8} {weight:6.2f}% ${holding['market_value']:10,.2f}")
    
    return {
        "weighted_beta": weighted_beta,
        "weighted_volatility": weighted_volatility,
        "weighted_sharpe": weighted_sharpe,
        "weighted_max_drawdown": weighted_max_drawdown,
        "top_5_concentration": top_5_concentration
    }

def generate_recommendations(df, performance_metrics, sector_analysis, asset_analysis, risk_metrics):
    """Generate portfolio recommendations"""
    
    print("\n💡 PORTFOLIO RECOMMENDATIONS")
    print("=" * 50)
    
    recommendations = []
    
    # Diversification recommendations
    if risk_metrics["top_5_concentration"] > 50:
        recommendations.append("⚠️ High concentration in top 5 holdings - consider diversifying")
    
    # Sector concentration
    max_sector_weight = sector_analysis["weight_pct"].max()
    if max_sector_weight > 30:
        recommendations.append(f"⚠️ High concentration in {sector_analysis['weight_pct'].idxmax()} sector ({max_sector_weight:.1f}%)")
    
    # Asset type diversification
    stock_weight = asset_analysis.loc["Stock", "weight_pct"] if "Stock" in asset_analysis.index else 0
    if stock_weight > 70:
        recommendations.append("💡 Consider adding more bonds and alternative investments")
    
    # Performance recommendations
    if performance_metrics["total_gain_loss_pct"] < 5:
        recommendations.append("📈 Portfolio underperforming - review individual holdings")
    
    # Risk recommendations
    if risk_metrics["weighted_beta"] > 1.2:
        recommendations.append("⚠️ High beta portfolio - consider adding defensive assets")
    
    if risk_metrics["weighted_volatility"] > 0.25:
        recommendations.append("📉 High volatility - consider reducing risk")
    
    # Print recommendations
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("✅ Portfolio appears well-balanced!")
    
    return recommendations

def main():
    """Main demo function"""
    
    print("🚀 Finnie Portfolio Analysis Demo")
    print("Developed by Sankar Subbayya")
    print("=" * 50)
    
    # Load portfolio data
    df = load_portfolio_data()
    if df is None:
        return
    
    # Run analyses
    performance_metrics = analyze_portfolio_performance(df)
    sector_analysis = analyze_sector_allocation(df)
    asset_analysis = analyze_asset_type_allocation(df)
    risk_metrics = analyze_risk_metrics(df)
    
    # Generate recommendations
    recommendations = generate_recommendations(df, performance_metrics, sector_analysis, asset_analysis, risk_metrics)
    
    print("\n🎉 Analysis Complete!")
    print("📊 This demonstrates the portfolio analysis capabilities of Finnie")
    print("💡 Upload your own CSV file to the Portfolio tab for personalized analysis")

if __name__ == "__main__":
    main()

"""
Portfolio Page - Portfolio analysis and management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render():
    """Render the Portfolio page."""
    st.title("📊 Portfolio Analysis")
    st.caption("Upload your holdings and get comprehensive portfolio insights")
    
    # Portfolio upload section
    st.subheader("📁 Upload Holdings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV file with your holdings",
            type=['csv'],
            help="CSV should have columns: symbol, quantity, cost_basis, date"
        )
    
    with col2:
        st.markdown("### Sample Format")
        sample_data = pd.DataFrame({
            'symbol': ['AAPL', 'MSFT', 'GOOGL'],
            'quantity': [10, 5, 3],
            'cost_basis': [150.00, 300.00, 2500.00],
            'date': ['2024-01-15', '2024-02-01', '2024-01-20']
        })
        st.dataframe(sample_data, use_container_width=True)
    
    # Process uploaded data
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.portfolio_data["holdings"] = df.to_dict('records')
            st.session_state.portfolio_data["last_updated"] = datetime.now().isoformat()
            st.success("Portfolio data uploaded successfully!")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Manual entry option
    with st.expander("✏️ Manual Entry"):
        st.markdown("Add holdings manually:")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            symbol = st.text_input("Symbol", placeholder="AAPL")
        with col2:
            quantity = st.number_input("Quantity", min_value=0.0, value=0.0)
        with col3:
            cost_basis = st.number_input("Cost Basis", min_value=0.0, value=0.0)
        with col4:
            date = st.date_input("Date", value=datetime.now().date())
        
        if st.button("Add Holding"):
            if symbol and quantity > 0 and cost_basis > 0:
                new_holding = {
                    'symbol': symbol.upper(),
                    'quantity': quantity,
                    'cost_basis': cost_basis,
                    'date': date.isoformat()
                }
                st.session_state.portfolio_data["holdings"].append(new_holding)
                st.success(f"Added {quantity} shares of {symbol}")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    # Portfolio analysis
    if st.session_state.portfolio_data["holdings"]:
        st.subheader("📈 Portfolio Analysis")
        
        # Convert to DataFrame for analysis
        holdings_df = pd.DataFrame(st.session_state.portfolio_data["holdings"])
        
        # Basic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value = (holdings_df['quantity'] * holdings_df['cost_basis']).sum()
            st.metric("Total Value", f"${total_value:,.2f}")
        
        with col2:
            num_holdings = len(holdings_df)
            st.metric("Number of Holdings", num_holdings)
        
        with col3:
            avg_position_size = total_value / num_holdings if num_holdings > 0 else 0
            st.metric("Avg Position Size", f"${avg_position_size:,.2f}")
        
        with col4:
            # Mock diversification score (would be calculated from real data)
            diversification_score = min(100, num_holdings * 20)
            st.metric("Diversification Score", f"{diversification_score}%")
        
        # Holdings table
        st.subheader("📋 Current Holdings")
        st.dataframe(holdings_df, use_container_width=True)
        
        # Portfolio allocation (mock data)
        st.subheader("🥧 Portfolio Allocation")
        
        # Mock allocation data
        allocation_data = {
            'Sector': ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Other'],
            'Percentage': [40, 25, 20, 10, 5]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=allocation_data['Percentage'],
                names=allocation_data['Sector'],
                title="Sector Allocation"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(
                x=allocation_data['Sector'],
                y=allocation_data['Percentage'],
                title="Sector Allocation (Bar Chart)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Performance metrics (mock data)
        st.subheader("📊 Performance Metrics")
        
        # Mock performance data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        returns = np.random.normal(0.001, 0.02, len(dates)).cumsum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Equity curve
            fig_equity = go.Figure()
            fig_equity.add_trace(go.Scatter(
                x=dates,
                y=returns,
                mode='lines',
                name='Portfolio Value',
                line=dict(color='blue')
            ))
            fig_equity.update_layout(
                title="Portfolio Equity Curve",
                xaxis_title="Date",
                yaxis_title="Cumulative Return"
            )
            st.plotly_chart(fig_equity, use_container_width=True)
        
        with col2:
            # Drawdown chart
            peak = returns.expanding().max()
            drawdown = (returns - peak) / peak * 100
            
            fig_drawdown = go.Figure()
            fig_drawdown.add_trace(go.Scatter(
                x=dates,
                y=drawdown,
                mode='lines',
                name='Drawdown %',
                fill='tonexty',
                line=dict(color='red')
            ))
            fig_drawdown.update_layout(
                title="Portfolio Drawdown",
                xaxis_title="Date",
                yaxis_title="Drawdown %"
            )
            st.plotly_chart(fig_drawdown, use_container_width=True)
        
        # Risk metrics
        st.subheader("⚠️ Risk Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            volatility = np.std(returns) * np.sqrt(252) * 100
            st.metric("Volatility (Annualized)", f"{volatility:.2f}%")
        
        with col2:
            sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        
        with col3:
            max_drawdown = drawdown.min()
            st.metric("Max Drawdown", f"{max_drawdown:.2f}%")
        
        with col4:
            var_95 = np.percentile(returns, 5)
            st.metric("VaR (95%)", f"{var_95:.2f}%")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        recommendations = [
            "Consider rebalancing your portfolio to maintain target allocation",
            "Your technology sector exposure is high - consider diversifying",
            "Monitor your risk metrics regularly",
            "Consider adding international exposure for diversification"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    else:
        st.info("👆 Upload your portfolio data or add holdings manually to see analysis")

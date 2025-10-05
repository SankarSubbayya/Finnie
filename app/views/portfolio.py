"""
Portfolio Page - Portfolio analysis and management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def normalize_portfolio_columns(df):
    """Normalize column names to handle different CSV formats"""
    
    # Create a copy to avoid modifying the original
    df_normalized = df.copy()
    
    # Column mapping for different formats
    column_mapping = {
        # Symbol variations
        'symbol': ['symbol', 'ticker', 'stock', 'asset'],
        'quantity': ['quantity', 'qty', 'shares', 'units', 'amount'],
        'purchase_price': ['purchase_price', 'cost', 'price', 'cost_per_share', 'purchase_cost'],
        'cost_basis': ['cost_basis', 'total_cost', 'investment', 'total_investment'],
        'purchase_date': ['purchase_date', 'date', 'buy_date', 'acquisition_date'],
        'current_price': ['current_price', 'market_price', 'price_now', 'current_value'],
        'market_value': ['market_value', 'current_value', 'total_value'],
        'sector': ['sector', 'industry', 'category'],
        'asset_type': ['asset_type', 'type', 'instrument_type']
    }
    
    # Normalize column names
    for standard_name, variations in column_mapping.items():
        for col in df_normalized.columns:
            if col.lower() in [v.lower() for v in variations]:
                df_normalized = df_normalized.rename(columns={col: standard_name})
                break
    
    # Calculate missing columns if possible
    if 'cost_basis' not in df_normalized.columns and 'quantity' in df_normalized.columns and 'purchase_price' in df_normalized.columns:
        df_normalized['cost_basis'] = df_normalized['quantity'] * df_normalized['purchase_price']
    
    if 'market_value' not in df_normalized.columns and 'quantity' in df_normalized.columns and 'current_price' in df_normalized.columns:
        df_normalized['market_value'] = df_normalized['quantity'] * df_normalized['current_price']
    
    # Calculate gain/loss if we have the required columns
    if 'market_value' in df_normalized.columns and 'cost_basis' in df_normalized.columns:
        df_normalized['gain_loss'] = df_normalized['market_value'] - df_normalized['cost_basis']
        df_normalized['gain_loss_pct'] = (df_normalized['gain_loss'] / df_normalized['cost_basis'] * 100).round(2)
    
    return df_normalized

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
        st.dataframe(sample_data, width='stretch')
    
    # Process uploaded data
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Normalize column names to handle different CSV formats
            df = normalize_portfolio_columns(df)
            
            st.session_state.portfolio_data["holdings"] = df.to_dict('records')
            st.session_state.portfolio_data["last_updated"] = datetime.now().isoformat()
            st.success("Portfolio data uploaded successfully!")
            
            # Show column mapping info
            st.info(f"📊 Loaded {len(df)} holdings with columns: {', '.join(df.columns)}")
            
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
            # Calculate total value based on available columns
            if 'market_value' in holdings_df.columns:
                total_value = holdings_df['market_value'].sum()
                st.metric("Total Market Value", f"${total_value:,.2f}")
            elif 'cost_basis' in holdings_df.columns:
                total_value = holdings_df['cost_basis'].sum()
                st.metric("Total Cost Basis", f"${total_value:,.2f}")
            else:
                total_value = 0
                st.metric("Total Value", "N/A")
        
        with col2:
            num_holdings = len(holdings_df)
            st.metric("Number of Holdings", num_holdings)
        
        with col3:
            avg_position_size = total_value / num_holdings if num_holdings > 0 else 0
            st.metric("Avg Position Size", f"${avg_position_size:,.2f}")
        
        with col4:
            # Calculate diversification score based on sectors if available
            if 'sector' in holdings_df.columns:
                num_sectors = holdings_df['sector'].nunique()
                diversification_score = min(100, num_sectors * 15 + num_holdings * 5)
            else:
                diversification_score = min(100, num_holdings * 20)
            st.metric("Diversification Score", f"{diversification_score}%")
        
        # Holdings table
        st.subheader("📋 Current Holdings")
        st.dataframe(holdings_df, width='stretch')
        
        # Portfolio allocation
        st.subheader("🥧 Portfolio Allocation")
        
        col1, col2 = st.columns(2)
        
        # Sector allocation if sector data is available
        if 'sector' in holdings_df.columns and total_value > 0:
            sector_allocation = holdings_df.groupby('sector').agg({
                'market_value' if 'market_value' in holdings_df.columns else 'cost_basis': 'sum'
            }).reset_index()
            sector_allocation.columns = ['Sector', 'Value']
            sector_allocation['Percentage'] = (sector_allocation['Value'] / total_value * 100).round(2)
            
            with col1:
                fig_pie = px.pie(
                    values=sector_allocation['Percentage'],
                    names=sector_allocation['Sector'],
                    title="Sector Allocation"
                )
                st.plotly_chart(fig_pie, width='stretch')
            
            with col2:
                fig_bar = px.bar(
                    x=sector_allocation['Sector'],
                    y=sector_allocation['Percentage'],
                    title="Sector Allocation (Bar Chart)"
                )
                fig_bar.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig_bar, width='stretch')
        else:
            # Show asset type allocation if available
            if 'asset_type' in holdings_df.columns and total_value > 0:
                asset_allocation = holdings_df.groupby('asset_type').agg({
                    'market_value' if 'market_value' in holdings_df.columns else 'cost_basis': 'sum'
                }).reset_index()
                asset_allocation.columns = ['Asset Type', 'Value']
                asset_allocation['Percentage'] = (asset_allocation['Value'] / total_value * 100).round(2)
                
                with col1:
                    fig_pie = px.pie(
                        values=asset_allocation['Percentage'],
                        names=asset_allocation['Asset Type'],
                        title="Asset Type Allocation"
                    )
                    st.plotly_chart(fig_pie, width='stretch')
                
                with col2:
                    fig_bar = px.bar(
                        x=asset_allocation['Asset Type'],
                        y=asset_allocation['Percentage'],
                        title="Asset Type Allocation (Bar Chart)"
                    )
                    fig_bar.update_layout(xaxis_tickangle=45)
                    st.plotly_chart(fig_bar, width='stretch')
            else:
                # Fallback to mock data
                st.info("📊 Upload CSV with sector or asset_type columns for detailed allocation analysis")
                
                allocation_data = {
                    'Sector': ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Other'],
                    'Percentage': [40, 25, 20, 10, 5]
                }
                
                with col1:
                    fig_pie = px.pie(
                        values=allocation_data['Percentage'],
                        names=allocation_data['Sector'],
                        title="Sample Sector Allocation"
                    )
                    st.plotly_chart(fig_pie, width='stretch')
                
                with col2:
                    fig_bar = px.bar(
                        x=allocation_data['Sector'],
                        y=allocation_data['Percentage'],
                        title="Sample Sector Allocation (Bar Chart)"
                    )
                    st.plotly_chart(fig_bar, width='stretch')
        
        # Performance metrics
        st.subheader("📊 Performance Metrics")
        
        # Show real performance if available
        if 'gain_loss' in holdings_df.columns and 'gain_loss_pct' in holdings_df.columns:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_gain_loss = holdings_df['gain_loss'].sum()
                st.metric("Total Gain/Loss", f"${total_gain_loss:,.2f}")
            
            with col2:
                avg_gain_loss_pct = holdings_df['gain_loss_pct'].mean()
                st.metric("Avg Return %", f"{avg_gain_loss_pct:.2f}%")
            
            with col3:
                best_performer = holdings_df.loc[holdings_df['gain_loss_pct'].idxmax()]
                st.metric("Best Performer", f"{best_performer['symbol']} ({best_performer['gain_loss_pct']:.1f}%)")
            
            with col4:
                worst_performer = holdings_df.loc[holdings_df['gain_loss_pct'].idxmin()]
                st.metric("Worst Performer", f"{worst_performer['symbol']} ({worst_performer['gain_loss_pct']:.1f}%)")
        
        # Mock performance data for charts
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)).cumsum(), index=dates)
        
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
            st.plotly_chart(fig_equity, width='stretch')
        
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
            st.plotly_chart(fig_drawdown, width='stretch')
        
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

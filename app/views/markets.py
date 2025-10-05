"""
Markets Page - Real-time market data and news
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render():
    """Render the Markets page."""
    st.title("📈 Market Intelligence")
    st.caption("Real-time market data, news, and analysis")
    
    # Market overview
    st.subheader("🌍 Market Overview")
    
    # Mock market data
    market_data = {
        'Index': ['S&P 500', 'NASDAQ', 'Dow Jones', 'Russell 2000'],
        'Price': [4750.23, 14850.67, 37500.12, 1950.45],
        'Change': [0.52, 0.78, 0.34, -0.12],
        'Change %': [0.01, 0.01, 0.01, -0.01]
    }
    
    df_market = pd.DataFrame(market_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    for i, (_, row) in enumerate(df_market.iterrows()):
        with [col1, col2, col3, col4][i]:
            change_color = "normal" if row['Change %'] >= 0 else "inverse"
            st.metric(
                row['Index'],
                f"${row['Price']:,.2f}",
                f"{row['Change']:+.2f} ({row['Change %']:+.2f}%)",
                delta_color=change_color
            )
    
    # Watchlist
    st.subheader("⭐ Watchlist")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        watchlist_symbols = st.multiselect(
            "Select symbols to watch",
            options=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'],
            default=['AAPL', 'MSFT', 'GOOGL']
        )
    
    with col2:
        if st.button("Update Watchlist"):
            st.session_state.portfolio_data["watchlist"] = watchlist_symbols
            st.success("Watchlist updated!")
    
    # Display watchlist data
    if watchlist_symbols:
        # Mock watchlist data
        watchlist_data = []
        for symbol in watchlist_symbols:
            price = np.random.uniform(100, 500)
            change = np.random.uniform(-5, 5)
            change_pct = (change / price) * 100
            
            watchlist_data.append({
                'Symbol': symbol,
                'Price': f"${price:.2f}",
                'Change': f"{change:+.2f}",
                'Change %': f"{change_pct:+.2f}%",
                'Volume': f"{np.random.randint(1000000, 10000000):,}"
            })
        
        df_watchlist = pd.DataFrame(watchlist_data)
        st.dataframe(df_watchlist, width='stretch')
        
        # Watchlist chart
        st.subheader("📊 Watchlist Performance")
        
        # Mock performance data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        fig = go.Figure()
        
        for symbol in watchlist_symbols[:3]:  # Limit to 3 for readability
            returns = np.random.normal(0.001, 0.02, len(dates)).cumsum()
            fig.add_trace(go.Scatter(
                x=dates,
                y=returns,
                mode='lines',
                name=symbol,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="30-Day Performance",
            xaxis_title="Date",
            yaxis_title="Cumulative Return %",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Market heatmap
    st.subheader("🔥 Sector Heatmap")
    
    # Mock sector data
    sectors = ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy', 'Industrial', 'Materials', 'Utilities']
    sector_returns = np.random.uniform(-3, 3, len(sectors))
    
    heatmap_data = pd.DataFrame({
        'Sector': sectors,
        'Return %': sector_returns
    })
    
    fig_heatmap = px.bar(
        heatmap_data,
        x='Sector',
        y='Return %',
        color='Return %',
        color_continuous_scale='RdYlGn',
        title="Sector Performance Today"
    )
    
    st.plotly_chart(fig_heatmap, width='stretch')
    
    # News feed
    st.subheader("📰 Market News")
    
    # Mock news data
    news_data = [
        {
            'title': 'Tech Stocks Rally on Strong Earnings',
            'source': 'Financial Times',
            'time': '2 hours ago',
            'sentiment': 'Positive'
        },
        {
            'title': 'Federal Reserve Hints at Rate Cuts',
            'source': 'Reuters',
            'time': '4 hours ago',
            'sentiment': 'Neutral'
        },
        {
            'title': 'Energy Sector Faces Headwinds',
            'source': 'Bloomberg',
            'time': '6 hours ago',
            'sentiment': 'Negative'
        },
        {
            'title': 'AI Companies See Surge in Investment',
            'source': 'Wall Street Journal',
            'time': '8 hours ago',
            'sentiment': 'Positive'
        }
    ]
    
    for news in news_data:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**{news['title']}**")
                st.caption(f"{news['source']} • {news['time']}")
            
            with col2:
                sentiment_color = {
                    'Positive': '🟢',
                    'Neutral': '🟡',
                    'Negative': '🔴'
                }[news['sentiment']]
                st.markdown(f"{sentiment_color} {news['sentiment']}")
            
            st.divider()
    
    # Economic calendar
    st.subheader("📅 Economic Calendar")
    
    # Mock calendar data
    calendar_data = [
        {
            'Date': 'Today',
            'Time': '10:00 AM',
            'Event': 'Consumer Price Index',
            'Impact': 'High',
            'Forecast': '3.2%'
        },
        {
            'Date': 'Tomorrow',
            'Time': '2:00 PM',
            'Event': 'Federal Reserve Meeting',
            'Impact': 'High',
            'Forecast': 'Rate Decision'
        },
        {
            'Date': 'Friday',
            'Time': '8:30 AM',
            'Event': 'Non-Farm Payrolls',
            'Impact': 'High',
            'Forecast': '200K'
        }
    ]
    
    df_calendar = pd.DataFrame(calendar_data)
    
    # Color code by impact
    def color_impact(val):
        if val == 'High':
            return 'background-color: #ffebee'
        elif val == 'Medium':
            return 'background-color: #fff3e0'
        else:
            return 'background-color: #e8f5e8'
    
    styled_calendar = df_calendar.style.map(color_impact, subset=['Impact'])
    st.dataframe(styled_calendar, width='stretch')

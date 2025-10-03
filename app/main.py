"""
Finnie - Financial AI Engine
Streamlit Multi-Tab Application

Main entry point for the Finnie application with tabs for:
- Chat: Conversational interface with AI agents
- Portfolio: Portfolio analysis and management
- Markets: Real-time market data and news
- Learn: Educational content and tutorials
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.pages import chat, portfolio, markets, learn
from app.utils import setup_page_config, initialize_session_state

def main():
    """Main application entry point."""
    setup_page_config()
    initialize_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        # st.image("docs/images/logo-poster-transparent.png", width=200)  # Removed SupportVectors logo
        st.title("📈 Finnie")
        st.caption("Financial AI Engine")
        st.caption("Developed by **Sankar Subbayya**")
        
        # Navigation menu
        selected_tab = option_menu(
            menu_title=None,
            options=["Chat", "Portfolio", "Markets", "Learn"],
            icons=["chat-dots", "pie-chart", "graph-up", "book"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
    
    # Main content area
    if selected_tab == "Chat":
        chat.render()
    elif selected_tab == "Portfolio":
        portfolio.render()
    elif selected_tab == "Markets":
        markets.render()
    elif selected_tab == "Learn":
        learn.render()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "📈 Finnie - Financial AI Engine | Developed by <strong>Sankar Subbayya</strong>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

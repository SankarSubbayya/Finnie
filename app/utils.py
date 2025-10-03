"""
Utility functions for the Finnie Streamlit application.
"""

import streamlit as st
from typing import Dict, Any
import json
from datetime import datetime

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Finnie - Financial AI Engine",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "risk_tolerance": "moderate",
            "investment_goals": [],
            "experience_level": "beginner",
            "preferences": {}
        }
    
    if "portfolio_data" not in st.session_state:
        st.session_state.portfolio_data = {
            "holdings": [],
            "watchlist": [],
            "last_updated": None
        }
    
    if "market_data" not in st.session_state:
        st.session_state.market_data = {
            "quotes": {},
            "news": [],
            "calendar": []
        }
    
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = {
            "completed_modules": [],
            "current_path": None,
            "notes": []
        }

def get_user_context() -> Dict[str, Any]:
    """Get current user context for AI agents."""
    return {
        "user_profile": st.session_state.user_profile,
        "portfolio_data": st.session_state.portfolio_data,
        "market_data": st.session_state.market_data,
        "learning_progress": st.session_state.learning_progress,
        "timestamp": datetime.now().isoformat()
    }

def save_user_data():
    """Save user data to session state."""
    # In a real implementation, this would save to a database
    # For now, we'll just ensure session state is updated
    pass

def load_user_data():
    """Load user data from storage."""
    # In a real implementation, this would load from a database
    # For now, we'll use session state
    pass

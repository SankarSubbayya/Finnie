"""
Chat Page - Conversational interface with AI agents
"""

import streamlit as st
from typing import List, Dict, Any
import json
from datetime import datetime

def render():
    """Render the Chat page."""
    st.title("💬 Chat with Finnie")
    st.caption("Ask questions about investing, get portfolio insights, or learn about financial concepts")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.markdown(f"**{source['title']}**")
                            st.markdown(f"*{source['url']}*")
                            st.markdown(f"Relevance: {source['score']:.2f}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about finance..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_ai_response(prompt)
                st.markdown(response["content"])
                
                # Show sources
                if response.get("sources"):
                    with st.expander("📚 Sources"):
                        for source in response["sources"]:
                            st.markdown(f"**{source['title']}**")
                            st.markdown(f"*{source['url']}*")
                            st.markdown(f"Relevance: {source['score']:.2f}")
        
        # Add AI response to messages
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["content"],
            "sources": response.get("sources", []),
            "timestamp": datetime.now().isoformat()
        })
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analyze Portfolio"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Please analyze my current portfolio",
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()
    
    with col2:
        if st.button("📈 Market Update"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Give me a market update",
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()
    
    with col3:
        if st.button("🎓 Explain Concept"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Explain a financial concept",
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()
    
    with col4:
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

def generate_ai_response(prompt: str) -> Dict[str, Any]:
    """Generate AI response using the LangGraph system."""
    # This is a placeholder - in the real implementation, this would call the LangGraph system
    # For now, we'll return a mock response
    
    # Simple keyword-based routing (will be replaced with LangGraph)
    if "portfolio" in prompt.lower():
        return {
            "content": "I'd be happy to analyze your portfolio! Please upload your holdings data in the Portfolio tab, or tell me about your current investments.",
            "sources": []
        }
    elif "market" in prompt.lower():
        return {
            "content": "Here's a quick market update: The S&P 500 is up 0.5% today. Tech stocks are leading gains, while energy stocks are mixed. Check the Markets tab for detailed quotes and news.",
            "sources": [
                {
                    "title": "Market Data",
                    "url": "https://finance.yahoo.com",
                    "score": 0.95
                }
            ]
        }
    elif "explain" in prompt.lower() or "what is" in prompt.lower():
        return {
            "content": "I'd be happy to explain that concept! Let me search our knowledge base for the most relevant information.",
            "sources": [
                {
                    "title": "Financial Education Content",
                    "url": "https://finnie.learn",
                    "score": 0.88
                }
            ]
        }
    else:
        return {
            "content": "I'm here to help with your financial questions! You can ask me about portfolio analysis, market updates, or financial concepts. What would you like to know?",
            "sources": []
        }

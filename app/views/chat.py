"""
Chat Page - Conversational interface with AI agents
"""

import streamlit as st
from typing import List, Dict, Any
import json
from datetime import datetime
import logging

# Import the LangGraph workflow
try:
    from graph.workflow import FinnieWorkflow
    from app.utils import get_user_context
    WORKFLOW_AVAILABLE = True
except ImportError as e:
    st.warning(f"LangGraph workflow not available: {e}")
    WORKFLOW_AVAILABLE = False

# Initialize the workflow
if WORKFLOW_AVAILABLE:
    try:
        workflow = FinnieWorkflow()
    except Exception as e:
        st.error(f"Failed to initialize workflow: {e}")
        WORKFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)

def render():
    """Render the Chat page."""
    st.title("💬 Chat with Finnie")
    st.caption("Ask questions about investing, get portfolio insights, or learn about financial concepts")
    
    # Debug info
    if st.checkbox("🔧 Show Debug Info"):
        st.write("Session state keys:", list(st.session_state.keys()))
        st.write("Messages count:", len(st.session_state.get("messages", [])))
        st.write("Workflow available:", WORKFLOW_AVAILABLE)
    
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
    
    # Show pre-populated text if available
    if "text_query" in st.session_state:
        st.info(f"💡 **Suggested question**: {st.session_state['text_query']}")
        if st.button("📝 Use this question"):
            # Add the suggested question as a user message
            st.session_state.messages.append({
                "role": "user",
                "content": st.session_state["text_query"],
                "timestamp": datetime.now().isoformat()
            })
            del st.session_state["text_query"]
            st.rerun()
    
    # Chat input
    prompt = st.chat_input("Ask me anything about finance...")
    
    if prompt:
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
            with st.spinner("🤖 AI agents are thinking..."):
                try:
                    response = generate_ai_response(prompt)
                    
                    # Display the main response content
                    if response and response.get("content"):
                        st.markdown(response["content"])
                    else:
                        st.error("No response content generated")
                        st.write("Response:", response)
                        
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.write("Please try again or check the debug info above.")
                
                # Show agent information
                if response.get("agent") and response.get("confidence"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"🤖 **Agent**: {response['agent'].title()}")
                    with col2:
                        confidence_color = "green" if response['confidence'] > 0.7 else "orange" if response['confidence'] > 0.4 else "red"
                        st.caption(f"🎯 **Confidence**: :{confidence_color}[{response['confidence']:.1%}]")
                
                # Show sources
                if response.get("sources"):
                    with st.expander("📚 Sources & References"):
                        for source in response["sources"]:
                            st.markdown(f"**{source['title']}**")
                            st.markdown(f"*{source['url']}*")
                            st.markdown(f"Relevance: {source['score']:.2f}")
                            st.markdown("---")
                
                # Show compliance status
                if response.get("approved") is not None:
                    if response["approved"]:
                        st.success("✅ Response approved by compliance")
                    else:
                        st.warning("⚠️ Response pending compliance review")
        
        # Add AI response to messages
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["content"],
            "sources": response.get("sources", []),
            "timestamp": datetime.now().isoformat()
        })
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Portfolio Analysis", help="Get AI-powered portfolio insights"):
            st.session_state["text_query"] = "Please analyze my current portfolio and provide recommendations"
            st.rerun()
    
    with col2:
        if st.button("📈 Market Intelligence", help="Get real-time market data and analysis"):
            st.session_state["text_query"] = "Give me a comprehensive market update with analysis"
            st.rerun()
    
    with col3:
        if st.button("🎓 Learn Finance", help="Get educational content about financial concepts"):
            st.session_state["text_query"] = "Teach me about investment strategies and risk management"
            st.rerun()
    
    with col4:
        if st.button("🔄 Clear Chat", help="Start a new conversation"):
            st.session_state.messages = []
            st.rerun()
    
    # Additional quick actions
    st.markdown("### 💡 Try These Questions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("What is diversification?"):
            st.session_state["text_query"] = "What is diversification and why is it important in investing?"
            st.rerun()
        
        if st.button("How do I calculate risk?"):
            st.session_state["text_query"] = "How do I calculate and assess investment risk?"
            st.rerun()
    
    with col2:
        if st.button("What are ETFs?"):
            st.session_state["text_query"] = "What are ETFs and how do they work?"
            st.rerun()
        
        if st.button("Market trends today"):
            st.session_state["text_query"] = "What are the current market trends and what should I watch?"
            st.rerun()

def generate_ai_response(prompt: str) -> Dict[str, Any]:
    """Generate AI response using the LangGraph system."""
    
    if not WORKFLOW_AVAILABLE:
        # Fallback to simple responses if workflow is not available
        return _generate_fallback_response(prompt)
    
    try:
        # Get user context from session state (with fallback)
        try:
            user_context = get_user_context()
        except AttributeError:
            # Fallback if session state is not available
            user_context = {
                "user_profile": {"experience_level": "beginner"},
                "portfolio_data": {"holdings": []},
                "market_data": {"quotes": {}},
                "learning_progress": {"completed_modules": []}
            }
        
        # Generate a unique user ID for this session
        user_id = st.session_state.get("user_id", "default_user") if hasattr(st, 'session_state') else "default_user"
        
        # Process the query through the LangGraph workflow
        result = workflow.process_query(
            user_id=user_id,
            query=prompt,
            context=user_context
        )
        
        # Extract response and sources
        response_content = result.get("response", "I'm sorry, I couldn't generate a response.")
        sources = result.get("sources", [])
        
        # Add agent information to the response
        agent = result.get("agent", "unknown")
        confidence = result.get("confidence", 0.0)
        
        # Enhance response with metadata
        if confidence > 0.7:
            response_content += f"\n\n*[Response from {agent.title()} Agent - High Confidence]*"
        elif confidence > 0.4:
            response_content += f"\n\n*[Response from {agent.title()} Agent - Medium Confidence]*"
        else:
            response_content += f"\n\n*[Response from {agent.title()} Agent - Low Confidence]*"
        
        return {
            "content": response_content,
            "sources": sources,
            "agent": agent,
            "confidence": confidence,
            "approved": result.get("approved", False)
        }
        
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        st.error(f"Error generating response: {str(e)}")
        
        # Fallback to simple response
        return _generate_fallback_response(prompt)

def _generate_fallback_response(prompt: str) -> Dict[str, Any]:
    """Generate a fallback response when the AI system is not available."""
    
    # Simple keyword-based routing as fallback
    if "portfolio" in prompt.lower():
        return {
            "content": "I'd be happy to analyze your portfolio! Please upload your holdings data in the Portfolio tab, or tell me about your current investments. You can also use the Portfolio tab to get detailed analysis with charts and metrics.",
            "sources": [
                {
                    "title": "Portfolio Analysis Guide",
                    "url": "https://finnie.learn/portfolio",
                    "score": 0.9
                }
            ]
        }
    elif "market" in prompt.lower():
        return {
            "content": "Here's a quick market update: The S&P 500 is up 0.5% today. Tech stocks are leading gains, while energy stocks are mixed. Check the Markets tab for detailed quotes, news, and market analysis.",
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
            "content": "I'd be happy to explain that concept! Let me search our knowledge base for the most relevant information. You can also check the Learn tab for comprehensive educational content.",
            "sources": [
                {
                    "title": "Financial Education Content",
                    "url": "https://finnie.learn",
                    "score": 0.88
                }
            ]
        }
    elif "help" in prompt.lower() or "how" in prompt.lower():
        return {
            "content": "I'm here to help with your financial questions! Here's what I can assist you with:\n\n• **Portfolio Analysis**: Upload your holdings and get detailed analysis\n• **Market Updates**: Get real-time market data and news\n• **Financial Education**: Learn about investing concepts and strategies\n• **Risk Assessment**: Understand your portfolio's risk profile\n\nWhat would you like to explore?",
            "sources": []
        }
    else:
        return {
            "content": "I'm here to help with your financial questions! You can ask me about:\n\n• Portfolio analysis and optimization\n• Market trends and updates\n• Financial concepts and education\n• Investment strategies\n• Risk management\n\nWhat would you like to know?",
            "sources": []
        }

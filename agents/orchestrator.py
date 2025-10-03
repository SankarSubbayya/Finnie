"""
Orchestrator Agent - Main coordinator for the multi-agent system
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Available agent types."""
    TUTOR = "tutor"
    PORTFOLIO = "portfolio"
    MARKET = "market"
    COMPLIANCE = "compliance"
    ONBOARDING = "onboarding"

@dataclass
class AgentState:
    """State object for the multi-agent system."""
    user_id: str
    query: str
    context: Dict[str, Any]
    retrieval: Dict[str, Any]
    market: Dict[str, Any]
    analysis: Dict[str, Any]
    compliance: Dict[str, Any]
    messages: List[Dict[str, Any]]
    current_agent: Optional[AgentType] = None
    intent: Optional[str] = None
    confidence: float = 0.0

class OrchestratorAgent:
    """Main orchestrator agent that routes queries to appropriate agents."""
    
    def __init__(self):
        self.agents = {}
        self.intent_keywords = {
            AgentType.TUTOR: [
                "explain", "what is", "how does", "learn", "teach", "concept",
                "definition", "meaning", "tutorial", "guide", "help me understand"
            ],
            AgentType.PORTFOLIO: [
                "portfolio", "analyze", "holdings", "performance", "allocation",
                "rebalance", "risk", "diversification", "sharpe", "volatility",
                "drawdown", "returns", "metrics"
            ],
            AgentType.MARKET: [
                "market", "price", "quote", "news", "update", "trend", "forecast",
                "analysis", "sector", "index", "stocks", "trading", "volatility"
            ],
            AgentType.ONBOARDING: [
                "start", "begin", "new", "setup", "profile", "goals", "risk",
                "preferences", "onboarding", "introduction"
            ]
        }
    
    def register_agent(self, agent_type: AgentType, agent_instance):
        """Register an agent with the orchestrator."""
        self.agents[agent_type] = agent_instance
        logger.info(f"Registered agent: {agent_type.value}")
    
    def route_query(self, state: AgentState) -> AgentType:
        """Route a query to the most appropriate agent."""
        query_lower = state.query.lower()
        
        # Calculate confidence scores for each agent
        scores = {}
        for agent_type, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            scores[agent_type] = score
        
        # Find the agent with the highest score
        if scores:
            best_agent = max(scores, key=scores.get)
            state.confidence = scores[best_agent] / len(query_lower.split())
            state.current_agent = best_agent
            state.intent = best_agent.value
        else:
            # Default to tutor for general queries
            state.current_agent = AgentType.TUTOR
            state.confidence = 0.5
            state.intent = "general"
        
        logger.info(f"Routed query to {state.current_agent.value} (confidence: {state.confidence:.2f})")
        return state.current_agent
    
    def execute_agent(self, state: AgentState) -> Dict[str, Any]:
        """Execute the appropriate agent for the current state."""
        if state.current_agent not in self.agents:
            return {
                "error": f"Agent {state.current_agent.value} not available",
                "response": "I'm sorry, that functionality is not available right now."
            }
        
        try:
            agent = self.agents[state.current_agent]
            result = agent.process(state)
            
            # Add metadata
            result.update({
                "agent": state.current_agent.value,
                "confidence": state.confidence,
                "intent": state.intent
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing agent {state.current_agent.value}: {str(e)}")
            return {
                "error": str(e),
                "response": "I encountered an error processing your request. Please try again."
            }
    
    def process_query(self, user_id: str, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user query through the multi-agent system."""
        # Initialize state
        state = AgentState(
            user_id=user_id,
            query=query,
            context=context or {},
            retrieval={},
            market={},
            analysis={},
            compliance={},
            messages=[]
        )
        
        # Route query to appropriate agent
        self.route_query(state)
        
        # Execute agent
        result = self.execute_agent(state)
        
        # Add to message history
        state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": state.context.get("timestamp")
        })
        
        state.messages.append({
            "role": "assistant",
            "content": result.get("response", ""),
            "agent": state.current_agent.value,
            "timestamp": state.context.get("timestamp")
        })
        
        return result

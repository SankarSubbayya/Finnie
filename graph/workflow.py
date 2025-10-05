"""
LangGraph Workflow - Main workflow orchestration
"""

from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import logging

from agents.orchestrator import OrchestratorAgent, AgentState, AgentType
from agents.tutor import TutorAgent
from agents.portfolio import PortfolioAnalystAgent
from agents.market import MarketIntelligenceAgent
from agents.compliance import ComplianceAgent

logger = logging.getLogger(__name__)

class FinnieState(TypedDict):
    """State definition for the Finnie workflow."""
    user_id: str
    query: str
    context: Dict[str, Any]
    retrieval: Dict[str, Any]
    market: Dict[str, Any]
    analysis: Dict[str, Any]
    compliance: Dict[str, Any]
    messages: List[Dict[str, Any]]
    current_agent: Optional[str]
    intent: Optional[str]
    confidence: float
    response: str
    sources: List[Dict[str, Any]]
    approved: bool

class FinnieWorkflow:
    """Main workflow class for the Finnie multi-agent system."""
    
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.tutor_agent = TutorAgent()
        self.portfolio_agent = PortfolioAnalystAgent()
        self.market_agent = MarketIntelligenceAgent()
        self.compliance_agent = ComplianceAgent()
        
        # Register agents with orchestrator
        self.orchestrator.register_agent(AgentType.TUTOR, self.tutor_agent)
        self.orchestrator.register_agent(AgentType.PORTFOLIO, self.portfolio_agent)
        self.orchestrator.register_agent(AgentType.MARKET, self.market_agent)
        
        # Build the workflow graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(FinnieState)
        
        # Add nodes
        workflow.add_node("router", self._router_node)
        workflow.add_node("tutor", self._tutor_node)
        workflow.add_node("portfolio", self._portfolio_node)
        workflow.add_node("market", self._market_node)
        workflow.add_node("compliance", self._compliance_node)
        workflow.add_node("responder", self._responder_node)
        
        # Add entry point from START to router
        workflow.set_entry_point("router")
        
        # Add conditional edges from router to specific agents
        workflow.add_conditional_edges(
            "router",
            self._route_to_agent,
            {
                "tutor": "tutor",
                "portfolio": "portfolio", 
                "market": "market"
            }
        )
        
        # Add edges from agents to compliance
        workflow.add_edge("tutor", "compliance")
        workflow.add_edge("portfolio", "compliance")
        workflow.add_edge("market", "compliance")
        
        # Add edge from compliance to responder
        workflow.add_edge("compliance", "responder")
        
        # Add edge from responder to END
        workflow.add_edge("responder", END)
        
        return workflow.compile()
    
    def _route_to_agent(self, state: FinnieState) -> str:
        """Determine which agent to route to based on the current agent."""
        return state.get("current_agent", "tutor")
    
    def _router_node(self, state: FinnieState) -> FinnieState:
        """Route the query to the appropriate agent."""
        try:
            # Convert state to AgentState
            agent_state = AgentState(
                user_id=state["user_id"],
                query=state["query"],
                context=state["context"],
                retrieval=state["retrieval"],
                market=state["market"],
                analysis=state["analysis"],
                compliance=state["compliance"],
                messages=state["messages"]
            )
            
            # Route the query
            agent_type = self.orchestrator.route_query(agent_state)
            
            # Update state with routing information
            state["current_agent"] = agent_type.value
            state["intent"] = agent_state.intent
            state["confidence"] = agent_state.confidence
            
            logger.info(f"Routed query to {agent_type.value}")
            
        except Exception as e:
            logger.error(f"Error in router node: {str(e)}")
            state["current_agent"] = "tutor"  # Default fallback
            state["intent"] = "general"
            state["confidence"] = 0.0
        
        return state
    
    def _tutor_node(self, state: FinnieState) -> FinnieState:
        """Process query through tutor agent."""
        if state["current_agent"] != "tutor":
            return state
        
        # Ensure analysis dictionary exists
        if "analysis" not in state:
            state["analysis"] = {}
        
        try:
            agent_state = AgentState(
                user_id=state["user_id"],
                query=state["query"],
                context=state["context"],
                retrieval=state["retrieval"],
                market=state["market"],
                analysis=state["analysis"],
                compliance=state["compliance"],
                messages=state["messages"]
            )
            
            result = self.tutor_agent.process(agent_state)
            
            # Update state with tutor response
            state["analysis"]["response"] = result["response"]
            state["sources"] = result.get("sources", [])
            state["analysis"]["follow_up_questions"] = result.get("follow_up_questions", [])
            state["analysis"]["concepts_covered"] = result.get("concepts_covered", [])
            
        except Exception as e:
            logger.error(f"Error in tutor node: {str(e)}")
            state["analysis"]["response"] = "I'm sorry, I encountered an error processing your educational request. Please try again."
            state["sources"] = []
        
        return state
    
    def _portfolio_node(self, state: FinnieState) -> FinnieState:
        """Process query through portfolio agent."""
        if state["current_agent"] != "portfolio":
            return state
        
        # Ensure analysis dictionary exists
        if "analysis" not in state:
            state["analysis"] = {}
        
        try:
            agent_state = AgentState(
                user_id=state["user_id"],
                query=state["query"],
                context=state["context"],
                retrieval=state["retrieval"],
                market=state["market"],
                analysis=state["analysis"],
                compliance=state["compliance"],
                messages=state["messages"]
            )
            
            result = self.portfolio_agent.process(agent_state)
            
            # Update state with portfolio response
            state["analysis"]["response"] = result["response"]
            state["sources"] = result.get("sources", [])
            state["analysis"]["recommendations"] = result.get("recommendations", [])
            state["analysis"]["metrics"] = result.get("metrics", {})
            
        except Exception as e:
            logger.error(f"Error in portfolio node: {str(e)}")
            state["analysis"]["response"] = "I'm sorry, I encountered an error analyzing your portfolio. Please try again."
            state["sources"] = []
        
        return state
    
    def _market_node(self, state: FinnieState) -> FinnieState:
        """Process query through market agent."""
        if state["current_agent"] != "market":
            return state
        
        # Ensure analysis dictionary exists
        if "analysis" not in state:
            state["analysis"] = {}
        
        try:
            agent_state = AgentState(
                user_id=state["user_id"],
                query=state["query"],
                context=state["context"],
                retrieval=state["retrieval"],
                market=state["market"],
                analysis=state["analysis"],
                compliance=state["compliance"],
                messages=state["messages"]
            )
            
            result = self.market_agent.process(agent_state)
            
            # Update state with market response
            state["analysis"]["response"] = result["response"]
            state["sources"] = result.get("sources", [])
            state["market"] = result.get("market_data", {})
            state["analysis"]["news"] = result.get("news", [])
            
        except Exception as e:
            logger.error(f"Error in market node: {str(e)}")
            state["analysis"]["response"] = "I'm sorry, I encountered an error retrieving market data. Please try again."
            state["sources"] = []
        
        return state
    
    def _compliance_node(self, state: FinnieState) -> FinnieState:
        """Process response through compliance agent."""
        try:
            # Ensure analysis dictionary exists
            if "analysis" not in state:
                state["analysis"] = {}
            
            # Get the response from analysis
            response = state["analysis"].get("response", "")
            agent_type = state["current_agent"] or "general"
            
            # Validate through compliance agent
            compliance_result = self.compliance_agent.validate_agent_response(
                {"response": response}, agent_type
            )
            
            # Update state with compliance results
            state["compliance"] = compliance_result["compliance"]
            state["analysis"]["response"] = compliance_result["response"]
            state["approved"] = compliance_result["approved"]
            
        except Exception as e:
            logger.error(f"Error in compliance node: {str(e)}")
            state["approved"] = False
            state["compliance"] = {
                "disclaimers": ["This response has not been compliance reviewed."],
                "risk_warnings": ["Please consult with a financial advisor before making investment decisions."]
            }
            # Ensure analysis exists even on error
            if "analysis" not in state:
                state["analysis"] = {}
        
        return state
    
    def _responder_node(self, state: FinnieState) -> FinnieState:
        """Format the final response."""
        try:
            # Ensure analysis dictionary exists
            if "analysis" not in state:
                state["analysis"] = {}
            
            response = state["analysis"].get("response", "")
            sources = state.get("sources", [])
            compliance = state.get("compliance", {})
            
            # Add disclaimers to response
            if compliance.get("disclaimers"):
                response += "\n\n---\n"
                response += "**Important Disclaimers:**\n"
                for disclaimer in compliance["disclaimers"]:
                    response += f"• {disclaimer}\n"
            
            # Add risk warnings
            if compliance.get("risk_warnings"):
                response += "\n**Risk Warnings:**\n"
                for warning in compliance["risk_warnings"]:
                    response += f"• {warning}\n"
            
            state["response"] = response
            
        except Exception as e:
            logger.error(f"Error in responder node: {str(e)}")
            state["response"] = "I'm sorry, I encountered an error formatting the response. Please try again."
        
        return state
    
    def process_query(self, user_id: str, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user query through the complete workflow."""
        try:
            # Initialize state
            initial_state = FinnieState(
                user_id=user_id,
                query=query,
                context=context or {},
                retrieval={},
                market={},
                analysis={},
                compliance={},
                messages=[],
                current_agent=None,
                intent=None,
                confidence=0.0,
                response="",
                sources=[],
                approved=False
            )
            
            # Run the workflow
            result = self.graph.invoke(initial_state)
            
            # Return the final result
            return {
                "response": result["response"],
                "sources": result["sources"],
                "agent": result["current_agent"],
                "intent": result["intent"],
                "confidence": result["confidence"],
                "approved": result["approved"],
                "compliance": result["compliance"],
                "analysis": result["analysis"]
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "sources": [],
                "agent": "error",
                "intent": "error",
                "confidence": 0.0,
                "approved": False,
                "compliance": {},
                "analysis": {}
            }

"""
Compliance & Safety Agent - Ensures all responses meet regulatory requirements
"""

from typing import Dict, Any, List, Optional
import logging
import re
from .orchestrator import AgentState

logger = logging.getLogger(__name__)

class ComplianceAgent:
    """Agent that ensures all responses meet compliance and safety requirements."""
    
    def __init__(self):
        self.disclaimers = {
            "general": "This information is for educational purposes only and should not be considered as investment advice.",
            "portfolio": "Portfolio analysis is for educational purposes only. Past performance does not guarantee future results.",
            "market": "Market data and analysis are for informational purposes only and should not be considered as investment advice.",
            "trading": "Trading involves risk and may not be suitable for all investors. Please consult with a financial advisor."
        }
        
        self.prohibited_content = [
            "guaranteed returns", "risk-free", "sure thing", "can't lose",
            "guaranteed profit", "guaranteed income", "no risk", "safe bet"
        ]
        
        self.risk_warnings = [
            "Investing involves risk, including the potential loss of principal.",
            "Past performance does not guarantee future results.",
            "Diversification does not ensure a profit or protect against loss.",
            "Consider your investment objectives and risk tolerance before investing."
        ]
    
    def process(self, state: AgentState) -> Dict[str, Any]:
        """Process and validate agent response for compliance."""
        # Get the response from the previous agent
        response = state.analysis.get("response", "")
        agent_type = state.current_agent.value if state.current_agent else "general"
        
        # Check for compliance issues
        compliance_checks = self._run_compliance_checks(response, agent_type)
        
        # Generate appropriate disclaimers
        disclaimers = self._generate_disclaimers(agent_type, compliance_checks)
        
        # Sanitize response if needed
        sanitized_response = self._sanitize_response(response, compliance_checks)
        
        # Add compliance metadata
        compliance_metadata = {
            "disclaimers": disclaimers,
            "risk_warnings": self._get_risk_warnings(agent_type),
            "compliance_flags": compliance_checks["flags"],
            "jurisdiction": "US",  # Default jurisdiction
            "last_updated": "2024-01-01"
        }
        
        return {
            "response": sanitized_response,
            "compliance": compliance_metadata,
            "approved": compliance_checks["approved"],
            "flags": compliance_checks["flags"]
        }
    
    def _run_compliance_checks(self, response: str, agent_type: str) -> Dict[str, Any]:
        """Run comprehensive compliance checks on the response."""
        checks = {
            "approved": True,
            "flags": [],
            "issues": []
        }
        
        response_lower = response.lower()
        
        # Check for prohibited content
        for prohibited in self.prohibited_content:
            if prohibited in response_lower:
                checks["approved"] = False
                checks["flags"].append("prohibited_content")
                checks["issues"].append(f"Contains prohibited phrase: '{prohibited}'")
        
        # Check for personalized advice
        advice_indicators = [
            "you should", "you must", "you need to", "i recommend you",
            "you ought to", "you would be wise to", "you would benefit from"
        ]
        
        for indicator in advice_indicators:
            if indicator in response_lower:
                checks["flags"].append("personalized_advice")
                checks["issues"].append("Contains personalized investment advice")
        
        # Check for specific investment recommendations
        recommendation_patterns = [
            r"buy\s+\w+", r"sell\s+\w+", r"invest\s+in\s+\w+",
            r"purchase\s+\w+", r"avoid\s+\w+"
        ]
        
        for pattern in recommendation_patterns:
            if re.search(pattern, response_lower):
                checks["flags"].append("investment_recommendation")
                checks["issues"].append("Contains specific investment recommendations")
        
        # Check for promises of returns
        return_promises = [
            r"guaranteed\s+\d+%", r"promise\s+\d+%", r"ensure\s+\d+%",
            r"guarantee\s+\d+%", r"promised\s+\d+%"
        ]
        
        for pattern in return_promises:
            if re.search(pattern, response_lower):
                checks["approved"] = False
                checks["flags"].append("return_promise")
                checks["issues"].append("Contains promises of specific returns")
        
        # Check for time-sensitive information
        time_sensitive = [
            "today only", "limited time", "act now", "immediate action",
            "urgent", "time-sensitive", "expires soon"
        ]
        
        for phrase in time_sensitive:
            if phrase in response_lower:
                checks["flags"].append("time_sensitive")
                checks["issues"].append("Contains time-sensitive language")
        
        return checks
    
    def _sanitize_response(self, response: str, compliance_checks: Dict[str, Any]) -> str:
        """Sanitize response to remove compliance issues."""
        sanitized = response
        
        # Remove prohibited content
        for prohibited in self.prohibited_content:
            sanitized = re.sub(prohibited, "[content removed for compliance]", sanitized, flags=re.IGNORECASE)
        
        # Replace personalized advice with educational language
        advice_replacements = {
            "you should": "one might consider",
            "you must": "it's important to understand that",
            "you need to": "it's worth noting that",
            "i recommend you": "research suggests that",
            "you ought to": "it may be beneficial to",
            "you would be wise to": "it's worth considering that",
            "you would benefit from": "one might benefit from"
        }
        
        for old, new in advice_replacements.items():
            sanitized = re.sub(old, new, sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def _generate_disclaimers(self, agent_type: str, compliance_checks: Dict[str, Any]) -> List[str]:
        """Generate appropriate disclaimers based on agent type and compliance checks."""
        disclaimers = []
        
        # Add general disclaimer
        disclaimers.append(self.disclaimers["general"])
        
        # Add agent-specific disclaimer
        if agent_type in self.disclaimers:
            disclaimers.append(self.disclaimers[agent_type])
        
        # Add specific disclaimers based on flags
        if "personalized_advice" in compliance_checks["flags"]:
            disclaimers.append("This response is for educational purposes only and should not be considered as personalized investment advice.")
        
        if "investment_recommendation" in compliance_checks["flags"]:
            disclaimers.append("Any investment examples are for educational purposes only and should not be considered as recommendations.")
        
        if "return_promise" in compliance_checks["flags"]:
            disclaimers.append("No investment can guarantee returns. All investments carry risk.")
        
        return disclaimers
    
    def _get_risk_warnings(self, agent_type: str) -> List[str]:
        """Get appropriate risk warnings for the agent type."""
        warnings = self.risk_warnings.copy()
        
        if agent_type == "portfolio":
            warnings.append("Portfolio analysis is based on historical data and may not reflect future performance.")
        
        elif agent_type == "market":
            warnings.append("Market data is subject to change and may not be current at the time of your decision.")
        
        elif agent_type == "trading":
            warnings.append("Trading involves substantial risk and may not be suitable for all investors.")
        
        return warnings
    
    def validate_agent_response(self, agent_response: Dict[str, Any], agent_type: str) -> Dict[str, Any]:
        """Validate a complete agent response for compliance."""
        response_text = agent_response.get("response", "")
        
        # Run compliance checks
        compliance_checks = self._run_compliance_checks(response_text, agent_type)
        
        # Generate disclaimers
        disclaimers = self._generate_disclaimers(agent_type, compliance_checks)
        
        # Sanitize response
        sanitized_response = self._sanitize_response(response_text, compliance_checks)
        
        # Create compliance metadata
        compliance_metadata = {
            "disclaimers": disclaimers,
            "risk_warnings": self._get_risk_warnings(agent_type),
            "compliance_flags": compliance_checks["flags"],
            "approved": compliance_checks["approved"],
            "jurisdiction": "US",
            "last_updated": "2024-01-01"
        }
        
        # Update the agent response
        agent_response["response"] = sanitized_response
        agent_response["compliance"] = compliance_metadata
        agent_response["approved"] = compliance_checks["approved"]
        
        return agent_response

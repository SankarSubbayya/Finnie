"""
Tutor Agent - Educational agent for teaching financial concepts
"""

from typing import Dict, Any, List
import logging
from .orchestrator import AgentState

logger = logging.getLogger(__name__)

class TutorAgent:
    """Educational agent that teaches financial concepts using Socratic Q&A."""
    
    def __init__(self, rag_system=None):
        self.rag_system = rag_system
        self.teaching_style = "socratic"  # socratic, direct, interactive
        self.difficulty_levels = ["beginner", "intermediate", "advanced"]
    
    def process(self, state: AgentState) -> Dict[str, Any]:
        """Process a tutoring request."""
        query = state.query
        user_context = state.context
        
        # Determine user's knowledge level
        knowledge_level = self._assess_knowledge_level(user_context)
        
        # Search for relevant educational content
        educational_content = self._search_educational_content(query, knowledge_level)
        
        # Generate educational response
        response = self._generate_educational_response(
            query, educational_content, knowledge_level, state
        )
        
        return {
            "response": response["content"],
            "sources": response.get("sources", []),
            "follow_up_questions": response.get("follow_up_questions", []),
            "difficulty_level": knowledge_level,
            "concepts_covered": response.get("concepts_covered", []),
            "learning_objectives": response.get("learning_objectives", [])
        }
    
    def _assess_knowledge_level(self, context: Dict[str, Any]) -> str:
        """Assess the user's knowledge level based on context."""
        user_profile = context.get("user_profile", {})
        experience_level = user_profile.get("experience_level", "beginner")
        
        # Map experience levels to knowledge levels
        level_mapping = {
            "beginner": "beginner",
            "intermediate": "intermediate", 
            "advanced": "advanced",
            "expert": "advanced"
        }
        
        return level_mapping.get(experience_level, "beginner")
    
    def _search_educational_content(self, query: str, knowledge_level: str) -> List[Dict[str, Any]]:
        """Search for relevant educational content."""
        if self.rag_system:
            # Use RAG system to find relevant content
            search_results = self.rag_system.search(
                query=query,
                filters={"level": knowledge_level, "type": "educational"},
                limit=5
            )
            return search_results
        else:
            # Fallback to mock content
            return self._get_mock_educational_content(query, knowledge_level)
    
    def _get_mock_educational_content(self, query: str, knowledge_level: str) -> List[Dict[str, Any]]:
        """Get mock educational content for testing."""
        mock_content = {
            "beginner": [
                {
                    "title": "Introduction to Investing",
                    "content": "Investing is the act of allocating resources, usually money, with the expectation of generating an income or profit...",
                    "url": "https://finnie.learn/investing-basics",
                    "level": "beginner",
                    "score": 0.95
                }
            ],
            "intermediate": [
                {
                    "title": "Portfolio Theory and Risk Management",
                    "content": "Modern Portfolio Theory (MPT) is a framework for constructing investment portfolios...",
                    "url": "https://finnie.learn/portfolio-theory",
                    "level": "intermediate",
                    "score": 0.92
                }
            ],
            "advanced": [
                {
                    "title": "Quantitative Analysis and Derivatives",
                    "content": "Quantitative analysis involves the use of mathematical and statistical methods...",
                    "url": "https://finnie.learn/quantitative-analysis",
                    "level": "advanced",
                    "score": 0.88
                }
            ]
        }
        
        return mock_content.get(knowledge_level, mock_content["beginner"])
    
    def _generate_educational_response(self, query: str, content: List[Dict[str, Any]], 
                                     knowledge_level: str, state: AgentState) -> Dict[str, Any]:
        """Generate an educational response using Socratic method."""
        
        if not content:
            return {
                "content": "I'd be happy to help you learn about that topic! However, I don't have specific content about it in my knowledge base. Could you rephrase your question or ask about a related concept?",
                "sources": [],
                "follow_up_questions": [
                    "What specific aspect of finance would you like to learn about?",
                    "Are you looking for beginner, intermediate, or advanced content?",
                    "What's your current experience level with investing?"
                ]
            }
        
        # Use the best matching content
        best_content = content[0]
        
        # Generate Socratic response
        response_parts = []
        
        # Start with a question to engage the user
        engagement_question = self._generate_engagement_question(query, knowledge_level)
        response_parts.append(engagement_question)
        
        # Provide the educational content
        response_parts.append(f"\n{best_content['content']}")
        
        # Add follow-up questions
        follow_up_questions = self._generate_follow_up_questions(query, knowledge_level)
        
        # Extract key concepts
        concepts_covered = self._extract_concepts(best_content['content'])
        
        # Generate learning objectives
        learning_objectives = self._generate_learning_objectives(query, concepts_covered)
        
        return {
            "content": "\n\n".join(response_parts),
            "sources": [{
                "title": best_content['title'],
                "url": best_content['url'],
                "score": best_content['score']
            }],
            "follow_up_questions": follow_up_questions,
            "concepts_covered": concepts_covered,
            "learning_objectives": learning_objectives
        }
    
    def _generate_engagement_question(self, query: str, knowledge_level: str) -> str:
        """Generate an engaging question to start the learning process."""
        questions = {
            "beginner": [
                "Great question! Let me help you understand this step by step.",
                "That's an excellent starting point for learning about finance!",
                "I'm excited to help you learn about this important concept!"
            ],
            "intermediate": [
                "Interesting question! Let's dive deeper into this concept.",
                "That shows good understanding! Let me build on what you know.",
                "Great question! This is a key concept in financial analysis."
            ],
            "advanced": [
                "Excellent question! This is a sophisticated concept that requires careful analysis.",
                "That's a nuanced question that touches on advanced financial theory.",
                "Great question! Let's explore the complexities of this topic."
            ]
        }
        
        import random
        return random.choice(questions.get(knowledge_level, questions["beginner"]))
    
    def _generate_follow_up_questions(self, query: str, knowledge_level: str) -> List[str]:
        """Generate follow-up questions to encourage deeper learning."""
        follow_ups = {
            "beginner": [
                "What do you think are the main benefits of this approach?",
                "How might this concept apply to your personal finances?",
                "What questions do you have about this topic?",
                "Would you like to see a practical example?"
            ],
            "intermediate": [
                "How does this relate to other financial concepts you know?",
                "What are the potential risks and limitations?",
                "How would you apply this in a real-world scenario?",
                "What factors would you consider when implementing this?"
            ],
            "advanced": [
                "What are the mathematical foundations of this concept?",
                "How does this relate to modern portfolio theory?",
                "What are the empirical studies that support this?",
                "How would you model this quantitatively?"
            ]
        }
        
        import random
        return random.sample(follow_ups.get(knowledge_level, follow_ups["beginner"]), 2)
    
    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from educational content."""
        # Simple keyword extraction (in production, use NLP libraries)
        financial_terms = [
            "portfolio", "risk", "return", "diversification", "volatility",
            "sharpe ratio", "beta", "alpha", "correlation", "covariance",
            "efficient frontier", "capital asset pricing model", "arbitrage"
        ]
        
        concepts = []
        content_lower = content.lower()
        for term in financial_terms:
            if term in content_lower:
                concepts.append(term.title())
        
        return concepts[:5]  # Limit to top 5 concepts
    
    def _generate_learning_objectives(self, query: str, concepts: List[str]) -> List[str]:
        """Generate learning objectives based on the query and concepts."""
        objectives = [
            f"Understand the concept of {concepts[0] if concepts else 'the topic'}",
            "Apply the knowledge to real-world scenarios",
            "Identify key factors and considerations"
        ]
        
        if len(concepts) > 1:
            objectives.append(f"Recognize the relationship between {concepts[0]} and {concepts[1]}")
        
        return objectives
